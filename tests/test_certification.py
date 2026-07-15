from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from process.certification import CertificationError, build_coverage_report, certify_release, validate_role_output_fixtures


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
CATALOG = PROCESS / "certification" / "cases.yaml"


@pytest.fixture
def external_tmp() -> Path:
    path = Path(tempfile.mkdtemp(prefix="sdd-certification-"))
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


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


def test_evidence_schema_supports_future_actual_model_shape_without_claiming_execution() -> None:
    schema = json.loads((PROCESS / "schemas/certification-evidence.schema.json").read_text(encoding="utf-8"))
    deterministic = certify_release(ROOT, CATALOG, Path(tempfile.gettempdir()) / "schema-check", check=True)
    assert list(Draft202012Validator(schema).iter_errors(deterministic)) == []
    forged_deterministic = copy.deepcopy(deterministic)
    forged_deterministic["cases"][0]["execution_mode"] = "actual-model"
    forged_deterministic["cases"][0]["read_pack"] = {"identity": "a" * 64}
    assert list(Draft202012Validator(schema).iter_errors(forged_deterministic))
    actual = copy.deepcopy(deterministic)
    actual.update({"evidence_kind": "actual-model", "actual_model_run": True})
    actual["model"] = {"family": "qwen-class", "id": "example-model-id", "runtime": "example-runtime"}
    actual["adapter"] = {"family": "qwen-class", "version": "example-adapter-1"}
    actual["cases"][0]["execution_mode"] = "actual-model"
    actual["cases"][0]["read_pack"] = {"identity": "a" * 64}
    actual["normalized_sha256"] = "b" * 64
    assert list(Draft202012Validator(schema).iter_errors(actual)), "partial actual-model forgery must fail"
    roles = ["analyst", "developer", "qa", "tech-lead"]
    classes = ["minor", "major", "hotfix"]
    for index, case in enumerate(actual["cases"]):
        case["execution_mode"] = "actual-model"
        case["read_pack"] = {"identity": "abcdef"[index % 6] * 64}
        case["role"] = roles[index % len(roles)]
        case["change_class"] = classes[index % len(classes)]
    for row in actual["planned_dimensions"]["roles"] + actual["planned_dimensions"]["classes"]:
        row["executed"] = True
    assert list(Draft202012Validator(schema).iter_errors(actual)) == []


def test_catalog_declares_role_class_dimensions_and_expected_outputs_without_execution() -> None:
    catalog = load_yaml(CATALOG)
    dimensions = catalog["planned_dimensions"]
    assert {row["role"] for row in dimensions["roles"]} == {"analyst", "developer", "qa", "tech-lead"}
    assert {row["change_class"] for row in dimensions["classes"]} == {"minor", "major", "hotfix"}
    assert all(row["expected_output"] and row["executed"] is False for row in dimensions["roles"])
    validated = validate_role_output_fixtures(ROOT, catalog)
    assert {row["role"] for row in validated} == {"analyst", "developer", "qa", "tech-lead"}
    assert {row["change_class"] for row in validated} == {"minor", "major", "hotfix"}
    assert all(row["sha256"] and row["executed"] is False for row in validated)


def test_valid_golden_check_is_repeatable_private_and_hash_bound(external_tmp: Path) -> None:
    raw = external_tmp / "raw-artifact-v0.2.0"
    first = certify_release(ROOT, CATALOG, raw, check=True)
    second = certify_release(ROOT, CATALOG, raw, check=True)
    assert first == second
    assert not raw.exists()
    written = certify_release(ROOT, CATALOG, raw, check=False)
    assert first["status"] == "passed"
    assert first["evidence_kind"] == "deterministic-fixture"
    assert first["actual_model_run"] is False
    assert first["model"] == {"family": "not-executed", "id": "not-executed", "runtime": "not-executed"}
    assert first["adapter"] == {"family": "not-executed", "version": "not-executed"}
    assert first["process_package_version"] == "0.2.0"
    assert first["normalized_sha256"]
    normalized_copy = {key: value for key, value in first.items() if key != "normalized_sha256"}
    assert hashlib.sha256(json.dumps(normalized_copy, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == first["normalized_sha256"]
    assert first["canonical_mutated"] is False
    assert first["raw_artifact"]["logical_version"] == "raw-artifact-v0.2.0"
    bundle = raw / "bundle.json"
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == written["raw_artifact"]["sha256"]
    assert "stdout" not in json.dumps(first).lower()
    case = first["cases"][0]
    assert case["evidence_id"] and case["run_id"]
    assert case["execution_mode"] == "deterministic-fixture"
    assert case["operation"]["input_artifact_sha256"]
    assert case["operation"]["output_artifact_sha256"]
    assert case["validation"]["result"] == "passed"
    assert case["canonical_snapshot_before"] == case["canonical_snapshot_after"]
    assert case["read_pack"]["not_applicable_reason"]
    assert case["human_intervention"] == {"required": False, "performed": False, "type": "none"}


def test_arbitrary_command_is_rejected_before_execution(tmp_path: Path, external_tmp: Path) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"][0]["operation"] = "powershell"
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.operation-not-allowed"):
        certify_release(ROOT, custom, external_tmp / "raw", check=True)


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
def test_negative_families_fail_closed_without_canonical_mutation(tmp_path: Path, external_tmp: Path, family: str) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"] = [case for case in catalog["cases"] if case["family"] == family]
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    evidence = certify_release(ROOT, custom, external_tmp / f"raw-{family}", check=True)
    assert evidence["status"] == "passed"
    assert evidence["cases"][0]["observed"] == "blocked"
    assert evidence["cases"][0]["canonical_mutated"] is False
    assert evidence["cases"][0]["canonical_snapshot_before"] == evidence["cases"][0]["canonical_snapshot_after"]


def test_negative_fixture_replaced_by_positive_payload_no_longer_blocks_or_matches(
    tmp_path: Path, external_tmp: Path
) -> None:
    catalog = load_yaml(CATALOG)
    negative = next(case for case in catalog["cases"] if case["family"] == "forbidden-approval")
    negative["fixture"] = "process/certification/positive-cases/preflight-valid.yaml"
    catalog["cases"] = [negative]
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    evidence = certify_release(ROOT, custom, external_tmp / "raw", check=True)
    assert evidence["cases"][0]["observed"] == "passed"
    assert evidence["cases"][0]["matches_golden"] is False
    assert evidence["status"] == "failed"


def test_mismatch_never_rewrites_golden_or_existing_raw_bundle(tmp_path: Path, external_tmp: Path) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"][0]["expected"]["status"] = "blocked"
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    raw = external_tmp / "raw"
    raw.mkdir()
    marker = raw / "bundle.json"
    marker.write_text("preserve", encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.output-exists"):
        certify_release(ROOT, custom, raw, check=False)
    assert marker.read_text(encoding="utf-8") == "preserve"
    fresh = external_tmp / "fresh"
    evidence = certify_release(ROOT, custom, fresh, check=True)
    assert evidence["status"] == "failed"
    assert not fresh.exists()


@pytest.mark.parametrize("attack", ["absolute", "credential", "production-id"])
def test_catalog_privacy_attacks_are_rejected(tmp_path: Path, external_tmp: Path, attack: str) -> None:
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
        certify_release(ROOT, custom, external_tmp / "raw", check=True)


@pytest.mark.parametrize("name", ["corporate-identifier", "internal-identifier", "email", "url", "ip"])
def test_fixture_content_requires_synthetic_privacy_allowlist(
    tmp_path: Path, external_tmp: Path, name: str
) -> None:
    catalog = load_yaml(CATALOG)
    catalog["cases"][0]["fixture"] = f"process/certification/privacy-cases/{name}.yaml"
    catalog["cases"] = [catalog["cases"][0]]
    custom = tmp_path / "cases.yaml"
    custom.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.privacy"):
        certify_release(ROOT, custom, external_tmp / "raw", check=True)


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


@pytest.mark.parametrize("relative", [".review-probe", "docs/review-probe", "tests/review-probe"])
@pytest.mark.parametrize("check", [True, False])
def test_any_output_under_repository_is_rejected(relative: str, check: bool) -> None:
    with pytest.raises(CertificationError, match="certification.unsafe-output"):
        certify_release(ROOT, CATALOG, ROOT / relative, check=check)


def test_runner_is_cwd_independent(external_tmp: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    tmp_path = external_tmp / "cwd"
    tmp_path.mkdir()
    monkeypatch.chdir(tmp_path)
    evidence = certify_release(ROOT, CATALOG, tmp_path / "raw", check=True)
    assert evidence["status"] == "passed"


def test_coverage_composes_accepted_and_active_delta_scenarios() -> None:
    report = build_coverage_report(ROOT, PROCESS / "certification" / "coverage.yaml")
    inventory = load_yaml(PROCESS / "certification" / "coverage.yaml")
    assert "default_evidence" not in inventory
    assert report["status"] in {"complete", "gaps"}
    assert report["summary"]["effective_scenarios"] == (
        report["summary"]["covered"] + report["summary"]["gaps"] + report["summary"]["future_work"]
    )
    assert report["future_work"]
    assert {row["source_kind"] for row in report["coverage"]} == {"accepted", "delta"}
    assert all(row["scenario"] and (row.get("evidence") or row.get("gap")) for row in report["coverage"])
    assert all(not isinstance(ref, str) or not (ref.startswith("pytest:") and "::" not in ref) for row in report["coverage"] for ref in row.get("evidence", []))
    future_selectors = {(row["capability"], row["requirement"], row.get("scenario")) for row in report["future_work"]}
    assert ("weak-model-guardrails", "Actual weak-model certification", None) in future_selectors
    assert not any(row["capability"] == "change-artifact-contracts" and row["requirement"] in {"Thin change artifact contract", "Full package artifact contract"} and row["source_kind"] == "accepted" for row in report["coverage"])


def test_explicit_residual_gap_wins_and_requires_all_fields(tmp_path: Path) -> None:
    coverage = load_yaml(PROCESS / "certification" / "coverage.yaml")
    manifest = load_yaml(PROCESS / "certification" / "evidence-manifest.yaml")
    row = manifest["coverage"][0]
    row.pop("evidence", None); row.pop("binding_id", None)
    row["gap"] = {
        "owner": "example-qa-owner", "risk": "medium", "reason": "synthetic gap",
        "compensation": "manual synthetic review", "follow_up": "work-item-2.11",
    }
    custom_manifest = tmp_path / "evidence-manifest.yaml"
    custom_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    coverage["evidence_manifest"] = custom_manifest.relative_to(ROOT).as_posix()
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    report = build_coverage_report(ROOT, custom)
    selected = next(item for item in report["coverage"] if item["capability"] == row["capability"] and item["requirement"] == row["requirement"] and item["scenario"] == row["scenario"])
    assert "gap" in selected and "evidence" not in selected
    assert report["status"] == "gaps"


def test_unrelated_existing_pytest_node_is_rejected_by_selector_binding(tmp_path: Path) -> None:
    coverage = load_yaml(PROCESS / "certification" / "coverage.yaml")
    manifest = load_yaml(PROCESS / "certification" / "evidence-manifest.yaml")
    manifest["coverage"][0]["evidence"] = ["pytest:tests/test_certification.py::test_full_package_regression_includes_certification_inventory"]
    custom_manifest = tmp_path / "evidence-manifest.yaml"
    custom_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    coverage["evidence_manifest"] = custom_manifest.relative_to(ROOT).as_posix()
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="coverage.binding-mismatch"):
        build_coverage_report(ROOT, custom)


def test_bare_pytest_file_reference_is_forbidden(tmp_path: Path) -> None:
    coverage = load_yaml(PROCESS / "certification" / "coverage.yaml")
    manifest = load_yaml(PROCESS / "certification" / "evidence-manifest.yaml")
    manifest["coverage"][0]["evidence"] = ["pytest:tests/test_artifact_gates.py"]
    custom_manifest = tmp_path / "evidence-manifest.yaml"
    custom_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    coverage["evidence_manifest"] = custom_manifest.relative_to(ROOT).as_posix()
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match="coverage.bare-pytest-file"):
        build_coverage_report(ROOT, custom)


@pytest.mark.parametrize("kind,code", [("duplicate", "coverage.duplicate-marker-selector"), ("unknown", "coverage.unknown-marker-selector")])
def test_source_owned_marker_rejects_duplicate_or_unknown_selector(tmp_path: Path, kind: str, code: str) -> None:
    coverage = load_yaml(PROCESS / "certification" / "coverage.yaml")
    selector = load_yaml(PROCESS / "certification" / "evidence-manifest.yaml")["coverage"][0]
    if kind == "unknown":
        selector = {**selector, "scenario": "Unknown synthetic scenario"}
    marker_file = tmp_path / "test_marker_probe.py"
    marker_file.write_text(
        "SCENARIO_COVERAGE = " + repr({"test_probe": [{key: selector[key] for key in ("source_kind", "capability", "requirement", "scenario")}] * (2 if kind == "duplicate" else 1)}) + "\n\ndef test_probe():\n    assert True\n",
        encoding="utf-8",
    )
    coverage["marker_sources"] = [marker_file.relative_to(ROOT).as_posix()]
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match=code):
        build_coverage_report(ROOT, custom)


def test_role_output_rejects_placeholder_or_tampered_canonical_source_hash(tmp_path: Path) -> None:
    source_root = tmp_path / "root"
    shutil.copytree(ROOT / "process/schemas", source_root / "process/schemas")
    shutil.copytree(ROOT / "process/certification/expected-role-outputs", source_root / "process/certification/expected-role-outputs")
    catalog = load_yaml(CATALOG)
    for role in catalog["planned_dimensions"]["roles"]:
        source = ROOT / load_yaml(ROOT / role["fixture"])["canonical_sources"][0]["path"]
        target = source_root / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    fixture_path = source_root / catalog["planned_dimensions"]["roles"][0]["fixture"]
    fixture = load_yaml(fixture_path)
    fixture["canonical_sources"][0]["sha256"] = "a" * 64
    fixture_path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
    declaration = catalog["planned_dimensions"]["roles"][0]
    declaration["sha256"] = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    with pytest.raises(CertificationError, match="certification.role-output-source-hash"):
        validate_role_output_fixtures(source_root, catalog)


def test_role_output_detects_canonical_source_mutation(tmp_path: Path) -> None:
    source_root = tmp_path / "root"
    shutil.copytree(ROOT / "process/schemas", source_root / "process/schemas")
    shutil.copytree(ROOT / "process/certification/expected-role-outputs", source_root / "process/certification/expected-role-outputs")
    catalog = load_yaml(CATALOG)
    for role in catalog["planned_dimensions"]["roles"]:
        source = ROOT / load_yaml(ROOT / role["fixture"])["canonical_sources"][0]["path"]
        target = source_root / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    validate_role_output_fixtures(source_root, catalog)
    first_source = load_yaml(source_root / catalog["planned_dimensions"]["roles"][0]["fixture"])["canonical_sources"][0]["path"]
    (source_root / first_source).write_text("mutated synthetic source", encoding="utf-8")
    with pytest.raises(CertificationError, match="certification.role-output-source-hash"):
        validate_role_output_fixtures(source_root, catalog)


@pytest.mark.parametrize("unsafe_path", ["../private/spec.md", "openspec/private/spec.md", "C:/private/spec.md"])
def test_role_output_rejects_unsafe_or_private_canonical_source_path(tmp_path: Path, unsafe_path: str) -> None:
    source_root = tmp_path / "root"
    shutil.copytree(ROOT / "process/schemas", source_root / "process/schemas")
    shutil.copytree(ROOT / "process/certification/expected-role-outputs", source_root / "process/certification/expected-role-outputs")
    catalog = load_yaml(CATALOG)
    fixture_path = source_root / catalog["planned_dimensions"]["roles"][0]["fixture"]
    fixture = load_yaml(fixture_path)
    fixture["canonical_sources"][0]["path"] = unsafe_path
    fixture_path.write_text(yaml.safe_dump(fixture, sort_keys=False), encoding="utf-8")
    catalog["planned_dimensions"]["roles"][0]["sha256"] = hashlib.sha256(fixture_path.read_bytes()).hexdigest()
    with pytest.raises(CertificationError, match="certification.privacy"):
        validate_role_output_fixtures(source_root, catalog)


def test_role_output_rejects_linked_canonical_source(tmp_path: Path) -> None:
    source_root = tmp_path / "root"
    shutil.copytree(ROOT / "process/schemas", source_root / "process/schemas")
    shutil.copytree(ROOT / "process/certification/expected-role-outputs", source_root / "process/certification/expected-role-outputs")
    catalog = load_yaml(CATALOG)
    for role in catalog["planned_dimensions"]["roles"]:
        source = ROOT / load_yaml(ROOT / role["fixture"])["canonical_sources"][0]["path"]
        target = source_root / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    first_fixture = load_yaml(source_root / catalog["planned_dimensions"]["roles"][0]["fixture"])
    linked_source = source_root / first_fixture["canonical_sources"][0]["path"]
    external = tmp_path / "external-spec.md"
    external.write_bytes(linked_source.read_bytes())
    linked_source.unlink()
    try:
        linked_source.symlink_to(external)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    with pytest.raises(CertificationError, match="certification.role-output-source-missing"):
        validate_role_output_fixtures(source_root, catalog)


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
    manifest = load_yaml(PROCESS / "certification" / "evidence-manifest.yaml")
    evidence_row = next(row for row in manifest["coverage"] if row.get("evidence"))
    if mutation == "unknown-case":
        evidence_row["evidence"] = ["case:does-not-exist"]
    elif mutation == "unknown-pytest":
        evidence_row["evidence"] = ["pytest:tests/test_certification.py::does_not_exist"]
    elif mutation == "duplicate":
        manifest["coverage"].append(copy.deepcopy(manifest["coverage"][0]))
    elif mutation == "gap-fields":
        evidence_row.pop("evidence")
        evidence_row["gap"] = {"owner": "qa"}
    else:
        coverage["delta_targets"].append({"capability": "missing", "requirement": "Not real", "change": "define-transfer-ready-process-package", "kind": "MODIFIED"})
    custom_manifest = tmp_path / "evidence-manifest.yaml"
    custom_manifest.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    coverage["evidence_manifest"] = custom_manifest.relative_to(ROOT).as_posix()
    custom = tmp_path / "coverage.yaml"
    custom.write_text(yaml.safe_dump(coverage, sort_keys=False), encoding="utf-8")
    with pytest.raises(CertificationError, match=code):
        build_coverage_report(ROOT, custom)


def test_full_package_regression_includes_certification_inventory() -> None:
    package = load_yaml(PROCESS / "package.yaml")
    declared = set(package["distribution"]["files"])
    actual = {path.name for path in PROCESS.iterdir() if path.is_file()}
    assert actual == declared
