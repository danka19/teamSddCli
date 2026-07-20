#!/usr/bin/env python3
"""Collect deterministic evidence for human archive review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import archive_change, load_yaml_input, prepare_archive


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change", type=Path)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parents[1] / "process")
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--archive-date")
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    approval = load_yaml_input(args.approval) if args.approval else None
    if args.apply:
        if args.archive_root is None or args.archive_date is None or approval is None:
            parser.error("--apply requires --archive-root, --archive-date, and --approval")
        operation = lambda: archive_change(
            args.package_root,
            args.change,
            archive_root=args.archive_root,
            archive_date=args.archive_date,
            approval=approval,
        )
    else:
        operation = lambda: prepare_archive(
            args.package_root,
            args.change,
            archive_root=args.archive_root,
            archive_date=args.archive_date,
            approval=approval,
        )
    return execute(operation, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
