"""Deterministic construction and validation of immutable transfer candidates."""

from __future__ import annotations

import hashlib
import copy
import json
import os
import errno
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .actual_certification import validate_normalized_evidence, validate_phase_gate
from .errors import OperationError
from .validators.config_validation import secret_diagnostics
from .validators.classification_migration import apply_migration, plan_migration
from .validators.config_discovery import validate_configuration
from .workflow_operations import (
    bootstrap_team_specs,
    create_change,
    rollback_process_package,
    update_process_package,
)


_RELEASE_ID = re.compile(r"^[a-z][a-z0-9.-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DRIVE = re.compile(r"^[A-Za-z]:")
_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
_REPARSE_POINT = 0x400
_MUTABLE_EVIDENCE_PARTS = {("process", "release", "evidence"), (".superpowers",), ("tests",)}
_RUNBOOKS = (
    "ARTIFACT_AND_LIFECYCLE_GATES.md", "CERTIFICATION_EVIDENCE.md",
    "CLASSIFICATION_AND_MIGRATION.md", "CORPORATE_FLOW_CONTROLS.md",
    "PACKAGED_GOVERNED_FLOW.md", "PROCESS_PACKAGE_SETUP.md",
    "TECH_LEAD_GOVERNANCE.md", "TRANSFER_RELEASE_CANDIDATE.md",
    "WEAK_MODEL_OPERATING_KIT.md",
    "CORPORATE_ADAPTATION_AND_PILOT.md",
    "GUIDED_OWNER_WORKFLOW.md",
)
_ENTRY_POINTS = (
    ("bootstrap_team_specs.py", ("scripts/bootstrap_team_specs.py", "--help"), (0,)),
    ("check_corporate_flow.py", ("scripts/check_corporate_flow.py", "--help"), (2,)),
    ("check_lifecycle_transition.py", ("scripts/check_lifecycle_transition.py", "--help"), (0,)),
    ("check_tech_lead_control.py", ("scripts/check_tech_lead_control.py", "--help"), (2,)),
    ("classify_change.py", ("scripts/classify_change.py", "--help"), (0,)),
    ("create_change.py", ("scripts/create_change.py", "--help"), (0,)),
    ("evaluate_change_gates.py", ("scripts/evaluate_change_gates.py", "--help"), (0,)),
    ("guided_owner_workflow.py", ("scripts/guided_owner_workflow.py", "--help"), (0,)),
    ("sdd.py", ("scripts/sdd.py", "--help"), (0,)),
    ("manage_release_candidate.py", ("scripts/manage_release_candidate.py", "validate", "--help"), (0,)),
    ("manual_fallback.py", ("scripts/manual_fallback.py", "--help"), (0,)),
    ("migrate_change_classification.py", ("scripts/migrate_change_classification.py", "--help"), (0,)),
    ("prepare_archive.py", ("scripts/prepare_archive.py", "--help"), (0,)),
    ("prepare_spec_pr.py", ("scripts/prepare_spec_pr.py", "--help"), (0,)),
    ("review_tech_lead.py", ("scripts/review_tech_lead.py", "--help"), (2,)),
    ("update_process_package.py", ("scripts/update_process_package.py", "--help"), (0,)),
    ("validate_change.py", ("scripts/validate_change.py", "--help"), (0,)),
    ("validate_corporate_adaptation.py", ("scripts/validate_corporate_adaptation.py", "--help"), (0,)),
    ("validate_external_mapping.py", ("scripts/validate_external_mapping.py", "--help"), (0,)),
    ("validate_guided_owner_workflow.py", ("scripts/validate_guided_owner_workflow.py", "--help"), (0,)),
    ("validate_process_config.py", ("scripts/validate_process_config.py", "--help"), (0,)),
    ("validate_traceability.py", ("scripts/validate_traceability.py", "--help"), (0,)),
)
_HOST_EVIDENCE = [
    {"platform_id": "windows", "evidence_level": "full-clean-rehearsal"},
    {"platform_id": "linux-wsl2", "evidence_level": "portability-smoke"},
    {"platform_id": "macos", "evidence_level": "not-certified"},
]
_VERIFICATION_COMMANDS = [
    "python -m pytest tests/test_release_candidate.py tests/test_process_package.py -q",
    "python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py tests/test_packaged_flow_cli.py -q",
]
_EVIDENCE_REQUIREMENTS = [
    "windows-full-clean-rehearsal", "linux-wsl2-portability-smoke", "negative-acceptance-cases"
]
_ROLLBACK_REFERENCE = "docs/runbooks/PROCESS_PACKAGE_SETUP.md"
_SELECTION_FILE = "release-certification-selection.yaml"
_AI_CONTRACT_PATHS = {
    "qwen-class": (
        "process/adapters/qwen-class.yaml",
        "process/certification/qwen-matrix.yaml",
        "process/model_adapter.py",
        "process/operation_plan.py",
        "process/roles/analyst.md",
        "process/roles/developer.md",
        "process/roles/qa.md",
        "process/roles/tech-lead.md",
        "process/schemas/weak-model-operation-evidence.schema.json",
    ),
    "deepseek-class": (
        "process/adapters/deepseek-class.yaml",
        "process/certification/qwen-matrix.yaml",
        "process/model_adapter.py",
        "process/operation_plan.py",
        "process/roles/analyst.md",
        "process/roles/developer.md",
        "process/roles/qa.md",
        "process/roles/tech-lead.md",
        "process/schemas/weak-model-operation-evidence.schema.json",
    ),
}
_HOST_FILES = {"windows.yaml": ("windows", "full-clean-rehearsal"), "linux-wsl2.yaml": ("linux-wsl2", "portability-smoke")}
_WINDOWS_SCENARIOS = {
    "clean-bootstrap", "config-compatibility", "minor-flow", "major-flow", "hotfix-flow",
    "migration-check", "migration-apply", "migration-idempotent", "update",
    "failed-update-hold", "rollback", "archive-history-preserved",
    "negative-acceptance-cases", "ai-disabled",
}
_LINUX_SCENARIOS = {
    "clean-bootstrap", "config-compatibility", "class-flow-smoke", "migration-smoke",
    "update-rollback-smoke", "negative-acceptance-cases", "ai-disabled",
}
_SCENARIO_CODES = {"migration-ok", "update-ok", "failed-update-held", "rollback-ok", "archive-unchanged"}


def _validate_baseline_reuse(
    selected: Mapping[str, Any], payload: Path, raw_root: Path
) -> list[str]:
    """Validate a successor's immutable matrix reference and current preflight."""
    family = selected.get("model_family")
    expected_paths = _AI_CONTRACT_PATHS.get(family)
    if expected_paths is None:
        return ["release.baseline-reuse-invalid"]
    hashes = selected.get("ai_contract_hashes")
    if not isinstance(hashes, list):
        return ["release.baseline-reuse-invalid"]
    declared = {
        item.get("path"): item.get("sha256")
        for item in hashes
        if isinstance(item, Mapping)
        and isinstance(item.get("path"), str)
        and isinstance(item.get("sha256"), str)
    }
    if set(declared) != set(expected_paths) or not all(_SHA256.fullmatch(value) for value in declared.values()):
        return ["release.baseline-reuse-invalid"]
    for relative in expected_paths:
        source = payload / relative
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != declared[relative]:
            return ["release.ai-contract-hash-mismatch"]

    baseline = selected.get("baseline")
    fresh = selected.get("fresh_preflight")
    if not isinstance(baseline, Mapping) or not isinstance(fresh, Mapping):
        return ["release.baseline-reuse-invalid"]
    baseline_path = baseline.get("normalized_evidence_path")
    baseline_hash = baseline.get("normalized_evidence_sha256")
    baseline_root = baseline.get("raw_logical_root")
    if not isinstance(baseline_path, str) or not isinstance(baseline_hash, str) or not isinstance(baseline_root, str):
        return ["release.baseline-reuse-invalid"]
    try:
        validate_portable_path(baseline_path)
        evidence_file = payload / "process" / baseline_path
        baseline_bytes = evidence_file.read_bytes()
        baseline_evidence = _load_mapping(evidence_file, "release.certification-evidence-invalid")
    except (OperationError, OSError):
        return ["release.baseline-evidence-missing"]
    if hashlib.sha256(baseline_bytes).hexdigest() != baseline_hash:
        return ["release.baseline-evidence-hash-mismatch"]
    if (
        baseline_evidence.get("status") != "passed"
        or baseline_evidence.get("raw_artifact", {}).get("logical_id") != baseline_root
        or not (raw_root / baseline_root).is_dir()
    ):
        return ["release.baseline-evidence-invalid"]
    if _contains_private(baseline_evidence):
        return ["release.evidence-private"]

    fresh_root = fresh.get("raw_logical_root")
    result_path = fresh.get("result_path")
    result_hash = fresh.get("result_sha256")
    adapter_version = fresh.get("adapter_version")
    if not all(isinstance(value, str) for value in (fresh_root, result_path, result_hash, adapter_version)):
        return ["release.baseline-reuse-invalid"]
    try:
        validate_portable_path(result_path)
        result_file = raw_root / fresh_root / result_path
        result_bytes = result_file.read_bytes()
        summary = json.loads(result_bytes)
    except (OSError, json.JSONDecodeError):
        return ["release.fresh-preflight-missing"]
    if hashlib.sha256(result_bytes).hexdigest() != result_hash:
        return ["release.fresh-preflight-hash-mismatch"]
    diagnostics = validate_phase_gate(
        summary, raw_root / fresh_root, "preflight", family, adapter_version, 5
    )
    if diagnostics:
        return ["release.fresh-preflight-failed"]
    return []


def _synthetic_upgrade_evidence(from_version: str, to_version: str) -> dict[str, Any]:
    """Build bounded rehearsal evidence; production callers supply their reviewed record."""
    return {
        "schema_version": "1.0",
        "change_id": "release-rehearsal-upgrade",
        "review": {
            "owner_type": "human",
            "state": "approved",
            "decision_ref": "decisions/release-rehearsal-upgrade.yaml",
        },
        "from": {"package_version": from_version, "openspec_version": "1.4.1"},
        "to": {"package_version": to_version, "openspec_version": "1.4.1"},
        "checks": {
            "compatibility_evidence_refs": ["evidence/release-rehearsal-compatibility.json"],
            "openspec_strict": {
                "status": "passed",
                "evidence_ref": "evidence/release-rehearsal-openspec.txt",
            },
            "validator_templates": {
                "status": "passed",
                "evidence_ref": "evidence/release-rehearsal-package-tests.txt",
            },
        },
        "rollback_or_hold": {
            "strategy": "rollback",
            "instructions": "Restore the retained package snapshot and configuration pin.",
        },
        "evidence_sha256": {},
    }


def _materialize_synthetic_upgrade_evidence(
    root: Path, process_root: Path, from_version: str, to_version: str
) -> Path:
    """Create checksum-bound synthetic rehearsal inputs outside the candidate payload."""
    document = _synthetic_upgrade_evidence(from_version, to_version)
    root.mkdir(parents=True, exist_ok=False)
    change = _load_mapping(
        process_root / "templates" / "change-v2" / "change.yaml",
        "release.rehearsal-failed",
    )
    change["id"] = document["change_id"]
    change["decision"]["state"] = "confirmed"
    (root / "change.yaml").write_text(
        yaml.safe_dump(change, sort_keys=False), encoding="utf-8", newline="\n"
    )
    (root / "proposal.md").write_text("# Reviewed rehearsal upgrade\n", encoding="utf-8", newline="\n")
    (root / "tasks.md").write_text("# Tasks\n\n- [x] Verify rehearsal upgrade.\n", encoding="utf-8", newline="\n")
    delta = root / change["spec_change"]["delta_paths"][0]
    delta.parent.mkdir(parents=True, exist_ok=True)
    delta.write_text("## MODIFIED Requirements\n", encoding="utf-8", newline="\n")
    references = [
        document["review"]["decision_ref"],
        *document["checks"]["compatibility_evidence_refs"],
        document["checks"]["openspec_strict"]["evidence_ref"],
        document["checks"]["validator_templates"]["evidence_ref"],
    ]
    for reference in references:
        path = root / reference
        path.parent.mkdir(parents=True, exist_ok=True)
        if reference == document["review"]["decision_ref"]:
            kind, status, producer = "human-decision", "approved", "human"
        elif reference in document["checks"]["compatibility_evidence_refs"]:
            kind, status, producer = "compatibility", "compatible", "deterministic-validator"
        elif reference == document["checks"]["openspec_strict"]["evidence_ref"]:
            kind, status, producer = "openspec-strict", "passed", "deterministic-validator"
        else:
            kind, status, producer = "validator-templates", "passed", "deterministic-validator"
        path.write_text(yaml.safe_dump({
            "schema_version": "1.0", "evidence_kind": kind,
            "change_id": document["change_id"], "from": document["from"], "to": document["to"],
            "status": status, "produced_by": producer,
        }, sort_keys=False), encoding="utf-8", newline="\n")
        document["evidence_sha256"][reference] = hashlib.sha256(path.read_bytes()).hexdigest()
    evidence_path = root / "upgrade-evidence.yaml"
    evidence_path.write_text(
        yaml.safe_dump(document, sort_keys=False), encoding="utf-8", newline="\n"
    )
    return evidence_path


def _next_minor_version(version: str) -> str:
    major, minor, _patch = (int(part) for part in version.split("."))
    return f"{major}.{minor + 1}.0"
_NEGATIVE_ACCEPTANCE = {
    "missing": "evidence-missing",
    "stale": "evidence-stale",
    "failed": "evidence-failed",
    "private": "evidence-private",
    "ai-only": "evidence-ai-only",
    "checksum-mismatch": "evidence-checksum-mismatch",
    "payload-mismatch": "candidate-digest-mismatch",
}
_INVENTORY_ARGV = [
    ["python", "--version"], ["node", "--version"], ["openspec", "--version"],
    ["git", "--version"], ["python", "-c", "import platform;print(platform.platform())"],
]
_PRIVATE_TEXT = re.compile(r"(?i)(?:(?<![a-z0-9])[a-z]:[\\/]|/users/|\\\\users\\|https?://(?!127\.0\.0\.1|localhost)|api[_-]?key\s*[=:]|sk-[a-z0-9_-]{12,})")


@dataclass(frozen=True)
class ReleaseInputs:
    release_id: str
    known_limitations: tuple[str, ...]
    raw_artifact_root: Path


@dataclass(frozen=True)
class RehearsalOptions:
    platform_id: str
    evidence_level: str
    mcp_status: str
    mcp_evidence_ref: str | None
    output: Path


def evaluate_release_acceptance(
    candidate_root: Path,
    manifest: Mapping[str, Any],
    host_evidence_root: Path,
    raw_artifact_root: Path,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    diagnostics: list[str] = []

    def reject(code: str) -> None:
        if code not in diagnostics:
            diagnostics.append(code)

    try:
        validation = validate_release_manifest(candidate_root, manifest)
        candidate = _safe_directory_root(candidate_root, "release.candidate-missing")
        payload = _safe_directory_root(candidate / "payload", "release.payload-missing")
    except OperationError as error:
        reject("candidate-digest-mismatch" if "manifest" in error.code or "payload" in error.code else error.code)
        return _acceptance_result(manifest, diagnostics)
    if validation["payload_sha256"] != manifest.get("payload_sha256"):
        reject("candidate-digest-mismatch")
    manifest_sha = hashlib.sha256((candidate / "release-manifest.yaml").read_bytes()).hexdigest()
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None or current.utcoffset() is None:
        reject("evidence-time-invalid")
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)

    try:
        host_root = _safe_directory_root(host_evidence_root, "release.host-evidence-missing")
        entries = {path.name for path in host_root.iterdir()}
    except OperationError:
        reject("evidence-missing")
        return _acceptance_result(manifest, diagnostics)
    for code in _validate_host_root_closure(entries):
        reject(code)
    host_schema = payload / "process/schemas/release-host-evidence.schema.json"
    for filename, (platform_id, evidence_level) in _HOST_FILES.items():
        path = host_root / filename
        if not path.is_file() or _is_link_or_reparse(path):
            reject("evidence-missing")
            continue
        try:
            row = _load_mapping(path, "release.host-evidence-invalid")
        except OperationError:
            reject("evidence-failed")
            continue
        for code in _validate_host_evidence_row(
            row, platform_id, evidence_level, manifest, manifest_sha, current, host_schema
        ):
            reject(code)

    try:
        raw_root = _safe_directory_root(raw_artifact_root, "release.raw-artifacts-invalid")
        declared = {item["reference"]: item["sha256"] for item in manifest.get("raw_artifacts", [])}
        actual: dict[str, str] = {}
        for path in sorted(raw_root.rglob("*")):
            if _is_link_or_reparse(path):
                raise OperationError("release.link-forbidden", "raw artifact links are forbidden")
            if path.is_file():
                relative = path.relative_to(raw_root).as_posix()
                validate_portable_path(relative)
                actual[f"artifact:{relative}"] = hashlib.sha256(path.read_bytes()).hexdigest()
                if _contains_private_bytes(path.read_bytes()):
                    reject("evidence-private")
        for code in _validate_raw_artifact_closure(declared, actual):
            reject(code)
    except (OperationError, OSError):
        reject("evidence-checksum-mismatch")
        return _acceptance_result(manifest, diagnostics)

    try:
        selection = _load_mapping(payload / f"process/{_SELECTION_FILE}", "release.certification-selection-invalid")
        _validate_schema(
            selection,
            payload / "process/schemas/release-certification-selection.schema.json",
            "release.certification-selection-invalid",
        )
        for selected in selection["selected"]:
            if selected["mode"] == "baseline-reuse":
                baseline_version = selected["baseline"]["process_package_version"]
                current_version = manifest["process_package"]["version"]
                if baseline_version == current_version:
                    reject("evidence-failed")
                    continue
                for code in _validate_baseline_reuse(selected, payload, raw_root):
                    reject("evidence-private" if code == "release.evidence-private" else "evidence-failed")
                continue
            logical_root = selected["raw_logical_root"]
            evidence_path = selected["normalized_evidence_path"]
            validate_portable_path(evidence_path)
            evidence = _load_mapping(payload / "process" / evidence_path, "release.certification-evidence-invalid")
            if evidence.get("status") != "passed" or evidence.get("raw_artifact", {}).get("logical_id") != logical_root:
                reject("evidence-failed")
                continue
            artifact_path = raw_root / logical_root
            if not artifact_path.is_dir():
                reject("evidence-missing")
                continue
            if _contains_private(evidence):
                reject("evidence-private")
            if validate_normalized_evidence(evidence, artifact_path, repository_root=payload):
                reject("evidence-failed")
    except OperationError:
        reject("evidence-missing")
    return _acceptance_result(manifest, diagnostics)


def _validate_host_root_closure(entries: Any) -> list[str]:
    if not isinstance(entries, set) or not all(isinstance(item, str) for item in entries):
        return ["evidence-invalid"]
    if entries == set(_HOST_FILES):
        return []
    return ["evidence-missing" if not set(_HOST_FILES) <= entries else "evidence-root-not-closed"]


def _validate_host_evidence_row(
    row: Any,
    platform_id: str,
    evidence_level: str,
    manifest: Mapping[str, Any],
    manifest_sha: str,
    current: datetime,
    schema_path: Path,
    *,
    require_negative_matrix: bool = True,
) -> list[str]:
    diagnostics: list[str] = []

    def add(code: str) -> None:
        if code not in diagnostics:
            diagnostics.append(code)

    if not isinstance(row, Mapping):
        return ["evidence-invalid"]
    if row.get("platform_id") != platform_id or row.get("evidence_level") != evidence_level:
        add("evidence-root-not-closed")
    if row.get("result") != "passed":
        add("evidence-failed")
    if row.get("ai_disabled") is not True or row.get("human_authority_substituted") is not False:
        add("evidence-ai-only")
    mcp = row.get("mcp")
    if not _mcp_consistent(mcp):
        add("evidence-mcp-inconsistent")
    try:
        _validate_schema(row, schema_path, "release.host-evidence-invalid")
    except OperationError:
        add("evidence-invalid")
        if _contains_private(row):
            add("evidence-private")
        return diagnostics
    if row.get("payload_sha256") != manifest.get("payload_sha256") or row.get("manifest_sha256") != manifest_sha:
        add("candidate-digest-mismatch")
    package = manifest.get("process_package")
    package_version = package.get("version") if isinstance(package, Mapping) else None
    if row.get("process_package_version") != package_version or row.get("config_schema_version") != manifest.get("config_schema_version"):
        add("incompatible-dependency")
    if not _inventory_compatible(row.get("inventory"), manifest.get("compatibility")):
        add("incompatible-dependency")
    commands = row.get("inventory_commands")
    if not isinstance(commands, list) or [item.get("argv") for item in commands if isinstance(item, Mapping)] != _INVENTORY_ARGV:
        add("incompatible-dependency")
    completed = _canonical_completed_at(row.get("completed_at"))
    if completed is None:
        add("evidence-failed")
    elif completed > current:
        add("evidence-future")
    elif (current - completed).total_seconds() > 30 * 86400:
        add("evidence-stale")
    required_scenarios = _WINDOWS_SCENARIOS if platform_id == "windows" else _LINUX_SCENARIOS
    scenario_ids = row.get("scenario_ids")
    if not isinstance(scenario_ids, list) or set(scenario_ids) != required_scenarios:
        add("evidence-failed")
    scenario_codes = row.get("scenario_codes")
    codes = set(scenario_codes) if isinstance(scenario_codes, list) else set()
    if not _SCENARIO_CODES <= codes:
        add("failed-update-hold" if "failed-update-held" not in codes else "evidence-failed")
    if row.get("archive_digest_before") != row.get("archive_digest_after"):
        add("archive-history-rewrite")
    if row.get("rollback_result") != "passed":
        add("failed-update-hold")
    if require_negative_matrix and not _negative_matrix_complete(row.get("negative_acceptance_cases")):
        add("evidence-failed")
    if _contains_private(row):
        add("evidence-private")
    return diagnostics


def _mcp_consistent(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    status = value.get("status")
    reference = value.get("evidence_ref")
    if status == "explicitly-unavailable":
        return reference is None
    if status != "provisioned" or not isinstance(reference, str):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{0,255}", reference)) and ".." not in reference


def _negative_matrix_complete(value: Any) -> bool:
    if not isinstance(value, list) or len(value) != len(_NEGATIVE_ACCEPTANCE):
        return False
    by_id = {
        item.get("case_id"): item for item in value
        if isinstance(item, Mapping) and isinstance(item.get("case_id"), str)
    }
    if set(by_id) != set(_NEGATIVE_ACCEPTANCE):
        return False
    return all(
        item.get("expected_code") == expected
        and item.get("result") == "passed"
        and isinstance(item.get("observed_codes"), list)
        and expected in item["observed_codes"]
        for case_id, expected in _NEGATIVE_ACCEPTANCE.items()
        for item in (by_id[case_id],)
    )


def _validate_raw_artifact_closure(declared: Any, actual: Any) -> list[str]:
    if not isinstance(declared, Mapping) or not isinstance(actual, Mapping):
        return ["evidence-invalid"]
    return [] if dict(actual) == dict(declared) else ["evidence-checksum-mismatch"]


def _run_negative_acceptance_matrix(
    base_row: Mapping[str, Any],
    manifest: Mapping[str, Any],
    manifest_sha: str,
    current: datetime,
    schema_path: Path,
) -> list[dict[str, Any]]:
    validation_base = copy.deepcopy(dict(base_row))
    scenario_ids = validation_base.get("scenario_ids")
    if isinstance(scenario_ids, list) and "negative-acceptance-cases" not in scenario_ids:
        scenario_ids.append("negative-acceptance-cases")
    rows: list[dict[str, Any]] = []
    for case_id, expected in _NEGATIVE_ACCEPTANCE.items():
        if case_id == "missing":
            observed = _validate_host_root_closure({"windows.yaml"})
        elif case_id == "checksum-mismatch":
            observed = _validate_raw_artifact_closure(
                {"artifact:synthetic/result.json": "a" * 64},
                {"artifact:synthetic/result.json": "b" * 64},
            )
        else:
            row = copy.deepcopy(validation_base)
            if case_id == "stale":
                row["completed_at"] = (current - timedelta(days=31)).strftime("%Y-%m-%dT%H:%M:%SZ")
            elif case_id == "failed":
                row["result"] = "failed"
            elif case_id == "private":
                row["mcp"] = {"status": "explicitly-unavailable", "evidence_ref": "api_key=sk-private-value-1234567890"}
            elif case_id == "ai-only":
                row["ai_disabled"] = False
            elif case_id == "payload-mismatch":
                row["payload_sha256"] = "b" * 64
            observed = _validate_host_evidence_row(
                row,
                str(validation_base.get("platform_id", "")),
                str(validation_base.get("evidence_level", "")),
                manifest,
                manifest_sha,
                current,
                schema_path,
                require_negative_matrix=False,
            )
        if expected not in observed:
            raise OperationError(
                "release.negative-acceptance-failed",
                "negative acceptance case did not observe its expected rejection",
            )
        rows.append({
            "case_id": case_id,
            "expected_code": expected,
            "observed_codes": observed,
            "result": "passed",
        })
    return rows


def _acceptance_result(manifest: Mapping[str, Any], diagnostics: list[str]) -> dict[str, Any]:
    return {
        "operation": "evaluate-release-acceptance",
        "status": "evidence-rejected" if diagnostics else "evidence-complete",
        "release_id": manifest.get("release_id"),
        "payload_sha256": manifest.get("payload_sha256"),
        "human_acceptance_required": True,
        "diagnostics": [{"code": code} for code in diagnostics],
    }


def _canonical_completed_at(value: Any) -> datetime | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _version_at_least(value: Any, minimum: str) -> bool:
    try:
        observed = tuple(int(part) for part in re.findall(r"\d+", str(value))[:2])
        required = tuple(int(part) for part in re.findall(r"\d+", minimum)[:2])
        return observed >= required
    except (TypeError, ValueError):
        return False


def _inventory_compatible(inventory: Any, compatibility: Any) -> bool:
    if not isinstance(inventory, dict) or not isinstance(compatibility, dict):
        return False
    return (
        _version_at_least(inventory.get("python"), compatibility.get("python", "3.11"))
        and _version_at_least(inventory.get("node"), compatibility.get("node", "20"))
        and _version_at_least(inventory.get("git"), compatibility.get("git", "2.40"))
        and str(inventory.get("openspec")) == str(compatibility.get("openspec"))
    )


def _contains_private(value: Any) -> bool:
    return bool(secret_diagnostics(value, "release-evidence")) or bool(
        _PRIVATE_TEXT.search(json.dumps(value, sort_keys=True))
    )


def _contains_private_bytes(data: bytes) -> bool:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        value = text
    return _contains_private(value)


def _host_evidence_id(release_id: str, platform_id: str) -> str:
    release_series = re.sub(r"-rc\d+$", "", release_id)
    return f"{release_series}-{platform_id}"


def rehearse_release_candidate(
    candidate_root: Path, workspace: Path, options: RehearsalOptions
) -> dict[str, Any]:
    if not isinstance(options, RehearsalOptions):
        raise OperationError("input-invalid", "rehearsal options must use the typed contract", exit_code=3)
    expected_level = {"windows": "full-clean-rehearsal", "linux-wsl2": "portability-smoke"}
    if expected_level.get(options.platform_id) != options.evidence_level:
        raise OperationError("input-invalid", "platform and evidence level are incompatible", exit_code=3)
    if not _mcp_consistent({"status": options.mcp_status, "evidence_ref": options.mcp_evidence_ref}):
        raise OperationError("input-invalid", "MCP observation is inconsistent", exit_code=3)

    candidate = _safe_directory_root(candidate_root, "release.candidate-missing")
    manifest = _load_mapping(candidate / "release-manifest.yaml", "release.manifest-file-invalid")
    validate_release_manifest(candidate, manifest)
    payload = _safe_directory_root(candidate / "payload", "release.payload-missing")
    requested_workspace = Path(os.path.abspath(workspace))
    requested_output = Path(os.path.abspath(options.output))
    _assert_existing_ancestry_safe(requested_workspace)
    _assert_existing_ancestry_safe(requested_output)
    for first, second in (
        (candidate, requested_workspace), (candidate, requested_output), (requested_workspace, requested_output)
    ):
        if first == second or first in second.parents or second in first.parents:
            raise OperationError("release.path-overlap", "candidate, workspace, and output must not overlap")
    if any(part.casefold() in {"archive", "accepted"} for part in requested_output.parts):
        raise OperationError("release.output-history-forbidden", "rehearsal output cannot enter accepted history")
    if os.path.lexists(requested_output):
        raise OperationError("release.output-exists", "rehearsal output must not exist")
    if requested_workspace.exists() and any(requested_workspace.iterdir()):
        raise OperationError("release.workspace-not-empty", "rehearsal workspace must be new or empty")
    requested_workspace.parent.mkdir(parents=True, exist_ok=True)
    requested_output.parent.mkdir(parents=True, exist_ok=True)

    try:
        inventory, inventory_commands = _observe_inventory()
        bootstrap = bootstrap_team_specs(
            payload / "process", payload / "templates/team-specs", requested_workspace
        )
        if bootstrap.get("ai_disabled") is not True:
            raise OperationError("release.rehearsal-failed", "bootstrap did not prove AI-disabled operation")
        synthetic_project = requested_workspace / "sample-app"
        synthetic_project.mkdir()
        config_result = validate_configuration(
            requested_workspace / "team-specs", {"sample-app": synthetic_project},
            lambda: str(manifest["openspec"]["cli_version"])
        )
        if config_result.exit_code != 0:
            codes = ",".join(item.code for item in config_result.sorted_diagnostics())
            raise OperationError("release.rehearsal-failed", f"configuration is incompatible: {codes}")
        changes_root = requested_workspace / "team-specs/openspec/changes"
        classes = ("minor", "major", "hotfix") if options.platform_id == "windows" else ("minor",)
        for classification in classes:
            change_type = {"minor": "behavior_change", "major": "new_feature", "hotfix": "bugfix"}[classification]
            created = create_change(
                requested_workspace / "process", changes_root,
                change_id=f"rehearsal-{classification}", title=f"Synthetic {classification} rehearsal",
                classification=classification, change_type=change_type,
            )
            if created.get("human_authority_substituted") is not False:
                raise OperationError("release.rehearsal-failed", "change creation substituted human authority")

        legacy = requested_workspace / "legacy/change.yaml"
        legacy.parent.mkdir(parents=True)
        legacy.write_text(_LEGACY_CHANGE, encoding="utf-8", newline="\n")
        migration_plan = plan_migration(legacy)
        migrated = apply_migration(legacy, expected_plan_digest=migration_plan.as_dict()["plan_digest"])
        current_plan = plan_migration(legacy)
        second = apply_migration(legacy, expected_plan_digest=current_plan.as_dict()["plan_digest"])
        if migrated.as_dict().get("status") != "applied" or second.as_dict().get("status") != "already-current":
            raise OperationError("release.rehearsal-failed", "migration did not apply idempotently")

        archive = requested_workspace / "team-specs/openspec/changes/archive"
        archive.mkdir(parents=True, exist_ok=True)
        (archive / "accepted.md").write_text(
            "immutable accepted history\n", encoding="utf-8", newline="\n"
        )
        archive_before = _tree_digest(archive)
        candidate_package = requested_workspace / "update-candidate"
        shutil.copytree(payload / "process", candidate_package)
        package = _load_mapping(candidate_package / "package.yaml", "release.rehearsal-failed")
        installed_version = str(package["package"]["version"])
        candidate_version = _next_minor_version(installed_version)
        package["package"]["version"] = candidate_version
        (candidate_package / "package.yaml").write_text(
            yaml.safe_dump(package, sort_keys=False), encoding="utf-8", newline="\n"
        )
        (candidate_package / "VERSION").write_text(f"{candidate_version}\n", encoding="utf-8", newline="\n")
        config_path = requested_workspace / "team-specs/sdd.config.yaml"
        backups = requested_workspace / "rollback-snapshots"
        upgrade_evidence = _materialize_synthetic_upgrade_evidence(
            requested_workspace / "upgrade-review",
            requested_workspace / "process",
            installed_version,
            candidate_version,
        )
        update = update_process_package(
            requested_workspace / "process",
            candidate_package,
            config_path,
            backups,
            upgrade_evidence=upgrade_evidence,
        )
        bad_candidate = requested_workspace / "failed-update-candidate"
        shutil.copytree(candidate_package, bad_candidate)
        (bad_candidate / "VERSION").write_text(
            f"{_next_minor_version(candidate_version)}\n", encoding="utf-8", newline="\n"
        )
        failed_update_held = False
        try:
            update_process_package(
                requested_workspace / "process",
                bad_candidate,
                config_path,
                backups,
                upgrade_evidence=upgrade_evidence,
            )
        except OperationError:
            failed_update_held = True
        if not failed_update_held:
            raise OperationError("release.rehearsal-failed", "failed update did not hold")
        rollback = rollback_process_package(
            requested_workspace / "process", backups / installed_version, config_path
        )
        archive_after = _tree_digest(archive)
        if archive_before != archive_after or update.get("accepted_history_mutated") is not False or rollback.get("accepted_history_mutated") is not False:
            raise OperationError("release.archive-history-rewrite", "maintenance rewrote accepted history")

        required_scenarios = _WINDOWS_SCENARIOS if options.platform_id == "windows" else _LINUX_SCENARIOS
        scenarios = sorted(required_scenarios - {"negative-acceptance-cases"})
        completed = datetime.now(timezone.utc).replace(microsecond=0)
        completed_at = completed.strftime("%Y-%m-%dT%H:%M:%SZ")
        manifest_sha = hashlib.sha256((candidate / "release-manifest.yaml").read_bytes()).hexdigest()
        evidence = {
            "schema_version": "1.0",
            "evidence_id": _host_evidence_id(manifest["release_id"], options.platform_id),
            "platform_id": options.platform_id, "evidence_level": options.evidence_level,
            "completed_at": completed_at, "payload_sha256": manifest["payload_sha256"],
            "manifest_sha256": manifest_sha,
            "process_package_version": manifest["process_package"]["version"],
            "config_schema_version": manifest["config_schema_version"],
            "inventory": inventory, "inventory_commands": inventory_commands,
            "mcp": {"status": options.mcp_status, "evidence_ref": options.mcp_evidence_ref},
            "scenario_ids": scenarios, "scenario_codes": sorted(_SCENARIO_CODES),
            "result": "passed", "ai_disabled": True, "human_authority_substituted": False,
            "privacy_scan": "passed", "archive_digest_before": archive_before,
            "archive_digest_after": archive_after, "rollback_result": "passed",
        }
        host_schema = payload / "process/schemas/release-host-evidence.schema.json"
        evidence["negative_acceptance_cases"] = _run_negative_acceptance_matrix(
            evidence, manifest, manifest_sha, completed, host_schema
        )
        evidence["scenario_ids"] = sorted([*scenarios, "negative-acceptance-cases"])
        _validate_schema(evidence, host_schema, "release.host-evidence-invalid")
        if _contains_private(evidence):
            raise OperationError("release.evidence-private", "rehearsal evidence contains private material")
        _write_yaml_no_replace(requested_output, evidence)
        return {
            "operation": "rehearse-release-candidate", "status": "rehearsal-complete",
            "platform_id": options.platform_id, "evidence_level": options.evidence_level,
            "payload_sha256": manifest["payload_sha256"],
            "human_acceptance_required": True,
        }
    except Exception:
        if requested_workspace.exists():
            shutil.rmtree(requested_workspace, ignore_errors=True)
        raise


_LEGACY_CHANGE = """# Synthetic legacy migration input.
id: sample-legacy-thin
title: Sample legacy thin package
mode: thin
type: config_ops
status: draft
systems: [sample-app]
quality: {strategy_ref: evidence/quality.md, regression_ref: evidence/regression.md}
review: {owner_refs: [sample-tech-leads]}
publication: {required: false}
spec_change: {required: true, delta_paths: [specs/sample/spec.md]}
classification_evidence:
  - id: local-change
    value: true
    source: {kind: proposal, ref: proposal.md}
    rationale: Synthetic migration evidence.
decision: {owner_type: human, owner_id: sample-tech-lead, state: confirmed, evidence_ref: decisions/classification.md}
policy: {id: sdd-core, version: 1.0.0}
extensions: {sample-note: preserve-me}
"""


def _observe_inventory() -> tuple[dict[str, str], list[dict[str, Any]]]:
    observed: list[dict[str, Any]] = []
    for argv in _INVENTORY_ARGV:
        executable = shutil.which(argv[0]) or argv[0]
        execution_argv = [executable, *argv[1:]]
        try:
            result = subprocess.run(
                execution_argv, shell=False, capture_output=True, text=True, timeout=20, check=False
            )
        except (OSError, subprocess.SubprocessError) as error:
            raise OperationError("release.inventory-failed", "required inventory command failed", exit_code=3) from error
        stdout = (result.stdout or result.stderr).strip()
        if result.returncode != 0 or not stdout:
            raise OperationError("release.inventory-failed", "required inventory command failed", exit_code=3)
        observed.append({"argv": argv, "exit_code": result.returncode, "stdout": stdout})
    return ({
        "os": observed[4]["stdout"], "architecture": os.environ.get("PROCESSOR_ARCHITECTURE", "unknown"),
        "shell": "PowerShell" if os.name == "nt" else "bash", "python": observed[0]["stdout"],
        "node": observed[1]["stdout"], "openspec": observed[2]["stdout"], "git": observed[3]["stdout"],
    }, observed)


def _tree_digest(root: Path) -> str:
    rows: list[dict[str, str]] = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rows.append({"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    return hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _write_yaml_no_replace(target: Path, value: Mapping[str, Any]) -> None:
    temporary = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    if os.path.lexists(temporary):
        raise OperationError("release.staging-exists", "evidence staging file already exists")
    data = yaml.safe_dump(dict(value), sort_keys=False, allow_unicode=True).encode("utf-8")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError as error:
            raise OperationError("release.output-exists", "rehearsal output appeared during publication") from error
        temporary.unlink()
        if hasattr(os, "O_DIRECTORY"):
            descriptor = os.open(target.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def validate_portable_path(value: str) -> str:
    """Return a canonical portable path or fail closed on Windows/POSIX threats."""
    if not isinstance(value, str) or not value or value in {".", ".."} or "\\" in value:
        raise OperationError("release.path-unsafe", "path is not portable")
    if value.startswith(("/", "//")) or _DRIVE.match(value) or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise OperationError("release.path-unsafe", "path is not portable")
    path = PurePosixPath(value)
    if str(path) != value or any(part in {"", ".", ".."} for part in path.parts):
        raise OperationError("release.path-unsafe", "path is not canonical")
    for part in path.parts:
        if ":" in part or part.endswith((".", " ")):
            raise OperationError("release.path-unsafe", "path is unsafe on Windows")
        if part.split(".", 1)[0].upper() in _RESERVED:
            raise OperationError("release.path-unsafe", "reserved Windows device name")
    return value


def _is_link_or_reparse(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & _REPARSE_POINT)


def _assert_existing_ancestry_safe(path: Path) -> Path:
    absolute = Path(os.path.abspath(path))
    chain: list[Path] = []
    current = absolute
    while True:
        chain.append(current)
        if current.parent == current:
            break
        current = current.parent
    for component in reversed(chain):
        if not os.path.lexists(component):
            break
        if _is_link_or_reparse(component):
            raise OperationError(
                "release.link-forbidden",
                "existing path ancestry contains a link or reparse point",
            )
    return absolute


def _safe_directory_root(path: Path, missing_code: str) -> Path:
    raw = _assert_existing_ancestry_safe(Path(path))
    try:
        if _is_link_or_reparse(raw):
            raise OperationError("release.link-forbidden", "root links and reparse points are forbidden")
    except FileNotFoundError as error:
        raise OperationError(missing_code, "required directory is missing", exit_code=3) from error
    if not raw.is_dir():
        raise OperationError(missing_code, "required directory is missing", exit_code=3)
    return raw.resolve()


def _assert_no_mutable_evidence(parts: tuple[str, ...]) -> None:
    folded = tuple(part.casefold() for part in parts)
    for denied in _MUTABLE_EVIDENCE_PARTS:
        target = tuple(part.casefold() for part in denied)
        if folded[: len(target)] == target:
            raise OperationError("release.mutable-evidence-forbidden", "mutable development or release evidence is not payload content")


def _is_python_bytecode(parts: tuple[str, ...]) -> bool:
    folded = tuple(part.casefold() for part in parts)
    return "__pycache__" in folded or folded[-1].endswith((".pyc", ".pyo"))


def _assert_no_python_bytecode(parts: tuple[str, ...]) -> None:
    if _is_python_bytecode(parts):
        raise OperationError("release.bytecode-forbidden", "Python bytecode is not release payload content")


def payload_inventory(payload_root: Path, *, _exclude_python_bytecode: bool = False) -> dict[str, Any]:
    """Inspect a payload and return its full sorted byte inventory and canonical digest."""
    root = _safe_directory_root(payload_root, "release.payload-missing")
    inventory: list[dict[str, Any]] = []
    identities: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        validate_portable_path(relative)
        parts = tuple(PurePosixPath(relative).parts)
        _assert_no_mutable_evidence(parts)
        if _exclude_python_bytecode and _is_python_bytecode(parts):
            continue
        _assert_no_python_bytecode(parts)
        identity = unicodedata.normalize("NFC", relative).casefold()
        previous = identities.setdefault(identity, relative)
        if previous != relative:
            raise OperationError("release.path-collision", "portable path identities collide")
        if _is_link_or_reparse(path):
            raise OperationError("release.link-forbidden", "links and reparse points are forbidden")
        if path.is_dir():
            continue
        if not path.is_file():
            raise OperationError("release.asset-unsafe", "payload contains a non-regular asset")
        data = path.read_bytes()
        inventory.append({"path": relative, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    encoded = json.dumps(inventory, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return {"inventory": inventory, "payload_sha256": hashlib.sha256(encoded).hexdigest()}


def _load_mapping(path: Path, code: str) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError(code, "required contract is missing or malformed", exit_code=3) from error
    if not isinstance(value, dict):
        raise OperationError(code, "required contract root must be a mapping", exit_code=3)
    return value


def _validate_schema(document: Mapping[str, Any], schema_path: Path, code: str) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise OperationError(code, "schema is missing or malformed", exit_code=3) from error
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        raise OperationError(code, "document does not satisfy its schema")


def _expected_allowlist() -> dict[str, Any]:
    entry_points = [
        {"name": name, "smoke": list(smoke), "expected_exit_codes": list(exits)}
        for name, smoke, exits in _ENTRY_POINTS
    ]
    next(item for item in entry_points if item["name"] == "manage_release_candidate.py")["additional_smokes"] = [
        ["scripts/manage_release_candidate.py", "accept", "--help"],
        ["scripts/manage_release_candidate.py", "rehearse", "--help"],
    ]
    return {
        "schema_version": "1.0",
        "requirements": ["requirements-test.txt"],
        "template_roots": ["templates/team-specs"],
        "runbooks": list(_RUNBOOKS),
        "entry_points": entry_points,
    }


def _validate_allowlist(allowlist: Mapping[str, Any], schema_path: Path) -> None:
    _validate_schema(allowlist, schema_path, "release.allowlist-invalid")
    if dict(allowlist) != _expected_allowlist():
        raise OperationError("release.allowlist-invalid", "allowlist differs from the public release contract")


def _assert_file(path: Path, relative: str) -> None:
    if not path.is_file() or _is_link_or_reparse(path):
        raise OperationError("release.asset-missing", f"declared asset is unavailable: {relative}", exit_code=3)


def _copy_file(source: Path, target: Path, relative: str) -> None:
    validate_portable_path(relative)
    _assert_file(source, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _copy_tree(source: Path, target: Path, relative: str) -> None:
    validate_portable_path(relative)
    if not source.is_dir() or _is_link_or_reparse(source):
        raise OperationError("release.asset-missing", f"declared asset root is unavailable: {relative}", exit_code=3)
    # Inspect source bytes and links before copying; destination receives regular files only.
    payload_inventory(source, _exclude_python_bytecode=True)

    def ignore_bytecode(_directory: str, names: list[str]) -> set[str]:
        return {
            name for name in names
            if name.casefold() == "__pycache__" or name.casefold().endswith((".pyc", ".pyo"))
        }

    shutil.copytree(source, target, ignore=ignore_bytecode)


def _raw_artifacts(root: Path) -> list[dict[str, Any]]:
    resolved = _safe_directory_root(root, "release.raw-artifacts-invalid")
    result: list[dict[str, Any]] = []
    identities: set[str] = set()
    for path in sorted(resolved.rglob("*"), key=lambda p: p.relative_to(resolved).as_posix()):
        relative = path.relative_to(resolved).as_posix()
        validate_portable_path(relative)
        identity = unicodedata.normalize("NFC", relative).casefold()
        if identity in identities:
            raise OperationError("release.path-collision", "raw artifact paths collide")
        identities.add(identity)
        if _is_link_or_reparse(path):
            raise OperationError("release.link-forbidden", "raw artifact links are forbidden")
        if path.is_dir():
            continue
        data = path.read_bytes()
        result.append({"reference": f"artifact:{relative}", "sha256": hashlib.sha256(data).hexdigest()})
    if not result:
        raise OperationError("release.raw-artifacts-invalid", "raw artifact root must contain evidence", exit_code=3)
    return result


def _certification_references(payload_root: Path) -> list[dict[str, str]]:
    evidence = payload_root / "process/certification/evidence"
    references: list[dict[str, str]] = []
    for path in sorted(evidence.glob("*.yaml")):
        name = path.name.casefold()
        family = "qwen" if "qwen" in name else "deepseek" if "deepseek" in name else None
        if family:
            references.append({
                "model_family": family,
                "path": path.relative_to(payload_root).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    if {item["model_family"] for item in references} != {"qwen", "deepseek"}:
        raise OperationError("release.certification-missing", "normalized Qwen and DeepSeek evidence is required")
    return references


def _validate_inputs(inputs: ReleaseInputs) -> None:
    if (
        not isinstance(inputs.release_id, str)
        or not _RELEASE_ID.fullmatch(inputs.release_id)
        or not isinstance(inputs.known_limitations, tuple)
        or any(not isinstance(value, str) or not value for value in inputs.known_limitations)
        or not isinstance(inputs.raw_artifact_root, Path)
    ):
        raise OperationError("input-invalid", "release inputs are malformed", exit_code=3)


def _package_contract(root: Path) -> dict[str, Any]:
    package = _load_mapping(root / "process/package.yaml", "release.package-invalid")
    _validate_schema(package, root / "process/schemas/process-package.schema.json", "release.package-invalid")
    return package


def _dependency_contract(root: Path, package: Mapping[str, Any]) -> dict[str, Any]:
    requirements: dict[str, str] = {}
    try:
        lines = (root / "requirements-test.txt").read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line and not line.startswith("#"):
                name, version = line.split("==", 1)
                requirements[name] = version
    except (OSError, UnicodeError, ValueError) as error:
        raise OperationError("release.dependencies-invalid", "dependency pins are missing or malformed", exit_code=3) from error
    return {
        "python": "3.11+", "node": "20+", "git": "2.40+",
        "openspec": package["openspec"]["cli_version"],
        "mcp": "provisioned-or-explicitly-unavailable",
        "shells": ["powershell-7+", "bash-5+"],
        "packages": [{"name": name, "version": requirements[name]} for name in sorted(requirements)],
    }


def _derived_manifest_fields(root: Path) -> dict[str, Any]:
    package = _package_contract(root)
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_allowlist(allowlist, root / "process/schemas/release-allowlist.schema.json")
    inspected = payload_inventory(root)
    _validate_declared_assets(root, allowlist, package, inspected["inventory"])
    try:
        config_schema = json.loads((root / "process/schemas/sdd-config.schema.json").read_text(encoding="utf-8"))
        config_version = config_schema["properties"]["config_schema_version"]["const"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise OperationError("release.config-contract-invalid", "config identity cannot be derived", exit_code=3) from error
    return {
        "payload_sha256": inspected["payload_sha256"],
        "inventory": inspected["inventory"],
        "allowlist_sha256": hashlib.sha256((root / "process/release-allowlist.yaml").read_bytes()).hexdigest(),
        "process_package": package["package"],
        "config_schema_version": config_version,
        "openspec": package["openspec"],
        "host_evidence": [dict(row) for row in _HOST_EVIDENCE],
        "compatibility": _dependency_contract(root, package),
        "verification": {
            "commands": list(_VERIFICATION_COMMANDS),
            "evidence_requirements": list(_EVIDENCE_REQUIREMENTS),
        },
        "weak_model_certification": _certification_references(root),
        "rollback_reference": _ROLLBACK_REFERENCE,
    }


def generate_release_manifest(payload_root: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Generate a byte-stable manifest exclusively from inputs and inspected contracts."""
    _validate_inputs(inputs)
    root = _safe_directory_root(payload_root, "release.payload-missing")
    derived = _derived_manifest_fields(root)
    return {
        "schema_version": "2.0",
        "release_id": inputs.release_id,
        **derived,
        "raw_artifacts": _raw_artifacts(inputs.raw_artifact_root),
        "known_limitations": list(inputs.known_limitations),
    }


def _declared_top_level(payload_root: Path, allowlist: Mapping[str, Any], package: Mapping[str, Any]) -> set[str]:
    declared = set(allowlist["requirements"])
    declared.update(allowlist["template_roots"])
    declared.update(f"docs/runbooks/{name}" for name in allowlist["runbooks"])
    declared.update(f"scripts/{item['name']}" for item in allowlist["entry_points"])
    declared.update(f"process/{name}" for name in package["distribution"]["files"])
    declared.update(f"process/{name}" for name in package["distribution"]["roots"])
    declared.update(package["canonical_sources"])
    return declared


def _validate_declared_assets(
    payload_root: Path,
    allowlist: Mapping[str, Any],
    package: Mapping[str, Any],
    inventory: list[dict[str, Any]],
) -> None:
    expected_scripts = {item["name"] for item in allowlist["entry_points"]}
    actual_scripts = {path.name for path in (payload_root / "scripts").iterdir() if path.is_file()}
    if actual_scripts != expected_scripts:
        raise OperationError("release.allowlist-mismatch", "public entry-point inventory differs from the allowlist")
    for relative in _declared_top_level(payload_root, allowlist, package):
        if not (payload_root / relative).exists():
            raise OperationError("release.asset-missing", "payload omits a declared release asset")
    exact = set(allowlist["requirements"])
    exact.update(f"docs/runbooks/{name}" for name in allowlist["runbooks"])
    exact.update(f"scripts/{item['name']}" for item in allowlist["entry_points"])
    exact.update(f"process/{name}" for name in package["distribution"]["files"])
    exact.update(package["canonical_sources"])
    roots = [*allowlist["template_roots"], *(f"process/{name}" for name in package["distribution"]["roots"])]
    for item in inventory:
        path = item["path"]
        if path not in exact and not any(path.startswith(f"{root}/") for root in roots):
            raise OperationError("release.allowlist-closure", "payload contains an undeclared asset")


def validate_release_manifest(
    candidate_root: Path, manifest: Mapping[str, Any], *, now: datetime | None = None
) -> dict[str, Any]:
    """Validate manifest schema and semantic binding to the immutable candidate payload."""
    del now  # Reserved for Task 2 evidence freshness without making Task 1 time-dependent.
    candidate = _safe_directory_root(candidate_root, "release.candidate-missing")
    payload_path = candidate / "payload"
    if os.path.lexists(payload_path):
        payload = _safe_directory_root(payload_path, "release.payload-missing")
        entries = {path.name for path in candidate.iterdir()}
        if entries != {"payload", "release-manifest.yaml"}:
            raise OperationError("release.candidate-closure", "candidate root contains undeclared content")
    else:
        raise OperationError(
            "release.candidate-closure",
            "candidate root must contain payload and its canonical manifest",
        )
    manifest_path = candidate / "release-manifest.yaml"
    try:
        if _is_link_or_reparse(manifest_path) or not manifest_path.is_file():
            raise OperationError(
                "release.manifest-file-unsafe",
                "candidate manifest must be one regular non-link file",
            )
    except FileNotFoundError as error:
        raise OperationError(
            "release.manifest-file-unsafe", "candidate manifest is missing"
        ) from error
    disk_manifest = _load_mapping(manifest_path, "release.manifest-file-invalid")
    if disk_manifest != dict(manifest):
        raise OperationError(
            "release.manifest-file-mismatch",
            "supplied manifest differs from the canonical candidate manifest",
        )
    schema_path = payload / "process/schemas/release-manifest.schema.json"
    derived = _derived_manifest_fields(payload)
    for field, expected in derived.items():
        if manifest.get(field) != expected:
            raise OperationError("release.manifest-derived-mismatch", f"manifest field is not derived from payload: {field}")
    _validate_schema(manifest, schema_path, "release.manifest-invalid")
    return {
        "operation": "validate-release-manifest", "status": "valid",
        "release_id": manifest["release_id"], "payload_sha256": derived["payload_sha256"],
    }


def _publish_no_replace(staging: Path, target: Path) -> None:
    """Atomically publish a directory and fail if the destination already exists."""
    if os.name == "nt":
        try:
            os.rename(staging, target)
        except OSError as error:
            if os.path.lexists(target):
                raise OperationError("release.destination-exists", "destination appeared during candidate construction") from error
            raise
        return
    if sys.platform.startswith("linux"):
        import ctypes

        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = getattr(libc, "renameat2", None)
        if renameat2 is None:
            raise OperationError("release.atomic-publish-unsupported", "atomic no-replace publication is unavailable", exit_code=3)
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(
            -100, os.fsencode(staging), -100, os.fsencode(target), 1
        )
        if result == 0:
            return
        error_number = ctypes.get_errno()
        if error_number == errno.EEXIST:
            raise OperationError("release.destination-exists", "destination appeared during candidate construction")
        raise OSError(error_number, os.strerror(error_number), str(target))
    raise OperationError("release.atomic-publish-unsupported", "host is not certified for atomic publication", exit_code=3)


def build_release_candidate(repository_root: Path, destination: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Atomically create one immutable allowlisted candidate in a new destination."""
    _validate_inputs(inputs)
    root = _safe_directory_root(repository_root, "release.repository-missing")
    requested = Path(os.path.abspath(destination))
    validate_portable_path(requested.name)
    _assert_existing_ancestry_safe(requested.parent)
    target = requested
    if target == root or root in target.parents or target in root.parents:
        raise OperationError("release.path-overlap", "source and destination must not overlap")
    if os.path.lexists(target):
        raise OperationError("release.destination-exists", "destination must not already exist")
    requested.parent.mkdir(parents=True, exist_ok=True)
    parent = _safe_directory_root(requested.parent, "release.destination-parent-invalid")
    target = parent / requested.name
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_allowlist(allowlist, root / "process/schemas/release-allowlist.schema.json")
    package = _package_contract(root)
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=target.parent))
    try:
        payload = staging / "payload"
        payload.mkdir()
        for name in package["distribution"]["files"]:
            _copy_file(root / "process" / name, payload / "process" / name, f"process/{name}")
        for name in package["distribution"]["roots"]:
            _copy_tree(root / "process" / name, payload / "process" / name, f"process/{name}")
        for relative in package["canonical_sources"]:
            _copy_file(root / relative, payload / relative, relative)
        for relative in allowlist["requirements"]:
            _copy_file(root / relative, payload / relative, relative)
        for relative in allowlist["template_roots"]:
            _copy_tree(root / relative, payload / relative, relative)
        for name in allowlist["runbooks"]:
            _copy_file(root / "docs/runbooks" / name, payload / "docs/runbooks" / name, f"docs/runbooks/{name}")
        for item in allowlist["entry_points"]:
            name = item["name"]
            _copy_file(root / "scripts" / name, payload / "scripts" / name, f"scripts/{name}")
        manifest = generate_release_manifest(payload, inputs)
        manifest_text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, line_break="\n")
        (staging / "release-manifest.yaml").write_text(manifest_text, encoding="utf-8", newline="\n")
        validate_release_manifest(staging, manifest)
        _publish_no_replace(staging, target)
        return manifest
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
