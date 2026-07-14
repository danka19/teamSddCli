"""Read-only lifecycle transition checks over the canonical policy snapshot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .artifact_gates import (
    TOOL_VERSION,
    GateReport,
    compile_gate_policy,
    evaluate_gate,
)
from .policy_validation import PolicySnapshot


@dataclass(frozen=True)
class TransitionReport:
    payload: dict[str, Any]

    @property
    def exit_code(self) -> int:
        return 0 if self.payload["allowed"] else 1

    def as_dict(self) -> dict[str, Any]:
        return self.payload

    def render_human(self) -> str:
        state = "allowed" if self.payload["allowed"] else "blocked"
        lines = [
            f"Transition: {state}",
            f"From: {self.payload['current_state']}",
            f"To: {self.payload['target_state']}",
            "Required gates:",
            *(f"- {gate}" for gate in self.payload["required_gates"]),
            "Blockers:",
            *(
                f"- {item['code']}: {item['message']}"
                for item in self.payload["blockers"]
            ),
            "Human decision is still required; this report does not mutate state."
        ]
        return "\n".join(lines)


def check_transition(
    document: dict[str, Any], target_state: str, snapshot: PolicySnapshot
) -> TransitionReport:
    """Return a transition decision without modifying the supplied document."""
    current_state = document.get("status")
    try:
        policy = compile_gate_policy(snapshot)
    except ValueError as error:
        return _report(
            document,
            target_state,
            (),
            [],
            [_blocker("lifecycle.policy-contract-invalid", str(error))],
            snapshot,
        )

    if current_state not in policy.lifecycle_states or target_state not in policy.lifecycle_states:
        return _report(
            document,
            target_state,
            (),
            [],
            [_blocker(
                "lifecycle.state-invalid",
                "Current and target states must use the accepted six-state lifecycle.",
            )],
            snapshot,
            policy=policy,
        )

    transition = f"{current_state}->{target_state}"
    if target_state not in policy.forward_transitions[current_state]:
        return _report(
            document,
            target_state,
            (),
            [],
            [_blocker(
                "lifecycle.transition-not-allowed",
                "Only a configured canonical lifecycle transition is allowed.",
            )],
            snapshot,
            policy=policy,
        )

    required_gates = policy.transition_gates[transition]
    gate_reports: list[GateReport] = []
    blockers: list[dict[str, str]] = []
    for gate in required_gates:
        if gate in {"implementation-start-approval", "archive-approval"}:
            continue
        report = evaluate_gate(document, snapshot, gate)
        gate_reports.append(report)
        blockers.extend(report.as_dict()["blocking_gaps"])
        if report.as_dict()["status"] == "awaiting_human_approval":
            blockers.append(_blocker(
                "lifecycle.human-approval-required",
                "Valid gate evidence does not replace the configured human approval.",
            ))

    transition_approval_required = transition in {
        "spec_review->draft",
        "spec_review->approved",
        "approved->in_implementation",
        "ready_to_archive->in_implementation",
        "ready_to_archive->archived",
    }
    transition_approval_recorded = (
        not transition_approval_required
        or _transition_approval_recorded(
            document,
            transition,
            _authorized_approvers(policy, document),
            require_reason=transition in {
                "spec_review->draft", "ready_to_archive->in_implementation"
            },
        )
    )
    if transition_approval_required and not transition_approval_recorded:
        rework = transition in {
            "spec_review->draft", "ready_to_archive->in_implementation"
        }
        blockers.append(_blocker(
            "lifecycle.rework-authorization-required" if rework
            else "lifecycle.human-approval-required",
            "Rework requires an authorized source-linked human reason."
            if rework else
            "This transition requires an authorized source-linked human decision; AI cannot approve it.",
        ))

    gate_approval_rows = [
        report.as_dict()["human_approval"] for report in gate_reports
        if report.as_dict()["human_approval"]["required"]
    ]
    approval_required = transition_approval_required or bool(gate_approval_rows)
    approval_recorded = transition_approval_recorded and all(
        row["recorded"] for row in gate_approval_rows
    )

    return _report(
        document,
        target_state,
        required_gates,
        gate_reports,
        blockers,
        snapshot,
        policy=policy,
        approval_required=approval_required,
        approval_recorded=approval_recorded,
    )


def _authorized_approvers(policy: Any, document: Mapping[str, Any]) -> tuple[str, ...]:
    classification = document.get("classification")
    slots = policy.reviewer_slots.get(classification, ())
    return tuple(
        policy.corporate_values[slot]
        for slot in slots
        if isinstance(policy.corporate_values.get(slot), str)
    )


def _transition_approval_recorded(
    document: Mapping[str, Any],
    transition: str,
    authorized: tuple[str, ...],
    *,
    require_reason: bool = False,
) -> bool:
    rows = document.get("transition_approvals")
    if not isinstance(rows, list) or not authorized:
        return False
    return any(
        isinstance(row, dict)
        and row.get("transition") == transition
        and row.get("owner_type") == "human"
        and row.get("owner_id") in authorized
        and row.get("state") == "approved"
        and bool(row.get("evidence_ref"))
        and (not require_reason or bool(row.get("reason")))
        for row in rows
    )


def _report(
    document: Mapping[str, Any],
    target_state: str,
    required_gates: tuple[str, ...],
    gate_reports: list[GateReport],
    blockers: list[dict[str, str]],
    snapshot: PolicySnapshot,
    *,
    policy: Any | None = None,
    approval_required: bool = False,
    approval_recorded: bool = False,
) -> TransitionReport:
    unique_blockers = {
        (item["code"], item.get("id", "transition"), item["message"]): {
            "code": item["code"],
            "id": item.get("id", "transition"),
            "message": item["message"],
        }
        for item in blockers
    }
    payload = {
        "schema_version": "1.0",
        "status": "blocked" if unique_blockers else "allowed",
        "allowed": not unique_blockers,
        "change_id": document.get("id"),
        "classification": document.get("classification"),
        "current_state": document.get("status"),
        "target_state": target_state,
        "required_gates": list(required_gates),
        "gate_reports": [report.as_dict() for report in gate_reports],
        "blockers": sorted(
            unique_blockers.values(), key=lambda item: (item["code"], item["id"])
        ),
        "human_approval": {
            "required": approval_required,
            "recorded": approval_recorded,
        },
        "decision_only": True,
        "lifecycle_mutated": False,
        "external_state": _external_state(document),
        "versions": {
            "report_schema": "1.0",
            "tool": TOOL_VERSION,
            "policy_set": {
                "id": snapshot.policy_set_id,
                "version": snapshot.policy_set_version,
            },
            "policies": dict(policy.policy_versions) if policy is not None else {},
        },
        "policy_sources": (
            [dict(item) for item in policy.policy_sources] if policy is not None else []
        ),
    }
    return TransitionReport(payload)


def _external_state(document: Mapping[str, Any]) -> dict[str, Any]:
    external = document.get("external_state")
    external = external if isinstance(external, dict) else {}
    return {
        "archived": document.get("status") == "archived",
        "delivered": external.get("delivered", "unknown"),
        "deployed": external.get("deployed", "unknown"),
        "tracker_done": external.get("tracker_done", "unknown"),
        "inferred": False,
    }


def _blocker(code: str, message: str) -> dict[str, str]:
    return {"code": code, "id": "transition", "message": message}
