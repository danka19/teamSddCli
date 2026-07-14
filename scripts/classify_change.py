#!/usr/bin/env python3
"""Evaluate schema-v2 change classification from the pinned policy set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.classification import evaluate_classification
from process.validators.policy_validation import validate_policy_bundle


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document must be a mapping")
    return value


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="Current classifications: minor, major, hotfix.",
    )
    parser.add_argument("change", type=Path)
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
                "diagnostics": [{"code": "classification.usage", "message": "Invalid command arguments."}],
            }, sort_keys=True))
        return 2
    try:
        change_path = args.change / "change.yaml" if args.change.is_dir() else args.change
        document = _load(change_path)
        config = _load(args.config)
        manifest = _load(args.process_root / "policies" / "manifest.yaml")
        policy = validate_policy_bundle(args.process_root, manifest, config, None)
        if policy.snapshot is None:
            payload = {
                "schema_version": "1.0",
                "status": "blocked",
                "diagnostics": [item.as_dict() for item in policy.diagnostics],
            }
            print(json.dumps(payload, sort_keys=True) if args.json_output else "Classification: blocked")
            return 1
        report = evaluate_classification(document, policy.snapshot)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
        payload = {
            "schema_version": "1.0",
            "status": "error",
            "diagnostics": [{
                "code": "classification.input-invalid",
                "message": type(error).__name__,
            }],
        }
        print(json.dumps(payload, sort_keys=True) if args.json_output else "Classification: error")
        return 3
    print(
        json.dumps(report.as_dict(), sort_keys=True)
        if args.json_output else report.render_human()
    )
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
