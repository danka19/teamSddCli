"""Scenario-first tests for read-only lifecycle transition decisions."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import yaml

from process.validators.artifact_gates import evaluate_gate
from process.validators.lifecycle import check_transition
from process.validators.policy_validation import PolicySnapshot, validate_policy_bundle
from scripts.check_lifecycle_transition import main as transition_main


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


def _document(status: str, classification: str = "minor") -> dict[str, Any]:
    snapshot = _snapshot()
    base: dict[str, Any] = {
        "schema_version": "1.0",
        "id": "sample-change",
        "status": status,
        "classification": classification,
        "evaluation_date": "2026-07-14",
        "major_impact_hotfix": False,
        "evidence": [],
        "approvals": [
            {
                "owner_type": "human",
                "owner_id": owner,
                "state": "approved",
                "evidence_ref": f"decisions/{owner}.yaml",
            }
            for owner in ("sample-tech-leads", "sample-qa-owners")
        ],
        "transition_approvals": [
            {
                "transition": transition,
                "owner_type": "human",
                "owner_id": "sample-tech-leads",
                "state": "approved",
                "evidence_ref": f"decisions/{transition.replace('->', '-')}.yaml",
                **({"reason": "Review requires a documented rework loop."} if transition in {
                    "spec_review->draft", "ready_to_archive->in_implementation"
                } else {}),
            }
            for transition in (
                "spec_review->draft",
                "spec_review->approved",
                "approved->in_implementation",
                "ready_to_archive->in_implementation",
                "ready_to_archive->archived",
            )
        ],
        "external_state": {
            "delivered": "unknown",
            "deployed": "unknown",
            "tracker_done": "unknown",
        },
    }
    required: set[str] = set()
    for gate in (
        "review-ready",
        "definition-of-ready",
        "implementation-complete",
        "definition-of-done",
        "release-transfer-readiness",
        "archive-readiness",
    ):
        report = evaluate_gate(base, snapshot, gate)
        required.update(row["id"] for row in report.as_dict()["obligations"])
    base["evidence"] = [_evidence(identifier) for identifier in sorted(required)]
    return base


def test_each_forward_adjacent_transition_uses_the_canonical_gate_relationship() -> None:
    cases = {
        ("draft", "spec_review"): ["review-ready"],
        ("spec_review", "approved"): ["definition-of-ready"],
        ("approved", "in_implementation"): ["implementation-start-approval"],
        ("in_implementation", "ready_to_archive"): [
            "implementation-complete",
            "definition-of-done",
            "release-transfer-readiness",
        ],
        ("ready_to_archive", "archived"): [
            "archive-readiness",
            "archive-approval",
        ],
    }

    for (current, target), required_gates in cases.items():
        document = _document(current)
        before = copy.deepcopy(document)
        report = check_transition(document, target, _snapshot())
        assert report.exit_code == 0, (current, target, report.as_dict())
        assert report.as_dict()["allowed"] is True
        assert report.as_dict()["required_gates"] == required_gates
        assert document == before
        assert report.as_dict()["lifecycle_mutated"] is False


def test_canonical_rework_transitions_require_reason_authority_and_evidence() -> None:
    for current, target in (
        ("spec_review", "draft"),
        ("ready_to_archive", "in_implementation"),
    ):
        document = _document(current)
        record = next(
            row for row in document["transition_approvals"]
            if row["transition"] == f"{current}->{target}"
        )
        record["reason"] = "Review found specific evidence that requires rework."
        before = copy.deepcopy(document)

        report = check_transition(document, target, _snapshot())

        assert report.exit_code == 0, report.as_dict()
        assert report.as_dict()["allowed"] is True
        assert report.as_dict()["human_approval"] == {
            "required": True,
            "recorded": True,
        }
        assert document == before

        for missing in ("reason", "evidence_ref"):
            invalid = copy.deepcopy(document)
            invalid_record = next(
                row for row in invalid["transition_approvals"]
                if row["transition"] == f"{current}->{target}"
            )
            invalid_record.pop(missing)
            blocked = check_transition(invalid, target, _snapshot())
            assert blocked.exit_code == 1
            assert any(
                item["code"] == "lifecycle.rework-authorization-required"
                for item in blocked.as_dict()["blockers"]
            )

        unauthorized = copy.deepcopy(document)
        unauthorized_record = next(
            row for row in unauthorized["transition_approvals"]
            if row["transition"] == f"{current}->{target}"
        )
        unauthorized_record["owner_id"] = "arbitrary-human"
        assert check_transition(unauthorized, target, _snapshot()).exit_code == 1


def test_other_skipped_backward_same_and_unknown_transitions_are_rejected() -> None:
    for current, target in (
        ("draft", "approved"),
        ("approved", "spec_review"),
        ("approved", "approved"),
        ("archived", "ready_to_archive"),
        ("unknown", "draft"),
        ("draft", "unknown"),
    ):
        report = check_transition(_document(current), target, _snapshot())
        assert report.exit_code == 1, (current, target)
        assert report.as_dict()["allowed"] is False
        assert report.as_dict()["blockers"][0]["code"] in {
            "lifecycle.state-invalid",
            "lifecycle.transition-not-allowed",
        }


def test_dor_start_and_archive_require_transition_specific_human_approval() -> None:
    for current, target in (
        ("spec_review", "approved"),
        ("approved", "in_implementation"),
        ("ready_to_archive", "archived"),
    ):
        document = _document(current)
        document["transition_approvals"] = [
            {
                "transition": f"{current}->{target}",
                "owner_type": "ai",
                "owner_id": "assistant",
                "state": "approved",
                "evidence_ref": "ai/run.txt",
            }
        ]
        report = check_transition(document, target, _snapshot())
        assert report.exit_code == 1
        assert any(
            item["code"] == "lifecycle.human-approval-required"
            for item in report.as_dict()["blockers"]
        )


def test_archive_readiness_rejects_bad_evidence_and_unresolved_hotfix_follow_up() -> None:
    document = _document("in_implementation", "hotfix")
    document["major_impact_hotfix"] = True
    target = _evidence("expanded-design-impact-analysis", **{
        "state": "deferred",
        "content": "Immediate substitute review completed.",
        "source_ref": "deferrals/D-2.yaml",
        "deferral": {
            "substitute_evidence": "reviews/urgent-design.md",
            "owner": "sample-tech-leads",
            "approver": {"type": "human", "id": "sample-tech-leads"},
            "residual_risk": "Detailed design follows implementation.",
            "follow_up": "Complete before archive readiness.",
            "expiry": {"type": "lifecycle_state", "lifecycle_state": "ready_to_archive"},
            "reconciled": False,
        },
    })
    document["evidence"].append(target)

    report = check_transition(document, "ready_to_archive", _snapshot())

    assert report.exit_code == 1
    assert any(
        item["code"] == "gate.hotfix-reconciliation-required"
        for item in report.as_dict()["blockers"]
    )


def test_transition_never_infers_delivery_deployment_or_tracker_done_from_archive() -> None:
    report = check_transition(_document("ready_to_archive"), "archived", _snapshot())

    assert report.as_dict()["external_state"] == {
        "archived": False,
        "delivered": "unknown",
        "deployed": "unknown",
        "tracker_done": "unknown",
        "inferred": False,
    }


def test_transition_cli_has_stable_human_json_and_exit_contract(tmp_path: Path, capsys) -> None:
    config = FIXTURES / "config" / "valid-central.yaml"
    valid_path = tmp_path / "valid.yaml"
    valid_path.write_text(
        yaml.safe_dump(_document("draft"), sort_keys=False), encoding="utf-8"
    )

    assert transition_main([
        str(valid_path), "--to", "spec_review", "--config", str(config), "--json"
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["allowed"] is True
    assert payload["lifecycle_mutated"] is False

    assert transition_main([
        str(valid_path), "--to", "archived", "--config", str(config)
    ]) == 1
    assert "Transition: blocked" in capsys.readouterr().out

    assert transition_main(["--json"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "usage"

    missing = tmp_path / "missing.yaml"
    assert transition_main([
        str(missing), "--to", "spec_review", "--config", str(config), "--json"
    ]) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "error"


def test_transition_blocks_when_gate_evidence_is_valid_but_approval_is_pending() -> None:
    document = _document("draft")
    document["approvals"] = []

    report = check_transition(document, "spec_review", _snapshot())

    assert report.exit_code == 1
    gate_report = report.as_dict()["gate_reports"][0]
    assert gate_report["blocking_gaps"] == []
    assert gate_report["status"] == "awaiting_human_approval"
    assert report.as_dict()["human_approval"] == {
        "required": True,
        "recorded": False,
    }
    assert any(
        item["code"] == "lifecycle.human-approval-required"
        for item in report.as_dict()["blockers"]
    )


SCENARIO_COVERAGE = {'test_archive_readiness_rejects_bad_evidence_and_unresolved_hotfix_follow_up': [{'capability': 'change-lifecycle',
                                                                                  'requirement': 'Delivered state is '
                                                                                                 'external to archive '
                                                                                                 'state',
                                                                                  'scenario': 'Archived spec may '
                                                                                              'precede or follow '
                                                                                              'delivery',
                                                                                  'source_kind': 'delta'},
                                                                                 {'capability': 'change-lifecycle',
                                                                                  'requirement': 'Lifecycle states',
                                                                                  'scenario': 'Hotfix accelerates '
                                                                                              'sequence but not '
                                                                                              'accountability',
                                                                                  'source_kind': 'delta'},
                                                                                 {'capability': 'change-lifecycle',
                                                                                  'requirement': 'Named corporate '
                                                                                                 'business gates',
                                                                                  'scenario': 'Definition of Done '
                                                                                              'precedes archive '
                                                                                              'readiness',
                                                                                  'source_kind': 'delta'}],
 'test_dor_start_and_archive_require_transition_specific_human_approval': [{'capability': 'change-lifecycle',
                                                                            'requirement': 'Deterministic transition '
                                                                                           'gates',
                                                                            'scenario': 'Approval transition checks '
                                                                                        'Definition of Ready',
                                                                            'source_kind': 'delta'},
                                                                           {'capability': 'change-lifecycle',
                                                                            'requirement': 'Deterministic transition '
                                                                                           'gates',
                                                                            'scenario': 'Draft cannot skip to archive '
                                                                                        'readiness',
                                                                            'source_kind': 'delta'},
                                                                           {'capability': 'change-lifecycle',
                                                                            'requirement': 'Deterministic transition '
                                                                                           'gates',
                                                                            'scenario': 'Archive requires explicit '
                                                                                        'human approval',
                                                                            'source_kind': 'delta'},
                                                                           {'capability': 'change-lifecycle',
                                                                            'requirement': 'Named corporate business '
                                                                                           'gates',
                                                                            'scenario': 'Definition of Ready precedes '
                                                                                        'approval',
                                                                            'source_kind': 'delta'}],
 'test_each_forward_adjacent_transition_uses_the_canonical_gate_relationship': [{'capability': 'change-lifecycle',
                                                                                 'requirement': 'Deterministic '
                                                                                                'transition gates',
                                                                                 'scenario': 'Allowed transitions are '
                                                                                             'explicit',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Deterministic '
                                                                                                'transition gates',
                                                                                 'scenario': 'Spec PR transition '
                                                                                             'checks structure',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Deterministic '
                                                                                                'transition gates',
                                                                                 'scenario': 'Draft cannot skip to '
                                                                                             'approved',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Deterministic '
                                                                                                'transition gates',
                                                                                 'scenario': 'Lifecycle expiry '
                                                                                             'remains due after '
                                                                                             'rework',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Lifecycle states',
                                                                                 'scenario': 'Minor route remains '
                                                                                             'compact',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Lifecycle states',
                                                                                 'scenario': 'Major route uses '
                                                                                             'expanded gates',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'MVP boundary for '
                                                                                                'lifecycle automation',
                                                                                 'scenario': 'Core process is '
                                                                                             'AI-disabled and '
                                                                                             'integration-independent',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'MVP boundary for '
                                                                                                'lifecycle automation',
                                                                                 'scenario': 'Deferred integration is '
                                                                                             'not fabricated',
                                                                                 'source_kind': 'delta'},
                                                                                {'capability': 'change-lifecycle',
                                                                                 'requirement': 'Named corporate '
                                                                                                'business gates',
                                                                                 'scenario': 'Review-ready gate '
                                                                                             'precedes Spec Review',
                                                                                 'source_kind': 'delta'}],
 'test_transition_never_infers_delivery_deployment_or_tracker_done_from_archive': [{'capability': 'change-lifecycle',
                                                                                    'requirement': 'Delivered state '
                                                                                                   'is external to '
                                                                                                   'archive state',
                                                                                    'scenario': 'Tracker transition '
                                                                                                'uses mapping',
                                                                                    'source_kind': 'delta'},
                                                                                   {'capability': 'change-lifecycle',
                                                                                    'requirement': 'Deterministic '
                                                                                                   'transition gates',
                                                                                    'scenario': 'Archive-readiness '
                                                                                                'transition checks '
                                                                                                'Definition of Done',
                                                                                    'source_kind': 'delta'}]}
