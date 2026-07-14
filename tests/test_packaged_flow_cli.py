"""CLI evidence/exit contracts for packaged deterministic operations."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.bootstrap_team_specs import main as bootstrap_main
from scripts.create_change import main as create_main
from scripts.prepare_spec_pr import main as spec_pr_main


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
TEAM_TEMPLATE = ROOT / "templates" / "team-specs"


def test_bootstrap_create_and_spec_pr_json_entry_points_are_non_interactive(
    tmp_path: Path, capsys,
) -> None:
    workspace = tmp_path / "workspace"
    assert bootstrap_main([
        str(workspace), "--package-root", str(PROCESS),
        "--team-template", str(TEAM_TEMPLATE), "--json",
    ]) == 0
    bootstrap = json.loads(capsys.readouterr().out)
    assert bootstrap["status"] == "created"

    changes = workspace / "team-specs" / "openspec" / "changes"
    assert create_main([
        "sample-minor-001", "--title", "Synthetic minor",
        "--classification", "minor", "--type", "behavior_change",
        "--changes-root", str(changes), "--package-root", str(workspace / "process"),
        "--json",
    ]) == 0
    created = json.loads(capsys.readouterr().out)
    assert created["decision_state"] == "pending-human-confirmation"

    assert spec_pr_main([
        str(changes / "sample-minor-001"),
        "--package-root", str(workspace / "process"), "--json",
    ]) == 0
    prepared = json.loads(capsys.readouterr().out)
    assert prepared["approved"] is False
    assert prepared["merged"] is False


def test_json_entry_points_return_stable_operator_error_without_traceback(
    tmp_path: Path, capsys,
) -> None:
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "human.txt").write_text("keep", encoding="utf-8")

    assert bootstrap_main([
        str(occupied), "--package-root", str(PROCESS),
        "--team-template", str(TEAM_TEMPLATE), "--json",
    ]) == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "error"
    assert payload["diagnostics"] == [{
        "code": "destination-not-empty",
        "message": "The operation could not be completed safely.",
    }]
    assert captured.err == ""
    assert (occupied / "human.txt").read_text(encoding="utf-8") == "keep"
