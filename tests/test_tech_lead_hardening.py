"""Adversarial regression tests for Phase 2 work item 2.6 review findings."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from process.validators.owners import AffectedPath, resolve_tech_lead_ownership
from process.validators.tech_lead import (
    check_control_state,
    evaluate_tech_lead_review,
    validate_tech_lead_input,
)
from scripts.check_tech_lead_control import main as control_main
from scripts.review_tech_lead import main as review_main
from tests.test_owner_governance import governed_owners, policy_snapshot, projects
from tests.test_tech_lead_review import (
    CONFIG,
    PROCESS,
    _control,
    _owners,
    _snapshot,
    review_input,
)


def _codes(payload: dict[str, object]) -> set[str]:
    return {row["code"] for row in payload["findings"]}


@pytest.mark.parametrize(
    ("source", "status", "expected"),
    [
        ("classification_report", "blocked", "tech-lead.classification-blocked"),
        ("classification_report", "invalid", "tech-lead.classification-invalid"),
        ("review_ready", "blocked", "tech-lead.review-ready-blocked"),
        ("definition_of_ready", "invalid", "tech-lead.dor-invalid"),
        ("definition_of_done", "blocked", "tech-lead.dod-blocked"),
        ("release_transfer_readiness", "invalid", "tech-lead.release-invalid"),
    ],
)
def test_non_green_source_reports_block_review_and_release_recommendation(
    source: str, status: str, expected: str,
) -> None:
    document = review_input()
    document["gate_reports"]["review_ready"] = "ready"
    if source == "classification_report":
        document[source]["status"] = status
    else:
        document["gate_reports"][source] = status

    payload = evaluate_tech_lead_review(
        document, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()

    assert payload["status"] == "blocked"
    assert payload["release_recommendation"] == "do-not-recommend"
    assert expected in _codes(payload)


def test_review_schema_closes_classification_and_gate_report_status_enums() -> None:
    document = review_input()
    document["gate_reports"]["review_ready"] = "ready"
    assert validate_tech_lead_input(document, PROCESS) == []

    for container, field in (
        ("classification_report", "status"),
        ("gate_reports", "review_ready"),
        ("gate_reports", "definition_of_ready"),
        ("gate_reports", "definition_of_done"),
        ("gate_reports", "release_transfer_readiness"),
    ):
        invalid = copy.deepcopy(document)
        invalid[container][field] = "free-text-green"
        diagnostics = validate_tech_lead_input(invalid, PROCESS)
        assert diagnostics and diagnostics[0]["code"] == "tech-lead.input-schema-invalid"


def _resume_resolution(record: dict[str, object], target: dict[str, object]) -> None:
    record["target_active_record_ids"] = [target["id"]]
    record["condition_evidence"] = [
        {
            "condition": condition,
            "source_evidence": ["evidence/context-restored.json"],
        }
        for condition in target["resume_conditions"]
    ]


def test_standalone_resume_is_invalid_and_cannot_be_eligible() -> None:
    resume = _control("resume")
    resume["target_active_record_ids"] = ["control-hold-1"]
    resume["condition_evidence"] = [{
        "condition": "canonical-context-restored",
        "source_evidence": ["evidence/context-restored.json"],
    }]

    result = check_control_state(
        [resume], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "invalid"
    assert result.resume_eligible is False
    assert "tech-lead.resume-without-active-control" in {
        item.code for item in result.diagnostics
    }


def test_resume_requires_condition_bound_evidence_for_every_targeted_record() -> None:
    stop = _control("stop")
    stop["resume_conditions"] = ["canonical-context-restored", "tests-green"]
    resume = _control("resume", at="2026-07-14T09:00:00Z")
    resume["target_active_record_ids"] = [stop["id"]]
    resume["condition_evidence"] = [{
        "condition": "canonical-context-restored",
        "source_evidence": ["evidence/unrelated.json"],
    }]

    result = check_control_state(
        [stop, resume], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "stopped"
    assert result.resume_eligible is False
    assert result.active_record_ids == (stop["id"],)
    assert "tech-lead.resume-condition-evidence-incomplete" in {
        item.code for item in result.diagnostics
    }


def test_resume_must_address_all_active_records_and_remains_check_only() -> None:
    stop = _control("stop")
    hold = _control("hold", at="2026-07-14T08:30:00Z")
    resume = _control("resume", at="2026-07-14T09:00:00Z")
    _resume_resolution(resume, stop)

    result = check_control_state(
        [stop, hold, resume], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )

    assert result.state == "held"
    assert result.resume_eligible is False
    assert result.active_record_ids == (stop["id"], hold["id"])
    assert result.control_state_mutated is False
    assert "tech-lead.resume-active-records-unaddressed" in {
        item.code for item in result.diagnostics
    }


def test_control_schema_requires_explicit_resume_targets_and_condition_evidence() -> None:
    document = review_input()
    document["gate_reports"]["review_ready"] = "ready"
    document["control_records"] = [_control("hold")]
    resume = _control("resume", at="2026-07-14T09:00:00Z")
    resume.pop("target_active_record_ids")
    resume.pop("condition_evidence")
    document["control_records"].append(resume)

    diagnostics = validate_tech_lead_input(document, PROCESS)

    assert diagnostics and diagnostics[0]["code"] == "tech-lead.input-schema-invalid"


@pytest.mark.parametrize("conflict", ["delegate", "escalation"])
def test_overlapping_zones_reject_every_incompatible_governance_field(
    conflict: str,
) -> None:
    owners = governed_owners()
    second = copy.deepcopy(owners["zones"][0])
    second["id"] = "sample-app-nested"
    second["paths"] = ["src/domain/**"]
    if conflict == "delegate":
        second["tech_lead"]["delegates"][0]["authority"] = ["resume"]
    else:
        owners["owner_groups"][1]["members"].append("sample-escalation-owner-two")
        second["tech_lead"]["escalation_route"] = "sample-escalation-owner-two"
    owners["zones"].append(second)
    registered = projects()
    registered["projects"][0]["owner_zones"].append(second["id"])

    resolution = resolve_tech_lead_ownership(
        owners,
        registered,
        [AffectedPath("sample-app", "src/domain/service.py")],
        policy_snapshot(),
    )

    assert [item.code for item in resolution.diagnostics] == [
        f"owners.{conflict}-conflict"
    ]


@pytest.mark.parametrize(
    ("field", "value", "expected"),
    [
        ("primary", None, "owners.primary-missing"),
        ("authority", "resume", "owners.authority-invalid"),
        ("escalation_route", ["sample-escalation"], "owners.escalation-invalid"),
    ],
)
def test_malformed_v2_governance_returns_diagnostics_instead_of_keyerror(
    field: str, value: object, expected: str,
) -> None:
    owners = governed_owners()
    if value is None:
        del owners["zones"][0]["tech_lead"][field]
    else:
        owners["zones"][0]["tech_lead"][field] = value

    resolution = resolve_tech_lead_ownership(
        owners,
        projects(),
        [AffectedPath("sample-app", "src/domain/service.py")],
        policy_snapshot(),
    )

    assert expected in {item.code for item in resolution.diagnostics}


def test_cli_rejects_malformed_owner_v2_with_stable_redacted_exit_3(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    private_marker = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
    document = review_input()
    document["gate_reports"]["review_ready"] = "ready"
    owners = _owners()
    owners["zones"][0]["tech_lead"]["authority"] = private_marker
    input_path = tmp_path / "review.yaml"
    owners_path = tmp_path / f"owners-{private_marker}.yaml"
    projects_path = tmp_path / "projects.yaml"
    input_path.write_text(yaml.safe_dump(document), encoding="utf-8")
    owners_path.write_text(yaml.safe_dump(owners), encoding="utf-8")
    projects_path.write_text(yaml.safe_dump(projects()), encoding="utf-8")
    args = [
        str(input_path), "--owners", str(owners_path), "--projects", str(projects_path),
        "--config", str(CONFIG), "--as-of", "2026-07-14", "--json",
    ]

    for cli in (review_main, control_main):
        assert cli(args) == 3
        raw = capsys.readouterr().out
        payload = json.loads(raw)
        assert payload["diagnostics"][0]["code"] == "owners.schema-invalid"
        assert private_marker not in raw


def test_as_of_filters_future_controls_before_state_derivation() -> None:
    future = _control("stop", at="2026-07-15T08:00:00Z")

    result = check_control_state(
        [future], _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )
    payload = result.as_dict()

    assert result.state == "invalid"
    assert result.active_record_ids == ()
    assert "tech-lead.control-record-future" in {
        item.code for item in result.diagnostics
    }
    assert payload["as_of"] == "2026-07-14"
    assert payload["evaluation_date"] == "2026-07-14"
    assert payload["snapshot_digest"] == _control("stop")["policy_snapshot"]["digest"]


def test_review_binds_as_of_to_evaluation_date_and_provenance() -> None:
    document = review_input()
    document["gate_reports"]["review_ready"] = "ready"
    document["evaluation_date"] = "2026-07-13"

    payload = evaluate_tech_lead_review(
        document, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    ).as_dict()

    assert payload["status"] == "blocked"
    assert "tech-lead.evaluation-date-mismatch" in _codes(payload)
    assert payload["as_of"] == "2026-07-14"
    assert payload["evaluation_date"] == "2026-07-13"
    assert payload["snapshot_digest"] == payload["policy_snapshot"]["digest"]

    control = check_control_state(
        [], _owners(), projects(), _snapshot(),
        as_of="2026-07-14", evaluation_date="2026-07-13",
    )
    assert control.state == "invalid"
    assert "tech-lead.evaluation-date-mismatch" in {
        item.code for item in control.diagnostics
    }


def test_cli_rejects_invalid_as_of_with_stable_exit_3(
    tmp_path: Path, capsys: pytest.CaptureFixture[str],
) -> None:
    document = review_input()
    input_path = tmp_path / "review.yaml"
    owners_path = tmp_path / "owners.yaml"
    projects_path = tmp_path / "projects.yaml"
    input_path.write_text(yaml.safe_dump(document), encoding="utf-8")
    owners_path.write_text(yaml.safe_dump(_owners()), encoding="utf-8")
    projects_path.write_text(yaml.safe_dump(projects()), encoding="utf-8")
    args = [
        str(input_path), "--owners", str(owners_path), "--projects", str(projects_path),
        "--config", str(CONFIG), "--as-of", "not-a-date", "--json",
    ]

    for cli in (review_main, control_main):
        assert cli(args) == 3
        payload = json.loads(capsys.readouterr().out)
        assert payload["diagnostics"] == [{"code": "tech-lead.as-of-invalid"}]
