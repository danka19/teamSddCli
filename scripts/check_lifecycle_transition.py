#!/usr/bin/env python3
"""Check a lifecycle transition without mutating the change package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.lifecycle import check_transition
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
    parser.add_argument("--to", required=True, dest="target_state")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument(
        "--process-root",
        type=Path,
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
                    "code": "lifecycle.usage",
                    "message": "Invalid command arguments.",
                }],
            }, sort_keys=True))
        return 2

    try:
        change_path = args.change / "change.yaml" if args.change.is_dir() else args.change
        document = _load(change_path)
        input_diagnostics = validate_gate_input(document, args.process_root)
        if input_diagnostics:
            payload = {
                "schema_version": "1.0",
                "status": "error",
                "diagnostics": input_diagnostics,
            }
            print(
                json.dumps(payload, sort_keys=True)
                if args.json_output else "Transition: error"
            )
            return 3
        config = _load(args.config)
        manifest = _load(args.process_root / "policies" / "manifest.yaml")
        result = validate_policy_bundle(args.process_root, manifest, config, None)
        if result.snapshot is None:
            payload = {
                "schema_version": "1.0",
                "status": "policy-contract-error",
                "diagnostics": [item.as_dict() for item in result.diagnostics],
            }
            print(
                json.dumps(payload, sort_keys=True)
                if args.json_output else "Transition: policy-contract-error"
            )
            return 3
        report = check_transition(document, args.target_state, result.snapshot)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
        payload = {
            "schema_version": "1.0",
            "status": "error",
            "diagnostics": [{
                "code": "lifecycle.input-invalid",
                "message": type(error).__name__,
            }],
        }
        print(json.dumps(payload, sort_keys=True) if args.json_output else "Transition: error")
        return 3

    print(
        json.dumps(report.as_dict(), sort_keys=True)
        if args.json_output else report.render_human()
    )
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
