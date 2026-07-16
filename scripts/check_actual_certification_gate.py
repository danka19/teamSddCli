"""Read-only deterministic gate for one actual-model phase summary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.actual_certification import validate_phase_gate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--phase", choices=("preflight", "matrix"), required=True)
    parser.add_argument("--model-family", choices=("qwen-class", "deepseek-class"), required=True)
    parser.add_argument("--adapter-version", required=True)
    parser.add_argument("--expected-count", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        summary = json.loads(args.result.read_text(encoding="utf-8"))
        diagnostics = validate_phase_gate(
            summary,
            args.artifact_root,
            args.phase,
            args.model_family,
            args.adapter_version,
            args.expected_count,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "blocked", "diagnostics": ["actual-model.gate-malformed"], "detail": str(error)}, sort_keys=True))
        return 3
    if not diagnostics:
        print(json.dumps({"status": "passed", "diagnostics": []}, sort_keys=True))
        return 0
    completed_failure = set(diagnostics) == {"actual-model.gate-case-failed"}
    status = "failed" if completed_failure else "blocked"
    print(json.dumps({"status": status, "diagnostics": diagnostics}, sort_keys=True))
    return 1 if completed_failure else 3


if __name__ == "__main__":
    raise SystemExit(main())
