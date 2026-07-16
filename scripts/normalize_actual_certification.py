"""Build normalized Git evidence from the complete append-only model inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.actual_certification import (
    ActualCertificationError,
    evaluate_frozen_model_output,
    select_model_profile,
    split_reasoning_envelope,
    validate_phase_gate,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _group(artifact_root: Path, path: Path) -> str:
    return "root" if path.parent == artifact_root else path.parent.relative_to(artifact_root).as_posix()


def _reference(path: Path, group: str, reason: str, route: dict | None = None) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    case = raw.get("case", {})
    ollama = raw.get("ollama", raw)
    reasoning, final_response = split_reasoning_envelope(ollama.get("response", ""), ollama.get("thinking", ""))
    exact_failed = raw.get("exact_result") == "failed"
    record = {
        "case_id": case.get("id", raw.get("case_id", path.stem)), "actual_model_run": True,
        "result": "failed" if exact_failed else "invalidated",
        "disposition": "failed-retained" if exact_failed else "invalidated-or-superseded",
        "reason": "exact-output-contract-failed" if exact_failed else reason,
        "raw_group": group, "raw_filename": path.name, "raw_sha256": _sha(path),
        "human_intervention": "mandatory-human-fallback",
        "fallback": (f"deterministic validator plus {route['mandatory_human_owner']}: {route['mandatory_human_decision']}" if route else "deterministic validator and named human execution remain mandatory"),
        "thinking_present": bool(reasoning), "final_response_present": bool(final_response),
        "done_reason": ollama.get("done_reason"), "duration_ms": ollama.get("client_duration_ms"),
        "prompt_tokens": ollama.get("prompt_eval_count"), "output_tokens": ollama.get("eval_count"),
    }
    if route:
        record.update(route)
    return record


def _ai_disabled_failure_reference(path: Path, group: str, raw: dict) -> dict:
    return {
        "case_id": raw.get("case_id", path.stem), "actual_model_run": False,
        "result": "failed", "disposition": "failed-retained", "reason": "ai-disabled-deterministic-failure",
        "outcome": {"exit_code": raw.get("exit_code")},
        "raw_group": group, "raw_logical_artifact_id": path.stem,
        "raw_filename": path.name, "raw_sha256": _sha(path),
        "human_intervention": "package-schema correction followed by deterministic retry",
        "fallback": "correct deterministic package validation and rerun the AI-disabled walkthrough",
    }


def _row(path: Path, group: str, repository_root: Path, case: dict, limitation: str, route: dict) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw_case = raw["case"]
    ollama = raw["ollama"]
    reasoning, final_response = split_reasoning_envelope(ollama.get("response", ""), ollama.get("thinking", ""))
    _, _, _, _, diagnostics = evaluate_frozen_model_output(repository_root, repository_root / "process", case, ollama)
    passed = not diagnostics
    manifest = raw["source_manifest"]
    return {
        "case_id": raw_case["id"], "phase": raw_case["phase"], "operation": raw_case["operation"], "actual_model_run": True,
        "role": raw_case["role"], "change_class": raw_case["change_class"], "risk_case": raw_case["risk_case"],
        "execution_identity": raw["execution_identity"], "run_group": group,
        "read_pack_identity": raw["read_pack_identity"], "source_manifest": manifest,
        "source_hashes": {source["stable_id"]: source["sha256"] for source in manifest},
        "raw_logical_artifact_id": path.stem, "raw_filename": path.name, "raw_sha256": _sha(path),
        "deterministic_validation_result": "passed" if passed else "failed", "diagnostics": diagnostics,
        "raw_recorded_validation_result": raw.get("validation", {}).get("result", "not-recorded"),
        "human_intervention": "none" if passed else "mandatory-human-fallback",
        "forbidden_action_result": "none-observed" if passed else "rejected-or-unreliable",
        "limitation": limitation,
        "fallback": f"deterministic validator plus {route['mandatory_human_owner']}: {route['mandatory_human_decision']}",
        **route,
        "duration_ms": ollama.get("client_duration_ms"), "prompt_tokens": ollama.get("prompt_eval_count"),
        "output_tokens": ollama.get("eval_count"), "done_reason": ollama.get("done_reason"),
        "thinking_present": bool(reasoning), "final_response_present": bool(final_response),
    }


def _default_reason(group: str) -> str:
    if group in {"qwen-contract-preflight-final-001", "qwen-matrix-001"}:
        return "reviewer-leading-prompt"
    if group.startswith("qwen-contract-preflight-00"):
        return "superseded-contract-attempt"
    if group.startswith("qwen-nonleading-"):
        return "superseded-nonleading-contract-remediation"
    return "superseded-model-or-runtime-attempt"


def normalize_remediation_evidence(
    baseline_evidence: Path,
    remediation_artifact_root: Path,
    preflight_result: Path,
    matrix_result: Path | None,
    model_family: str,
    *,
    repository_root: Path | None = None,
) -> dict:
    """Link immutable adapter 1.0 evidence to new adapter 2.0 phase summaries."""
    repository_root = (repository_root or Path(__file__).resolve().parents[1]).resolve()
    baseline_path = baseline_evidence.resolve()
    try:
        baseline_relative = baseline_path.relative_to(repository_root).as_posix()
    except ValueError as error:
        raise ActualCertificationError("actual-model.baseline-path-outside-repository") from error
    baseline = yaml.safe_load(baseline_path.read_text(encoding="utf-8"))
    preflight = json.loads(preflight_result.read_text(encoding="utf-8"))
    if not isinstance(baseline, dict) or not isinstance(preflight, dict):
        raise ActualCertificationError("actual-model.normalization-input-malformed")
    if baseline.get("adapter", {}).get("version") != "1.0" or baseline.get("adapter", {}).get("family") != model_family:
        raise ActualCertificationError("actual-model.baseline-adapter-mismatch")
    preflight_diagnostics = validate_phase_gate(
        preflight, remediation_artifact_root, "preflight", model_family, "2.0", 5
    )
    if preflight_diagnostics:
        raise ActualCertificationError(preflight_diagnostics[0])
    if matrix_result is None:
        raise ActualCertificationError("actual-model.matrix-result-required")
    matrix = json.loads(matrix_result.read_text(encoding="utf-8"))
    if not isinstance(matrix, dict):
        raise ActualCertificationError("actual-model.normalization-input-malformed")
    matrix_diagnostics = validate_phase_gate(
        matrix, remediation_artifact_root, "matrix", model_family, "2.0", 15
    )
    if matrix_diagnostics:
        raise ActualCertificationError(matrix_diagnostics[0])
    document = {
        "schema_version": "1.2",
        "evidence_id": f"phase-2-11-{model_family.removesuffix('-class')}-remediation",
        "process_package_version": preflight.get("process_package_version"),
        "adapter": {"family": model_family, "version": "2.0", "authority": "advisory-only"},
        "model": preflight.get("model"),
        "source_catalog": preflight.get("source_catalog"),
        "raw_artifact": {"logical_id": remediation_artifact_root.name, "stored_in_git": False},
        "baseline_reference": {
            "path": baseline_relative,
            "sha256": _sha(baseline_path),
            "raw_logical_artifact_id": baseline.get("raw_artifact", {}).get("logical_id"),
            "adapter_version": "1.0",
        },
        "preflight": {"status": preflight.get("status"), "cases": preflight.get("cases", [])},
        "matrix": {"status": matrix.get("status"), "cases": matrix.get("cases", [])},
        "status": "passed",
        "limitations": preflight.get("limitations", []),
    }
    return document


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--existing", type=Path)
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--preflight-group")
    parser.add_argument("--matrix-group")
    parser.add_argument("--baseline-evidence", type=Path)
    parser.add_argument("--remediation-artifact-root", type=Path)
    parser.add_argument("--preflight-result", type=Path)
    parser.add_argument("--matrix-result", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-family", choices=("qwen-class", "deepseek-class"), default="qwen-class")
    args = parser.parse_args(argv)
    repository_root = Path(__file__).resolve().parents[1]
    if args.baseline_evidence is not None:
        if args.remediation_artifact_root is None or args.preflight_result is None:
            parser.error("--remediation-artifact-root and --preflight-result are required with --baseline-evidence")
        try:
            document = normalize_remediation_evidence(
                args.baseline_evidence,
                args.remediation_artifact_root,
                args.preflight_result,
                args.matrix_result,
                args.model_family,
                repository_root=repository_root,
            )
            with args.output.open("x", encoding="utf-8", newline="\n") as handle:
                yaml.safe_dump(document, handle, sort_keys=False, allow_unicode=True)
        except (
            OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError,
            ActualCertificationError, TypeError, AttributeError, KeyError,
        ) as error:
            print(json.dumps({"status": "blocked", "diagnostic": str(error)}, sort_keys=True))
            return 3
        return 0
    if any(value is None for value in (args.existing, args.artifact_root, args.preflight_group, args.matrix_group)):
        parser.error("legacy mode requires --existing, --artifact-root, --preflight-group, and --matrix-group")
    old = yaml.safe_load(args.existing.read_text(encoding="utf-8"))
    catalog = yaml.safe_load((repository_root / "process/certification/qwen-matrix.yaml").read_text(encoding="utf-8"))
    cases = {case["id"]: case for case in catalog["cases"]}
    routes = catalog["fallback_routes"]
    model = select_model_profile(catalog, args.model_family)
    prefix = args.model_family.removesuffix("-class")
    limitation = model.get("limitation", "family-level proxy; corporate-runtime equivalence is not established")
    existing = {
        (str(row.get("raw_group", "root")), str(row.get("raw_filename", ""))): row
        for row in old.get("failed_attempts", [])
    }
    preflight_paths = sorted((args.artifact_root / args.preflight_group).glob(f"{prefix}*.json"))
    matrix_paths = sorted((args.artifact_root / args.matrix_group).glob(f"{prefix}*.json"))
    active = {(_group(args.artifact_root, path), path.name) for path in [*preflight_paths, *matrix_paths]}
    runtime_show_path = args.artifact_root / "runtime-probe-001" / f"{prefix}-runtime-show.json"
    failed: list[dict] = []
    for path in sorted(args.artifact_root.rglob(f"{prefix}*.json")):
        if path == runtime_show_path or path.name in {"ollama-runtime-probe.json", f"{prefix}-runtime-probe.json"}:
            continue
        group = _group(args.artifact_root, path)
        key = (group, path.name)
        if key in active:
            continue
        prior = existing.get(key, {})
        route = catalog.get("exact_output_fallback_route") if group == "exact-output-preflight-001" else None
        failed.append(_reference(path, group, str(prior.get("reason") or _default_reason(group)), route))
    for path in sorted(args.artifact_root.rglob("ai-disabled-*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("exit_code") != 0:
            failed.append(_ai_disabled_failure_reference(path, _group(args.artifact_root, path), raw))
    probe_group = "runtime-probe-001"
    probe_filename = "ollama-runtime-probe.json" if prefix == "qwen" else f"{prefix}-runtime-probe.json"
    probe_path = args.artifact_root / probe_group / probe_filename
    probe_raw = json.loads(probe_path.read_text(encoding="utf-8"))
    runtime_show_raw = json.loads(runtime_show_path.read_text(encoding="utf-8")) if runtime_show_path.is_file() else None
    document = {
        "schema_version": "1.1", "evidence_id": f"phase-2-11-{prefix}-2026-07-15", "process_package_version": "0.2.0",
        "adapter": {"family": args.model_family, "version": "1.0", "authority": "advisory-only"},
        "model": {**model, "actual_model_run": True},
        "raw_artifact": {"logical_id": args.artifact_root.name, "stored_in_git": False},
        "source": {"catalog": "process/certification/qwen-matrix.yaml", "case_semantics": "shared-frozen-non-leading"},
        "limitations": [limitation], "failed_attempts": failed,
        "runtime_probe": {
            "result": "passed", "raw_group": probe_group, "raw_logical_artifact_id": probe_path.stem,
            "raw_filename": probe_path.name, "raw_sha256": _sha(probe_path), "runtime_version": probe_raw["runtime_version"],
            "model_tag": probe_raw["model_tag"], "model_digest": probe_raw["model_digest"], "endpoint": probe_raw["endpoint"],
            "adapter_version": probe_raw["adapter_version"], "process_package_version": probe_raw["process_package_version"],
            "model_show": ({"raw_group": probe_group, "raw_filename": runtime_show_path.name,
                "raw_sha256": _sha(runtime_show_path), **runtime_show_raw["cross_validation"]} if runtime_show_raw else None),
        },
        "preflight": {"actual_model_run": True, "raw_group": args.preflight_group, "cases": [_row(path, args.preflight_group, repository_root, cases[(case_id := json.loads(path.read_text(encoding="utf-8"))["case"]["id"])], limitation, routes[case_id]) for path in preflight_paths]},
        "matrix": {"actual_model_run": True, "raw_group": args.matrix_group, "cases": [_row(path, args.matrix_group, repository_root, cases[(case_id := json.loads(path.read_text(encoding="utf-8"))["case"]["id"])], limitation, routes[case_id]) for path in matrix_paths]},
    }
    for section in ("preflight", "matrix"):
        for row in document[section]["cases"]:
            row["endpoint"] = probe_raw["endpoint"]
            row["runtime_probe_sha256"] = document["runtime_probe"]["raw_sha256"]
    args.output.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
