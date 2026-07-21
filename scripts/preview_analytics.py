#!/usr/bin/env python3
"""Read and preview a typed analytics package without external actions."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.analytics_artifacts import preview_analytics, validate_analytics_package


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = validate_analytics_package(args.package)
    payload = preview_analytics(args.package, report)
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True) if args.json else payload["status"])
    return 0 if report["status"] == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
