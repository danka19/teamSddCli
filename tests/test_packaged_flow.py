"""Vertical acceptance tests for the packaged deterministic governed flow."""

from __future__ import annotations

import json
import hashlib
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
PROCESS_VERSION = (PROCESS / "VERSION").read_text(encoding="utf-8").strip()


def _yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _upgrade_evidence(root: Path, to_version: str = "0.4.0") -> Path:
    document = {
        "schema_version": "1.0",
        "change_id": "synthetic-process-upgrade",
        "review": {"owner_type": "human", "state": "approved", "decision_ref": "decisions/process-upgrade.yaml"},
        "from": {"package_version": PROCESS_VERSION, "openspec_version": "1.4.1"},
        "to": {"package_version": to_version, "openspec_version": "1.4.1"},
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


def test_bootstrap_and_create_copy_only_versioned_assets_with_json_evidence(
    tmp_path: Path,
) -> None:
    target = tmp_path / "workspace"

    bootstrap = bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)

    assert bootstrap["status"] == "created"
    assert bootstrap["operation"] == "bootstrap-team-specs"
    assert bootstrap["package"] == {
        "id": "sdd-process",
        "version": (PROCESS / "VERSION").read_text(encoding="utf-8").strip(),
    }
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


def test_bootstrap_reuses_one_versioned_package_without_policy_fork(
    tmp_path: Path,
) -> None:
    target = tmp_path / "workspace"

    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)

    config = _yaml(target / "team-specs" / "sdd.config.yaml")
    package_root = (target / "team-specs" / config["process_package"]["location"]).resolve()
    assert package_root == (target / "process").resolve()
    assert (package_root / "package.yaml").is_file()
    assert (package_root / "policies" / "manifest.yaml").is_file()
    assert not (target / "team-specs" / "process").exists()
    assert not (target / "team-specs" / "policies").exists()
    assert list(target.rglob("package.yaml")) == [target / "process" / "package.yaml"]


def test_bootstrap_installs_managed_gigacode_role_gate(tmp_path: Path) -> None:
    target = tmp_path / "workspace"

    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, target)

    source = PROCESS / "gigacode" / "skills" / "sdd-process-companion.md"
    installed = target / ".gigacode" / "skills" / "sdd-process-companion.md"
    assert installed.read_bytes() == source.read_bytes()
    assert "Какова ваша роль в этом чате" in installed.read_text(encoding="utf-8")
    companion = installed.read_text(encoding="utf-8")
    for token in (
        "## Режим `analyst-discovery`",
        "## Режим `guided-change`",
        "покажи короткий план тем",
        "задавай по одному вопросу",
        "`confirmed`",
        "`proposed`",
        "`unknown`",
        "`conflict`",
        "не создавай и не редактируй файлы",
        "показать первую команду",
    ):
        assert token in companion


def test_companion_keeps_discovery_and_action_permissions_separate() -> None:
    companion = (
        PROCESS / "gigacode" / "skills" / "sdd-process-companion.md"
    ).read_text(encoding="utf-8")
    discovery = companion.split("## Режим `analyst-discovery`", 1)[1].split(
        "## Режим `guided-change`", 1
    )[0]
    assert "сначала покажи короткий план тем" in discovery
    assert "после явного разрешения" in discovery
    assert "только после подтверждения итоговой сводки" in discovery
    assert "не создавай и не редактируй файлы" in discovery
    assert "только один разрешённый текущим этапом черновик" in discovery
    assert "прекращает вопросы" in discovery
    assert "Ответ «не знаю» не заменяй догадкой" in discovery
    assert "объясни влияние пробела" in discovery
    assert "назначь вопрос владельцу решения" in discovery


def test_update_rejects_modified_managed_gigacode_file_without_mutation(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "workspace"
    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, workspace)
    installed = workspace / "process"
    candidate = tmp_path / "candidate"
    shutil.copytree(installed, candidate)
    candidate_manifest = _yaml(candidate / "package.yaml")
    candidate_manifest["package"]["version"] = "0.4.0"
    (candidate / "package.yaml").write_text(
        yaml.safe_dump(candidate_manifest, sort_keys=False), encoding="utf-8"
    )
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    managed = workspace / ".gigacode" / "AGENTS.md"
    managed.write_text("local override\n", encoding="utf-8")
    process_before = (installed / "VERSION").read_bytes()
    config_path = workspace / "team-specs" / "sdd.config.yaml"
    config_before = config_path.read_bytes()

    with pytest.raises(OperationError, match="gigacode-managed-file-conflict"):
        update_process_package(
            installed,
            candidate,
            config_path,
            tmp_path / "rollbacks",
            upgrade_evidence=_upgrade_evidence(tmp_path / "upgrade-review", "0.4.0"),
        )

    assert (installed / "VERSION").read_bytes() == process_before
    assert config_path.read_bytes() == config_before
    assert managed.read_text(encoding="utf-8") == "local override\n"

def test_update_migrates_only_known_legacy_config_defaults(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    bootstrap_team_specs(PROCESS, TEAM_TEMPLATE, workspace)
    installed = workspace / "process"
    candidate = tmp_path / "candidate"
    shutil.copytree(installed, candidate)
    candidate_manifest = _yaml(candidate / "package.yaml")
    candidate_manifest["package"]["version"] = "0.4.0"
    (candidate / "package.yaml").write_text(
        yaml.safe_dump(candidate_manifest, sort_keys=False), encoding="utf-8"
    )
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")

    config_path = workspace / "team-specs" / "sdd.config.yaml"
    config = _yaml(config_path)
    del config["policy_set"]["overrides"]
    config["validation"] = {"mode": "strict"}
    config["process_package"]["location"] = "../../process"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

    update_process_package(
        installed,
        candidate,
        config_path,
        tmp_path / "rollbacks",
        upgrade_evidence=_upgrade_evidence(tmp_path / "upgrade-review", "0.4.0"),
    )

    migrated = _yaml(config_path)
    assert migrated["policy_set"]["overrides"] == []
    assert migrated["validation"] == {"strict": True, "placeholders_allowed": False}
    assert migrated["process_package"]["location"] == "../process"

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
    package_ignore = shutil.ignore_patterns("release")
    shutil.copytree(PROCESS, installed, ignore=package_ignore)
    shutil.copytree(PROCESS, candidate, ignore=package_ignore)
    candidate_package = _yaml(candidate / "package.yaml")
    candidate_package["package"]["version"] = "0.4.0"
    (candidate / "package.yaml").write_text(
        yaml.safe_dump(candidate_package, sort_keys=False), encoding="utf-8"
    )
    (candidate / "VERSION").write_text("0.4.0\n", encoding="utf-8")
    managed = installed.parent / ".gigacode" / "skills" / "sdd-process-companion.md"
    managed.parent.mkdir(parents=True)
    managed.write_bytes((installed / "gigacode" / "skills" / "sdd-process-companion.md").read_bytes())
    (candidate / "gigacode" / "skills" / "sdd-process-companion.md").write_text(
        "candidate managed instruction\n", encoding="utf-8"
    )
    managed_before = managed.read_bytes()
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

    update = update_process_package(
        installed,
        candidate,
        config_path,
        backups,
        upgrade_evidence=_upgrade_evidence(tmp_path / "upgrade-review"),
    )

    assert update["status"] == "updated"
    assert update["from_version"] == PROCESS_VERSION
    assert update["to_version"] == "0.4.0"
    assert _yaml(config_path)["process_package"]["version"] == "0.4.0"
    assert history.read_bytes() == history_before
    assert managed.read_text(encoding="utf-8") == "candidate managed instruction\n"
    backup = backups / PROCESS_VERSION
    assert backup.is_dir()

    rollback = rollback_process_package(installed, backup, config_path)

    assert rollback["status"] == "rolled-back"
    assert _yaml(config_path)["process_package"]["version"] == PROCESS_VERSION
    assert history.read_bytes() == history_before
    assert managed.read_bytes() == managed_before

    bad = tmp_path / "bad-candidate"
    shutil.copytree(PROCESS, bad, ignore=shutil.ignore_patterns("release"))
    (bad / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    installed_before = (installed / "VERSION").read_bytes()
    config_before = config_path.read_bytes()
    with pytest.raises(OperationError, match="package-version-mismatch"):
        update_process_package(installed, bad, config_path, backups)
    assert (installed / "VERSION").read_bytes() == installed_before
    assert config_path.read_bytes() == config_before
    assert history.read_bytes() == history_before


SCENARIO_COVERAGE = {"test_bootstrap_reuses_one_versioned_package_without_policy_fork":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Process package distribution","scenario":"Manual forks are not the default reuse model"}],"test_bootstrap_and_create_copy_only_versioned_assets_with_json_evidence":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Process package distribution","scenario":"One versioned folder carries process assets"}],"test_spec_pr_and_archive_preparation_collect_evidence_without_authority":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Practical developer and agent workflow","scenario":"Archive readiness links implementation evidence"},{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Repository content split","scenario":"Code PR references canonical specs"}],
 'test_manual_fallback_covers_unavailable_integrations_without_ai': [{'capability': 'change-artifact-contracts',
                                                                      'requirement': 'Artifact matrix baseline status',
                                                                      'scenario': 'Deferred integrations are explicit',
                                                                      'source_kind': 'delta'},
                                                                     {'capability': 'change-lifecycle',
                                                                      'requirement': 'MVP boundary for lifecycle '
                                                                                     'automation',
                                                                      'scenario': 'Core process is AI-disabled and '
                                                                                  'integration-independent',
                                                                      'source_kind': 'delta'},
                                                                     {'capability': 'change-lifecycle',
                                                                      'requirement': 'MVP boundary for lifecycle '
                                                                                     'automation',
                                                                      'scenario': 'Deferred integration is not '
                                                                                  'fabricated',
                                                                      'source_kind': 'delta'}],
 'test_traceability_allows_conditional_links_pending_before_archive': [{'capability': 'traceability-contract',
                                                                        'requirement': 'Archive-readiness '
                                                                                       'traceability',
                                                                        'scenario': 'Pending traceability is allowed '
                                                                                    'before archive readiness',
                                                                        'source_kind': 'delta'}],
 'test_traceability_and_external_mapping_fail_closed_and_keep_canonical_ids': [{'capability': 'change-lifecycle',
                                                                                'requirement': 'Delivered state is '
                                                                                               'external to archive '
                                                                                               'state',
                                                                                'scenario': 'Tracker transition uses '
                                                                                            'mapping',
                                                                                'source_kind': 'delta'},
                                                                               {'capability': 'repo-topology-config',
                                                                                'requirement': 'External workflow '
                                                                                               'mapping',
                                                                                'scenario': 'Mapping distinguishes '
                                                                                            'archive and delivered',
                                                                                'source_kind': 'delta'},
                                                                               {'capability': 'repo-topology-config',
                                                                                'requirement': 'External workflow '
                                                                                               'mapping',
                                                                                'scenario': 'Unmapped external status '
                                                                                            'blocks automation',
                                                                                'source_kind': 'delta'}]}
