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

from process.actual_certification import evaluate_frozen_model_output


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _group(artifact_root: Path, path: Path) -> str:
    return "root" if path.parent == artifact_root else path.parent.relative_to(artifact_root).as_posix()


def _reference(path: Path, group: str, reason: str) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    case = raw.get("case", {})
    return {
        "case_id": case.get("id", raw.get("case_id", path.stem)), "actual_model_run": True,
        "result": "invalidated", "disposition": "invalidated-or-superseded", "reason": reason,
        "raw_group": group, "raw_filename": path.name, "raw_sha256": _sha(path),
        "human_intervention": "mandatory-human-fallback",
        "fallback": "deterministic validator and named human execution remain mandatory",
    }


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


def _row(path: Path, group: str, repository_root: Path, case: dict) -> dict:
    raw = json.loads(path.read_text(encoding="utf-8"))
    raw_case = raw["case"]
    ollama = raw["ollama"]
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
        "limitation": "qwen3.5:9b is a family-level proxy for the target-environment Qwen3.6-35B, not equivalence proof",
        "fallback": "deterministic validator and named human decision remain mandatory",
        "duration_ms": ollama.get("client_duration_ms"), "prompt_tokens": ollama.get("prompt_eval_count"),
        "output_tokens": ollama.get("eval_count"), "done_reason": ollama.get("done_reason"),
    }


def _default_reason(group: str) -> str:
    if group in {"qwen-contract-preflight-final-001", "qwen-matrix-001"}:
        return "reviewer-leading-prompt"
    if group.startswith("qwen-contract-preflight-00"):
        return "superseded-contract-attempt"
    if group.startswith("qwen-nonleading-"):
        return "superseded-nonleading-contract-remediation"
    return "superseded-model-or-runtime-attempt"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--existing", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--preflight-group", required=True)
    parser.add_argument("--matrix-group", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    old = yaml.safe_load(args.existing.read_text(encoding="utf-8"))
    catalog = yaml.safe_load((repository_root / "process/certification/qwen-matrix.yaml").read_text(encoding="utf-8"))
    cases = {case["id"]: case for case in catalog["cases"]}
    existing = {
        (str(row.get("raw_group", "root")), str(row.get("raw_filename", ""))): row
        for row in old.get("failed_attempts", [])
    }
    preflight_paths = sorted((args.artifact_root / args.preflight_group).glob("qwen*.json"))
    matrix_paths = sorted((args.artifact_root / args.matrix_group).glob("qwen*.json"))
    active = {(_group(args.artifact_root, path), path.name) for path in [*preflight_paths, *matrix_paths]}
    failed: list[dict] = []
    for path in sorted(args.artifact_root.rglob("qwen*.json")):
        group = _group(args.artifact_root, path)
        key = (group, path.name)
        if key in active:
            continue
        prior = existing.get(key, {})
        failed.append(_reference(path, group, str(prior.get("reason") or _default_reason(group))))
    for path in sorted(args.artifact_root.rglob("ai-disabled-*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("exit_code") != 0:
            failed.append(_ai_disabled_failure_reference(path, _group(args.artifact_root, path), raw))
    probe_group = "runtime-probe-001"
    probe_path = args.artifact_root / probe_group / "ollama-runtime-probe.json"
    probe_raw = json.loads(probe_path.read_text(encoding="utf-8"))
    document = {
        "schema_version": "1.1", "evidence_id": old["evidence_id"], "process_package_version": "0.2.0",
        "adapter": {"family": "qwen-class", "version": "1.0", "authority": "advisory-only"},
        "model": {"family": "qwen-class", "name": "qwen3.5:9b", "digest": "6488c96fa5fa", "runtime": "Ollama", "runtime_version": "0.30.11", "actual_model_run": True},
        "raw_artifact": old["raw_artifact"], "source": old["source"],
        "limitations": ["qwen3.5:9b is a family-level proxy for the target-environment Qwen3.6-35B model, not equivalence proof.", "DeepSeek-family certification remains mandatory before work item 2.11 can close."],
        "ai_disabled": old["ai_disabled"], "failed_attempts": failed,
        "runtime_probe": {
            "result": "passed", "raw_group": probe_group, "raw_logical_artifact_id": "ollama-runtime-probe",
            "raw_filename": probe_path.name, "raw_sha256": _sha(probe_path), "runtime_version": probe_raw["runtime_version"],
            "model_tag": probe_raw["model_tag"], "model_digest": probe_raw["model_digest"], "endpoint": probe_raw["endpoint"],
            "adapter_version": probe_raw["adapter_version"], "process_package_version": probe_raw["process_package_version"],
        },
        "preflight": {"actual_model_run": True, "raw_group": args.preflight_group, "cases": [_row(path, args.preflight_group, repository_root, cases[json.loads(path.read_text(encoding="utf-8"))["case"]["id"]]) for path in preflight_paths]},
        "matrix": {"actual_model_run": True, "raw_group": args.matrix_group, "cases": [_row(path, args.matrix_group, repository_root, cases[json.loads(path.read_text(encoding="utf-8"))["case"]["id"]]) for path in matrix_paths]},
        "deepseek": {"status": "planned-not-executed", "closure_effect": "work item 2.11 remains in_progress"},
    }
    for section in ("preflight", "matrix"):
        for row in document[section]["cases"]:
            row["endpoint"] = probe_raw["endpoint"]
            row["runtime_probe_sha256"] = document["runtime_probe"]["raw_sha256"]
    args.output.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
