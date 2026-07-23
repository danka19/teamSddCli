#!/usr/bin/env python3
"""Validate the canonical operations catalog and its derived views."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
if __package__ in {None, ""}: sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from process.operations_catalog import validate_operations_catalog
ROOT = Path(__file__).resolve().parents[1]
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--json", action="store_true"); args = parser.parse_args(argv)
    errors = validate_operations_catalog(ROOT); payload = {"operation": "validate-operations-catalog", "status": "valid" if not errors else "invalid", "errors": errors}
    print(json.dumps(payload, sort_keys=True) if args.json else f"Operations catalog: {payload['status']}")
    return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
