"""Scenario-first tests for deterministic Phase 2 classification behavior."""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from process.validators.classification import evaluate_classification
from process.validators.policy_validation import (
    EffectiveRule,
    PolicySnapshot,
    validate_policy_bundle,
)
from scripts.classify_change import main as classify_main


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


def _document(
    *,
    declared: str,
    facts: dict[str, bool | str],
    decision_state: str = "confirmed",
) -> dict[str, Any]:
    value = copy.deepcopy(_yaml(FIXTURES / "valid" / "minor.yaml"))
    value["classification"] = declared
    value["decision"]["state"] = decision_state
    value["classification_evidence"] = [
        {
            "id": identifier,
            "value": fact,
            "source": {"kind": "design", "ref": f"evidence/{identifier}.md"},
            "rationale": f"Synthetic evidence for {identifier}.",
        }
        for identifier, fact in facts.items()
    ]
    return value


def _minor_facts(snapshot: PolicySnapshot) -> dict[str, bool | str]:
    return {
        identifier: True
        for identifier in snapshot.rules["classification.minor-conditions"].value
    }


def _snapshot_with_rule(
    snapshot: PolicySnapshot, identifier: str, value: Any
) -> PolicySnapshot:
    rules = dict(snapshot.rules)
    retained = rules.get(identifier)
    rules[identifier] = replace(retained, value=value) if retained else EffectiveRule(
        value=value,
        source="bundled-policy",
        policy_id="classification",
        policy_version=snapshot.policy_set_version,
        pointer="/rules/test/value",
    )
    return replace(snapshot, rules=MappingProxyType(rules))


def _snapshot_without_rule(
    snapshot: PolicySnapshot, identifier: str
) -> PolicySnapshot:
    rules = dict(snapshot.rules)
    rules.pop(identifier, None)
    return replace(snapshot, rules=MappingProxyType(rules))


def _policy_blocker_codes(report: Any) -> set[str]:
    return {item["code"] for item in report.as_dict()["blockers"]}


def test_classifier_fails_closed_when_required_policy_rule_is_missing_or_malformed() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    candidates = (
        _snapshot_without_rule(snapshot, "classification.minor-conditions"),
        _snapshot_with_rule(snapshot, "classification.minor-conditions", "local-change"),
        _snapshot_without_rule(snapshot, "artifacts.minor-required"),
    )

    for candidate in candidates:
        report = evaluate_classification(document, candidate)
        assert report.exit_code == 1
        assert report.as_dict()["selected_class"] is None
        assert "classification.policy-contract-invalid" in _policy_blocker_codes(report)


def test_classifier_fails_closed_on_changed_class_and_route_policy_relationships() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))
    route_rule = {
        "minor": ("major",),
        "major": (),
        "hotfix": ("major",),
    }

    candidates = (
        _snapshot_with_rule(
            snapshot,
            "classification.allowed-classes",
            ("minor", "major", "expedited"),
        ),
        _snapshot_with_rule(snapshot, "classification.no-downgrade", False),
        _snapshot_without_rule(snapshot, "classification.allowed-stricter-routes"),
        _snapshot_with_rule(
            snapshot,
            "classification.allowed-stricter-routes",
            MappingProxyType({**route_rule, "minor": ("hotfix",)}),
        ),
    )

    for candidate in candidates:
        report = evaluate_classification(document, candidate)
        assert report.exit_code == 1
        assert "classification.policy-contract-invalid" in _policy_blocker_codes(report)


def test_classifier_fails_closed_on_changed_obligation_or_reviewer_mapping() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    candidates = (
        _snapshot_without_rule(snapshot, "classification.obligation-rules"),
        _snapshot_with_rule(
            snapshot,
            "classification.obligation-rules",
            MappingProxyType({"minor": ("artifacts.minor-required",)}),
        ),
        _snapshot_without_rule(snapshot, "classification.reviewer-slots"),
        _snapshot_with_rule(
            snapshot,
            "classification.reviewer-slots",
            MappingProxyType({
                "minor": ("qa_owner",),
                "major": ("tech_lead_owner", "qa_owner"),
                "hotfix": ("tech_lead_owner", "qa_owner"),
            }),
        ),
    )

    for candidate in candidates:
        report = evaluate_classification(document, candidate)
        assert report.exit_code == 1
        assert "classification.policy-contract-invalid" in _policy_blocker_codes(report)


def test_classifier_reports_the_compiled_snapshot_policy_version() -> None:
    snapshot = replace(_snapshot(), policy_set_version="2.7.3")
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    report = evaluate_classification(document, snapshot)

    assert report.as_dict()["versions"]["policy_set"] == {
        "id": "sdd-core",
        "version": "2.7.3",
    }


def test_classifier_fails_closed_on_conflicting_required_rule_version() -> None:
    snapshot = _snapshot()
    rules = dict(snapshot.rules)
    rules["classification.allowed-classes"] = replace(
        rules["classification.allowed-classes"], policy_version="9.9.9"
    )
    candidate = replace(snapshot, rules=MappingProxyType(rules))
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    report = evaluate_classification(document, candidate)

    assert report.exit_code == 1
    assert "classification.policy-contract-invalid" in _policy_blocker_codes(report)


def test_minor_requires_every_condition_and_reports_sources() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    report = evaluate_classification(document, snapshot)

    assert report.exit_code == 0
    assert report.as_dict()["selected_class"] == "minor"
    assert report.as_dict()["satisfied_conditions"] == sorted(_minor_facts(snapshot))
    assert report.as_dict()["source_inputs"][0] == {
        "id": "local-change",
        "value": True,
        "source": {"kind": "design", "ref": "evidence/local-change.md"},
    }


def test_unknown_or_missing_minor_fact_blocks_minor() -> None:
    snapshot = _snapshot()
    facts = _minor_facts(snapshot)
    facts["simple-rollback"] = "unknown"
    facts.pop("small-scope")

    report = evaluate_classification(_document(declared="minor", facts=facts), snapshot)

    assert report.exit_code == 1
    assert report.as_dict()["selected_class"] is None
    assert report.as_dict()["unknown_inputs"] == ["simple-rollback", "small-scope"]
    assert {item["code"] for item in report.as_dict()["blockers"]} == {
        "classification.minor-evidence-incomplete",
        "classification.human-confirmation-invalid",
    }


def test_major_returns_every_trigger_and_rejects_minor_downgrade() -> None:
    snapshot = _snapshot()
    triggers = list(snapshot.rules["classification.major-triggers"].value)
    facts = {identifier: True for identifier in triggers}

    report = evaluate_classification(_document(declared="minor", facts=facts), snapshot)

    assert report.exit_code == 1
    assert report.as_dict()["proposed_class"] == "major"
    assert report.as_dict()["triggered_rules"] == sorted(triggers)
    assert "classification.under-classified" in {
        item["code"] for item in report.as_dict()["blockers"]
    }
    assert set(snapshot.rules["artifacts.major-required"].value) <= set(
        report.as_dict()["required_artifacts"]
    )
    assert report.as_dict()["required_reviewers"] == [
        "sample-qa-owners", "sample-tech-leads"
    ]


def test_new_feature_metadata_cannot_hide_major_trigger_by_omitting_evidence() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))
    document["type"] = "new_feature"

    report = evaluate_classification(document, snapshot)

    assert report.exit_code == 1
    assert report.as_dict()["proposed_class"] == "major"
    assert "new-feature" in report.as_dict()["triggered_rules"]
    assert "classification.under-classified" in {
        item["code"] for item in report.as_dict()["blockers"]
    }


def test_pseudo_hotfix_is_rejected_without_increasing_harm() -> None:
    snapshot = _snapshot()
    facts = {
        "delay-increases-harm": False,
        "accelerated-route-required": True,
        "bounded-scope": True,
        "named-decision-owner": True,
    }

    report = evaluate_classification(_document(declared="hotfix", facts=facts), snapshot)

    assert report.exit_code == 1
    assert report.as_dict()["proposed_class"] is None
    assert "classification.hotfix-ineligible" in {
        item["code"] for item in report.as_dict()["blockers"]
    }


def test_major_impact_hotfix_retains_major_and_hotfix_obligations() -> None:
    snapshot = _snapshot()
    facts = {
        identifier: True
        for identifier in snapshot.rules["classification.hotfix-eligibility"].value
    }
    facts.update({"security-impact": True, "public-api-impact": True})

    report = evaluate_classification(_document(declared="hotfix", facts=facts), snapshot)
    payload = report.as_dict()

    assert report.exit_code == 0
    assert payload["selected_class"] == "hotfix"
    assert payload["triggered_rules"] == ["public-api-impact", "security-impact"]
    assert set(snapshot.rules["artifacts.major-required"].value) <= set(
        payload["required_artifacts"]
    )
    assert set(snapshot.rules["artifacts.hotfix-entry-required"].value) <= set(
        payload["required_artifacts"]
    )


def test_hotfix_eligible_change_may_use_reasoned_standard_major_route() -> None:
    snapshot = _snapshot()
    facts = {
        identifier: True
        for identifier in snapshot.rules["classification.hotfix-eligibility"].value
    }
    facts["security-impact"] = True
    document = _document(declared="major", facts=facts)
    document["extensions"] = {
        "stricter-route-reason": "Human owner selected the standard major sequence."
    }

    report = evaluate_classification(document, snapshot)
    payload = report.as_dict()

    assert report.exit_code == 0
    assert payload["selected_class"] == "major"
    assert payload["proposed_class"] == "hotfix"
    assert payload["triggered_rules"] == ["security-impact"]
    assert set(snapshot.rules["artifacts.major-required"].value) <= set(
        payload["required_artifacts"]
    )
    assert set(snapshot.rules["artifacts.hotfix-entry-required"].value) <= set(
        payload["required_artifacts"]
    )
    assert set(snapshot.rules["artifacts.hotfix-reconciliation-required"].value) <= set(
        payload["required_artifacts"]
    )


def test_report_is_stable_and_includes_versions_reviewers_and_human_state() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))

    first = evaluate_classification(document, snapshot).as_dict()
    second = evaluate_classification(copy.deepcopy(document), snapshot).as_dict()

    assert first == second
    assert first["versions"] == {
        "report_schema": "1.0",
        "tool": "0.2.0",
        "policy_set": {"id": "sdd-core", "version": "1.0.0"},
    }
    assert first["required_reviewers"] == ["sample-tech-leads"]
    assert first["human_decision"]["state"] == "confirmed"
    human = evaluate_classification(document, snapshot).render_human()
    for section in (
        "Source inputs:", "Satisfied conditions:", "Triggered rules:",
        "Unknown inputs:", "Required artifacts:", "Required reviewers:",
        "Human decision:",
    ):
        assert section in human


def test_pending_or_ai_confirmation_never_confirms_classification() -> None:
    snapshot = _snapshot()
    pending = _document(
        declared="minor", facts=_minor_facts(snapshot), decision_state="pending"
    )
    ai = copy.deepcopy(pending)
    ai["decision"].update({"owner_type": "ai", "state": "confirmed"})

    for document in (pending, ai):
        report = evaluate_classification(document, snapshot)
        assert report.exit_code == 1
        assert "classification.human-confirmation-required" in {
            item["code"] for item in report.as_dict()["blockers"]
        }


def test_audited_correction_recalculates_source_fact() -> None:
    snapshot = _snapshot()
    facts = _minor_facts(snapshot)
    facts["security-impact"] = True
    document = _document(declared="minor", facts=facts, decision_state="corrected")
    document["classification_corrections"] = [{
        "evidence_id": "security-impact",
        "previous_value": True,
        "corrected_value": False,
        "author_type": "human",
        "author_id": "sample-tech-lead",
        "reason": "The linked threat review proves there is no security impact.",
        "date": "2026-07-14",
        "reference": "evidence/security-review.md",
    }]

    report = evaluate_classification(document, snapshot)

    assert report.exit_code == 0
    assert report.as_dict()["selected_class"] == "minor"
    assert report.as_dict()["corrections"][0]["evidence_id"] == "security-impact"


def test_stricter_route_is_allowed_but_authority_text_cannot_downgrade_major() -> None:
    snapshot = _snapshot()
    stricter = _document(declared="major", facts=_minor_facts(snapshot))
    stricter["extensions"] = {"stricter-route-reason": "Local policy requires major."}
    major = _document(declared="minor", facts={"security-impact": True})

    assert evaluate_classification(stricter, snapshot).exit_code == 0
    assert evaluate_classification(stricter, snapshot).as_dict()["selected_class"] == "major"

    unjustified = copy.deepcopy(stricter)
    unjustified.pop("extensions")
    unjustified_report = evaluate_classification(unjustified, snapshot)
    assert unjustified_report.exit_code == 1
    assert "classification.stricter-route-reason-required" in {
        item["code"] for item in unjustified_report.as_dict()["blockers"]
    }

    for attempted_override in (
        {"waiver": "allow minor"},
        {"tech-lead-decision": "approve minor"},
        {"ai-recommendation": "minor"},
        {"free-text": "risk accepted"},
    ):
        candidate = copy.deepcopy(major)
        candidate["extensions"] = attempted_override
        report = evaluate_classification(candidate, snapshot)
        assert report.exit_code == 1
        assert report.as_dict()["proposed_class"] == "major"


def test_change_v2_schema_accepts_only_audited_human_corrections() -> None:
    snapshot = _snapshot()
    document = _document(declared="minor", facts=_minor_facts(snapshot))
    correction = {
        "evidence_id": "local-change",
        "previous_value": False,
        "corrected_value": True,
        "author_type": "human",
        "author_id": "sample-tech-lead",
        "reason": "The reviewed source evidence corrected the recorded fact.",
        "date": "2026-07-14",
        "reference": "evidence/correction.md",
    }
    document["classification_corrections"] = [correction]
    schema = json.loads(
        (ROOT / "process" / "schemas" / "change-v2.schema.json").read_text(
            encoding="utf-8"
        )
    )

    assert list(Draft202012Validator(schema).iter_errors(document)) == []
    document["classification_corrections"][0]["author_type"] = "ai"
    assert list(Draft202012Validator(schema).iter_errors(document))


def test_target_template_examples_and_read_pack_offer_only_current_classes(capsys) -> None:
    package = _yaml(ROOT / "process" / "package.yaml")
    paths = [package["templates"]["change_v2"], *package["examples"]["classification"]]
    seen: set[str] = set()
    for relative in paths:
        path = ROOT / "process" / relative
        text = path.read_text(encoding="utf-8")
        document = _yaml(path)
        assert "mode:" not in text
        assert document["classification"] in {"minor", "major", "hotfix"}
        assert document["schema_version"] == 2
        seen.add(document["classification"])
    assert seen == {"minor", "major", "hotfix"}

    read_pack = ROOT / "process" / package["read_packs"]["classification"]
    read_pack_text = read_pack.read_text(encoding="utf-8")
    assert "minor" in read_pack_text and "major" in read_pack_text and "hotfix" in read_pack_text
    assert "thin" not in read_pack_text and "full" not in read_pack_text

    assert classify_main(["--help"]) == 0
    help_text = capsys.readouterr().out
    assert "minor" in help_text and "major" in help_text and "hotfix" in help_text
    assert "thin" not in help_text and "full" not in help_text


SCENARIO_COVERAGE = {'test_audited_correction_recalculates_source_fact': [{'capability': 'corporate-change-classification',
                                                       'requirement': 'Human-owned classification confirmation and '
                                                                      'correction',
                                                       'scenario': 'Erroneous source input is corrected and '
                                                                   'recalculated',
                                                       'source_kind': 'delta'}],
 'test_classifier_fails_closed_on_changed_class_and_route_policy_relationships': [{'capability': 'corporate-change-classification',
                                                                                   'requirement': 'Human-owned '
                                                                                                  'classification '
                                                                                                  'confirmation and '
                                                                                                  'correction',
                                                                                   'scenario': 'Class criteria change '
                                                                                               'only through policy '
                                                                                               'change',
                                                                                   'source_kind': 'delta'}],
 'test_major_impact_hotfix_retains_major_and_hotfix_obligations': [{'capability': 'corporate-change-classification',
                                                                    'requirement': 'Accelerated hotfix route',
                                                                    'scenario': 'Urgent harmful delay qualifies for '
                                                                                'hotfix assessment',
                                                                    'source_kind': 'delta'},
                                                                   {'capability': 'corporate-change-classification',
                                                                    'requirement': 'Accelerated hotfix route',
                                                                    'scenario': 'Hotfix preserves minimum safety '
                                                                                'evidence',
                                                                    'source_kind': 'delta'},
                                                                   {'capability': 'corporate-change-classification',
                                                                    'requirement': 'Accelerated hotfix route',
                                                                    'scenario': 'Major-impact hotfix keeps risk '
                                                                                'obligations visible',
                                                                    'source_kind': 'delta'}],
 'test_major_returns_every_trigger_and_rejects_minor_downgrade': [{'capability': 'corporate-change-classification',
                                                                   'requirement': 'Conservative major triggers',
                                                                   'scenario': 'Any material trigger requires major',
                                                                   'source_kind': 'delta'},
                                                                  {'capability': 'corporate-change-classification',
                                                                   'requirement': 'Conservative major triggers',
                                                                   'scenario': 'Multiple triggers remain visible',
                                                                   'source_kind': 'delta'},
                                                                  {'capability': 'corporate-change-classification',
                                                                   'requirement': 'Human-owned classification '
                                                                                  'confirmation and correction',
                                                                   'scenario': 'Under-classification is rejected',
                                                                   'source_kind': 'delta'}],
 'test_minor_requires_every_condition_and_reports_sources': [{'capability': 'corporate-change-classification',
                                                              'requirement': 'Deterministic minor eligibility',
                                                              'scenario': 'Bounded low-impact change qualifies as '
                                                                          'minor',
                                                              'source_kind': 'delta'}],
 'test_pending_or_ai_confirmation_never_confirms_classification': [{'capability': 'corporate-change-classification',
                                                                    'requirement': 'Human-owned classification '
                                                                                   'confirmation and correction',
                                                                    'scenario': 'AI recommendation is advisory',
                                                                    'source_kind': 'delta'}],
 'test_pseudo_hotfix_is_rejected_without_increasing_harm': [{'capability': 'corporate-change-classification',
                                                             'requirement': 'Accelerated hotfix route',
                                                             'scenario': 'Convenience does not qualify as hotfix',
                                                             'source_kind': 'delta'}],
 'test_report_is_stable_and_includes_versions_reviewers_and_human_state': [{'capability': 'corporate-change-classification',
                                                                            'requirement': 'Explainable '
                                                                                           'classification report',
                                                                            'scenario': 'Report explains the result',
                                                                            'source_kind': 'delta'},
                                                                           {'capability': 'corporate-change-classification',
                                                                            'requirement': 'Explainable '
                                                                                           'classification report',
                                                                            'scenario': 'Machine-readable result is '
                                                                                        'stable',
                                                                            'source_kind': 'delta'}],
 'test_stricter_route_is_allowed_but_authority_text_cannot_downgrade_major': [{'capability': 'corporate-change-classification',
                                                                               'requirement': 'Human-owned '
                                                                                              'classification '
                                                                                              'confirmation and '
                                                                                              'correction',
                                                                               'scenario': 'Stricter route may be '
                                                                                           'selected',
                                                                               'source_kind': 'delta'}],
 'test_unknown_or_missing_minor_fact_blocks_minor': [{'capability': 'corporate-change-classification',
                                                      'requirement': 'Deterministic minor eligibility',
                                                      'scenario': 'Missing minor evidence blocks minor route',
                                                      'source_kind': 'delta'}]}
