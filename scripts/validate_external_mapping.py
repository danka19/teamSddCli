#!/usr/bin/env python3
"""Validate the distinct external workflow-state mapping without mutation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import load_yaml_input, validate_external_mapping


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return execute(
        lambda: {"operation": "validate-external-mapping", **validate_external_mapping(load_yaml_input(args.input))},
        args.json,
    )


if __name__ == "__main__":
    raise SystemExit(main())
