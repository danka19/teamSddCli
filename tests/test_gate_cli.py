"""CLI and schema tests for standalone deterministic gate evaluation."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from process.validators.artifact_gates import evaluate_gate
from process.validators.gate_input import validate_gate_input
from process.validators.policy_validation import validate_policy_bundle
from scripts.evaluate_change_gates import main as gate_main


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
CONFIG = ROOT / "tests" / "fixtures" / "policy-v2" / "config" / "valid-central.yaml"
GATES = (
    "review-ready",
    "definition-of-ready",
    "implementation-complete",
    "definition-of-done",
    "release-transfer-readiness",
    "archive-readiness",
)


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _input() -> dict[str, Any]:
    result = validate_policy_bundle(
        PROCESS,
        _yaml(PROCESS / "policies" / "manifest.yaml"),
        _yaml(CONFIG),
        None,
    )
    assert result.snapshot is not None
    document: dict[str, Any] = {
        "schema_version": "1.0",
        "id": "sample-change",
        "classification": "minor",
        "status": "draft",
        "evaluation_date": "2026-07-14",
        "major_impact_hotfix": False,
        "evidence": [],
        "approvals": [{
            "owner_type": "human",
            "owner_id": "sample-tech-leads",
            "state": "approved",
            "evidence_ref": "decisions/tech-lead.yaml",
        }],
        "transition_approvals": [],
        "external_state": {
            "delivered": "unknown",
            "deployed": "unknown",
            "tracker_done": "unknown",
        },
    }
    required: set[str] = set()
    for gate in GATES:
        report = evaluate_gate(document, result.snapshot, gate)
        required.update(row["id"] for row in report.as_dict()["obligations"])
    document["evidence"] = [{
        "id": identifier,
        "state": "satisfied",
        "content": f"Reviewed substantive evidence for {identifier}.",
        "source_ref": f"evidence/{identifier}.md",
        "fresh": True,
        "valid_through": "2026-07-14",
    } for identifier in sorted(required)]
    return document


def _write(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_json_cli_evaluates_all_six_reports_deterministically_without_mutation(
    tmp_path: Path, capsys: Any,
) -> None:
    change = tmp_path / "gate-input.yaml"
    original = _input()
    _write(change, original)

    args = [str(change), "--config", str(CONFIG), "--json"]
    assert gate_main(args) == 0
    first = json.loads(capsys.readouterr().out)
    assert gate_main(args) == 0
    second = json.loads(capsys.readouterr().out)

    assert first == second
    assert first["status"] == "ready"
    assert [report["gate"] for report in first["reports"]] == list(GATES)
    assert first["lifecycle_mutated"] is False
    assert _yaml(change) == original


def test_human_cli_returns_blocked_for_missing_substantive_evidence(
    tmp_path: Path, capsys: Any,
) -> None:
    change = tmp_path / "blocked.yaml"
    document = _input()
    document["evidence"] = []
    _write(change, document)

    assert gate_main([
        str(change), "--gate", "review-ready", "--config", str(CONFIG)
    ]) == 1
    output = capsys.readouterr().out
    assert "Gate evaluation: blocked" in output
    assert "review-ready" in output


def test_cli_rejects_usage_and_unvalidated_input_with_stable_codes(
    tmp_path: Path, capsys: Any,
) -> None:
    assert gate_main(["--json"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "usage"

    change = tmp_path / "invalid.yaml"
    invalid = _input()
    invalid["evidence"][0]["unexpected"] = "free-form boundary"
    _write(change, invalid)
    assert gate_main([
        str(change), "--config", str(CONFIG), "--json"
    ]) == 3
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "error"
    assert payload["diagnostics"][0]["code"] == "gate.input-schema-invalid"


def test_cli_returns_policy_contract_error_without_exposing_local_paths(
    tmp_path: Path, capsys: Any,
) -> None:
    package = tmp_path / "process"
    shutil.copytree(PROCESS, package)
    policy_path = package / "policies" / "gates.yaml"
    policy = _yaml(policy_path)
    policy["rules"] = [
        rule for rule in policy["rules"] if rule["id"] != "gates.review-ready"
    ]
    _write(policy_path, policy)
    change = tmp_path / "input.yaml"
    _write(change, _input())

    assert gate_main([
        str(change), "--config", str(CONFIG), "--process-root", str(package), "--json"
    ]) == 3
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "policy-contract-error"
    rendered = json.dumps(payload)
    assert str(tmp_path) not in rendered


def test_cli_blocks_when_evidence_is_valid_but_authorized_approval_is_pending(
    tmp_path: Path, capsys: Any,
) -> None:
    change = tmp_path / "pending.yaml"
    document = _input()
    document["approvals"] = []
    _write(change, document)

    assert gate_main([
        str(change), "--gate", "review-ready", "--config", str(CONFIG), "--json"
    ]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "blocked"
    assert payload["reports"][0]["status"] == "awaiting_human_approval"
    assert payload["reports"][0]["blocking_gaps"] == []


def test_exception_expiry_schema_rejects_free_text_and_accepts_typed_conditions() -> None:
    document = _input()
    document["classification"] = "hotfix"
    document["evidence"][0] = {
        "id": document["evidence"][0]["id"],
        "state": "deferred",
        "content": "Substitute evidence is source linked.",
        "source_ref": "deferrals/D-4.yaml",
        "fresh": True,
        "deferral": {
            "substitute_evidence": "reviews/substitute.md",
            "owner": "sample-tech-leads",
            "approver": {"type": "human", "id": "sample-tech-leads"},
            "residual_risk": "Bounded residual risk remains.",
            "follow_up": "Reconcile before archive readiness.",
            "expiry": {
                "type": "lifecycle_state",
                "lifecycle_state": "ready_to_archive",
            },
            "reconciled": False,
        },
    }
    assert validate_gate_input(document, PROCESS) == []

    document["evidence"][0]["deferral"]["expiry"] = "ready_to_archive"
    assert validate_gate_input(document, PROCESS)[0]["code"] == "gate.input-schema-invalid"


def test_lifecycle_history_contract_is_versioned_source_linked_and_human_recorded() -> None:
    document = _input()
    document["status"] = "in_implementation"
    document["lifecycle_history"] = {
        "schema_version": "1.0",
        "reached_states": [
            {
                "id": "reached-ready-to-archive-1",
                "state": "ready_to_archive",
                "reached_at": "2026-07-14T08:00:00Z",
                "source_ref": "decisions/ready-to-archive-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
            {
                "id": "rework-in-implementation-1",
                "state": "in_implementation",
                "reached_at": "2026-07-14T09:00:00Z",
                "source_ref": "decisions/rework-in-implementation-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
        ],
    }

    assert validate_gate_input(document, PROCESS) == []

    ai_recorded = copy.deepcopy(document)
    ai_recorded["lifecycle_history"]["reached_states"][0]["recorded_by"] = {
        "type": "ai", "id": "assistant"
    }
    assert any(
        item["code"] == "gate.input-schema-invalid"
        for item in validate_gate_input(ai_recorded, PROCESS)
    )

    for field, value, expected_code in (
        ("state", "done", "gate.input-schema-invalid"),
        ("reached_at", "2026-07-14", "gate.lifecycle-history-inconsistent"),
    ):
        malformed = copy.deepcopy(document)
        malformed["lifecycle_history"]["reached_states"][0][field] = value
        assert any(
            item["code"] == expected_code
            for item in validate_gate_input(malformed, PROCESS)
        )


def test_lifecycle_history_rejects_duplicate_or_inconsistent_records() -> None:
    document = _input()
    document["status"] = "in_implementation"
    document["lifecycle_history"] = {
        "schema_version": "1.0",
        "reached_states": [
            {
                "id": "reached-ready-to-archive-1",
                "state": "ready_to_archive",
                "reached_at": "2026-07-14T08:00:00Z",
                "source_ref": "decisions/ready-to-archive-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
            {
                "id": "rework-in-implementation-1",
                "state": "in_implementation",
                "reached_at": "2026-07-14T09:00:00Z",
                "source_ref": "decisions/rework-in-implementation-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
        ],
    }

    duplicate = copy.deepcopy(document)
    duplicate["lifecycle_history"]["reached_states"][1]["id"] = (
        "reached-ready-to-archive-1"
    )
    assert any(
        item["code"] == "gate.lifecycle-history-id-duplicate"
        for item in validate_gate_input(duplicate, PROCESS)
    )

    out_of_order = copy.deepcopy(document)
    out_of_order["lifecycle_history"]["reached_states"][1]["reached_at"] = (
        "2026-07-14T07:00:00Z"
    )
    assert any(
        item["code"] == "gate.lifecycle-history-inconsistent"
        for item in validate_gate_input(out_of_order, PROCESS)
    )

    wrong_current = copy.deepcopy(document)
    wrong_current["status"] = "approved"
    assert any(
        item["code"] == "gate.lifecycle-history-inconsistent"
        for item in validate_gate_input(wrong_current, PROCESS)
    )


def test_cli_keeps_lifecycle_deferral_due_after_rework(
    tmp_path: Path, capsys: Any,
) -> None:
    change = tmp_path / "reworked.yaml"
    document = _input()
    document["classification"] = "hotfix"
    document["major_impact_hotfix"] = True
    document["status"] = "in_implementation"
    document["lifecycle_history"] = {
        "schema_version": "1.0",
        "reached_states": [
            {
                "id": "reached-ready-to-archive-1",
                "state": "ready_to_archive",
                "reached_at": "2026-07-14T08:00:00Z",
                "source_ref": "decisions/ready-to-archive-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
            {
                "id": "rework-in-implementation-1",
                "state": "in_implementation",
                "reached_at": "2026-07-14T09:00:00Z",
                "source_ref": "decisions/rework-in-implementation-1.yaml",
                "recorded_by": {"type": "human", "id": "sample-tech-leads"},
            },
        ],
    }
    document["evidence"].append({
        "id": "expanded-design-impact-analysis",
        "state": "deferred",
        "content": "Immediate substitute review completed.",
        "source_ref": "deferrals/D-9.yaml",
        "fresh": True,
        "deferral": {
            "substitute_evidence": "reviews/urgent-design.md",
            "owner": "sample-tech-leads",
            "approver": {"type": "human", "id": "sample-tech-leads"},
            "residual_risk": "Detailed design follows implementation.",
            "follow_up": "Complete when archive readiness is reached.",
            "expiry": {
                "type": "lifecycle_state",
                "lifecycle_state": "ready_to_archive",
            },
            "reconciled": False,
        },
    })
    _write(change, document)

    assert gate_main([
        str(change),
        "--gate", "definition-of-ready",
        "--config", str(CONFIG),
        "--json",
    ]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert any(
        item["code"] == "gate.deferral-due"
        for item in payload["reports"][0]["blocking_gaps"]
    )
    assert _yaml(change) == document


def test_malformed_unhashable_lifecycle_history_id_fails_closed_without_mutation(
    tmp_path: Path, capsys: Any,
) -> None:
    document = _input()
    document["status"] = "in_implementation"
    document["lifecycle_history"] = {
        "schema_version": "1.0",
        "reached_states": [{
            "id": {"unexpected": "mapping"},
            "state": "in_implementation",
            "reached_at": "2026-07-14T09:00:00Z",
            "source_ref": "decisions/in-implementation.yaml",
            "recorded_by": {"type": "human", "id": "sample-tech-leads"},
        }],
    }

    diagnostics = validate_gate_input(document, PROCESS)

    assert diagnostics == [{
        "code": "gate.input-schema-invalid",
        "pointer": "/lifecycle_history/reached_states/0/id",
        "message": "Gate input does not satisfy the pinned schema.",
    }]

    change = tmp_path / "malformed-history.yaml"
    _write(change, document)
    before = change.read_bytes()

    assert gate_main([
        str(change), "--gate", "definition-of-ready",
        "--config", str(CONFIG), "--json",
    ]) == 3
    payload = json.loads(capsys.readouterr().out)

    assert payload["status"] == "error"
    assert payload["diagnostics"] == diagnostics
    assert capsys.readouterr().err == ""
    assert change.read_bytes() == before
