#!/usr/bin/env python3
"""Collect deterministic evidence for human archive review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import prepare_archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change", type=Path)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1] / "process")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    return execute(lambda: prepare_archive(args.package_root, args.change), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
