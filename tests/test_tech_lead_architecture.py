"""Adversarial architecture tests for Phase 2 work item 2.6."""

from __future__ import annotations

import ast
import copy
import inspect
import textwrap
from types import MappingProxyType

import pytest

from process.validators.policy_validation import EffectiveRule, PolicySnapshot
from process.validators.tech_lead import (
    BLOCKING_CONTROL_DIAGNOSTICS,
    TechLeadPolicyError,
    check_control_state,
    compile_tech_lead_policy,
    evaluate_tech_lead_review,
    validate_tech_lead_input,
)
from tests.test_owner_governance import projects
from tests.test_tech_lead_review import (
    PROCESS,
    _control,
    _owners,
    _snapshot,
    review_input,
)


@pytest.mark.parametrize(
    ("mutate", "expected_code"),
    [
        (
            lambda row: row["policy_snapshot"].update({"digest": "0" * 64}),
            "tech-lead.policy-snapshot-mismatch",
        ),
        (
            lambda row: row.update({"trigger": "self-asserted-trigger"}),
            "tech-lead.control-trigger-unknown",
        ),
        (
            lambda row: row["accountable_actor"].update({"id": "self-appointed"}),
            "tech-lead.control-authority-forbidden",
        ),
        (
            lambda row: row.update({"affected_work": ["sample-app:unowned/file.py"]}),
            "owners.affected-path-uncovered",
        ),
        (
            lambda row: row.update({"escalation_route": "self-appointed"}),
            "tech-lead.control-escalation-conflict",
        ),
    ],
)
def test_invalid_authoritative_control_record_never_returns_clear_exit_zero(
    mutate, expected_code: str,
) -> None:
    record = _control("stop")
    mutate(record)

    result = check_control_state(
        [record], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "invalid"
    assert result.exit_code == 1
    assert result.resume_eligible is False
    assert expected_code in {item.code for item in result.diagnostics}
    assert result.control_state_mutated is False


def test_rfc3339_instants_are_utc_normalized_for_order_cutoff_and_provenance() -> None:
    stop = _control("stop", at="2026-07-15T01:00:00+02:00")
    included = check_control_state(
        [stop], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )
    assert included.state == "stopped"
    assert included.as_dict()["as_of_cutoff"] == "2026-07-14T23:59:59.999999Z"

    resume = _control("resume", at="2026-07-14T10:30:00+03:00")
    resume["target_active_record_ids"] = [stop["id"]]
    out_of_order = check_control_state(
        [_control("stop", at="2026-07-14T08:00:00Z"), resume],
        _owners(), projects(), _snapshot(), as_of="2026-07-14",
    )
    assert out_of_order.state == "invalid"
    assert "tech-lead.control-order-invalid" in {
        item.code for item in out_of_order.diagnostics
    }

    naive = _control("stop", at="2026-07-14T08:00:00")
    invalid = check_control_state(
        [naive], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )
    assert invalid.state == "invalid"
    assert "tech-lead.control-recorded-at-invalid" in {
        item.code for item in invalid.diagnostics
    }


def test_equal_utc_instants_fail_closed_instead_of_using_offset_representation() -> None:
    stop = _control("stop", at="2026-07-14T08:00:00Z")
    resume = _control("resume", at="2026-07-14T10:00:00+02:00")
    resume["target_active_record_ids"] = [stop["id"]]

    result = check_control_state(
        [stop, resume], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "invalid"
    assert result.exit_code == 1
    assert "tech-lead.control-time-tie" in {item.code for item in result.diagnostics}


@pytest.mark.parametrize(
    ("field", "value", "expected_code"),
    [
        ("event", "self-asserted-event", "tech-lead.checkpoint-unknown"),
        ("kind", "scheduled", "tech-lead.checkpoint-kind-conflict"),
        ("source_ref", "notes/self-asserted.yaml", "tech-lead.checkpoint-source-conflict"),
        ("owner_ref", "self-appointed", "tech-lead.checkpoint-owner-conflict"),
    ],
)
def test_checkpoint_must_match_canonical_policy_and_resolved_owner(
    field: str, value: str, expected_code: str,
) -> None:
    document = review_input()
    document["checkpoint"]["owner_ref"] = "sample-tech-leads"
    assert validate_tech_lead_input(document, PROCESS) == []
    document["checkpoint"][field] = value

    payload = evaluate_tech_lead_review(
        document, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()

    assert payload["status"] == "blocked"
    assert expected_code in {finding["code"] for finding in payload["findings"]}


def test_locked_finding_fields_are_compiled_and_tampering_fails_closed() -> None:
    snapshot = _snapshot()
    compiled = compile_tech_lead_policy(snapshot)
    assert compiled.finding_fields == (
        "code", "severity", "blocking", "source_ref", "zone", "role",
        "action", "policy_snapshot",
    )

    rules = dict(snapshot.rules)
    original = rules["tech-lead.finding-fields"]
    rules["tech-lead.finding-fields"] = EffectiveRule(
        value=tuple(item for item in original.value if item != "action"),
        source=original.source,
        policy_id=original.policy_id,
        policy_version=original.policy_version,
        pointer=original.pointer,
    )
    tampered = PolicySnapshot(
        policy_set_id=snapshot.policy_set_id,
        policy_set_version=snapshot.policy_set_version,
        rules=MappingProxyType(rules),
        corporate_values=snapshot.corporate_values,
    )

    with pytest.raises(TechLeadPolicyError, match="tech-lead.finding-fields"):
        compile_tech_lead_policy(tampered)


@pytest.mark.parametrize("position", ["before", "between", "after"])
@pytest.mark.parametrize(
    ("mutate", "expected_code"),
    [
        (
            lambda row: row["policy_snapshot"].update({"digest": "0" * 64}),
            "tech-lead.policy-snapshot-mismatch",
        ),
        (
            lambda row: row.update({"trigger": "self-asserted-trigger"}),
            "tech-lead.control-trigger-unknown",
        ),
        (
            lambda row: row["accountable_actor"].update({"id": "self-appointed"}),
            "tech-lead.control-authority-forbidden",
        ),
        (
            lambda row: row.update({"affected_work": ["sample-app:unowned/file.py"]}),
            "owners.affected-path-uncovered",
        ),
        (
            lambda row: row.update({"escalation_route": "self-appointed"}),
            "tech-lead.control-escalation-conflict",
        ),
        (
            lambda row: row.update({"recorded_at": "2026-07-15T08:00:00Z"}),
            "tech-lead.control-record-future",
        ),
    ],
)
def test_bad_authoritative_record_invalidates_eligible_sequence_in_any_position(
    position: str, mutate, expected_code: str,
) -> None:
    stop = _control("stop", at="2026-07-14T08:00:00Z")
    resume = _control("resume", at="2026-07-14T09:00:00Z")
    bad_times = {
        "before": "2026-07-14T07:00:00Z",
        "between": "2026-07-14T08:30:00Z",
        "after": "2026-07-14T10:00:00Z",
    }
    bad = _control("stop", at=bad_times[position])
    bad["id"] = "control-bad-1"
    bad["source_ref"] = "controls/bad-1.yaml"
    mutate(bad)
    records = {
        "before": [bad, stop, resume],
        "between": [stop, bad, resume],
        "after": [stop, resume, bad],
    }[position]

    result = check_control_state(
        records, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "invalid"
    assert result.resume_eligible is False
    assert result.exit_code == 1
    assert result.active_record_ids == (stop["id"],)
    assert expected_code in {item.code for item in result.diagnostics}
    assert result.control_state_mutated is False
    assert result.lifecycle_mutated is False


def test_every_local_control_diagnostic_is_in_the_blocking_catalog() -> None:
    tree = ast.parse(textwrap.dedent(inspect.getsource(check_control_state)))
    emitted = {
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_diag"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    }

    assert emitted == BLOCKING_CONTROL_DIAGNOSTICS


@pytest.mark.parametrize(
    ("case", "position", "expected_code"),
    [
        ("without-active", "before", "tech-lead.resume-without-active-control"),
        ("inactive-target", "between", "tech-lead.resume-target-inactive"),
        ("inactive-target", "after", "tech-lead.resume-target-inactive"),
        ("unaddressed", "between", "tech-lead.resume-active-records-unaddressed"),
        ("unaddressed", "after", "tech-lead.resume-active-records-unaddressed"),
        ("condition", "between", "tech-lead.resume-condition-evidence-incomplete"),
        ("condition", "after", "tech-lead.resume-condition-evidence-incomplete"),
        ("evidence", "between", "tech-lead.resume-evidence-incomplete"),
        ("evidence", "after", "tech-lead.resume-evidence-incomplete"),
    ],
)
def test_malformed_resume_diagnostic_invalidates_surrounding_valid_sequence(
    case: str, position: str, expected_code: str,
) -> None:
    stop = _control("stop", at="2026-07-14T08:00:00Z")
    active = [stop]
    if case == "unaddressed":
        active.append(_control("hold", at="2026-07-14T08:15:00Z"))

    valid = _control("resume", at="2026-07-14T09:00:00Z")
    valid["id"] = "control-valid-resume"
    valid["source_ref"] = "controls/valid-resume.yaml"
    valid["target_active_record_ids"] = [str(row["id"]) for row in active]

    bad_at = "2026-07-14T07:00:00Z" if position == "before" else (
        "2026-07-14T08:30:00Z" if position == "between" else "2026-07-14T10:00:00Z"
    )
    bad = _control("resume", at=bad_at)
    bad["id"] = "control-bad-resume"
    bad["source_ref"] = "controls/bad-resume.yaml"
    if case == "inactive-target":
        bad["target_active_record_ids"] = ["control-missing"]
    elif case == "unaddressed":
        bad["target_active_record_ids"] = [str(stop["id"])]
    elif case == "condition":
        bad["target_active_record_ids"] = [str(stop["id"])]
        bad["condition_evidence"] = [{
            "condition": "canonical-context-restored",
            "source_evidence": ["evidence/unbound.json"],
        }]
    elif case == "evidence":
        bad["target_active_record_ids"] = [str(stop["id"])]
        bad["corrective_evidence"] = []
        bad["approvals"] = []

    if position == "before":
        records = [bad, *active, valid]
    elif position == "between":
        records = [*active, bad, valid]
    else:
        records = [*active, valid, bad]

    result = check_control_state(
        records, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "invalid"
    assert result.exit_code == 1
    assert result.resume_eligible is False
    assert result.active_record_ids == tuple(str(row["id"]) for row in active)
    assert expected_code in {item.code for item in result.diagnostics}
    assert result.control_state_mutated is False
    assert result.lifecycle_mutated is False
