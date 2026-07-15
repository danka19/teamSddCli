"""Run one append-only Phase 2.11 certification slice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.actual_certification import (
    ActualCertificationError,
    execute_ai_disabled,
    execute_model_catalog,
    probe_ollama,
)


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--phase", choices=("ai-disabled", "runtime-probe", "preflight", "matrix"), required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    catalog_name = "ai-disabled-walkthroughs.yaml" if args.phase == "ai-disabled" else "qwen-matrix.yaml"
    try:
        catalog = yaml.safe_load((root / "process/certification" / catalog_name).read_text(encoding="utf-8"))
        if not isinstance(catalog, dict):
            raise ActualCertificationError("actual-model.invalid-catalog")
        if args.phase == "ai-disabled":
            evidence = execute_ai_disabled(root, catalog, args.raw_output)
        elif args.phase == "runtime-probe":
            evidence = probe_ollama(root, catalog, args.raw_output)
        else:
            evidence = execute_model_catalog(root, root / "process", catalog, args.raw_output, phase=args.phase)
    except (OSError, UnicodeError, yaml.YAMLError, ActualCertificationError) as error:
        print(json.dumps({"status": "blocked", "diagnostic": str(error)}, sort_keys=True))
        return 3
    print(json.dumps(evidence, sort_keys=True, indent=2))
    return 0 if evidence.get("status", evidence.get("result")) == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
