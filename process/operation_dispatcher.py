"""Fail-closed local dispatcher for catalog-defined P3 operations."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence
import yaml
from .guided_workflow import guide, operation_input_digest
from .errors import OperationError
from .operation_cli import execute
from .operations_catalog import DEFAULT_CATALOG, load_operations_catalog, operation_by_id

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sdd")
    sub = parser.add_subparsers(dest="command", required=True)
    def json_flag(p: argparse.ArgumentParser) -> None: p.add_argument("--json", action="store_true")
    guide_parser = sub.add_parser("guide"); guide_parser.add_argument("situation"); guide_parser.add_argument("--role"); guide_parser.add_argument("--fact", action="append", default=[]); guide_parser.add_argument("--unavailable", action="append", default=[]); json_flag(guide_parser)
    next_parser = sub.add_parser("next"); next_parser.add_argument("--change", required=True); next_parser.add_argument("--role"); json_flag(next_parser)
    op_parser = sub.add_parser("op"); op_sub = op_parser.add_subparsers(dest="op_command", required=True)
    op_list = op_sub.add_parser("list"); op_list.add_argument("--include-internal", action="store_true"); op_list.add_argument("--role"); json_flag(op_list)
    op_show = op_sub.add_parser("show"); op_show.add_argument("operation_id"); op_show.add_argument("--role"); json_flag(op_show)
    for command in ("check", "prepare", "request", "run"):
        child = sub.add_parser(command); child.add_argument("operation_id"); child.add_argument("--role"); json_flag(child)
    return parser

def _blocked(operation: str, code: str, **details: Any) -> dict[str, Any]:
    return {"operation": operation, "schema_version": "1.0", "status": "blocked", "blockers": [{"code": code, **details}], "lifecycle_mutated": False, "external_state_mutated": False}

def _facts(values: Sequence[str]) -> dict[str, str]:
    result = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key or not item: raise ValueError
        result[key] = item
    return result

def _card(item: dict[str, Any]) -> dict[str, Any]:
    fields = ("id", "title", "visibility", "allowed_roles", "inputs", "outputs", "mutation_level", "risk_level", "human_decision", "confirmation_required", "evidence", "fallback", "runbook")
    return {field: item[field] for field in fields}

def _run_entrypoint(operation: dict[str, Any], forwarded: Sequence[str]) -> dict[str, Any]:
    args = list(forwarded)
    if "--json" in args: args.remove("--json")
    args.append("--json")
    try:
        completed = subprocess.run([sys.executable, str(REPOSITORY_ROOT / operation["entrypoint"]), *args], cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False, shell=False)
    except OSError as error:
        raise OperationError("operation-spawn-failed", "catalog operation could not start", exit_code=3) from error
    if completed.returncode not in {0, 1, 3}: return {"status": "operational-error", "child_exit_code": completed.returncode, "diagnostics": [{"code": "child-operation-failed"}]}
    try: evidence = json.loads(completed.stdout)
    except json.JSONDecodeError: return {"status": "operational-error", "child_exit_code": completed.returncode, "diagnostics": [{"code": "child-output-invalid"}]}
    return {"status": "ok" if completed.returncode == 0 else "blocked" if completed.returncode == 1 else "operational-error", "child_exit_code": completed.returncode, "evidence": evidence, "diagnostics": []}

def dispatch(args: argparse.Namespace, *, catalog_path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    catalog = load_operations_catalog(catalog_path)
    operation = lambda identifier: operation_by_id(identifier, catalog_path)
    if args.command == "guide":
        try:
            facts = _facts(args.fact)
            if args.role:
                if facts.get("human_role") and facts["human_role"] != args.role:
                    raise ValueError
                facts["human_role"] = args.role
            result = guide(args.situation, facts, set(args.unavailable))
        except ValueError:
            return _blocked("sdd-guide", "invalid-context")
        result["operation"] = "sdd-guide"
        if result["status"] == "blocked": return result
        resolved = [operation(item) for item in result["commands"]]
        if any(item is None for item in resolved): return _blocked("sdd-guide", "catalog-route-unknown-operation")
        permitted = [item for item in resolved if item and result["known_facts"]["human_role"] in item["allowed_roles"]]
        if not permitted: return _blocked("sdd-guide", "role-not-permitted")
        result["commands"] = [item["id"] for item in permitted]
        return result
    if args.command == "next":
        path = Path(args.change); path = path / "change.yaml" if path.is_dir() else path
        if not path.is_file(): return _blocked("sdd-next", "missing-change")
        try: state = yaml.safe_load(path.read_text(encoding="utf-8")).get("lifecycle_state")
        except (OSError, UnicodeError, yaml.YAMLError, AttributeError): state = None
        if not isinstance(state, str) or not state: return _blocked("sdd-next", "missing-lifecycle-state")
        result = guide("existing-change", {"human_role": args.role or "", "change_id": path.parent.name, "lifecycle_state": state}, set()); result["operation"] = "sdd-next"; return result
    if args.command == "op":
        if args.op_command == "list":
            visible = {"public"} | ({"internal", "deprecated"} if args.include_internal else set())
            return {"operation": "sdd-op-list", "schema_version": "1.0", "status": "ok", "operations": [_card(item) for item in catalog["operations"] if item["visibility"] in visible and (not args.role or args.role in item["allowed_roles"])], "lifecycle_mutated": False, "external_state_mutated": False}
        item = operation(args.operation_id)
        if item is None or item["visibility"] == "forbidden": return _blocked("sdd-op-show", "unknown-operation")
        if args.role and args.role not in item["allowed_roles"]: return _blocked("sdd-op-show", "role-not-permitted", operation_id=item["id"])
        return {"operation": "sdd-op-show", "schema_version": "1.0", "status": "ok", "operation_id": item["id"], **_card(item), "lifecycle_mutated": False, "external_state_mutated": False}
    item = operation(args.operation_id)
    if item is None: return _blocked(f"sdd-{args.command}", "unknown-operation")
    if not args.role: return _blocked(f"sdd-{args.command}", "role-required", operation_id=item["id"])
    if args.role not in item["allowed_roles"]: return _blocked(f"sdd-{args.command}", "role-not-permitted", operation_id=item["id"])
    if item["mutation_level"] == "mutate_external": return _blocked(f"sdd-{args.command}", "p3-external-operation-forbidden", operation_id=item["id"])
    if args.command == "request":
        if not item["mutation_level"].startswith("mutate_") or not item["confirmation_required"]:
            return _blocked("sdd-request", "operation-not-requestable", operation_id=item["id"])
        return {
            "operation": "sdd-request", "schema_version": "1.0", "status": "confirmation-requested",
            "operation_id": item["id"], "input_digest": operation_input_digest(item["id"], args.forwarded),
            "authority_granted": False, "review_required": True,
            "trusted_event_metadata_required": True,
            "lifecycle_mutated": False, "external_state_mutated": False,
        }
    if args.command == "run": return _blocked("sdd-run", "confirmation-contract-pending", operation_id=item["id"])
    required = "read_only" if args.command == "check" else "prepare"
    if item["mutation_level"] != required: return _blocked(f"sdd-{args.command}", "operation-class-not-permitted", operation_id=item["id"])
    return {"operation": f"sdd-{args.command}", "schema_version": "1.0", "operation_id": item["id"], "lifecycle_mutated": False, "external_state_mutated": False, **_run_entrypoint(item, args.forwarded)}

def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    try:
        args, forwarded = build_parser().parse_known_args(raw_argv)
        if hasattr(args, "operation_id"):
            args.forwarded = forwarded
    except SystemExit:
        if "--json" in raw_argv:
            print(json.dumps({"schema_version": "1.0", "status": "error", "diagnostics": [{"code": "invalid-command", "message": "The command could not be parsed safely."}]}, sort_keys=True))
            return 1
        raise
    args.json = args.json or (hasattr(args, "forwarded") and "--json" in args.forwarded)
    try:
        payload = dispatch(args)
    except OperationError as error:
        return execute(lambda: (_ for _ in ()).throw(error), args.json)
    except (OSError, UnicodeDecodeError) as error:
        return execute(
            lambda: (_ for _ in ()).throw(OperationError("operation-failed", "local operation failed", exit_code=3)),
            args.json,
        )
    print(json.dumps(payload, sort_keys=True) if args.json else f"{payload['operation']}: {payload['status']}")
    return 0 if payload["status"] in {"ok", "guided", "confirmation-requested"} else 3 if payload["status"] == "operational-error" else 1
