"""CLI and schema tests for standalone deterministic gate evaluation."""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import yaml

from process.validators.artifact_gates import evaluate_gate
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
