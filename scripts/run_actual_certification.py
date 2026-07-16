"""Run one append-only Phase 2.11 certification slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.actual_certification import (
    ActualCertificationError,
    execute_ai_disabled,
    execute_model_catalog,
    probe_ollama,
    validate_phase_gate,
)


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--phase", choices=("ai-disabled", "runtime-probe", "preflight", "matrix"), required=True)
    parser.add_argument("--model-family", choices=("qwen-class", "deepseek-class"), default="qwen-class")
    parser.add_argument("--result-output", type=Path)
    parser.add_argument("--preflight-result", type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog_name = "ai-disabled-walkthroughs.yaml" if args.phase == "ai-disabled" else "qwen-matrix.yaml"
    try:
        if args.phase in {"preflight", "matrix"} and args.result_output is None:
            raise ActualCertificationError("actual-model.result-output-required")
        if args.phase == "matrix" and args.preflight_result is None:
            raise ActualCertificationError("actual-model.preflight-result-required")
        if args.result_output is not None and args.result_output.exists():
            raise ActualCertificationError("actual-model.result-output-exists")
        catalog = yaml.safe_load((root / "process/certification" / catalog_name).read_text(encoding="utf-8"))
        if not isinstance(catalog, dict):
            raise ActualCertificationError("actual-model.invalid-catalog")
        if args.phase == "ai-disabled":
            evidence = execute_ai_disabled(root, catalog, args.raw_output)
        elif args.phase == "runtime-probe":
            evidence = probe_ollama(root, catalog, args.raw_output, model_family=args.model_family)
        else:
            if args.phase == "matrix":
                preflight = json.loads(args.preflight_result.read_text(encoding="utf-8"))
                gate_diagnostics = validate_phase_gate(
                    preflight,
                    args.raw_output.parent,
                    "preflight",
                    args.model_family,
                    "2.0",
                    5,
                )
                if gate_diagnostics:
                    raise ActualCertificationError("actual-model.preflight-gate")
            evidence = execute_model_catalog(root, root / "process", catalog, args.raw_output, phase=args.phase, model_family=args.model_family)
        if args.result_output is not None:
            with args.result_output.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(evidence, handle, sort_keys=True, indent=2)
                handle.write("\n")
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError, ActualCertificationError) as error:
        print(json.dumps({"status": "blocked", "diagnostic": str(error)}, sort_keys=True))
        return 3
    print(json.dumps(evidence, sort_keys=True, indent=2))
    return 0 if evidence.get("status", evidence.get("result")) == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
