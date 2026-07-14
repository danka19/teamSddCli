"""Build an authority-labelled weak-model read pack without invoking a model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.weak_model_kit import build_read_pack


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("request")
    parser.add_argument("--repository-root", default=str(ROOT))
    parser.add_argument("--process-root", default=str(ROOT / "process"))
    args = parser.parse_args(argv)
    try:
        request = yaml.safe_load(Path(args.request).read_text(encoding="utf-8"))
        if not isinstance(request, dict):
            raise ValueError("request must be a mapping")
        report = build_read_pack(Path(args.repository_root), Path(args.process_root), request)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as error:
        print(json.dumps({"status": "usage", "diagnostics": [{"code": "read-pack.usage", "detail": str(error)}]}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "ready" else 3


if __name__ == "__main__":
    raise SystemExit(main())

