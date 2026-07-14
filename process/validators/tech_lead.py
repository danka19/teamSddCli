"""Deterministic, non-mutating Tech Lead review and control-state checks."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .config_discovery import load_schema_resources
from .config_validation import Diagnostic, schema_diagnostics
from .owners import AffectedPath, TechLeadResolution, resolve_tech_lead_ownership
from .policy_validation import PolicySnapshot


TECH_LEAD_VIEWS = (
    "under-classification",
    "missing-canonical-context",
    "architecture-disposition",
    "owner-dependency",
    "scope-drift",
    "control-state",
    "completion-dod",
    "release-recommendation",
    "waiver-expiry",
    "hotfix-follow-up",
    "checkpoint-summary",
)
ALLOWED_ACTIONS = ("stop", "hold", "escalate", "resume")
FORBIDDEN_AUTHORITIES = (
    "qa-approval", "product-approval", "security-approval", "release-approval",
    "merge-approval", "archive-approval", "tracker-approval",
)
INDEPENDENT_APPROVALS = (
    "qa", "product", "security", "release", "merge", "archive", "tracker",
)
FINDING_FIELDS = (
    "code", "severity", "blocking", "source_ref", "zone", "role", "action",
    "policy_snapshot",
)


class TechLeadPolicyError(ValueError):
    pass


@dataclass(frozen=True)
class CompiledTechLeadPolicy:
    policy_set: tuple[str, str]
    snapshot_digest: str
    views: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    forbidden_authorities: tuple[str, ...]
    independent_approvals: tuple[str, ...]
    finding_fields: tuple[str, ...]
    checkpoints: tuple[Mapping[str, str], ...]
    checkpoint_owner: str
    stop_triggers: tuple[str, ...]
    policy_sources: tuple[Mapping[str, str], ...]


@dataclass(frozen=True)
class TechLeadReport:
    payload: Mapping[str, Any]

    @property
    def exit_code(self) -> int:
        return 1 if self.payload["status"] == "blocked" else 0

    def as_dict(self) -> dict[str, Any]:
        return _thaw(self.payload)

    def render_human(self) -> str:
        return "\n".join((
            f"Tech Lead review: {self.payload['status']}",
            f"Change: {self.payload.get('change_id')}",
            f"Findings: {len(self.payload['findings'])}",
            f"Release recommendation: {self.payload['release_recommendation']}",
            "Decision only: true",
        ))


@dataclass(frozen=True)
class ControlState:
    state: str
    resume_eligible: bool
    active_record_ids: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    as_of: str | None = None
    as_of_cutoff: str | None = None
    evaluation_date: str | None = None
    snapshot_digest: str | None = None
    decision_only: bool = True
    control_state_mutated: bool = False
    lifecycle_mutated: bool = False

    @property
    def exit_code(self) -> int:
        return 1 if self.state in {"stopped", "held", "escalated", "invalid"} else 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "status": "blocked" if self.exit_code else "reviewable",
            "state": self.state,
            "resume_eligible": self.resume_eligible,
            "active_record_ids": list(self.active_record_ids),
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "as_of": self.as_of,
            "as_of_cutoff": self.as_of_cutoff,
            "evaluation_date": self.evaluation_date,
            "snapshot_digest": self.snapshot_digest,
            "decision_only": self.decision_only,
            "control_state_mutated": self.control_state_mutated,
            "lifecycle_mutated": self.lifecycle_mutated,
        }


def policy_snapshot_digest(snapshot: PolicySnapshot) -> str:
    payload = {
        "id": snapshot.policy_set_id,
        "version": snapshot.policy_set_version,
        "corporate_values": _thaw(snapshot.corporate_values),
        "rules": {
            identifier: {
                "value": _thaw(rule.value),
                "source": rule.source,
                "policy_id": rule.policy_id,
                "policy_version": rule.policy_version,
                "pointer": rule.pointer,
            }
            for identifier, rule in sorted(snapshot.rules.items())
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def compile_tech_lead_policy(snapshot: PolicySnapshot) -> CompiledTechLeadPolicy:
    expected = {
        "tech-lead.views": TECH_LEAD_VIEWS,
        "tech-lead.control-actions": ALLOWED_ACTIONS,
        "tech-lead.forbidden-authorities": FORBIDDEN_AUTHORITIES,
        "tech-lead.independent-approvals": INDEPENDENT_APPROVALS,
    }
    sources: list[Mapping[str, str]] = []
    for identifier, value in expected.items():
        rule = snapshot.rules.get(identifier)
        if rule is None or rule.policy_id != "tech-lead" or tuple(rule.value) != value:
            raise TechLeadPolicyError(f"Required immutable rule {identifier} is missing or changed.")
        sources.append(MappingProxyType({
            "rule": identifier,
            "policy_id": rule.policy_id,
            "policy_version": rule.policy_version,
            "source": rule.source,
            "pointer": rule.pointer,
        }))
    finding_rule = snapshot.rules.get("tech-lead.finding-fields")
    finding_fields = tuple(
        str(item).replace("-", "_")
        for item in (
            finding_rule.value
            if finding_rule is not None and isinstance(finding_rule.value, tuple)
            else ()
        )
    )
    if (
        finding_rule is None
        or finding_rule.policy_id != "tech-lead"
        or finding_fields != FINDING_FIELDS
    ):
        raise TechLeadPolicyError(
            "Required immutable rule tech-lead.finding-fields is missing or changed."
        )
    sources.append(MappingProxyType({
        "rule": "tech-lead.finding-fields",
        "policy_id": finding_rule.policy_id,
        "policy_version": finding_rule.policy_version,
        "source": finding_rule.source,
        "pointer": finding_rule.pointer,
    }))
    checkpoint_rule = snapshot.rules.get("tech-lead.checkpoints")
    checkpoints: list[Mapping[str, str]] = []
    if (
        checkpoint_rule is not None
        and checkpoint_rule.policy_id == "tech-lead"
        and isinstance(checkpoint_rule.value, tuple)
    ):
        for item in checkpoint_rule.value:
            if not isinstance(item, Mapping):
                checkpoints = []
                break
            normalized = {
                "event": item.get("event"),
                "kind": item.get("kind"),
                "source_ref": item.get("source-ref"),
            }
            if (
                set(item) != {"event", "kind", "source-ref"}
                or not all(
                    isinstance(value, str) and bool(value)
                    for value in normalized.values()
                )
                or normalized["kind"] not in {"scheduled", "event-driven"}
            ):
                checkpoints = []
                break
            checkpoints.append(MappingProxyType(normalized))
    if not checkpoints or len({item["event"] for item in checkpoints}) != len(checkpoints):
        raise TechLeadPolicyError(
            "Required immutable rule tech-lead.checkpoints is missing or changed."
        )
    checkpoint_owner = snapshot.corporate_values.get("tech_lead_owner")
    if not isinstance(checkpoint_owner, str) or not checkpoint_owner:
        raise TechLeadPolicyError("Configured Tech Lead checkpoint owner is missing.")
    sources.append(MappingProxyType({
        "rule": "tech-lead.checkpoints",
        "policy_id": checkpoint_rule.policy_id,
        "policy_version": checkpoint_rule.policy_version,
        "source": checkpoint_rule.source,
        "pointer": checkpoint_rule.pointer,
    }))
    for identifier in ("tech-lead.decision-only", "tech-lead.human-control-required"):
        rule = snapshot.rules.get(identifier)
        if rule is None or rule.policy_id != "tech-lead" or rule.value is not True:
            raise TechLeadPolicyError(f"Required immutable rule {identifier} is missing or changed.")
    stop_rule = snapshot.rules.get("flow.production-stop-triggers")
    additional_rule = snapshot.rules.get("flow.additional-stop-triggers")
    if stop_rule is None or stop_rule.policy_id != "flow-controls":
        raise TechLeadPolicyError("Canonical stop triggers are missing or changed.")
    stop_triggers = tuple(stop_rule.value) + (
        tuple(additional_rule.value) if additional_rule is not None else ()
    )
    return CompiledTechLeadPolicy(
        policy_set=(snapshot.policy_set_id, snapshot.policy_set_version),
        snapshot_digest=policy_snapshot_digest(snapshot),
        views=TECH_LEAD_VIEWS,
        allowed_actions=ALLOWED_ACTIONS,
        forbidden_authorities=FORBIDDEN_AUTHORITIES,
        independent_approvals=INDEPENDENT_APPROVALS,
        finding_fields=finding_fields,
        checkpoints=tuple(checkpoints),
        checkpoint_owner=checkpoint_owner,
        stop_triggers=stop_triggers,
        policy_sources=tuple(sources),
    )


def validate_tech_lead_input(document: Any, process_root: Any) -> list[dict[str, str]]:
    resources = load_schema_resources(process_root / "schemas")
    diagnostics = schema_diagnostics(
        "tech-lead-review-input.schema.json",
        document,
        "tech-lead-review-input",
        stage=4,
        schema_resources=resources,
    )
    return [{
        "code": "tech-lead.input-schema-invalid",
        "pointer": item.pointer or "/",
        "message": "Tech Lead input does not satisfy the pinned schema.",
    } for item in diagnostics]


def validate_owner_registry_input(document: Any, process_root: Any) -> list[dict[str, str]]:
    resources = load_schema_resources(process_root / "schemas")
    diagnostics = schema_diagnostics(
        "owners.schema.json",
        document,
        "owners-registry",
        stage=8,
        schema_resources=resources,
    )
    return [{
        "code": "owners.schema-invalid",
        "pointer": item.pointer or "/",
        "message": "Owner registry does not satisfy the pinned schema.",
    } for item in diagnostics]


def validate_evaluation_cutoff(as_of: Any) -> list[dict[str, str]]:
    try:
        date.fromisoformat(as_of)
    except (TypeError, ValueError):
        return [{"code": "tech-lead.as-of-invalid"}]
    return []


def check_control_state(
    records: Sequence[Mapping[str, Any]],
    owners: Mapping[str, Any],
    projects: Mapping[str, Any],
    snapshot: PolicySnapshot,
    *,
    as_of: str | None = None,
    evaluation_date: str | None = None,
) -> ControlState:
    cutoff: datetime | None = None
    cutoff_text: str | None = None
    if as_of is not None:
        try:
            cutoff = _date_cutoff(as_of)
            cutoff_text = _format_utc(cutoff)
        except (TypeError, ValueError):
            return ControlState(
                state="invalid", resume_eligible=False, active_record_ids=(),
                diagnostics=(_diag(
                    "tech-lead.as-of-invalid",
                    "The evaluation cutoff must be an ISO calendar date.",
                ),),
                as_of=as_of, evaluation_date=evaluation_date,
            )
    try:
        policy = compile_tech_lead_policy(snapshot)
    except TechLeadPolicyError as error:
        return ControlState(
            state="invalid", resume_eligible=False, active_record_ids=(),
            diagnostics=(_diag("tech-lead.policy-contract-invalid", str(error)),),
            as_of=as_of, evaluation_date=evaluation_date,
            as_of_cutoff=cutoff_text,
            snapshot_digest=policy_snapshot_digest(snapshot),
        )
    diagnostics: list[Diagnostic] = []
    if as_of is not None:
        if evaluation_date is not None and evaluation_date != as_of:
            return ControlState(
                state="invalid", resume_eligible=False, active_record_ids=(),
                diagnostics=(_diag(
                    "tech-lead.evaluation-date-mismatch",
                    "The input evaluation date does not match the requested cutoff.",
                ),),
                as_of=as_of, evaluation_date=evaluation_date,
                as_of_cutoff=cutoff_text,
                snapshot_digest=policy.snapshot_digest,
            )
    current_records: list[Mapping[str, Any]] = []
    record_instants: list[datetime] = []
    for record in records:
        instant = _parse_rfc3339(record.get("recorded_at"))
        if instant is None:
            diagnostics.append(_diag(
                "tech-lead.control-recorded-at-invalid",
                "A control record timestamp must be an RFC3339 timezone-aware instant.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if cutoff is not None and instant > cutoff:
            diagnostics.append(_diag(
                "tech-lead.control-record-future",
                "A future control record was excluded before state derivation.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        current_records.append(record)
        record_instants.append(instant)
    ids = [json.dumps(row.get("id"), sort_keys=True, default=str) for row in current_records]
    if len(ids) != len(set(ids)):
        diagnostics.append(_diag(
            "tech-lead.control-id-duplicate",
            "Control record identifiers must be unique.",
        ))
    if record_instants != sorted(record_instants):
        diagnostics.append(_diag(
            "tech-lead.control-order-invalid",
            "Control records must be supplied in source chronological order.",
        ))
    if len(record_instants) != len(set(record_instants)):
        diagnostics.append(_diag(
            "tech-lead.control-time-tie",
            "Control records must have distinct UTC instants so source order is unambiguous.",
        ))
    if any(item.code in {
        "tech-lead.control-id-duplicate", "tech-lead.control-order-invalid",
        "tech-lead.control-time-tie",
    } for item in diagnostics):
        return ControlState(
            state="invalid", resume_eligible=False, active_record_ids=(),
            diagnostics=tuple(diagnostics),
            as_of=as_of, evaluation_date=evaluation_date,
            as_of_cutoff=cutoff_text,
            snapshot_digest=policy.snapshot_digest,
        )
    active: list[Mapping[str, Any]] = []
    state = "clear"
    eligible = False
    for record in current_records:
        action = record.get("action")
        if action not in policy.allowed_actions:
            diagnostics.append(_diag(
                "tech-lead.control-action-unknown",
                "The control action is not part of the immutable contract.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if record.get("severity") not in {"low", "medium", "high", "critical"}:
            diagnostics.append(_diag(
                "tech-lead.control-severity-unknown",
                "The control severity is not part of the immutable contract.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if record.get("trigger") not in policy.stop_triggers:
            diagnostics.append(_diag(
                "tech-lead.control-trigger-unknown",
                "The control trigger is absent from the immutable policy snapshot.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if not _snapshot_matches(record.get("policy_snapshot"), policy):
            diagnostics.append(_diag(
                "tech-lead.policy-snapshot-mismatch",
                "A control record was evaluated against a different policy snapshot.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        actor = record.get("accountable_actor", {})
        if actor.get("type") != "human":
            diagnostics.append(_diag(
                "tech-lead.control-ai-authority-forbidden",
                "AI output cannot create an accountable control decision.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        affected = _affected_from_record(record)
        resolution = resolve_tech_lead_ownership(owners, projects, affected, snapshot)
        if resolution.diagnostics:
            diagnostics.extend(resolution.diagnostics)
            continue
        required_authority = "resume" if action == "resume" else "stop-hold"
        if not _actor_authorized(str(actor.get("id", "")), required_authority, resolution):
            diagnostics.append(_diag(
                "tech-lead.control-authority-forbidden",
                "The accountable human lacks authority for this control action.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if record.get("escalation_route") != resolution.escalation_route:
            diagnostics.append(_diag(
                "tech-lead.control-escalation-conflict",
                "The control record escalation route conflicts with owner governance.",
                source=str(record.get("source_ref", "control-record")),
            ))
            continue
        if action in {"stop", "hold", "escalate"}:
            active.append(record)
            state = {"stop": "stopped", "hold": "held", "escalate": "escalated"}[action]
            eligible = False
        elif action == "resume":
            if not active:
                diagnostics.append(_diag(
                    "tech-lead.resume-without-active-control",
                    "A resume record must reference an earlier active stop, hold, or escalation.",
                    source=str(record.get("source_ref", "control-record")),
                ))
                state = "invalid"
                eligible = False
                continue
            approvals = record.get("approvals", [])
            if any(row.get("type") != "human" for row in approvals if isinstance(row, Mapping)):
                diagnostics.append(_diag(
                    "tech-lead.control-ai-approval-forbidden",
                    "AI output cannot satisfy a required human resume approval.",
                    source=str(record.get("source_ref", "control-record")),
                ))
                continue
            active_ids = {str(row.get("id")) for row in active}
            target_ids = {
                value for value in record.get("target_active_record_ids", [])
                if isinstance(value, str)
            }
            unknown_targets = target_ids - active_ids
            if unknown_targets:
                diagnostics.append(_diag(
                    "tech-lead.resume-target-inactive",
                    "A resume target is not an active control record.",
                    source=str(record.get("source_ref", "control-record")),
                ))
            unaddressed = active_ids - target_ids
            if unaddressed:
                diagnostics.append(_diag(
                    "tech-lead.resume-active-records-unaddressed",
                    "Every active control record must be explicitly addressed before resume is eligible.",
                    source=str(record.get("source_ref", "control-record")),
                ))
            condition_sources: dict[str, set[str]] = {}
            for row in record.get("condition_evidence", []):
                if not isinstance(row, Mapping) or not isinstance(row.get("condition"), str):
                    continue
                condition_sources.setdefault(row["condition"], set()).update(
                    source for source in row.get("source_evidence", [])
                    if isinstance(source, str) and source
                )
            corrective = {
                source for source in record.get("corrective_evidence", [])
                if isinstance(source, str) and source
            }
            required_conditions = {
                condition
                for active_record in active
                if str(active_record.get("id")) in target_ids
                for condition in active_record.get("resume_conditions", [])
                if isinstance(condition, str)
            }
            evidence_complete = all(
                condition_sources.get(condition)
                and condition_sources[condition] <= corrective
                for condition in required_conditions
            )
            if not evidence_complete:
                diagnostics.append(_diag(
                    "tech-lead.resume-condition-evidence-incomplete",
                    "Every resume condition must be bound to corrective source evidence.",
                    source=str(record.get("source_ref", "control-record")),
                ))
            eligible = (
                bool(corrective) and bool(approvals) and bool(target_ids)
                and not unknown_targets and not unaddressed and evidence_complete
            )
            if eligible:
                state = "resume-eligible"
            else:
                if not corrective or not approvals:
                    diagnostics.append(_diag(
                        "tech-lead.resume-evidence-incomplete",
                        "Resume remains ineligible until corrective evidence and human approvals exist.",
                        source=str(record.get("source_ref", "control-record")),
                    ))
                state = _active_control_state(active)
            # Check-only: active records deliberately remain active until work item 2.7.
    if state == "clear" and diagnostics:
        state = "invalid"
    return ControlState(
        state=state,
        resume_eligible=eligible,
        active_record_ids=tuple(str(row.get("id")) for row in active),
        diagnostics=tuple(diagnostics),
        as_of=as_of,
        as_of_cutoff=cutoff_text,
        evaluation_date=evaluation_date or as_of,
        snapshot_digest=policy.snapshot_digest,
    )


def evaluate_tech_lead_review(
    document: Mapping[str, Any],
    owners: Mapping[str, Any],
    projects: Mapping[str, Any],
    snapshot: PolicySnapshot,
    *,
    as_of: str,
) -> TechLeadReport:
    try:
        policy = compile_tech_lead_policy(snapshot)
    except TechLeadPolicyError as error:
        return _report(document, None, [_finding(
            "tech-lead.policy-contract-invalid", True, "policy-manifest", "global",
            "tech_lead", "Restore the immutable Tech Lead policy.",
            {"id": snapshot.policy_set_id, "version": snapshot.policy_set_version,
             "digest": policy_snapshot_digest(snapshot)},
        )], {}, as_of=as_of)
    policy_ref = {"id": policy.policy_set[0], "version": policy.policy_set[1], "digest": policy.snapshot_digest}
    views: dict[str, list[dict[str, Any]]] = {name: [] for name in TECH_LEAD_VIEWS}

    try:
        today = date.fromisoformat(as_of)
    except (TypeError, ValueError):
        today = date.min
        views["missing-canonical-context"].append(_finding(
            "tech-lead.as-of-invalid", True, "as-of", "global", "tech_lead",
            "Supply an ISO calendar date evaluation cutoff.", policy_ref,
        ))
    if document.get("evaluation_date") != as_of:
        views["missing-canonical-context"].append(_finding(
            "tech-lead.evaluation-date-mismatch", True, "evaluation_date", "global",
            "tech_lead", "Regenerate the review input for the requested evaluation cutoff.",
            policy_ref,
        ))

    for source_name in ("policy_snapshot", "classification_report", "gate_reports"):
        candidate = document.get(source_name)
        if source_name != "policy_snapshot" and isinstance(candidate, Mapping):
            candidate = candidate.get("policy_snapshot")
        if not _snapshot_matches(candidate, policy):
            views["missing-canonical-context"].append(_finding(
                "tech-lead.policy-snapshot-mismatch", True, str(source_name), "global",
                "tech_lead", "Regenerate the source report from the same policy snapshot.", policy_ref,
            ))
    if document.get("classification") == "minor" and document.get("classification_report", {}).get("triggered_major") is True:
        views["under-classification"].append(_finding(
            "tech-lead.under-classification", True, "reports/classification.json", "global",
            "tech_lead", "Reject minor and recalculate or select the stricter route.", policy_ref,
        ))
    classification_report = document.get("classification_report", {})
    classification_status = classification_report.get("status")
    if classification_status not in {"valid", "human-confirmed"}:
        suffix = "invalid" if classification_status == "invalid" else "blocked"
        views["under-classification"].append(_finding(
            f"tech-lead.classification-{suffix}", True,
            str(classification_report.get("source_ref", "classification-report")),
            "global", "tech_lead",
            "Resolve the canonical classification report before Tech Lead review.",
            policy_ref,
        ))
    for key in ("requirements", "scenarios", "affected"):
        if not document.get(key):
            views["missing-canonical-context"].append(_finding(
                "tech-lead.canonical-context-missing", True, key, "global", "tech_lead",
                f"Provide source-linked {key}.", policy_ref,
            ))
    architecture = document.get("architecture_disposition", {})
    if architecture.get("state") not in {"accepted", "proposed", "not-required"}:
        views["architecture-disposition"].append(_finding(
            "tech-lead.architecture-disposition-missing", True,
            str(architecture.get("source_ref", "architecture")), "global", "tech_lead",
            "Record an accepted/proposed decision or evidence-based not-required result.", policy_ref,
        ))
    affected = [
        AffectedPath(str(row.get("repository", "")), str(row.get("path", "")))
        for row in document.get("affected", []) if isinstance(row, Mapping)
    ]
    resolution = resolve_tech_lead_ownership(owners, projects, affected, snapshot)
    for item in resolution.diagnostics:
        views["owner-dependency"].append(_finding(
            item.code, True, item.source or "owners-registry", "global", "tech_lead",
            "Resolve owner-zone coverage or authority conflict.", policy_ref,
        ))
    if any(not row.get("owner") for row in document.get("dependencies", [])):
        views["owner-dependency"].append(_finding(
            "tech-lead.dependency-owner-missing", True, "dependencies", "global",
            "tech_lead", "Assign a resolvable human dependency owner.", policy_ref,
        ))
    scope = document.get("scope", {})
    if scope.get("baseline") != scope.get("current") and scope.get("reassessment", {}).get("state") not in {"approved", "complete"}:
        views["scope-drift"].append(_finding(
            "tech-lead.scope-reassessment-required", True,
            str(scope.get("reassessment", {}).get("source_ref", "scope")), "global",
            "tech_lead", "Reassess classification, gates, owners, regression, and approval.", policy_ref,
        ))
    control = check_control_state(
        document.get("control_records", []), owners, projects, snapshot,
        as_of=as_of, evaluation_date=str(document.get("evaluation_date", "")),
    )
    for item in control.diagnostics:
        views["control-state"].append(_finding(
            item.code, True, item.source or "control-record", "global", "tech_lead",
            "Resolve the invalid human control record.", policy_ref,
        ))
    if control.state in {"stopped", "held", "escalated"}:
        views["control-state"].append(_finding(
            "tech-lead.control-active", True, "control-records", "global", "tech_lead",
            "Keep work held until an authorized resume is eligible.", policy_ref,
        ))
    gates = document.get("gate_reports", {})
    gate_checks = (
        ("review_ready", "review-ready", "missing-canonical-context"),
        ("definition_of_ready", "dor", "missing-canonical-context"),
        ("definition_of_done", "dod", "completion-dod"),
        ("release_transfer_readiness", "release", "release-recommendation"),
    )
    for field, label, view in gate_checks:
        status = gates.get(field)
        if status == "ready":
            continue
        suffix = "invalid" if status == "invalid" else "blocked"
        views[view].append(_finding(
            f"tech-lead.{label}-{suffix}", True,
            str(gates.get("source_ref", "gates")), "global", "tech_lead",
            f"Resolve the canonical {label} report before Tech Lead review.", policy_ref,
        ))
    for waiver in document.get("waivers", []):
        try:
            expired = date.fromisoformat(str(waiver.get("expires_on"))) < today
        except ValueError:
            expired = True
        if expired or waiver.get("valid") is not True:
            views["waiver-expiry"].append(_finding(
                "tech-lead.waiver-expired", True, str(waiver.get("source_ref", "waiver")),
                "global", "tech_lead", "Renew, close, or reject the expired waiver.", policy_ref,
            ))
    if document.get("classification") == "hotfix":
        for row in document.get("deferrals", []):
            if row.get("reconciled") is not True:
                views["hotfix-follow-up"].append(_finding(
                    "tech-lead.hotfix-follow-up-due", True,
                    str(row.get("source_ref", "deferral")), "global", "tech_lead",
                    "Complete source-linked hotfix reconciliation.", policy_ref,
                ))
    checkpoint = document.get("checkpoint", {})
    definition = next(
        (item for item in policy.checkpoints if item["event"] == checkpoint.get("event")),
        None,
    )
    if definition is None:
        views["checkpoint-summary"].append(_finding(
            "tech-lead.checkpoint-unknown", True,
            str(checkpoint.get("source_ref", "checkpoint")), "global", "tech_lead",
            "Select a checkpoint from the canonical Tech Lead policy.", policy_ref,
        ))
    else:
        if checkpoint.get("kind") != definition["kind"]:
            views["checkpoint-summary"].append(_finding(
                "tech-lead.checkpoint-kind-conflict", True,
                str(checkpoint.get("source_ref", "checkpoint")), "global", "tech_lead",
                "Use the configured checkpoint kind.", policy_ref,
            ))
        if checkpoint.get("source_ref") != definition["source_ref"]:
            views["checkpoint-summary"].append(_finding(
                "tech-lead.checkpoint-source-conflict", True,
                str(checkpoint.get("source_ref", "checkpoint")), "global", "tech_lead",
                "Use the configured checkpoint source.", policy_ref,
            ))
    if checkpoint.get("owner_ref") != policy.checkpoint_owner:
        views["checkpoint-summary"].append(_finding(
            "tech-lead.checkpoint-owner-conflict", True,
            str(checkpoint.get("source_ref", "checkpoint")), "global", "tech_lead",
            "Use the Tech Lead owner resolved by canonical configuration.", policy_ref,
        ))
    findings = [item for name in TECH_LEAD_VIEWS for item in views[name]]
    return _report(document, policy, findings, views, as_of=as_of)


def _report(
    document: Mapping[str, Any], policy: CompiledTechLeadPolicy | None,
    findings: list[dict[str, Any]], views: Mapping[str, Any],
    *, as_of: str,
) -> TechLeadReport:
    blocked = any(item["blocking"] for item in findings)
    gates = document.get("gate_reports", {})
    release = "recommend" if not blocked and gates.get("release_transfer_readiness") == "ready" else "do-not-recommend"
    payload = {
        "schema_version": "1.0", "status": "blocked" if blocked else "reviewable",
        "change_id": document.get("id"), "views": views, "findings": findings,
        "release_recommendation": release,
        "independent_approvals": {role: "still-required" for role in INDEPENDENT_APPROVALS},
        "decision_only": True, "control_state_mutated": False, "lifecycle_mutated": False,
        "as_of": as_of,
        "as_of_cutoff": _format_utc(_date_cutoff(as_of)) if _valid_date(as_of) else None,
        "evaluation_date": document.get("evaluation_date"),
        "snapshot_digest": (
            policy.snapshot_digest if policy else document.get("policy_snapshot", {}).get("digest")
        ),
        "policy_snapshot": ({"id": policy.policy_set[0], "version": policy.policy_set[1],
                             "digest": policy.snapshot_digest} if policy else None),
    }
    return TechLeadReport(_freeze(payload))


def _finding(
    code: str, blocking: bool, source_ref: str, zone: str, role: str,
    action: str, policy_ref: Mapping[str, str],
) -> dict[str, Any]:
    values = (
        code, "error" if blocking else "warning", blocking, source_ref, zone,
        role, action, dict(policy_ref),
    )
    return dict(zip(FINDING_FIELDS, values, strict=True))


def _snapshot_matches(value: Any, policy: CompiledTechLeadPolicy) -> bool:
    return isinstance(value, Mapping) and value == {
        "id": policy.policy_set[0], "version": policy.policy_set[1],
        "digest": policy.snapshot_digest,
    }


def _parse_rfc3339(value: Any) -> datetime | None:
    try:
        if not isinstance(value, str):
            return None
        parsed = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            return None
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def _date_cutoff(value: str) -> datetime:
    return datetime.combine(date.fromisoformat(value), time.max, tzinfo=timezone.utc)


def _format_utc(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _valid_date(value: Any) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def _active_control_state(active: Sequence[Mapping[str, Any]]) -> str:
    if not active:
        return "clear"
    return {
        "stop": "stopped", "hold": "held", "escalate": "escalated",
    }.get(str(active[-1].get("action")), "invalid")


def _affected_from_record(record: Mapping[str, Any]) -> list[AffectedPath]:
    result: list[AffectedPath] = []
    for value in record.get("affected_work", []):
        if isinstance(value, str) and ":" in value:
            repository, path = value.split(":", 1)
            result.append(AffectedPath(repository, path))
    return result


def _actor_authorized(actor: str, authority: str, resolution: TechLeadResolution) -> bool:
    if actor == resolution.primary:
        return authority in resolution.authority
    return any(actor == item.owner and authority in item.authority for item in resolution.delegates)


def _diag(code: str, message: str, *, source: str = "tech-lead") -> Diagnostic:
    return Diagnostic(code, "tech-lead", message, 8, source=source)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_thaw(item) for item in value]
    return value
