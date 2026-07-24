"""CLI evidence/exit contracts for packaged deterministic operations."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.bootstrap_team_specs import main as bootstrap_main
from scripts.create_change import main as create_main
from scripts.prepare_spec_pr import main as spec_pr_main
from scripts.prepare_archive import main as archive_main
from scripts.update_process_package import main as update_main
from scripts.validate_traceability import main as traceability_main
from scripts.validate_external_mapping import main as external_mapping_main
from scripts.manual_fallback import main as fallback_main
from process.operation_cli import execute


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


def test_bootstrap_accepts_the_declared_operations_catalog(tmp_path: Path, capsys) -> None:
    """Package validation dispatches the operations catalog to its own loader."""
    workspace = tmp_path / "workspace"

    assert bootstrap_main([
        str(workspace), "--package-root", str(PROCESS),
        "--team-template", str(TEAM_TEMPLATE), "--json",
    ]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "created"
    assert (workspace / "process" / "schemas" / "operations-catalog.schema.json").is_file()


SCENARIO_COVERAGE = {
    "test_bootstrap_accepts_the_declared_operations_catalog": [
        {
            "source_kind": "accepted",
            "capability": "repo-topology-config",
            "requirement": "Process package carries operation-dispatch assets",
            "scenario": "Bootstrap carries one coherent operation contract",
        },
    ],
}


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


def test_malformed_root_and_unexpected_failure_are_redacted_exit3(
    tmp_path: Path, capsys,
) -> None:
    malformed = tmp_path / "malformed.yaml"
    malformed.write_text("- not\n- a-mapping\n", encoding="utf-8")

    assert traceability_main([str(malformed), "--json"]) == 3
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "operational-error"
    assert payload["diagnostics"] == [{
        "code": "input-invalid",
        "message": "A required local operation failed.",
    }]
    assert captured.err == ""

    def unexpected() -> dict:
        raise RuntimeError("C:/private/secret should never render")

    assert execute(unexpected, True) == 3
    captured = capsys.readouterr()
    assert "private" not in captured.out
    assert "secret" not in captured.out
    assert captured.err == ""


def test_external_mapping_and_manual_fallback_thin_clis_are_stable_and_cwd_independent(
    tmp_path: Path,
) -> None:
    mapping = tmp_path / "mapping.yaml"
    mapping.write_text(
        "schema_version: '1.0'\npolicy: {id: sdd-core, version: 1.0.0}\nstates:\n"
        "  openspec_archive: archived\n  release_readiness: release-ready\n"
        "  deployment: deployed\n  consumer_acceptance: accepted\n  tracker_done: done\n",
        encoding="utf-8",
    )
    mapping_script = ROOT / "scripts" / "validate_external_mapping.py"
    fallback_script = ROOT / "scripts" / "manual_fallback.py"

    mapped = subprocess.run(
        [sys.executable, str(mapping_script), str(mapping), "--json"],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert mapped.returncode == 0
    assert json.loads(mapped.stdout)["states"]["tracker_done"] == "done"
    assert mapped.stderr == ""

    fallback = subprocess.run(
        [sys.executable, str(fallback_script), "--unavailable", "jira", "--unavailable", "mcp", "--json"],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert fallback.returncode == 0
    assert json.loads(fallback.stdout)["unavailable"] == ["jira", "mcp"]
    assert fallback.stderr == ""

    unknown = subprocess.run(
        [sys.executable, str(fallback_script), "--unavailable", "unknown", "--json"],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert unknown.returncode == 1
    assert json.loads(unknown.stdout)["diagnostics"][0]["code"] == "integration-unknown"
    assert unknown.stderr == ""


def test_every_file_based_entry_point_uses_exit3_for_missing_or_malformed_root(
    tmp_path: Path, capsys,
) -> None:
    missing = tmp_path / "missing"
    malformed = tmp_path / "malformed.yaml"
    malformed.write_text("[]\n", encoding="utf-8")
    cases = [
        (bootstrap_main, [str(tmp_path / "workspace"), "--package-root", str(missing), "--team-template", str(TEAM_TEMPLATE), "--json"]),
        (create_main, ["sample-change-001", "--title", "Sample", "--classification", "minor", "--type", "behavior_change", "--changes-root", str(tmp_path / "changes"), "--package-root", str(missing), "--json"]),
        (spec_pr_main, [str(missing), "--package-root", str(PROCESS), "--json"]),
        (archive_main, [str(missing), "--package-root", str(PROCESS), "--json"]),
            (update_main, ["check", str(missing), str(missing), str(malformed), "--evidence", str(malformed), "--json"]),
        (traceability_main, [str(malformed), "--json"]),
        (external_mapping_main, [str(malformed), "--json"]),
    ]
    for main, args in cases:
        assert main(args) == 3
        captured = capsys.readouterr()
        payload = json.loads(captured.out)
        assert payload["status"] == "operational-error"
        assert captured.err == ""
