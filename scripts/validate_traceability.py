#!/usr/bin/env python3
"""Validate governance traceability and emit a canonical-ID derived view."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import validate_traceability


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    def operation():
        value = yaml.safe_load(args.input.read_text(encoding="utf-8"))
        return {"operation": "validate-traceability", **validate_traceability(value)}
    return execute(operation, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
