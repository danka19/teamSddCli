#!/usr/bin/env python3
"""Create one draft class-aware change from the versioned package template."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import create_change


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--classification", required=True, choices=("minor", "major", "hotfix"))
    parser.add_argument("--type", dest="change_type", required=True, choices=("new_feature", "behavior_change", "bugfix", "refactor", "docs_only", "config_ops"))
    parser.add_argument("--changes-root", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1] / "process")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return execute(lambda: create_change(args.package_root, args.changes_root, change_id=args.change_id, title=args.title, classification=args.classification, change_type=args.change_type), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
