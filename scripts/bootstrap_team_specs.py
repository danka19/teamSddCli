#!/usr/bin/env python3
"""Bootstrap a central team-specs workspace from versioned package assets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import bootstrap_team_specs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1] / "process")
    parser.add_argument("--team-template", type=Path, default=Path(__file__).resolve().parents[1] / "templates" / "team-specs")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return execute(lambda: bootstrap_team_specs(args.package_root, args.team_template, args.destination), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
