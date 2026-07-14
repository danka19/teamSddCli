"""Scenario-first tests for deterministic Tech Lead decision support."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import yaml
import pytest

from process.validators.policy_validation import validate_policy_bundle
from process.validators.tech_lead import (
    TECH_LEAD_VIEWS,
    check_control_state,
    compile_tech_lead_policy,
    evaluate_tech_lead_review,
    policy_snapshot_digest,
    validate_tech_lead_input,
)
from scripts.check_tech_lead_control import main as control_main
from scripts.review_tech_lead import main as review_main
from tests.test_owner_governance import governed_owners, projects


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
CONFIG = ROOT / "tests" / "fixtures" / "policy-v2" / "config" / "valid-central.yaml"


def _yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _snapshot():
    result = validate_policy_bundle(
        PROCESS,
        _yaml(PROCESS / "policies" / "manifest.yaml"),
        _yaml(CONFIG),
        None,
    )
    assert result.snapshot is not None, result.diagnostics
    return result.snapshot


def _policy_ref() -> dict[str, str]:
    snapshot = _snapshot()
    return {
        "id": snapshot.policy_set_id,
        "version": snapshot.policy_set_version,
        "digest": policy_snapshot_digest(snapshot),
    }


def _owners() -> dict[str, object]:
    value = governed_owners()
    value["owner_groups"][1]["id"] = "sample-escalation"
    value["zones"][0]["tech_lead"]["escalation_route"] = "sample-escalation"
    return value


def _control(action: str, *, actor_type: str = "human", at: str = "2026-07-14T08:00:00Z") -> dict[str, object]:
    record = {
        "schema_version": "1.0",
        "id": f"control-{action}-1",
        "action": action,
        "trigger": "required-context-missing-or-contradictory",
        "severity": "high",
        "source_evidence": ["evidence/context-check.json"],
        "affected_work": ["sample-app:src/domain/service.py"],
        "safety_action": "Keep affected work non-mutating.",
        "accountable_actor": {
            "type": actor_type,
            "id": "sample-primary" if actor_type == "human" else "assistant",
            "role": "tech_lead",
        },
        "escalation_route": "sample-escalation",
        "response_expectation": "Resolve before further work.",
        "resume_conditions": ["canonical-context-restored"],
        "corrective_evidence": ["evidence/context-restored.json"] if action == "resume" else [],
        "residual_risk": "No known residual risk." if action == "resume" else "Context is incomplete.",
        "approvals": ([{
            "type": "human", "id": "sample-primary", "role": "tech_lead",
            "source_ref": "decisions/resume.yaml",
        }] if action == "resume" else []),
        "follow_up": "Continue source-linked review.",
        "recorded_at": at,
        "source_ref": f"controls/{action}-1.yaml",
        "policy_snapshot": _policy_ref(),
    }
    if action == "resume":
        record["target_active_record_ids"] = ["control-stop-1"]
        record["condition_evidence"] = [{
            "condition": "canonical-context-restored",
            "source_evidence": ["evidence/context-restored.json"],
        }]
    return record


def review_input() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "id": "sample-change",
        "classification": "minor",
        "status": "in_implementation",
        "evaluation_date": "2026-07-14",
        "policy_snapshot": _policy_ref(),
        "classification_report": {
            "source_ref": "reports/classification.json",
            "policy_snapshot": _policy_ref(),
            "status": "human-confirmed",
            "triggered_major": False,
        },
        "gate_reports": {
            "source_ref": "reports/gates.json",
            "policy_snapshot": _policy_ref(),
            "review_ready": "ready",
            "definition_of_ready": "ready",
            "definition_of_done": "ready",
            "release_transfer_readiness": "ready",
        },
        "requirements": [{"id": "REQ-1", "source_ref": "specs/sample/spec.md"}],
        "scenarios": [{"id": "SC-1", "source_ref": "specs/sample/spec.md"}],
        "design_decisions": [{"id": "ADR-1", "state": "accepted", "source_ref": "decisions/adr-1.md"}],
        "affected": [{"repository": "sample-app", "path": "src/domain/service.py", "zone": "sample-app"}],
        "dependencies": [{"id": "sample-dependency", "owner": "sample-primary", "source_ref": "design.md"}],
        "risks": [{"id": "R-1", "owner": "sample-primary", "source_ref": "risks.yaml"}],
        "scope": {
            "baseline": ["REQ-1"],
            "current": ["REQ-1"],
            "reassessment": {"state": "not-required", "source_ref": "decisions/scope.yaml"},
        },
        "architecture_disposition": {"state": "accepted", "source_ref": "decisions/adr-1.md"},
        "waivers": [],
        "deferrals": [],
        "control_records": [],
        "checkpoint": {"kind": "event-driven", "event": "change-updated", "source_ref": "config/checkpoints.yaml", "owner_ref": "sample-tech-leads"},
    }


def test_policy_compiles_to_immutable_source_bound_contract() -> None:
    compiled = compile_tech_lead_policy(_snapshot())

    assert compiled.policy_set == ("sdd-core", "1.0.0")
    assert compiled.snapshot_digest == policy_snapshot_digest(_snapshot())
    assert compiled.views == TECH_LEAD_VIEWS
    assert compiled.allowed_actions == ("stop", "hold", "escalate", "resume")
    assert "qa-approval" in compiled.forbidden_authorities
    assert compiled.policy_sources


def test_review_exposes_all_views_and_never_mutates_or_substitutes_approvals() -> None:
    report = evaluate_tech_lead_review(
        review_input(), _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()

    assert tuple(report["views"]) == TECH_LEAD_VIEWS
    assert report["status"] == "reviewable"
    assert report["decision_only"] is True
    assert report["control_state_mutated"] is False
    assert report["lifecycle_mutated"] is False
    assert report["release_recommendation"] == "recommend"
    assert report["independent_approvals"] == {
        role: "still-required"
        for role in ("qa", "product", "security", "release", "merge", "archive", "tracker")
    }
    for finding in report["findings"]:
        assert set(finding) == {
            "code", "severity", "blocking", "source_ref", "zone",
            "role", "action", "policy_snapshot",
        }


def test_mixed_snapshot_missing_context_scope_drift_and_expiry_fail_closed() -> None:
    document = review_input()
    document["classification_report"]["policy_snapshot"]["digest"] = "0" * 64
    document["requirements"] = []
    document["scope"]["current"].append("REQ-2")
    document["scope"]["reassessment"] = {"state": "missing", "source_ref": "decisions/scope.yaml"}
    document["waivers"] = [{
        "id": "W-1", "valid": True, "expires_on": "2026-07-13",
        "source_ref": "waivers/W-1.yaml",
    }]

    payload = evaluate_tech_lead_review(
        document, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()
    codes = {finding["code"] for finding in payload["findings"]}

    assert payload["status"] == "blocked"
    assert {
        "tech-lead.policy-snapshot-mismatch",
        "tech-lead.canonical-context-missing",
        "tech-lead.scope-reassessment-required",
        "tech-lead.waiver-expired",
    } <= codes


def test_stop_persists_and_ai_or_incomplete_resume_cannot_clear_it() -> None:
    records = [_control("stop")]
    stopped = check_control_state(records, _owners(), projects(), _snapshot())
    assert stopped.state == "stopped"
    assert stopped.resume_eligible is False
    assert stopped.control_state_mutated is False

    ai_resume = copy.deepcopy(_control("resume", actor_type="ai", at="2026-07-14T09:00:00Z"))
    invalid = check_control_state([*records, ai_resume], _owners(), projects(), _snapshot())
    assert invalid.state == "stopped"
    assert "tech-lead.control-ai-authority-forbidden" in {item.code for item in invalid.diagnostics}

    incomplete = _control("resume", at="2026-07-14T09:00:00Z")
    incomplete["corrective_evidence"] = []
    unresolved = check_control_state([*records, incomplete], _owners(), projects(), _snapshot())
    assert unresolved.state == "stopped"
    assert unresolved.resume_eligible is False


def test_authorized_resume_is_eligible_but_remains_check_only() -> None:
    hold = _control("hold")
    resume = _control("resume", at="2026-07-14T09:00:00Z")
    resume["target_active_record_ids"] = [hold["id"]]
    result = check_control_state(
        [hold, resume],
        _owners(), projects(), _snapshot(),
    )

    assert result.state == "resume-eligible"
    assert result.resume_eligible is True
    assert result.decision_only is True
    assert result.control_state_mutated is False
    assert result.lifecycle_mutated is False


def test_control_records_reject_duplicate_ids_and_out_of_order_sources() -> None:
    duplicate = [_control("stop"), _control("hold", at="2026-07-14T09:00:00Z")]
    duplicate[1]["id"] = duplicate[0]["id"]
    result = check_control_state(duplicate, _owners(), projects(), _snapshot())
    assert "tech-lead.control-id-duplicate" in {item.code for item in result.diagnostics}

    out_of_order = [
        _control("stop", at="2026-07-14T10:00:00Z"),
        _control("resume", at="2026-07-14T09:00:00Z"),
    ]
    result = check_control_state(out_of_order, _owners(), projects(), _snapshot())
    assert "tech-lead.control-order-invalid" in {item.code for item in result.diagnostics}


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("action", "approve", "tech-lead.control-action-unknown"),
        ("severity", "urgent", "tech-lead.control-severity-unknown"),
        ("trigger", "free-text-trigger", "tech-lead.control-trigger-unknown"),
    ],
)
def test_control_records_reject_unknown_protocol_values(
    field: str, value: str, code: str,
) -> None:
    record = _control("stop")
    record[field] = value

    result = check_control_state([record], _owners(), projects(), _snapshot())

    assert code in {item.code for item in result.diagnostics}


def test_resume_rejects_mixed_snapshot_ai_approval_and_incomplete_evidence() -> None:
    stopped = _control("stop")
    mixed = _control("resume", at="2026-07-14T09:00:00Z")
    mixed["policy_snapshot"]["digest"] = "0" * 64
    result = check_control_state([stopped, mixed], _owners(), projects(), _snapshot())
    assert "tech-lead.policy-snapshot-mismatch" in {item.code for item in result.diagnostics}

    ai_approval = _control("resume", at="2026-07-14T09:00:00Z")
    ai_approval["approvals"][0]["type"] = "ai"
    result = check_control_state([stopped, ai_approval], _owners(), projects(), _snapshot())
    assert "tech-lead.control-ai-approval-forbidden" in {item.code for item in result.diagnostics}

    incomplete = _control("resume", at="2026-07-14T09:00:00Z")
    incomplete["corrective_evidence"] = []
    result = check_control_state([stopped, incomplete], _owners(), projects(), _snapshot())
    assert "tech-lead.resume-evidence-incomplete" in {item.code for item in result.diagnostics}


def test_hotfix_follow_up_and_uncovered_owner_path_are_blocking_views() -> None:
    document = review_input()
    document["classification"] = "hotfix"
    document["deferrals"] = [{
        "id": "D-1", "reconciled": False, "source_ref": "deferrals/D-1.yaml",
    }]
    document["affected"][0]["path"] = "unowned/area.txt"

    payload = evaluate_tech_lead_review(
        document, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()
    codes = {item["code"] for item in payload["findings"]}

    assert "tech-lead.hotfix-follow-up-due" in codes
    assert "owners.affected-path-uncovered" in codes


def test_versioned_input_and_control_schemas_reject_free_text_authority() -> None:
    assert validate_tech_lead_input(review_input(), PROCESS) == []
    invalid = review_input()
    invalid["control_records"] = [_control("resume", actor_type="ai")]

    diagnostics = validate_tech_lead_input(invalid, PROCESS)

    assert diagnostics[0]["code"] == "tech-lead.input-schema-invalid"


def test_thin_review_and_control_clis_are_deterministic_and_non_mutating(
    tmp_path: Path, capsys,
) -> None:
    input_path = tmp_path / "review.yaml"
    owners_path = tmp_path / "owners.yaml"
    projects_path = tmp_path / "projects.yaml"
    input_path.write_text(yaml.safe_dump(review_input(), sort_keys=False), encoding="utf-8")
    owners_path.write_text(yaml.safe_dump(_owners(), sort_keys=False), encoding="utf-8")
    projects_path.write_text(yaml.safe_dump(projects(), sort_keys=False), encoding="utf-8")
    before = input_path.read_bytes()
    common = [
        str(input_path), "--owners", str(owners_path), "--projects", str(projects_path),
        "--config", str(CONFIG), "--as-of", "2026-07-14", "--json",
    ]

    assert review_main(common) == 0
    first = json.loads(capsys.readouterr().out)
    assert review_main(common) == 0
    assert json.loads(capsys.readouterr().out) == first
    assert first["control_state_mutated"] is False

    control_input = review_input()
    control_input["control_records"] = [_control("hold")]
    input_path.write_text(yaml.safe_dump(control_input, sort_keys=False), encoding="utf-8")
    held = input_path.read_bytes()
    assert control_main(common) == 1
    control_payload = json.loads(capsys.readouterr().out)
    assert control_payload["state"] == "held"
    assert control_payload["control_state_mutated"] is False
    assert input_path.read_bytes() == held
    assert before != held


def test_cli_malformed_paths_and_private_values_have_stable_redacted_exits(
    tmp_path: Path, capsys,
) -> None:
    private = tmp_path / "private-user-token-ghp_abcdefghijklmnopqrstuvwxyz1234567890.yaml"
    args = [
        str(private), "--owners", str(private), "--projects", str(private),
        "--config", str(private), "--as-of", "2026-07-14", "--json",
    ]

    assert review_main(args) == 2
    review_payload = capsys.readouterr().out
    assert json.loads(review_payload)["status"] == "usage"
    assert str(private) not in review_payload

    assert control_main(args) == 2
    control_payload = capsys.readouterr().out
    assert json.loads(control_payload)["status"] == "usage"
    assert str(private) not in control_payload


@pytest.mark.parametrize(
    "script",
    ["review_tech_lead.py", "check_tech_lead_control.py"],
)
def test_real_entry_points_import_package_from_any_working_directory(
    script: str, tmp_path: Path,
) -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 2
    assert json.loads(completed.stdout)["status"] == "usage"
    assert completed.stderr == ""
