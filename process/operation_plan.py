"""Deterministic operation planning from verified operation facts."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable


class OperationPlanError(ValueError):
    """Stable fail-closed operation-plan error."""


_POLICIES: dict[str, tuple[str, tuple[str, ...], str | None, dict[str, Any]]] = {
    "bounded-role-review": ("draft-content", ("bounded-draft",), "evidence-boundary-note", {}),
    "requirements-review": ("draft-content", ("bounded-draft",), "requirements-note", {}),
    "source-linked-analysis": ("draft-content", ("bounded-draft",), "evidence-boundary-note", {"canonical_mutation_requested": False}),
    "implementation-preparation": ("draft-content", ("bounded-draft",), "implementation-prep-note", {"canonical_mutation_requested": False}),
    "qa-review-draft": ("draft-content", ("bounded-draft",), "qa-review-note", {"qa_decision": "absent"}),
    "tech-lead-advisory-review": ("draft-content", ("bounded-draft",), "tech-lead-review-note", {"release_decision": "absent", "hold_state": "clear"}),
    "qa-evidence-review": ("blocked-summary", ("missing-context",), None, {"expected_behavior": "absent", "environment_evidence": "absent", "supplied_context": "absent"}),
    "release-readiness-review": ("blocked-summary", ("authority-required", "unsafe-resume"), None, {"human_release_decision": "absent", "corrective_evidence": "absent", "hold_state": "active"}),
    "implementation-evidence-review": ("blocked-summary", ("unsupported-evidence",), None, {"command_output": "absent", "committed_note": "absent", "ci_reference": "absent"}),
    "requirement-approval-request": ("blocked-summary", ("authority-required",), None, {"product_owner_decision": "absent"}),
    "test-evidence-review": ("blocked-summary", ("unsupported-evidence",), None, {"executable_output": "absent", "ci_reference": "absent", "manual_record": "absent"}),
    "hold-resume-review": ("blocked-summary", ("unsafe-resume", "authority-required"), None, {"hold_state": "active", "corrective_evidence": "absent", "authorized_human_decision": "absent"}),
    "retry-evidence-review": ("blocked-summary", ("failed-run-missing",), None, {"original_attempt_output": "absent", "replacement_requested": True}),
    "qa-sufficiency-review": ("blocked-summary", ("qa-evidence-insufficient", "authority-required"), None, {"command_output": "absent", "manual_qa_record": "absent", "qa_owner_decision": "absent"}),
    "hotfix-archive-readiness-review": ("blocked-summary", ("reconciliation-missing",), None, {"change_class": "hotfix", "reconciliation_record": "absent", "approved_disposition": "absent"}),
    "design-context-review": ("blocked-summary", ("missing-context",), None, {"system_map": "absent", "accepted_design": "absent", "supplied_context": "absent"}),
    "source-conflict-review": ("blocked-summary", ("conflicting-context",), None, {"canonical_disposition": "absent"}),
    "implementation-continuation-request": ("blocked-summary", ("human-stop-required",), None, {"required_human_review": "pending"}),
    "qa-gate-request": ("blocked-summary", ("authority-required",), None, {"qa_owner_decision": "absent", "deterministic_gate_record": "absent"}),
    "lifecycle-transition-request": ("blocked-summary", ("lifecycle-authority-required",), None, {"deterministic_gates": "incomplete", "authorized_human_decision": "absent"}),
}

_OWNER_CODES = {
    "analyst": "owner-analyst-or-change-owner",
    "developer": "owner-developer-or-change-owner",
    "qa": "owner-qa-or-test-owner",
    "tech_lead": "owner-tech-lead",
}


def _stable_unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def build_operation_plan(
    case: dict[str, Any], verified_source_ids: list[str]
) -> dict[str, Any]:
    """Evaluate one supported operation from facts without certification expectations."""
    operation = case.get("operation")
    policy = _POLICIES.get(operation)
    facts = case.get("facts")
    role = case.get("role")
    if (
        policy is None
        or not isinstance(facts, dict)
        or not facts
        or role not in _OWNER_CODES
        or not verified_source_ids
        or any(not isinstance(item, str) or not item for item in verified_source_ids)
    ):
        raise OperationPlanError("operation-plan.unsupported-input")
    action, reasons, artifact_kind, predicates = policy
    if any(facts.get(key) != expected for key, expected in predicates.items()):
        raise OperationPlanError("operation-plan.contradictory-input")
    if operation == "source-conflict-review":
        statements = facts.get("statements")
        if not isinstance(statements, list) or len(statements) < 2 or len({str(item.get("text")) for item in statements if isinstance(item, dict)}) < 2:
            raise OperationPlanError("operation-plan.contradictory-input")

    missing_inputs = (
        [str(key).replace("_", "-") for key, value in facts.items() if value is None or value == "absent"]
        if action == "blocked-summary"
        else []
    )
    if action == "blocked-summary" and not missing_inputs:
        missing_inputs = [f"reason-{reason}" for reason in reasons]
    human_actions = [_OWNER_CODES[role]]
    human_actions.extend(
        ["review-bounded-draft"]
        if action == "draft-content"
        else [f"resolve-{reason}" for reason in reasons]
    )
    facts_bytes = json.dumps(
        facts, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return {
        "action": action,
        "artifact_kind": artifact_kind,
        "reason_codes": list(reasons),
        "source_inventory": _stable_unique([*verified_source_ids, "case-facts"]),
        "case_facts_sha256": hashlib.sha256(facts_bytes).hexdigest(),
        "human_action_codes": human_actions,
        "unresolved_input_codes": missing_inputs,
    }
