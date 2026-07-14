"""Validate discovered SDD process configuration before gated work."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from process.validators.config_discovery import default_runtime_probe, validate_configuration
from process.validators.config_validation import Diagnostic, ValidationResult


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("start", help="Repository directory where discovery starts.")
    parser.add_argument(
        "--registry", action="append", default=[], metavar="ID=PATH",
        help="Explicit repeatable repository registry mapping.",
    )
    parser.add_argument("--json", action="store_true", help="Emit one JSON result object.")
    return parser.parse_args(argv)


def main(
    argv: list[str] | None = None,
    *,
    runtime_probe: Callable[[], str] | None = None,
    stdout: Callable[[str], object] = print,
    stderr: Callable[[str], object] | None = None,
) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    error_output = stderr or (lambda message: print(message, file=sys.stderr))
    start = Path(args.start)
    usage_error = False
    try:
        mappings = parse_registry(args.registry)
    except ValueError:
        usage_error = True
        result = ValidationResult()
        result.add(Diagnostic(
            "usage.registry", "usage",
            "A registry mapping is malformed or duplicates an identifier.", 0,
            hint="Pass each mapping once as --registry ID=PATH.",
        ))
    if not usage_error and not start.is_dir():
        usage_error = True
        result = ValidationResult()
        result.add(Diagnostic(
            "usage.start-directory", "usage",
            "The explicit start directory does not exist or is not a directory.", 0,
            hint="Pass an existing repository directory.",
        ))
    elif not usage_error:
        try:
            result = validate_configuration(
                start.resolve(), mappings, runtime_probe or default_runtime_probe
            )
        except Exception:
            result = ValidationResult()
            result.add(Diagnostic(
                "internal.validator-failure", "operational",
                "The validator failed unexpectedly without exposing internal paths or data.", 10,
                hint="Re-run focused tests and inspect the local traceback in a controlled environment.",
            ))
    if args.json:
        stdout(json.dumps(result.as_payload(), sort_keys=True, separators=(",", ":")))
    else:
        if result.diagnostics:
            for diagnostic in result.sorted_diagnostics():
                location = " ".join(
                    item for item in (diagnostic.source, diagnostic.pointer) if item
                )
                prefix = f"ERROR [{diagnostic.code}] {diagnostic.category}"
                message = f"{prefix} {location}: {diagnostic.message}" if location else f"{prefix}: {diagnostic.message}"
                if diagnostic.hint:
                    message += f" Hint: {diagnostic.hint}"
                error_output(message)
        else:
            stdout(f"OK [config.valid] compatible {result.mode} configuration")
    return 2 if usage_error else result.exit_code


def parse_registry(values: list[str]) -> dict[str, Path]:
    mappings: dict[str, Path] = {}
    for value in values:
        identifier, separator, path = value.partition("=")
        if (
            not separator
            or not identifier
            or not path
            or identifier in mappings
            or not identifier[0].islower()
            or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-" for character in identifier)
        ):
            raise ValueError("invalid registry mapping")
        mappings[identifier] = Path(path).resolve()
    return mappings


if __name__ == "__main__":
    raise SystemExit(main())
