#!/usr/bin/env python3
"""Check or apply bounded legacy classification migration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.classification_migration import apply_migration, plan_migration


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("path", type=Path)
    check.add_argument("--json", action="store_true", dest="json_output")
    apply = subparsers.add_parser("apply")
    apply.add_argument("path", type=Path)
    apply.add_argument("--plan-digest", required=True)
    apply.add_argument("--json", action="store_true", dest="json_output")
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
                "diagnostics": [{"code": "migration.usage", "message": "Invalid command arguments."}],
            }, sort_keys=True))
        return 2
    try:
        result = (
            plan_migration(args.path)
            if args.command == "check"
            else apply_migration(args.path, expected_plan_digest=args.plan_digest)
        )
    except (OSError, UnicodeError, ValueError) as error:
        payload = {
            "schema_version": "1.0",
            "status": "error",
            "diagnostics": [{"code": "migration.input-invalid", "message": type(error).__name__}],
        }
        print(json.dumps(payload, sort_keys=True) if args.json_output else "Migration: error")
        return 3
    print(
        json.dumps(result.as_dict(), sort_keys=True)
        if args.json_output else result.render_human()
    )
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
