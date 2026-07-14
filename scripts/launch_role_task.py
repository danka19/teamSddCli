"""Select the exact role instruction and output boundary outside the model."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.weak_model_kit import ContractError, build_role_launch


ROOT = Path(__file__).resolve().parents[1]


class UsageError(ValueError):
    pass


class ContractParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def main(argv: list[str] | None = None) -> int:
    parser = ContractParser(add_help=False)
    parser.add_argument("read_pack")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--repository-root", default=str(ROOT))
    parser.add_argument("--process-root", default=str(ROOT / "process"))
    try:
        args = parser.parse_args(argv)
        read_pack = yaml.safe_load(Path(args.read_pack).read_text(encoding="utf-8"))
        if not isinstance(read_pack, dict):
            raise ValueError("read pack must be a mapping")
        launch = build_role_launch(
            Path(args.repository_root), Path(args.process_root), read_pack,
            Path(args.read_pack).resolve().relative_to(Path(args.repository_root).resolve()).as_posix(),
            args.evidence,
        )
    except UsageError:
        print(json.dumps({"status": "usage", "diagnostics": [{"code": "role-launch.usage"}]}, sort_keys=True))
        return 2
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, ContractError, TypeError, KeyError):
        print(json.dumps({"status": "blocked", "diagnostics": [{"code": "role-launch.blocked"}]}, sort_keys=True))
        return 3
    print(json.dumps(launch, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
