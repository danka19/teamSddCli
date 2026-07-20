#!/usr/bin/env python3
"""Return a catalog-declared next workflow step without mutating process state."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.guided_workflow import DEFAULT_CATALOG, guide
from process.operation_cli import execute


def _facts(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key or not item or key in result:
            raise argparse.ArgumentTypeError("facts must be unique key=value pairs")
        result[key] = item
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("situation")
    parser.add_argument("--fact", action="append", default=[])
    parser.add_argument("--unavailable", action="append", default=[])
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        facts = _facts(args.fact)
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))
    payload = guide(args.situation, facts, set(args.unavailable), catalog_path=args.catalog)
    return execute(lambda: payload, args.json) if payload["status"] == "guided" else _render_block(payload, args.json)


def _render_block(payload: dict, json_output: bool) -> int:
    import json
    print(json.dumps(payload, sort_keys=True) if json_output else "GUIDANCE: blocked")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
