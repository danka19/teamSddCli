#!/usr/bin/env python3
"""Check, update, or roll back a versioned process package transactionally."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.operation_cli import execute
from process.workflow_operations import (
    check_package_compatibility,
    rollback_process_package,
    update_process_package,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    update = sub.add_parser("update")
    rollback = sub.add_parser("rollback")
    for item in (check, update):
        item.add_argument("installed", type=Path)
        item.add_argument("candidate", type=Path)
        item.add_argument("config", type=Path)
        item.add_argument("--evidence", type=Path, required=True)
        item.add_argument("--json", action="store_true")
    update.add_argument("--backup-root", type=Path, required=True)
    rollback.add_argument("installed", type=Path)
    rollback.add_argument("backup", type=Path)
    rollback.add_argument("config", type=Path)
    rollback.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "check":
        op = lambda: check_package_compatibility(
            args.installed, args.candidate, args.config, upgrade_evidence=args.evidence
        )
    elif args.command == "update":
        op = lambda: update_process_package(
            args.installed,
            args.candidate,
            args.config,
            args.backup_root,
            upgrade_evidence=args.evidence,
        )
    else:
        op = lambda: rollback_process_package(args.installed, args.backup, args.config)
    return execute(op, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
