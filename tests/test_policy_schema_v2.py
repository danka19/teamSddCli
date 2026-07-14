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

    for item in manifest["policies"]:
        policy = load_yaml(ROOT / "process" / item["path"])
        policy["rules"] = policy["rules"][1:]

        assert errors("policy-document.schema.json", policy), item["kind"]


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
