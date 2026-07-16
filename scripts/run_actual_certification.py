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
    create_actual_certification_directory,
    execute_ai_disabled,
    execute_model_catalog,
    load_adapter_profile,
    preflight_model_execution_identity,
    probe_ollama,
    revalidate_actual_certification_destination,
    validate_phase_gate,
    validate_actual_certification_destinations,
    write_operational_result_exclusive,
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
    result_output: Path | None = None
    destination_established = False
    operation_state: dict = {
        "actual_model_run": False,
        "observed_identity": None,
    }
    try:
        if args.phase in {"runtime-probe", "preflight", "matrix"} and args.result_output is None:
            raise ActualCertificationError("actual-model.result-output-required")
        if args.phase == "matrix" and args.preflight_result is None:
            raise ActualCertificationError("actual-model.preflight-result-required")
        raw_output, result_output = validate_actual_certification_destinations(
            root, args.raw_output, args.result_output
        )
        catalog = yaml.safe_load((root / "process/certification" / catalog_name).read_text(encoding="utf-8"))
        if not isinstance(catalog, dict):
            raise ActualCertificationError("actual-model.invalid-catalog")
        preflight_observed_identity = None
        initial_observed_identity = None
        if args.phase == "matrix":
            preflight = json.loads(args.preflight_result.read_text(encoding="utf-8"))
            adapter_version = load_adapter_profile(
                root / "process", args.model_family
            )["schema_version"]
            gate_diagnostics = validate_phase_gate(
                preflight,
                raw_output.parent,
                "preflight",
                args.model_family,
                adapter_version,
                5,
            )
            if gate_diagnostics:
                raise ActualCertificationError("actual-model.preflight-gate")
            preflight_observed_identity = preflight.get("observed_identity")
            initial_observed_identity = preflight_model_execution_identity(
                root / "process",
                catalog,
                args.model_family,
                preflight_observed_identity=preflight_observed_identity,
            )
            operation_state["observed_identity"] = initial_observed_identity
        raw_output = create_actual_certification_directory(root, raw_output)
        destination_established = True
        if args.phase == "ai-disabled":
            evidence = execute_ai_disabled(
                root, catalog, raw_output, destination_guard=True
            )
        elif args.phase == "runtime-probe":
            evidence = probe_ollama(
                root,
                catalog,
                raw_output,
                model_family=args.model_family,
                destination_guard=True,
            )
        else:
            operation_state["actual_model_run"] = "unknown"
            evidence = execute_model_catalog(
                root,
                root / "process",
                catalog,
                raw_output,
                phase=args.phase,
                model_family=args.model_family,
                preflight_observed_identity=preflight_observed_identity,
                destination_guard=True,
                initial_observed_identity=initial_observed_identity,
                operation_state=operation_state,
            )
        if result_output is not None:
            revalidate_actual_certification_destination(
                root, raw_output, require_directory=True
            )
            revalidate_actual_certification_destination(
                root, result_output.parent, require_directory=True
            )
            if result_output.exists() or result_output.is_symlink():
                raise ActualCertificationError(
                    "actual-model.result-output-exists"
                )
            with result_output.open("x", encoding="utf-8", newline="\n") as handle:
                json.dump(evidence, handle, sort_keys=True, indent=2)
                handle.write("\n")
    except KeyboardInterrupt:
        error = ActualCertificationError("actual-model.interrupted")
        if (
            destination_established
            and result_output is not None
            and not result_output.exists()
        ):
            try:
                write_operational_result_exclusive(
                    result_output,
                    args.phase,
                    args.model_family,
                    str(error),
                    observed_identity=operation_state.get(
                        "observed_identity"
                    ),
                    actual_model_run=operation_state.get(
                        "actual_model_run", "unknown"
                    ),
                    repository_root=root,
                )
            except (OSError, ActualCertificationError):
                pass
        print(json.dumps({"status": "blocked", "diagnostic": str(error)}, sort_keys=True))
        return 3
    except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError, ActualCertificationError) as error:
        if (
            destination_established
            and result_output is not None
            and not result_output.exists()
        ):
            try:
                write_operational_result_exclusive(
                    result_output,
                    args.phase,
                    args.model_family,
                    str(error),
                    observed_identity=operation_state.get(
                        "observed_identity"
                    ),
                    actual_model_run=operation_state.get(
                        "actual_model_run", "unknown"
                    ),
                    repository_root=root,
                )
            except (OSError, ActualCertificationError):
                pass
        print(json.dumps({"status": "blocked", "diagnostic": str(error)}, sort_keys=True))
        return 3
    print(json.dumps(evidence, sort_keys=True, indent=2))
    return 0 if evidence.get("status", evidence.get("result")) == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
