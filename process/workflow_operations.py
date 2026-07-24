"""Deterministic package/bootstrap workflow operations.

The module owns bounded filesystem preparation only. It never records human
approval, mutates lifecycle state, calls an integration, or infers authority.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .errors import OperationError
from .guided_workflow import load_catalog
from .operations_catalog import load_operations_catalog

from .validators.config_discovery import (
    BUNDLED_SCHEMA_ROOT,
    load_schema_resources,
    validate_package_schemas,
)
from .validators.config_validation import (
    ValidationResult,
    config_compatibility,
    package_compatibility,
    schema_diagnostics,
)
from .validators.artifact_gates import evaluate_gate
from .validators.gate_input import validate_gate_input
from .validators.policy_validation import validate_policy_bundle


CHANGE_ID = re.compile(r"^[a-z][a-z0-9-]*$")
CLASSIFICATIONS = {"minor", "major", "hotfix"}
CHANGE_TYPES = {
    "new_feature", "behavior_change", "bugfix", "refactor", "docs_only", "config_ops"
}
EXTERNAL_STATES = {
    "openspec_archive": "archived",
    "release_readiness": "release-ready",
    "deployment": "deployed",
    "consumer_acceptance": "accepted",
    "tracker_done": "done",
}
FALLBACK_COMMANDS = {
    "jira": "Record tracker status and source reference manually; do not infer Done.",
    "confluence": "Keep OpenSpec/Markdown canonical and queue publication explicitly.",
    "model-runtime": "Run deterministic validators and complete the human review worksheet.",
    "mcp": "Use approved local files and record the unavailable connector as evidence.",
    "role-inbox": "Route the evidence pack to the configured human owner out of band.",
}

BUNDLED_PACKAGE_ROOT = Path(__file__).resolve().parent


def load_yaml_input(path: Path) -> dict[str, Any]:
    """Load one CLI input mapping with stable operational-failure semantics."""
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("input-invalid", "required input is missing or malformed", exit_code=3) from error
    if not isinstance(value, dict):
        raise OperationError("input-invalid", "required input root must be a mapping", exit_code=3)
    return value


def _normalize_known_legacy_config(
    config: dict[str, Any], installed_root: Path, central_root: Path
) -> dict[str, Any]:
    """Migrate only documented legacy defaults when their target is provably local."""
    normalized = json.loads(json.dumps(config))
    policy = normalized.get("policy_set")
    if isinstance(policy, dict) and "overrides" not in policy:
        policy["overrides"] = []
    if normalized.get("validation") == {"mode": "strict"}:
        normalized["validation"] = {"strict": True, "placeholders_allowed": False}
    pin = normalized.get("process_package")
    if (
        isinstance(pin, dict)
        and pin.get("location") == "../../process"
        and (central_root.parent / "process").resolve() == installed_root.resolve()
    ):
        pin["location"] = "../process"
    return normalized

def bootstrap_team_specs(
    package_root: Path, team_template: Path, destination: Path
) -> dict[str, Any]:
    """Create one synthetic central workspace from immutable package sources."""
    package_root = _safe_root(package_root, "package-source")
    team_template = _safe_root(team_template, "team-template")
    destination = _absolute(destination)
    template_config = _load_yaml(team_template / "sdd.config.yaml")
    package = _validate_standalone_package(package_root, template_config)["package"]
    if destination.exists() and any(destination.iterdir()):
        raise OperationError("destination-not-empty", "bootstrap destination must be empty")
    if not team_template.is_dir():
        raise OperationError("template-missing", "team-specs template is missing")

    staging = destination.with_name(f".{destination.name}.bootstrap")
    if staging.exists():
        raise OperationError("staging-exists", "bootstrap staging destination already exists")
    try:
        staging.mkdir(parents=True)
        _copy_versioned_tree(package_root, staging / "process")
        _copy_versioned_tree(team_template, staging / "team-specs")
        _install_gigacode_templates(package_root, staging)
        config_path = staging / "team-specs" / "sdd.config.yaml"
        config = _load_yaml(config_path)
        config["process_package"]["location"] = "../process"
        config_path.write_text(
            yaml.safe_dump(config, sort_keys=False), encoding="utf-8", newline="\n"
        )
        if destination.exists():
            destination.rmdir()
        shutil.move(str(staging), str(destination))
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    return _evidence(
        "bootstrap-team-specs",
        "created",
        package,
        destination,
        destination.rglob("*"),
    )


def create_change(
    package_root: Path,
    changes_root: Path,
    *,
    change_id: str,
    title: str,
    classification: str,
    change_type: str,
) -> dict[str, Any]:
    """Create a draft package from the versioned template without approving it."""
    package_root = _safe_root(package_root, "package-source")
    _validate_standalone_package(package_root)
    changes_root = _absolute(changes_root)
    if not CHANGE_ID.fullmatch(change_id):
        raise OperationError("change-id-invalid", "change id must be portable lower kebab-case")
    if classification not in CLASSIFICATIONS:
        raise OperationError("classification-invalid", "classification must be minor, major, or hotfix")
    if change_type not in CHANGE_TYPES:
        raise OperationError("change-type-invalid", "unsupported change type")
    if not title.strip():
        raise OperationError("title-invalid", "title must be non-empty")
    template = package_root / "templates" / "change"
    if not template.is_dir():
        raise OperationError("template-missing", "versioned change template is missing")
    destination = (changes_root / change_id).resolve()
    try:
        destination.relative_to(changes_root)
    except ValueError as error:
        raise OperationError("destination-unsafe", "change destination escapes changes root") from error
    if destination.exists():
        raise OperationError("destination-exists", "change destination already exists")
    changes_root.mkdir(parents=True, exist_ok=True)
    staging = changes_root / f".{change_id}.create"
    if staging.exists():
        raise OperationError("staging-exists", "change staging destination already exists")
    try:
        _copy_versioned_tree(template, staging)
        change_path = staging / "change.yaml"
        change = _load_yaml(change_path)
        change.update({
            "id": change_id,
            "title": title.strip(),
            "classification": classification,
            "type": change_type,
            "status": "draft",
            "decision": {
                "owner_type": "human",
                "owner_id": "sample-tech-lead",
                "state": "pending",
                "evidence_ref": "decisions/classification.md",
            },
            "compatibility": {"source": "native-v2"},
        })
        change_path.write_text(
            yaml.safe_dump(change, sort_keys=False), encoding="utf-8", newline="\n"
        )
        gate_path = staging / "gate-input.yaml"
        gate = _load_yaml(gate_path)
        gate.update({"id": change_id, "classification": classification, "status": "draft"})
        gate_path.write_text(
            yaml.safe_dump(gate, sort_keys=False), encoding="utf-8", newline="\n"
        )
        shutil.move(str(staging), str(destination))
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    evidence = _evidence(
        "create-change", "created", _load_yaml(package_root / "package.yaml"),
        destination, destination.rglob("*"),
    )
    evidence.update({
        "change_id": change_id,
        "classification": classification,
        "decision_state": "pending-human-confirmation",
        "lifecycle_mutated": False,
    })
    return evidence


def prepare_spec_pr(package_root: Path, change_root: Path) -> dict[str, Any]:
    """Collect immutable Spec PR evidence without creating or approving a PR."""
    return _prepare_review(package_root, change_root, "prepare-spec-pr")


def prepare_archive(
    package_root: Path,
    change_root: Path,
    *,
    archive_root: Path | None = None,
    archive_date: str | None = None,
    approval: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Collect archive evidence and, when requested, resolve the guarded history contract."""
    evidence = _prepare_review(package_root, change_root, "prepare-archive")
    if archive_root is None and archive_date is None and approval is None:
        return evidence
    target, commit_subject, approval_ref = _archive_contract(
        package_root, change_root, archive_root, archive_date, approval
    )
    evidence.update({
        "archive_path": target.as_posix(),
        "archive_date": archive_date,
        "required_commit_subject": commit_subject,
        "approval_ref": approval_ref,
        "approved": True,
        "approval_verified": True,
    })
    return evidence


def archive_change(
    package_root: Path,
    change_root: Path,
    *,
    archive_root: Path,
    archive_date: str,
    approval: dict[str, Any],
) -> dict[str, Any]:
    """Move one explicitly approved local change to its dated archive path."""
    evidence = prepare_archive(
        package_root,
        change_root,
        archive_root=archive_root,
        archive_date=archive_date,
        approval=approval,
    )
    source = _safe_root(change_root, "archive-source")
    target = _absolute(Path(evidence["archive_path"]))
    if target.exists():
        raise OperationError("archive-target-exists", "dated archive target already exists")
    target.parent.mkdir(parents=True, exist_ok=True)
    _assert_path_identity_safe(target.parent)
    shutil.move(str(source), str(target))
    result = validate_archive_history(
        target,
        str(evidence["required_commit_subject"]),
        str(evidence["change_id"]),
    )
    evidence.update(result)
    evidence.update({
        "operation": "archive-change",
        "status": "archived-locally",
        "archived": True,
        "lifecycle_mutated": True,
        "git_commit_created": False,
        "merge_performed": False,
        "release_performed": False,
        "deployment_performed": False,
    })
    return evidence


def validate_archive_history(
    archive_path: Path, commit_subject: str, change_id: str
) -> dict[str, Any]:
    """Validate the deterministic dated path and greppable commit convention."""
    expected_name = re.compile(rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(change_id)}$")
    if not expected_name.fullmatch(Path(archive_path).name):
        raise OperationError("archive-path-invalid", "archive path must use YYYY-MM-DD-change-id")
    try:
        date.fromisoformat(Path(archive_path).name[:10])
    except ValueError as error:
        raise OperationError("archive-date-invalid", "archive date must be a real ISO date") from error
    expected_subject = f"spec: archive {change_id}"
    if commit_subject != expected_subject:
        raise OperationError("archive-commit-invalid", "archive commit subject does not match the stable grammar")
    return {
        "status": "valid",
        "archive_path": _absolute(archive_path).as_posix(),
        "required_commit_subject": expected_subject,
        "human_authority_substituted": False,
    }


def _archive_contract(
    package_root: Path,
    change_root: Path,
    archive_root: Path | None,
    archive_date: str | None,
    approval: dict[str, Any] | None,
) -> tuple[Path, str, str]:
    source = _safe_root(change_root, "archive-source")
    if archive_root is None:
        raise OperationError("archive-root-required", "archive root is required")
    archive = _absolute(archive_root)
    if source.parent == archive or source.parent.name == "archive":
        raise OperationError("archive-source-already-archived", "change source is already archived")
    if archive.name != "archive" or source.parent != archive.parent:
        raise OperationError("archive-path-unsafe", "archive source and root must share one canonical changes root")
    _assert_path_identity_safe(source)
    _assert_path_identity_safe(source.parent)
    if archive.exists():
        if not archive.is_dir():
            raise OperationError("archive-path-unsafe", "archive root must be a directory")
        _assert_path_identity_safe(archive)
        _assert_safe_tree(archive)
    if not isinstance(archive_date, str):
        raise OperationError("archive-date-invalid", "archive date must be YYYY-MM-DD")
    try:
        parsed_date = date.fromisoformat(archive_date)
    except ValueError as error:
        raise OperationError("archive-date-invalid", "archive date must be a real ISO date") from error
    if parsed_date.isoformat() != archive_date:
        raise OperationError("archive-date-invalid", "archive date must be canonical YYYY-MM-DD")
    change = _load_yaml(source / "change.yaml")
    change_id = change.get("id")
    if not isinstance(change_id, str) or not CHANGE_ID.fullmatch(change_id):
        raise OperationError("change-id-invalid", "archive change id must be portable lower kebab-case")
    _assert_archive_readiness(_safe_root(package_root, "package-source"), source, change)
    if (
        not isinstance(approval, dict)
        or approval.get("change_id") != change_id
        or approval.get("owner_type") != "human"
        or approval.get("state") != "approved"
        or not _local_reference(approval.get("decision_ref"))
    ):
        raise OperationError("archive-approval-required", "explicit matching human archive approval is required")
    target = _absolute(archive / f"{archive_date}-{change_id}")
    try:
        target.relative_to(archive)
    except ValueError as error:
        raise OperationError("archive-path-unsafe", "archive target escapes archive root") from error
    if target.exists():
        raise OperationError("archive-target-exists", "dated archive target already exists")
    return target, f"spec: archive {change_id}", str(approval["decision_ref"])


def _assert_archive_readiness(
    package_root: Path, source: Path, change: dict[str, Any]
) -> None:
    """Require the canonical local gate and traceability records before movement."""
    if change.get("status") != "ready_to_archive":
        raise OperationError("archive-readiness-required", "change must be ready_to_archive")
    gate = _load_yaml(source / "gate-input.yaml")
    diagnostics = validate_gate_input(gate, package_root)
    if diagnostics:
        raise OperationError("archive-readiness-invalid", "archive gate input is invalid")
    if (
        gate.get("id") != change.get("id")
        or gate.get("classification") != change.get("classification")
        or gate.get("status") != "ready_to_archive"
    ):
        raise OperationError("archive-readiness-mismatch", "archive gate input does not match the change")
    config_path = source.parent.parent.parent / "sdd.config.yaml"
    config = _load_yaml(config_path)
    manifest = _load_yaml(package_root / "policies" / "manifest.yaml")
    policy = validate_policy_bundle(package_root, manifest, config, None)
    if policy.snapshot is None or policy.diagnostics:
        raise OperationError("archive-readiness-invalid", "archive policy cannot be resolved")
    report = evaluate_gate(gate, policy.snapshot, "archive-readiness")
    if report.as_dict()["blocking_gaps"]:
        raise OperationError("archive-readiness-blocked", "deterministic archive-readiness gate is blocked")
    traceability = _load_yaml(source / "traceability.yaml")
    if (
        traceability.get("classification") != change.get("classification")
        or traceability.get("lifecycle_state") != "ready_to_archive"
    ):
        raise OperationError("archive-readiness-mismatch", "traceability does not match archive readiness")
    validate_traceability(traceability)


def validate_traceability(document: dict[str, Any]) -> dict[str, Any]:
    """Validate canonical governance links and return a derived ID-only view."""
    schema = json.loads((BUNDLED_SCHEMA_ROOT / "traceability-v2.schema.json").read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: (list(error.absolute_path), error.validator),
    )
    if errors:
        raise OperationError("traceability-schema-invalid", "traceability does not satisfy the trusted schema")
    classification = document.get("classification")
    lifecycle_state = document.get("lifecycle_state")
    policy = document.get("policy")
    links = document.get("links")
    identifiers: list[str] = []
    evidence_identifiers: list[str] = []
    derived_evidence: list[dict[str, str]] = []
    for link in links:
        identifiers.append(str(link["record_id"]))
        for field in ("requirement_refs", "scenario_refs", "task_refs"):
            for reference in link[field]:
                if not _local_reference(reference):
                    raise OperationError("traceability-reference-invalid", "references must be bounded local IDs or paths")
        evidence_links = link["evidence_links"]
        kinds = [str(row["kind"]) for row in evidence_links]
        local_ids = [str(row["record_id"]) for row in evidence_links]
        if len(set(kinds)) != len(kinds) or len(set(local_ids)) != len(local_ids):
            raise OperationError("traceability-evidence-duplicate", "evidence kinds and ids must be unique per link")
        for row in evidence_links:
            if not _local_reference(row["source_ref"]) or any(not _local_reference(ref) for ref in row["evidence_refs"]):
                raise OperationError("traceability-reference-invalid", "evidence references must be bounded local IDs or paths")
            evidence_identifiers.append(str(row["record_id"]))
            derived_evidence.append({
                "record_id": str(row["record_id"]),
                "kind": str(row["kind"]),
                "status": str(row["status"]),
                "policy_version": str(row["policy_version"]),
            })
        if lifecycle_state in {"ready_to_archive", "archived"}:
            if any(row["status"] == "pending" for row in evidence_links):
                raise OperationError("traceability-archive-pending", "pending traceability blocks archive readiness")
            by_kind = {str(row["kind"]): str(row["status"]) for row in evidence_links}
            concrete = {"classification", "dor", "dod", "implementation", "qa", "regression", "approval"}
            if any(by_kind.get(kind) != "concrete" for kind in concrete):
                raise OperationError("traceability-archive-incomplete", "required archive evidence is incomplete")
            resolved = {"release"}
            if classification == "major":
                resolved |= {"automation", "architecture"}
            if any(by_kind.get(kind) not in {"concrete", "not-applicable"} for kind in resolved):
                raise OperationError("traceability-archive-incomplete", "class-applicable archive evidence is unresolved")
            if classification == "hotfix" and by_kind.get("hotfix-reconciliation") != "concrete":
                raise OperationError("traceability-archive-incomplete", "hotfix reconciliation is incomplete")
    if len(set(identifiers)) != len(identifiers):
        raise OperationError("traceability-id-duplicate", "record ids must be unique")
    if len(set(evidence_identifiers)) != len(evidence_identifiers):
        raise OperationError("traceability-evidence-duplicate", "evidence record ids must be globally unique")
    return {
        "schema_version": "1.0",
        "status": "valid",
        "policy": dict(policy),
        "classification": classification,
        "lifecycle_state": lifecycle_state,
        "record_ids": sorted(identifiers),
        "evidence_links": sorted(derived_evidence, key=lambda row: row["record_id"]),
        "canonical_source": "openspec/changes/adopt-nis-corporate-process-governance/specs/traceability-contract/spec.md",
    }


def validate_external_mapping(document: dict[str, Any]) -> dict[str, Any]:
    """Fail closed unless all five external concepts remain explicitly distinct."""
    if document.get("schema_version") != "1.0":
        raise OperationError("external-mapping-schema-invalid", "schema_version must be 1.0")
    if document.get("policy") != {"id": "sdd-core", "version": "1.0.0"}:
        raise OperationError("external-mapping-policy-invalid", "canonical policy identity is required")
    states = document.get("states")
    if not isinstance(states, dict) or set(states) != set(EXTERNAL_STATES):
        raise OperationError("external-mapping-incomplete", "all five external states are required")
    for key, expected in EXTERNAL_STATES.items():
        if states.get(key) != expected:
            raise OperationError("external-mapping-unknown", f"unknown mapping for {key}")
    if len(set(states.values())) != len(states):
        raise OperationError("external-mapping-collapsed", "distinct states cannot be collapsed")
    return {
        "schema_version": "1.0",
        "status": "valid",
        "policy": dict(document["policy"]),
        "states": dict(states),
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }


def manual_fallback_plan(unavailable: set[str]) -> dict[str, Any]:
    """Build deterministic manual instructions for unavailable optional surfaces."""
    unknown = set(unavailable) - set(FALLBACK_COMMANDS)
    if unknown:
        raise OperationError("integration-unknown", "an unsupported integration name was supplied")
    ordered = sorted(unavailable)
    return {
        "schema_version": "1.0",
        "status": "manual-fallback-required" if ordered else "integrations-available",
        "unavailable": ordered,
        "steps": [
            {"integration": name, "deterministic_command": FALLBACK_COMMANDS[name]}
            for name in ordered
        ],
        "core_gates": [
            "validate-process-config", "classify-change", "evaluate-change-gates",
            "review-tech-lead", "check-corporate-flow",
        ],
        "ai_disabled": True,
        "human_authority_substituted": False,
    }


def update_process_package(
    installed_root: Path,
    candidate_root: Path,
    config_path: Path,
    backup_root: Path,
    *,
    upgrade_evidence: dict[str, Any] | Path | None = None,
    upgrade_evidence_root: Path | None = None,
) -> dict[str, Any]:
    """Install a compatible package transactionally while retaining rollback state."""
    installed_root = _safe_root(installed_root, "installed-package")
    candidate_root = _safe_root(candidate_root, "candidate-package")
    config_path = _absolute(config_path)
    backup_root = _absolute(backup_root)
    config = _normalize_known_legacy_config(_load_yaml(config_path), installed_root, config_path.parent)
    installed_snapshot = _validate_standalone_package(installed_root, config)
    candidate_snapshot = _validate_standalone_package(candidate_root, config, require_config_version=False)
    installed = installed_snapshot["identity"]
    candidate = candidate_snapshot["identity"]
    _assert_config_pin(config, installed, installed_root, config_path.parent)
    if candidate["id"] != installed["id"]:
        raise OperationError("package-id-mismatch", "candidate package id differs")
    if candidate["version"] == installed["version"]:
        raise OperationError("package-version-unchanged", "candidate version is already installed")
    if _semver(candidate["version"]) <= _semver(installed["version"]):
        raise OperationError("package-downgrade-forbidden", "normal update requires a forward semantic version")
    reviewed_upgrade = validate_reviewed_upgrade_evidence(
        upgrade_evidence,
        from_identity={
            "package_version": installed["version"],
            "openspec_version": str(installed_snapshot["package"]["openspec"]["cli_version"]),
        },
        to_identity={
            "package_version": candidate["version"],
            "openspec_version": str(candidate_snapshot["package"]["openspec"]["cli_version"]),
        },
        evidence_root=upgrade_evidence_root,
    )
    gigacode_changes = _prepare_gigacode_update(
        installed_root, candidate_root, installed_root.parent
    )
    _assert_non_overlapping(installed_root, backup_root)
    _assert_non_overlapping(candidate_root, backup_root)
    backup = backup_root / installed["version"]
    backup_staging = backup_root / f".{installed['version']}.snapshot"
    proof = backup_root / f"{installed['version']}.rollback.yaml"
    if backup.exists():
        raise OperationError("rollback-exists", "rollback snapshot already exists")
    backup_root.mkdir(parents=True, exist_ok=True)
    original_config = config_path.read_bytes()
    displaced = installed_root.with_name(f".{installed_root.name}.previous")
    staged = installed_root.with_name(f".{installed_root.name}.candidate")
    if displaced.exists() or staged.exists() or backup_staging.exists() or proof.exists():
        raise OperationError("staging-exists", "update staging path already exists")
    try:
        _copy_versioned_tree(installed_root, backup_staging)
        _validate_standalone_package(backup_staging, config)
        shutil.move(str(backup_staging), str(backup))
        _write_yaml_atomic(proof, {
            "schema_version": "1.0",
            "from_version": installed["version"],
            "to_version": candidate["version"],
            "snapshot_sha256": _snapshot_digest(backup),
        })
        _copy_versioned_tree(candidate_root, staged)
        _validate_standalone_package(staged, config, require_config_version=False)
        shutil.move(str(installed_root), str(displaced))
        shutil.move(str(staged), str(installed_root))
        config["process_package"]["version"] = candidate["version"]
        _write_yaml_atomic(config_path, config)
        _apply_gigacode_updates(gigacode_changes)
        shutil.rmtree(displaced)
    except Exception:
        _restore_gigacode_updates(gigacode_changes)
        if staged.exists():
            shutil.rmtree(staged)
        if backup_staging.exists():
            shutil.rmtree(backup_staging)
        if installed_root.exists() and displaced.exists():
            shutil.rmtree(installed_root)
        if displaced.exists():
            shutil.move(str(displaced), str(installed_root))
        config_path.write_bytes(original_config)
        if backup.exists():
            shutil.rmtree(backup)
        if proof.exists():
            proof.unlink()
        raise
    return {
        "schema_version": "1.0",
        "operation": "update-process-package",
        "status": "updated",
        "from_version": installed["version"],
        "to_version": candidate["version"],
        "rollback_ref": backup.as_posix(),
        "accepted_history_mutated": False,
        "ai_disabled": True,
        "upgrade_evidence": reviewed_upgrade,
    }


def check_package_compatibility(
    installed_root: Path,
    candidate_root: Path,
    config_path: Path,
    *,
    upgrade_evidence: dict[str, Any] | Path | None = None,
    upgrade_evidence_root: Path | None = None,
) -> dict[str, Any]:
    """Check update inputs without writing package, config, or history."""
    installed_root = _safe_root(installed_root, "installed-package")
    candidate_root = _safe_root(candidate_root, "candidate-package")
    config_path = _absolute(config_path)
    config = _normalize_known_legacy_config(_load_yaml(config_path), installed_root, config_path.parent)
    installed_snapshot = _validate_standalone_package(installed_root, config)
    candidate_snapshot = _validate_standalone_package(candidate_root, config, require_config_version=False)
    installed = installed_snapshot["identity"]
    candidate = candidate_snapshot["identity"]
    _assert_config_pin(config, installed, installed_root, config_path.parent)
    if installed["id"] != candidate["id"]:
        raise OperationError("package-id-mismatch", "candidate package id differs")
    if _semver(candidate["version"]) <= _semver(installed["version"]):
        raise OperationError("package-downgrade-forbidden", "normal update requires a forward semantic version")
    gigacode_changes = _prepare_gigacode_update(
        installed_root, candidate_root, installed_root.parent
    )
    reviewed_upgrade = validate_reviewed_upgrade_evidence(
        upgrade_evidence,
        from_identity={
            "package_version": installed["version"],
            "openspec_version": str(installed_snapshot["package"]["openspec"]["cli_version"]),
        },
        to_identity={
            "package_version": candidate["version"],
            "openspec_version": str(candidate_snapshot["package"]["openspec"]["cli_version"]),
        },
        evidence_root=upgrade_evidence_root,
    )
    return {
        "schema_version": "1.0",
        "operation": "check-package-compatibility",
        "status": "compatible",
        "installed": installed,
        "candidate": candidate,
        "configuration_mutated": False,
        "accepted_history_mutated": False,
        "ai_disabled": True,
        "human_authority_substituted": False,
        "upgrade_evidence": reviewed_upgrade,
        "managed_gigacode_files": [target.relative_to(installed_root.parent).as_posix() for _, target, _ in gigacode_changes],
    }


def validate_reviewed_upgrade_evidence(
    evidence: dict[str, Any] | Path | None,
    *,
    from_identity: dict[str, str],
    to_identity: dict[str, str],
    evidence_root: Path | None = None,
) -> dict[str, str]:
    """Validate human-reviewed, identity-bound evidence before package mutation."""
    if evidence is None:
        raise OperationError("upgrade-evidence-required", "reviewed upgrade evidence is required")
    if isinstance(evidence, Path):
        evidence_path = _absolute(evidence)
        root = _safe_root(evidence_path.parent, "upgrade-evidence-root")
        if _is_link_or_reparse(evidence_path) or not evidence_path.is_file():
            raise OperationError("upgrade-evidence-invalid", "upgrade evidence must be one regular non-link file")
        document = load_yaml_input(evidence_path)
    else:
        if evidence_root is None:
            raise OperationError("upgrade-evidence-invalid", "in-memory upgrade evidence requires a bounded evidence root")
        root = _safe_root(evidence_root, "upgrade-evidence-root")
        document = evidence
    if not isinstance(document, dict):
        raise OperationError("upgrade-evidence-invalid", "upgrade evidence must be a mapping")
    schema_path = BUNDLED_SCHEMA_ROOT / "upgrade-evidence.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if list(Draft202012Validator(schema).iter_errors(document)):
        raise OperationError("upgrade-evidence-invalid", "upgrade evidence does not satisfy the trusted schema")
    review = document["review"]
    if review["owner_type"] != "human" or review["state"] != "approved":
        raise OperationError("upgrade-review-required", "an explicit human-reviewed upgrade decision is required")
    if document["from"] != from_identity or document["to"] != to_identity:
        raise OperationError("upgrade-evidence-mismatch", "upgrade evidence does not match package/OpenSpec identities")
    change = _load_yaml(root / "change.yaml")
    if change.get("id") != document["change_id"]:
        raise OperationError("upgrade-evidence-mismatch", "upgrade evidence does not match its reviewed change package")
    change_schema = json.loads((BUNDLED_SCHEMA_ROOT / "change-v2.schema.json").read_text(encoding="utf-8"))
    if list(Draft202012Validator(change_schema).iter_errors(change)):
        raise OperationError("upgrade-change-package-invalid", "reviewed upgrade change metadata is invalid")
    if change.get("decision", {}).get("state") not in {"confirmed", "corrected"}:
        raise OperationError("upgrade-review-required", "reviewed upgrade change decision is not confirmed")
    if not (root / "proposal.md").is_file() or not (root / "tasks.md").is_file():
        raise OperationError("upgrade-change-package-invalid", "reviewed upgrade change package is incomplete")
    delta_paths = change.get("spec_change", {}).get("delta_paths", [])
    if change.get("spec_change", {}).get("required") and (
        not delta_paths
        or any(
            not _local_reference(relative)
            or not _is_relative_to(_absolute(root / Path(relative)), root)
            or not _absolute(root / Path(relative)).is_file()
            for relative in delta_paths
        )
    ):
        raise OperationError("upgrade-change-package-invalid", "reviewed upgrade delta package is incomplete")
    references = [
        review["decision_ref"],
        *document["checks"]["compatibility_evidence_refs"],
        document["checks"]["openspec_strict"]["evidence_ref"],
    ]
    validator_check = document["checks"]["validator_templates"]
    if validator_check["status"] == "passed":
        references.append(validator_check["evidence_ref"])
    if any(not _local_reference(reference) for reference in references):
        raise OperationError("upgrade-evidence-invalid", "upgrade evidence references must be bounded local paths or IDs")
    digests = document["evidence_sha256"]
    if set(digests) != set(references):
        raise OperationError("upgrade-evidence-invalid", "upgrade evidence digest inventory must match its references")
    expected_results = {
        review["decision_ref"]: ("human-decision", "approved", "human"),
        **{
            reference: ("compatibility", "compatible", "deterministic-validator")
            for reference in document["checks"]["compatibility_evidence_refs"]
        },
        document["checks"]["openspec_strict"]["evidence_ref"]: (
            "openspec-strict", "passed", "deterministic-validator"
        ),
    }
    if validator_check["status"] == "passed":
        expected_results[validator_check["evidence_ref"]] = (
            "validator-templates", "passed", "deterministic-validator"
        )
    result_schema = json.loads(
        (BUNDLED_SCHEMA_ROOT / "upgrade-check-result.schema.json").read_text(encoding="utf-8")
    )
    for reference in references:
        referenced = _absolute(root / Path(reference.replace("\\", "/")))
        try:
            referenced.relative_to(root)
        except ValueError as error:
            raise OperationError("upgrade-evidence-invalid", "upgrade evidence reference escapes its package") from error
        if _is_link_or_reparse(referenced) or not referenced.is_file():
            raise OperationError("upgrade-evidence-reference-missing", "upgrade evidence reference is missing or unsafe")
        if hashlib.sha256(referenced.read_bytes()).hexdigest() != digests[reference]:
            raise OperationError("upgrade-evidence-digest-mismatch", "upgrade evidence reference digest does not match")
        result = _load_yaml(referenced)
        if list(Draft202012Validator(result_schema).iter_errors(result)):
            raise OperationError("upgrade-evidence-result-invalid", "upgrade evidence result is not schema-valid")
        expected_kind, expected_status, expected_producer = expected_results[reference]
        if (
            result.get("evidence_kind") != expected_kind
            or result.get("status") != expected_status
            or result.get("produced_by") != expected_producer
            or result.get("change_id") != document["change_id"]
            or result.get("from") != from_identity
            or result.get("to") != to_identity
        ):
            raise OperationError("upgrade-evidence-result-invalid", "upgrade evidence result does not prove the declared check")
    return {
        "change_id": str(document["change_id"]),
        "review_state": str(review["state"]),
        "decision_ref": str(review["decision_ref"]),
        "rollback_or_hold": str(document["rollback_or_hold"]["strategy"]),
    }


def rollback_process_package(
    installed_root: Path, backup_root: Path, config_path: Path
) -> dict[str, Any]:
    """Restore a retained compatible package/config pin transactionally."""
    installed_root = _safe_root(installed_root, "installed-package")
    backup_root = _safe_root(backup_root, "rollback-package")
    config_path = _absolute(config_path)
    config = _load_yaml(config_path)
    current = _validate_standalone_package(installed_root, config)["identity"]
    target = _validate_standalone_package(backup_root, config, require_config_version=False)["identity"]
    proof = backup_root.parent / f"{backup_root.name}.rollback.yaml"
    if not proof.is_file():
        raise OperationError("rollback-proof-invalid", "rollback snapshot proof is missing or invalid")
    try:
        proof_data = _load_yaml(proof)
    except OperationError as error:
        raise OperationError("rollback-proof-invalid", "rollback snapshot proof is missing or invalid") from error
    if (
        proof_data.get("schema_version") != "1.0"
        or proof_data.get("from_version") != target["version"]
        or proof_data.get("to_version") != current["version"]
        or proof_data.get("snapshot_sha256") != _snapshot_digest(backup_root)
    ):
        raise OperationError("rollback-proof-invalid", "rollback snapshot proof is missing or invalid")
    _assert_config_pin(config, current, installed_root, config_path.parent)
    gigacode_changes = _prepare_gigacode_update(
        installed_root, backup_root, installed_root.parent
    )
    original_config = config_path.read_bytes()
    displaced = installed_root.with_name(f".{installed_root.name}.rollback-current")
    staged = installed_root.with_name(f".{installed_root.name}.rollback-target")
    if displaced.exists() or staged.exists():
        raise OperationError("staging-exists", "rollback staging path already exists")
    try:
        _copy_versioned_tree(backup_root, staged)
        shutil.move(str(installed_root), str(displaced))
        shutil.move(str(staged), str(installed_root))
        config["process_package"]["version"] = target["version"]
        _write_yaml_atomic(config_path, config)
        _apply_gigacode_updates(gigacode_changes)
        shutil.rmtree(displaced)
    except Exception:
        _restore_gigacode_updates(gigacode_changes)
        if staged.exists():
            shutil.rmtree(staged)
        if installed_root.exists() and displaced.exists():
            shutil.rmtree(installed_root)
        if displaced.exists():
            shutil.move(str(displaced), str(installed_root))
        config_path.write_bytes(original_config)
        raise
    return {
        "schema_version": "1.0",
        "operation": "rollback-process-package",
        "status": "rolled-back",
        "from_version": current["version"],
        "to_version": target["version"],
        "accepted_history_mutated": False,
        "ai_disabled": True,
    }


def _prepare_review(package_root: Path, change_root: Path, operation: str) -> dict[str, Any]:
    package = _load_yaml(package_root.resolve() / "package.yaml")
    change_root = change_root.resolve()
    change = _load_yaml(change_root / "change.yaml")
    if change.get("schema_version") != 2 or change.get("classification") not in CLASSIFICATIONS:
        raise OperationError("change-invalid", "schema-v2 class-aware change metadata is required")
    evidence = _evidence(operation, "prepared-for-human-review", package, change_root, change_root.rglob("*"))
    evidence.update({
        "change_id": change.get("id"),
        "policy": dict(change.get("policy", {})),
        "approved": False,
        "merged": False,
        "archived": False,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    })
    return evidence


def _package_identity(root: Path) -> dict[str, str]:
    package = _load_yaml(root / "package.yaml")
    identity = package.get("package")
    version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else ""
    if not isinstance(identity, dict) or identity.get("id") != "sdd-process":
        raise OperationError("package-invalid", "package identity is invalid")
    if identity.get("version") != version:
        raise OperationError("package-version-mismatch", "package.yaml and VERSION differ")
    return {"id": str(identity["id"]), "version": str(version)}


def _assert_config_pin(config: dict[str, Any], identity: dict[str, str], installed: Path, central: Path) -> None:
    pin = config.get("process_package")
    if not isinstance(pin, dict) or pin.get("id") != identity["id"] or pin.get("version") != identity["version"]:
        raise OperationError("config-pin-mismatch", "configuration does not pin the installed package")
    location = pin.get("location")
    if not isinstance(location, str) or (central / location).resolve() != installed:
        raise OperationError("config-location-mismatch", "configuration location does not identify the installed package")


def _write_yaml_atomic(path: Path, value: dict[str, Any]) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", delete=False, dir=path.parent, suffix=".tmp") as handle:
        yaml.safe_dump(value, handle, sort_keys=False)
        temporary = Path(handle.name)
    temporary.replace(path)


def _local_reference(value: Any) -> bool:
    if not isinstance(value, str) or not value or "://" in value or value.startswith(("/", "\\")):
        return False
    return ".." not in Path(value.replace("\\", "/")).parts


def _copy_versioned_tree(source: Path, destination: Path) -> None:
    source = _safe_root(source, "copy-source")
    destination = _absolute(destination)
    _assert_non_overlapping(source, destination)
    package_path = source / "package.yaml"
    if package_path.is_file():
        package = _load_yaml(package_path)
        distribution = package.get("distribution")
        if not isinstance(distribution, dict):
            raise OperationError("package-contract-invalid", "distribution manifest is missing")
        destination.mkdir(parents=True)
        for relative in distribution.get("roots", []):
            source_root = _declared_directory(source, relative)
            shutil.copytree(
                source_root, destination / relative,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
        for relative in distribution.get("files", []):
            source_file = _declared_file(source, relative)
            destination_file = destination / relative
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, destination_file)
        return
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))


def _install_gigacode_templates(package_root: Path, workspace_root: Path) -> None:
    """Install declared GigaCode templates into a new empty workspace."""
    _apply_gigacode_updates(_prepare_gigacode_update(None, package_root, workspace_root))


def _prepare_gigacode_update(
    installed_root: Path | None, candidate_root: Path, workspace_root: Path
) -> list[tuple[Path | None, Path, bytes | None]]:
    """Return safe managed-file writes/deletes; fail before mutating local overrides."""
    candidate_files = _gigacode_template_files(candidate_root)
    previous_files = _gigacode_template_files(installed_root) if installed_root is not None else {}
    if not candidate_files and not previous_files:
        return []
    workspace = _absolute(workspace_root)
    managed_root = workspace / ".gigacode"
    if managed_root.exists() and (not managed_root.is_dir() or _is_link_or_reparse(managed_root)):
        raise OperationError("gigacode-target-unsafe", "managed .gigacode target must be a regular directory")
    changes: list[tuple[Path | None, Path, bytes | None]] = []
    for relative in sorted(candidate_files.keys() | previous_files.keys()):
        source = candidate_files.get(relative)
        previous = previous_files.get(relative)
        target = managed_root / relative
        try:
            target.relative_to(managed_root)
        except ValueError as error:
            raise OperationError("gigacode-target-unsafe", "managed GigaCode file escapes .gigacode") from error
        if target.exists():
            if not target.is_file() or _is_link_or_reparse(target):
                raise OperationError("gigacode-managed-file-conflict", target.as_posix())
            current = target.read_bytes()
            if source is not None and current == source.read_bytes():
                continue
            if previous is None or current != previous.read_bytes():
                raise OperationError("gigacode-managed-file-conflict", target.as_posix())
            changes.append((source, target, current))
        elif source is not None:
            changes.append((source, target, None))
    return changes


def _gigacode_template_files(package_root: Path | None) -> dict[str, Path]:
    if package_root is None:
        return {}
    package = _load_yaml(package_root / "package.yaml")
    contract = package.get("gigacode")
    if contract is None:
        return {}
    if not isinstance(contract, dict) or contract.get("target") != ".gigacode":
        raise OperationError("package-contract-invalid", "GigaCode manifest target is invalid")
    files = contract.get("files")
    if not isinstance(files, list) or not files:
        raise OperationError("package-contract-invalid", "GigaCode manifest files are missing")
    template_root = _declared_directory(package_root, "gigacode")
    result: dict[str, Path] = {}
    for relative in files:
        if not isinstance(relative, str) or relative in result:
            raise OperationError("package-contract-invalid", "GigaCode manifest file is invalid")
        result[relative] = _declared_file(template_root, relative)
    return result


def _apply_gigacode_updates(
    changes: list[tuple[Path | None, Path, bytes | None]],
) -> None:
    for source, target, _ in changes:
        if source is None:
            target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        _write_bytes_atomic(target, source.read_bytes())


def _restore_gigacode_updates(
    changes: list[tuple[Path | None, Path, bytes | None]],
) -> None:
    for _, target, original in reversed(changes):
        if original is None:
            if target.exists():
                target.unlink()
        else:
            _write_bytes_atomic(target, original)


def _write_bytes_atomic(path: Path, payload: bytes) -> None:
    staging = path.with_name(f".{path.name}.candidate")
    if staging.exists():
        raise OperationError("staging-exists", "managed GigaCode staging path already exists")
    try:
        staging.write_bytes(payload)
        os.replace(staging, path)
    finally:
        if staging.exists():
            staging.unlink()

def _validate_standalone_package(
    root: Path,
    config: dict[str, Any] | None = None,
    *,
    require_config_version: bool = True,
) -> dict[str, Any]:
    """Validate one package snapshot without discovery, runtime, or mutation."""
    root = _safe_root(root, "package")
    resources = load_schema_resources(_declared_directory(root, "schemas"))
    package = _load_yaml(root / "package.yaml")
    diagnostics = schema_diagnostics(
        "process-package.schema.json", package, "process-package", stage=1,
        schema_resources=resources,
    )
    if diagnostics:
        raise OperationError("package-contract-invalid", "package manifest does not satisfy the trusted schema")
    identity = _package_identity(root)

    workflow_path = _declared_file(root, package.get("workflow"))
    workflow = _load_yaml(workflow_path)
    if schema_diagnostics(
        "workflow.schema.json", workflow, "process-workflow", stage=1,
        schema_resources=resources,
    ):
        raise OperationError("package-workflow-invalid", "declared workflow is invalid")

    schemas = package.get("schemas")
    if not isinstance(schemas, dict):
        raise OperationError("package-contract-invalid", "schema declarations are missing")
    for relative in schemas.values():
        _declared_file(root, relative)
    schema_result = ValidationResult()
    validate_package_schemas(root, schemas, schema_result)
    if schema_result.diagnostics:
        raise OperationError("package-schema-invalid", "a declared package schema is invalid")

    templates = package.get("templates")
    if not isinstance(templates, dict):
        raise OperationError("package-contract-invalid", "template declarations are missing")
    for relative in templates.values():
        _declared_file(root, relative)

    catalogs = package.get("catalogs")
    if not isinstance(catalogs, dict):
        raise OperationError("package-contract-invalid", "catalog declarations are missing")
    guided_workflow_path = _declared_file(root, catalogs.get("guided_owner_workflow"))
    operations_reference = catalogs.get("operations")
    if operations_reference is not None:
        operations_path = _declared_file(root, operations_reference)
        load_operations_catalog(operations_path)
        load_catalog(guided_workflow_path, operations_path=operations_path)

    distribution = package.get("distribution")
    if not isinstance(distribution, dict):
        raise OperationError("package-contract-invalid", "distribution manifest is missing")
    declared_files = set(distribution.get("files", []))
    declared_roots = set(distribution.get("roots", []))
    for relative in declared_files:
        _declared_file(root, relative)
    for relative in declared_roots:
        _declared_directory(root, relative)
    for child in root.iterdir():
        if child.name in {"__pycache__", ".DS_Store"}:
            continue
        # Frozen host/release evidence is retained beside the trusted repository
        # source package, but is deliberately absent from standalone candidates.
        if child.name == "release" and root == BUNDLED_PACKAGE_ROOT:
            continue
        if child.is_file() and child.name not in declared_files:
            raise OperationError("package-asset-undeclared", "package root contains an undeclared file")
        if child.is_dir() and child.name not in declared_roots:
            raise OperationError("package-asset-undeclared", "package root contains an undeclared directory")

    policy_manifest_path = _declared_file(root, package.get("policies"))
    manifest = _load_yaml(policy_manifest_path)
    if schema_diagnostics(
        "policy-manifest.schema.json", manifest, "policy-manifest", stage=1,
        schema_resources=resources,
    ):
        raise OperationError("package-policy-invalid", "policy manifest is invalid")
    policy_config = config or {
        "policy_set": {
            "id": "sdd-core", "version": "1.0.0",
            "corporate_values": {
                "tech_lead_owner": "sample-tech-leads",
                "qa_owner": "sample-qa-owners",
                "escalation_route": "sample-tech-leads",
                "evidence_retention_days": 30,
            },
            "overrides": [],
        }
    }
    policy_result = validate_policy_bundle(root, manifest, policy_config, None)
    if policy_result.snapshot is None or policy_result.diagnostics:
        raise OperationError("package-policy-invalid", "declared policies are incomplete or incompatible")

    for relative in package.get("canonical_sources", []):
        if not _local_reference(relative):
            raise OperationError("package-reference-invalid", "canonical source reference is unsafe")

    if config is not None:
        config_schema_errors = schema_diagnostics(
            "sdd-config.schema.json", config, "central-config", stage=1,
            schema_resources=resources,
        )
        config_compatibility_errors = [
            item for item in config_compatibility(config)
            if item.code != "compat.package-version"
        ]
        if config_schema_errors or config_compatibility_errors:
            raise OperationError("config-contract-invalid", "configuration is invalid or incompatible")
        compatibility = package_compatibility(
            config, package, workflow, identity["version"], None
        )
        trusted_compatibility = [
            item for item in compatibility if item.code != "compat.package-version"
        ]
        if require_config_version and trusted_compatibility:
            raise OperationError("package-compatibility-invalid", "package and configuration are incompatible")
        if not require_config_version:
            non_version = [
                item for item in compatibility
                if item.code not in {"compat.package-version", "compat.config-package-version"}
            ]
            if non_version:
                raise OperationError("package-compatibility-invalid", "candidate package is incompatible")
    return {"package": package, "workflow": workflow, "identity": identity}


def _declared_file(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not _local_reference(relative):
        raise OperationError("package-reference-invalid", "declared package path is unsafe")
    path = _absolute(root / Path(*relative.replace("\\", "/").split("/")))
    try:
        path.relative_to(root)
    except ValueError as error:
        raise OperationError("package-reference-invalid", "declared package path escapes the package") from error
    if not path.is_file():
        raise OperationError("package-asset-missing", "a declared package asset is missing")
    return path


def _declared_directory(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not _local_reference(relative):
        raise OperationError("package-reference-invalid", "declared package directory is unsafe")
    path = _absolute(root / Path(*relative.replace("\\", "/").split("/")))
    try:
        path.relative_to(root)
    except ValueError as error:
        raise OperationError("package-reference-invalid", "declared package directory escapes the package") from error
    if not path.is_dir():
        raise OperationError("package-asset-missing", "a declared package directory is missing")
    return path


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _safe_root(path: Path, label: str) -> Path:
    root = _absolute(path)
    if not root.is_dir():
        raise OperationError("input-invalid", f"{label} is not a directory", exit_code=3)
    _assert_path_identity_safe(root)
    _assert_safe_tree(root)
    return root


def _assert_path_identity_safe(path: Path) -> None:
    """Reject a root or existing ancestry redirected through a link/reparse point."""
    absolute = _absolute(path)
    try:
        resolved = absolute.resolve(strict=True)
        info = absolute.lstat()
    except (OSError, RuntimeError) as error:
        raise OperationError("filesystem-link-forbidden", "path identity cannot be verified") from error
    attributes = getattr(info, "st_file_attributes", 0)
    if (
        resolved != absolute
        or stat.S_ISLNK(info.st_mode)
        or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    ):
        raise OperationError("filesystem-link-forbidden", "links and reparse points are forbidden")


def _is_link_or_reparse(path: Path) -> bool:
    try:
        info = path.lstat()
    except OSError:
        return False
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(
        attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def _assert_safe_tree(root: Path) -> None:
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        for name in [*directories, *files]:
            path = Path(current) / name
            info = path.lstat()
            attributes = getattr(info, "st_file_attributes", 0)
            if stat.S_ISLNK(info.st_mode) or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
                raise OperationError("filesystem-link-forbidden", "links and reparse points are forbidden")


def _assert_non_overlapping(source: Path, destination: Path) -> None:
    if _is_relative_to(destination, source):
        raise OperationError("filesystem-overlap-forbidden", "copy destination overlaps its source")
    if _is_relative_to(source, destination):
        raise OperationError("filesystem-overlap-forbidden", "copy source overlaps its destination")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _semver(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", value)
    if match is None:
        raise OperationError("package-version-invalid", "package version must be semantic x.y.z")
    return tuple(int(part) for part in match.groups())


def _snapshot_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.as_posix()):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("input-invalid", "required YAML is missing or malformed", exit_code=3) from error
    if not isinstance(value, dict):
        raise OperationError("input-invalid", "required YAML root must be a mapping", exit_code=3)
    return value


def _evidence(
    operation: str,
    status: str,
    package: dict[str, Any],
    root: Path,
    paths: Any,
) -> dict[str, Any]:
    files = []
    for path in sorted((item for item in paths if item.is_file()), key=lambda item: item.as_posix()):
        files.append({
            "path": path.relative_to(root).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return {
        "schema_version": "1.0",
        "operation": operation,
        "status": status,
        "package": dict(package["package"]),
        "files": files,
        "ai_disabled": True,
        "human_authority_substituted": False,
    }
