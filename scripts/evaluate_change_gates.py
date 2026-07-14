#!/usr/bin/env python3
"""Evaluate one or all class-aware change gates without mutating lifecycle state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.artifact_gates import SUPPORTED_GATES, evaluate_gate
from process.validators.gate_input import validate_gate_input
from process.validators.policy_validation import validate_policy_bundle


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document must be a mapping")
    return value


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change", type=Path)
    parser.add_argument(
        "--gate", action="append", choices=SUPPORTED_GATES,
        help="Evaluate one named gate; repeat for several. Defaults to all six reports.",
    )
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--process-root", type=Path,
        default=Path(__file__).resolve().parents[1] / "process",
    )
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    raw_args = sys.argv[1:] if argv is None else argv
    try:
        args = parse_args(raw_args)
    except SystemExit as error:
        if error.code == 0:
            return 0
        if "--json" in raw_args:
            print(json.dumps({
                "schema_version": "1.0",
                "status": "usage",
                "diagnostics": [{
                    "code": "gate.usage",
                    "message": "Invalid command arguments.",
                }],
            }, sort_keys=True))
        return 2

    try:
        change_path = args.change / "gate-input.yaml" if args.change.is_dir() else args.change
        document = _load(change_path)
        diagnostics = validate_gate_input(document, args.process_root)
        if diagnostics:
            return _emit_error("error", diagnostics, args.json_output)
        config = _load(args.config)
        manifest = _load(args.process_root / "policies" / "manifest.yaml")
        policy = validate_policy_bundle(args.process_root, manifest, config, None)
        if policy.snapshot is None:
            diagnostics = [{
                "code": item.code,
                "message": item.message,
            } for item in sorted(
                policy.diagnostics, key=lambda item: (item.code, item.pointer or "")
            )]
            return _emit_error(
                "policy-contract-error", diagnostics, args.json_output
            )
        selected = tuple(args.gate or SUPPORTED_GATES)
        reports = [
            evaluate_gate(document, policy.snapshot, gate) for gate in selected
        ]
    except (OSError, UnicodeError, ValueError, yaml.YAMLError):
        return _emit_error("error", [{
            "code": "gate.input-invalid",
            "message": "A required local input is missing or invalid.",
        }], args.json_output)

    if any(
        gap["code"] == "gate.policy-contract-invalid"
        for report in reports
        for gap in report.as_dict()["blocking_gaps"]
    ):
        return _emit_error("policy-contract-error", [{
            "code": "gate.policy-contract-invalid",
            "message": "The resolved policy contract is incomplete or incompatible.",
        }], args.json_output)

    blocked = any(report.exit_code == 1 for report in reports)
    payload = {
        "schema_version": "1.0",
        "status": "blocked" if blocked else "ready",
        "change_id": document.get("id"),
        "reports": [report.as_dict() for report in reports],
        "decision_only": True,
        "lifecycle_mutated": False,
    }
    if args.json_output:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"Gate evaluation: {'blocked' if blocked else 'ready'}")
        for report in reports:
            print(report.render_human())
    return 1 if blocked else 0


def _emit_error(
    status: str, diagnostics: list[dict[str, str]], json_output: bool
) -> int:
    payload = {
        "schema_version": "1.0",
        "status": status,
        "diagnostics": diagnostics,
    }
    print(
        json.dumps(payload, sort_keys=True)
        if json_output else f"Gate evaluation: {status}"
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
