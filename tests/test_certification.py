from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path

import pytest
import yaml

from process.certification import CertificationError, build_coverage_report, certify_release


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
CATALOG = PROCESS / "certification" / "cases.yaml"


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_package_registers_closed_certification_contracts_and_assets() -> None:
    package = load_yaml(PROCESS / "package.yaml")
    assert package["schemas"]["certification_case"] == "schemas/certification-case.schema.json"
    assert package["schemas"]["certification_evidence"] == "schemas/certification-evidence.schema.json"
    assert package["schemas"]["coverage_report"] == "schemas/coverage-report.schema.json"
    assert package["certification"]["case_catalog"] == "certification/cases.yaml"
    assert "certification.py" in package["distribution"]["files"]
    for name in ("certification-case", "certification-evidence", "coverage-report"):
        schema = json.loads((PROCESS / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
        assert schema["additionalProperties"] is False


def test_valid_golden_check_is_repeatable_private_and_hash_bound(tmp_path: Path) -> None:
    raw = tmp_path / "raw-artifact-v0.2.0"
    first = certify_release(ROOT, CATALOG, raw, check=True)
    second = certify_release(ROOT, CATALOG, raw, check=True)
    assert first == second
    assert not raw.exists()
    written = certify_release(ROOT, CATALOG, raw, check=False)
    assert first["status"] == "passed"
    assert first["evidence_kind"] == "deterministic-fixture"
    assert first["actual_model_run"] is False
    assert first["model"] == first["runtime"] == "not-executed"
    assert first["canonical_mutated"] is False
    assert first["raw_artifact"]["logical_version"] == "raw-artifact-v0.2.0"
    bundle = raw / "bundle.json"
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == written["raw_artifact"]["sha256"]
    assert "stdout" not in json.dumps(first).lower()


def test_arbitrary_command_is_rejected_before_execution(tmp_path: Path) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"][0]["operation"] = "powershell"
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.operation-not-allowed"):
        certify_release(ROOT, custom, tmp_path / "raw", check=True)


@pytest.mark.parametrize(
    "family",
    [
        "missing-context",
        "conflicting-sources",
        "fabricated-evidence",
        "forbidden-approval",
        "skipped-stop",
        "invalid-lifecycle-transition",
        "adapter-failure",
        "context-limit",
    ],
)
def test_negative_families_fail_closed_without_canonical_mutation(tmp_path: Path, family: str) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"] = [case for case in catalog["cases"] if case["family"] == family]
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    canonical = ROOT / "process" / "VERSION"
    before = canonical.read_bytes()
    evidence = certify_release(ROOT, custom, tmp_path / f"raw-{family}", check=True)
    assert evidence["status"] == "passed"
    assert evidence["cases"][0]["observed"] == "blocked"
    assert evidence["cases"][0]["canonical_mutated"] is False
    assert canonical.read_bytes() == before


def test_mismatch_never_rewrites_golden_or_existing_raw_bundle(tmp_path: Path) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"][0]["expected"]["status"] = "blocked"
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    raw = tmp_path / "raw"
    raw.mkdir()
    marker = raw / "bundle.json"
    marker.write_text("preserve", encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.output-exists"):
        certify_release(ROOT, custom, raw, check=False)
    assert marker.read_text(encoding="utf-8") == "preserve"
    fresh = tmp_path / "fresh"
    evidence = certify_release(ROOT, custom, fresh, check=True)
    assert evidence["status"] == "failed"
    assert not fresh.exists()


@pytest.mark.parametrize("attack", ["absolute", "credential", "production-id"])
def test_catalog_privacy_attacks_are_rejected(tmp_path: Path, attack: str) -> None:
    catalog = load_yaml(CATALOG)
    if attack == "absolute":
        catalog["cases"][0]["fixture"] = str(ROOT / "process" / "VERSION")
    elif attack == "credential":
        catalog["cases"][0]["fixture"] = "synthetic/password-secret.yaml"
    else:
        catalog["cases"][0]["fixture"] = "synthetic/prod-payments.yaml"
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.privacy"):
        certify_release(ROOT, custom, tmp_path / "raw", check=True)


def test_output_overlap_and_symlink_are_rejected(tmp_path: Path) -> None:
    with pytest.raises(CertificationError, match="certification.unsafe-output"):
        certify_release(ROOT, CATALOG, ROOT / "process" / "certification" / "raw", check=False)
    if hasattr(os, "symlink"):
        target = tmp_path / "target"
        target.mkdir()
        link = tmp_path / "link"
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            pytest.skip("symlink creation is unavailable")
        with pytest.raises(CertificationError, match="certification.unsafe-output"):
            certify_release(ROOT, CATALOG, link, check=False)


def test_runner_is_cwd_independent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    evidence = certify_release(ROOT, CATALOG, tmp_path / "raw", check=True)
    assert evidence["status"] == "passed"


def test_coverage_composes_accepted_and_active_delta_scenarios() -> None:
    report = build_coverage_report(ROOT, PROCESS / "certification" / "coverage.yaml")
    assert report["status"] == "complete"
    assert report["future_work"]
    assert {row["source_kind"] for row in report["coverage"]} == {"accepted", "delta"}
    assert all(row["scenario"] and row["evidence"] for row in report["coverage"])


@pytest.mark.parametrize("mutation,code", [
    ("unknown-case", "coverage.unknown-case"),
    ("unknown-pytest", "coverage.unknown-pytest"),
    ("duplicate", "coverage.duplicate-selector"),
    ("gap-fields", "coverage.invalid-gap"),
    ("delta-target", "coverage.unknown-delta-target"),
])
def test_coverage_rejects_unknown_duplicates_invalid_gaps_and_delta_targets(
    tmp_path: Path, mutation: str, code: str
) -> None:
    coverage = load_yaml(PROCESS / "certification" / "coverage.yaml")
    if mutation == "unknown-case":
        coverage["coverage"][0]["evidence"] = "case:does-not-exist"
    elif mutation == "unknown-pytest":
        coverage["coverage"][0]["evidence"] = "pytest:tests/test_certification.py::does_not_exist"
    elif mutation == "duplicate":
        coverage["coverage"].append(copy.deepcopy(coverage["coverage"][0]))
    elif mutation == "gap-fields":
        coverage["coverage"][0].pop("evidence")
        coverage["coverage"][0]["gap"] = {"owner": "qa"}
    else:
        coverage["delta_targets"].append({"capability": "missing", "requirement": "Not real", "change": "define-transfer-ready-process-package", "kind": "MODIFIED"})
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match=code):
        build_coverage_report(ROOT, custom)


def test_full_package_regression_includes_certification_inventory() -> None:
    package = load_yaml(PROCESS / "package.yaml")
    declared = set(package["distribution"]["files"])
    actual = {path.name for path in PROCESS.iterdir() if path.is_file()}
    assert actual == declared
