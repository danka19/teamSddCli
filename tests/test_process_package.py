"""Scenario-first evidence for the Phase 2.1 process package skeleton.

This module deliberately keeps schema loading, referential checks, and the
bounded sensitive-value scan in tests. Production discovery and diagnostics
belong to work item 2.2.
"""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from process.certification import FIXTURE_PRIVATE


REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESS_ROOT = REPO_ROOT / "process"
SCHEMA_ROOT = PROCESS_ROOT / "schemas"
TEAM_SPECS = REPO_ROOT / "templates" / "team-specs"
PROJECT_ADAPTER = REPO_ROOT / "templates" / "project-adapter" / ".sdd-project.yaml"
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "process-package"

SCHEMA_FILES = {
    "package": "process-package.schema.json",
    "workflow": "workflow.schema.json",
    "config": "sdd-config.schema.json",
    "projects": "projects.schema.json",
    "owners": "owners.schema.json",
    "adapter": "project-adapter.schema.json",
    "reference": "reference.schema.json",
    "release": "release-manifest.schema.json",
    "release_allowlist": "release-allowlist.schema.json",
    "release_certification_selection": "release-certification-selection.schema.json",
    "release_host_evidence": "release-host-evidence.schema.json",
    "change_v2": "change-v2.schema.json",
    "policy_manifest": "policy-manifest.schema.json",
    "policy_document": "policy-document.schema.json",
    "gate_evaluation_input": "gate-evaluation-input.schema.json",
    "tech_lead_review_input": "tech-lead-review-input.schema.json",
    "tech_lead_control_record": "tech-lead-control-record.schema.json",
    "corporate_flow_input": "corporate-flow-input.schema.json",
    "traceability_v2": "traceability-v2.schema.json",
    "external_mapping": "external-mapping.schema.json",
    "operation_evidence": "operation-evidence.schema.json",
    "read_pack_request": "read-pack-request.schema.json",
    "task_launch": "task-launch.schema.json",
    "weak_model_operation_plan": "weak-model-operation-plan.schema.json",
    "read_pack": "read-pack.schema.json",
    "weak_model_operation_evidence": "weak-model-operation-evidence.schema.json",
    "parallel_plan": "parallel-plan.schema.json",
    "certification_case": "certification-case.schema.json",
    "certification_evidence": "certification-evidence.schema.json",
    "coverage_report": "coverage-report.schema.json",
    "feedback_policy": "feedback-policy.schema.json",
    "role_output_fixture": "role-output-fixture.schema.json",
    "actual_certification_operational_result": "actual-certification-operational-result.schema.json",
    "corporate_environment_inventory": "corporate-environment-inventory.schema.json",
    "corporate_adaptation_checklist": "corporate-adaptation-checklist.schema.json",
    "corporate_pilot_evidence": "corporate-pilot-evidence.schema.json",
    "corporate_no_fork_assessment": "corporate-no-fork-assessment.schema.json",
}

SENSITIVE_PATTERNS = {
    "secret/private": re.compile(
        r"(?im)(password|api[_-]?key|access[_-]?token|private[_-]?key)\s*:|"
        r"C:\\Users\\|/Users/[^/\s]+/|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    ),
    "production": re.compile(
        r"(?im)https?://|ssh://|git@|\b(?:prod|production|corp|internal)\b"
    ),
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} must contain a YAML mapping"
    return data


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_ROOT / SCHEMA_FILES[name]).read_text(encoding="utf-8"))


def schema_errors(name: str, data: dict[str, Any]) -> list[ValidationError]:
    registry = Registry()
    for schema_path in SCHEMA_ROOT.glob("*.json"):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        registry = registry.with_resource(
            schema_path.name,
            Resource.from_contents(schema, default_specification=DRAFT202012),
        )
    return list(
        Draft202012Validator(load_schema(name), registry=registry).iter_errors(data)
    )


def local_refs(value: Any) -> list[str]:
    if isinstance(value, dict):
        refs = [value["$ref"]] if isinstance(value.get("$ref"), str) else []
        return refs + [ref for child in value.values() for ref in local_refs(child)]
    if isinstance(value, list):
        return [ref for child in value for ref in local_refs(child)]
    return []


def assert_local_references_resolve(filename: str, schema: dict[str, Any]) -> None:
    for reference in local_refs(schema):
        assert "://" not in reference, f"{filename} has network reference {reference}"
        relative_path, separator, fragment = reference.partition("#")
        target_schema = schema
        if relative_path:
            target = (SCHEMA_ROOT / relative_path).resolve()
            assert target.is_file(), f"{filename} has unresolved local reference {reference}"
            target_schema = json.loads(target.read_text(encoding="utf-8"))
        if separator:
            resource = Resource.from_contents(
                target_schema,
                default_specification=DRAFT202012,
            )
            Registry().resolver_with_root(resource).lookup(f"#{fragment}")


def referential_errors(
    config: dict[str, Any],
    projects: dict[str, Any],
    owners: dict[str, Any],
    adapter: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    project_ids = {project["id"] for project in projects["projects"]}
    zone_ids = {zone["id"] for zone in owners["zones"]}
    owner_group_ids = {group["id"] for group in owners["owner_groups"]}

    for project in projects["projects"]:
        for zone_id in project["owner_zones"]:
            if zone_id not in zone_ids:
                errors.append(f"reference: project {project['id']} uses unknown owner zone {zone_id}")

    for zone in owners["zones"]:
        for group_id in zone["owner_groups"]:
            if group_id not in owner_group_ids:
                errors.append(f"reference: zone {zone['id']} uses unknown owner group {group_id}")

    for group_id in owners["default_owner_groups"]:
        if group_id not in owner_group_ids:
            errors.append(f"reference: defaults use unknown owner group {group_id}")

    if adapter["project_id"] not in project_ids:
        errors.append(f"reference: adapter uses unknown project {adapter['project_id']}")
    central_package = {
        key: config["process_package"][key] for key in ("id", "version")
    }
    if adapter["process_package"] != central_package:
        errors.append("reference: adapter and central config consume different process packages")
    return errors


def scan_categories(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return {category for category, pattern in SENSITIVE_PATTERNS.items() if pattern.search(text)}


def yaml_files(root: Path) -> list[Path]:
    return sorted([*root.rglob("*.yaml"), *root.rglob("*.yml")])


def test_package_schemas_are_valid_and_use_only_local_references() -> None:
    assert set(path.name for path in SCHEMA_ROOT.glob("*.json")) == set(SCHEMA_FILES.values())

    for schema_name, filename in SCHEMA_FILES.items():
        schema = load_schema(schema_name)
        Draft202012Validator.check_schema(schema)
        assert_local_references_resolve(filename, schema)


def test_fragment_only_reference_resolves_within_current_schema() -> None:
    schema = {"$defs": {"identifier": {"type": "string"}}, "$ref": "#/$defs/identifier"}
    Draft202012Validator.check_schema(schema)
    assert_local_references_resolve("inline schema", schema)


def test_workflow_contract_declares_packaged_flow_dependencies_without_owning_policy() -> None:
    workflow = load_yaml(PROCESS_ROOT / "workflow.yaml")["workflow"]

    assert set(workflow) == {"id", "topology", "artifact_dependencies"}
    dependencies = {
        row["id"]: set(row["requires"])
        for row in workflow["artifact_dependencies"]
    }
    assert dependencies == {
        "change": set(),
        "classification": {"change"},
        "spec-pr-preparation": {"classification"},
        "readiness-gates": {"spec-pr-preparation"},
        "control-evidence": {"readiness-gates"},
        "release-evidence": {"control-evidence"},
        "traceability": {"classification", "readiness-gates", "control-evidence", "release-evidence"},
        "archive-preparation": {"traceability", "release-evidence"},
    }
    workflow_text = json.dumps(workflow).lower()
    for frozen_term in ("stages", "minor", "major", "hotfix", "approval", "threshold"):
        assert frozen_term not in workflow_text


def test_repository_reference_shape_is_shared_and_accepts_supported_forms() -> None:
    expected_ref = "reference.schema.json#/$defs/repositoryReference"
    projects_schema = load_schema("projects")
    adapter_schema = load_schema("adapter")
    assert (
        projects_schema["properties"]["projects"]["items"]["properties"]["repository"]
        ["properties"]["reference"]["$ref"]
        == expected_ref
    )
    assert (
        adapter_schema["properties"]["team_specs"]["properties"]["reference"]["$ref"]
        == expected_ref
    )

    references = load_yaml(FIXTURES / "valid" / "repository-references.yaml")["references"]
    references.extend(
        [
            "registry:prod-services",
            "sibling:private-tools",
            "path:departments/internal-tools",
        ]
    )
    projects = load_yaml(TEAM_SPECS / "projects.yaml")
    adapter = load_yaml(PROJECT_ADAPTER)
    for reference in references:
        candidate_projects = copy.deepcopy(projects)
        candidate_projects["projects"][0]["repository"]["reference"] = reference
        assert schema_errors("projects", candidate_projects) == []

        candidate_adapter = copy.deepcopy(adapter)
        candidate_adapter["team_specs"]["reference"] = reference
        assert schema_errors("adapter", candidate_adapter) == []

    assert scan_categories(TEAM_SPECS / "projects.yaml") == set()
    assert scan_categories(PROJECT_ADAPTER) == set()


def test_unsafe_repository_reference_fixtures_fail_at_reference_field() -> None:
    references = load_yaml(
        FIXTURES / "invalid" / "unsafe-references" / "references.yaml"
    )["references"]
    projects = load_yaml(TEAM_SPECS / "projects.yaml")
    adapter = load_yaml(PROJECT_ADAPTER)
    for reference in references:
        candidate_projects = copy.deepcopy(projects)
        candidate_projects["projects"][0]["repository"]["reference"] = reference
        project_errors = schema_errors("projects", candidate_projects)
        assert any(
            error.validator == "oneOf"
            and list(error.absolute_path) == ["projects", 0, "repository", "reference"]
            for error in project_errors
        ), f"unsafe project reference unexpectedly validated: {reference}"

        candidate_adapter = copy.deepcopy(adapter)
        candidate_adapter["team_specs"]["reference"] = reference
        adapter_errors = schema_errors("adapter", candidate_adapter)
        assert any(
            error.validator == "oneOf"
            and list(error.absolute_path) == ["team_specs", "reference"]
            for error in adapter_errors
        ), f"unsafe adapter reference unexpectedly validated: {reference}"


def test_release_manifest_base_contract_covers_accepted_transfer_evidence() -> None:
    release = load_yaml(FIXTURES / "valid" / "release-manifest.yaml")
    assert {
        "payload_sha256",
        "inventory",
        "allowlist_sha256",
        "host_evidence",
        "compatibility",
        "verification",
        "raw_artifacts",
        "weak_model_certification",
        "known_limitations",
        "rollback_reference",
    } <= set(release)
    hosts = release["host_evidence"]
    assert hosts == [
        {"platform_id": "windows", "evidence_level": "full-clean-rehearsal"},
        {"platform_id": "linux-wsl2", "evidence_level": "portability-smoke"},
        {"platform_id": "macos", "evidence_level": "not-certified"},
    ]
    assert {"python", "node", "git", "openspec", "mcp", "shells", "packages"} == set(
        release["compatibility"]
    )
    package_versions = {
        package["name"]: package["version"]
        for package in release["compatibility"]["packages"]
    }
    pinned_lines = (REPO_ROOT / "requirements-test.txt").read_text(
        encoding="utf-8"
    ).splitlines()
    pinned_packages = dict(
        line.split("==", 1)
        for line in pinned_lines if line
    )
    assert package_versions == pinned_packages
    for asset in release["inventory"]:
        assert {"path", "size", "sha256"} <= set(asset)
        assert re.fullmatch(r"[0-9a-f]{64}", asset["sha256"])
    assert release["verification"]["commands"]
    assert release["verification"]["evidence_requirements"]
    for artifact in release["raw_artifacts"]:
        assert re.fullmatch(r"[0-9a-f]{64}", artifact["sha256"])
    assert {"qwen", "deepseek"} == {
        certification["model_family"]
        for certification in release["weak_model_certification"]
    }


def test_incomplete_release_manifest_fails_for_new_mandatory_sections() -> None:
    fixture = load_yaml(
        FIXTURES / "invalid" / "incomplete-release-manifest" / "release-manifest.yaml"
    )
    errors = schema_errors("release", fixture)
    for field in ("inventory", "host_evidence", "verification", "raw_artifacts", "weak_model_certification"):
        assert any(
            error.validator == "required"
            and list(error.absolute_path) == []
            and f"'{field}' is a required property" == error.message
            for error in errors
        ), f"release manifest did not require {field}: {errors}"

    assert any(error.validator == "required" and "'compatibility' is a required property" == error.message for error in errors)


def test_synthetic_central_topology_is_coherent() -> None:
    package = load_yaml(PROCESS_ROOT / "package.yaml")
    workflow = load_yaml(PROCESS_ROOT / "workflow.yaml")
    config = load_yaml(TEAM_SPECS / "sdd.config.yaml")
    projects = load_yaml(TEAM_SPECS / "projects.yaml")
    owners = load_yaml(TEAM_SPECS / "owners.yaml")
    adapter = load_yaml(PROJECT_ADAPTER)
    release = load_yaml(FIXTURES / "valid" / "release-manifest.yaml")

    for schema_name, document in (
        ("package", package),
        ("workflow", workflow),
        ("config", config),
        ("projects", projects),
        ("owners", owners),
        ("adapter", adapter),
        ("release", release),
    ):
        assert schema_errors(schema_name, document) == []

    version = (PROCESS_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version == package["package"]["version"] == config["process_package"]["version"]
    assert version == adapter["process_package"]["version"] == release["process_package"]["version"]
    assert adapter["config_schema_version"] == config["config_schema_version"]
    assert package["openspec"]["cli_version"] == config["openspec"]["cli_version"] == "1.4.1"

    assert (PROCESS_ROOT / package["workflow"]).is_file()
    assert (TEAM_SPECS / config["process_package"]["location"]).resolve() == PROCESS_ROOT.resolve()
    for schema_path in package["schemas"].values():
        assert (PROCESS_ROOT / schema_path).is_file()
    for source_path in package["canonical_sources"]:
        assert (REPO_ROOT / source_path).is_file()
    for source_path in workflow["canonical_sources"]:
        assert (REPO_ROOT / source_path).is_file()

    operational_schema = load_schema(
        "actual_certification_operational_result"
    )
    operational_result = {
        "schema_version": "1.0",
        "evidence_kind": "actual-model-operational-result",
        "status": "blocked",
        "actual_model_run": False,
        "phase": "preflight",
        "diagnostic": "actual-model.runtime-failure",
        "adapter": {"family": "qwen-class", "version": "2.1"},
    }
    assert list(
        Draft202012Validator(operational_schema).iter_errors(
            operational_result
        )
    ) == []
    assert list(
        Draft202012Validator(operational_schema).iter_errors(
            {**operational_result, "unexpected": True}
        )
    )

    repo_paths = {path.relative_to(REPO_ROOT).as_posix() for path in REPO_ROOT.rglob("*")}
    manifest_paths = [asset["path"] for asset in release["inventory"]]
    manifest_paths.extend(
        evidence["path"] for evidence in release["weak_model_certification"]
    )
    manifest_paths.append(release["rollback_reference"])
    for manifest_path in manifest_paths:
        assert manifest_path in repo_paths, f"release manifest has unresolved path {manifest_path}"

    artifact_ids = {
        artifact["id"] for artifact in workflow["workflow"]["artifact_dependencies"]
    }
    for artifact in workflow["workflow"]["artifact_dependencies"]:
        assert set(artifact["requires"]) <= artifact_ids

    for registry_path in config["registries"].values():
        assert (TEAM_SPECS / registry_path).is_file()
    for root_path in config["canonical_paths"].values():
        assert (TEAM_SPECS / root_path).is_dir()

    assert referential_errors(config, projects, owners, adapter) == []


def test_central_specs_and_project_implementation_truth_stay_separate() -> None:
    config = load_yaml(TEAM_SPECS / "sdd.config.yaml")
    projects = load_yaml(TEAM_SPECS / "projects.yaml")
    adapter = load_yaml(PROJECT_ADAPTER)

    assert set(config["canonical_paths"]) == {
        "changes",
        "specs",
        "analytics",
        "traceability",
        "waivers",
        "evidence",
        "publication",
    }
    assert not {"code", "tests"} & set(config["canonical_paths"])
    assert projects["projects"][0]["repository"] == {"reference": "sibling:sample-app"}
    assert projects["projects"][0]["local_paths"] == {"code": "src", "tests": "tests"}
    assert adapter["local_paths"] == {"code": "src", "tests": "tests"}
    assert adapter["team_specs"] == {
        "reference": "sibling:team-specs",
        "config_path": "sdd.config.yaml",
    }
    assert not (TEAM_SPECS / "src").exists()
    assert not (TEAM_SPECS / "tests").exists()


def test_clean_templates_and_positive_fixtures_have_no_sensitive_values() -> None:
    files = [
        PROCESS_ROOT / "package.yaml",
        PROCESS_ROOT / "workflow.yaml",
        *yaml_files(TEAM_SPECS),
        PROJECT_ADAPTER,
        *yaml_files(FIXTURES / "valid"),
    ]
    assert files
    findings = {str(path.relative_to(REPO_ROOT)): scan_categories(path) for path in files}
    assert {path: categories for path, categories in findings.items() if categories} == {}


def test_certification_tree_sensitive_content_is_limited_to_named_negative_privacy_fixtures() -> None:
    def without_canonical_sources(value):
        if isinstance(value, dict):
            return {
                key: "<local-ollama-endpoint>"
                if key == "endpoint" and item == "http://127.0.0.1:11434"
                else without_canonical_sources(item)
                for key, item in value.items()
                if key not in {"canonical_sources", "sources", "source_definitions", "source_manifest"}
            }
        if isinstance(value, list):
            return [without_canonical_sources(item) for item in value]
        return value

    files = [path for path in yaml_files(PROCESS_ROOT / "certification") if path.name not in {"cases.yaml", "coverage.yaml", "evidence-manifest.yaml"}]
    findings = {
        path.relative_to(PROCESS_ROOT).as_posix()
        for path in files
        if FIXTURE_PRIVATE.search(yaml.safe_dump(without_canonical_sources(load_yaml(path))))
    }
    assert findings == {
        "certification/privacy-cases/corporate-identifier.yaml",
        "certification/privacy-cases/internal-identifier.yaml",
        "certification/privacy-cases/email.yaml",
        "certification/privacy-cases/url.yaml",
        "certification/privacy-cases/ip.yaml",
    }


@pytest.mark.parametrize(
    ("schema_name", "relative_path", "expected_validator", "expected_path"),
    [
        ("package", "missing-package-version/package.yaml", "required", ["package"]),
        ("config", "missing-config-version/sdd.config.yaml", "required", []),
        ("projects", "invalid-schema/projects.yaml", "type", ["projects"]),
    ],
)
def test_invalid_schema_fixtures_fail_stably(
    schema_name: str,
    relative_path: str,
    expected_validator: str,
    expected_path: list[str],
) -> None:
    fixture = load_yaml(FIXTURES / "invalid" / relative_path)
    errors = schema_errors(schema_name, fixture)
    assert any(
        error.validator == expected_validator and list(error.absolute_path) == expected_path
        for error in errors
    ), f"schema: {relative_path} did not fail with {expected_validator} at {expected_path}: {errors}"


def test_invalid_cross_file_reference_fails_stably() -> None:
    config = load_yaml(TEAM_SPECS / "sdd.config.yaml")
    projects = load_yaml(FIXTURES / "invalid" / "invalid-reference" / "projects.yaml")
    owners = load_yaml(TEAM_SPECS / "owners.yaml")
    adapter = load_yaml(PROJECT_ADAPTER)

    assert any(
        error.startswith("reference:")
        for error in referential_errors(config, projects, owners, adapter)
    )


@pytest.mark.parametrize(
    ("relative_path", "expected_category"),
    [
        ("secret-value/sdd.config.yaml", "secret/private"),
        ("production-value/projects.yaml", "production"),
    ],
)
def test_sensitive_negative_fixtures_fail_with_stable_category(
    relative_path: str, expected_category: str
) -> None:
    fixture = FIXTURES / "invalid" / relative_path
    assert expected_category in scan_categories(fixture)


SCENARIO_COVERAGE = {"test_central_specs_and_project_implementation_truth_stay_separate":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Repository content split","scenario":"Project repos own implementation truth"}],"test_synthetic_central_topology_is_coherent":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"First supported topology","scenario":"Central team-specs is the recommended first topology"},{"source_kind":"accepted","capability":"repo-topology-config","requirement":"OpenSpec version pin and upgrade policy","scenario":"OpenSpec version is pinned centrally"},{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Process configuration files","scenario":"Central config declares supported process assumptions"},{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Repository content split","scenario":"team-specs owns process and requirement truth"}],"test_workflow_contract_declares_packaged_flow_dependencies_without_owning_policy":[{"source_kind":"accepted","capability":"repo-topology-config","requirement":"Process package distribution","scenario":"Artifact dependencies are shared by skills and validators"}]}
