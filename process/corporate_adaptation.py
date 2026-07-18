"""Deterministic validation for corporate-adaptation and pilot artifacts."""

from __future__ import annotations

import json
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from process.validators.config_validation import Diagnostic, pointer, secret_diagnostics


CONTRACTS = {
    "environment-inventory": "corporate-environment-inventory.schema.json",
    "configuration-checklist": "corporate-adaptation-checklist.schema.json",
    "pilot-entry-checklist": "corporate-adaptation-checklist.schema.json",
    "pilot-evidence": "corporate-pilot-evidence.schema.json",
    "no-fork-assessment": "corporate-no-fork-assessment.schema.json",
}

PACKAGE_DOCUMENTS = (
    "templates/corporate-adaptation/environment-inventory.yaml",
    "templates/corporate-adaptation/configuration-checklist.yaml",
    "templates/corporate-adaptation/pilot-entry-checklist.yaml",
    "templates/corporate-adaptation/pilot-evidence.yaml",
    "templates/corporate-adaptation/no-fork-assessment.yaml",
    "examples/corporate-adaptation/pilot-evidence-synthetic.yaml",
    "examples/corporate-adaptation/no-fork-routed-synthetic.yaml",
)

_EMAIL = re.compile(r"(?i)\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b")
_URL = re.compile(r"(?i)https?://[^\s\]}>,]+")
_IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
_ABSOLUTE_PATH = re.compile(r"(?i)(?:\b[a-z]:[\\/]|\\\\users\\|/(?:users|home)/)")
_UNC_PATH = re.compile(r"\\\\[a-z0-9$_.-]+[\\/]", re.IGNORECASE)
_INTERNAL_HOST = re.compile(r"(?i)\b(?:[a-z0-9-]+\.)+(?:corp|internal|local|lan)\b")
_PRODUCTION_ID = re.compile(r"(?i)\b[a-z0-9]+-(?:prod|corp|internal)-[a-z0-9-]+\b")
_URL_SCHEME = re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^\s\]}>,]+")
_SENSITIVE_EXTERNAL_KEYS = {
    "canonical_external_source",
    "configuration_revision",
    "internal_process_package_changes",
    "version_or_configuration",
}


@dataclass
class AdaptationResult:
    kind: str = "unknown"
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def exit_code(self) -> int:
        if not self.diagnostics:
            return 0
        return 3 if any(item.category == "operational" for item in self.diagnostics) else 1

    def as_payload(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "status": "valid" if not self.diagnostics else (
                "error" if self.exit_code == 3 else "invalid"
            ),
            "kind": self.kind,
            "diagnostics": [item.as_dict() for item in self.sorted_diagnostics()],
        }

    def sorted_diagnostics(self) -> list[Diagnostic]:
        return sorted(
            self.diagnostics,
            key=lambda item: (item.stage, item.code, item.source or "", item.pointer or ""),
        )


def _schema_diagnostics(document: Any, kind: str, process_root: Path) -> list[Diagnostic]:
    schema_name = CONTRACTS.get(kind)
    if schema_name is None:
        return [Diagnostic(
            "adaptation.kind-unsupported", "schema",
            "Document kind is missing or unsupported.", 1, source="document", pointer="/kind",
        )]
    try:
        schema = json.loads((process_root / "schemas" / schema_name).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return [Diagnostic(
            "adaptation.schema-unavailable", "operational",
            "The bundled adaptation schema is missing or malformed.", 1, source=schema_name,
        )]
    return [
        Diagnostic(
            "adaptation.schema-invalid", "schema",
            f"Document does not satisfy the {kind} contract ({error.validator}).",
            1, source="document", pointer=pointer(error.absolute_path),
        )
        for error in sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(document),
            key=lambda item: (list(item.absolute_path), item.message),
        )
    ]


def _private_value_diagnostics(document: Any, kind: str) -> list[Diagnostic]:
    findings: list[Diagnostic] = []

    def add(parts: list[Any], message: str) -> None:
        findings.append(Diagnostic(
            "adaptation.private-value", "privacy", message, 3,
            source="document", pointer=pointer(parts),
            hint="Use null, unresolved status, or clearly synthetic values in the external package.",
        ))

    def identity_or_reference_field(parts: list[Any]) -> bool:
        key = str(parts[-1]) if parts else ""
        return (
            key in _SENSITIVE_EXTERNAL_KEYS
            or key.endswith(("_id", "_ids", "_ref", "_refs"))
        )

    def visit(value: Any, parts: list[Any], field_parts: list[Any] | None = None) -> None:
        field_parts = parts if field_parts is None else field_parts
        if isinstance(value, dict):
            for key, child in value.items():
                visit(child, [*parts, key], [*parts, key])
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, [*parts, index], field_parts)
        elif isinstance(value, str):
            if _EMAIL.search(value):
                add(parts, "Email addresses are not allowed in external templates or examples.")
            if _IPV4.search(value):
                add(parts, "Private or local IP addresses are not allowed in external templates or examples.")
            if _ABSOLUTE_PATH.search(value):
                add(parts, "User or host absolute paths are not allowed in external templates or examples.")
            if value.startswith("/") or _UNC_PATH.search(value):
                add(parts, "Absolute POSIX or UNC paths are not allowed in external templates or examples.")
            if _INTERNAL_HOST.search(value):
                add(parts, "Internal host names are not allowed in external templates or examples.")
            if _PRODUCTION_ID.search(value):
                add(parts, "Production-like identifiers are not allowed in external templates or examples.")
            for match in _URL_SCHEME.finditer(value):
                host = (urlparse(match.group(0)).hostname or "").casefold()
                scheme = urlparse(match.group(0)).scheme.casefold()
                if scheme not in {"http", "https"} or not host.endswith(".invalid"):
                    add(parts, "Real or non-reserved URLs are not allowed in external templates or examples.")
            if identity_or_reference_field(field_parts) and "synthetic" not in value.casefold():
                add(parts, "External identity and reference fields must use explicit synthetic values.")

    if isinstance(document, dict) and kind == "environment-inventory":
        inventory = document.get("inventory")
        def inspect_fact(value: Any, parts: list[Any]) -> None:
            if isinstance(value, dict):
                if "status" in value and (
                    value.get("status") != "unresolved"
                    or value.get("value") is not None
                    or value.get("evidence_refs") not in ([], None)
                ):
                    add(parts, "The external inventory template must keep environment facts unresolved and empty.")
                for key, child in value.items():
                    inspect_fact(child, [*parts, key])
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    inspect_fact(child, [*parts, index])
        inspect_fact(inventory, ["inventory"])

    visit(document, [])
    return list({(item.code, item.pointer): item for item in findings}.values())


def _semantic_diagnostics(document: Any, kind: str) -> list[Diagnostic]:
    if not isinstance(document, dict):
        return []
    findings: list[Diagnostic] = []
    if kind in {"configuration-checklist", "pilot-entry-checklist"} and document.get("status") == "green":
        checks = document.get("checks", {})
        allowed = {"verified"}
        if kind == "configuration-checklist":
            allowed_by_name = {"unresolved_inputs": {"verified", "not-applicable"}}
        else:
            allowed_by_name = {}
        if not isinstance(checks, dict) or any(
            not isinstance(check, dict)
            or check.get("status") not in allowed_by_name.get(name, allowed)
            for name, check in checks.items()
        ):
            findings.append(Diagnostic(
                "adaptation.green-checklist-incomplete", "readiness",
                "A green checklist requires every mandatory check to be verified.",
                4, source="document", pointer="/checks",
            ))
    findings_value = document.get("findings", [])
    recorded_changes = document.get("internal_process_package_changes", [])
    content_reports_fork = (
        document.get("internal_package_fork_detected") is True
        or bool(recorded_changes)
        or (
            isinstance(findings_value, list)
            and any(
                isinstance(row, dict) and row.get("internal_package_modified") is True
                for row in findings_value
            )
        )
    )
    if kind == "no-fork-assessment" and content_reports_fork:
        findings.append(Diagnostic(
            "adaptation.internal-fork-detected", "governance",
            "An internal process-package fork blocks a compliant no-fork result.",
            4, source="document", pointer="/internal_package_fork_detected",
        ))
    if kind == "pilot-evidence":
        decisions = document.get("human_decisions", [])
        decision_ids = [
            row.get("decision_id") for row in decisions if isinstance(row, dict)
        ] if isinstance(decisions, list) else []
        if len(decision_ids) != len(set(decision_ids)):
            findings.append(Diagnostic(
                "adaptation.decision-id-duplicate", "traceability",
                "Human decision identifiers must be unique within pilot evidence.",
                4, source="document", pointer="/human_decisions",
            ))
        gates = document.get("gates", {})
        if isinstance(gates, dict):
            known = {value for value in decision_ids if isinstance(value, str)}
            for gate_name, gate in gates.items():
                if not isinstance(gate, dict) or not isinstance(gate.get("decision_ref"), str):
                    continue
                reference = gate["decision_ref"]
                normalized = reference.removeprefix("decision:")
                if normalized not in known:
                    findings.append(Diagnostic(
                        "adaptation.decision-ref-missing", "traceability",
                        "Gate decision reference does not resolve to human_decisions.",
                        4, source="document", pointer=f"/gates/{gate_name}/decision_ref",
                    ))
    return findings


def validate_document(
    document: Any,
    kind: str,
    process_root: Path,
    *,
    external_package: bool = False,
) -> AdaptationResult:
    """Validate one adaptation document without mutating it or external state."""
    result = AdaptationResult(kind=str(kind))
    result.diagnostics.extend(_schema_diagnostics(document, str(kind), process_root))
    result.diagnostics.extend(secret_diagnostics(document, "document", stage=2))
    if external_package:
        result.diagnostics.extend(_private_value_diagnostics(document, str(kind)))
    result.diagnostics.extend(_semantic_diagnostics(document, str(kind)))
    unique = {
        (item.code, item.source, item.pointer): item for item in result.diagnostics
    }
    result.diagnostics = list(unique.values())
    return result


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _has_link_or_reparse_ancestor(process_root: Path, path: Path) -> bool:
    """Reject links/reparse points from the package root through the target."""
    try:
        root_info = os.lstat(process_root)
    except OSError:
        return True
    root_attributes = getattr(root_info, "st_file_attributes", 0)
    if stat.S_ISLNK(root_info.st_mode) or root_attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
        return True
    try:
        relative = path.relative_to(process_root)
    except ValueError:
        return True
    current = process_root
    for part in relative.parts:
        current = current / part
        try:
            info = os.lstat(current)
        except OSError:
            return True
        attributes = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            return True
    return False


def validate_package_templates(process_root: Path) -> AdaptationResult:
    """Validate the exact shipped adaptation templates and synthetic examples."""
    result = AdaptationResult(kind="corporate-adaptation-package")
    expected = set(PACKAGE_DOCUMENTS)
    adaptation_roots = (
        process_root / "templates" / "corporate-adaptation",
        process_root / "examples" / "corporate-adaptation",
    )
    discovered: set[str] = set()
    for root in adaptation_roots:
        if not root.exists() or _has_link_or_reparse_ancestor(process_root, root):
            result.diagnostics.append(Diagnostic(
                "adaptation.package-document-invalid", "operational",
                "An adaptation package root is missing, linked, or unsafe.",
                0, source=root.relative_to(process_root).as_posix(),
            ))
            continue
        discovered.update(
            path.relative_to(process_root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and path.suffix.casefold() in {".yaml", ".yml"}
        )
    if discovered != expected:
        result.diagnostics.append(Diagnostic(
            "adaptation.package-closure", "privacy",
            "The shipped adaptation document inventory differs from the closed contract.",
            0, source="corporate-adaptation-package",
        ))
    for relative in sorted(expected | discovered):
        path = process_root / relative
        try:
            if _has_link_or_reparse_ancestor(process_root, path) or not path.is_file():
                raise OSError("unsafe package document")
            document = _load_yaml(path)
        except (OSError, UnicodeError, yaml.YAMLError):
            result.diagnostics.append(Diagnostic(
                "adaptation.package-document-invalid", "operational",
                "A required package template or example is missing or malformed.",
                0, source=relative,
            ))
            continue
        kind = document.get("kind", "unknown") if isinstance(document, dict) else "unknown"
        checked = validate_document(
            document, str(kind), process_root, external_package=True
        )
        for item in checked.diagnostics:
            result.diagnostics.append(Diagnostic(
                item.code, item.category, item.message, item.stage,
                severity=item.severity, source=relative, pointer=item.pointer, hint=item.hint,
            ))
    return result
