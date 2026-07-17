#!/usr/bin/env python3
"""Build or validate an immutable transfer release candidate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.errors import OperationError
from process.release_candidate import ReleaseInputs, build_release_candidate, validate_release_manifest


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise OperationError("input-invalid", message, exit_code=3)


def _mapping(path: Path) -> dict:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("input-invalid", "required input is missing or malformed", exit_code=3) from error
    if not isinstance(value, dict):
        raise OperationError("input-invalid", "required input root must be a mapping", exit_code=3)
    return value


def _parser() -> Parser:
    parser = Parser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    build = modes.add_parser("build")
    build.add_argument("--root", required=True, type=Path)
    build.add_argument("--destination", required=True, type=Path)
    build.add_argument("--inputs", required=True, type=Path)
    validate = modes.add_parser("validate")
    validate.add_argument("--candidate", required=True, type=Path)
    validate.add_argument("--manifest", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        if args.mode == "build":
            values = _mapping(args.inputs)
            try:
                limitations = values.get("known_limitations", [])
                if not isinstance(limitations, list):
                    raise TypeError("known_limitations must be a list")
                inputs = ReleaseInputs(
                    release_id=values["release_id"],
                    known_limitations=tuple(limitations),
                    raw_artifact_root=Path(values["raw_artifact_root"]),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise OperationError("input-invalid", "release input fields are malformed", exit_code=3) from error
            result = build_release_candidate(args.root, args.destination, inputs)
            payload = {"operation": "build-release-candidate", "status": "created", "release_id": result["release_id"], "payload_sha256": result["payload_sha256"]}
        else:
            manifest = _mapping(args.manifest)
            payload = validate_release_manifest(args.candidate, manifest)
        print(json.dumps(payload, sort_keys=True))
        return 0
    except OperationError as error:
        print(json.dumps({"status": "rejected" if error.exit_code == 1 else "operational-error", "diagnostics": [{"code": error.code}]} , sort_keys=True))
        return error.exit_code
    except Exception:
        print(json.dumps({"status": "operational-error", "diagnostics": [{"code": "operation-failed"}]}, sort_keys=True))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
