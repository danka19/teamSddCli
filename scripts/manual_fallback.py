#!/usr/bin/env python3
"""Build the deterministic AI-disabled fallback plan for unavailable surfaces."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import manual_fallback_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unavailable", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return execute(
        lambda: {"operation": "manual-fallback", **manual_fallback_plan(set(args.unavailable))},
        args.json,
    )


if __name__ == "__main__":
    raise SystemExit(main())
