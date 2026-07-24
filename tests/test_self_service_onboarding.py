"""Acceptance tests for the public self-service ``sdd`` entrypoint."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_installed_launcher_metadata_and_version_diagnostics(capsys) -> None:
    """The portable package exposes the versioned public command."""
    from scripts.sdd import main

    pyproject = ROOT / "pyproject.toml"
    assert pyproject.is_file()
    assert "sdd = \"process.operation_dispatcher:main\"" in pyproject.read_text(encoding="utf-8")

    assert main(["--version", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "operation": "sdd-version",
        "package": {"id": "sdd-process", "version": "0.3.6"},
        "schema_version": "1.0",
        "status": "ok",
    }


def test_start_and_next_render_one_canonical_continuation_result(tmp_path: Path, capsys) -> None:
    from scripts.sdd import main
    from process.workflow_operations import create_change

    assert main(["start", "new-requirement", "--role", "Analyst", "--fact", "classification=minor", "--json"]) == 0
    started = json.loads(capsys.readouterr().out)
    assert started["status"] == "guided"
    assert started["missing_facts"] == []
    assert started["role_owner"] == "Tech Lead"
    assert started["authority_boundary"] == "Classification remains pending and no gate is approved."
    assert started["next_command"] == "sdd request create-change --role Analyst --json"
    assert started["lifecycle_mutated"] is False

    changes = tmp_path / "changes"
    create_change(
        ROOT / "process",
        changes,
        change_id="sample-minor-001",
        title="Sample minor change",
        classification="minor",
        change_type="config_ops",
    )
    change = changes / "sample-minor-001"
    persisted_change = yaml.safe_load((change / "change.yaml").read_text(encoding="utf-8"))
    assert persisted_change["status"] == "draft"
    assert "lifecycle_state" not in persisted_change
    assert main(["next", "--change", str(change), "--role", "Developer", "--json"]) == 0
    continued = json.loads(capsys.readouterr().out)
    assert continued["status"] == "guided"
    assert continued["missing_facts"] == []
    assert continued["role_owner"] == "Analyst"
    assert continued["next_command"] == "sdd prepare prepare-spec-pr --role Developer --json"
    assert continued["lifecycle_mutated"] is False
    assert continued["external_state_mutated"] is False


def test_next_rejects_noncanonical_or_unsupported_persisted_status(tmp_path: Path, capsys) -> None:
    from scripts.sdd import main

    noncanonical = tmp_path / "noncanonical.yaml"
    noncanonical.write_text("lifecycle_state: approved\n", encoding="utf-8")
    assert main(["next", "--change", str(noncanonical), "--role", "Developer", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["blockers"][0]["code"] == "missing-change-status"

    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("status: impossible\n", encoding="utf-8")
    assert main(["next", "--change", str(invalid), "--role", "Developer", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["blockers"][0]["code"] == "invalid-context"


def test_start_reports_missing_fact_without_guessing(capsys) -> None:
    from scripts.sdd import main

    assert main(["start", "new-requirement", "--role", "Analyst", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "blocked"
    assert payload["missing_facts"] == ["classification"]
    assert payload["next_command"] is None
    assert payload["lifecycle_mutated"] is False


def test_start_human_renderer_uses_the_same_next_command(capsys) -> None:
    from scripts.sdd import main

    assert main(["start", "new-requirement", "--role", "Analyst", "--fact", "classification=minor"]) == 0
    assert "sdd request create-change --role Analyst --json" in capsys.readouterr().out


def test_start_can_select_a_situation_interactively(monkeypatch, capsys) -> None:
    from scripts.sdd import main

    monkeypatch.setattr("builtins.input", lambda _prompt: "new-requirement")
    assert main(["start", "--role", "Analyst", "--fact", "classification=minor", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["route_id"] == "new-requirement"


def test_setup_requires_confirmation_and_bootstraps_only_an_empty_destination(tmp_path: Path, capsys) -> None:
    from scripts.sdd import main

    destination = tmp_path / "workspace"
    base_args = [
        "setup", str(destination), "--package-root", str(ROOT / "process"),
        "--team-template", str(ROOT / "templates" / "team-specs"), "--json",
    ]
    assert main(base_args) == 1
    blocked = json.loads(capsys.readouterr().out)
    assert blocked["blockers"][0]["code"] == "confirmation-required"
    assert not destination.exists()

    assert main([*base_args[:-1], "--confirm", "--json"]) == 0
    created = json.loads(capsys.readouterr().out)
    assert created["status"] == "created"
    assert created["workspace"] == str(destination)
    assert created["next_command"] == "sdd start new-requirement --role Analyst --json"
    assert (destination / "team-specs" / "sdd.config.yaml").is_file()

    assert main([*base_args[:-1], "--confirm", "--json"]) == 1
    nonempty = json.loads(capsys.readouterr().out)
    assert nonempty["blockers"][0]["code"] == "destination-not-empty"


def test_installed_windows_or_posix_console_script_delegates_to_the_dispatcher(tmp_path: Path) -> None:
    environment = tmp_path / "environment"
    created = subprocess.run(
        [sys.executable, "-m", "venv", "--system-site-packages", str(environment)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert created.returncode == 0, created.stderr
    python = environment / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    completed = subprocess.run(
        [str(python), "-m", "pip", "install", "--no-deps", str(ROOT)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert completed.returncode == 0, completed.stderr
    launcher = environment / ("Scripts/sdd.exe" if sys.platform == "win32" else "bin/sdd")
    invoked = subprocess.run([str(launcher), "--version", "--json"], capture_output=True, text=True, check=False)
    assert invoked.returncode == 0, invoked.stderr
    assert json.loads(invoked.stdout)["package"] == {"id": "sdd-process", "version": "0.3.6"}
    help_output = subprocess.run([str(launcher), "--help"], capture_output=True, text=True, check=False)
    assert help_output.returncode == 0, help_output.stderr
    assert all(token in help_output.stdout for token in ("setup", "start", "next", "0.3.6"))
    workspace = tmp_path / "installed-workspace"
    setup = subprocess.run(
        [str(launcher), "setup", str(workspace), "--confirm", "--json"],
        capture_output=True, text=True, check=False,
    )
    assert setup.returncode == 0, setup.stderr
    assert json.loads(setup.stdout)["status"] == "created"
    assert (workspace / "team-specs" / "sdd.config.yaml").is_file()


def test_setup_rejects_invalid_package_without_creating_the_destination(tmp_path: Path, capsys) -> None:
    from scripts.sdd import main

    destination = tmp_path / "workspace"
    assert main([
        "setup", str(destination), "--confirm", "--package-root", str(tmp_path / "missing"),
        "--team-template", str(ROOT / "templates" / "team-specs"), "--json",
    ]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["blockers"][0]["code"] == "input-invalid"
    assert not destination.exists()


def test_clean_sandbox_walkthrough_prepares_minor_change_spec_pr_and_archive(tmp_path: Path, capsys) -> None:
    from scripts.create_change import main as create_change
    from scripts.sdd import main

    workspace = tmp_path / "workspace"
    assert main([
        "setup", str(workspace), "--confirm", "--package-root", str(ROOT / "process"),
        "--team-template", str(ROOT / "templates" / "team-specs"), "--json",
    ]) == 0
    capsys.readouterr()
    changes = workspace / "team-specs" / "openspec" / "changes"
    assert create_change([
        "sample-minor-001", "--title", "Synthetic minor", "--classification", "minor",
        "--type", "behavior_change", "--changes-root", str(changes),
        "--package-root", str(workspace / "process"), "--json",
    ]) == 0
    capsys.readouterr()

    for operation in ("prepare-spec-pr", "prepare-archive"):
        assert main([
            "prepare", operation, "--role", "Developer", "--", str(changes / "sample-minor-001"),
            "--package-root", str(workspace / "process"), "--json",
        ]) == 0
        payload = json.loads(capsys.readouterr().out)
        assert payload["operation"] == f"sdd-prepare"
        assert payload["external_state_mutated"] is False
