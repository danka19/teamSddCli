#!/usr/bin/env python3
"""Check that onboarding guidance was generated from the current route catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.guided_workflow import DEFAULT_CATALOG, load_catalog


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GUIDE = ROOT / "docs" / "runbooks" / "GUIDED_OWNER_WORKFLOW.md"
MARKER = "<!-- guided-catalog-sha256: "


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--guide", type=Path, default=DEFAULT_GUIDE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        load_catalog(args.catalog)
        expected = hashlib.sha256(args.catalog.read_bytes()).hexdigest()
        guide = args.guide.read_text(encoding="utf-8")
        marker = f"{MARKER}{expected} -->"
        if marker not in guide:
            raise ValueError("guide marker does not match catalog")
    except (OSError, UnicodeError, ValueError):
        payload = {"operation": "validate-guided-owner-workflow", "status": "invalid"}
        print(json.dumps(payload, sort_keys=True) if args.json else "Guided owner workflow: invalid")
        return 1
    payload = {
        "operation": "validate-guided-owner-workflow",
        "status": "valid",
        "guide": "docs/runbooks/GUIDED_OWNER_WORKFLOW.md",
        "catalog": "process/catalogs/guided-owner-workflow.yaml",
    }
    print(json.dumps(payload, sort_keys=True) if args.json else "Guided owner workflow: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
