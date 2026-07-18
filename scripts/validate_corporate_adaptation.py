"""Validate one corporate-adaptation document or the shipped template package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from process.corporate_adaptation import (
    CONTRACTS,
    AdaptationResult,
    validate_document,
    validate_package_templates,
)
from process.validators.config_validation import Diagnostic


class UsageArgumentError(ValueError):
    """A parser error rendered through the stable result contract."""


class ContractArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageArgumentError(message)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = ContractArgumentParser(description=__doc__)
    parser.add_argument("document", nargs="?", help="YAML document to validate.")
    parser.add_argument("--package", action="store_true", help="Validate all shipped templates and examples.")
    parser.add_argument("--process-root", default=str(REPO_ROOT / "process"), help="Versioned process package root.")
    parser.add_argument("--kind", choices=sorted(CONTRACTS), help="Explicit contract kind; defaults to the document kind.")
    parser.add_argument("--external-package", action="store_true", help="Reject private values allowed only in real local configuration.")
    parser.add_argument("--json", action="store_true", help="Emit one JSON result object.")
    args = parser.parse_args(argv)
    if args.package == bool(args.document):
        raise UsageArgumentError("pass exactly one document or --package")
    return args


def main(
    argv: list[str] | None = None,
    *,
    stdout: Callable[[str], object] = print,
    stderr: Callable[[str], object] | None = None,
) -> int:
    error_output = stderr or (lambda message: print(message, file=sys.stderr))
    raw_args = sys.argv[1:] if argv is None else argv
    json_output = "--json" in raw_args
    try:
        args = parse_args(raw_args)
    except UsageArgumentError:
        result = AdaptationResult()
        result.diagnostics.append(Diagnostic(
            "adaptation.usage", "usage",
            "Pass exactly one YAML document or --package using documented options.", 0,
        ))
        if json_output:
            stdout(json.dumps(result.as_payload(), sort_keys=True, separators=(",", ":")))
        else:
            error_output("ERROR [adaptation.usage] invalid command arguments")
        return 2
    except SystemExit as error:
        return int(error.code)
    process_root = Path(args.process_root)
    if args.package:
        result = validate_package_templates(process_root)
    else:
        try:
            document = yaml.safe_load(Path(args.document).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            result = AdaptationResult()
            result.diagnostics.append(Diagnostic(
                "adaptation.document-invalid", "operational",
                "The requested YAML document is missing or malformed.", 0,
            ))
        else:
            inferred_kind = document.get("kind", "unknown") if isinstance(document, dict) else "unknown"
            result = validate_document(
                document,
                args.kind or str(inferred_kind),
                process_root,
                external_package=args.external_package,
            )
    if args.json:
        stdout(json.dumps(result.as_payload(), sort_keys=True, separators=(",", ":")))
    elif result.diagnostics:
        for item in result.sorted_diagnostics():
            error_output(f"ERROR [{item.code}] {item.message}")
    else:
        stdout(f"OK [adaptation.valid] {result.kind}")
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
