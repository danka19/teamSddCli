"""Scenario-first evidence for Phase 2 work item 2.3.

These tests cover only the static change/policy/config foundation.  They do not
classify a change, migrate legacy metadata, evaluate a gate, or mutate workflow
state.
"""

from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from process.validators.policy_validation import validate_policy_bundle
from process.validators.change_v2_validation import change_v2_integrity_diagnostics


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "process" / "schemas"
POLICIES = ROOT / "process" / "policies"
FIXTURES = ROOT / "tests" / "fixtures" / "policy-v2"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def validator(name: str) -> Draft202012Validator:
    registry = Registry()
    for path in sorted(SCHEMAS.glob("*.json")):
        schema = load_json(path)
        registry = registry.with_resource(
            path.name,
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
    return Draft202012Validator(load_json(SCHEMAS / name), registry=registry)


def errors(name: str, document: dict[str, Any]) -> list[Any]:
    return list(validator(name).iter_errors(document))


def diagnostic_codes(result: Any) -> list[str]:
    return [item.code for item in result.diagnostics]


def test_change_v2_accepts_all_classes_and_preserves_decision_facts() -> None:
    for classification in ("minor", "major", "hotfix"):
        document = load_yaml(FIXTURES / "valid" / f"{classification}.yaml")
        assert errors("change-v2.schema.json", document) == []
        assert document["schema_version"] == 2
        assert document["classification"] == classification
        assert document["type"] != document["status"]
        assert {item["value"] for item in document["classification_evidence"]} <= {
            True,
            False,
            "unknown",
        }
        assert document["decision"]["owner_type"] == "human"
        assert document["policy"] == {
            "id": "sdd-core",
            "version": "1.0.0",
        }
        assert "mode" not in document

    canonical_types = (
        "new_feature",
        "behavior_change",
        "bugfix",
        "refactor",
        "docs_only",
        "config_ops",
    )
    candidate = load_yaml(FIXTURES / "valid" / "minor.yaml")
    for work_type in canonical_types:
        candidate["type"] = work_type
        assert errors("change-v2.schema.json", candidate) == [], work_type
    for legacy_or_route_value in ("feature", "maintenance", "emergency", "hotfix"):
        candidate["type"] = legacy_or_route_value
        assert errors("change-v2.schema.json", candidate), legacy_or_route_value


def test_change_v2_rejects_unknown_class_and_legacy_mode() -> None:
    valid = load_yaml(FIXTURES / "valid" / "minor.yaml")

    unknown = copy.deepcopy(valid)
    unknown["classification"] = "routine"
    assert errors("change-v2.schema.json", unknown)

    conflicting = copy.deepcopy(valid)
    conflicting["mode"] = "thin"
    assert any(error.validator == "additionalProperties" for error in errors(
        "change-v2.schema.json", conflicting
    ))

    duplicate = copy.deepcopy(valid)
    duplicate["classification_evidence"].append(
        copy.deepcopy(duplicate["classification_evidence"][0])
    )
    assert [item.code for item in change_v2_integrity_diagnostics(duplicate)] == [
        "change.evidence-id-duplicate"
    ]


def test_native_v2_change_rejects_legacy_reference() -> None:
    native = load_yaml(FIXTURES / "valid" / "minor.yaml")
    native["compatibility"]["legacy_ref"] = "legacy-change.yaml"

    assert errors("change-v2.schema.json", native)


def test_negative_change_fixtures_retain_facts_without_computing_a_verdict() -> None:
    expected_facts = {
        "unknown-impact.yaml": ("unknown-impact", "unknown"),
        "under-classification.yaml": ("major-trigger", True),
        "major-impact-hotfix.yaml": ("major-impact", True),
        "pseudo-hotfix.yaml": ("delay-increases-harm", False),
    }
    for filename, (fact_id, value) in expected_facts.items():
        document = load_yaml(FIXTURES / "decision-inputs" / filename)
        assert errors("change-v2.schema.json", document) == []
        evidence = {item["id"]: item["value"] for item in document["classification_evidence"]}
        assert evidence[fact_id] == value


def test_manifest_pins_one_versioned_local_policy_set() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    assert errors("policy-manifest.schema.json", manifest) == []
    assert manifest["policy_set"] == {"id": "sdd-core", "version": "1.0.0"}
    assert {item["kind"] for item in manifest["policies"]} == {
        "classification",
        "artifact-matrix",
        "gates",
        "regression",
        "flow-controls",
        "release",
        "pilot-safety",
        "failed-runs",
    }
    for item in manifest["policies"]:
        assert not Path(item["path"]).is_absolute()
        policy = load_yaml(ROOT / "process" / item["path"])
        assert errors("policy-document.schema.json", policy) == []
        assert policy["policy_id"] == item["id"]
        assert policy["version"] == item["version"]
        assert policy["kind"] == item["kind"]


def test_policy_document_schema_requires_kind_specific_foundation_catalogs() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    required_catalogs = {
        "classification": {
            "classification.minor-conditions": {
                "local-change", "small-scope", "simple-rollback",
                "no-user-scenario-impact", "no-sla-impact",
                "no-security-compliance-impact", "no-external-integration-impact",
                "no-data-model-impact", "no-component-interaction-impact",
                "no-public-api-impact", "no-cross-repository-impact",
                "no-reliability-impact", "no-performance-impact",
                "no-operations-impact", "no-governed-test-impact",
                "no-governed-documentation-impact",
                "no-architecture-decision-required",
            },
            "classification.major-triggers": {
                "new-feature", "business-logic-change", "user-scenario-change",
                "component-interaction-change", "required-test-behavior-change",
                "governed-documentation-change", "public-api-impact",
                "integration-impact", "data-impact", "security-impact",
                "compliance-impact", "sla-impact", "external-dependency",
                "cross-repository-work", "reliability-impact",
                "performance-impact", "operations-impact", "regression-risk",
                "high-rollback-cost", "architecture-decision-required",
            },
            "classification.hotfix-eligibility": {
                "delay-increases-harm", "accelerated-route-required",
                "bounded-scope", "named-decision-owner",
            },
            "classification.hotfix-obligations": {
                "human-ownership", "minimum-scenario-evidence",
                "minimum-regression-evidence", "rollback-or-hold",
                "traceability", "required-security-compliance-review",
                "reconciliation-follow-up", "retain-major-impact-obligations",
            },
        },
        "artifact-matrix": {
            "artifacts.minor-required": {
                "proposal-intent", "openspec-delta-when-behavior-changes",
                "testable-scenarios", "classification-rationale",
                "bounded-impact-risk-evidence", "quality-regression-approach",
                "basic-traceability", "implementation-plan",
                "verification-evidence", "rollback-or-hold", "human-decisions",
            },
            "artifacts.major-required": {
                "expanded-design-impact-analysis",
                "architecture-decision-or-not-required",
                "owner-dependency-map", "quality-strategy",
                "qa-test-plan-or-valid-waiver",
                "automation-plan-or-valid-waiver", "broad-regression-matrix",
                "migration-evidence-when-applicable",
                "rollback-evidence-when-applicable",
                "release-transfer-package-or-not-applicable",
                "complete-traceability", "class-appropriate-approvals",
            },
            "artifacts.hotfix-entry-required": {
                "harm-urgency-rationale", "bounded-scope", "affected-contour",
                "named-decision-owner", "known-gaps", "testable-scenario",
                "minimum-safety-regression-evidence", "rollback-or-hold",
                "required-risk-decisions", "traceability", "reconciliation-plan",
            },
            "artifacts.hotfix-reconciliation-required": {
                "deferred-artifact-disposition", "post-change-verification",
                "release-transfer-package-when-applicable",
                "completed-reconciliation-follow-up",
            },
            "artifacts.conditional-not-applicable": {
                "openspec-delta-when-behavior-changes",
                "architecture-decision-or-not-required",
                "migration-evidence-when-applicable",
                "rollback-evidence-when-applicable",
                "release-transfer-package-or-not-applicable",
                "release-transfer-evidence-when-applicable",
            },
            "artifacts.waiver-eligible": {
                "qa-test-plan-or-valid-waiver",
                "automation-plan-or-valid-waiver",
            },
            "artifacts.hotfix-deferrable": {
                "expanded-design-impact-analysis",
                "architecture-decision-or-not-required",
                "owner-dependency-map", "quality-strategy",
                "qa-test-plan-or-valid-waiver",
                "automation-plan-or-valid-waiver", "broad-regression-matrix",
                "migration-evidence-when-applicable",
                "release-transfer-package-or-not-applicable",
            },
        },
        "gates": {
            "gates.named-catalog": {
                "review-ready", "definition-of-ready",
                "implementation-start-approval", "implementation-complete",
                "definition-of-done", "release-transfer-readiness",
                "archive-readiness", "archive-approval",
            },
            "gates.common-definition-of-ready": {
                "business-goal-value", "owner", "scope-and-exclusions",
                "type-classification-rationale", "affected-systems-owners",
                "dependencies", "requirements-scenarios", "acceptance-criteria",
                "quality-verification-strategy", "security-data-operations-assessment",
                "rollback-or-hold", "initial-traceability",
                "resolved-blocking-questions", "valid-waivers", "human-approvals",
            },
            "gates.definition-of-done": {
                "acceptance-evidence", "defect-disposition",
                "review-comment-disposition", "documentation-current",
                "traceability-current", "required-checks-complete",
                "valid-waivers", "class-obligations-resolved",
            },
            "gates.release-transfer-readiness": {
                "version-or-tag", "release-notes", "included-scope-ids",
                "verification-summary", "known-limitations",
                "deployment-or-transfer-instructions", "rollback-or-hold",
                "operational-support-checks", "responsible-roles",
                "unresolved-follow-ups",
            },
            "gates.archive-readiness": {
                "definition-of-done", "release-transfer-evidence-when-applicable",
                "traceability", "waiver-disposition", "follow-up-disposition",
                "current-policy-compatibility",
            },
            "gates.review-ready": {
                "proposal-intent", "openspec-delta-when-behavior-changes",
                "testable-scenarios", "classification-rationale",
                "basic-traceability",
            },
            "gates.implementation-complete": {
                "implementation-evidence", "required-tests",
                "required-checks-complete", "verification-evidence",
            },
        },
        "regression": {
            "regression.matrix-required-fields": {
                "product-or-module", "requirement-scenario", "change-class",
                "risk-trigger", "required-check", "test-data-environment",
                "evidence-type", "owner", "current-result",
            },
            "regression.minimum-obligations": {
                "source-linked-evidence", "applicable-row-or-not-applicable",
                "qa-owner-disposition", "visible-coverage-gaps",
            },
        },
        "flow-controls": {
            "flow.production-stop-triggers": {
                "required-context-missing-or-contradictory",
                "material-scope-drift-unassessed",
                "required-verification-unavailable", "critical-defect-unresolved",
                "security-compliance-access-policy-violation",
                "unauthorized-data-or-output-leakage-risk",
                "mandatory-evidence-collection-failure", "owner-authority-conflict",
                "rollback-or-hold-unavailable", "canonical-evidence-corruption",
                "approved-safety-authority-exceeded",
            },
        },
        "release": {
            "release.distinct-states": {
                "implementation-complete", "definition-of-done", "release-ready",
                "archive-ready", "archived", "delivered",
            },
            "release.package-minimums": {
                "artifact-version", "included-changes", "requirements-scenarios",
                "verification-evidence", "known-limitations",
                "configuration-assumptions", "installation-transfer-steps",
                "rollback-or-hold", "operations-support-contacts",
                "unresolved-follow-ups",
            },
            "release.lifecycle-states": {
                "draft", "spec_review", "approved", "in_implementation",
                "ready_to_archive", "archived",
            },
            "release.external-state-non-inference": {
                "delivered", "deployed", "tracker-done",
            },
        },
        "pilot-safety": {
            "pilot.minimum-risk-controls": {
                "data-privacy", "secrets", "access", "accidental-delivery",
                "rollback-or-hold", "adapters-and-mcps", "model-runtime-behavior",
                "logging", "external-dependencies", "support-ownership",
                "evidence-corruption", "process-bypass",
            },
        },
        "failed-runs": {
            "failed-runs.attempt-kinds": {
                "validation", "ai", "adapter", "integration", "workflow",
            },
            "failed-runs.minimum-fields": {
                "attempt-id", "outcome", "source", "time",
                "version-or-configuration", "owner-disposition",
            },
        },
    }

    for item in manifest["policies"]:
        policy = load_yaml(ROOT / "process" / item["path"])
        rules = {rule["id"]: rule for rule in policy["rules"]}
        for rule_id, required_items in required_catalogs[item["kind"]].items():
            assert rule_id in rules, rule_id
            assert set(rules[rule_id]["value"]) == required_items, rule_id
            for missing_item in required_items:
                candidate = copy.deepcopy(policy)
                candidate_rule = next(
                    rule for rule in candidate["rules"] if rule["id"] == rule_id
                )
                candidate_rule["value"].remove(missing_item)
                assert errors("policy-document.schema.json", candidate), (
                    rule_id,
                    missing_item,
                )


def test_policy_bundle_builds_immutable_provenance_snapshot() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
    result = validate_policy_bundle(ROOT / "process", manifest, config, None)

    assert result.diagnostics == []
    assert result.snapshot is not None
    retained = result.snapshot.rules["classification.no-downgrade"]
    assert retained.value is True
    assert retained.source == "bundled-policy"
    assert retained.policy_id == "classification"
    assert retained.pointer.startswith("/rules/")


def test_policy_bundle_rejects_missing_values_and_weakening_with_provenance() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    cases = {
        "missing-corporate-value.yaml": "policy.corporate-value-missing",
        "weaken-locked.yaml": "policy.override-locked",
        "delete-additive.yaml": "policy.override-additive-delete",
        "weaken-stricter-only.yaml": "policy.override-not-stricter",
        "unknown-rule.yaml": "policy.override-unknown-rule",
    }
    for filename, expected in cases.items():
        config = load_yaml(FIXTURES / "config" / filename)
        result = validate_policy_bundle(ROOT / "process", manifest, config, None)
        assert expected in diagnostic_codes(result), filename
        diagnostic = next(item for item in result.diagnostics if item.code == expected)
        assert diagnostic.source == "central-config"
        assert diagnostic.pointer.startswith("/policy_set/")


def test_stricter_only_rejects_boolean_and_incomparable_numeric_types() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")

    for value in (True, 2.0):
        config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
        config["policy_set"]["overrides"] = [{
            "rule_id": "regression.minimum-scenarios",
            "operation": "set",
            "value": value,
        }]

        result = validate_policy_bundle(ROOT / "process", manifest, config, None)

        assert "policy.override-not-stricter" in diagnostic_codes(result), value


def test_adapter_override_is_bounded_and_cannot_supply_policy_paths() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
    adapter = load_yaml(FIXTURES / "config" / "invalid-adapter-policy-path.yaml")
    result = validate_policy_bundle(ROOT / "process", manifest, config, adapter)
    assert "policy.adapter-path-forbidden" in diagnostic_codes(result)


def test_adapter_addition_builds_on_central_addition_in_discovery_order() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
    adapter = {
        "policy_set": {
            "id": "sdd-core",
            "version": "1.0.0",
            "overrides": [{
                "rule_id": "classification.additional-major-triggers",
                "operation": "add",
                "value": ["sample-project-trigger"],
            }],
        }
    }
    result = validate_policy_bundle(ROOT / "process", manifest, config, adapter)
    assert result.diagnostics == []
    assert result.snapshot is not None
    assert result.snapshot.rules["classification.additional-major-triggers"].value == (
        "sample-corporate-trigger",
        "sample-project-trigger",
    )
    assert result.snapshot.rules["classification.additional-major-triggers"].source == (
        "project-adapter"
    )


def test_additive_overrides_enforce_slot_value_type_with_provenance() -> None:
    manifest = load_yaml(POLICIES / "manifest.yaml")
    invalid_values = ("scalar-trigger", {"trigger": "object"}, ["not valid id"])

    for source, invalid_value in (
        ("central-config", invalid_values[0]),
        ("central-config", invalid_values[1]),
        ("project-adapter", invalid_values[2]),
    ):
        config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
        adapter = None
        override = {
            "rule_id": "classification.additional-major-triggers",
            "operation": "add",
            "value": invalid_value,
        }
        if source == "central-config":
            config["policy_set"]["overrides"] = [override]
        else:
            config["policy_set"]["overrides"] = []
            adapter = {
                "policy_set": {
                    "id": "sdd-core",
                    "version": "1.0.0",
                    "overrides": [override],
                }
            }

        result = validate_policy_bundle(ROOT / "process", manifest, config, adapter)

        assert result.snapshot is None
        diagnostic = next(
            item
            for item in result.diagnostics
            if item.code == "policy.override-value-invalid"
        )
        assert diagnostic.source == source
        assert diagnostic.pointer == "/policy_set/overrides/0/value"


def test_policy_integrity_rejects_versions_duplicates_missing_refs_and_cycles(
    tmp_path: Path,
) -> None:
    config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
    for name, expected in {
        "version-mismatch": "policy.version-mismatch",
        "duplicate-rule": "policy.rule-id-duplicate",
        "missing-reference": "policy.reference-missing",
        "cyclic-requirements": "policy.requirement-cycle",
    }.items():
        package = tmp_path / name
        shutil.copytree(ROOT / "process", package)
        candidate = load_yaml(package / "policies" / "manifest.yaml")
        if name == "version-mismatch":
            candidate["policies"][0]["version"] = "1.0.1"
        elif name in {"duplicate-rule", "missing-reference"}:
            policy_path = package / "policies" / "classification.yaml"
            policy = load_yaml(policy_path)
            if name == "duplicate-rule":
                policy["rules"].append(copy.deepcopy(policy["rules"][0]))
            else:
                policy["rules"][0]["refs"] = ["missing.rule"]
            policy_path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")
        else:
            candidate["policies"][0]["requires"] = ["failed-runs"]
        result = validate_policy_bundle(package, candidate, config, None)
        assert expected in diagnostic_codes(result), name


def test_policy_integrity_rejects_missing_requires_before_cycle_detection(
    tmp_path: Path,
) -> None:
    package = tmp_path / "missing-requires"
    shutil.copytree(ROOT / "process", package)
    manifest = load_yaml(package / "policies" / "manifest.yaml")
    config = load_yaml(FIXTURES / "config" / "valid-central.yaml")
    policy_path = package / "policies" / "classification.yaml"
    policy = load_yaml(policy_path)
    policy["rules"].append({
        "id": "classification.additional-check",
        "override_mode": "replaceable",
        "value": True,
        "requires": ["missing.rule"],
    })
    policy_path.write_text(yaml.safe_dump(policy, sort_keys=False), encoding="utf-8")

    result = validate_policy_bundle(package, manifest, config, None)

    assert "policy.reference-missing" in diagnostic_codes(result)
    assert "policy.requirement-cycle" not in diagnostic_codes(result)
