"""Thin CLI for deterministic fixture certification and coverage reporting."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.certification import CertificationError, build_coverage_report, certify_release


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        evidence = certify_release(root, args.catalog or root / "process/certification/cases.yaml", args.raw_output, check=args.check)
        coverage = build_coverage_report(root, args.coverage or root / "process/certification/coverage.yaml")
        result = {"status": evidence["status"], "evidence": evidence, "coverage": coverage}
    except (CertificationError, OSError, ValueError) as error:
        result = {"status": "blocked", "diagnostics": [{"code": str(error)}]}
        print(json.dumps(result, sort_keys=True))
        return 3
    print(json.dumps(result, sort_keys=True))
    return 0 if evidence["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
