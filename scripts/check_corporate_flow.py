"""Thin check-only corporate-flow CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.corporate_flow import (
    evaluate_corporate_flow,
    validate_corporate_flow_input,
    validate_evaluation_cutoff,
)
from process.validators.config_validation import secret_diagnostics
from process.validators.owners import owner_registry_diagnostics
from process.validators.policy_validation import validate_policy_bundle
from process.validators.tech_lead import validate_owner_registry_input


DEFAULT_PROCESS = Path(__file__).resolve().parents[1] / "process"


class UsageArgumentError(ValueError):
    pass


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
        print(json.dumps({"schema_version": "1.0", "status": "usage", "diagnostics": [{"code": "corporate-flow.usage"}]}, sort_keys=True))
        return 2
    diagnostics = validate_corporate_flow_input(document, process_root)
    if diagnostics:
        return _error(diagnostics, args.json)
    secret_findings = secret_diagnostics(document, "corporate-flow-input", stage=3)
    if secret_findings:
        return _error([row.as_dict() for row in secret_findings], args.json)
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
        return _error([{"code": "corporate-flow.policy-contract-invalid"}], args.json)
    owner_diagnostics = owner_registry_diagnostics(owners, projects, policy.snapshot)
    if owner_diagnostics:
        return _error([row.as_dict() for row in owner_diagnostics], args.json)
    report = evaluate_corporate_flow(
        document, owners, projects, policy.snapshot, as_of=args.as_of
    )
    print(json.dumps(report.as_dict(), sort_keys=True) if args.json else report.render_human())
    return report.exit_code


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("document root must be a mapping")
    return value


def _error(diagnostics: list[dict[str, Any]], json_output: bool) -> int:
    payload = {"schema_version": "1.0", "status": "error", "diagnostics": diagnostics}
    print(json.dumps(payload, sort_keys=True) if json_output else "Corporate flow: error")
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
