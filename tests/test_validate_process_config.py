"""Scenario-first tests for Phase 2 work item 2.2 config validation."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

import yaml
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_yaml(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def read_yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def build_central_layout(root: Path) -> Path:
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    shutil.copytree(REPO_ROOT / "process", root / "process")

    for relative in (
        "openspec/changes",
        "openspec/specs",
        "analytics",
        "traceability",
        "waivers",
        "evidence",
        "publication",
        "repos/product-internal-tools",
    ):
        (root / relative).mkdir(parents=True)

    write_yaml(
        root / "sdd.config.yaml",
        {
            "config_schema_version": "1.1",
            "topology": "central-team-specs",
            "process_package": {
                "id": "sdd-process",
                "version": "0.2.0",
                "location": "process",
            },
            "openspec": {"cli_version": "1.4.1"},
            "policy_set": {
                "id": "sdd-core",
                "version": "1.0.0",
                "corporate_values": {
                    "tech_lead_owner": "production-platform-team",
                    "qa_owner": "production-platform-team",
                    "escalation_route": "production-platform-team",
                    "evidence_retention_days": 30,
                },
                "overrides": [],
            },
            "canonical_paths": {
                "changes": "openspec/changes",
                "specs": "openspec/specs",
                "analytics": "analytics",
                "traceability": "traceability",
                "waivers": "waivers",
                "evidence": "evidence",
                "publication": "publication",
            },
            "registries": {"projects": "projects.yaml", "owners": "owners.yaml"},
            "validation": {"strict": True, "placeholders_allowed": False},
        },
    )
    write_yaml(
        root / "projects.yaml",
        {
            "schema_version": "1.0",
            "projects": [
                {
                    "id": "product-internal-tools",
                    "repository": {"reference": "path:repos/product-internal-tools"},
                    "adapter_allowed": True,
                    "owner_zones": ["private-product-zone"],
                    "local_paths": {"code": "src", "tests": "tests"},
                }
            ],
        },
    )
    write_yaml(
        root / "owners.yaml",
        {
            "schema_version": "1.0",
            "owner_groups": [
                {
                    "id": "production-platform-team",
                    "roles": ["tech_lead", "qa"],
                    "members": ["sample-user"],
                }
            ],
            "zones": [
                {
                    "id": "private-product-zone",
                    "paths": ["product-internal-tools/**"],
                    "owner_groups": ["production-platform-team"],
                }
            ],
            "default_owner_groups": ["production-platform-team"],
        },
    )
    return root


def build_adapter_layout(base: Path, reference_kind: str) -> tuple[Path, list[str]]:
    project = base / "sample-app"
    central = base / "team-specs"
    registry_args: list[str] = []

    if reference_kind == "path":
        central = project / "central"
        reference = "path:central"
    elif reference_kind == "registry":
        reference = "registry:central"
        registry_args = ["--registry", f"central={central}"]
    else:
        reference = "sibling:team-specs"

    build_central_layout(central)
    project.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(project)], check=True)

    projects = read_yaml(central / "projects.yaml")
    registered = projects["projects"]
    assert isinstance(registered, list)
    registered[0]["id"] = "sample-app"
    registered[0]["repository"]["reference"] = "path:repos/product-internal-tools"
    write_yaml(central / "projects.yaml", projects)

    write_yaml(
        project / ".sdd-project.yaml",
        {
            "schema_version": "1.1",
            "config_schema_version": "1.1",
            "project_id": "sample-app",
            "team_specs": {"reference": reference, "config_path": "sdd.config.yaml"},
            "process_package": {"id": "sdd-process", "version": "0.2.0"},
            "policy_set": {"id": "sdd-core", "version": "1.0.0", "overrides": []},
            "local_paths": {"code": "src", "tests": "tests"},
        },
    )
    return project, registry_args


def run_cli(
    args: list[str],
    probe: Callable[[], str],
) -> tuple[int, str, str]:
    from scripts import validate_process_config

    stdout: list[str] = []
    stderr: list[str] = []
    code = validate_process_config.main(
        args,
        runtime_probe=probe,
        stdout=stdout.append,
        stderr=stderr.append,
    )
    return code, "\n".join(stdout), "\n".join(stderr)


def test_valid_central_mode_reports_exact_compatibility_json(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")

    code, stdout, stderr = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 0
    assert stderr == ""
    payload = json.loads(stdout)
    assert set(payload) == {
        "schema_version",
        "status",
        "mode",
        "diagnostics",
        "compatibility",
    }
    assert payload["status"] == "valid"
    assert payload["mode"] == "central"
    assert payload["diagnostics"] == []
    assert payload["compatibility"] == {
        "config_schema_version": "1.1",
        "topology": "central-team-specs",
        "process_package": {"id": "sdd-process", "version": "0.2.0"},
        "policy_set": {"id": "sdd-core", "version": "1.0.0"},
        "openspec": {"required": "1.4.1", "runtime": "1.4.1"},
    }


def diagnostic_codes(stdout: str) -> list[str]:
    return [item["code"] for item in json.loads(stdout)["diagnostics"]]


def test_valid_adapter_modes_use_only_explicit_reference_resolution(tmp_path: Path) -> None:
    for reference_kind in ("sibling", "path", "registry"):
        project, registry_args = build_adapter_layout(tmp_path / reference_kind, reference_kind)
        code, stdout, stderr = run_cli(
            [str(project), "--json", *registry_args], lambda: "1.4.1"
        )
        assert (code, stderr) == (0, "")
        assert json.loads(stdout)["mode"] == "adapter"


def test_missing_and_ambiguous_discovery_fail_before_runtime_probe(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    calls = 0

    def probe() -> str:
        nonlocal calls
        calls += 1
        return "1.4.1"

    code, stdout, _ = run_cli([str(root), "--json"], probe)
    assert code == 1
    assert diagnostic_codes(stdout) == ["discovery.config-missing"]

    (root / "sdd.config.yaml").write_text("{}\n", encoding="utf-8")
    (root / ".sdd-project.yaml").write_text("{}\n", encoding="utf-8")
    code, stdout, _ = run_cli([str(root), "--json"], probe)
    assert code == 1
    assert diagnostic_codes(stdout) == ["discovery.config-ambiguous"]
    assert calls == 0


def test_missing_registry_and_unsafe_reference_are_stable(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path / "missing-map", "registry")
    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")
    assert code == 1
    assert "reference.registry-missing" in diagnostic_codes(stdout)

    project, _ = build_adapter_layout(tmp_path / "unsafe", "path")
    adapter = read_yaml(project / ".sdd-project.yaml")
    adapter["team_specs"]["reference"] = "path:../team-specs"
    write_yaml(project / ".sdd-project.yaml", adapter)
    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")
    assert code == 1
    assert "reference.invalid" in diagnostic_codes(stdout)


def test_windows_rooted_package_location_is_rejected_before_resolution(
    tmp_path: Path,
) -> None:
    root = build_central_layout(tmp_path / "central")
    _set_yaml(
        root / "sdd.config.yaml",
        ("process_package", "location"),
        r"\Users\private-account\process",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["package.location-invalid"]


def test_registry_symlink_cannot_escape_central_root(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")
    outside_directory = tmp_path / "outside"
    outside_directory.mkdir()
    shutil.copyfile(root / "projects.yaml", outside_directory / "projects.yaml")
    linked_directory = root / "linked"
    try:
        linked_directory.symlink_to(outside_directory, target_is_directory=True)
    except OSError as error:
        if os.name != "nt":
            pytest.skip(f"directory symlink creation is unavailable: {error}")
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(linked_directory), str(outside_directory)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            pytest.skip("directory symlink/junction creation is unavailable")
    _set_yaml(
        root / "sdd.config.yaml",
        ("registries", "projects"),
        "linked/projects.yaml",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["registry.path-unsafe"]


def test_adapter_rejects_ambiguous_resolved_central_root(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path, "sibling")
    central = tmp_path / "team-specs"
    (central / ".sdd-project.yaml").write_text("{}\n", encoding="utf-8")

    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["discovery.config-ambiguous"]


def test_schema_diagnostics_never_echo_an_absolute_reference(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path, "sibling")
    unsafe = "path:C:/Users/private-account/secret-repository"
    adapter = read_yaml(project / ".sdd-project.yaml")
    adapter["team_specs"]["reference"] = unsafe
    write_yaml(project / ".sdd-project.yaml", adapter)

    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")

    assert code == 1
    assert "reference.invalid" in diagnostic_codes(stdout)
    assert unsafe not in stdout
    assert "C:/Users/private-account" not in stdout


def test_invalid_owner_project_and_adapter_relations_are_reported(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path, "sibling")
    central = tmp_path / "team-specs"
    projects = read_yaml(central / "projects.yaml")
    projects["projects"][0]["owner_zones"] = ["missing-zone"]
    projects["projects"][0]["adapter_allowed"] = False
    write_yaml(central / "projects.yaml", projects)

    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")

    assert code == 1
    codes = diagnostic_codes(stdout)
    assert "integrity.project-owner-zone" in codes
    assert "integrity.adapter-not-allowed" in codes


def test_static_version_mismatches_prevent_runtime_probe(tmp_path: Path) -> None:
    mutations = {
        "config": lambda root: _set_yaml(
            root / "sdd.config.yaml", ("process_package", "version"), "9.9.9"
        ),
        "package": lambda root: _set_yaml(
            root / "process/package.yaml", ("package", "version"), "9.9.9"
        ),
        "version-file": lambda root: (root / "process/VERSION").write_text(
            "9.9.9\n", encoding="utf-8"
        ),
        "openspec": lambda root: _set_yaml(
            root / "sdd.config.yaml", ("openspec", "cli_version"), "9.9.9"
        ),
    }
    for name, mutate in mutations.items():
        root = build_central_layout(tmp_path / name)
        mutate(root)
        called = False

        def probe() -> str:
            nonlocal called
            called = True
            return "1.4.1"

        code, stdout, _ = run_cli([str(root), "--json"], probe)
        assert code == 1
        assert any(code.startswith("compat.") for code in diagnostic_codes(stdout))
        assert not called


def test_adapter_package_version_mismatch_is_explicit(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path, "sibling")
    _set_yaml(
        project / ".sdd-project.yaml", ("process_package", "version"), "9.9.9"
    )

    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")

    assert code == 1
    assert "compat.adapter-package-version" in diagnostic_codes(stdout)


def test_policy_weakening_has_human_json_parity_and_provenance(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")
    config = read_yaml(root / "sdd.config.yaml")
    config["policy_set"]["overrides"] = [
        {
            "rule_id": "classification.no-downgrade",
            "operation": "set",
            "value": False,
        }
    ]
    write_yaml(root / "sdd.config.yaml", config)

    json_code, json_stdout, json_stderr = run_cli(
        [str(root), "--json"], lambda: "1.4.1"
    )
    human_code, human_stdout, human_stderr = run_cli(
        [str(root)], lambda: "1.4.1"
    )

    assert json_code == human_code == 1
    assert json_stderr == human_stdout == ""
    assert diagnostic_codes(json_stdout) == ["policy.override-locked"]
    diagnostic = json.loads(json_stdout)["diagnostics"][0]
    assert diagnostic["source"] == "central-config"
    assert diagnostic["pointer"] == "/policy_set/overrides/0"
    assert "[policy.override-locked]" in human_stderr


def test_missing_corporate_policy_value_is_not_guessed(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")
    config = read_yaml(root / "sdd.config.yaml")
    del config["policy_set"]["corporate_values"]["qa_owner"]
    write_yaml(root / "sdd.config.yaml", config)

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["policy.corporate-value-missing"]
    assert json.loads(stdout)["diagnostics"][0]["pointer"].endswith("/qa_owner")


@pytest.mark.parametrize(
    "field",
    ("tech_lead_owner", "qa_owner", "escalation_route"),
)
def test_corporate_policy_owner_references_must_resolve_against_registry(
    tmp_path: Path,
    field: str,
) -> None:
    root = build_central_layout(tmp_path / field)
    config = read_yaml(root / "sdd.config.yaml")
    config["policy_set"]["corporate_values"][field] = "missing-owner-reference"
    write_yaml(root / "sdd.config.yaml", config)
    called = False

    def probe() -> str:
        nonlocal called
        called = True
        return "1.4.1"

    code, stdout, _ = run_cli([str(root), "--json"], probe)

    assert code == 1
    assert diagnostic_codes(stdout) == ["policy.corporate-owner-unresolved"]
    assert json.loads(stdout)["diagnostics"][0]["pointer"].endswith(f"/{field}")
    assert not called


def test_adapter_cannot_supply_arbitrary_policy_paths(tmp_path: Path) -> None:
    project, _ = build_adapter_layout(tmp_path, "sibling")
    adapter = read_yaml(project / ".sdd-project.yaml")
    adapter["policy_paths"] = ["sample/policy.yaml"]
    write_yaml(project / ".sdd-project.yaml", adapter)

    code, stdout, _ = run_cli([str(project), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["policy.adapter-path-forbidden"]


def _set_yaml(path: Path, keys: tuple[str, ...], value: object) -> None:
    data = read_yaml(path)
    target = data
    for key in keys[:-1]:
        target = target[key]
    target[keys[-1]] = value
    write_yaml(path, data)


def test_unsupported_topology_is_not_silently_accepted(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")
    _set_yaml(root / "sdd.config.yaml", ("topology",), "federated")

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert "compat.topology" in diagnostic_codes(stdout)


def test_malformed_and_duplicate_key_yaml_are_rejected(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "malformed")
    (root / "sdd.config.yaml").write_text("config_schema_version: [\n", encoding="utf-8")
    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")
    assert code == 1
    assert diagnostic_codes(stdout) == ["yaml.invalid"]

    root = build_central_layout(tmp_path / "duplicate")
    config_text = (root / "sdd.config.yaml").read_text(encoding="utf-8")
    (root / "sdd.config.yaml").write_text(
        "topology: central-team-specs\n" + config_text, encoding="utf-8"
    )
    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")
    assert code == 1
    assert diagnostic_codes(stdout) == ["yaml.duplicate-key"]


def test_runtime_is_checked_last_and_has_distinct_exit_codes(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")
    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.0")
    assert code == 1
    assert diagnostic_codes(stdout) == ["compat.openspec-runtime"]

    def unavailable() -> str:
        raise FileNotFoundError("openspec")

    code, stdout, _ = run_cli([str(root), "--json"], unavailable)
    assert code == 3
    assert diagnostic_codes(stdout) == ["runtime.openspec-unavailable"]


@pytest.mark.parametrize("runtime", ["1.4.1-beta.1", "1.4.1+corporate"])
def test_runtime_requires_exact_stable_openspec_version(
    tmp_path: Path, runtime: str
) -> None:
    root = build_central_layout(tmp_path / runtime.replace("+", "-"))

    code, stdout, _ = run_cli([str(root), "--json"], lambda: runtime)

    assert code == 1
    assert diagnostic_codes(stdout) == ["compat.openspec-runtime"]
    assert json.loads(stdout)["compatibility"]["openspec"]["runtime"] == runtime


@pytest.mark.parametrize("reference_keyword", ["$ref", "$dynamicRef"])
def test_package_schemas_reject_remote_reference_keywords(
    tmp_path: Path, reference_keyword: str
) -> None:
    root = build_central_layout(tmp_path / reference_keyword.removeprefix("$"))
    schema_path = root / "process" / "schemas" / "workflow.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["$defs"] = {
        "remote": {reference_keyword: "https://example.invalid/remote.schema.json"}
    }
    schema_path.write_text(json.dumps(schema), encoding="utf-8")

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["package.schema-invalid"]


@pytest.mark.parametrize("reference_keyword", ["$ref", "$dynamicRef"])
def test_package_schema_graph_rejects_indirect_remote_references(
    tmp_path: Path, reference_keyword: str
) -> None:
    root = build_central_layout(tmp_path / reference_keyword.removeprefix("$"))
    schema_root = root / "process" / "schemas"
    workflow_path = schema_root / "workflow.schema.json"
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    workflow["$defs"] = {"indirect": {"$ref": "auxiliary.schema.json"}}
    workflow_path.write_text(json.dumps(workflow), encoding="utf-8")
    (schema_root / "auxiliary.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                reference_keyword: "https://example.invalid/remote.schema.json",
            }
        ),
        encoding="utf-8",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["package.schema-invalid"]


@pytest.mark.parametrize("reference_keyword", ["$ref", "$dynamicRef"])
def test_package_schema_graph_rejects_relative_reference_under_remote_id(
    tmp_path: Path, reference_keyword: str
) -> None:
    root = build_central_layout(tmp_path / reference_keyword.removeprefix("$"))
    schema_root = root / "process" / "schemas"
    workflow_path = schema_root / "workflow.schema.json"
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    workflow["$defs"] = {
        "remote-base": {
            "$id": "https://example.invalid/base/",
            reference_keyword: "auxiliary.schema.json",
        }
    }
    workflow_path.write_text(json.dumps(workflow), encoding="utf-8")
    (schema_root / "auxiliary.schema.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema"}),
        encoding="utf-8",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["package.schema-invalid"]


@pytest.mark.parametrize("reference_keyword", ["$ref", "$dynamicRef"])
def test_package_schema_graph_resolves_reference_from_local_relative_id(
    tmp_path: Path, reference_keyword: str
) -> None:
    root = build_central_layout(tmp_path / reference_keyword.removeprefix("$"))
    schema_root = root / "process" / "schemas"
    workflow_path = schema_root / "workflow.schema.json"
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    workflow["$defs"] = {
        "local-base": {
            "$id": "nested/",
            reference_keyword: "auxiliary.schema.json",
        }
    }
    workflow_path.write_text(json.dumps(workflow), encoding="utf-8")
    nested = schema_root / "nested"
    nested.mkdir()
    (nested / "auxiliary.schema.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema"}),
        encoding="utf-8",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 0
    assert diagnostic_codes(stdout) == []


def test_package_schema_graph_stays_contained_and_handles_local_cycles(
    tmp_path: Path,
) -> None:
    root = build_central_layout(tmp_path / "cyclic-escape")
    schema_root = root / "process" / "schemas"
    workflow_path = schema_root / "workflow.schema.json"
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    workflow["$defs"] = {"cycle": {"$ref": "cycle-a.schema.json"}}
    workflow_path.write_text(json.dumps(workflow), encoding="utf-8")
    (schema_root / "cycle-a.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$ref": "cycle-b.schema.json",
            }
        ),
        encoding="utf-8",
    )
    (schema_root / "cycle-b.schema.json").write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$defs": {
                    "cycle": {"$ref": "cycle-a.schema.json"},
                    "escape": {"$ref": "../outside.schema.json"},
                },
            }
        ),
        encoding="utf-8",
    )
    (root / "process" / "outside.schema.json").write_text(
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema"}),
        encoding="utf-8",
    )

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert diagnostic_codes(stdout) == ["package.schema-invalid"]


def test_schema_validation_uses_injected_immutable_resources(
    tmp_path: Path, monkeypatch
) -> None:
    from process.validators import config_discovery, config_validation

    loader = getattr(config_discovery, "load_schema_resources", None)
    assert loader is not None, "schema resources must be loaded by the I/O boundary"
    resources = loader(REPO_ROOT / "process" / "schemas")
    with pytest.raises(TypeError):
        resources["new.schema.json"] = {}
    with pytest.raises(TypeError):
        resources["sdd-config.schema.json"]["type"] = "array"

    root = build_central_layout(tmp_path / "central")
    config = read_yaml(root / "sdd.config.yaml")

    def fail_on_validation_file_io(*args, **kwargs):
        raise AssertionError("pure schema validation attempted filesystem I/O")

    monkeypatch.setattr(Path, "read_text", fail_on_validation_file_io)
    diagnostics = config_validation.schema_diagnostics(
        "sdd-config.schema.json",
        config,
        "central-config",
        stage=4,
        schema_resources=resources,
    )

    assert diagnostics == []
    assert not hasattr(config_validation, "SCHEMA_ROOT")


def test_secret_diagnostics_are_redacted_and_human_json_codes_match(tmp_path: Path) -> None:
    token = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
    root = build_central_layout(tmp_path / "central")
    config = read_yaml(root / "sdd.config.yaml")
    config["api_key"] = token
    write_yaml(root / "sdd.config.yaml", config)

    json_code, json_stdout, json_stderr = run_cli(
        [str(root), "--json"], lambda: "1.4.1"
    )
    human_code, human_stdout, human_stderr = run_cli([str(root)], lambda: "1.4.1")

    assert json_code == human_code == 1
    assert json_stderr == human_stdout == ""
    assert diagnostic_codes(json_stdout) == ["secret.inline-credential"]
    assert "[secret.inline-credential]" in human_stderr
    combined = json_stdout + human_stderr
    assert token not in combined
    assert str(root.resolve()) not in combined


@pytest.mark.parametrize(
    ("value", "expected_code"),
    [
        ("-----BEGIN PRIVATE KEY-----\nredacted\n", "secret.private-key"),
        ("https://sample-user:sample-password@example.invalid/repo", "secret.uri-userinfo"),
        ("https://example.invalid/path?access_token=redacted", "secret.query-credential"),
        ("AKIAABCDEFGHIJKLMNOP", "secret.recognizable-token"),
    ],
)
def test_high_confidence_secret_forms_are_rejected_without_echo(
    tmp_path: Path, value: str, expected_code: str
) -> None:
    root = build_central_layout(tmp_path / "central")
    config = read_yaml(root / "sdd.config.yaml")
    config["note"] = value
    write_yaml(root / "sdd.config.yaml", config)

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 1
    assert expected_code in diagnostic_codes(stdout)
    assert value not in stdout


def test_diagnostics_are_deterministic_and_do_not_false_positive_semantic_ids(
    tmp_path: Path,
) -> None:
    root = build_central_layout(tmp_path / "central")
    first = run_cli([str(root), "--json"], lambda: "1.4.1")
    second = run_cli([str(root), "--json"], lambda: "1.4.1")
    assert first == second
    assert first[0] == 0


def test_behavior_is_independent_of_current_working_directory(
    tmp_path: Path, monkeypatch
) -> None:
    root = build_central_layout(tmp_path / "central")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    code, stdout, _ = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert code == 0
    assert json.loads(stdout)["status"] == "valid"


def test_real_entry_point_imports_package_from_any_working_directory(
    tmp_path: Path,
) -> None:
    root = build_central_layout(tmp_path / "central")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()

    completed = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "validate_process_config.py"),
            str(root),
            "--json",
        ],
        cwd=elsewhere,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["status"] == "valid"


@pytest.mark.parametrize(
    ("human_args", "json_args"),
    [
        ([], ["--json"]),
        (["{root}", "--unknown"], ["{root}", "--unknown", "--json"]),
        (["{root}", "--registry"], ["{root}", "--registry", "--json"]),
    ],
    ids=["missing-start", "unknown-option", "malformed-option"],
)
def test_generic_parser_failures_use_stable_human_and_json_contracts(
    tmp_path: Path, human_args: list[str], json_args: list[str]
) -> None:
    root = build_central_layout(tmp_path / "central")
    human = [value.format(root=root) for value in human_args]
    machine = [value.format(root=root) for value in json_args]

    json_code, json_stdout, json_stderr = run_cli(machine, lambda: "1.4.1")
    human_code, human_stdout, human_stderr = run_cli(human, lambda: "1.4.1")

    assert json_code == human_code == 2
    assert json_stderr == human_stdout == ""
    assert diagnostic_codes(json_stdout) == ["usage.arguments"]
    assert json.loads(json_stdout)["status"] == "invalid"
    assert json_stdout.count("\n") == 0
    assert "[usage.arguments]" in human_stderr
    assert not human_stderr.lower().startswith("usage:")
    assert "\nusage:" not in human_stderr.lower()
    assert ": error:" not in human_stderr.lower()


def test_nonexistent_start_directory_is_usage_error(tmp_path: Path) -> None:
    code, _, _ = run_cli(
        [str(tmp_path / "missing"), "--json"], lambda: "1.4.1"
    )
    assert code == 2


def test_malformed_registry_has_human_json_usage_parity(tmp_path: Path) -> None:
    root = build_central_layout(tmp_path / "central")

    json_code, json_stdout, json_stderr = run_cli(
        [str(root), "--registry", "malformed", "--json"], lambda: "1.4.1"
    )
    human_code, human_stdout, human_stderr = run_cli(
        [str(root), "--registry", "malformed"], lambda: "1.4.1"
    )

    assert json_code == human_code == 2
    assert json_stderr == human_stdout == ""
    assert diagnostic_codes(json_stdout) == ["usage.registry"]
    assert json.loads(json_stdout)["status"] == "invalid"
    assert "[usage.registry]" in human_stderr
