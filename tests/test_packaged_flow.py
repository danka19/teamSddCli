"""Vertical acceptance tests for the packaged deterministic governed flow."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from process.workflow_operations import (
    OperationError,
    bootstrap_team_specs,
    create_change,
    manual_fallback_plan,
    prepare_archive,
    prepare_spec_pr,
    rollback_process_package,
    update_process_package,
    validate_external_mapping,
    validate_traceability,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
TEAM_TEMPLATE = ROOT / "templates" / "team-specs"


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_bootstrap_and_create_copy_only_versioned_assets_with_json_evidence(
    tmp_path: Path,
) -> None:
    target = tmp_path / "workspace"

    bootstrap = bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)

    assert bootstrap["status"] == "created"
    assert bootstrap["operation"] == "bootstrap-team-specs"
    assert bootstrap["package"] == {"id": "sdd-process", "version": "0.2.0"}
    assert bootstrap["ai_disabled"] is True
    assert bootstrap["human_authority_substituted"] is False
    assert (target / "process" / "templates" / "change" / "change.yaml").is_file()
    config = _yaml(target / "team-specs" / "sdd.config.yaml")
    assert config["process_package"]["location"] == "../process"
    assert all(
        not row["path"].startswith("templates/change/")
        for row in bootstrap["files"]
    )

    created = create_change(
        target / "process",
        target / "team-specs" / "openspec" / "changes",
        change_id="sample-change-001",
        title="Synthetic minor flow",
        classification="minor",
        change_type="behavior_change",
    )

    assert created["status"] == "created"
    assert created["operation"] == "create-change"
    assert created["decision_state"] == "pending-human-confirmation"
    assert created["lifecycle_mutated"] is False
    change = _yaml(
        target
        / "team-specs"
        / "openspec"
        / "changes"
        / "sample-change-001"
        / "change.yaml"
    )
    assert change["classification"] == "minor"
    assert change["compatibility"] == {"source": "native-v2"}
    assert "mode" not in change

    json.dumps(bootstrap, sort_keys=True)
    json.dumps(created, sort_keys=True)


def test_bootstrap_and_create_reject_unsafe_or_existing_destinations(
    tmp_path: Path,
) -> None:
    nonempty = tmp_path / "nonempty"
    nonempty.mkdir()
    (nonempty / "owned.txt").write_text("human data", encoding="utf-8")

    with pytest.raises(OperationError, match="destination-not-empty"):
        bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, nonempty)
    assert (nonempty / "owned.txt").read_text(encoding="utf-8") == "human data"

    target = tmp_path / "workspace"
    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)
    changes = target / "team-specs" / "openspec" / "changes"
    create_change(
        target / "process",
        changes,
        change_id="sample-change-001",
        title="Synthetic minor flow",
        classification="minor",
        change_type="behavior_change",
    )
    with pytest.raises(OperationError, match="destination-exists"):
        create_change(
            target / "process",
            changes,
            change_id="sample-change-001",
            title="Would overwrite",
            classification="major",
            change_type="new_feature",
        )
    with pytest.raises(OperationError, match="change-id-invalid"):
        create_change(
            target / "process",
            changes,
            change_id="../escape",
            title="Unsafe",
            classification="minor",
            change_type="behavior_change",
        )


@pytest.mark.parametrize("classification", ["minor", "major", "hotfix"])
def test_reference_change_creation_is_class_aware_and_ai_disabled(
    tmp_path: Path, classification: str,
) -> None:
    changes = tmp_path / "changes"
    evidence = create_change(
        PROCESS,
        changes,
        change_id=f"sample-{classification}-001",
        title=f"Synthetic {classification} flow",
        classification=classification,
        change_type="bugfix" if classification == "hotfix" else "behavior_change",
    )

    change = _yaml(changes / f"sample-{classification}-001" / "change.yaml")
    assert change["classification"] == classification
    assert change["decision"]["owner_type"] == "human"
    assert change["decision"]["state"] == "pending"
    assert evidence["ai_disabled"] is True


def test_spec_pr_and_archive_preparation_collect_evidence_without_authority(
    tmp_path: Path,
) -> None:
    changes = tmp_path / "changes"
    create_change(
        PROCESS,
        changes,
        change_id="sample-major-001",
        title="Synthetic major flow",
        classification="major",
        change_type="new_feature",
    )
    change = changes / "sample-major-001"
    before = {path.relative_to(change).as_posix(): path.read_bytes() for path in change.rglob("*") if path.is_file()}

    pr = prepare_spec_pr(PROCESS, change)
    archive = prepare_archive(PROCESS, change)

    for report, operation in ((pr, "prepare-spec-pr"), (archive, "prepare-archive")):
        assert report["operation"] == operation
        assert report["status"] == "prepared-for-human-review"
        assert report["approved"] is False
        assert report["merged"] is False
        assert report["archived"] is False
        assert report["lifecycle_mutated"] is False
    after = {path.relative_to(change).as_posix(): path.read_bytes() for path in change.rglob("*") if path.is_file()}
    assert after == before


def test_traceability_and_external_mapping_fail_closed_and_keep_canonical_ids() -> None:
    traceability = {
        "schema_version": "2.0",
        "classification": "hotfix",
        "lifecycle_state": "ready_to_archive",
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "links": [{
            "record_id": "trace-sample-001",
            "requirement_refs": ["REQ-SAMPLE-001"],
            "scenario_refs": ["SCN-SAMPLE-001"],
            "task_refs": ["TASK-SAMPLE-001"],
            "evidence_links": [
                {"record_id": f"evidence-{kind}-001", "kind": kind, "status": "concrete", "source_ref": f"evidence/{kind}-001.yaml", "evidence_refs": [f"EV-{kind.upper()}-001"], "policy_version": "1.0.0"}
                for kind in ("classification", "dor", "dod", "implementation", "qa", "regression", "release", "approval", "hotfix-reconciliation")
            ],
        }],
    }
    view = validate_traceability(traceability)
    assert view["policy"] == {"id": "sdd-core", "version": "1.0.0"}
    assert view["record_ids"] == ["trace-sample-001"]
    assert "rules" not in view

    incomplete = json.loads(json.dumps(traceability))
    incomplete["links"][0]["evidence_links"] = [
        row for row in incomplete["links"][0]["evidence_links"]
        if row["kind"] != "hotfix-reconciliation"
    ]
    with pytest.raises(OperationError, match="traceability-archive-incomplete"):
        validate_traceability(incomplete)

    mapping = {
        "schema_version": "1.0",
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "states": {
            "openspec_archive": "archived",
            "release_readiness": "release-ready",
            "deployment": "deployed",
            "consumer_acceptance": "accepted",
            "tracker_done": "done",
        },
    }
    result = validate_external_mapping(mapping)
    assert result["states"] == mapping["states"]
    unknown = json.loads(json.dumps(mapping))
    unknown["states"]["deployment"] = "unknown"
    with pytest.raises(OperationError, match="external-mapping-unknown"):
        validate_external_mapping(unknown)


def test_traceability_allows_conditional_links_pending_before_archive() -> None:
    document = {
        "schema_version": "2.0",
        "classification": "minor",
        "lifecycle_state": "draft",
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "links": [{
            "record_id": "trace-minor-001",
            "requirement_refs": ["REQ-MINOR-001"],
            "scenario_refs": ["SCN-MINOR-001"],
            "task_refs": ["TASK-MINOR-001"],
            "evidence_links": [
                {"record_id": "evidence-classification-001", "kind": "classification", "status": "concrete", "source_ref": "classification/decision-001.yaml", "evidence_refs": ["EV-CLASS-001"], "policy_version": "1.0.0"},
                {"record_id": "evidence-dor-001", "kind": "dor", "status": "pending", "source_ref": "gates/dor-001.yaml", "evidence_refs": ["EV-DOR-001"], "policy_version": "1.0.0"},
                {"record_id": "evidence-dod-001", "kind": "dod", "status": "pending", "source_ref": "gates/dod-001.yaml", "evidence_refs": ["EV-DOD-001"], "policy_version": "1.0.0"},
            ],
        }],
    }

    assert validate_traceability(document)["status"] == "valid"


def test_manual_fallback_covers_unavailable_integrations_without_ai() -> None:
    plan = manual_fallback_plan({"jira", "confluence", "model-runtime", "mcp", "role-inbox"})

    assert plan["ai_disabled"] is True
    assert plan["human_authority_substituted"] is False
    assert set(plan["unavailable"]) == {"jira", "confluence", "model-runtime", "mcp", "role-inbox"}
    assert {row["integration"] for row in plan["steps"]} == set(plan["unavailable"])
    assert all(row["deterministic_command"] for row in plan["steps"])
    with pytest.raises(OperationError, match="integration-unknown"):
        manual_fallback_plan({"mystery-service"})


def test_update_and_rollback_are_transactional_and_preserve_openspec_history(
    tmp_path: Path,
) -> None:
    installed = tmp_path / "process"
    candidate = tmp_path / "candidate"
    shutil.copytree(PROCESS, installed)
    shutil.copytree(PROCESS, candidate)
    candidate_package = _yaml(candidate / "package.yaml")
    candidate_package["package"]["version"] = "0.3.0"
    (candidate / "package.yaml").write_text(
        yaml.safe_dump(candidate_package, sort_keys=False), encoding="utf-8"
    )
    (candidate / "VERSION").write_text("0.3.0\n", encoding="utf-8")
    central = tmp_path / "team-specs"
    shutil.copytree(TEAM_TEMPLATE, central)
    config_path = central / "sdd.config.yaml"
    config = _yaml(config_path)
    config["process_package"]["location"] = "../process"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    history = central / "openspec" / "changes" / "archive" / "accepted.md"
    history.parent.mkdir(parents=True)
    history.write_text("accepted history\n", encoding="utf-8")
    history_before = history.read_bytes()
    backups = tmp_path / "rollbacks"

    update = update_process_package(installed, candidate, config_path, backups)

    assert update["status"] == "updated"
    assert update["from_version"] == "0.2.0"
    assert update["to_version"] == "0.3.0"
    assert _yaml(config_path)["process_package"]["version"] == "0.3.0"
    assert history.read_bytes() == history_before
    backup = backups / "0.2.0"
    assert backup.is_dir()

    rollback = rollback_process_package(installed, backup, config_path)

    assert rollback["status"] == "rolled-back"
    assert _yaml(config_path)["process_package"]["version"] == "0.2.0"
    assert history.read_bytes() == history_before

    bad = tmp_path / "bad-candidate"
    shutil.copytree(PROCESS, bad)
    (bad / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    installed_before = (installed / "VERSION").read_bytes()
    config_before = config_path.read_bytes()
    with pytest.raises(OperationError, match="package-version-mismatch"):
        update_process_package(installed, bad, config_path, backups)
    assert (installed / "VERSION").read_bytes() == installed_before
    assert config_path.read_bytes() == config_before
    assert history.read_bytes() == history_before
