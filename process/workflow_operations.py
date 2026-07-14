"""Deterministic package/bootstrap workflow operations.

The module owns bounded filesystem preparation only. It never records human
approval, mutates lifecycle state, calls an integration, or infers authority.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml


CHANGE_ID = re.compile(r"^[a-z][a-z0-9-]*$")
CLASSIFICATIONS = {"minor", "major", "hotfix"}
CHANGE_TYPES = {
    "new_feature", "behavior_change", "bugfix", "refactor", "docs_only", "config_ops"
}
TRACEABILITY_FIELDS = {
    "classification_refs",
    "gate_refs",
    "control_refs",
    "release_refs",
    "waiver_deferral_refs",
    "hotfix_reconciliation_refs",
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


class OperationError(ValueError):
    """Stable operator-safe workflow error."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def bootstrap_team_specs(
    package_root: Path, team_template: Path, destination: Path
) -> dict[str, Any]:
    """Create one synthetic central workspace from immutable package sources."""
    package_root = package_root.resolve()
    team_template = team_template.resolve()
    destination = destination.resolve()
    package = _load_yaml(package_root / "package.yaml")
    if package.get("package", {}).get("id") != "sdd-process":
        raise OperationError("package-invalid", "expected the sdd-process package")
    if not (package_root / "VERSION").is_file():
        raise OperationError("package-invalid", "VERSION is missing")
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
    package_root = package_root.resolve()
    changes_root = changes_root.resolve()
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


def prepare_archive(package_root: Path, change_root: Path) -> dict[str, Any]:
    """Collect archive-review evidence without changing canonical lifecycle state."""
    return _prepare_review(package_root, change_root, "prepare-archive")


def validate_traceability(document: dict[str, Any]) -> dict[str, Any]:
    """Validate canonical governance links and return a derived ID-only view."""
    if document.get("schema_version") != "2.0":
        raise OperationError("traceability-schema-invalid", "schema_version must be 2.0")
    classification = document.get("classification")
    lifecycle_state = document.get("lifecycle_state")
    if classification not in CLASSIFICATIONS or lifecycle_state not in {
        "draft", "spec_review", "approved", "in_implementation", "ready_to_archive", "archived"
    }:
        raise OperationError("traceability-context-invalid", "class and lifecycle context are required")
    policy = document.get("policy")
    if policy != {"id": "sdd-core", "version": "1.0.0"}:
        raise OperationError("traceability-policy-invalid", "canonical policy identity is required")
    links = document.get("links")
    if not isinstance(links, list) or not links:
        raise OperationError("traceability-links-missing", "at least one link is required")
    identifiers: list[str] = []
    for link in links:
        if not isinstance(link, dict) or not CHANGE_ID.fullmatch(str(link.get("record_id", ""))):
            raise OperationError("traceability-id-invalid", "each link requires a canonical record id")
        if not _nonempty_strings(link.get("requirement_refs")) or not _nonempty_strings(link.get("scenario_refs")):
            raise OperationError("traceability-source-missing", "requirement and scenario references are required")
        if not _nonempty_strings(link.get("classification_refs")) or not _nonempty_strings(link.get("gate_refs")):
            raise OperationError(
                "traceability-link-incomplete",
                "classification and gate links are required",
            )
        if lifecycle_state in {"ready_to_archive", "archived"} and not _nonempty_strings(link.get("release_refs")):
            raise OperationError("traceability-link-incomplete", "release evidence is required at archive readiness")
        if classification == "hotfix" and lifecycle_state in {"ready_to_archive", "archived"} and not _nonempty_strings(link.get("hotfix_reconciliation_refs")):
            raise OperationError("traceability-link-incomplete", "hotfix reconciliation is required at archive readiness")
        for field in TRACEABILITY_FIELDS | {"requirement_refs", "scenario_refs", "task_refs"}:
            references = link.get(field)
            if not isinstance(references, list) or any(not isinstance(item, str) or not item for item in references):
                raise OperationError("traceability-reference-invalid", "reference collections must contain strings")
            for reference in references:
                if not _local_reference(reference):
                    raise OperationError("traceability-reference-invalid", "references must be bounded local IDs or paths")
        identifiers.append(str(link["record_id"]))
    if len(set(identifiers)) != len(identifiers):
        raise OperationError("traceability-id-duplicate", "record ids must be unique")
    return {
        "schema_version": "1.0",
        "status": "valid",
        "policy": dict(policy),
        "classification": classification,
        "lifecycle_state": lifecycle_state,
        "record_ids": sorted(identifiers),
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
) -> dict[str, Any]:
    """Install a compatible package transactionally while retaining rollback state."""
    installed_root = installed_root.resolve()
    candidate_root = candidate_root.resolve()
    config_path = config_path.resolve()
    backup_root = backup_root.resolve()
    installed = _package_identity(installed_root)
    candidate = _package_identity(candidate_root)
    config = _load_yaml(config_path)
    _assert_config_pin(config, installed, installed_root, config_path.parent)
    if candidate["id"] != installed["id"]:
        raise OperationError("package-id-mismatch", "candidate package id differs")
    if candidate["version"] == installed["version"]:
        raise OperationError("package-version-unchanged", "candidate version is already installed")
    backup = backup_root / installed["version"]
    if backup.exists():
        raise OperationError("rollback-exists", "rollback snapshot already exists")
    backup_root.mkdir(parents=True, exist_ok=True)
    _copy_versioned_tree(installed_root, backup)
    original_config = config_path.read_bytes()
    displaced = installed_root.with_name(f".{installed_root.name}.previous")
    staged = installed_root.with_name(f".{installed_root.name}.candidate")
    if displaced.exists() or staged.exists():
        shutil.rmtree(backup)
        raise OperationError("staging-exists", "update staging path already exists")
    try:
        _copy_versioned_tree(candidate_root, staged)
        shutil.move(str(installed_root), str(displaced))
        shutil.move(str(staged), str(installed_root))
        config["process_package"]["version"] = candidate["version"]
        _write_yaml_atomic(config_path, config)
        shutil.rmtree(displaced)
    except Exception:
        if staged.exists():
            shutil.rmtree(staged)
        if installed_root.exists() and displaced.exists():
            shutil.rmtree(installed_root)
        if displaced.exists():
            shutil.move(str(displaced), str(installed_root))
        config_path.write_bytes(original_config)
        if backup.exists():
            shutil.rmtree(backup)
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
    }


def check_package_compatibility(
    installed_root: Path, candidate_root: Path, config_path: Path
) -> dict[str, Any]:
    """Check update inputs without writing package, config, or history."""
    installed_root = installed_root.resolve()
    installed = _package_identity(installed_root)
    candidate = _package_identity(candidate_root.resolve())
    config = _load_yaml(config_path.resolve())
    _assert_config_pin(config, installed, installed_root, config_path.resolve().parent)
    if installed["id"] != candidate["id"]:
        raise OperationError("package-id-mismatch", "candidate package id differs")
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
    }


def rollback_process_package(
    installed_root: Path, backup_root: Path, config_path: Path
) -> dict[str, Any]:
    """Restore a retained compatible package/config pin transactionally."""
    installed_root = installed_root.resolve()
    backup_root = backup_root.resolve()
    config_path = config_path.resolve()
    current = _package_identity(installed_root)
    target = _package_identity(backup_root)
    config = _load_yaml(config_path)
    _assert_config_pin(config, current, installed_root, config_path.parent)
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
        shutil.rmtree(displaced)
    except Exception:
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


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def _local_reference(value: Any) -> bool:
    if not isinstance(value, str) or not value or "://" in value or value.startswith(("/", "\\")):
        return False
    return ".." not in Path(value.replace("\\", "/")).parts


def _copy_versioned_tree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("input-invalid", "required YAML is missing or malformed") from error
    if not isinstance(value, dict):
        raise OperationError("input-invalid", "required YAML root must be a mapping")
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
