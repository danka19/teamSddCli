import os
import subprocess
from pathlib import Path

import pytest
import yaml

from process.errors import OperationError
from process.workflow_operations import (
    archive_change,
    create_change,
    prepare_archive,
    validate_archive_history,
)
from process.validators.artifact_gates import evaluate_gate
from process.validators.policy_validation import validate_policy_bundle


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
TEAM_CONFIG = ROOT / "templates" / "team-specs" / "sdd.config.yaml"


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_yaml(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def make_change(tmp_path: Path, change_id: str = "sample-archive-001") -> tuple[Path, Path]:
    changes = tmp_path / "openspec" / "changes"
    create_change(
        PROCESS,
        changes,
        change_id=change_id,
        title="Synthetic archive change",
        classification="minor",
        change_type="behavior_change",
    )
    (tmp_path / "sdd.config.yaml").write_bytes(TEAM_CONFIG.read_bytes())
    return changes / change_id, changes / "archive"


def make_archive_ready(change: Path) -> None:
    metadata = load_yaml(change / "change.yaml")
    metadata["status"] = "ready_to_archive"
    write_yaml(change / "change.yaml", metadata)

    config = load_yaml(change.parent.parent.parent / "sdd.config.yaml")
    manifest = load_yaml(PROCESS / "policies" / "manifest.yaml")
    policy = validate_policy_bundle(PROCESS, manifest, config, None)
    assert policy.snapshot is not None and policy.diagnostics == []
    gate = load_yaml(change / "gate-input.yaml")
    gate["status"] = "ready_to_archive"
    initial = evaluate_gate(gate, policy.snapshot, "archive-readiness")
    gate["evidence"] = [
        {
            "id": row["id"],
            "state": "satisfied",
            "content": f"Reviewed substantive evidence for {row['id']}.",
            "source_ref": f"evidence/{row['id']}.md",
            "fresh": True,
        }
        for row in initial.as_dict()["obligations"]
    ]
    final = evaluate_gate(gate, policy.snapshot, "archive-readiness")
    assert final.as_dict()["blocking_gaps"] == []
    write_yaml(change / "gate-input.yaml", gate)

    evidence = [
        {
            "record_id": f"evidence-{kind}-001",
            "kind": kind,
            "status": "not-applicable" if kind == "release" else "concrete",
            "source_ref": f"evidence/{kind}.yaml",
            "evidence_refs": [f"EV-{kind.upper()}-001"],
            "policy_version": "1.0.0",
        }
        for kind in (
            "classification", "dor", "dod", "implementation", "qa",
            "regression", "release", "approval",
        )
    ]
    write_yaml(change / "traceability.yaml", {
        "schema_version": "2.0",
        "classification": metadata["classification"],
        "lifecycle_state": "ready_to_archive",
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "links": [{
            "record_id": "trace-archive-001",
            "requirement_refs": ["REQ-ARCHIVE-001"],
            "scenario_refs": ["SCN-ARCHIVE-001"],
            "task_refs": ["TASK-ARCHIVE-001"],
            "evidence_links": evidence,
        }],
    })


def approval(change_id: str = "sample-archive-001") -> dict[str, str]:
    return {
        "change_id": change_id,
        "owner_type": "human",
        "state": "approved",
        "decision_ref": "decisions/archive-approval.yaml",
    }


def test_archive_operation_uses_dated_history_path(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)

    result = archive_change(
        PROCESS,
        change,
        archive_root=archive_root,
        archive_date="2026-07-20",
        approval=approval(),
    )

    target = archive_root / "2026-07-20-sample-archive-001"
    assert result["archive_path"] == target.as_posix()
    assert result["archived"] is True
    assert not change.exists()
    assert (target / "change.yaml").is_file()


def test_archive_commit_subject_is_greppable(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)
    prepared = prepare_archive(
        PROCESS,
        change,
        archive_root=archive_root,
        archive_date="2026-07-20",
        approval=approval(),
    )

    assert prepared["required_commit_subject"] == "spec: archive sample-archive-001"
    assert validate_archive_history(
        archive_root / "2026-07-20-sample-archive-001",
        "spec: archive sample-archive-001",
        "sample-archive-001",
    )["status"] == "valid"
    with pytest.raises(OperationError, match="archive-commit-invalid"):
        validate_archive_history(
            archive_root / "2026-07-20-sample-archive-001",
            "archive sample-archive-001",
            "sample-archive-001",
        )


def test_archive_operation_rejects_missing_approval_and_unsafe_state(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)

    with pytest.raises(OperationError, match="archive-readiness-required"):
        archive_change(
            PROCESS, change, archive_root=archive_root,
            archive_date="2026-07-20", approval=approval(),
        )
    assert change.is_dir()
    make_archive_ready(change)

    with pytest.raises(OperationError, match="archive-approval-required"):
        archive_change(
            PROCESS,
            change,
            archive_root=archive_root,
            archive_date="2026-07-20",
            approval={**approval(), "state": "pending"},
        )
    assert change.is_dir()

    collision = archive_root / "2026-07-20-sample-archive-001"
    collision.mkdir(parents=True)
    with pytest.raises(OperationError, match="archive-target-exists"):
        archive_change(
            PROCESS,
            change,
            archive_root=archive_root,
            archive_date="2026-07-20",
            approval=approval(),
        )
    assert change.is_dir()

    with pytest.raises(OperationError, match="archive-date-invalid"):
        archive_change(
            PROCESS,
            change,
            archive_root=archive_root,
            archive_date="20-07-2026",
            approval=approval(),
        )

    other_change, _ = make_change(tmp_path / "other", "other-archive-001")
    make_archive_ready(other_change)
    with pytest.raises(OperationError, match="archive-path-unsafe"):
        archive_change(
            PROCESS,
            other_change,
            archive_root=archive_root,
            archive_date="2026-07-21",
            approval=approval("other-archive-001"),
        )


def test_archive_operation_rejects_already_archived_source(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)
    result = archive_change(
        PROCESS,
        change,
        archive_root=archive_root,
        archive_date="2026-07-20",
        approval=approval(),
    )

    with pytest.raises(OperationError, match="archive-source-already-archived"):
        archive_change(
            PROCESS,
            Path(result["archive_path"]),
            archive_root=archive_root,
            archive_date="2026-07-21",
            approval=approval(),
        )


def test_archive_operation_rejects_linked_archive_root_without_mutation(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)
    outside = tmp_path / "outside"
    outside.mkdir()
    if os.name == "nt":
        created = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(archive_root), str(outside)],
            capture_output=True,
            text=True,
            check=False,
        )
        if created.returncode:
            pytest.skip("directory junction creation is unavailable on this host")
    else:
        try:
            os.symlink(outside, archive_root, target_is_directory=True)
        except OSError:
            pytest.skip("directory symlink creation is unavailable on this host")

    before = {path.relative_to(change).as_posix(): path.read_bytes() for path in change.rglob("*") if path.is_file()}
    with pytest.raises(OperationError, match="filesystem-link-forbidden"):
        archive_change(
            PROCESS, change, archive_root=archive_root,
            archive_date="2026-07-20", approval=approval(),
        )
    after = {path.relative_to(change).as_posix(): path.read_bytes() for path in change.rglob("*") if path.is_file()}
    assert after == before
    assert not any(outside.iterdir())


def test_archive_operation_rejects_blocked_readiness_byte_identically(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)

    def snapshot() -> dict[str, bytes]:
        return {
            path.relative_to(change).as_posix(): path.read_bytes()
            for path in change.rglob("*") if path.is_file()
        }

    gate = load_yaml(change / "gate-input.yaml")
    gate["evidence"] = []
    write_yaml(change / "gate-input.yaml", gate)
    before = snapshot()
    with pytest.raises(OperationError, match="archive-readiness-blocked"):
        archive_change(PROCESS, change, archive_root=archive_root, archive_date="2026-07-20", approval=approval())
    assert snapshot() == before

    make_archive_ready(change)
    traceability = load_yaml(change / "traceability.yaml")
    traceability["links"][0]["evidence_links"][0]["status"] = "pending"
    write_yaml(change / "traceability.yaml", traceability)
    before = snapshot()
    with pytest.raises(OperationError, match="traceability-archive-pending"):
        archive_change(PROCESS, change, archive_root=archive_root, archive_date="2026-07-20", approval=approval())
    assert snapshot() == before

    make_archive_ready(change)
    gate = load_yaml(change / "gate-input.yaml")
    gate["id"] = "different-change"
    write_yaml(change / "gate-input.yaml", gate)
    before = snapshot()
    with pytest.raises(OperationError, match="archive-readiness-mismatch"):
        archive_change(PROCESS, change, archive_root=archive_root, archive_date="2026-07-20", approval=approval())
    assert snapshot() == before


def test_archive_convention_does_not_replace_approval_or_external_authority(tmp_path: Path) -> None:
    change, archive_root = make_change(tmp_path)
    make_archive_ready(change)
    with pytest.raises(OperationError, match="archive-approval-required"):
        archive_change(
            PROCESS, change, archive_root=archive_root,
            archive_date="2026-07-20", approval={**approval(), "owner_type": "ai"},
        )
    assert change.is_dir()

    result = archive_change(
        PROCESS, change, archive_root=archive_root,
        archive_date="2026-07-20", approval=approval(),
    )
    assert result["git_commit_created"] is False
    assert result["merge_performed"] is False
    assert result["release_performed"] is False
    assert result["deployment_performed"] is False
    assert result["human_authority_substituted"] is False


SCENARIO_COVERAGE = {
    "test_archive_operation_uses_dated_history_path": [
        {
            "source_kind": "delta",
            "capability": "change-lifecycle",
            "requirement": "Archive history convention",
            "scenario": "Archive uses dated history path",
        }
    ],
    "test_archive_commit_subject_is_greppable": [
        {
            "source_kind": "delta",
            "capability": "change-lifecycle",
            "requirement": "Archive history convention",
            "scenario": "Archive commit is greppable",
        }
    ],
    "test_archive_convention_does_not_replace_approval_or_external_authority": [
        {
            "source_kind": "delta",
            "capability": "change-lifecycle",
            "requirement": "Archive history convention",
            "scenario": "Archive convention does not replace approval",
        }
    ],
}
