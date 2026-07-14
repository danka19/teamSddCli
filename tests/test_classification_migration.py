"""Scenario-first tests for bounded legacy classification migration and CLIs."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

import yaml

from process.validators.classification_migration import apply_migration, plan_migration
from scripts.classify_change import main as classify_main
from scripts.migrate_change_classification import main as migrate_main


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "classification-migration"
POLICY_FIXTURES = ROOT / "tests" / "fixtures" / "policy-v2"


def _copy(name: str, tmp_path: Path) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    target = tmp_path / "change.yaml"
    shutil.copyfile(FIXTURES / name, target)
    return target


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_check_is_non_mutating_stable_and_never_proposes_hotfix(tmp_path: Path) -> None:
    for name, expected in (("legacy-thin.yaml", "minor"), ("legacy-full.yaml", "major")):
        path = _copy(name, tmp_path / name.removesuffix(".yaml"))
        before = path.read_bytes()

        first = plan_migration(path)
        second = plan_migration(path)

        assert path.read_bytes() == before
        assert first.as_dict() == second.as_dict()
        assert first.exit_code == 0
        assert first.as_dict()["status"] == "ready"
        assert first.as_dict()["mapping"] == {"mode": name.split("-")[1].split(".")[0], "classification": expected}
        assert first.as_dict()["mapping"]["classification"] != "hotfix"
        assert first.as_dict()["diagnostics"] == [{
            "code": "migration.legacy-mode-deprecated",
            "source_field": "mode",
            "message": "Legacy mode is read only for deterministic migration.",
        }]
        assert first.as_dict()["affected_files"] == ["change.yaml"]
        assert first.as_dict()["preserved_fields"] == sorted(
            key for key in _load(path) if key != "mode"
        )
        assert first.render_human() == second.render_human()
        human = first.render_human()
        for section in (
            "Schema:", "Validation:", "Preserved fields:", "Affected files:",
            "Rollback:", "Hold required:",
        ):
            assert section in human


def test_conflict_and_ambiguous_legacy_metadata_are_refused(tmp_path: Path) -> None:
    conflict = _copy("legacy-thin.yaml", tmp_path / "conflict")
    conflict.write_text(conflict.read_text(encoding="utf-8") + "classification: major\n", encoding="utf-8")
    ambiguous = _copy("legacy-thin.yaml", tmp_path / "ambiguous")
    ambiguous.write_text(ambiguous.read_text(encoding="utf-8").replace("mode: thin", "mode: routine"), encoding="utf-8")

    assert plan_migration(conflict).as_dict()["ambiguities"] == ["legacy-target-conflict"]
    assert plan_migration(ambiguous).as_dict()["ambiguities"] == ["unsupported-legacy-mode"]
    assert plan_migration(conflict).exit_code == 1
    assert plan_migration(ambiguous).exit_code == 1


def test_apply_requires_matching_valid_plan_and_preserves_metadata_and_comments(tmp_path: Path) -> None:
    path = _copy("legacy-thin.yaml", tmp_path)
    before = _load(path)

    stale = apply_migration(path, expected_plan_digest="wrong")
    assert stale.exit_code == 1
    assert _load(path) == before
    assert stale.as_dict()["hold_evidence"]["required"] is True

    plan = plan_migration(path)
    applied = apply_migration(path, expected_plan_digest=plan.as_dict()["plan_digest"])
    migrated = _load(path)

    assert applied.exit_code == 0
    assert applied.as_dict()["status"] == "applied"
    assert migrated["schema_version"] == 2
    assert migrated["classification"] == "minor"
    assert "mode" not in migrated
    assert migrated["compatibility"]["source"] == "migrated"
    for key, value in before.items():
        if key != "mode":
            assert migrated[key] == value
    assert path.read_text(encoding="utf-8").startswith("# This comment")
    backup = Path(applied.as_dict()["rollback_evidence"]["backup_path"])
    assert backup.read_bytes() == (FIXTURES / "legacy-thin.yaml").read_bytes()


def test_second_apply_is_idempotent_and_does_not_rewrite_or_add_backup(tmp_path: Path) -> None:
    path = _copy("legacy-full.yaml", tmp_path)
    plan = plan_migration(path)
    apply_migration(path, expected_plan_digest=plan.as_dict()["plan_digest"])
    before = path.read_bytes()

    current_plan = plan_migration(path)
    second = apply_migration(
        path, expected_plan_digest=current_plan.as_dict()["plan_digest"]
    )

    assert second.exit_code == 0
    assert second.as_dict()["status"] == "already-current"
    assert path.read_bytes() == before
    assert len(list(tmp_path.glob("*.bak"))) == 1


def test_archived_or_accepted_history_is_reported_but_never_rewritten(tmp_path: Path) -> None:
    archive_path = tmp_path / "openspec" / "changes" / "archive" / "sample" / "change.yaml"
    archive_path.parent.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "legacy-thin.yaml", archive_path)
    accepted_path = tmp_path / "openspec" / "specs" / "sample" / "change.yaml"
    accepted_path.parent.mkdir(parents=True)
    shutil.copyfile(FIXTURES / "legacy-full.yaml", accepted_path)

    for path in (archive_path, accepted_path):
        before = path.read_bytes()
        plan = plan_migration(path)
        result = apply_migration(path, expected_plan_digest=plan.as_dict()["plan_digest"])
        assert plan.as_dict()["status"] == "excluded-history"
        assert result.as_dict()["status"] == "excluded-history"
        assert path.read_bytes() == before


def test_migration_cli_has_stable_human_json_and_exit_semantics(
    tmp_path: Path, capsys
) -> None:
    path = _copy("legacy-thin.yaml", tmp_path)
    assert migrate_main(["check", str(path), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ready"

    assert migrate_main(["check", str(path)]) == 0
    human = capsys.readouterr().out
    assert "Migration: ready" in human
    assert payload["plan_digest"] in human

    assert migrate_main(["apply", str(path), "--plan-digest", "wrong", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "blocked"


def test_classifier_cli_consumes_policy_snapshot_and_emits_stable_json(
    tmp_path: Path, capsys
) -> None:
    document = _load(POLICY_FIXTURES / "valid" / "minor.yaml")
    policy = _load(ROOT / "process" / "policies" / "classification.yaml")
    minor = next(
        row["value"] for row in policy["rules"]
        if row["id"] == "classification.minor-conditions"
    )
    document["classification_evidence"] = [
        {
            "id": identifier,
            "value": True,
            "source": {"kind": "proposal", "ref": "proposal.md"},
            "rationale": "Synthetic CLI evidence.",
        }
        for identifier in minor
    ]
    change = tmp_path / "change.yaml"
    change.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    args = [
        str(change),
        "--config", str(POLICY_FIXTURES / "config" / "valid-central.yaml"),
        "--process-root", str(ROOT / "process"),
        "--json",
    ]

    assert classify_main(args) == 0
    first = json.loads(capsys.readouterr().out)
    assert classify_main(args) == 0
    second = json.loads(capsys.readouterr().out)
    assert first == second
    assert first["selected_class"] == "minor"


def test_both_clis_render_json_usage_errors_with_exit_two(capsys) -> None:
    assert classify_main(["missing.yaml", "--json"]) == 2
    classify_payload = json.loads(capsys.readouterr().out)
    assert classify_payload["status"] == "usage"

    assert migrate_main(["apply", "missing.yaml", "--json"]) == 2
    migrate_payload = json.loads(capsys.readouterr().out)
    assert migrate_payload["status"] == "usage"
