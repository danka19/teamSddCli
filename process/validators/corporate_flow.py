"""Deterministic, check-only corporate-flow governance evaluation."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .config_discovery import load_schema_resources
from .config_validation import schema_diagnostics
from .policy_validation import Diagnostic, PolicySnapshot
from .tech_lead import check_control_state, policy_snapshot_digest


REQUIRED_REASSESSMENTS = {
    "classification", "readiness", "owners", "regression", "estimates", "approval",
}
REQUIRED_ROLES = {
    "product", "analyst", "developer", "qa", "tech_lead", "release_support",
}
REQUIRED_PILOT_RISKS = {
    "data-privacy", "secrets", "access", "accidental-delivery", "rollback-or-hold",
    "adapters-and-mcps", "model-runtime-behavior", "logging", "external-dependencies",
    "support-ownership", "evidence-corruption", "process-bypass",
}
REQUIRED_RELEASE_CHAIN = {
    "tracker", "canonical_spec", "implementation", "ci_test", "release", "external_delivery",
}
OPERATIONAL_FAILED_RUN_FLAGS = {
    "canonical-evidence-corruption", "rollback-or-hold-unavailable",
    "unresolved-mandatory-check", "unsafe-continuation",
}
CANONICAL_STOP_TRIGGERS = {
    "required-context-missing-or-contradictory", "material-scope-drift-unassessed",
    "required-verification-unavailable", "critical-defect-unresolved",
    "security-compliance-access-policy-violation", "unauthorized-data-or-output-leakage-risk",
    "mandatory-evidence-collection-failure", "owner-authority-conflict",
    "rollback-or-hold-unavailable", "canonical-evidence-corruption",
    "approved-safety-authority-exceeded",
}
REGRESSION_FIELDS = (
    "product-or-module", "requirement-scenario", "change-class", "risk-trigger",
    "required-check", "test-data-environment", "evidence-type", "owner", "current-result",
)


@dataclass(frozen=True)
class CorporateFlowReport:
    payload: Mapping[str, Any]

    @property
    def exit_code(self) -> int:
        return 0 if self.payload["may_continue"] else 1

    def as_dict(self) -> dict[str, Any]:
        return json.loads(json.dumps(self.payload))

    def render_human(self) -> str:
        return "\n".join((
            f"Corporate flow: {self.payload['status']}",
            f"May continue: {str(self.payload['may_continue']).lower()}",
            f"Findings: {len(self.payload['findings'])}",
            f"Active records: {len(self.payload['active_record_ids'])}",
            "Check only: true",
        ))


def governance_record_digest(record: Mapping[str, Any]) -> str:
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def validate_corporate_flow_input(document: Any, process_root: Path) -> list[dict[str, str]]:
    resources = load_schema_resources(process_root / "schemas")
    diagnostics = schema_diagnostics(
        "corporate-flow-input.schema.json", document, "corporate-flow-input",
        stage=4, schema_resources=resources,
    )
    return [{
        "code": "corporate-flow.input-schema-invalid",
        "pointer": item.pointer or "/",
        "message": "Corporate-flow input does not satisfy the pinned schema.",
    } for item in diagnostics]


def validate_evaluation_cutoff(as_of: Any) -> list[dict[str, str]]:
    try:
        date.fromisoformat(as_of)
    except (TypeError, ValueError):
        return [{"code": "corporate-flow.as-of-invalid"}]
    return []


def evaluate_corporate_flow(
    document: Mapping[str, Any],
    owners: Mapping[str, Any],
    projects: Mapping[str, Any],
    snapshot: PolicySnapshot,
    *,
    as_of: str,
) -> CorporateFlowReport:
    findings: list[dict[str, Any]] = []
    active_ids: list[str] = []
    try:
        cutoff = datetime.combine(date.fromisoformat(as_of), time.max, tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return _report(document, snapshot, as_of, [_finding(
            "corporate-flow.as-of-invalid", "Evaluation cutoff must be an ISO date.", "input",
        )], [])

    expected_policy = {
        "id": snapshot.policy_set_id,
        "version": snapshot.policy_set_version,
        "digest": policy_snapshot_digest(snapshot),
    }
    policy_contract = {
        "regression.matrix-required-fields": REGRESSION_FIELDS,
        "flow.production-stop-triggers": tuple(CANONICAL_STOP_TRIGGERS),
        "failed-runs.attempt-kinds": ("validation", "ai", "adapter", "integration", "workflow"),
        "failed-runs.successful-retry-preserves-failure": True,
        "pilot.ai-disabled-core-required": True,
        "release.evidence-chain": ("tracker", "canonical-spec", "implementation", "ci-test", "release", "external-delivery"),
        "release.consumer-acceptance-separate": True,
        "failed-runs.retry-chain-fields": ("run-id", "attempt-kind", "attempt-ordinal", "input-refs", "output-refs", "retry-of", "predecessor-digest"),
    }
    for identifier, expected in policy_contract.items():
        rule = snapshot.rules.get(identifier)
        actual = rule.value if rule is not None else None
        valid = (
            set(actual) == set(expected)
            if identifier == "flow.production-stop-triggers" and isinstance(actual, tuple)
            else actual == expected
        )
        if rule is None or not valid:
            findings.append(_finding("corporate-flow.policy-contract-invalid", f"Required immutable policy rule {identifier} is missing or changed.", identifier))
    if str(document.get("evaluation_date", "")) != as_of:
        findings.append(_finding("corporate-flow.evaluation-date-mismatch", "Input evaluation date must match the requested cutoff.", "input"))
    records = [row for row in document.get("records", []) if isinstance(row, Mapping)]
    controls = [row for row in document.get("tech_lead_control_records", []) if isinstance(row, Mapping)]
    scope_ids = set(_strings(document.get("scope_ids")))
    evidence = {
        str(row.get("id")): row for row in document.get("evidence_catalog", [])
        if isinstance(row, Mapping) and isinstance(row.get("id"), str)
    }

    ids: list[str] = []
    instants: list[tuple[str, datetime]] = []
    superseded_ids: set[str] = set()
    for record in records:
        identifier = str(record.get("record_id", ""))
        ids.append(identifier)
        instant = _instant(record.get("recorded_at"))
        if instant is None:
            findings.append(_finding("governance.record-time-invalid", "Record time must be RFC3339 with timezone.", identifier))
        else:
            instants.append((identifier, instant))
            if instant > cutoff:
                findings.append(_finding("governance.record-future", "Future record is outside the evaluation cutoff.", identifier))
        record_scopes = set(_strings(record.get("scope_ids")))
        if not record_scopes or not record_scopes <= scope_ids:
            findings.append(_finding("governance.scope-mismatch", "Record scope is outside the checked bundle.", identifier))
        if record.get("policy_snapshot") != expected_policy:
            findings.append(_finding("governance.policy-snapshot-mismatch", "Record policy digest or pin does not match.", identifier))
        for ref in _strings(record.get("evidence_refs")):
            target = evidence.get(ref)
            if target is None:
                findings.append(_finding("governance.evidence-ref-unknown", "Evidence reference is absent from the local bundle.", identifier))
            elif not record_scopes <= set(_strings(target.get("scope_ids"))):
                findings.append(_finding("governance.evidence-scope-mismatch", "Evidence reference has incompatible scope.", identifier))
        actor = record.get("accountable_decision", {})
        if not isinstance(actor, Mapping) or actor.get("actor_type") != "human":
            findings.append(_finding("governance.human-decision-required", "Accountable decisions require a named human.", identifier))
        source_ref = record.get("source_ref")
        if not _local_ref(source_ref):
            findings.append(_finding("governance.source-ref-invalid", "Source reference must stay within the local bundle.", identifier))
        supersedes = record.get("supersedes")
        if supersedes is not None:
            predecessor = next((row for row in records if row.get("record_id") == supersedes), None)
            invalid_supersedes = (
                predecessor is None
                or predecessor.get("record_type") != record.get("record_type")
                or set(_strings(predecessor.get("scope_ids"))) != record_scopes
                or (_instant(predecessor.get("recorded_at")) or cutoff) >= (instant or cutoff)
            )
            if invalid_supersedes:
                findings.append(_finding("governance.supersedes-invalid", "Correction must append after the same record family and scope.", identifier))
            else:
                superseded_ids.add(str(supersedes))

    control_ids = [str(row.get("id", "")) for row in controls]
    ids.extend(control_ids)
    for control in controls:
        instant = _instant(control.get("recorded_at"))
        if instant is not None:
            instants.append((str(control.get("id", "")), instant))
    for duplicate in sorted({value for value in ids if value and ids.count(value) > 1}):
        findings.append(_finding("governance.record-id-duplicate", "Record identifiers are globally unique across the governance ledger.", duplicate))
    seen_instants: dict[datetime, list[str]] = {}
    for identifier, instant in instants:
        seen_instants.setdefault(instant, []).append(identifier)
    for tied in seen_instants.values():
        if len(tied) > 1:
            findings.append(_finding("governance.record-time-tie", "Equal instants make source ordering ambiguous.", ",".join(sorted(tied))))
    record_instants = [_instant(row.get("recorded_at")) for row in records]
    valid_instants = [row for row in record_instants if row is not None]
    if valid_instants != sorted(valid_instants):
        findings.append(_finding("governance.record-order-invalid", "Records must be supplied in source chronological order.", "records"))

    by_type: dict[str, list[Mapping[str, Any]]] = {}
    by_id = {str(row.get("record_id")): row for row in records}
    for record in records:
        if str(record.get("record_id")) not in superseded_ids:
            by_type.setdefault(str(record.get("record_type")), []).append(record)

    _check_triage(by_type, findings, active_ids)
    _check_scope_drift(by_type, by_id, findings)
    _check_quality(by_type, owners, snapshot, findings)
    _check_exceptions_and_evidence(by_type, by_id, as_of, findings)
    _check_release(by_type, evidence, findings)
    _check_roles(by_type, findings)
    _check_portfolio_and_pilot(by_type, findings)
    _check_failed_runs(by_type, by_id, findings, active_ids)
    _check_pilot_safety(by_type, snapshot, findings, active_ids)
    _check_payload_evidence(by_type, evidence, findings)

    if controls:
        state = check_control_state(
            controls, owners, projects, snapshot,
            as_of=as_of, evaluation_date=str(document.get("evaluation_date", "")),
        )
        active_ids.extend(str(value) for value in state.active_record_ids)
        if state.exit_code:
            findings.append(_finding("flow.active-control", "Existing Tech Lead control state blocks continuation.", "tech-lead-control"))
        for item in state.diagnostics:
            findings.append(_finding(item.code, item.message, item.source or "tech-lead-control"))

    return _report(document, snapshot, as_of, findings, active_ids)


def _check_triage(by_type: Mapping[str, list[Mapping[str, Any]]], findings: list[dict[str, Any]], active: list[str]) -> None:
    triage = _latest(by_type.get("initiative-triage", []))
    if triage is None:
        findings.append(_finding("flow.triage-missing", "Preliminary initiative triage is required.", "initiative"))
        return
    outcome = triage.get("payload", {}).get("outcome")
    if outcome == "proceed":
        baseline = _latest(by_type.get("approved-baseline", []))
        if baseline is None or baseline.get("payload", {}).get("approved") is not True:
            findings.append(_finding("flow.approved-baseline-missing", "Proceed requires a separately approved input baseline.", str(triage.get("record_id"))))
        elif baseline.get("payload", {}).get("quality_strategy_ref") not in {
            row.get("record_id") for row in by_type.get("quality-strategy", [])
        }:
            findings.append(_finding("flow.baseline-quality-strategy-unknown", "Approved baseline must link the applicable quality strategy.", str(baseline.get("record_id"))))
    elif outcome in {"hold", "split", "redirect", "reject"}:
        active.append(str(triage.get("record_id")))
        findings.append(_finding("flow.triage-not-proceeding", "Triage outcome does not authorize continuation.", str(triage.get("record_id"))))
    else:
        findings.append(_finding("flow.triage-outcome-invalid", "Unknown triage outcome.", str(triage.get("record_id"))))


def _check_scope_drift(by_type: Mapping[str, list[Mapping[str, Any]]], by_id: Mapping[str, Mapping[str, Any]], findings: list[dict[str, Any]]) -> None:
    for record in by_type.get("scope-drift", []):
        payload = record.get("payload", {})
        if payload.get("baseline_ref") not in by_id:
            findings.append(_finding("flow.scope-baseline-unknown", "Scope drift references an unknown baseline.", str(record.get("record_id"))))
        if payload.get("material") is True and not REQUIRED_REASSESSMENTS <= set(_strings(payload.get("reassessments"))):
            findings.append(_finding("flow.scope-reassessment-incomplete", "Material drift requires classification, readiness, owners, regression, estimates, and approval reassessment.", str(record.get("record_id"))))
        if payload.get("material") is True and payload.get("approval_decision_ref") not in by_id:
            findings.append(_finding("flow.scope-approval-missing", "Material drift requires a source-linked human approval decision.", str(record.get("record_id"))))


def _check_quality(by_type: Mapping[str, list[Mapping[str, Any]]], owners: Mapping[str, Any], snapshot: PolicySnapshot, findings: list[dict[str, Any]]) -> None:
    strategies = by_type.get("quality-strategy", [])
    rows = by_type.get("regression-row", [])
    qa_decisions = {str(row.get("record_id")): row for row in by_type.get("qa-decision", [])}
    if not strategies:
        findings.append(_finding("quality.strategy-missing", "Class-aware quality strategy is required.", "quality"))
    if not rows:
        findings.append(_finding("quality.regression-gap", "At least one applicable regression row or approved N/A rationale is required.", "regression"))
    for strategy in strategies:
        ref = strategy.get("payload", {}).get("qa_decision_ref")
        if ref not in qa_decisions:
            findings.append(_finding("quality.qa-decision-missing", "Quality strategy requires a configured QA decision.", str(strategy.get("record_id"))))
    for row in rows:
        if row.get("payload", {}).get("current_result") not in {"passed", "not-applicable-approved"}:
            findings.append(_finding("quality.regression-result-blocking", "Regression result is failed, stale, missing, or not run.", str(row.get("record_id"))))
    for decision in qa_decisions.values():
        actor = decision.get("accountable_decision", {})
        if not _owner_authorized(str(actor.get("actor_id", "")), "qa_owner", owners, snapshot):
            findings.append(_finding("quality.qa-authority-invalid", "QA sufficiency and result disposition require the configured QA owner.", str(decision.get("record_id"))))
        payload = decision.get("payload", {})
        if payload.get("decision") not in {"sufficient", "passed", "not-applicable-approved"} or payload.get("gate_may_proceed") is not True:
            findings.append(_finding("quality.qa-decision-blocking", "QA disposition does not permit the affected gate to proceed.", str(decision.get("record_id"))))


def _check_exceptions_and_evidence(by_type: Mapping[str, list[Mapping[str, Any]]], by_id: Mapping[str, Mapping[str, Any]], as_of: str, findings: list[dict[str, Any]]) -> None:
    for record in by_type.get("exception", []):
        payload = record.get("payload", {})
        expiry = payload.get("expires_on")
        if isinstance(expiry, str):
            try:
                if date.fromisoformat(expiry) < date.fromisoformat(as_of):
                    findings.append(_finding("flow.exception-expired", "Expired deviation, waiver, or deferral cannot authorize continuation.", str(record.get("record_id"))))
            except ValueError:
                findings.append(_finding("flow.exception-expiry-invalid", "Exception expiry must be an ISO date.", str(record.get("record_id"))))
    for record in by_type.get("human-decision", []):
        if record.get("accountable_decision", {}).get("actor_type") != "human":
            findings.append(_finding("flow.human-decision-authority-invalid", "Human decisions cannot be attributed to AI.", str(record.get("record_id"))))
    for record in by_type.get("ai-execution", []):
        payload = record.get("payload", {})
        if not payload.get("reviewer_disposition") or not payload.get("model_runtime"):
            findings.append(_finding("flow.ai-evidence-incomplete", "AI evidence requires reproducible runtime metadata and human disposition.", str(record.get("record_id"))))


def _check_release(by_type: Mapping[str, list[Mapping[str, Any]]], evidence: Mapping[str, Mapping[str, Any]], findings: list[dict[str, Any]]) -> None:
    releases = by_type.get("release-handoff", [])
    if not releases:
        findings.append(_finding("release.handoff-missing", "Per-change release or transfer handoff is required.", "release"))
        return
    for record in releases:
        payload = record.get("payload", {})
        chain = payload.get("chain", {})
        if not isinstance(chain, Mapping) or not REQUIRED_RELEASE_CHAIN <= set(chain):
            findings.append(_finding("release.evidence-chain-incomplete", "Tracker-to-delivery evidence chain is incomplete.", str(record.get("record_id"))))
        elif any(value not in evidence for value in chain.values()):
            findings.append(_finding("release.evidence-chain-unknown", "Release chain contains an unknown local evidence reference.", str(record.get("record_id"))))
        status = payload.get("artifact_repository_status")
        if status == "available" and "artifact_repository" not in chain:
            findings.append(_finding("release.artifact-coordinate-missing", "Applicable artifact repository evidence is missing.", str(record.get("record_id"))))
        if status == "unavailable" and not (payload.get("artifact_repository_substitute") in evidence and payload.get("substitute_decision_ref")):
            findings.append(_finding("release.artifact-substitute-missing", "Unavailable repository requires approved substitute evidence, never a fabricated coordinate.", str(record.get("record_id"))))
    acceptances = by_type.get("consumer-acceptance", [])
    release_ids = {str(row.get("record_id")) for row in releases}
    if not any(row.get("payload", {}).get("package_ref") in release_ids for row in acceptances):
        findings.append(_finding("release.consumer-acceptance-missing", "Consumer acceptance or deviation must be a separate source-linked record.", "release"))


def _check_roles(by_type: Mapping[str, list[Mapping[str, Any]]], findings: list[dict[str, Any]]) -> None:
    role_map = _latest(by_type.get("role-map", []))
    if role_map is None:
        findings.append(_finding("roles.map-missing", "Portable human role map is required.", "roles"))
        return
    payload = role_map.get("payload", {})
    rows = payload.get("roles", [])
    mapped: set[str] = set()
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, Mapping):
            continue
        mapped.add(str(row.get("role")))
        if row.get("owner_type") not in {"human", "group"} or str(row.get("owner_id", "")).lower() in {"ai", "assistant", "team", "generic"}:
            findings.append(_finding("roles.ai-substitution-forbidden", "Required human authority cannot be assigned to AI or a generic team label.", str(role_map.get("record_id"))))
    required = set(REQUIRED_ROLES)
    if payload.get("architecture_applicable") is True:
        required.add("architecture")
    if payload.get("security_applicable") is True:
        required.add("security")
    if not required <= mapped:
        findings.append(_finding("roles.required-owner-missing", "Required portable role mapping is incomplete.", str(role_map.get("record_id"))))
    walkthroughs = {row.get("payload", {}).get("role"): row for row in by_type.get("role-walkthrough", [])}
    for role in required:
        walkthrough = walkthroughs.get(role)
        payload = walkthrough.get("payload", {}) if walkthrough else {}
        if not walkthrough or not payload.get("scenario_evidence") or not payload.get("negative_cases") or payload.get("reviewer_disposition") != "passed":
            findings.append(_finding("roles.walkthrough-evidence-missing", "Checklist-only role understanding is insufficient.", str(role)))


def _check_portfolio_and_pilot(by_type: Mapping[str, list[Mapping[str, Any]]], findings: list[dict[str, Any]]) -> None:
    wip = _latest(by_type.get("portfolio-wip", []))
    if wip is None:
        findings.append(_finding("portfolio.wip-record-missing", "Approved WIP limit record is required.", "portfolio"))
    else:
        payload = wip.get("payload", {})
        if len(_strings(payload.get("active_change_ids"))) > int(payload.get("limit", 0)) and payload.get("decision") not in {"prioritize", "hold", "authorized-exception"}:
            findings.append(_finding("portfolio.wip-decision-required", "Exceeded WIP requires explicit prioritization, hold, or authorized exception.", str(wip.get("record_id"))))
    pilot = _latest(by_type.get("pilot-selection", []))
    if pilot is None:
        findings.append(_finding("pilot.selection-missing", "Synthetic pilot candidate selection record is required.", "pilot"))
    elif pilot.get("payload", {}).get("rollback_feasibility") != "verified":
        findings.append(_finding("pilot.rollback-unavailable", "Pilot candidate cannot proceed without verified rollback feasibility.", str(pilot.get("record_id"))))


def _check_failed_runs(by_type: Mapping[str, list[Mapping[str, Any]]], by_id: Mapping[str, Mapping[str, Any]], findings: list[dict[str, Any]], active: list[str]) -> None:
    attempts = by_type.get("failed-run", [])
    sequences: dict[tuple[str, int], list[str]] = {}
    for record in attempts:
        identifier = str(record.get("record_id"))
        payload = record.get("payload", {})
        if record.get("supersedes") is not None:
            findings.append(_finding("failed-run.supersede-forbidden", "Failed-run history is append-only and cannot be overwritten.", identifier))
        ordinal = payload.get("attempt_ordinal")
        if isinstance(ordinal, int):
            sequences.setdefault((str(payload.get("run_id")), ordinal), []).append(identifier)
        retry_of = payload.get("retry_of")
        if ordinal == 1 and (retry_of is not None or payload.get("predecessor_digest") is not None):
            findings.append(_finding("failed-run.initial-attempt-link-invalid", "Initial attempt cannot claim a retry predecessor.", identifier))
        if isinstance(ordinal, int) and ordinal > 1:
            predecessor = by_id.get(str(retry_of))
            if predecessor is None or predecessor.get("record_type") != "failed-run":
                findings.append(_finding("failed-run.retry-predecessor-missing", "Retry must preserve and link the prior attempt.", identifier))
            else:
                expected = governance_record_digest(predecessor)
                if payload.get("predecessor_digest") != expected:
                    findings.append(_finding("failed-run.predecessor-digest-mismatch", "Retry predecessor digest does not match immutable source evidence.", identifier))
                previous = predecessor.get("payload", {})
                if previous.get("run_id") != payload.get("run_id") or previous.get("attempt_ordinal") != ordinal - 1:
                    findings.append(_finding("failed-run.retry-sequence-invalid", "Retry chain run and ordinal must be contiguous.", identifier))
                if previous.get("outcome") != "failed":
                    findings.append(_finding("failed-run.retry-after-success-invalid", "A retry can only follow a retained failed attempt.", identifier))
        flags = set(_strings(payload.get("operational_flags")))
        if flags & OPERATIONAL_FAILED_RUN_FLAGS:
            active.append(identifier)
            findings.append(_finding("failed-run.operational-stop-required", "Failed attempt requires stop, hold, escalation, or remediation.", identifier))
    for identifiers in sequences.values():
        if len(identifiers) > 1:
            findings.append(_finding("failed-run.attempt-ordinal-duplicate", "Run attempt ordinals must be unique.", ",".join(sorted(identifiers))))


def _check_pilot_safety(by_type: Mapping[str, list[Mapping[str, Any]]], snapshot: PolicySnapshot, findings: list[dict[str, Any]], active: list[str]) -> None:
    record = _latest(by_type.get("pilot-safety", []))
    if record is None:
        findings.append(_finding("pilot.safety-record-missing", "Monitored-pilot safety record is required.", "pilot-safety"))
        return
    payload = record.get("payload", {})
    rows = payload.get("risks", [])
    mapped = {str(row.get("risk")): row for row in rows if isinstance(row, Mapping)}
    configured_rule = snapshot.rules.get("pilot.minimum-risk-controls")
    configured = set(configured_rule.value) if configured_rule is not None else set()
    required = REQUIRED_PILOT_RISKS | configured
    if not required <= set(mapped):
        findings.append(_finding("pilot.required-risk-missing", "Locked pilot risk set is incomplete.", str(record.get("record_id"))))
    if payload.get("ai_disabled_path") is not True:
        findings.append(_finding("pilot.ai-disabled-path-missing", "Core pilot safety path must work with AI disabled.", str(record.get("record_id"))))
    unsafe = [risk for risk, row in mapped.items() if row.get("status") != "controlled"]
    if unsafe:
        active.append(str(record.get("record_id")))
        findings.append(_finding("pilot.unsafe-risk-active", "Uncontrolled pilot risk requires hold or stop.", str(record.get("record_id"))))


def _check_payload_evidence(by_type: Mapping[str, list[Mapping[str, Any]]], evidence: Mapping[str, Mapping[str, Any]], findings: list[dict[str, Any]]) -> None:
    paths = {
        "regression-row": ("evidence_ref",),
        "ai-execution": ("output_ref",),
        "failed-run": ("input_refs", "output_refs"),
    }
    for record_type, fields in paths.items():
        for record in by_type.get(record_type, []):
            payload = record.get("payload", {})
            for field in fields:
                value = payload.get(field)
                refs = _strings(value) if isinstance(value, (list, tuple)) else [str(value)]
                if any(ref not in evidence for ref in refs):
                    findings.append(_finding("governance.payload-evidence-unknown", "Typed payload evidence reference is absent from the local bundle.", str(record.get("record_id"))))
    for record in by_type.get("pilot-safety", []):
        for risk in record.get("payload", {}).get("risks", []):
            if isinstance(risk, Mapping) and risk.get("evidence_ref") not in evidence:
                findings.append(_finding("governance.payload-evidence-unknown", "Pilot risk evidence is absent from the local bundle.", str(record.get("record_id"))))


def _owner_authorized(actor: str, slot: str, owners: Mapping[str, Any], snapshot: PolicySnapshot) -> bool:
    expected = snapshot.corporate_values.get(slot)
    if actor == expected:
        return True
    for group in owners.get("owner_groups", []):
        if isinstance(group, Mapping) and group.get("id") == expected:
            return actor in _strings(group.get("members"))
    return False


def _report(document: Mapping[str, Any], snapshot: PolicySnapshot, as_of: str, findings: Sequence[Mapping[str, Any]], active: Sequence[str]) -> CorporateFlowReport:
    sorted_findings = sorted(
        [dict(row) for row in findings], key=lambda row: (str(row.get("code")), str(row.get("source_ref"))),
    )
    may_continue = not sorted_findings
    triage = next((row for row in document.get("records", []) if isinstance(row, Mapping) and row.get("record_type") == "initiative-triage"), None)
    payload = {
        "schema_version": "1.0",
        "status": "may_continue" if may_continue else "blocked",
        "may_continue": may_continue,
        "change_id": document.get("change_id"),
        "as_of": as_of,
        "as_of_cutoff": f"{as_of}T23:59:59.999999Z",
        "evaluation_date": document.get("evaluation_date"),
        "policy_snapshot": {
            "id": snapshot.policy_set_id,
            "version": snapshot.policy_set_version,
            "digest": policy_snapshot_digest(snapshot),
        },
        "policy_sources": [
            {
                "rule": identifier,
                "policy_id": rule.policy_id,
                "policy_version": rule.policy_version,
                "source": rule.source,
                "pointer": rule.pointer,
            }
            for identifier, rule in sorted(snapshot.rules.items())
            if identifier.startswith(("flow.", "regression.", "release.", "pilot.", "failed-runs."))
        ],
        "triage_outcome": triage.get("payload", {}).get("outcome") if triage else None,
        "proceed_is_not_dor": True,
        "findings": sorted_findings,
        "active_record_ids": sorted(set(active)),
        "decision_only": True,
        "control_state_mutated": False,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }
    return CorporateFlowReport(payload)


def _finding(code: str, message: str, source_ref: str) -> dict[str, Any]:
    return {"code": code, "severity": "error", "blocking": True, "message": message, "source_ref": source_ref}


def _latest(records: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    return max(records, key=lambda row: str(row.get("recorded_at", "")), default=None)


def _strings(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, (list, tuple)) else []


def _instant(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def _local_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value or "://" in value or value.startswith(("/", "\\")):
        return False
    return ".." not in Path(value).parts
