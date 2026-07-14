"""Scenario-first tests for class-aware artifact and business-gate reports."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from process.validators.artifact_gates import evaluate_gate
from process.validators.policy_validation import PolicySnapshot, validate_policy_bundle


ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / "process" / "policies"
FIXTURES = ROOT / "tests" / "fixtures" / "policy-v2"


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _snapshot() -> PolicySnapshot:
    result = validate_policy_bundle(
        ROOT / "process",
        _yaml(POLICIES / "manifest.yaml"),
        _yaml(FIXTURES / "config" / "valid-central.yaml"),
        None,
    )
    assert result.diagnostics == []
    assert result.snapshot is not None
    return result.snapshot


def _evidence(identifier: str, **updates: Any) -> dict[str, Any]:
    value = {
        "id": identifier,
        "state": "satisfied",
        "content": f"Reviewed substantive evidence for {identifier}.",
        "source_ref": f"evidence/{identifier}.md",
        "fresh": True,
    }
    value.update(updates)
    return value


def _required_ids(report: Any) -> set[str]:
    return {row["id"] for row in report.as_dict()["obligations"]}


def _satisfy(report: Any) -> list[dict[str, Any]]:
    return [_evidence(identifier) for identifier in sorted(_required_ids(report))]


def _gate(
    gate: str,
    classification: str,
    evidence: list[dict[str, Any]] | None = None,
    *,
    major_impact_hotfix: bool = False,
) -> Any:
    return evaluate_gate(
        {
            "id": "sample-change",
            "classification": classification,
            "major_impact_hotfix": major_impact_hotfix,
            "evidence": evidence or [],
        },
        _snapshot(),
        gate,
    )


def test_matrix_is_class_aware_and_major_impact_hotfix_retains_major_obligations() -> None:
    minor = _gate("definition-of-ready", "minor")
    major = _gate("definition-of-ready", "major")
    hotfix = _gate("definition-of-ready", "hotfix", major_impact_hotfix=True)

    assert "bounded-impact-risk-evidence" in _required_ids(minor)
    assert "expanded-design-impact-analysis" not in _required_ids(minor)
    assert "expanded-design-impact-analysis" in _required_ids(major)
    assert "harm-urgency-rationale" in _required_ids(hotfix)
    assert "expanded-design-impact-analysis" in _required_ids(hotfix)


def test_required_artifact_must_be_substantive_current_and_source_linked() -> None:
    empty = _gate("definition-of-ready", "minor")
    evidence = _satisfy(empty)
    target = next(row for row in evidence if row["id"] == "business-goal-value")

    for invalid in (
        {**target, "content": "TODO"},
        {**target, "content": "TODO: add evidence later"},
        {**target, "fresh": False},
        {**target, "source_ref": ""},
    ):
        candidate = [invalid if row["id"] == target["id"] else row for row in evidence]
        payload = _gate("definition-of-ready", "minor", candidate).as_dict()
        gap = next(row for row in payload["blocking_gaps"] if row["id"] == target["id"])
        assert gap["code"] in {
            "gate.placeholder-evidence",
            "gate.stale-evidence",
            "gate.source-missing",
        }


def test_conditional_not_applicable_requires_structured_human_rationale() -> None:
    empty = _gate("definition-of-ready", "major")
    evidence = _satisfy(empty)
    target_id = "architecture-decision-or-not-required"

    invalid = _evidence(
        target_id,
        state="not_applicable",
        content="Not needed.",
        rationale="No architectural boundary changes.",
        approver={"type": "ai", "id": "assistant"},
    )
    candidate = [invalid if row["id"] == target_id else row for row in evidence]
    assert _gate("definition-of-ready", "major", candidate).exit_code == 1

    invalid["approver"] = {"type": "human", "id": "sample-tech-lead"}
    report = _gate("definition-of-ready", "major", candidate)
    assert report.exit_code == 0
    row = next(row for row in report.as_dict()["obligations"] if row["id"] == target_id)
    assert row["state"] == "not_applicable"


def test_only_eligible_artifact_accepts_a_current_human_approved_waiver() -> None:
    empty = _gate("definition-of-ready", "major")
    evidence = _satisfy(empty)
    waiver = {
        "state": "waived",
        "content": "Existing regression suite is substitute evidence.",
        "source_ref": "decisions/W-17.yaml",
        "fresh": True,
        "waiver": {
            "reason": "No new automation surface.",
            "substitute_evidence": "runs/regression-17.json",
            "approver": {"type": "human", "id": "sample-qa-owner"},
            "residual_risk": "Manual coverage remains.",
            "follow_up": "Review after release.",
            "expired": False,
        },
    }

    eligible_id = "automation-plan-or-valid-waiver"
    valid = [{"id": eligible_id, **waiver} if row["id"] == eligible_id else row for row in evidence]
    assert _gate("definition-of-ready", "major", valid).exit_code == 0

    stale = [
        {**row, "fresh": False} if row["id"] == eligible_id else row
        for row in valid
    ]
    assert any(
        row["code"] == "gate.stale-evidence"
        for row in _gate(
            "definition-of-ready", "major", stale
        ).as_dict()["blocking_gaps"]
    )

    placeholder_waiver = copy.deepcopy(valid)
    next(
        row for row in placeholder_waiver if row["id"] == eligible_id
    )["waiver"]["reason"] = "TODO: justify later"
    assert any(
        row["code"] == "gate.waiver-invalid"
        for row in _gate(
            "definition-of-ready", "major", placeholder_waiver
        ).as_dict()["blocking_gaps"]
    )

    safety_id = "rollback-or-hold"
    invalid = [{"id": safety_id, **waiver} if row["id"] == safety_id else row for row in evidence]
    payload = _gate("definition-of-ready", "major", invalid).as_dict()
    assert any(
        row["id"] == safety_id and row["code"] == "gate.waiver-ineligible"
        for row in payload["blocking_gaps"]
    )


def test_hotfix_deferral_is_restricted_and_reconciliation_blocks_done() -> None:
    empty = _gate("definition-of-ready", "hotfix", major_impact_hotfix=True)
    evidence = _satisfy(empty)
    deferral = {
        "state": "deferred",
        "content": "Immediate substitute review completed.",
        "source_ref": "deferrals/D-2.yaml",
        "fresh": True,
        "deferral": {
            "substitute_evidence": "reviews/urgent-design.md",
            "owner": "sample-tech-lead",
            "approver": {"type": "human", "id": "sample-tech-lead"},
            "residual_risk": "Detailed design follows implementation.",
            "follow_up": "Complete before archive readiness.",
            "expiry": "ready_to_archive",
            "reconciled": False,
        },
    }
    allowed_id = "expanded-design-impact-analysis"
    allowed = [{"id": allowed_id, **deferral} if row["id"] == allowed_id else row for row in evidence]
    assert _gate("definition-of-ready", "hotfix", allowed, major_impact_hotfix=True).exit_code == 0

    safety_id = "minimum-safety-regression-evidence"
    rejected = [{"id": safety_id, **deferral} if row["id"] == safety_id else row for row in evidence]
    payload = _gate("definition-of-ready", "hotfix", rejected, major_impact_hotfix=True).as_dict()
    assert any(row["code"] == "gate.deferral-ineligible" for row in payload["blocking_gaps"])

    done = _gate("definition-of-done", "hotfix", allowed, major_impact_hotfix=True)
    assert any(
        row["code"] == "gate.hotfix-reconciliation-required"
        for row in done.as_dict()["blocking_gaps"]
    )


def test_all_named_reports_are_stable_and_keep_required_human_approval_explicit() -> None:
    gates = (
        "review-ready",
        "definition-of-ready",
        "implementation-complete",
        "definition-of-done",
        "release-transfer-readiness",
        "archive-readiness",
    )
    for gate in gates:
        initial = _gate(gate, "minor")
        evidence = _satisfy(initial)
        first = _gate(gate, "minor", evidence).as_dict()
        second = _gate(gate, "minor", copy.deepcopy(evidence)).as_dict()
        assert first == second
        assert first["gate"] == gate
        assert first["versions"]["tool"] == "0.3.0"
        assert first["versions"]["policy_set"] == {"id": "sdd-core", "version": "1.0.0"}
        assert {source["policy_id"] for source in first["policy_sources"]} >= {
            "artifact-matrix", "classification", "gates", "release"
        }
        assert first["human_approval"]["required"] is True
        assert first["human_approval"]["recorded"] is False
        assert first["status"] == "awaiting_human_approval"


def test_ai_completion_text_is_never_implementation_evidence() -> None:
    initial = _gate("implementation-complete", "minor")
    evidence = _satisfy(initial)
    target_id = "implementation-evidence"
    ai = _evidence(
        target_id,
        content="The AI assistant says implementation is complete.",
        source_ref="ai/run-42.txt",
        source_kind="ai-statement",
    )
    candidate = [ai if row["id"] == target_id else row for row in evidence]

    payload = _gate("implementation-complete", "minor", candidate).as_dict()

    assert payload["status"] == "blocked"
    assert any(row["code"] == "gate.ai-statement-not-evidence" for row in payload["blocking_gaps"])


def test_release_not_applicable_is_approved_and_does_not_infer_external_done() -> None:
    initial = _gate("release-transfer-readiness", "minor")
    evidence = _satisfy(initial)
    evidence.append({
        "id": "release-transfer-readiness",
        "state": "not_applicable",
        "content": "No releasable or transferable outcome.",
        "source_ref": "decisions/release-na.yaml",
        "fresh": True,
        "rationale": "Documentation-only internal correction.",
        "approver": {"type": "human", "id": "sample-tech-lead"},
    })

    payload = _gate("release-transfer-readiness", "minor", evidence).as_dict()

    assert payload["external_state"] == {
        "archived": False,
        "delivered": "unknown",
        "deployed": "unknown",
        "tracker_done": "unknown",
        "inferred": False,
    }


def test_evaluator_fails_closed_on_missing_or_wrong_policy_provenance() -> None:
    snapshot = _snapshot()
    rules = dict(snapshot.rules)
    rules.pop("gates.common-definition-of-ready")
    missing = replace(snapshot, rules=MappingProxyType(rules))
    report = evaluate_gate(
        {"id": "sample-change", "classification": "minor", "evidence": []},
        missing,
        "definition-of-ready",
    )
    assert report.exit_code == 1
    assert report.as_dict()["blocking_gaps"][0]["code"] == "gate.policy-contract-invalid"


def test_evaluator_fails_closed_when_canonical_gate_semantics_are_missing_or_changed() -> None:
    snapshot = _snapshot()
    required = (
        "artifacts.conditional-not-applicable",
        "artifacts.not-applicable-required-fields",
        "artifacts.waiver-eligible",
        "artifacts.waiver-required-fields",
        "artifacts.hotfix-deferrable",
        "artifacts.hotfix-deferral-required-fields",
        "artifacts.placeholder-markers",
        "gates.review-ready",
        "gates.implementation-complete",
        "gates.report-rule-relationships",
        "release.lifecycle-states",
        "release.forward-transitions",
        "release.transition-gates",
        "release.external-state-non-inference",
    )
    document = {"id": "sample-change", "classification": "minor", "evidence": []}

    for identifier in required:
        rules = dict(snapshot.rules)
        rules.pop(identifier, None)
        candidate = replace(snapshot, rules=MappingProxyType(rules))
        report = evaluate_gate(document, candidate, "definition-of-ready")
        assert report.exit_code == 1, identifier
        assert report.as_dict()["blocking_gaps"][0]["code"] == (
            "gate.policy-contract-invalid"
        ), identifier

    rules = dict(snapshot.rules)
    rules["artifacts.waiver-eligible"] = replace(
        rules["artifacts.waiver-eligible"], value=("unknown-artifact",)
    )
    changed = replace(snapshot, rules=MappingProxyType(rules))
    assert evaluate_gate(document, changed, "definition-of-ready").exit_code == 1

    rules = dict(snapshot.rules)
    rules["release.forward-transitions"] = replace(
        rules["release.forward-transitions"],
        value=MappingProxyType({"draft": ("approved",)}),
    )
    malformed = replace(snapshot, rules=MappingProxyType(rules))
    assert evaluate_gate(document, malformed, "definition-of-ready").exit_code == 1

    rules = dict(snapshot.rules)
    rules["release.distinct-states"] = replace(
        rules["release.distinct-states"], policy_id="gates"
    )
    wrong_source = replace(snapshot, rules=MappingProxyType(rules))
    report = evaluate_gate(document, wrong_source, "definition-of-ready")
    assert report.exit_code == 1
    assert report.as_dict()["blocking_gaps"][0]["code"] == "gate.policy-contract-invalid"


def test_evidence_valid_through_is_inclusive_and_stale_on_the_next_day() -> None:
    initial = evaluate_gate(
        {
            "id": "sample-change",
            "classification": "minor",
            "evaluation_date": "2026-07-14",
            "evidence": [],
        },
        _snapshot(),
        "implementation-complete",
    )
    evidence = _satisfy(initial)
    target_id = "implementation-evidence"
    for valid_through, expected_code in (
        ("2026-07-14", None),
        ("2026-07-13", "gate.stale-evidence"),
        ("not-a-date", "gate.freshness-invalid"),
    ):
        candidate = [
            {**row, "valid_through": valid_through}
            if row["id"] == target_id else row
            for row in evidence
        ]
        report = evaluate_gate(
            {
                "id": "sample-change",
                "classification": "minor",
                "evaluation_date": "2026-07-14",
                "evidence": candidate,
            },
            _snapshot(),
            "implementation-complete",
        )
        codes = {item["code"] for item in report.as_dict()["blocking_gaps"]}
        assert (expected_code in codes) if expected_code else not codes
