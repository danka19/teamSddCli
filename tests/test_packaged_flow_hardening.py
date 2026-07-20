"""Adversarial regressions for packaged-flow review findings."""

from __future__ import annotations

import os
import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from process import workflow_operations as operations
from process.workflow_operations import (
    OperationError,
    check_package_compatibility,
    update_process_package,
    rollback_process_package,
    validate_traceability,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"


def _upgrade_evidence(root: Path) -> Path:
    document = {
        "schema_version": "1.0",
        "change_id": "synthetic-process-upgrade",
        "review": {"owner_type": "human", "state": "approved", "decision_ref": "decisions/process-upgrade.yaml"},
        "from": {"package_version": "0.3.0", "openspec_version": "1.4.1"},
        "to": {"package_version": "0.4.0", "openspec_version": "1.4.1"},
        "checks": {
            "compatibility_evidence_refs": ["evidence/package-compatibility.json"],
            "openspec_strict": {"status": "passed", "evidence_ref": "evidence/openspec-strict.txt"},
            "validator_templates": {"status": "passed", "evidence_ref": "evidence/validator-templates.txt"},
        },
        "rollback_or_hold": {"strategy": "rollback", "instructions": "Restore the retained package snapshot and configuration pin."},
        "evidence_sha256": {},
    }
    root.mkdir(parents=True, exist_ok=True)
    change = _yaml(PROCESS / "templates" / "change-v2" / "change.yaml")
    change["id"] = document["change_id"]
    change["decision"]["state"] = "confirmed"
    (root / "change.yaml").write_text(yaml.safe_dump(change, sort_keys=False), encoding="utf-8")
    (root / "proposal.md").write_text("# Reviewed process upgrade\n", encoding="utf-8")
    (root / "tasks.md").write_text("# Tasks\n\n- [x] Verify upgrade.\n", encoding="utf-8")
    delta = root / change["spec_change"]["delta_paths"][0]
    delta.parent.mkdir(parents=True, exist_ok=True)
    delta.write_text("## MODIFIED Requirements\n", encoding="utf-8")
    references = ["decisions/process-upgrade.yaml", "evidence/package-compatibility.json", "evidence/openspec-strict.txt", "evidence/validator-templates.txt"]
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
        }, sort_keys=False), encoding="utf-8")
        document["evidence_sha256"][reference] = hashlib.sha256(path.read_bytes()).hexdigest()
    evidence = root / "upgrade-evidence.yaml"
    evidence.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return evidence
TEAM_TEMPLATE = ROOT / "templates" / "team-specs"


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_yaml(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def _update_fixture(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    installed = tmp_path / "process"
    candidate = tmp_path / "candidate"
    central = tmp_path / "team-specs"
    backups = tmp_path / "rollbacks"
    package_ignore = shutil.ignore_patterns("__pycache__", "*.pyc", "release")
    shutil.copytree(PROCESS, installed, ignore=package_ignore)
    shutil.copytree(PROCESS, candidate, ignore=package_ignore)
    shutil.copytree(TEAM_TEMPLATE, central)
    package = _yaml(candidate / "package.yaml")
    package["package"]["version"] = "0.4.0"
    _write_yaml(candidate / "package.yaml", package)
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    config = _yaml(central / "sdd.config.yaml")
    config["process_package"]["location"] = "../process"
    _write_yaml(central / "sdd.config.yaml", config)
    return installed, candidate, central / "sdd.config.yaml", backups


def test_repository_release_evidence_is_not_treated_as_a_distribution_root(
    tmp_path: Path,
) -> None:
    operations._validate_standalone_package(PROCESS)
    installed, candidate, config, _ = _update_fixture(tmp_path)
    (candidate / "release").mkdir()
    (candidate / "release" / "injected.txt").write_text("undeclared", encoding="utf-8")

    with pytest.raises(OperationError, match="package-asset-undeclared"):
        check_package_compatibility(installed, candidate, config)


def test_standalone_package_validation_rejects_missing_declared_asset_before_write(
    tmp_path: Path,
) -> None:
    installed, candidate, config, backups = _update_fixture(tmp_path)
    (candidate / "schemas" / "external-mapping.schema.json").unlink()
    installed_before = (installed / "VERSION").read_bytes()
    config_before = config.read_bytes()

    with pytest.raises(OperationError, match="package-asset-missing"):
        check_package_compatibility(installed, candidate, config)
    with pytest.raises(OperationError, match="package-asset-missing"):
        update_process_package(
            installed, candidate, config, backups, upgrade_evidence=_upgrade_evidence(tmp_path / "missing-asset-review")
        )

    assert (installed / "VERSION").read_bytes() == installed_before
    assert config.read_bytes() == config_before
    assert not backups.exists()


def test_recursive_link_is_rejected_before_copy_or_destination_mutation(
    tmp_path: Path,
) -> None:
    installed, candidate, config, backups = _update_fixture(tmp_path)
    target = tmp_path / "outside"
    target.mkdir()
    (target / "outside.txt").write_text("outside", encoding="utf-8")
    link = candidate / "templates" / "change" / "linked"
    try:
        os.symlink(target, link, target_is_directory=True)
    except OSError:
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            pytest.skip("symlink and junction creation are unavailable")

    with pytest.raises(OperationError, match="filesystem-link-forbidden"):
        update_process_package(installed, candidate, config, backups)

    assert (installed / "VERSION").read_text(encoding="utf-8").strip() == "0.3.0"
    assert not backups.exists()


def test_update_failure_restores_package_and_pin_and_removes_partial_backup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    installed, candidate, config, backups = _update_fixture(tmp_path)
    installed_before = (installed / "VERSION").read_bytes()
    config_before = config.read_bytes()

    def fail_write(path: Path, value: dict) -> None:
        raise OSError("synthetic config write failure")

    monkeypatch.setattr(operations, "_write_yaml_atomic", fail_write)
    with pytest.raises(OSError, match="synthetic config write failure"):
        update_process_package(
            installed, candidate, config, backups, upgrade_evidence=_upgrade_evidence(tmp_path / "failure-review")
        )

    assert (installed / "VERSION").read_bytes() == installed_before
    assert config.read_bytes() == config_before
    assert not backups.exists() or list(backups.iterdir()) == []
    assert not any(tmp_path.glob(".process.*"))


def test_update_requires_forward_semver_and_rejects_undeclared_assets(
    tmp_path: Path,
) -> None:
    installed, candidate, config, backups = _update_fixture(tmp_path)
    package = _yaml(candidate / "package.yaml")
    package["package"]["version"] = "0.1.9"
    _write_yaml(candidate / "package.yaml", package)
    (candidate / "VERSION").write_text("0.1.9\n", encoding="utf-8")

    with pytest.raises(OperationError, match="package-downgrade-forbidden"):
        check_package_compatibility(installed, candidate, config)

    package["package"]["version"] = "0.4.0"
    _write_yaml(candidate / "package.yaml", package)
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    (candidate / "rogue.txt").write_text("not declared", encoding="utf-8")
    with pytest.raises(OperationError, match="package-asset-undeclared"):
        update_process_package(installed, candidate, config, backups)


def test_rollback_requires_update_generated_verified_snapshot(
    tmp_path: Path,
) -> None:
    installed, candidate, config, _ = _update_fixture(tmp_path)
    fake_backup = tmp_path / "fake-backup"
    shutil.copytree(candidate, fake_backup)

    with pytest.raises(OperationError, match="rollback-proof-invalid"):
        rollback_process_package(installed, fake_backup, config)


def test_backup_destination_cannot_overlap_installed_package(tmp_path: Path) -> None:
    installed, candidate, config, _ = _update_fixture(tmp_path)
    inside = installed / "rollbacks"

    with pytest.raises(OperationError, match="filesystem-overlap-forbidden"):
        update_process_package(
            installed, candidate, config, inside, upgrade_evidence=_upgrade_evidence(tmp_path / "overlap-review")
        )

    assert not inside.exists()


def _traceability(classification: str = "major", state: str = "ready_to_archive") -> dict:
    kinds = [
        "classification", "dor", "dod", "implementation", "qa", "automation",
        "architecture", "regression", "release", "approval",
    ]
    if classification == "hotfix":
        kinds.append("hotfix-reconciliation")
    return {
        "schema_version": "2.0",
        "classification": classification,
        "lifecycle_state": state,
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "links": [{
            "record_id": "trace-sample-001",
            "requirement_refs": ["REQ-SAMPLE-001"],
            "scenario_refs": ["SCN-SAMPLE-001"],
            "task_refs": ["TASK-SAMPLE-001"],
            "evidence_links": [{
                "record_id": f"evidence-{kind}-001",
                "kind": kind,
                "status": "concrete",
                "source_ref": f"evidence/{kind}-001.yaml",
                "evidence_refs": [f"EV-{kind.upper()}-001"],
                "policy_version": "1.0.0",
            } for kind in kinds],
        }],
    }


def test_traceability_is_schema_first_and_rejects_unknown_empty_and_duplicate_data() -> None:
    document = _traceability()
    document["unexpected"] = True
    with pytest.raises(OperationError, match="traceability-schema-invalid"):
        validate_traceability(document)

    document = _traceability()
    document["links"][0]["requirement_refs"] = []
    with pytest.raises(OperationError, match="traceability-schema-invalid"):
        validate_traceability(document)

    document = _traceability()
    document["links"][0]["scenario_refs"] *= 2
    with pytest.raises(OperationError, match="traceability-schema-invalid"):
        validate_traceability(document)

    document = _traceability()
    document["links"][0]["evidence_links"][0]["status"] = "unknown"
    with pytest.raises(OperationError, match="traceability-schema-invalid"):
        validate_traceability(document)


def test_traceability_rejects_duplicate_evidence_ids_and_kinds() -> None:
    duplicate_id = _traceability()
    duplicate_id["links"][0]["evidence_links"][1]["record_id"] = duplicate_id["links"][0]["evidence_links"][0]["record_id"]
    with pytest.raises(OperationError, match="traceability-evidence-duplicate"):
        validate_traceability(duplicate_id)

    duplicate_kind = _traceability()
    duplicate_kind["links"][0]["evidence_links"][1]["kind"] = duplicate_kind["links"][0]["evidence_links"][0]["kind"]
    with pytest.raises(OperationError, match="traceability-evidence-duplicate"):
        validate_traceability(duplicate_kind)


def test_archive_traceability_fails_closed_for_class_obligations_and_pending_links() -> None:
    major = _traceability()
    major["links"][0]["evidence_links"] = [
        row for row in major["links"][0]["evidence_links"] if row["kind"] != "architecture"
    ]
    with pytest.raises(OperationError, match="traceability-archive-incomplete"):
        validate_traceability(major)

    hotfix = _traceability("hotfix")
    reconciliation = next(row for row in hotfix["links"][0]["evidence_links"] if row["kind"] == "hotfix-reconciliation")
    reconciliation["status"] = "pending"
    with pytest.raises(OperationError, match="traceability-archive-pending"):
        validate_traceability(hotfix)

    major = _traceability()
    major["links"][0]["evidence_links"].append({
        "record_id": "evidence-waiver-001", "kind": "waiver-deferral",
        "status": "pending", "source_ref": "waivers/W-1.yaml",
        "evidence_refs": ["EV-WAIVER-001"], "policy_version": "1.0.0",
    })
    with pytest.raises(OperationError, match="traceability-archive-pending"):
        validate_traceability(major)


def test_traceability_derived_view_keeps_ids_versions_and_status_without_rules() -> None:
    view = validate_traceability(_traceability())

    assert view["record_ids"] == ["trace-sample-001"]
    assert all(row["record_id"] and row["policy_version"] == "1.0.0" for row in view["evidence_links"])
    assert "rules" not in view


def test_minor_archive_traceability_accepts_practical_class_evidence() -> None:
    minor = _traceability("minor")
    minor["links"][0]["evidence_links"] = [
        row for row in minor["links"][0]["evidence_links"]
        if row["kind"] not in {"automation", "architecture"}
    ]

    view = validate_traceability(minor)

    assert view["status"] == "valid"
    assert view["classification"] == "minor"


SCENARIO_COVERAGE = {'test_archive_traceability_fails_closed_for_class_obligations_and_pending_links': [{'capability': 'traceability-contract',
                                                                                     'requirement': 'Archive-readiness '
                                                                                                    'traceability',
                                                                                     'scenario': 'Major package '
                                                                                                 'archive checks '
                                                                                                 'expanded evidence',
                                                                                     'source_kind': 'delta'},
                                                                                    {'capability': 'traceability-contract',
                                                                                     'requirement': 'Archive-readiness '
                                                                                                    'traceability',
                                                                                     'scenario': 'Hotfix package '
                                                                                                 'links '
                                                                                                 'reconciliation',
                                                                                     'source_kind': 'delta'},
                                                                                    {'capability': 'traceability-contract',
                                                                                     'requirement': 'Archive-readiness '
                                                                                                    'traceability',
                                                                                     'scenario': 'Pending downstream '
                                                                                                 'link blocks archive '
                                                                                                 'readiness',
                                                                                     'source_kind': 'delta'}],
 'test_minor_archive_traceability_accepts_practical_class_evidence': [{'capability': 'traceability-contract',
                                                                       'requirement': 'Archive-readiness traceability',
                                                                       'scenario': 'Minor package accepts practical '
                                                                                   'evidence',
                                                                       'source_kind': 'delta'}],
 'test_traceability_derived_view_keeps_ids_versions_and_status_without_rules': [{'capability': 'traceability-contract',
                                                                                 'requirement': 'Archive-readiness '
                                                                                                'traceability',
                                                                                 'scenario': 'Verification evidence '
                                                                                             'remains source-linked',
                                                                                 'source_kind': 'delta'}]}
