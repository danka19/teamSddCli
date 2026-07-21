"""Pure class-aware artifact and business-gate evaluation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import Any, Mapping

from .gate_input import lifecycle_state_was_reached
from .policy_validation import EffectiveRule, PolicySnapshot


TOOL_VERSION = "0.3.4"

_SUPPORTED_CLASSES = ("minor", "major", "hotfix")
_SUPPORTED_STATES = (
    "draft", "spec_review", "approved", "in_implementation",
    "ready_to_archive", "archived",
)
_SUPPORTED_GATES = (
    "review-ready",
    "definition-of-ready",
    "implementation-complete",
    "definition-of-done",
    "release-transfer-readiness",
    "archive-readiness",
)
SUPPORTED_GATES = _SUPPORTED_GATES
class _PolicyContractError(ValueError):
    pass


@dataclass(frozen=True)
class CompiledGatePolicy:
    policy_set_id: str
    policy_set_version: str
    classes: tuple[str, ...]
    named_gates: tuple[str, ...]
    artifact_rules: Mapping[str, tuple[str, ...]]
    class_rule_ids: Mapping[str, tuple[str, ...]]
    reviewer_slots: Mapping[str, tuple[str, ...]]
    common_ready: tuple[str, ...]
    common_done: tuple[str, ...]
    release_ready: tuple[str, ...]
    archive_ready: tuple[str, ...]
    release_minimums: tuple[str, ...]
    report_rule_relationships: Mapping[str, tuple[str, ...]]
    rule_values: Mapping[str, tuple[str, ...]]
    conditional_not_applicable: tuple[str, ...]
    not_applicable_required_fields: tuple[str, ...]
    waiver_eligible: tuple[str, ...]
    waiver_required_fields: tuple[str, ...]
    hotfix_deferrable: tuple[str, ...]
    hotfix_deferral_required_fields: tuple[str, ...]
    placeholder_markers: tuple[str, ...]
    lifecycle_states: tuple[str, ...]
    forward_transitions: Mapping[str, tuple[str, ...]]
    transition_gates: Mapping[str, tuple[str, ...]]
    external_state_non_inference: tuple[str, ...]
    corporate_values: Mapping[str, Any]
    policy_sources: tuple[Mapping[str, str], ...]
    policy_versions: Mapping[str, str]


@dataclass(frozen=True)
class GateReport:
    payload: dict[str, Any]

    @property
    def exit_code(self) -> int:
        return 0 if self.payload["status"] == "ready" else 1

    def as_dict(self) -> dict[str, Any]:
        return self.payload

    def render_human(self) -> str:
        blockers = self.payload["blocking_gaps"]
        advisories = self.payload["advisory_gaps"]
        lines = [
            f"Gate: {self.payload['gate']}",
            f"Status: {self.payload['status']}",
            f"Classification: {self.payload['classification']}",
            "Blocking gaps:",
            *(f"- {item['id']}: {item['message']}" for item in blockers),
            "Advisory gaps:",
            *(f"- {item['id']}: {item['message']}" for item in advisories),
            "Required human approvals:",
            *(f"- {item}" for item in self.payload["human_approval"]["approvers"]),
        ]
        return "\n".join(lines)


def evaluate_gate(
    document: dict[str, Any], snapshot: PolicySnapshot, gate: str
) -> GateReport:
    """Evaluate one named gate without mutating canonical lifecycle state."""
    try:
        policy = compile_gate_policy(snapshot)
    except _PolicyContractError as error:
        return _invalid_policy_report(document, snapshot, gate, str(error))

    classification = document.get("classification")
    if gate not in _SUPPORTED_GATES:
        return _blocked_report(
            document,
            snapshot,
            gate,
            "gate.unknown-gate",
            "The requested gate is not supported by the compiled policy contract.",
        )
    if classification not in policy.classes:
        return _blocked_report(
            document,
            snapshot,
            gate,
            "gate.classification-invalid",
            "A confirmed minor, major, or hotfix classification is required.",
        )

    required = _required_obligations(policy, gate, classification, document)
    evidence_rows = document.get("evidence", [])
    evidence = {
        row.get("id"): row
        for row in evidence_rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    } if isinstance(evidence_rows, list) else {}

    gate_na = evidence.get(gate)
    release_not_applicable = (
        gate == "release-transfer-readiness"
        and isinstance(gate_na, dict)
        and gate_na.get("state") == "not_applicable"
        and _valid_not_applicable(gate_na, policy, classification)
    )
    if release_not_applicable:
        required = ()

    obligations: list[dict[str, Any]] = []
    blockers: list[dict[str, str]] = []
    for identifier in required:
        row = evidence.get(identifier)
        result, gap = _evaluate_obligation(
            identifier,
            row,
            policy=policy,
            classification=classification,
            gate=gate,
            evaluation_date=document.get("evaluation_date"),
            lifecycle_state=document.get("status"),
            lifecycle_history=document.get("lifecycle_history"),
        )
        obligations.append(result)
        if gap is not None:
            blockers.append(gap)

    if classification == "hotfix" and gate in {
        "definition-of-done", "archive-readiness"
    }:
        for row in evidence.values():
            deferral = row.get("deferral") if isinstance(row, dict) else None
            if (
                isinstance(deferral, dict)
                and row.get("state") == "deferred"
                and deferral.get("reconciled") is not True
            ):
                blockers.append(_gap(
                    "gate.hotfix-reconciliation-required",
                    str(row.get("id")),
                    "A hotfix deferral remains a mandatory reconciliation obligation.",
                ))

    advisory_gaps = _advisory_gaps(evidence_rows)
    approvers = _required_approvers(policy, classification)
    approvals = document.get("approvals", [])
    approved = _human_approvals_recorded(approvers, approvals)
    if blockers:
        status = "blocked"
    elif approvers and not approved:
        status = "awaiting_human_approval"
    else:
        status = "ready"

    payload = {
        "schema_version": "1.0",
        "status": status,
        "gate": gate,
        "change_id": document.get("id"),
        "classification": classification,
        "obligations": obligations,
        "blocking_gaps": sorted(blockers, key=lambda item: (item["code"], item["id"])),
        "advisory_gaps": advisory_gaps,
        "human_approval": {
            "required": bool(approvers),
            "approvers": list(approvers),
            "recorded": approved,
            "decision": "required" if approvers and not approved else "recorded",
        },
        "decision_only": True,
        "lifecycle_mutated": False,
        "external_state": _external_state(document),
        "versions": {
            "report_schema": "1.0",
            "tool": TOOL_VERSION,
            "policy_set": {
                "id": policy.policy_set_id,
                "version": policy.policy_set_version,
            },
            "policies": dict(policy.policy_versions),
        },
        "policy_sources": [dict(item) for item in policy.policy_sources],
    }
    return GateReport(payload)


def _required_obligations(
    policy: CompiledGatePolicy,
    gate: str,
    classification: str,
    document: dict[str, Any],
) -> tuple[str, ...]:
    class_keys = [classification]
    if classification == "hotfix" and document.get("major_impact_hotfix") is True:
        class_keys.append("major-impact-hotfix")

    class_artifacts: list[str] = []
    for key in class_keys:
        for rule_id in policy.class_rule_ids.get(key, ()):
            class_artifacts.extend(policy.artifact_rules[rule_id])

    values: list[str] = []
    for rule_id in policy.report_rule_relationships[gate]:
        if rule_id == "classification.obligation-rules":
            values.extend(class_artifacts)
        else:
            values.extend(policy.rule_values[rule_id])
    return tuple(dict.fromkeys(values))


def _evaluate_obligation(
    identifier: str,
    row: Any,
    *,
    policy: CompiledGatePolicy,
    classification: str,
    gate: str,
    evaluation_date: Any,
    lifecycle_state: Any,
    lifecycle_history: Any,
) -> tuple[dict[str, Any], dict[str, str] | None]:
    if not isinstance(row, dict):
        return (
            {"id": identifier, "state": "missing", "source_ref": None},
            _gap("gate.evidence-missing", identifier, "Required evidence is missing."),
        )

    state = row.get("state")
    base = {
        "id": identifier,
        "state": state if isinstance(state, str) else "invalid",
        "source_ref": row.get("source_ref"),
    }
    if row.get("fresh") is not True:
        return base, _gap(
            "gate.stale-evidence", identifier,
            "Required evidence is missing freshness confirmation or is stale.",
        )
    freshness_gap = _freshness_gap(row, evaluation_date)
    if freshness_gap is not None:
        return base, freshness_gap
    if not isinstance(row.get("source_ref"), str) or not row["source_ref"].strip():
        return base, _gap(
            "gate.source-missing", identifier,
            "Required evidence must be source-linked.",
        )
    if state == "not_applicable":
        if identifier not in policy.conditional_not_applicable:
            return base, _gap(
                "gate.not-applicable-ineligible", identifier,
                "This obligation is not conditionally applicable.",
            )
        if not _valid_not_applicable(row, policy, classification):
            return base, _gap(
                "gate.not-applicable-invalid", identifier,
                "Not-applicable evidence requires a rationale and human approval.",
            )
        return base, None

    if state == "waived":
        if identifier not in policy.waiver_eligible:
            return base, _gap(
                "gate.waiver-ineligible", identifier,
                "This corporate minimum cannot be waived.",
            )
        waiver = row.get("waiver")
        if not _valid_waiver(waiver, policy, classification):
            return base, _gap(
                "gate.waiver-invalid", identifier,
                "The waiver is missing current role-authorized evidence.",
            )
        expiry_due = _expiry_due(
            waiver.get("expiry"), evaluation_date, lifecycle_state,
            policy.lifecycle_states, lifecycle_history,
        )
        if expiry_due is None:
            return base, _gap(
                "gate.waiver-invalid", identifier,
                "The waiver expiry condition is malformed.",
            )
        if expiry_due:
            return base, _gap(
                "gate.waiver-expired", identifier,
                "The waiver is no longer valid at the evaluation date or lifecycle state.",
            )
        return base, None

    if state == "deferred":
        if classification != "hotfix" or identifier not in policy.hotfix_deferrable:
            return base, _gap(
                "gate.deferral-ineligible", identifier,
                "Only explicitly permitted non-safety hotfix evidence may be deferred.",
            )
        deferral = row.get("deferral")
        if not _valid_deferral(deferral, policy, classification):
            return base, _gap(
                "gate.deferral-invalid", identifier,
                "The hotfix deferral lacks owner, approval, risk, follow-up, or expiry.",
            )
        expiry_due = _expiry_due(
            deferral.get("expiry"), evaluation_date, lifecycle_state,
            policy.lifecycle_states, lifecycle_history,
        )
        if expiry_due is None:
            return base, _gap(
                "gate.deferral-invalid", identifier,
                "The hotfix deferral expiry condition is malformed.",
            )
        if deferral.get("reconciled") is not True and expiry_due:
            return base, _gap(
                "gate.deferral-due", identifier,
                "The hotfix deferral is due and has not been reconciled.",
            )
        if gate in {"definition-of-done", "archive-readiness"}:
            return base, _gap(
                "gate.hotfix-reconciliation-required", identifier,
                "Deferred hotfix evidence must be reconciled before closure.",
            )
        return base, None

    if state != "satisfied":
        return base, _gap(
            "gate.evidence-invalid", identifier,
            "Evidence has an unsupported state.",
        )
    if row.get("source_kind") == "ai-statement":
        return base, _gap(
            "gate.ai-statement-not-evidence", identifier,
            "An AI completion statement is advisory and is not implementation evidence.",
        )
    content = row.get("content")
    if (
        not isinstance(content, str)
        or len(content.strip()) < 8
        or _is_placeholder(content, policy.placeholder_markers)
    ):
        return base, _gap(
            "gate.placeholder-evidence", identifier,
            "Required evidence is empty, placeholder-only, or non-substantive.",
        )
    return base, None


def _valid_not_applicable(
    row: Mapping[str, Any], policy: CompiledGatePolicy, classification: str
) -> bool:
    return _required_record_fields(
        row,
        policy.not_applicable_required_fields,
        authorized_owners=_required_approvers(policy, classification),
        placeholder_markers=policy.placeholder_markers,
    )


def _valid_waiver(
    value: Any, policy: CompiledGatePolicy, classification: str
) -> bool:
    return (
        isinstance(value, dict)
        and _required_record_fields(
            value,
            policy.waiver_required_fields,
            authorized_owners=_required_approvers(policy, classification),
            placeholder_markers=policy.placeholder_markers,
        )
    )


def _valid_deferral(
    value: Any, policy: CompiledGatePolicy, classification: str
) -> bool:
    return isinstance(value, dict) and _required_record_fields(
        value,
        policy.hotfix_deferral_required_fields,
        allow_false=("reconciled",),
        authorized_owners=_required_approvers(policy, classification),
        placeholder_markers=policy.placeholder_markers,
    )


def _required_record_fields(
    value: Mapping[str, Any],
    fields: tuple[str, ...],
    *,
    allow_false: tuple[str, ...] = (),
    authorized_owners: tuple[str, ...] = (),
    placeholder_markers: tuple[str, ...] = (),
) -> bool:
    for field in fields:
        key = field.replace("-", "_")
        item = value.get(key)
        if field == "source-ref":
            item = value.get("source_ref")
        if field == "approver":
            if not (
                isinstance(item, dict)
                and item.get("type") == "human"
                and item.get("id") in authorized_owners
            ):
                return False
        elif field == "owner":
            if item not in authorized_owners:
                return False
        elif key in allow_false:
            if item not in (True, False):
                return False
        elif not item or (
            isinstance(item, str) and _is_placeholder(item, placeholder_markers)
        ):
            return False
    return True


def _expiry_due(
    value: Any,
    evaluation_date: Any,
    lifecycle_state: Any,
    lifecycle_states: tuple[str, ...],
    lifecycle_history: Any,
) -> bool | None:
    if not isinstance(value, dict) or value.get("type") not in {
        "date", "lifecycle_state"
    }:
        return None
    if value["type"] == "date":
        if set(value) != {"type", "date"}:
            return None
        try:
            evaluated = date.fromisoformat(evaluation_date)
            expires = date.fromisoformat(value["date"])
        except (TypeError, ValueError):
            return None
        return evaluated >= expires
    if set(value) != {"type", "lifecycle_state"}:
        return None
    due_state = value.get("lifecycle_state")
    return lifecycle_state_was_reached(
        lifecycle_state,
        lifecycle_history,
        evaluation_date,
        due_state,
        lifecycle_states,
    )


def _normalized_marker(value: str) -> str:
    normalized = re.sub(r"[^a-z]+", "-", value.strip().lower()).strip("-")
    return "ellipsis" if value.strip() == "..." else normalized


def _is_placeholder(value: str, markers: tuple[str, ...]) -> bool:
    normalized = _normalized_marker(value)
    return normalized in markers or any(
        normalized.startswith(f"{marker}-")
        for marker in markers
        if marker in {"todo", "tbd", "placeholder", "coming-soon", "not-needed"}
    )


def _freshness_gap(
    row: Mapping[str, Any], evaluation_date: Any
) -> dict[str, str] | None:
    valid_through = row.get("valid_through")
    if valid_through is None:
        return None
    try:
        evaluated = date.fromisoformat(evaluation_date)
        expires = date.fromisoformat(valid_through)
    except (TypeError, ValueError):
        return _gap(
            "gate.freshness-invalid",
            str(row.get("id")),
            "Freshness dates must use valid ISO calendar dates.",
        )
    if expires < evaluated:
        return _gap(
            "gate.stale-evidence",
            str(row.get("id")),
            "Evidence expired before the explicit evaluation date.",
        )
    return None


def _advisory_gaps(rows: Any) -> list[dict[str, str]]:
    if not isinstance(rows, list):
        return []
    return sorted([
        _gap(
            "gate.advisory-gap",
            str(row.get("id")),
            str(row.get("message") or "Advisory evidence gap."),
        )
        for row in rows
        if isinstance(row, dict) and row.get("state") == "advisory"
    ], key=lambda item: item["id"])


def _required_approvers(
    policy: CompiledGatePolicy, classification: str
) -> tuple[str, ...]:
    values: list[str] = []
    for slot in policy.reviewer_slots[classification]:
        value = policy.corporate_values.get(slot)
        if isinstance(value, str) and value:
            values.append(value)
    return tuple(dict.fromkeys(sorted(values)))


def _human_approvals_recorded(approvers: tuple[str, ...], rows: Any) -> bool:
    if not approvers:
        return True
    if not isinstance(rows, list):
        return False
    approved = {
        row.get("owner_id")
        for row in rows
        if isinstance(row, dict)
        and row.get("owner_type") == "human"
        and row.get("state") == "approved"
        and row.get("evidence_ref")
    }
    return set(approvers) <= approved


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


def compile_gate_policy(snapshot: PolicySnapshot) -> CompiledGatePolicy:
    if not isinstance(snapshot.policy_set_id, str) or not snapshot.policy_set_id:
        raise _PolicyContractError("The policy-set id is missing.")
    if not isinstance(snapshot.policy_set_version, str) or not re.fullmatch(
        r"\d+\.\d+\.\d+", snapshot.policy_set_version
    ):
        raise _PolicyContractError("The policy-set version is invalid.")

    classes = _string_tuple(snapshot, "classification.allowed-classes", "classification")
    if classes != _SUPPORTED_CLASSES:
        raise _PolicyContractError("The supported classification set changed.")
    class_rule_ids = _string_tuple_mapping(
        snapshot, "classification.obligation-rules", "classification"
    )
    reviewer_slots = _string_tuple_mapping(
        snapshot, "classification.reviewer-slots", "classification"
    )
    if not set(_SUPPORTED_CLASSES) <= set(class_rule_ids) or not set(
        _SUPPORTED_CLASSES
    ) <= set(reviewer_slots):
        raise _PolicyContractError("Class obligation or reviewer mappings are incomplete.")

    artifact_rule_ids = tuple(dict.fromkeys(
        rule_id for ids in class_rule_ids.values() for rule_id in ids
    ))
    artifact_rules = MappingProxyType({
        rule_id: _string_tuple(
            snapshot,
            rule_id,
            "artifact-matrix",
            allow_empty=rule_id == "artifacts.additional-required-artifacts",
        )
        for rule_id in artifact_rule_ids
    })
    named = _string_tuple(snapshot, "gates.named-catalog", "gates")
    if not set(_SUPPORTED_GATES) <= set(named):
        raise _PolicyContractError("The named gate catalog is incomplete.")
    common_ready = _string_tuple(
        snapshot, "gates.common-definition-of-ready", "gates"
    )
    common_done = _string_tuple(snapshot, "gates.definition-of-done", "gates")
    release_ready = _string_tuple(
        snapshot, "gates.release-transfer-readiness", "gates"
    )
    archive_ready = _string_tuple(snapshot, "gates.archive-readiness", "gates")
    release_minimums = _string_tuple(
        snapshot, "release.package-minimums", "release"
    )
    conditional_not_applicable = _string_tuple(
        snapshot, "artifacts.conditional-not-applicable", "artifact-matrix"
    )
    not_applicable_required_fields = _string_tuple(
        snapshot, "artifacts.not-applicable-required-fields", "artifact-matrix"
    )
    waiver_eligible = _string_tuple(
        snapshot, "artifacts.waiver-eligible", "artifact-matrix"
    )
    waiver_required_fields = _string_tuple(
        snapshot, "artifacts.waiver-required-fields", "artifact-matrix"
    )
    hotfix_deferrable = _string_tuple(
        snapshot, "artifacts.hotfix-deferrable", "artifact-matrix"
    )
    hotfix_deferral_required_fields = _string_tuple(
        snapshot, "artifacts.hotfix-deferral-required-fields", "artifact-matrix"
    )
    placeholder_markers = _string_tuple(
        snapshot, "artifacts.placeholder-markers", "artifact-matrix"
    )
    review_ready = _string_tuple(snapshot, "gates.review-ready", "gates")
    implementation_complete = _string_tuple(
        snapshot, "gates.implementation-complete", "gates"
    )
    report_rule_relationships = _string_tuple_mapping(
        snapshot, "gates.report-rule-relationships", "gates"
    )
    expected_report_rules = {
        "gates.review-ready": review_ready,
        "gates.common-definition-of-ready": common_ready,
        "gates.implementation-complete": implementation_complete,
        "gates.definition-of-done": common_done,
        "gates.release-transfer-readiness": release_ready,
        "gates.archive-readiness": archive_ready,
        "release.package-minimums": release_minimums,
    }
    if set(report_rule_relationships) != set(_SUPPORTED_GATES):
        raise _PolicyContractError("Gate report relationships are incomplete.")
    if any(
        rule_id not in expected_report_rules
        and rule_id != "classification.obligation-rules"
        for rule_ids in report_rule_relationships.values()
        for rule_id in rule_ids
    ):
        raise _PolicyContractError("A gate report relationship references an invalid rule.")

    all_artifacts = {
        artifact for values in artifact_rules.values() for artifact in values
    }
    if not set(conditional_not_applicable) <= all_artifacts | {
        "release-transfer-evidence-when-applicable"
    }:
        raise _PolicyContractError("Conditional applicability references an unknown artifact.")
    if not set(waiver_eligible) <= all_artifacts:
        raise _PolicyContractError("Waiver eligibility references an unknown artifact.")
    if not set(hotfix_deferrable) <= set(artifact_rules["artifacts.major-required"]):
        raise _PolicyContractError("Hotfix deferral permits a non-major or safety artifact.")

    lifecycle_states = _string_tuple(snapshot, "release.lifecycle-states", "release")
    if lifecycle_states != _SUPPORTED_STATES:
        raise _PolicyContractError("The accepted six lifecycle states changed.")
    forward_transitions = _string_tuple_mapping(
        snapshot, "release.forward-transitions", "release"
    )
    expected_forward = {
        "draft": ("spec_review",),
        "spec_review": ("draft", "approved"),
        "approved": ("in_implementation",),
        "in_implementation": ("ready_to_archive",),
        "ready_to_archive": ("in_implementation", "archived"),
        "archived": (),
    }
    if dict(forward_transitions) != expected_forward:
        raise _PolicyContractError("Lifecycle transitions do not match the canonical flow.")
    transition_gates = _string_tuple_mapping(
        snapshot, "release.transition-gates", "release"
    )
    expected_transition_ids = {
        f"{state}->{target}"
        for state, targets in forward_transitions.items()
        for target in targets
    }
    if set(transition_gates) != expected_transition_ids or any(
        gate_id not in named
        for gate_ids in transition_gates.values()
        for gate_id in gate_ids
    ):
        raise _PolicyContractError("Lifecycle transition gate relationships are invalid.")
    external_state_non_inference = _string_tuple(
        snapshot, "release.external-state-non-inference", "release"
    )
    if external_state_non_inference != ("delivered", "deployed", "tracker-done"):
        raise _PolicyContractError("External delivery states must remain non-inferred.")
    distinct = _string_tuple(snapshot, "release.distinct-states", "release")
    if distinct != (
        "implementation-complete", "definition-of-done", "release-ready",
        "archive-ready", "archived", "delivered",
    ):
        raise _PolicyContractError("Release, archive, and delivered states are not distinct.")
    _boolean(snapshot, "gates.human-approval-required", "gates", True)
    _boolean(snapshot, "release.final-archive-human-approval", "release", True)
    _boolean(snapshot, "release.hotfix-reconciliation", "release", True)

    required_ids = tuple(dict.fromkeys((
        "classification.allowed-classes",
        "classification.obligation-rules",
        "classification.reviewer-slots",
        *artifact_rule_ids,
        "artifacts.conditional-not-applicable",
        "artifacts.not-applicable-required-fields",
        "artifacts.waiver-eligible",
        "artifacts.waiver-required-fields",
        "artifacts.hotfix-deferrable",
        "artifacts.hotfix-deferral-required-fields",
        "artifacts.placeholder-markers",
        "gates.named-catalog",
        "gates.review-ready",
        "gates.common-definition-of-ready",
        "gates.implementation-complete",
        "gates.definition-of-done",
        "gates.release-transfer-readiness",
        "gates.archive-readiness",
        "gates.human-approval-required",
        "gates.report-rule-relationships",
        "release.package-minimums",
        "release.lifecycle-states",
        "release.forward-transitions",
        "release.transition-gates",
        "release.external-state-non-inference",
        "release.distinct-states",
        "release.final-archive-human-approval",
        "release.hotfix-reconciliation",
    )))
    sources = tuple(MappingProxyType({
        "rule_id": identifier,
        "policy_id": snapshot.rules[identifier].policy_id,
        "policy_version": snapshot.rules[identifier].policy_version,
        "source": snapshot.rules[identifier].source,
        "pointer": snapshot.rules[identifier].pointer,
    }) for identifier in sorted(required_ids))
    versions: dict[str, str] = {}
    for source in sources:
        existing = versions.get(source["policy_id"])
        if existing is not None and existing != source["policy_version"]:
            raise _PolicyContractError("A required policy has conflicting versions.")
        versions[source["policy_id"]] = source["policy_version"]

    policy = CompiledGatePolicy(
        policy_set_id=snapshot.policy_set_id,
        policy_set_version=snapshot.policy_set_version,
        classes=classes,
        named_gates=named,
        artifact_rules=artifact_rules,
        class_rule_ids=class_rule_ids,
        reviewer_slots=reviewer_slots,
        common_ready=common_ready,
        common_done=common_done,
        release_ready=release_ready,
        archive_ready=archive_ready,
        release_minimums=release_minimums,
        report_rule_relationships=report_rule_relationships,
        rule_values=MappingProxyType(expected_report_rules),
        conditional_not_applicable=conditional_not_applicable,
        not_applicable_required_fields=not_applicable_required_fields,
        waiver_eligible=waiver_eligible,
        waiver_required_fields=waiver_required_fields,
        hotfix_deferrable=hotfix_deferrable,
        hotfix_deferral_required_fields=hotfix_deferral_required_fields,
        placeholder_markers=placeholder_markers,
        lifecycle_states=lifecycle_states,
        forward_transitions=forward_transitions,
        transition_gates=transition_gates,
        external_state_non_inference=external_state_non_inference,
        corporate_values=snapshot.corporate_values,
        policy_sources=sources,
        policy_versions=MappingProxyType(dict(sorted(versions.items()))),
    )
    return policy


def _rule(
    snapshot: PolicySnapshot, identifier: str, policy_id: str
) -> EffectiveRule:
    rule = snapshot.rules.get(identifier)
    if (
        rule is None
        or rule.policy_id != policy_id
        or not isinstance(rule.policy_version, str)
        or not re.fullmatch(r"\d+\.\d+\.\d+", rule.policy_version)
    ):
        raise _PolicyContractError(
            f"Required rule {identifier} is missing or has invalid provenance."
        )
    return rule


def _string_tuple(
    snapshot: PolicySnapshot,
    identifier: str,
    policy_id: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    value = _rule(snapshot, identifier, policy_id).value
    if (
        not isinstance(value, tuple)
        or (not value and not allow_empty)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise _PolicyContractError(f"Required rule {identifier} is malformed.")
    return value


def _string_tuple_mapping(
    snapshot: PolicySnapshot, identifier: str, policy_id: str
) -> Mapping[str, tuple[str, ...]]:
    value = _rule(snapshot, identifier, policy_id).value
    if not isinstance(value, Mapping):
        raise _PolicyContractError(f"Required rule {identifier} is malformed.")
    normalized: dict[str, tuple[str, ...]] = {}
    for key, items in value.items():
        if (
            not isinstance(key, str)
            or not isinstance(items, tuple)
            or any(not isinstance(item, str) or not item for item in items)
            or len(set(items)) != len(items)
        ):
            raise _PolicyContractError(f"Required rule {identifier} is malformed.")
        normalized[key] = items
    return MappingProxyType(normalized)


def _boolean(
    snapshot: PolicySnapshot, identifier: str, policy_id: str, expected: bool
) -> bool:
    value = _rule(snapshot, identifier, policy_id).value
    if value is not expected:
        raise _PolicyContractError(f"Required rule {identifier} changed.")
    return value


def _gap(code: str, identifier: str, message: str) -> dict[str, str]:
    return {"code": code, "id": identifier, "message": message}


def _invalid_policy_report(
    document: Mapping[str, Any], snapshot: PolicySnapshot, gate: str, message: str
) -> GateReport:
    return _blocked_report(
        document, snapshot, gate, "gate.policy-contract-invalid", message
    )


def _blocked_report(
    document: Mapping[str, Any],
    snapshot: PolicySnapshot,
    gate: str,
    code: str,
    message: str,
) -> GateReport:
    return GateReport({
        "schema_version": "1.0",
        "status": "blocked",
        "gate": gate,
        "change_id": document.get("id"),
        "classification": document.get("classification"),
        "obligations": [],
        "blocking_gaps": [_gap(code, "policy", message)],
        "advisory_gaps": [],
        "human_approval": {
            "required": True,
            "approvers": [],
            "recorded": False,
            "decision": "blocked",
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
            "policies": {},
        },
        "policy_sources": [],
    })
