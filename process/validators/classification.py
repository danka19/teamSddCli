"""Pure deterministic classification over a resolved immutable policy snapshot."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .policy_validation import PolicySnapshot


TOOL_VERSION = "0.2.0"


@dataclass(frozen=True)
class ClassificationBlocker:
    code: str
    field: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "field": self.field, "message": self.message}


@dataclass(frozen=True)
class ClassificationReport:
    payload: dict[str, Any]

    @property
    def exit_code(self) -> int:
        return 0 if self.payload["status"] == "valid" else 1

    def as_dict(self) -> dict[str, Any]:
        return self.payload

    def render_human(self) -> str:
        selected = self.payload["selected_class"] or "blocked"
        lines = [
            f"Classification: {selected}",
            f"Status: {self.payload['status']}",
            f"Policy: {self.payload['versions']['policy_set']['id']} "
            f"{self.payload['versions']['policy_set']['version']}",
            "Source inputs: " + ", ".join(
                f"{item['id']}={item['value']} ({(item.get('source') or {}).get('ref', 'unknown')})"
                for item in self.payload["source_inputs"]
            ),
            "Satisfied conditions: " + ", ".join(self.payload["satisfied_conditions"]),
            "Triggered rules: " + ", ".join(self.payload["triggered_rules"]),
            "Unknown inputs: " + ", ".join(self.payload["unknown_inputs"]),
            "Required artifacts: " + ", ".join(self.payload["required_artifacts"]),
            "Required reviewers: " + ", ".join(self.payload["required_reviewers"]),
            "Human decision: "
            f"{self.payload['human_decision']['state']} by "
            f"{self.payload['human_decision']['owner_id']}",
        ]
        for blocker in self.payload["blockers"]:
            lines.append(f"BLOCKER {blocker['code']}: {blocker['message']}")
        return "\n".join(lines)


def evaluate_classification(
    document: dict[str, Any], snapshot: PolicySnapshot
) -> ClassificationReport:
    """Evaluate class facts without mutating metadata or granting authority."""
    evidence_rows = document.get("classification_evidence", [])
    evidence: dict[str, dict[str, Any]] = {}
    for row in evidence_rows if isinstance(evidence_rows, list) else []:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            evidence[row["id"]] = dict(row)

    corrections, correction_blockers = _apply_corrections(
        evidence, document.get("classification_corrections", [])
    )
    blockers = list(correction_blockers)

    minor_conditions = _rule_values(snapshot, "classification.minor-conditions")
    major_triggers = [
        *_rule_values(snapshot, "classification.major-triggers"),
        *_rule_values(snapshot, "classification.additional-major-triggers"),
    ]
    hotfix_conditions = _rule_values(snapshot, "classification.hotfix-eligibility")

    for identifier, row in _metadata_major_facts(document, major_triggers).items():
        evidence[identifier] = row

    satisfied_minor = sorted(
        identifier
        for identifier in minor_conditions
        if _fact(evidence, identifier) is True
    )
    unknown_minor = sorted(
        identifier
        for identifier in minor_conditions
        if _fact(evidence, identifier) in (None, "unknown")
    )
    triggered = sorted(
        identifier
        for identifier in major_triggers
        if _fact(evidence, identifier) is True
    )
    unknown_hotfix = sorted(
        identifier
        for identifier in hotfix_conditions
        if _fact(evidence, identifier) in (None, "unknown")
    )
    hotfix_eligible = bool(hotfix_conditions) and all(
        _fact(evidence, identifier) is True for identifier in hotfix_conditions
    )

    declared = document.get("classification")
    proposed: str | None
    if hotfix_eligible:
        proposed = "hotfix"
    elif triggered:
        proposed = "major"
    elif len(satisfied_minor) == len(minor_conditions):
        proposed = "minor"
    else:
        proposed = None

    if declared == "hotfix" and not hotfix_eligible:
        blockers.append(ClassificationBlocker(
            "classification.hotfix-ineligible",
            "/classification",
            "Hotfix requires every harm, urgency, scope, and owner condition.",
        ))
    elif declared == "minor" and proposed in {"major", "hotfix"}:
        blockers.append(ClassificationBlocker(
            "classification.under-classified",
            "/classification",
            "The declared minor route cannot weaken a major or hotfix result.",
        ))
    elif declared not in {"minor", "major", "hotfix"}:
        blockers.append(ClassificationBlocker(
            "classification.invalid",
            "/classification",
            "Classification must be minor, major, or hotfix.",
        ))
    elif proposed is not None and not _route_is_allowed(declared, proposed):
        blockers.append(ClassificationBlocker(
            "classification.route-mismatch",
            "/classification",
            "The declared route is incompatible with deterministic evidence.",
        ))
    elif _requires_stricter_route_reason(declared, proposed):
        extensions = document.get("extensions")
        reason = (
            extensions.get("stricter-route-reason")
            if isinstance(extensions, dict) else None
        )
        if not isinstance(reason, str) or not reason.strip():
            blockers.append(ClassificationBlocker(
                "classification.stricter-route-reason-required",
                "/extensions/stricter-route-reason",
                "A human-selected stricter route requires a recorded reason.",
            ))

    if proposed is None and declared != "hotfix":
        blockers.append(ClassificationBlocker(
            "classification.minor-evidence-incomplete",
            "/classification_evidence",
            "Minor requires every condition; missing or unknown facts block the route.",
        ))

    decision = document.get("decision")
    decision_map = decision if isinstance(decision, dict) else {}
    human_confirmed = (
        decision_map.get("owner_type") == "human"
        and decision_map.get("state") in {"confirmed", "corrected"}
        and bool(decision_map.get("owner_id"))
        and bool(decision_map.get("evidence_ref"))
    )
    if not human_confirmed:
        blockers.append(ClassificationBlocker(
            "classification.human-confirmation-required",
            "/decision",
            "An authorized human confirmation is required; AI is advisory only.",
        ))
    elif proposed is None:
        blockers.append(ClassificationBlocker(
            "classification.human-confirmation-invalid",
            "/decision/state",
            "Human confirmation cannot replace missing deterministic evidence.",
        ))

    selected = None
    if proposed is not None and not blockers:
        selected = declared

    obligation_class = selected or (
        proposed if proposed in {"minor", "major", "hotfix"} else declared
    )
    required_artifacts = _required_artifacts(
        snapshot, obligation_class, triggered, proposed
    )
    required_reviewers = _required_reviewers(snapshot, obligation_class)
    source_inputs = [
        {
            "id": identifier,
            "value": row.get("value"),
            "source": row.get("source"),
        }
        for identifier, row in evidence.items()
    ]
    blocker_payload = [
        item.as_dict()
        for item in sorted(blockers, key=lambda item: (item.code, item.field))
    ]
    payload = {
        "schema_version": "1.0",
        "status": "blocked" if blocker_payload else "valid",
        "change_id": document.get("id"),
        "declared_class": declared,
        "proposed_class": proposed,
        "selected_class": selected,
        "source_inputs": source_inputs,
        "satisfied_conditions": satisfied_minor,
        "triggered_rules": triggered,
        "unknown_inputs": sorted(set([
            *unknown_minor,
            *(unknown_hotfix if declared == "hotfix" else []),
        ])),
        "blockers": blocker_payload,
        "required_artifacts": required_artifacts,
        "required_reviewers": required_reviewers,
        "human_decision": {
            "owner_type": decision_map.get("owner_type"),
            "owner_id": decision_map.get("owner_id"),
            "state": decision_map.get("state"),
            "evidence_ref": decision_map.get("evidence_ref"),
            "confirmed": human_confirmed,
        },
        "corrections": corrections,
        "versions": {
            "report_schema": "1.0",
            "tool": TOOL_VERSION,
            "policy_set": {
                "id": snapshot.policy_set_id,
                "version": snapshot.policy_set_version,
            },
        },
    }
    return ClassificationReport(payload)


def _apply_corrections(
    evidence: dict[str, dict[str, Any]], rows: Any
) -> tuple[list[dict[str, Any]], list[ClassificationBlocker]]:
    retained: list[dict[str, Any]] = []
    blockers: list[ClassificationBlocker] = []
    if not isinstance(rows, list):
        return retained, [ClassificationBlocker(
            "classification.correction-invalid",
            "/classification_corrections",
            "Classification corrections must be structured records.",
        )]
    required = {
        "evidence_id", "previous_value", "corrected_value", "author_type",
        "author_id", "reason", "date", "reference",
    }
    for index, row in enumerate(rows):
        pointer = f"/classification_corrections/{index}"
        if not isinstance(row, dict) or not required <= set(row):
            blockers.append(ClassificationBlocker(
                "classification.correction-invalid", pointer,
                "A correction requires source fact, human author, reason, date, and reference.",
            ))
            continue
        identifier = row["evidence_id"]
        original = evidence.get(identifier)
        if (
            row.get("author_type") != "human"
            or not isinstance(original, dict)
            or original.get("value") != row.get("previous_value")
            or row.get("corrected_value") not in (True, False, "unknown")
            or not all(row.get(key) for key in ("author_id", "reason", "date", "reference"))
        ):
            blockers.append(ClassificationBlocker(
                "classification.correction-invalid", pointer,
                "The correction does not match source evidence or lacks human audit data.",
            ))
            continue
        original["value"] = row["corrected_value"]
        retained.append({key: row[key] for key in sorted(required)})
    return retained, blockers


def _fact(evidence: dict[str, dict[str, Any]], identifier: str) -> Any:
    row = evidence.get(identifier)
    return row.get("value") if isinstance(row, dict) else None


def _metadata_major_facts(
    document: dict[str, Any], major_triggers: list[str]
) -> dict[str, dict[str, Any]]:
    """Return major facts that are already unambiguous in canonical metadata."""
    derived: dict[str, dict[str, Any]] = {}
    if document.get("type") == "new_feature" and "new-feature" in major_triggers:
        derived["new-feature"] = {
            "id": "new-feature",
            "value": True,
            "source": {"kind": "metadata", "ref": "/type"},
            "rationale": "Work type new_feature is a canonical major trigger.",
        }
    return derived


def _rule_values(snapshot: PolicySnapshot, identifier: str) -> list[str]:
    rule = snapshot.rules.get(identifier)
    if rule is None or not isinstance(rule.value, tuple):
        return []
    return [str(item) for item in rule.value]


def _route_is_allowed(declared: str, proposed: str) -> bool:
    if declared == proposed:
        return True
    return declared == "major" and proposed in {"minor", "hotfix"}


def _requires_stricter_route_reason(declared: Any, proposed: str | None) -> bool:
    return declared == "major" and proposed in {"minor", "hotfix"}


def _required_artifacts(
    snapshot: PolicySnapshot,
    selected: str | None,
    triggered: list[str],
    proposed: str | None,
) -> list[str]:
    if selected is None:
        return []
    identifiers = ["artifacts.additional-required-artifacts"]
    if selected == "minor":
        identifiers.append("artifacts.minor-required")
    elif selected == "major":
        identifiers.extend(("artifacts.minor-required", "artifacts.major-required"))
        if proposed == "hotfix":
            identifiers.extend((
                "artifacts.hotfix-entry-required",
                "artifacts.hotfix-reconciliation-required",
            ))
    else:
        identifiers.extend((
            "artifacts.hotfix-entry-required",
            "artifacts.hotfix-reconciliation-required",
        ))
        if triggered:
            identifiers.append("artifacts.major-required")
    values = {
        item for identifier in identifiers for item in _rule_values(snapshot, identifier)
    }
    return sorted(values)


def _required_reviewers(snapshot: PolicySnapshot, selected: str | None) -> list[str]:
    if selected is None:
        return []
    values = [snapshot.corporate_values.get("tech_lead_owner")]
    if selected in {"major", "hotfix"}:
        values.append(snapshot.corporate_values.get("qa_owner"))
    return sorted({str(item) for item in values if item})
