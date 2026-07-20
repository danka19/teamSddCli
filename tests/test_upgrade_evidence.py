import shutil
import hashlib
from pathlib import Path

import pytest
import yaml

from process.errors import OperationError
from process.workflow_operations import (
    check_package_compatibility,
    update_process_package,
    validate_reviewed_upgrade_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
TEAM_TEMPLATE = ROOT / "templates" / "team-specs"


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_yaml(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def update_fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    installed = tmp_path / "process"
    candidate = tmp_path / "candidate"
    shutil.copytree(PROCESS, installed, ignore=shutil.ignore_patterns("release"))
    shutil.copytree(PROCESS, candidate, ignore=shutil.ignore_patterns("release"))
    package = load_yaml(candidate / "package.yaml")
    package["package"]["version"] = "0.4.0"
    write_yaml(candidate / "package.yaml", package)
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    central = tmp_path / "team-specs"
    shutil.copytree(TEAM_TEMPLATE, central)
    config = load_yaml(central / "sdd.config.yaml")
    config["process_package"]["location"] = "../process"
    write_yaml(central / "sdd.config.yaml", config)
    return installed, candidate, central / "sdd.config.yaml", tmp_path / "backups"


def reviewed_evidence() -> dict:
    return {
        "schema_version": "1.0",
        "change_id": "close-release-integrity-gaps",
        "review": {
            "owner_type": "human",
            "state": "approved",
            "decision_ref": "decisions/process-upgrade.yaml",
        },
        "from": {"package_version": "0.3.0", "openspec_version": "1.4.1"},
        "to": {"package_version": "0.4.0", "openspec_version": "1.4.1"},
        "checks": {
            "compatibility_evidence_refs": ["evidence/package-compatibility.json"],
            "openspec_strict": {"status": "passed", "evidence_ref": "evidence/openspec-strict.txt"},
            "validator_templates": {"status": "passed", "evidence_ref": "evidence/validator-templates.txt"},
        },
        "rollback_or_hold": {
            "strategy": "rollback",
            "instructions": "Restore the retained package snapshot and configuration pin.",
        },
        "evidence_sha256": {},
    }


def materialize_evidence(root: Path, document: dict | None = None) -> Path:
    value = reviewed_evidence() if document is None else document
    root.mkdir(parents=True, exist_ok=True)
    change = load_yaml(PROCESS / "templates" / "change-v2" / "change.yaml")
    change["id"] = value["change_id"]
    change["decision"]["state"] = "confirmed"
    write_yaml(root / "change.yaml", change)
    (root / "proposal.md").write_text("# Reviewed process upgrade\n", encoding="utf-8")
    (root / "tasks.md").write_text("# Tasks\n\n- [x] Verify upgrade.\n", encoding="utf-8")
    delta = root / change["spec_change"]["delta_paths"][0]
    delta.parent.mkdir(parents=True, exist_ok=True)
    delta.write_text("## MODIFIED Requirements\n", encoding="utf-8")
    references = [
        value["review"]["decision_ref"],
        *value["checks"]["compatibility_evidence_refs"],
        value["checks"]["openspec_strict"]["evidence_ref"],
    ]
    validator = value["checks"]["validator_templates"]
    if validator["status"] == "passed":
        references.append(validator["evidence_ref"])
    value["evidence_sha256"] = {}
    for reference in references:
        path = root / reference
        path.parent.mkdir(parents=True, exist_ok=True)
        if reference == value["review"]["decision_ref"]:
            kind, status, producer = "human-decision", "approved", "human"
        elif reference in value["checks"]["compatibility_evidence_refs"]:
            kind, status, producer = "compatibility", "compatible", "deterministic-validator"
        elif reference == value["checks"]["openspec_strict"]["evidence_ref"]:
            kind, status, producer = "openspec-strict", "passed", "deterministic-validator"
        else:
            kind, status, producer = "validator-templates", "passed", "deterministic-validator"
        write_yaml(path, {
            "schema_version": "1.0", "evidence_kind": kind,
            "change_id": value["change_id"], "from": value["from"], "to": value["to"],
            "status": status, "produced_by": producer,
        })
        value["evidence_sha256"][reference] = hashlib.sha256(path.read_bytes()).hexdigest()
    evidence_path = root / "upgrade-evidence.yaml"
    write_yaml(evidence_path, value)
    return evidence_path


def test_process_package_upgrade_requires_reviewed_evidence(tmp_path: Path) -> None:
    installed, candidate, config, backups = update_fixture(tmp_path)
    installed_before = (installed / "VERSION").read_bytes()

    with pytest.raises(OperationError, match="upgrade-evidence-required"):
        update_process_package(installed, candidate, config, backups)
    assert (installed / "VERSION").read_bytes() == installed_before
    assert not backups.exists()

    ai_only = reviewed_evidence()
    ai_only["review"]["owner_type"] = "ai"
    with pytest.raises(OperationError, match="upgrade-review-required"):
        check_package_compatibility(
            installed, candidate, config,
            upgrade_evidence=materialize_evidence(tmp_path / "ai-only", ai_only),
        )

    mismatched = reviewed_evidence()
    mismatched["to"]["package_version"] = "0.5.0"
    with pytest.raises(OperationError, match="upgrade-evidence-mismatch"):
        check_package_compatibility(
            installed, candidate, config,
            upgrade_evidence=materialize_evidence(tmp_path / "mismatched", mismatched),
        )

    incomplete = reviewed_evidence()
    del incomplete["rollback_or_hold"]
    with pytest.raises(OperationError, match="upgrade-evidence-invalid"):
        validate_reviewed_upgrade_evidence(
            materialize_evidence(tmp_path / "incomplete", incomplete),
            from_identity={"package_version": "0.3.0", "openspec_version": "1.4.1"},
            to_identity={"package_version": "0.4.0", "openspec_version": "1.4.1"},
        )

    report = check_package_compatibility(
        installed, candidate, config,
        upgrade_evidence=materialize_evidence(tmp_path / "valid"),
    )
    assert report["upgrade_evidence"] == {
        "change_id": "close-release-integrity-gaps",
        "review_state": "approved",
        "decision_ref": "decisions/process-upgrade.yaml",
        "rollback_or_hold": "rollback",
    }


def test_upgrade_evidence_accepts_explicit_non_applicability(tmp_path: Path) -> None:
    installed, candidate, config, _ = update_fixture(tmp_path)
    evidence = reviewed_evidence()
    evidence["checks"]["validator_templates"] = {
        "status": "not_applicable",
        "reason": "No validator or template surface changes in this package update.",
    }

    assert check_package_compatibility(
        installed, candidate, config,
        upgrade_evidence=materialize_evidence(tmp_path / "not-applicable", evidence),
    )["status"] == "compatible"

    missing = materialize_evidence(tmp_path / "missing")
    (missing.parent / "evidence" / "openspec-strict.txt").unlink()
    with pytest.raises(OperationError, match="upgrade-evidence-reference-missing"):
        check_package_compatibility(installed, candidate, config, upgrade_evidence=missing)

    tampered = materialize_evidence(tmp_path / "tampered")
    (tampered.parent / "evidence" / "package-compatibility.json").write_text(
        "tampered\n", encoding="utf-8"
    )
    with pytest.raises(OperationError, match="upgrade-evidence-digest-mismatch"):
        check_package_compatibility(installed, candidate, config, upgrade_evidence=tampered)

    invalid_result = materialize_evidence(tmp_path / "invalid-result")
    invalid_document = load_yaml(invalid_result)
    result_path = invalid_result.parent / "evidence" / "openspec-strict.txt"
    result = load_yaml(result_path)
    result["status"] = "compatible"
    write_yaml(result_path, result)
    invalid_document["evidence_sha256"]["evidence/openspec-strict.txt"] = hashlib.sha256(
        result_path.read_bytes()
    ).hexdigest()
    write_yaml(invalid_result, invalid_document)
    with pytest.raises(OperationError, match="upgrade-evidence-result-invalid"):
        check_package_compatibility(installed, candidate, config, upgrade_evidence=invalid_result)

    invalid_change = materialize_evidence(tmp_path / "invalid-change")
    write_yaml(invalid_change.parent / "change.yaml", {"id": "close-release-integrity-gaps"})
    with pytest.raises(OperationError, match="upgrade-change-package-invalid"):
        check_package_compatibility(installed, candidate, config, upgrade_evidence=invalid_change)


SCENARIO_COVERAGE = {
    "test_process_package_upgrade_requires_reviewed_evidence": [
        {
            "source_kind": "delta",
            "capability": "repo-topology-config",
            "requirement": "OpenSpec version pin and upgrade policy",
            "scenario": "Upgrade requires reviewed evidence",
        }
    ]
}
