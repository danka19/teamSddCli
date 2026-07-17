from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from process.release_candidate import (
    ReleaseInputs,
    build_release_candidate,
    generate_release_manifest,
    payload_inventory,
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
    "validate_external_mapping.py",
    "validate_process_config.py",
    "validate_traceability.py",
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
        "WEAK_MODEL_OPERATING_KIT.md",
    }
    assert {item["name"] for item in allowlist["entry_points"]} == EXPECTED_ENTRY_POINTS
    assert all(item["smoke"] for item in allowlist["entry_points"])


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


def test_validator_rejects_payload_mutation_and_undeclared_extra(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    (candidate / "payload/undeclared.txt").write_text("extra", encoding="utf-8")
    with pytest.raises(OperationError, match="release.inventory-mismatch"):
        validate_release_manifest(candidate, manifest)
    (candidate / "payload/undeclared.txt").unlink()
    (candidate / "payload/process/release/evidence").mkdir(parents=True)
    (candidate / "payload/process/release/evidence/dev.yaml").write_text("private: true\n", encoding="utf-8")
    with pytest.raises(OperationError, match="release.mutable-evidence-forbidden"):
        payload_inventory(candidate / "payload")


def test_every_entry_point_smokes_from_standalone_candidate(candidate_tmp: Path) -> None:
    candidate, manifest = _build(candidate_tmp)
    standalone = candidate_tmp / "standalone"
    shutil.copytree(candidate / "payload", standalone)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    allowlist = yaml.safe_load((standalone / "process/release-allowlist.yaml").read_text(encoding="utf-8"))
    for item in allowlist["entry_points"]:
        result = subprocess.run(
            [sys.executable, *item["smoke"]], cwd=standalone, env=env,
            capture_output=True, text=True, timeout=20,
        )
        assert result.returncode in item["expected_exit_codes"], (
            item["name"], result.returncode, result.stdout, result.stderr
        )
    copied_manifest = copy.deepcopy(manifest)
    assert generate_release_manifest(standalone, _inputs(candidate_tmp)) == copied_manifest
