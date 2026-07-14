"""Scenario-first evidence for the Phase 2.1 process package skeleton.

This module deliberately keeps schema loading, referential checks, and the
bounded sensitive-value scan in tests. Production discovery and diagnostics
belong to work item 2.2.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator


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
    "release": "release-manifest.schema.json",
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


def schema_errors(name: str, data: dict[str, Any]) -> list[str]:
    return [error.message for error in Draft202012Validator(load_schema(name)).iter_errors(data)]


def local_refs(value: Any) -> list[str]:
    if isinstance(value, dict):
        refs = [value["$ref"]] if isinstance(value.get("$ref"), str) else []
        return refs + [ref for child in value.values() for ref in local_refs(child)]
    if isinstance(value, list):
        return [ref for child in value for ref in local_refs(child)]
    return []


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
        for reference in local_refs(schema):
            assert "://" not in reference, f"{filename} has network reference {reference}"
            target = (SCHEMA_ROOT / reference.split("#", 1)[0]).resolve()
            assert target.is_file(), f"{filename} has unresolved local reference {reference}"


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

    stage_ids = {stage["id"] for stage in workflow["workflow"]["stages"]}
    for stage in workflow["workflow"]["stages"]:
        assert set(stage["requires"]) <= stage_ids

    for registry_path in config["registries"].values():
        assert (TEAM_SPECS / registry_path).is_file()
    for root_path in config["canonical_paths"].values():
        assert (TEAM_SPECS / root_path).is_dir()

    assert referential_errors(config, projects, owners, adapter) == []


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


@pytest.mark.parametrize(
    ("schema_name", "relative_path"),
    [
        ("package", "missing-package-version/package.yaml"),
        ("config", "missing-config-version/sdd.config.yaml"),
        ("projects", "invalid-schema/projects.yaml"),
    ],
)
def test_invalid_schema_fixtures_fail_stably(schema_name: str, relative_path: str) -> None:
    fixture = load_yaml(FIXTURES / "invalid" / relative_path)
    assert schema_errors(schema_name, fixture), f"schema: {relative_path} unexpectedly validated"


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
