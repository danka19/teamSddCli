"""Check whether AI-assisted tasks are safe to launch concurrently."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.weak_model_kit import validate_parallel_plan


class UsageError(ValueError):
    pass


class ContractParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def main(argv: list[str] | None = None) -> int:
    parser = ContractParser(add_help=False)
    parser.add_argument("plan")
    try:
        args = parser.parse_args(argv)
        plan = yaml.safe_load(Path(args.plan).read_text(encoding="utf-8"))
        if not isinstance(plan, dict):
            raise ValueError("plan must be a mapping")
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, TypeError, KeyError, UsageError):
        print(json.dumps({"status": "usage", "diagnostics": [{"code": "parallel.usage"}]}, sort_keys=True))
        return 2
    report = validate_parallel_plan(plan)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "parallel-safe" else 3


if __name__ == "__main__":
    raise SystemExit(main())
