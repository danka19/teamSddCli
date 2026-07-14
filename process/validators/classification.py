"""Pure deterministic classification over a resolved immutable policy snapshot."""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from .policy_validation import PolicySnapshot


TOOL_VERSION = "0.2.0"

_SUPPORTED_CLASSES = ("minor", "major", "hotfix")
_REQUIRED_STRICTER_ROUTES = {
    "minor": ("major",),
    "major": (),
    "hotfix": ("major",),
}
_REQUIRED_OBLIGATION_RULES = {
    "minor": (
        "artifacts.additional-required-artifacts",
        "artifacts.minor-required",
    ),
    "major": (
        "artifacts.additional-required-artifacts",
        "artifacts.minor-required",
        "artifacts.major-required",
    ),
    "hotfix": (
        "artifacts.additional-required-artifacts",
        "artifacts.hotfix-entry-required",
        "artifacts.hotfix-reconciliation-required",
    ),
    "major-impact-hotfix": ("artifacts.major-required",),
    "standard-major-from-hotfix": (
        "artifacts.hotfix-entry-required",
        "artifacts.hotfix-reconciliation-required",
    ),
}
_REQUIRED_REVIEWER_SLOTS = {
    "minor": ("tech_lead_owner",),
    "major": ("tech_lead_owner", "qa_owner"),
    "hotfix": ("tech_lead_owner", "qa_owner"),
}


@dataclass(frozen=True)
class ClassificationBlocker:
    code: str
    field: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "field": self.field, "message": self.message}


@dataclass(frozen=True)
class CompiledClassificationPolicy:
    policy_set_id: str
    policy_set_version: str
    allowed_classes: tuple[str, ...]
    minor_conditions: tuple[str, ...]
    major_triggers: tuple[str, ...]
    hotfix_conditions: tuple[str, ...]
    stricter_routes: Mapping[str, tuple[str, ...]]
    artifacts_by_rule: Mapping[str, tuple[str, ...]]
    obligation_rules: Mapping[str, tuple[str, ...]]
    reviewers_by_class: Mapping[str, tuple[str, ...]]


class _PolicyContractError(ValueError):
    pass


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
    try:
        policy = _compile_classification_policy(snapshot)
    except _PolicyContractError as error:
        return _invalid_policy_report(document, snapshot, str(error))

    evidence_rows = document.get("classification_evidence", [])
    evidence: dict[str, dict[str, Any]] = {}
    for row in evidence_rows if isinstance(evidence_rows, list) else []:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            evidence[row["id"]] = dict(row)

    corrections, correction_blockers = _apply_corrections(
        evidence, document.get("classification_corrections", [])
    )
    blockers = list(correction_blockers)

    minor_conditions = policy.minor_conditions
    major_triggers = policy.major_triggers
    hotfix_conditions = policy.hotfix_conditions

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
    elif declared not in policy.allowed_classes:
        blockers.append(ClassificationBlocker(
            "classification.invalid",
            "/classification",
            "Classification must be minor, major, or hotfix.",
        ))
    elif proposed is not None and not _route_is_allowed(policy, declared, proposed):
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
        policy, obligation_class, triggered, proposed
    )
    required_reviewers = _required_reviewers(policy, obligation_class)
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
                "id": policy.policy_set_id,
                "version": policy.policy_set_version,
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


def _route_is_allowed(
    policy: CompiledClassificationPolicy, declared: str, proposed: str
) -> bool:
    return declared == proposed or declared in policy.stricter_routes[proposed]


def _requires_stricter_route_reason(declared: Any, proposed: str | None) -> bool:
    return declared == "major" and proposed in {"minor", "hotfix"}


def _required_artifacts(
    policy: CompiledClassificationPolicy,
    selected: str | None,
    triggered: list[str],
    proposed: str | None,
) -> list[str]:
    if selected is None:
        return []
    identifiers = list(policy.obligation_rules[selected])
    if selected == "major" and proposed == "hotfix":
        identifiers.extend(policy.obligation_rules["standard-major-from-hotfix"])
    elif selected == "hotfix" and triggered:
        identifiers.extend(policy.obligation_rules["major-impact-hotfix"])
    values = {
        item
        for identifier in identifiers
        for item in policy.artifacts_by_rule[identifier]
    }
    return sorted(values)


def _required_reviewers(
    policy: CompiledClassificationPolicy, selected: str | None
) -> list[str]:
    if selected is None:
        return []
    return sorted(policy.reviewers_by_class[selected])


def _compile_classification_policy(
    snapshot: PolicySnapshot,
) -> CompiledClassificationPolicy:
    if not isinstance(snapshot.policy_set_id, str) or not snapshot.policy_set_id:
        raise _PolicyContractError("The resolved policy-set id is missing.")
    if (
        not isinstance(snapshot.policy_set_version, str)
        or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", snapshot.policy_set_version) is None
    ):
        raise _PolicyContractError("The resolved policy-set version is invalid.")

    allowed_classes = _required_string_tuple(snapshot, "classification.allowed-classes")
    if allowed_classes != _SUPPORTED_CLASSES:
        raise _PolicyContractError("The supported classification set has changed.")
    no_downgrade = _required_rule_value(snapshot, "classification.no-downgrade")
    if no_downgrade is not True:
        raise _PolicyContractError("The no-downgrade rule must remain enabled.")

    stricter_routes = _required_string_tuple_mapping(
        snapshot, "classification.allowed-stricter-routes"
    )
    if dict(stricter_routes) != _REQUIRED_STRICTER_ROUTES:
        raise _PolicyContractError("The supported stricter-route relationship changed.")
    obligation_rules = _required_string_tuple_mapping(
        snapshot, "classification.obligation-rules"
    )
    if dict(obligation_rules) != _REQUIRED_OBLIGATION_RULES:
        raise _PolicyContractError("The classification obligation mapping changed.")
    reviewer_slots = _required_string_tuple_mapping(
        snapshot, "classification.reviewer-slots"
    )
    if dict(reviewer_slots) != _REQUIRED_REVIEWER_SLOTS:
        raise _PolicyContractError("The classification reviewer mapping changed.")

    minor_conditions = _required_string_tuple(
        snapshot, "classification.minor-conditions"
    )
    major_triggers = tuple(dict.fromkeys((
        *_required_string_tuple(snapshot, "classification.major-triggers"),
        *_required_string_tuple(
            snapshot, "classification.additional-major-triggers", allow_empty=True
        ),
    )))
    hotfix_conditions = _required_string_tuple(
        snapshot, "classification.hotfix-eligibility"
    )

    artifact_rule_ids = tuple(dict.fromkeys(
        identifier
        for identifiers in obligation_rules.values()
        for identifier in identifiers
    ))
    _validate_policy_provenance(
        snapshot,
        (
            "classification.allowed-classes",
            "classification.no-downgrade",
            "classification.allowed-stricter-routes",
            "classification.obligation-rules",
            "classification.reviewer-slots",
            "classification.minor-conditions",
            "classification.major-triggers",
            "classification.additional-major-triggers",
            "classification.hotfix-eligibility",
        ),
        "classification",
    )
    _validate_policy_provenance(
        snapshot, artifact_rule_ids, "artifact-matrix"
    )
    artifacts_by_rule = MappingProxyType({
        identifier: _required_string_tuple(
            snapshot,
            identifier,
            allow_empty=identifier == "artifacts.additional-required-artifacts",
        )
        for identifier in artifact_rule_ids
    })
    reviewers_by_class: dict[str, tuple[str, ...]] = {}
    for classification, slots in reviewer_slots.items():
        reviewers: list[str] = []
        for slot in slots:
            owner = snapshot.corporate_values.get(slot)
            if not isinstance(owner, str) or not owner:
                raise _PolicyContractError(
                    f"Required reviewer slot {slot} is missing or invalid."
                )
            reviewers.append(owner)
        reviewers_by_class[classification] = tuple(dict.fromkeys(reviewers))

    return CompiledClassificationPolicy(
        policy_set_id=snapshot.policy_set_id,
        policy_set_version=snapshot.policy_set_version,
        allowed_classes=allowed_classes,
        minor_conditions=minor_conditions,
        major_triggers=major_triggers,
        hotfix_conditions=hotfix_conditions,
        stricter_routes=stricter_routes,
        artifacts_by_rule=artifacts_by_rule,
        obligation_rules=obligation_rules,
        reviewers_by_class=MappingProxyType(reviewers_by_class),
    )


def _required_rule_value(snapshot: PolicySnapshot, identifier: str) -> Any:
    rule = snapshot.rules.get(identifier)
    if rule is None:
        raise _PolicyContractError(f"Required policy rule {identifier} is missing.")
    return rule.value


def _validate_policy_provenance(
    snapshot: PolicySnapshot,
    identifiers: tuple[str, ...],
    expected_policy_id: str,
) -> None:
    versions: set[str] = set()
    for identifier in identifiers:
        rule = snapshot.rules.get(identifier)
        if (
            rule is None
            or rule.policy_id != expected_policy_id
            or not isinstance(rule.policy_version, str)
            or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", rule.policy_version) is None
        ):
            raise _PolicyContractError(
                f"Required policy rule {identifier} has invalid provenance."
            )
        versions.add(rule.policy_version)
    if len(versions) != 1:
        raise _PolicyContractError(
            f"Required {expected_policy_id} rules have conflicting versions."
        )


def _required_string_tuple(
    snapshot: PolicySnapshot, identifier: str, *, allow_empty: bool = False
) -> tuple[str, ...]:
    value = _required_rule_value(snapshot, identifier)
    if (
        not isinstance(value, tuple)
        or (not value and not allow_empty)
        or any(not isinstance(item, str) or not item for item in value)
        or len(set(value)) != len(value)
    ):
        raise _PolicyContractError(
            f"Required policy rule {identifier} must be a unique string list."
        )
    return value


def _required_string_tuple_mapping(
    snapshot: PolicySnapshot, identifier: str
) -> Mapping[str, tuple[str, ...]]:
    value = _required_rule_value(snapshot, identifier)
    if not isinstance(value, Mapping):
        raise _PolicyContractError(
            f"Required policy rule {identifier} must be a mapping."
        )
    normalized: dict[str, tuple[str, ...]] = {}
    for key, items in value.items():
        if (
            not isinstance(key, str)
            or not isinstance(items, tuple)
            or any(not isinstance(item, str) or not item for item in items)
            or len(set(items)) != len(items)
        ):
            raise _PolicyContractError(
                f"Required policy rule {identifier} has an invalid relationship."
            )
        normalized[key] = items
    return MappingProxyType(normalized)


def _invalid_policy_report(
    document: dict[str, Any], snapshot: PolicySnapshot, message: str
) -> ClassificationReport:
    decision = document.get("decision")
    decision_map = decision if isinstance(decision, dict) else {}
    return ClassificationReport({
        "schema_version": "1.0",
        "status": "blocked",
        "change_id": document.get("id"),
        "declared_class": document.get("classification"),
        "proposed_class": None,
        "selected_class": None,
        "source_inputs": [],
        "satisfied_conditions": [],
        "triggered_rules": [],
        "unknown_inputs": [],
        "blockers": [ClassificationBlocker(
            "classification.policy-contract-invalid",
            "/policy_set",
            message,
        ).as_dict()],
        "required_artifacts": [],
        "required_reviewers": [],
        "human_decision": {
            "owner_type": decision_map.get("owner_type"),
            "owner_id": decision_map.get("owner_id"),
            "state": decision_map.get("state"),
            "evidence_ref": decision_map.get("evidence_ref"),
            "confirmed": False,
        },
        "corrections": [],
        "versions": {
            "report_schema": "1.0",
            "tool": TOOL_VERSION,
            "policy_set": {
                "id": snapshot.policy_set_id,
                "version": snapshot.policy_set_version,
            },
        },
    })
