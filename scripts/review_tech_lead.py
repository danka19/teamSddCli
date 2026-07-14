"""Thin deterministic Tech Lead review CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.policy_validation import validate_policy_bundle
from process.validators.owners import owner_registry_diagnostics
from process.validators.tech_lead import (
    evaluate_tech_lead_review,
    validate_evaluation_cutoff,
    validate_owner_registry_input,
    validate_tech_lead_input,
)


DEFAULT_PROCESS = Path(__file__).resolve().parents[1] / "process"


class UsageArgumentError(ValueError):
    """Parser failure rendered only through the stable CLI contract."""


class ContractArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageArgumentError(message)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = ContractArgumentParser(add_help=False)
    parser.add_argument("input")
    parser.add_argument("--owners", required=True)
    parser.add_argument("--projects", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--process-root", default=str(DEFAULT_PROCESS))
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        process_root = Path(args.process_root)
        document = _load(Path(args.input))
        owners = _load(Path(args.owners))
        projects = _load(Path(args.projects))
        config = _load(Path(args.config))
    except (SystemExit, UsageArgumentError, OSError, UnicodeError, yaml.YAMLError, ValueError):
        print(json.dumps({"schema_version": "1.0", "status": "usage", "diagnostics": [{"code": "tech-lead.usage"}]}, sort_keys=True))
        return 2
    diagnostics = validate_tech_lead_input(document, process_root)
    if diagnostics:
        return _error(diagnostics, args.json)
    diagnostics = validate_owner_registry_input(owners, process_root)
    if diagnostics:
        return _error(diagnostics, args.json)
    diagnostics = validate_evaluation_cutoff(args.as_of)
    if diagnostics:
        return _error(diagnostics, args.json)
    policy = validate_policy_bundle(
        process_root, _load(process_root / "policies" / "manifest.yaml"), config, None
    )
    if policy.snapshot is None:
        return _error([{"code": "tech-lead.policy-contract-invalid"}], args.json)
    owner_diagnostics = owner_registry_diagnostics(owners, projects, policy.snapshot)
    if owner_diagnostics:
        return _error([item.as_dict() for item in owner_diagnostics], args.json)
    report = evaluate_tech_lead_review(
        document, owners, projects, policy.snapshot, as_of=args.as_of
    )
    payload = report.as_dict()
    print(json.dumps(payload, sort_keys=True) if args.json else report.render_human())
    return report.exit_code


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a mapping")
    return value


def _error(diagnostics: list[dict[str, Any]], json_output: bool) -> int:
    payload = {"schema_version": "1.0", "status": "error", "diagnostics": diagnostics}
    print(json.dumps(payload, sort_keys=True) if json_output else "Tech Lead review: error")
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
