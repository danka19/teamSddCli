from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

import process.release_candidate as release_candidate_module
from process.release_candidate import (
    RehearsalOptions,
    ReleaseInputs,
    build_release_candidate,
    evaluate_release_acceptance,
    generate_release_manifest,
    payload_inventory,
    rehearse_release_candidate,
    validate_portable_path,
    validate_release_manifest,
)
from process.workflow_operations import OperationError


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ENTRY_POINTS = {
    "bootstrap_team_specs.py",
    "check_corporate_flow.py",
    "check_lifecycle_transition.py",
    "check_tech_lead_control.py",
    "classify_change.py",
    "create_change.py",
    "evaluate_change_gates.py",
    "manage_release_candidate.py",
    "manual_fallback.py",
    "migrate_change_classification.py",
    "prepare_archive.py",
    "prepare_spec_pr.py",
    "review_tech_lead.py",
    "update_process_package.py",
    "validate_change.py",
    "validate_corporate_adaptation.py",
    "validate_external_mapping.py",
    "validate_process_config.py",
    "validate_traceability.py",
}

EXPECTED_CERTIFICATIONS = {
    "qwen-class": "phase-2-14-qwen-adapter-2-2-2026-07-18.yaml",
    "deepseek-class": "phase-2-14-deepseek-adapter-2-2-2026-07-18.yaml",
}


@pytest.fixture
def candidate_tmp(tmp_path: Path):
    root = ROOT.parent / f".release-candidate-tests-{tmp_path.name}"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    try:
        yield root
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _inputs(tmp_path: Path) -> ReleaseInputs:
    raw = tmp_path / "raw"
    raw.mkdir(exist_ok=True)
    (raw / "actual-model-output.json").write_text('{"result":"pass"}\n', encoding="utf-8")
    return ReleaseInputs("phase-2-12-rc1", ("macOS is not certified",), raw)


def _build(tmp_path: Path, name: str = "candidate") -> tuple[Path, dict]:
    destination = tmp_path / name
    manifest = build_release_candidate(ROOT, destination, _inputs(tmp_path))
    return destination, manifest


def _write_manifest(candidate: Path, manifest: dict) -> None:
    (candidate / "release-manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )


WINDOWS_SCENARIOS = [
    "clean-bootstrap", "config-compatibility", "minor-flow", "major-flow",
    "hotfix-flow", "migration-check", "migration-apply", "migration-idempotent",
    "update", "failed-update-hold", "rollback", "archive-history-preserved",
    "negative-acceptance-cases", "ai-disabled",
]
LINUX_SCENARIOS = [
    "clean-bootstrap", "config-compatibility", "class-flow-smoke", "migration-smoke",
    "update-rollback-smoke", "negative-acceptance-cases", "ai-disabled",
]


def _acceptance_build(tmp_path: Path) -> tuple[Path, dict, Path]:
    raw = tmp_path / "acceptance-raw"
    selection = yaml.safe_load(
        (ROOT / "process/release-certification-selection.yaml").read_text(encoding="utf-8")
    )
    for row in selection["selected"]:
        target = raw / row["raw_logical_root"]
        target.mkdir(parents=True)
        (target / "result.json").write_text('{"result":"passed"}\n', encoding="utf-8")
    candidate = tmp_path / "acceptance-candidate"
    inputs = ReleaseInputs("phase-2-12-rc1", ("macOS is not certified",), raw)
    manifest = build_release_candidate(ROOT, candidate, inputs)
    return candidate, manifest, raw


def _host_row(candidate: Path, manifest: dict, platform: str) -> dict:
    windows = platform == "windows"
    digest = "a" * 64
    return {
        "schema_version": "1.0",
        "evidence_id": f"phase-2-12-{platform}",
        "platform_id": platform,
        "evidence_level": "full-clean-rehearsal" if windows else "portability-smoke",
        "completed_at": "2026-07-17T00:00:00Z",
        "payload_sha256": manifest["payload_sha256"],
        "manifest_sha256": hashlib.sha256((candidate / "release-manifest.yaml").read_bytes()).hexdigest(),
        "process_package_version": manifest["process_package"]["version"],
        "config_schema_version": manifest["config_schema_version"],
        "inventory": {
            "os": "Windows 11" if windows else "Ubuntu 24.04 on WSL2",
            "architecture": "x86_64", "shell": "PowerShell 7" if windows else "bash 5",
            "python": "3.13.5", "node": "22.17.0", "openspec": "1.4.1", "git": "2.50.1",
        },
        "inventory_commands": [
            {"argv": ["python", "--version"], "exit_code": 0, "stdout": "Python 3.13.5"},
            {"argv": ["node", "--version"], "exit_code": 0, "stdout": "v22.17.0"},
            {"argv": ["openspec", "--version"], "exit_code": 0, "stdout": "1.4.1"},
            {"argv": ["git", "--version"], "exit_code": 0, "stdout": "git version 2.50.1"},
            {"argv": ["python", "-c", "import platform;print(platform.platform())"], "exit_code": 0, "stdout": "synthetic-host"},
        ],
        "mcp": {"status": "explicitly-unavailable", "evidence_ref": None},
        "scenario_ids": WINDOWS_SCENARIOS if windows else LINUX_SCENARIOS,
        "scenario_codes": ["migration-ok", "update-ok", "failed-update-held", "rollback-ok", "archive-unchanged"],
        "negative_acceptance_cases": [
            {"case_id": case_id, "expected_code": code, "observed_codes": [code], "result": "passed"}
            for case_id, code in (
                ("missing", "evidence-missing"), ("stale", "evidence-stale"),
                ("failed", "evidence-failed"), ("private", "evidence-private"),
                ("ai-only", "evidence-ai-only"),
                ("checksum-mismatch", "evidence-checksum-mismatch"),
                ("payload-mismatch", "candidate-digest-mismatch"),
            )
        ],
        "result": "passed", "ai_disabled": True, "human_authority_substituted": False,
        "privacy_scan": "passed", "archive_digest_before": digest,
        "archive_digest_after": digest, "rollback_result": "passed",
    }


def _host_evidence(tmp_path: Path, candidate: Path, manifest: dict) -> Path:
    root = tmp_path / "host-evidence"
    root.mkdir()
    for platform in ("windows", "linux-wsl2"):
        (root / f"{platform}.yaml").write_text(
            yaml.safe_dump(_host_row(candidate, manifest, platform), sort_keys=False), encoding="utf-8"
        )
    return root


def test_allowlist_is_schema_valid_and_exact() -> None:
    allowlist = yaml.safe_load((ROOT / "process/release-allowlist.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "process/schemas/release-allowlist.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(allowlist)) == []
    assert allowlist["requirements"] == ["requirements-test.txt"]
    assert allowlist["template_roots"] == ["templates/team-specs"]
    assert set(allowlist["runbooks"]) == {
        "ARTIFACT_AND_LIFECYCLE_GATES.md", "CERTIFICATION_EVIDENCE.md",
        "CLASSIFICATION_AND_MIGRATION.md", "CORPORATE_FLOW_CONTROLS.md",
        "PACKAGED_GOVERNED_FLOW.md", "PROCESS_PACKAGE_SETUP.md",
        "TECH_LEAD_GOVERNANCE.md", "TRANSFER_RELEASE_CANDIDATE.md",
        "WEAK_MODEL_OPERATING_KIT.md", "CORPORATE_ADAPTATION_AND_PILOT.md",
    }
    assert {item["name"] for item in allowlist["entry_points"]} == EXPECTED_ENTRY_POINTS
    assert all(item["smoke"] for item in allowlist["entry_points"])
    manage = next(item for item in allowlist["entry_points"] if item["name"] == "manage_release_candidate.py")
    assert manage["additional_smokes"] == [
        ["scripts/manage_release_candidate.py", "accept", "--help"],
        ["scripts/manage_release_candidate.py", "rehearse", "--help"],
    ]


def test_release_certification_selection_is_schema_valid_and_exact() -> None:
    selection = yaml.safe_load(
        (ROOT / "process/release-certification-selection.yaml").read_text(encoding="utf-8")
    )
    schema = json.loads(
        (ROOT / "process/schemas/release-certification-selection.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert list(Draft202012Validator(schema).iter_errors(selection)) == []
    assert {
        row["model_family"]: Path(row["normalized_evidence_path"]).name
        for row in selection["selected"]
    } == EXPECTED_CERTIFICATIONS
    normalized = {
        row["model_family"]: yaml.safe_load(
            (ROOT / "process" / row["normalized_evidence_path"]).read_text(encoding="utf-8")
        )
        for row in selection["selected"]
    }
    assert all(
        row["raw_logical_root"] == normalized[row["model_family"]]["raw_artifact"]["logical_id"]
        for row in selection["selected"]
    )


def test_acceptance_closes_exact_hosts_and_selected_certification_roots(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate, manifest, raw = _acceptance_build(candidate_tmp)
    hosts = _host_evidence(candidate_tmp, candidate, manifest)
    observed: list[Path] = []

    def valid_selected(evidence: dict, artifact_root: Path, **_: object) -> list[str]:
        observed.append(artifact_root)
        assert evidence["status"] == "passed"
        return []

    monkeypatch.setattr(release_candidate_module, "validate_normalized_evidence", valid_selected)
    result = evaluate_release_acceptance(
        candidate, manifest, hosts, raw,
        now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc),
    )

    assert result == {
        "operation": "evaluate-release-acceptance",
        "status": "evidence-complete",
        "release_id": "phase-2-12-rc1",
        "payload_sha256": manifest["payload_sha256"],
        "human_acceptance_required": True,
        "diagnostics": [],
    }
    assert {path.name for path in observed} == {
        row["raw_logical_root"]
        for row in yaml.safe_load(
            (ROOT / "process/release-certification-selection.yaml").read_text(encoding="utf-8")
        )["selected"]
    }


@pytest.mark.parametrize(
    ("case", "expected"),
    [
        ("evidence-missing", "evidence-missing"),
        ("evidence-stale", "evidence-stale"),
        ("evidence-future", "evidence-future"),
        ("evidence-failed", "evidence-failed"),
        ("evidence-private", "evidence-private"),
        ("evidence-ai-only", "evidence-ai-only"),
        ("evidence-checksum-mismatch", "evidence-checksum-mismatch"),
        ("candidate-digest-mismatch", "candidate-digest-mismatch"),
        ("incompatible-dependency", "incompatible-dependency"),
        ("failed-update-hold", "failed-update-hold"),
        ("archive-history-rewrite", "archive-history-rewrite"),
    ],
)
def test_acceptance_rejects_negative_cases(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch, case: str, expected: str
) -> None:
    candidate, manifest, raw = _acceptance_build(candidate_tmp)
    hosts = _host_evidence(candidate_tmp, candidate, manifest)
    monkeypatch.setattr(release_candidate_module, "validate_normalized_evidence", lambda *args, **kwargs: [])
    windows_path = hosts / "windows.yaml"
    windows = yaml.safe_load(windows_path.read_text(encoding="utf-8"))
    if case == "evidence-missing":
        (hosts / "linux-wsl2.yaml").unlink()
    elif case == "evidence-stale":
        windows["completed_at"] = "2026-06-16T00:00:00Z"
    elif case == "evidence-future":
        windows["completed_at"] = "2026-07-18T00:00:00Z"
    elif case == "evidence-failed":
        windows["result"] = "failed"
    elif case == "evidence-private":
        windows["mcp"]["evidence_ref"] = "api_key=sk-secret-value-1234567890"
    elif case == "evidence-ai-only":
        windows["ai_disabled"] = False
    elif case == "evidence-checksum-mismatch":
        selected = yaml.safe_load(
            (ROOT / "process/release-certification-selection.yaml").read_text(encoding="utf-8")
        )["selected"][0]
        (raw / selected["raw_logical_root"] / "result.json").write_text("changed\n", encoding="utf-8")
    elif case == "candidate-digest-mismatch":
        windows["payload_sha256"] = "b" * 64
    elif case == "incompatible-dependency":
        windows["inventory"]["python"] = "2.7.18"
    elif case == "failed-update-hold":
        windows["scenario_codes"].remove("failed-update-held")
    else:
        windows["archive_digest_after"] = "b" * 64
    windows_path.write_text(yaml.safe_dump(windows, sort_keys=False), encoding="utf-8")

    result = evaluate_release_acceptance(
        candidate, manifest, hosts, raw,
        now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc),
    )

    assert result["status"] == "evidence-rejected"
    assert result["human_acceptance_required"] is True
    assert expected in [row["code"] for row in result["diagnostics"]]


@pytest.mark.parametrize(
    ("status", "reference"),
    [("provisioned", None), ("provisioned", ""), ("explicitly-unavailable", "evidence/mcp.json")],
)
def test_acceptance_rejects_inconsistent_mcp_observation(
    candidate_tmp: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: str,
    reference: str | None,
) -> None:
    candidate, manifest, raw = _acceptance_build(candidate_tmp)
    hosts = _host_evidence(candidate_tmp, candidate, manifest)
    monkeypatch.setattr(release_candidate_module, "validate_normalized_evidence", lambda *args, **kwargs: [])
    path = hosts / "windows.yaml"
    row = yaml.safe_load(path.read_text(encoding="utf-8"))
    row["mcp"] = {"status": status, "evidence_ref": reference}
    path.write_text(yaml.safe_dump(row, sort_keys=False), encoding="utf-8")

    result = evaluate_release_acceptance(candidate, manifest, hosts, raw, now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc))

    assert result["status"] == "evidence-rejected"
    assert "evidence-mcp-inconsistent" in [item["code"] for item in result["diagnostics"]]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scenario_ids", [["unhashable"]]),
        ("scenario_codes", [{"unhashable": True}]),
        ("mcp", []),
        ("inventory", []),
        ("completed_at", {"wrong": "type"}),
    ],
)
def test_acceptance_rejects_schema_invalid_host_rows_without_type_errors(
    candidate_tmp: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
) -> None:
    candidate, manifest, raw = _acceptance_build(candidate_tmp)
    hosts = _host_evidence(candidate_tmp, candidate, manifest)
    monkeypatch.setattr(release_candidate_module, "validate_normalized_evidence", lambda *args, **kwargs: [])
    path = hosts / "windows.yaml"
    row = yaml.safe_load(path.read_text(encoding="utf-8"))
    row[field] = value
    path.write_text(yaml.safe_dump(row, sort_keys=False), encoding="utf-8")

    result = evaluate_release_acceptance(candidate, manifest, hosts, raw, now=datetime(2026, 7, 17, 12, tzinfo=timezone.utc))

    assert result["status"] == "evidence-rejected"
    assert "evidence-invalid" in [item["code"] for item in result["diagnostics"]]


def test_rehearsal_orchestrates_ai_disabled_migration_update_rollback_and_exclusive_evidence(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate, manifest, _ = _acceptance_build(candidate_tmp)
    payload_before = payload_inventory(candidate / "payload")["payload_sha256"]
    inventory = _host_row(candidate, manifest, "windows")
    monkeypatch.setattr(
        release_candidate_module,
        "_observe_inventory",
        lambda: (inventory["inventory"], inventory["inventory_commands"]),
        raising=False,
    )
    workspace = candidate_tmp / "rehearsal-workspace"
    output = candidate_tmp / "windows-evidence.yaml"

    result = rehearse_release_candidate(
        candidate,
        workspace,
        RehearsalOptions("windows", "full-clean-rehearsal", "explicitly-unavailable", None, output),
    )

    assert result["status"] == "rehearsal-complete"
    evidence = yaml.safe_load(output.read_text(encoding="utf-8"))
    schema = json.loads(
        (candidate / "payload/process/schemas/release-host-evidence.schema.json").read_text(encoding="utf-8")
    )
    assert list(Draft202012Validator(schema).iter_errors(evidence)) == []
    assert set(evidence["scenario_ids"]) == set(WINDOWS_SCENARIOS)
    assert evidence["archive_digest_before"] == evidence["archive_digest_after"]
    assert (
        workspace / "team-specs/openspec/changes/archive/accepted.md"
    ).read_bytes() == b"immutable accepted history\n"
    assert evidence["rollback_result"] == "passed"
    assert {item["case_id"] for item in evidence["negative_acceptance_cases"]} == {
        "missing", "stale", "failed", "private", "ai-only", "checksum-mismatch", "payload-mismatch"
    }
    assert all(item["result"] == "passed" for item in evidence["negative_acceptance_cases"])
    assert evidence["ai_disabled"] is True
    assert evidence["human_authority_substituted"] is False
    assert payload_inventory(candidate / "payload")["payload_sha256"] == payload_before
    with pytest.raises(OperationError, match="release.output-exists"):
        rehearse_release_candidate(
            candidate,
            candidate_tmp / "second-workspace",
            RehearsalOptions("windows", "full-clean-rehearsal", "explicitly-unavailable", None, output),
        )


def test_inventory_runs_fixed_argv_without_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[list[str], bool]] = []

    class Completed:
        returncode = 0
        stdout = "version 99\n"
        stderr = ""

    def run(argv: list[str], **kwargs: object) -> Completed:
        calls.append((argv, bool(kwargs.get("shell"))))
        return Completed()

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(
        release_candidate_module.shutil,
        "which",
        lambda command: f"/resolved/{command}",
    )
    inventory, commands = release_candidate_module._observe_inventory()
    assert len(commands) == 5
    assert all(shell is False for _, shell in calls)
    assert [argv[0] for argv, _ in calls] == [f"/resolved/{row['argv'][0]}" for row in commands]
    assert [argv[1:] for argv, _ in calls] == [row["argv"][1:] for row in commands]
    assert set(inventory) == {"os", "architecture", "shell", "python", "node", "openspec", "git"}


def test_inventory_resolves_windows_command_shims_without_shell(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Completed:
        returncode = 0
        stdout = "version 99\n"
        stderr = ""

    def run(argv: list[str], **kwargs: object) -> Completed:
        if argv[0] == "openspec":
            raise FileNotFoundError("Windows cannot execute the PowerShell shim directly")
        assert kwargs.get("shell") is False
        return Completed()

    monkeypatch.setattr(subprocess, "run", run)
    monkeypatch.setattr(
        release_candidate_module.shutil,
        "which",
        lambda command: "C:/npm/openspec.CMD" if command == "openspec" else command,
        raising=False,
    )

    _, commands = release_candidate_module._observe_inventory()

    assert commands[2]["argv"] == ["openspec", "--version"]


def test_candidate_includes_declared_canonical_sources_for_certification_revalidation(
    candidate_tmp: Path,
) -> None:
    candidate, _, _ = _acceptance_build(candidate_tmp)
    package = yaml.safe_load((ROOT / "process/package.yaml").read_text(encoding="utf-8"))

    for relative in package["canonical_sources"]:
        assert (candidate / "payload" / relative).read_bytes() == (ROOT / relative).read_bytes()


def test_privacy_scan_allows_localhost_endpoint_but_rejects_windows_user_path() -> None:
    assert not release_candidate_module._contains_private_bytes(
        b'{"endpoint":"http://127.0.0.1:11434"}'
    )
    assert release_candidate_module._contains_private_bytes(
        b'{"path":"C:\\\\Users\\\\private-user\\\\artifact.json"}'
    )


def test_negative_acceptance_matrix_fails_closed_when_expected_rejection_is_not_observed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(release_candidate_module, "_validate_host_evidence_row", lambda *args, **kwargs: [])
    with pytest.raises(OperationError, match="release.negative-acceptance-failed"):
        release_candidate_module._run_negative_acceptance_matrix(
            {"platform_id": "windows"},
            {"payload_sha256": "a" * 64, "compatibility": {}},
            "b" * 64,
            datetime(2026, 7, 17, tzinfo=timezone.utc),
            ROOT / "process/schemas/release-host-evidence.schema.json",
        )


def test_runbook_accept_examples_use_candidate_payload_entry_point() -> None:
    text = (ROOT / "docs/runbooks/TRANSFER_RELEASE_CANDIDATE.md").read_text(encoding="utf-8")
    assert "C:\\release\\candidate\\payload\\scripts\\manage_release_candidate.py accept" in text
    assert "/mnt/c/release/candidate/payload/scripts/manage_release_candidate.py accept" in text


@pytest.mark.parametrize("mutation", ["duplicate", "wrong-smoke", "wrong-exit"])
def test_allowlist_rejects_non_exact_entry_point_contract(mutation: str) -> None:
    allowlist = yaml.safe_load((ROOT / "process/release-allowlist.yaml").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "process/schemas/release-allowlist.schema.json").read_text(encoding="utf-8"))
    if mutation == "duplicate":
        allowlist["entry_points"][-1] = copy.deepcopy(allowlist["entry_points"][0])
    elif mutation == "wrong-smoke":
        allowlist["entry_points"][0]["smoke"] = ["scripts/validate_change.py", "--help"]
    else:
        allowlist["entry_points"][0]["expected_exit_codes"] = [0, 1, 2, 3]
    assert list(Draft202012Validator(schema).iter_errors(allowlist))


def test_build_is_byte_stable_and_manifest_binds_payload_only(candidate_tmp: Path) -> None:
    first, manifest_a = _build(candidate_tmp, "candidate-a")
    second, manifest_b = _build(candidate_tmp, "candidate-b")
    assert manifest_a == manifest_b
    assert (first / "release-manifest.yaml").read_bytes() == (second / "release-manifest.yaml").read_bytes()
    assert manifest_a["inventory"] == sorted(manifest_a["inventory"], key=lambda item: item["path"])
    assert manifest_a["payload_sha256"] == payload_inventory(first / "payload")["payload_sha256"]
    original = manifest_a["payload_sha256"]
    (first / "release-manifest.yaml").write_text("changed outside payload\n", encoding="utf-8")
    assert payload_inventory(first / "payload")["payload_sha256"] == original
    assert manifest_a["host_evidence"] == [
        {"platform_id": "windows", "evidence_level": "full-clean-rehearsal"},
        {"platform_id": "linux-wsl2", "evidence_level": "portability-smoke"},
        {"platform_id": "macos", "evidence_level": "not-certified"},
    ]


def test_candidate_contains_only_allowlisted_self_contained_assets(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    payload = candidate / "payload"
    package = yaml.safe_load((ROOT / "process/package.yaml").read_text(encoding="utf-8"))
    expected = {f"process/{name}" for name in package["distribution"]["files"]}
    expected |= {f"process/{name}" for name in package["distribution"]["roots"]}
    assert all((payload / path).exists() for path in expected)
    assert (payload / "requirements-test.txt").is_file()
    assert (payload / "templates/team-specs").is_dir()
    assert all((payload / "docs/runbooks" / name).is_file() for name in yaml.safe_load(
        (ROOT / "process/release-allowlist.yaml").read_text(encoding="utf-8")
    )["runbooks"])
    assert {path.name for path in (payload / "scripts").iterdir()} == EXPECTED_ENTRY_POINTS
    assert validate_release_manifest(candidate, manifest)["status"] == "valid"


@pytest.mark.parametrize("field", [
    "process_package", "config_schema_version", "openspec", "host_evidence",
    "compatibility", "verification_commands", "verification_requirements",
    "certification_path", "certification_checksum", "rollback_reference",
])
def test_validator_rederives_every_committed_manifest_field(
    candidate_tmp: Path, field: str
) -> None:
    candidate, manifest = _build(candidate_tmp)
    tampered = copy.deepcopy(manifest)
    if field == "process_package":
        tampered[field]["version"] = "9.9.9"
    elif field == "config_schema_version":
        tampered[field] = "9.9"
    elif field == "openspec":
        tampered[field]["cli_version"] = "9.9.9"
    elif field == "host_evidence":
        tampered[field][0]["evidence_level"] = "portability-smoke"
    elif field == "compatibility":
        tampered[field]["python"] = "99+"
    elif field == "verification_commands":
        tampered["verification"]["commands"][0] = "python arbitrary.py"
    elif field == "verification_requirements":
        tampered["verification"]["evidence_requirements"][0] = "arbitrary"
    elif field == "certification_path":
        tampered["weak_model_certification"][0]["path"] = tampered["weak_model_certification"][1]["path"]
    elif field == "certification_checksum":
        tampered["weak_model_certification"][0]["sha256"] = "0" * 64
    else:
        tampered[field] = "docs/runbooks/TRANSFER_RELEASE_CANDIDATE.md"
    _write_manifest(candidate, tampered)
    with pytest.raises(OperationError, match="release.manifest-derived-mismatch"):
        validate_release_manifest(candidate, tampered)


def test_recomputed_manifest_cannot_authorize_undeclared_payload_extra(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    extra = candidate / "payload/undeclared.txt"
    extra.write_text("not declared\n", encoding="utf-8")
    recomputed = payload_inventory(candidate / "payload")
    manifest["inventory"] = recomputed["inventory"]
    manifest["payload_sha256"] = recomputed["payload_sha256"]
    _write_manifest(candidate, manifest)
    with pytest.raises(OperationError, match="release.allowlist-closure"):
        validate_release_manifest(candidate, manifest)


def test_returned_manifest_cannot_mutate_validator_derived_constants(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    manifest["host_evidence"][0]["evidence_level"] = "portability-smoke"
    manifest["verification"]["commands"][0] = "python arbitrary.py"
    _write_manifest(candidate, manifest)
    with pytest.raises(OperationError, match="release.manifest-derived-mismatch"):
        validate_release_manifest(candidate, manifest)


@pytest.mark.parametrize("unsafe", [
    "C:/escape.txt", "C:escape.txt", "//server/share.txt", "/absolute.txt",
    ".", "a/../b", "a/./b", "name:stream", "bad\x01name", "trail. ",
    "CON", "con.txt", "dir/AUX.log", "LPT9.md", "COM1",
])
def test_portable_paths_reject_cross_platform_threats(unsafe: str) -> None:
    with pytest.raises(OperationError, match="release.path-unsafe"):
        validate_portable_path(unsafe)


def test_inventory_rejects_unicode_casefold_collision_and_links(tmp_path: Path) -> None:
    root = tmp_path / "payload"
    root.mkdir()
    (root / "é.txt").write_text("a", encoding="utf-8")
    (root / "e\u0301.txt").write_text("b", encoding="utf-8")
    with pytest.raises(OperationError, match="release.path-collision"):
        payload_inventory(root)
    shutil.rmtree(root)
    root.mkdir()
    target = root / "target.txt"
    target.write_text("x", encoding="utf-8")
    try:
        os.symlink(target, root / "linked.txt")
    except OSError:
        pytest.skip("symlinks are unavailable on this Windows host")
    with pytest.raises(OperationError, match="release.link-forbidden"):
        payload_inventory(root)


@pytest.mark.parametrize(
    "relative",
    ["process/validators/__pycache__/check.cpython-313.pyc", "process/validators/check.pyc", "process/validators/check.pyo"],
)
def test_inventory_rejects_python_bytecode(tmp_path: Path, relative: str) -> None:
    root = tmp_path / "payload"
    target = root / relative
    target.parent.mkdir(parents=True)
    target.write_bytes(b"compiled-python-bytecode")

    with pytest.raises(OperationError, match="release.bytecode-forbidden"):
        payload_inventory(root)


def test_copy_tree_excludes_python_bytecode_from_source(tmp_path: Path) -> None:
    source = tmp_path / "source"
    target = tmp_path / "target"
    (source / "__pycache__").mkdir(parents=True)
    (source / "validator.py").write_text("VALUE = 1\n", encoding="utf-8")
    (source / "validator.pyc").write_bytes(b"compiled-python-bytecode")
    (source / "__pycache__/validator.cpython-313.pyc").write_bytes(b"compiled-python-bytecode")

    release_candidate_module._copy_tree(source, target, "process/validators")

    assert (target / "validator.py").is_file()
    assert not (target / "validator.pyc").exists()
    assert not (target / "__pycache__").exists()


def test_payload_root_link_or_reparse_is_rejected_before_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "payload"
    root.mkdir()
    (root / "asset.txt").write_text("x", encoding="utf-8")
    original = release_candidate_module._is_link_or_reparse
    seen: list[Path] = []

    def fake(path: Path) -> bool:
        seen.append(path)
        return path == root or original(path)

    monkeypatch.setattr(release_candidate_module, "_is_link_or_reparse", fake)
    with pytest.raises(OperationError, match="release.link-forbidden"):
        payload_inventory(root)
    assert seen[-1] == root


def test_candidate_root_link_bypass_is_rejected(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate, manifest = _build(candidate_tmp)
    original = release_candidate_module._is_link_or_reparse

    def fake(path: Path) -> bool:
        return path == candidate or original(path)

    monkeypatch.setattr(release_candidate_module, "_is_link_or_reparse", fake)
    with pytest.raises(OperationError, match="release.link-forbidden"):
        validate_release_manifest(candidate, manifest)


def test_existing_ancestor_reparse_is_rejected_before_root_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ancestor = tmp_path / "alias"
    payload = ancestor / "nested" / "payload"
    payload.mkdir(parents=True)
    original = release_candidate_module._is_link_or_reparse

    def fake(path: Path) -> bool:
        return path == ancestor or original(path)

    monkeypatch.setattr(release_candidate_module, "_is_link_or_reparse", fake)
    with pytest.raises(OperationError, match="release.link-forbidden"):
        payload_inventory(payload)


def test_builder_rejects_overlap_and_preexisting_destination(candidate_tmp: Path) -> None:
    inputs = _inputs(candidate_tmp)
    existing = candidate_tmp / "existing"
    existing.mkdir()
    with pytest.raises(OperationError, match="release.destination-exists"):
        build_release_candidate(ROOT, existing, inputs)
    with pytest.raises(OperationError, match="release.path-overlap"):
        build_release_candidate(ROOT, ROOT / "nested-candidate", inputs)
    with pytest.raises(OperationError, match="release.path-overlap"):
        build_release_candidate(ROOT, ROOT.parent, inputs)


def test_overlap_rejection_has_no_parent_creation_side_effect(tmp_path: Path) -> None:
    new_parent = ROOT / f".overlap-side-effect-{tmp_path.name}"
    assert not new_parent.exists()
    with pytest.raises(OperationError, match="release.path-overlap"):
        build_release_candidate(ROOT, new_parent / "candidate", _inputs(tmp_path))
    assert not new_parent.exists()


def test_destination_ancestor_reparse_is_rejected_before_child_creation(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ancestor = candidate_tmp / "alias"
    ancestor.mkdir()
    child = ancestor / "new-parent"
    original = release_candidate_module._is_link_or_reparse

    def fake(path: Path) -> bool:
        return path == ancestor or original(path)

    monkeypatch.setattr(release_candidate_module, "_is_link_or_reparse", fake)
    with pytest.raises(OperationError, match="release.link-forbidden"):
        build_release_candidate(ROOT, child / "candidate", _inputs(candidate_tmp))
    assert not child.exists()


def test_builder_creates_missing_parent_before_atomic_staging(candidate_tmp: Path) -> None:
    destination = candidate_tmp / "missing" / "parent" / "candidate"
    manifest = build_release_candidate(ROOT, destination, _inputs(candidate_tmp))
    assert destination.is_dir()
    assert validate_release_manifest(destination, manifest)["status"] == "valid"


def test_atomic_publish_rejects_destination_created_during_build(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = candidate_tmp / "raced-candidate"
    original = release_candidate_module._publish_no_replace

    def race(staging: Path, target: Path) -> None:
        target.mkdir()
        original(staging, target)

    monkeypatch.setattr(release_candidate_module, "_publish_no_replace", race)
    with pytest.raises(OperationError, match="release.destination-exists"):
        build_release_candidate(ROOT, destination, _inputs(candidate_tmp))
    assert destination.is_dir()
    assert not any(candidate_tmp.glob(".raced-candidate.*"))


def test_release_inputs_reject_string_known_limitations(candidate_tmp: Path) -> None:
    inputs = ReleaseInputs("phase-2-12-rc1", "not-a-list", _inputs(candidate_tmp).raw_artifact_root)  # type: ignore[arg-type]
    with pytest.raises(OperationError, match="input-invalid") as raised:
        build_release_candidate(ROOT, candidate_tmp / "bad-input", inputs)
    assert raised.value.exit_code == 3


def test_validator_rejects_payload_mutation_and_undeclared_extra(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    (candidate / "payload/undeclared.txt").write_text("extra", encoding="utf-8")
    with pytest.raises(OperationError, match="release.allowlist-closure"):
        validate_release_manifest(candidate, manifest)
    (candidate / "payload/undeclared.txt").unlink()
    (candidate / "payload/process/release/evidence").mkdir(parents=True)
    (candidate / "payload/process/release/evidence/dev.yaml").write_text("private: true\n", encoding="utf-8")
    with pytest.raises(OperationError, match="release.mutable-evidence-forbidden"):
        payload_inventory(candidate / "payload")


def test_validator_requires_supplied_manifest_to_equal_canonical_disk_file(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    on_disk = copy.deepcopy(manifest)
    on_disk["known_limitations"] = ["different caller-owned limitation"]
    _write_manifest(candidate, on_disk)
    with pytest.raises(OperationError, match="release.manifest-file-mismatch"):
        validate_release_manifest(candidate, manifest)


@pytest.mark.parametrize("kind", ["directory", "reparse", "malformed"])
def test_validator_rejects_unsafe_or_malformed_disk_manifest(
    candidate_tmp: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    candidate, manifest = _build(candidate_tmp)
    path = candidate / "release-manifest.yaml"
    if kind == "directory":
        path.unlink()
        path.mkdir()
    elif kind == "reparse":
        original = release_candidate_module._is_link_or_reparse
        monkeypatch.setattr(
            release_candidate_module,
            "_is_link_or_reparse",
            lambda candidate_path: candidate_path == path or original(candidate_path),
        )
    else:
        path.write_text("not: [valid", encoding="utf-8")
    code = "release.manifest-file-unsafe" if kind != "malformed" else "release.manifest-file-invalid"
    with pytest.raises(OperationError, match=code):
        validate_release_manifest(candidate, manifest)


SCENARIO_COVERAGE = {
    "test_build_is_byte_stable_and_manifest_binds_payload_only": [
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Release evidence and auditability",
            "scenario": "Release manifest identifies what was certified",
        }
    ],
    "test_candidate_includes_declared_canonical_sources_for_certification_revalidation": [
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Transfer-ready release candidate contents",
            "scenario": "Release candidate contains the reusable core",
        }
    ],
    "test_privacy_scan_allows_localhost_endpoint_but_rejects_windows_user_path": [
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Transfer-ready release candidate contents",
            "scenario": "Release candidate does not contain corporate values",
        }
    ],
    "test_rehearsal_orchestrates_ai_disabled_migration_update_rollback_and_exclusive_evidence": [
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Reproducible bootstrap and maintenance",
            "scenario": "Supported hosts produce proportionate governed evidence",
        },
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Reproducible bootstrap and maintenance",
            "scenario": "Clean environment can bootstrap the reference setup",
        },
        {
            "source_kind": "delta",
            "capability": "transfer-readiness",
            "requirement": "Reproducible bootstrap and maintenance",
            "scenario": "Upgrade can be rolled back",
        },
    ],
}


def test_every_entry_point_smokes_from_standalone_candidate(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    standalone = candidate_tmp / "standalone"
    shutil.copytree(candidate / "payload", standalone)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    allowlist = yaml.safe_load((standalone / "process/release-allowlist.yaml").read_text(encoding="utf-8"))
    for item in allowlist["entry_points"]:
        for smoke in [item["smoke"], *item.get("additional_smokes", [])]:
            result = subprocess.run(
                [sys.executable, *smoke], cwd=standalone, env=env,
                capture_output=True, text=True, timeout=20,
            )
            assert result.returncode in item["expected_exit_codes"], (
                item["name"], result.returncode, result.stdout, result.stderr
            )
    copied_manifest = copy.deepcopy(manifest)
    assert generate_release_manifest(standalone, _inputs(candidate_tmp)) == copied_manifest
