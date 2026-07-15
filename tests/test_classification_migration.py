"""Scenario-first tests for bounded legacy classification migration and CLIs."""

from __future__ import annotations

import copy
import json
import os
import shutil
from pathlib import Path

import pytest
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


def test_check_refuses_arbitrary_or_invalid_target_documents_without_mutation(
    tmp_path: Path,
) -> None:
    arbitrary = tmp_path / "arbitrary" / "change.yaml"
    arbitrary.parent.mkdir(parents=True)
    arbitrary.write_text("mode: thin\nunrelated: value\n", encoding="utf-8")
    invalid = _copy("legacy-thin.yaml", tmp_path / "invalid")
    invalid.write_text(
        invalid.read_text(encoding="utf-8").replace(
            "decision: {owner_type: human, owner_id: sample-tech-lead, state: confirmed, evidence_ref: decisions/classification.md}\n",
            "",
        ),
        encoding="utf-8",
    )

    for path in (arbitrary, invalid):
        before = path.read_bytes()
        result = plan_migration(path)
        assert result.exit_code == 1
        assert result.as_dict()["status"] == "blocked"
        assert result.as_dict()["validation_result"] == "invalid"
        assert "target-schema-validation-failed" in result.as_dict()["ambiguities"]
        assert path.read_bytes() == before
        assert not list(path.parent.glob(".*classification-v2*.tmp"))


def test_migration_refuses_structurally_valid_legacy_metadata_at_unsupported_targets(
    tmp_path: Path,
) -> None:
    for relative in (Path("settings.yaml"), Path("nested") / "change.yml"):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / "legacy-thin.yaml", target)
        before = target.read_bytes()

        result = plan_migration(target)

        assert result.exit_code == 1
        assert result.as_dict()["status"] == "blocked"
        assert result.as_dict()["ambiguities"] == ["unsupported-metadata-target"]
        assert result.as_dict()["validation_result"] == "invalid"
        assert target.read_bytes() == before
        assert not target.with_name(target.name + ".pre-classification-v2.bak").exists()


def test_plan_digest_is_bound_to_canonical_resolved_change_target(
    tmp_path: Path,
) -> None:
    first = _copy("legacy-thin.yaml", tmp_path / "a")
    second = _copy("legacy-thin.yaml", tmp_path / "b")
    second_before = second.read_bytes()

    first_plan = plan_migration(first)
    second_plan = plan_migration(second)

    assert first_plan.as_dict()["affected_files"] == second_plan.as_dict()["affected_files"]
    assert first_plan.as_dict()["source_sha256"] == second_plan.as_dict()["source_sha256"]
    assert first_plan.as_dict()["plan_digest"] != second_plan.as_dict()["plan_digest"]
    assert str(first.parent.resolve()) not in json.dumps(first_plan.as_dict())
    assert str(second.parent.resolve()) not in json.dumps(second_plan.as_dict())

    refused = apply_migration(
        second, expected_plan_digest=first_plan.as_dict()["plan_digest"]
    )

    assert refused.exit_code == 1
    assert refused.as_dict()["status"] == "blocked"
    assert refused.as_dict()["hold_evidence"]["reasons"] == ["plan-digest-mismatch"]
    assert second.read_bytes() == second_before
    assert not second.with_name(second.name + ".pre-classification-v2.bak").exists()


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


def test_apply_uses_same_directory_atomic_replace_and_cleans_temp_on_failure(
    tmp_path: Path, monkeypatch
) -> None:
    success = _copy("legacy-thin.yaml", tmp_path / "success")
    real_replace = os.replace
    replacements: list[tuple[Path, Path]] = []

    def recording_replace(source: str | os.PathLike[str], target: str | os.PathLike[str]) -> None:
        source_path = Path(source)
        target_path = Path(target)
        assert source_path.parent == target_path.parent == success.parent
        assert source_path.is_file()
        replacements.append((source_path, target_path))
        real_replace(source_path, target_path)

    monkeypatch.setattr(os, "replace", recording_replace)
    success_plan = plan_migration(success)
    applied = apply_migration(
        success, expected_plan_digest=success_plan.as_dict()["plan_digest"]
    )

    assert applied.as_dict()["status"] == "applied"
    assert replacements and replacements[0][1] == success
    assert not list(success.parent.glob(".*classification-v2*.tmp"))

    failure = _copy("legacy-full.yaml", tmp_path / "failure")
    failure_before = failure.read_bytes()

    def failing_replace(source: str | os.PathLike[str], target: str | os.PathLike[str]) -> None:
        raise OSError("synthetic replace failure")

    monkeypatch.setattr(os, "replace", failing_replace)
    failure_plan = plan_migration(failure)
    with pytest.raises(OSError, match="synthetic replace failure"):
        apply_migration(
            failure, expected_plan_digest=failure_plan.as_dict()["plan_digest"]
        )

    assert failure.read_bytes() == failure_before
    assert failure.with_name(failure.name + ".pre-classification-v2.bak").read_bytes() == failure_before
    assert not list(failure.parent.glob(".*classification-v2*.tmp"))


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


SCENARIO_COVERAGE = {'test_apply_requires_matching_valid_plan_and_preserves_metadata_and_comments': [{'capability': 'change-package-foundation',
                                                                                  'requirement': 'Deterministic '
                                                                                                 'classification '
                                                                                                 'migration command',
                                                                                  'scenario': 'Apply mode preserves '
                                                                                              'unrelated metadata',
                                                                                  'source_kind': 'delta'}],
 'test_archived_or_accepted_history_is_reported_but_never_rewritten': [{'capability': 'change-package-foundation',
                                                                        'requirement': 'Deterministic classification '
                                                                                       'migration command',
                                                                        'scenario': 'Archived history is excluded',
                                                                        'source_kind': 'delta'}],
 'test_check_is_non_mutating_stable_and_never_proposes_hotfix': [{'capability': 'change-package-foundation',
                                                                  'requirement': 'Classification-aware placeholder '
                                                                                 'validation',
                                                                  'scenario': 'Real package rejects undecided '
                                                                              'classification',
                                                                  'source_kind': 'delta'},
                                                                 {'capability': 'change-package-foundation',
                                                                  'requirement': 'Deterministic classification '
                                                                                 'migration command',
                                                                  'scenario': 'Check mode is non-mutating',
                                                                  'source_kind': 'delta'}],
 'test_check_refuses_arbitrary_or_invalid_target_documents_without_mutation': [{'capability': 'change-package-foundation',
                                                                                'requirement': 'Classification-aware '
                                                                                               'placeholder '
                                                                                               'validation',
                                                                                'scenario': 'Target route examples '
                                                                                            'validate structurally',
                                                                                'source_kind': 'delta'}],
 'test_conflict_and_ambiguous_legacy_metadata_are_refused': [{'capability': 'change-package-foundation',
                                                              'requirement': 'Bounded legacy compatibility',
                                                              'scenario': 'Legacy package receives deprecation result',
                                                              'source_kind': 'delta'},
                                                             {'capability': 'change-package-foundation',
                                                              'requirement': 'Bounded legacy compatibility',
                                                              'scenario': 'Conflicting metadata is rejected',
                                                              'source_kind': 'delta'},
                                                             {'capability': 'change-package-foundation',
                                                              'requirement': 'Bounded legacy compatibility',
                                                              'scenario': 'Compatibility end is versioned',
                                                              'source_kind': 'delta'},
                                                             {'capability': 'change-package-foundation',
                                                              'requirement': 'Versioned corporate classification '
                                                                             'metadata',
                                                              'scenario': 'Version 2 metadata is explicit',
                                                              'source_kind': 'delta'},
                                                             {'capability': 'change-package-foundation',
                                                              'requirement': 'Versioned corporate classification '
                                                                             'metadata',
                                                              'scenario': 'New writer does not emit legacy mode',
                                                              'source_kind': 'delta'}]}
