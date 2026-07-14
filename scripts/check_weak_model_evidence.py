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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence")
    args = parser.parse_args(argv)
    try:
        evidence = yaml.safe_load(Path(args.evidence).read_text(encoding="utf-8"))
        if not isinstance(evidence, dict):
            raise ValueError("evidence must be a mapping")
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
        print(json.dumps({"status": "usage", "diagnostics": [{"code": "evidence.usage", "detail": str(error)}]}, sort_keys=True))
        return 2
    diagnostics = validate_operation_evidence(evidence)
    print(json.dumps({"status": "accepted-draft" if not diagnostics else "rejected", "diagnostics": diagnostics}, sort_keys=True))
    return 0 if not diagnostics else 3


if __name__ == "__main__":
    raise SystemExit(main())

