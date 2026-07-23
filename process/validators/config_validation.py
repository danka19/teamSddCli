"""Pure diagnostics, schema, compatibility, and integrity checks."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


CONFIG_SCHEMA_VERSION = "1.1"
TOPOLOGY = "central-team-specs"
PACKAGE_ID = "sdd-process"
PACKAGE_VERSION = "0.3.5"
POLICY_SET_ID = "sdd-core"
POLICY_SET_VERSION = "1.0.0"
OPENSPEC_VERSION = "1.4.1"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    category: str
    message: str
    stage: int
    severity: str = "error"
    source: str | None = None
    pointer: str | None = None
    hint: str | None = None

    def as_dict(self) -> dict[str, str]:
        value = {
            "code": self.code,
            "category": self.category,
            "severity": self.severity,
            "message": self.message,
        }
        for key in ("source", "pointer", "hint"):
            item = getattr(self, key)
            if item is not None:
                value[key] = item
        return value


@dataclass
class ValidationResult:
    mode: str = "unknown"
    diagnostics: list[Diagnostic] = field(default_factory=list)
    runtime_version: str | None = None

    @property
    def exit_code(self) -> int:
        if not self.diagnostics:
            return 0
        return 3 if any(item.category == "operational" for item in self.diagnostics) else 1

    def add(self, *items: Diagnostic) -> None:
        self.diagnostics.extend(items)

    def sorted_diagnostics(self) -> list[Diagnostic]:
        return sorted(
            self.diagnostics,
            key=lambda item: (
                item.stage,
                item.code,
                item.source or "",
                item.pointer or "",
                item.message,
            ),
        )

    def as_payload(self) -> dict[str, Any]:
        status = "valid" if not self.diagnostics else (
            "error" if self.exit_code == 3 else "invalid"
        )
        return {
            "schema_version": "1.0",
            "status": status,
            "mode": self.mode,
            "diagnostics": [item.as_dict() for item in self.sorted_diagnostics()],
            "compatibility": {
                "config_schema_version": CONFIG_SCHEMA_VERSION,
                "topology": TOPOLOGY,
                "process_package": {"id": PACKAGE_ID, "version": PACKAGE_VERSION},
                "policy_set": {"id": POLICY_SET_ID, "version": POLICY_SET_VERSION},
                "openspec": {
                    "required": OPENSPEC_VERSION,
                    "runtime": self.runtime_version,
                },
            },
        }


def pointer(parts: Iterable[Any]) -> str:
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded) if encoded else ""


def _schema_registry(schema_resources: Mapping[str, Any]) -> Registry:
    registry = Registry()
    for name in sorted(schema_resources):
        schema = schema_resources[name]
        registry = registry.with_resource(
            name,
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
    return registry


def schema_diagnostics(
    schema_name: str,
    data: Any,
    source: str,
    *,
    stage: int,
    schema_resources: Mapping[str, Any],
) -> list[Diagnostic]:
    schema = schema_resources[schema_name]
    validator = Draft202012Validator(
        schema, registry=_schema_registry(schema_resources)
    )
    return [
        Diagnostic(
            "schema.invalid",
            "schema",
            f"Document does not satisfy the bundled schema ({error.validator}).",
            stage,
            source=source,
            pointer=pointer(error.absolute_path),
            hint="Correct the document to match the bundled schema.",
        )
        for error in sorted(
            validator.iter_errors(data),
            key=lambda error: (list(error.absolute_path), error.message),
        )
    ]


_CREDENTIAL_KEY = re.compile(
    r"^(?:password|passphrase|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)$",
    re.IGNORECASE,
)
_PEM_KEY = re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
_URI_USERINFO = re.compile(r"[a-z][a-z0-9+.-]*://[^\s/@:]+:[^\s/@]+@", re.IGNORECASE)
_TOKEN = re.compile(
    r"(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})"
)
_QUERY_SECRET = re.compile(
    r"[?&](?:password|passwd|token|access_token|api_key)=[^&#\s]+", re.IGNORECASE
)


def secret_diagnostics(data: Any, source: str, *, stage: int = 3) -> list[Diagnostic]:
    findings: list[Diagnostic] = []

    def visit(value: Any, parts: list[Any]) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_parts = [*parts, key]
                if _CREDENTIAL_KEY.fullmatch(str(key)) and child not in (None, "", [], {}):
                    findings.append(
                        Diagnostic(
                            "secret.inline-credential",
                            "security",
                            "Inline credential material is not allowed.",
                            stage,
                            source=source,
                            pointer=pointer(child_parts),
                            hint="Use approved ignored or managed secret storage.",
                        )
                    )
                    continue
                visit(child, child_parts)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, [*parts, index])
        elif isinstance(value, str):
            patterns = (
                ("secret.private-key", _PEM_KEY, "Private key material is not allowed."),
                ("secret.uri-userinfo", _URI_USERINFO, "URI userinfo credentials are not allowed."),
                ("secret.recognizable-token", _TOKEN, "Recognizable inline token material is not allowed."),
                ("secret.query-credential", _QUERY_SECRET, "Credentials in URI query parameters are not allowed."),
            )
            for code, pattern, message in patterns:
                if pattern.search(value):
                    findings.append(
                        Diagnostic(
                            code,
                            "security",
                            message,
                            stage,
                            source=source,
                            pointer=pointer(parts),
                            hint="Remove the inline value and use approved secret storage.",
                        )
                    )
    visit(data, [])
    unique = {(item.code, item.source, item.pointer): item for item in findings}
    return list(unique.values())


def config_compatibility(data: Any) -> list[Diagnostic]:
    if not isinstance(data, dict):
        return []
    expected = (
        ("config_schema_version", data.get("config_schema_version"), CONFIG_SCHEMA_VERSION, "compat.config-schema"),
        ("topology", data.get("topology"), TOPOLOGY, "compat.topology"),
        ("process_package/id", _nested(data, "process_package", "id"), PACKAGE_ID, "compat.package-id"),
        ("process_package/version", _nested(data, "process_package", "version"), PACKAGE_VERSION, "compat.package-version"),
        ("openspec/cli_version", _nested(data, "openspec", "cli_version"), OPENSPEC_VERSION, "compat.openspec-pin"),
        ("policy_set/id", _nested(data, "policy_set", "id"), POLICY_SET_ID, "compat.policy-set-id"),
        ("policy_set/version", _nested(data, "policy_set", "version"), POLICY_SET_VERSION, "compat.policy-set-version"),
    )
    return [
        Diagnostic(
            code,
            "compatibility",
            f"Unsupported value; required value is {required}.",
            7,
            source="central-config",
            pointer=f"/{path}",
            hint="Use the exact version and topology certified by this package.",
        )
        for path, actual, required, code in expected
        if actual is not None and str(actual) != required
    ]


def adapter_compatibility(data: Any) -> list[Diagnostic]:
    if not isinstance(data, dict):
        return []
    expected = (
        ("schema_version", data.get("schema_version"), CONFIG_SCHEMA_VERSION, "compat.adapter-schema"),
        ("config_schema_version", data.get("config_schema_version"), CONFIG_SCHEMA_VERSION, "compat.adapter-config-schema"),
        ("process_package/id", _nested(data, "process_package", "id"), PACKAGE_ID, "compat.adapter-package-id"),
        ("process_package/version", _nested(data, "process_package", "version"), PACKAGE_VERSION, "compat.adapter-package-version"),
        ("policy_set/id", _nested(data, "policy_set", "id"), POLICY_SET_ID, "compat.adapter-policy-set-id"),
        ("policy_set/version", _nested(data, "policy_set", "version"), POLICY_SET_VERSION, "compat.adapter-policy-set-version"),
    )
    return [
        Diagnostic(
            code,
            "compatibility",
            f"Adapter value is incompatible; required value is {required}.",
            7,
            source="project-adapter",
            pointer=f"/{path}",
        )
        for path, actual, required, code in expected
        if actual is not None and str(actual) != required
    ]


def package_compatibility(
    config: dict[str, Any], package: dict[str, Any], workflow: dict[str, Any], version: str,
    adapter: dict[str, Any] | None,
) -> list[Diagnostic]:
    values = (
        ("compat.package-id", _nested(package, "package", "id"), PACKAGE_ID, "process-package", "/package/id"),
        ("compat.package-version", _nested(package, "package", "version"), PACKAGE_VERSION, "process-package", "/package/version"),
        ("compat.config-package-version", _nested(config, "process_package", "version"), _nested(package, "package", "version"), "central-config", "/process_package/version"),
        ("compat.version-file", version, _nested(package, "package", "version"), "package-version", ""),
        ("compat.package-openspec-pin", _nested(package, "openspec", "cli_version"), OPENSPEC_VERSION, "process-package", "/openspec/cli_version"),
        ("compat.config-openspec-pin", _nested(config, "openspec", "cli_version"), _nested(package, "openspec", "cli_version"), "central-config", "/openspec/cli_version"),
        ("compat.workflow-topology", _nested(workflow, "workflow", "topology"), TOPOLOGY, "process-workflow", "/workflow/topology"),
        ("compat.config-policy-set-id", _nested(config, "policy_set", "id"), POLICY_SET_ID, "central-config", "/policy_set/id"),
        ("compat.config-policy-set-version", _nested(config, "policy_set", "version"), POLICY_SET_VERSION, "central-config", "/policy_set/version"),
    )
    diagnostics = [
        Diagnostic(
            code,
            "compatibility",
            "Version, identifier, or topology does not match the certified package contract.",
            7,
            source=source,
            pointer=path,
            hint="Align config, adapter, package metadata, workflow, and VERSION exactly.",
        )
        for code, actual, required, source, path in values
        if actual is not None and required is not None and str(actual) != str(required)
    ]
    if adapter is not None:
        for key in ("id", "version"):
            if _nested(adapter, "process_package", key) != _nested(config, "process_package", key):
                diagnostics.append(
                    Diagnostic(
                        f"compat.adapter-package-{key}",
                        "compatibility",
                        "Adapter and central config consume different process packages.",
                        7,
                        source="project-adapter",
                        pointer=f"/process_package/{key}",
                    )
                )
        for key in ("id", "version"):
            if _nested(adapter, "policy_set", key) != _nested(config, "policy_set", key):
                diagnostics.append(
                    Diagnostic(
                        f"compat.adapter-policy-set-{key}",
                        "compatibility",
                        "Adapter and central config consume different policy sets.",
                        7,
                        source="project-adapter",
                        pointer=f"/policy_set/{key}",
                    )
                )
    return diagnostics


def integrity_diagnostics(
    projects: dict[str, Any], owners: dict[str, Any], adapter: dict[str, Any] | None
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    project_rows = projects.get("projects", [])
    group_rows = owners.get("owner_groups", [])
    zone_rows = owners.get("zones", [])
    project_ids = _unique_ids(project_rows, "project", diagnostics)
    group_ids = _unique_ids(group_rows, "owner-group", diagnostics)
    zone_ids = _unique_ids(zone_rows, "owner-zone", diagnostics)

    for index, project in enumerate(project_rows):
        for zone in project.get("owner_zones", []):
            if zone not in zone_ids:
                diagnostics.append(Diagnostic(
                    "integrity.project-owner-zone", "integrity",
                    "Project references an unknown owner zone.", 8,
                    source="projects-registry", pointer=f"/projects/{index}/owner_zones",
                ))
    for index, zone in enumerate(zone_rows):
        for group in zone.get("owner_groups", []):
            if group not in group_ids:
                diagnostics.append(Diagnostic(
                    "integrity.owner-zone-group", "integrity",
                    "Owner zone references an unknown owner group.", 8,
                    source="owners-registry", pointer=f"/zones/{index}/owner_groups",
                ))
    for group in owners.get("default_owner_groups", []):
        if group not in group_ids:
            diagnostics.append(Diagnostic(
                "integrity.default-owner-group", "integrity",
                "Default owner group is not registered.", 8,
                source="owners-registry", pointer="/default_owner_groups",
            ))
    if adapter is not None:
        project_id = adapter.get("project_id")
        matches = [row for row in project_rows if row.get("id") == project_id]
        if project_id not in project_ids:
            diagnostics.append(Diagnostic(
                "integrity.adapter-project", "integrity",
                "Adapter project is not present in the central project registry.", 8,
                source="project-adapter", pointer="/project_id",
            ))
        elif matches and not matches[0].get("adapter_allowed"):
            diagnostics.append(Diagnostic(
                "integrity.adapter-not-allowed", "integrity",
                "The registered project does not allow a project adapter.", 8,
                source="project-adapter", pointer="/project_id",
            ))
    return diagnostics


def _unique_ids(rows: Any, kind: str, diagnostics: list[Diagnostic]) -> set[str]:
    seen: set[str] = set()
    if not isinstance(rows, list):
        return seen
    for index, row in enumerate(rows):
        identifier = row.get("id") if isinstance(row, dict) else None
        if isinstance(identifier, str) and identifier in seen:
            diagnostics.append(Diagnostic(
                "integrity.duplicate-id", "integrity", f"Duplicate {kind} identifier.", 8,
                pointer=f"/{index}/id",
            ))
        elif isinstance(identifier, str):
            seen.add(identifier)
    return seen


def _nested(value: Any, *keys: str) -> Any:
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value
