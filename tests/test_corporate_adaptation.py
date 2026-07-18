"""Scenario-first tests for Phase 2 work item 2.13 corporate adaptation."""

from __future__ import annotations

import json
import copy
import os
import shutil
import subprocess
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from process.validators.config_validation import secret_diagnostics


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
FIXTURES = ROOT / "tests" / "fixtures" / "corporate-adaptation"


def load_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def schema_errors(schema_name: str, document: dict[str, object]) -> list[str]:
    schema = json.loads(
        (PROCESS / "schemas" / schema_name).read_text(encoding="utf-8")
    )
    return [
        error.message
        for error in Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(document)
    ]


def test_environment_inventory_template_covers_required_corporate_inputs() -> None:
    template = load_yaml(
        PROCESS / "templates" / "corporate-adaptation" / "environment-inventory.yaml"
    )

    assert schema_errors("corporate-environment-inventory.schema.json", template) == []
    assert set(template["inventory"]) == {
        "host",
        "runtimes",
        "tools",
        "package_distribution",
        "network_policy",
        "integrations",
        "mcp",
        "ai",
    }
    assert set(template["inventory"]["integrations"]) == {
        "bitbucket",
        "jenkins",
        "jira",
        "confluence",
    }


def test_environment_inventory_rejects_missing_mcp_section() -> None:
    invalid = load_yaml(
        FIXTURES / "invalid" / "environment-inventory-missing-mcp.yaml"
    )

    errors = schema_errors("corporate-environment-inventory.schema.json", invalid)

    assert any("mcp" in error for error in errors)


def test_environment_inventory_requires_every_leaf_and_complete_valid_fixture() -> None:
    valid = load_yaml(FIXTURES / "valid" / "environment-inventory.yaml")
    assert schema_errors("corporate-environment-inventory.schema.json", valid) == []

    required_leaves = {
        "host": "shells",
        "runtimes": "node",
        "tools": "openspec",
        "package_distribution": "integrity_verification",
        "network_policy": "proxy_tls",
        "mcp": "available_servers",
        "ai": "available_models",
    }
    for section, leaf in required_leaves.items():
        incomplete = copy.deepcopy(valid)
        del incomplete["inventory"][section][leaf]
        assert schema_errors(
            "corporate-environment-inventory.schema.json", incomplete
        ), (section, leaf)


def test_environment_inventory_enforces_fact_states_and_timestamp_format() -> None:
    valid = load_yaml(FIXTURES / "valid" / "environment-inventory.yaml")
    candidates = []

    unresolved_with_value = copy.deepcopy(valid)
    unresolved_with_value["inventory"]["tools"]["git"] = {
        "status": "unresolved",
        "value": "guessed-version",
        "evidence_refs": [],
        "notes": "Not verified.",
    }
    candidates.append(unresolved_with_value)

    verified_without_value = copy.deepcopy(valid)
    verified_without_value["inventory"]["tools"]["git"]["value"] = None
    candidates.append(verified_without_value)

    not_applicable_with_value = copy.deepcopy(valid)
    not_applicable_with_value["inventory"]["ai"]["available_models"] = {
        "status": "not-applicable",
        "value": ["guessed-model"],
        "evidence_refs": [],
        "notes": "AI is unavailable.",
    }
    candidates.append(not_applicable_with_value)

    invalid_timestamp = copy.deepcopy(valid)
    invalid_timestamp["metadata"]["collected_at"] = "not-a-timestamp"
    candidates.append(invalid_timestamp)

    for candidate in candidates:
        assert schema_errors(
            "corporate-environment-inventory.schema.json", candidate
        )


def test_configuration_and_pilot_entry_templates_require_safety_checks() -> None:
    configuration = load_yaml(
        PROCESS / "templates" / "corporate-adaptation" / "configuration-checklist.yaml"
    )
    pilot_entry = load_yaml(
        PROCESS / "templates" / "corporate-adaptation" / "pilot-entry-checklist.yaml"
    )

    assert schema_errors("corporate-adaptation-checklist.schema.json", configuration) == []
    assert schema_errors("corporate-adaptation-checklist.schema.json", pilot_entry) == []
    assert set(configuration["checks"]) == {
        "installed_package",
        "project_mappings",
        "owner_mappings",
        "secret_references",
        "integration_wiring",
        "rollback_path",
        "ai_disabled_fallback",
        "unresolved_inputs",
    }
    assert set(pilot_entry["checks"]) == {
        "external_release_acceptance",
        "environment_inventory",
        "configuration",
        "pilot_candidate",
        "human_owners",
        "deterministic_gates",
        "ai_disabled_gates",
        "privacy_controls",
        "rollback_or_hold",
        "entry_decision",
    }


def test_populated_green_checklists_validate_required_pilot_entry_evidence() -> None:
    from process.corporate_adaptation import validate_document

    configuration = load_yaml(FIXTURES / "valid" / "configuration-checklist.yaml")
    pilot_entry = load_yaml(FIXTURES / "valid" / "pilot-entry-checklist.yaml")

    for document in (configuration, pilot_entry):
        assert schema_errors("corporate-adaptation-checklist.schema.json", document) == []
        assert diagnostic_codes(validate_document(document, document["kind"], PROCESS)) == []


def test_checklist_schema_rejects_false_green_and_missing_evaluation_identity() -> None:
    pilot_entry = load_yaml(FIXTURES / "valid" / "pilot-entry-checklist.yaml")
    false_green = copy.deepcopy(pilot_entry)
    false_green["checks"]["external_release_acceptance"] = {
        "status": "failed",
        "evidence_refs": [],
        "notes": "Synthetic acceptance failure.",
    }
    missing_identity = copy.deepcopy(pilot_entry)
    missing_identity["evaluated_at"] = None
    missing_identity["evaluated_by_role"] = None

    for candidate in (false_green, missing_identity):
        assert schema_errors("corporate-adaptation-checklist.schema.json", candidate)


def test_checklist_rejects_missing_fallback_and_inline_secret() -> None:
    missing = load_yaml(
        FIXTURES / "invalid" / "pilot-entry-missing-fallback.yaml"
    )
    inline = load_yaml(
        FIXTURES / "invalid" / "configuration-inline-secret.yaml"
    )

    assert any(
        "ai_disabled_gates" in error
        for error in schema_errors("corporate-adaptation-checklist.schema.json", missing)
    )
    assert schema_errors("corporate-adaptation-checklist.schema.json", inline) == []
    assert secret_diagnostics(inline, "configuration-checklist")


def test_pilot_evidence_template_and_synthetic_example_cover_full_audit_path() -> None:
    from process.corporate_adaptation import validate_document

    template = load_yaml(
        PROCESS / "templates" / "corporate-adaptation" / "pilot-evidence.yaml"
    )
    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )

    assert schema_errors("corporate-pilot-evidence.schema.json", template) == []
    assert schema_errors("corporate-pilot-evidence.schema.json", example) == []
    assert example["evidence_kind"] == "synthetic-example"
    assert set(example["gates"]) == {
        "definition_of_ready",
        "implementation_complete",
        "definition_of_done",
        "release_or_transfer",
        "archive_readiness",
    }
    assert example["human_decisions"]
    assert example["traceability"]["requirement_ids"]
    assert example["traceability"]["scenario_ids"]
    assert example["selection"]["change_id"]
    assert example["selection"]["class_rationale"]
    assert example["installed_state"]["release_id"]
    assert example["installed_state"]["runtime_versions"]
    assert example["installed_state"]["adapter_versions"]
    assert example["delivery"]["pr_refs"]
    assert example["delivery"]["test_refs"]
    assert example["failed_attempts"]
    assert example["interventions"]
    assert example["deviations"]
    assert example["privacy"]["storage_ref"]
    assert example["rollback_or_hold"]["evidence_refs"]
    assert example["follow_up_changes"]
    assert diagnostic_codes(validate_document(example, "pilot-evidence", PROCESS, external_package=True)) == []


def test_pilot_evidence_rejects_missing_human_decisions() -> None:
    invalid = load_yaml(
        FIXTURES / "invalid" / "pilot-evidence-missing-human-decisions.yaml"
    )

    errors = schema_errors("corporate-pilot-evidence.schema.json", invalid)

    assert any("human_decisions" in error for error in errors)


def test_pilot_evidence_rejects_false_pass_and_dangling_decision_refs() -> None:
    from process.corporate_adaptation import validate_document

    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )
    false_pass = copy.deepcopy(example)
    false_pass["installed_state"]["release_id"] = None
    false_pass["gates"]["definition_of_done"] = {
        "status": "not-evaluated",
        "evidence_refs": [],
        "decision_ref": None,
        "notes": None,
    }
    dangling = copy.deepcopy(example)
    dangling["gates"]["definition_of_ready"]["decision_ref"] = "decision:missing"

    assert schema_errors("corporate-pilot-evidence.schema.json", false_pass)
    assert "adaptation.decision-ref-missing" in diagnostic_codes(
        validate_document(dangling, "pilot-evidence", PROCESS)
    )


def test_pilot_gate_states_require_evidence_or_disposition() -> None:
    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )
    invalid = copy.deepcopy(example)
    invalid["gates"]["definition_of_ready"]["evidence_refs"] = []

    assert schema_errors("corporate-pilot-evidence.schema.json", invalid)


def diagnostic_codes(result: object) -> list[str]:
    return [item.code for item in result.diagnostics]


def test_no_fork_contract_routes_reusable_findings_to_external_openspec() -> None:
    from process.corporate_adaptation import validate_document

    template = load_yaml(
        PROCESS / "templates" / "corporate-adaptation" / "no-fork-assessment.yaml"
    )
    routed = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "no-fork-routed-synthetic.yaml"
    )
    invalid = load_yaml(
        FIXTURES / "invalid" / "no-fork-internal-reusable-change.yaml"
    )

    assert diagnostic_codes(validate_document(template, "no-fork-assessment", PROCESS, external_package=True)) == []
    assert diagnostic_codes(validate_document(routed, "no-fork-assessment", PROCESS, external_package=True)) == []
    assert "adaptation.schema-invalid" in diagnostic_codes(
        validate_document(invalid, "no-fork-assessment", PROCESS, external_package=True)
    )
    assert "adaptation.internal-fork-detected" in diagnostic_codes(
        validate_document(invalid, "no-fork-assessment", PROCESS, external_package=True)
    )


def test_external_package_privacy_scan_rejects_private_values_and_secrets() -> None:
    from process.corporate_adaptation import validate_document

    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )
    private = copy.deepcopy(example)
    private["installed_state"]["mcp_wiring_ref"] = "https://jira.internal.corp/secret"
    secret = copy.deepcopy(example)
    secret["api_key"] = "ghp_abcdefghijklmnopqrstuvwxyz123456"

    assert "adaptation.private-value" in diagnostic_codes(
        validate_document(private, "pilot-evidence", PROCESS, external_package=True)
    )
    assert "secret.inline-credential" in diagnostic_codes(
        validate_document(secret, "pilot-evidence", PROCESS, external_package=True)
    )


def test_green_checklist_fails_closed_when_any_required_check_is_unresolved() -> None:
    from process.corporate_adaptation import validate_document

    checklist = load_yaml(FIXTURES / "valid" / "pilot-entry-checklist.yaml")
    checklist["checks"]["ai_disabled_gates"] = {
        "status": "unresolved",
        "evidence_refs": [],
        "notes": "Synthetic unresolved gate.",
    }

    assert "adaptation.green-checklist-incomplete" in diagnostic_codes(
        validate_document(checklist, "pilot-entry-checklist", PROCESS)
    )


def test_external_package_privacy_scan_rejects_common_private_value_forms() -> None:
    from process.corporate_adaptation import validate_document

    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )
    private_values = (
        "jira.internal.corp",
        "ACME-PROD-123",
        "10.1.2.3",
        "127.0.0.1",
        r"\\corpserver\secretshare\project",
        "/opt/corporate/private.yaml",
        "ssh://git.corp/team/private.git",
    )
    for private_value in private_values:
        candidate = copy.deepcopy(example)
        candidate["installed_state"]["mcp_wiring_ref"] = private_value
        assert "adaptation.private-value" in diagnostic_codes(
            validate_document(
                candidate, "pilot-evidence", PROCESS, external_package=True
            )
        ), private_value


def test_external_package_privacy_scan_rejects_ordinary_real_identifiers() -> None:
    from process.corporate_adaptation import validate_document

    example = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    )
    for private_value in ("JIRA-4821", "john.smith", "team-alpha/private-repo"):
        candidate = copy.deepcopy(example)
        candidate["installed_state"]["mcp_wiring_ref"] = private_value
        assert "adaptation.private-value" in diagnostic_codes(
            validate_document(candidate, "pilot-evidence", PROCESS, external_package=True)
        ), private_value


def test_no_fork_detection_is_derived_from_recorded_changes_and_findings() -> None:
    from process.corporate_adaptation import validate_document

    routed = load_yaml(
        PROCESS / "examples" / "corporate-adaptation" / "no-fork-routed-synthetic.yaml"
    )
    hidden_change = copy.deepcopy(routed)
    hidden_change["internal_process_package_changes"] = ["process/private-rule.py"]
    modified_finding = copy.deepcopy(routed)
    modified_finding["findings"].append({
        "finding_id": "hidden-adapter-fork",
        "scope": "thin-adapter",
        "description": "Synthetic hidden package modification.",
        "disposition": "thin-adapter",
        "external_change_ref": None,
        "internal_package_modified": True,
        "evidence_refs": ["evidence:synthetic-hidden-fork"],
    })

    for candidate in (hidden_change, modified_finding):
        assert schema_errors("corporate-no-fork-assessment.schema.json", candidate)
        assert "adaptation.internal-fork-detected" in diagnostic_codes(
            validate_document(candidate, "no-fork-assessment", PROCESS)
        )


def test_package_validation_and_cli_are_deterministic_and_non_mutating() -> None:
    from process.corporate_adaptation import validate_package_templates
    from scripts import validate_corporate_adaptation

    target = PROCESS / "examples" / "corporate-adaptation" / "pilot-evidence-synthetic.yaml"
    before = target.read_bytes()

    result = validate_package_templates(PROCESS)
    stdout: list[str] = []
    stderr: list[str] = []
    code = validate_corporate_adaptation.main(
        [str(target), "--external-package", "--json"],
        stdout=stdout.append,
        stderr=stderr.append,
    )

    assert diagnostic_codes(result) == []
    assert code == 0
    assert stderr == []
    assert json.loads(stdout[0]) == {
        "schema_version": "1.0",
        "status": "valid",
        "kind": "pilot-evidence",
        "diagnostics": [],
    }
    assert target.read_bytes() == before

    repeated: list[str] = []
    repeated_code = validate_corporate_adaptation.main(
        [str(target), "--kind", "pilot-evidence", "--external-package", "--json"],
        stdout=repeated.append,
        stderr=stderr.append,
    )
    assert repeated_code == 0
    assert repeated == stdout


def test_package_scan_rejects_extra_adaptation_documents(tmp_path: Path) -> None:
    from process.corporate_adaptation import validate_package_templates

    process_root = tmp_path / "process"
    shutil.copytree(PROCESS, process_root)
    extra = process_root / "templates" / "corporate-adaptation" / "private-extra.yaml"
    extra.write_text(
        "kind: pilot-evidence\nprivate_ref: ssh://git.corp/team/private.git\n",
        encoding="utf-8",
    )

    codes = diagnostic_codes(validate_package_templates(process_root))

    assert "adaptation.package-closure" in codes
    assert "adaptation.private-value" in codes


def test_package_scan_rejects_yml_extras_and_linked_ancestors(tmp_path: Path) -> None:
    from process.corporate_adaptation import validate_package_templates

    process_root = tmp_path / "process"
    shutil.copytree(PROCESS, process_root)
    extra = process_root / "examples" / "corporate-adaptation" / "private-extra.yml"
    extra.write_text(
        "kind: pilot-evidence\nmcp_wiring_ref: JIRA-4821\n",
        encoding="utf-8",
    )
    codes = diagnostic_codes(validate_package_templates(process_root))
    assert "adaptation.package-closure" in codes
    assert "adaptation.private-value" in codes

    extra.unlink()
    target = tmp_path / "linked-adaptation"
    shutil.move(str(process_root / "templates" / "corporate-adaptation"), target)
    try:
        os.symlink(target, process_root / "templates" / "corporate-adaptation", target_is_directory=True)
    except OSError:
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(process_root / "templates" / "corporate-adaptation"), str(target)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            pytest.skip("symlink and junction creation are unavailable")

    assert "adaptation.package-document-invalid" in diagnostic_codes(
        validate_package_templates(process_root)
    )


def test_cli_usage_and_operational_errors_remain_machine_readable_json() -> None:
    from scripts import validate_corporate_adaptation

    for args, expected_code, expected_diagnostic in (
        (["--json"], 2, "adaptation.usage"),
        (["missing.yaml", "--json"], 3, "adaptation.document-invalid"),
    ):
        stdout: list[str] = []
        stderr: list[str] = []
        code = validate_corporate_adaptation.main(
            args, stdout=stdout.append, stderr=stderr.append
        )
        assert code == expected_code
        assert stderr == []
        payload = json.loads(stdout[0])
        assert payload["diagnostics"][0]["code"] == expected_diagnostic


def test_process_package_registers_adaptation_contracts_and_public_cli() -> None:
    package = load_yaml(PROCESS / "package.yaml")
    allowlist = load_yaml(PROCESS / "release-allowlist.yaml")

    assert package["schemas"] | {
        "corporate_environment_inventory": "schemas/corporate-environment-inventory.schema.json",
        "corporate_adaptation_checklist": "schemas/corporate-adaptation-checklist.schema.json",
        "corporate_pilot_evidence": "schemas/corporate-pilot-evidence.schema.json",
        "corporate_no_fork_assessment": "schemas/corporate-no-fork-assessment.schema.json",
    } == package["schemas"]
    assert set(package["templates"].values()) >= {
        f"templates/corporate-adaptation/{name}"
        for name in (
            "environment-inventory.yaml",
            "configuration-checklist.yaml",
            "pilot-entry-checklist.yaml",
            "pilot-evidence.yaml",
            "no-fork-assessment.yaml",
        )
    }
    assert {value for value in package["examples"].values() if isinstance(value, str)} >= {
        "examples/corporate-adaptation/pilot-evidence-synthetic.yaml",
        "examples/corporate-adaptation/no-fork-routed-synthetic.yaml",
    }
    assert "corporate_adaptation.py" in package["distribution"]["files"]
    assert "CORPORATE_ADAPTATION_AND_PILOT.md" in allowlist["runbooks"]
    assert "validate_corporate_adaptation.py" in {
        item["name"] for item in allowlist["entry_points"]
    }


SCENARIO_COVERAGE = {
    "test_environment_inventory_template_covers_required_corporate_inputs": [
        {
            "capability": "transfer-readiness",
            "requirement": "Corporate adaptation boundary",
            "scenario": "Unknown environment facts remain explicit",
            "source_kind": "delta",
        }
    ],
    "test_populated_green_checklists_validate_required_pilot_entry_evidence": [
        {
            "capability": "transfer-readiness",
            "requirement": "Corporate pilot entry and acceptance",
            "scenario": "Pilot entry checks the real environment",
            "source_kind": "delta",
        }
    ],
    "test_pilot_evidence_template_and_synthetic_example_cover_full_audit_path": [
        {
            "capability": "transfer-readiness",
            "requirement": "Release evidence and auditability",
            "scenario": "Pilot evidence identifies installed state",
            "source_kind": "delta",
        },
        {
            "capability": "transfer-readiness",
            "requirement": "Corporate pilot entry and acceptance",
            "scenario": "Pilot executes one selected real governed change",
            "source_kind": "delta",
        },
    ],
    "test_no_fork_contract_routes_reusable_findings_to_external_openspec": [
        {
            "capability": "transfer-readiness",
            "requirement": "Corporate adaptation boundary",
            "scenario": "Corporate environment is not the primary development surface",
            "source_kind": "delta",
        }
    ],
}
