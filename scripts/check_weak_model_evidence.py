"""Reject unsupported weak-model completion and authority claims."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.weak_model_kit import validate_operation_evidence


ROOT = Path(__file__).resolve().parents[1]


class UsageError(ValueError):
    pass


class ContractParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def main(argv: list[str] | None = None) -> int:
    parser = ContractParser(add_help=False)
    parser.add_argument("evidence")
    parser.add_argument("--launch", required=True)
    parser.add_argument("--read-pack", required=True)
    parser.add_argument("--process-root", default=str(ROOT / "process"))
    try:
        args = parser.parse_args(argv)
        evidence = yaml.safe_load(Path(args.evidence).read_text(encoding="utf-8"))
        launch = yaml.safe_load(Path(args.launch).read_text(encoding="utf-8"))
        read_pack = yaml.safe_load(Path(args.read_pack).read_text(encoding="utf-8"))
        if not all(isinstance(item, dict) for item in (evidence, launch, read_pack)):
            raise ValueError("documents must be mappings")
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, TypeError, KeyError, UsageError):
        print(json.dumps({"status": "usage", "diagnostics": [{"code": "evidence.usage"}]}, sort_keys=True))
        return 2
    diagnostics = validate_operation_evidence(evidence, launch, read_pack, Path(args.process_root))
    print(json.dumps({"status": "accepted-draft" if not diagnostics else "rejected", "diagnostics": diagnostics}, sort_keys=True))
    return 0 if not diagnostics else 3


if __name__ == "__main__":
    raise SystemExit(main())
