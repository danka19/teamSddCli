"""Fail-closed local dispatcher for catalog-defined P3 operations."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence
import yaml
from .guided_workflow import guide, operation_input_digest, validate_operation_confirmation_event
from .errors import OperationError
from .operation_cli import execute
from .operations_catalog import DEFAULT_CATALOG, load_operations_catalog, operation_by_id
from .workflow_operations import bootstrap_team_specs

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

def _package_identity() -> dict[str, str]:
    return dict(yaml.safe_load((REPOSITORY_ROOT / "process" / "package.yaml").read_text(encoding="utf-8"))["package"])

def build_parser() -> argparse.ArgumentParser:
    package = _package_identity()
    parser = argparse.ArgumentParser(prog="sdd", description=f"{package['id']} {package['version']}")
    sub = parser.add_subparsers(dest="command", required=True)
    def json_flag(p: argparse.ArgumentParser) -> None: p.add_argument("--json", action="store_true")
    guide_parser = sub.add_parser("guide"); guide_parser.add_argument("situation"); guide_parser.add_argument("--role"); guide_parser.add_argument("--fact", action="append", default=[]); guide_parser.add_argument("--unavailable", action="append", default=[]); json_flag(guide_parser)
    start_parser = sub.add_parser("start"); start_parser.add_argument("situation", nargs="?"); start_parser.add_argument("--role"); start_parser.add_argument("--fact", action="append", default=[]); start_parser.add_argument("--unavailable", action="append", default=[]); json_flag(start_parser)
    setup_parser = sub.add_parser("setup"); setup_parser.add_argument("destination", type=Path); setup_parser.add_argument("--package-root", type=Path, default=REPOSITORY_ROOT / "process"); setup_parser.add_argument("--team-template", type=Path, default=REPOSITORY_ROOT / "templates" / "team-specs"); setup_parser.add_argument("--confirm", action="store_true"); json_flag(setup_parser)
    next_parser = sub.add_parser("next"); next_parser.add_argument("--change", required=True); next_parser.add_argument("--role"); json_flag(next_parser)
    op_parser = sub.add_parser("op"); op_sub = op_parser.add_subparsers(dest="op_command", required=True)
    op_list = op_sub.add_parser("list"); op_list.add_argument("--include-internal", action="store_true"); op_list.add_argument("--role"); json_flag(op_list)
    op_show = op_sub.add_parser("show"); op_show.add_argument("operation_id"); op_show.add_argument("--role"); json_flag(op_show)
    for command in ("check", "prepare", "request", "run"):
        child = sub.add_parser(command); child.add_argument("operation_id"); child.add_argument("--role")
        if command == "run": child.add_argument("--confirmation-event")
        json_flag(child)
    return parser

def _blocked(operation: str, code: str, **details: Any) -> dict[str, Any]:
    return {"operation": operation, "schema_version": "1.0", "status": "blocked", "blockers": [{"code": code, **details}], "lifecycle_mutated": False, "external_state_mutated": False}

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def _valid_supplied_confirmation(path: str, forwarded: Sequence[str]) -> bool:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return validate_operation_confirmation_event(value, forwarded_argv=forwarded, now=_utc_now())

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
    if args[:1] == ["--"]:
        args = args[1:]
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

def _continuation(result: dict[str, Any], catalog_path: Path) -> dict[str, Any]:
    """Render the only public next step from an existing guided route."""
    role = result.get("known_facts", {}).get("human_role")
    decision = result.get("human_decision", {})
    missing = []
    for blocker in result.get("blockers", []):
        if blocker.get("code") == "missing-context":
            missing.extend(blocker.get("required_facts", []))
    next_command = None
    if result.get("status") == "guided" and role:
        for operation_id in result.get("commands", []):
            item = operation_by_id(operation_id, catalog_path)
            if item is None or role not in item["allowed_roles"]:
                continue
            verb = "request" if item["mutation_level"].startswith("mutate_") else "prepare" if item["mutation_level"] == "prepare" else "check"
            next_command = f"sdd {verb} {operation_id} --role {role} --json"
            break
    return {
        **result,
        "missing_facts": missing,
        "role_owner": decision.get("owner"),
        "authority_boundary": decision.get("consequence"),
        "fallback": (result.get("fallbacks") or [None])[0],
        "next_command": next_command,
    }

def _render_human(payload: dict[str, Any]) -> str:
    if "next_command" not in payload:
        return f"{payload['operation']}: {payload['status']}"
    lines = [f"{payload['operation']}: {payload['status']}"]
    if payload.get("missing_facts"):
        lines.append("Missing facts: " + ", ".join(payload["missing_facts"]))
    if payload.get("role_owner"):
        lines.append("Human owner: " + payload["role_owner"])
    if payload.get("authority_boundary"):
        lines.append("Boundary: " + payload["authority_boundary"])
    if payload.get("next_command"):
        lines.append("Next: " + payload["next_command"])
    return "\n".join(lines)

def dispatch(args: argparse.Namespace, *, catalog_path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    catalog = load_operations_catalog(catalog_path)
    operation = lambda identifier: operation_by_id(identifier, catalog_path)
    if args.command == "setup":
        if not args.confirm:
            return _blocked("sdd-setup", "confirmation-required")
        if args.destination.exists() and any(args.destination.iterdir()):
            return _blocked("sdd-setup", "destination-not-empty")
        try:
            bootstrap_team_specs(args.package_root, args.team_template, args.destination)
        except OperationError as error:
            return _blocked("sdd-setup", error.code)
        return {
            "operation": "sdd-setup", "schema_version": "1.0", "status": "created",
            "workspace": str(args.destination), "configuration": str(args.destination / "team-specs" / "sdd.config.yaml"),
            "next_command": "sdd start new-requirement --role Analyst --json",
            "lifecycle_mutated": False, "external_state_mutated": False,
        }
    if args.command in {"guide", "start"}:
        try:
            if args.command == "start" and not args.situation:
                args.situation = input("Situation (new-requirement, existing-change, urgent-incident, blocked-operation): ").strip()
            facts = _facts(args.fact)
            if args.role:
                if facts.get("human_role") and facts["human_role"] != args.role:
                    raise ValueError
                facts["human_role"] = args.role
            result = guide(args.situation, facts, set(args.unavailable))
        except ValueError:
            return _blocked(f"sdd-{args.command}", "invalid-context")
        result["operation"] = f"sdd-{args.command}"
        if result["status"] == "blocked": return _continuation(result, catalog_path) if args.command == "start" else result
        resolved = [operation(item) for item in result["commands"]]
        if any(item is None for item in resolved): return _blocked("sdd-guide", "catalog-route-unknown-operation")
        permitted = [item for item in resolved if item and result["known_facts"]["human_role"] in item["allowed_roles"]]
        if not permitted: return _blocked("sdd-guide", "role-not-permitted")
        result["commands"] = [item["id"] for item in permitted]
        return _continuation(result, catalog_path) if args.command == "start" else result
    if args.command == "next":
        path = Path(args.change); path = path / "change.yaml" if path.is_dir() else path
        if not path.is_file(): return _blocked("sdd-next", "missing-change")
        try: state = yaml.safe_load(path.read_text(encoding="utf-8")).get("lifecycle_state")
        except (OSError, UnicodeError, yaml.YAMLError, AttributeError): state = None
        if not isinstance(state, str) or not state: return _blocked("sdd-next", "missing-lifecycle-state")
        result = guide("existing-change", {"human_role": args.role or "", "change_id": path.parent.name, "lifecycle_state": state}, set()); result["operation"] = "sdd-next"; return _continuation(result, catalog_path)
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
    if args.command == "run":
        if args.confirmation_event and not _valid_supplied_confirmation(args.confirmation_event, args.forwarded):
            return _blocked("sdd-run", "operation-confirmation-invalid", operation_id=item["id"])
        return _blocked("sdd-run", "confirmation-contract-pending", operation_id=item["id"])
    required = "read_only" if args.command == "check" else "prepare"
    if item["mutation_level"] != required: return _blocked(f"sdd-{args.command}", "operation-class-not-permitted", operation_id=item["id"])
    return {"operation": f"sdd-{args.command}", "schema_version": "1.0", "operation_id": item["id"], "lifecycle_mutated": False, "external_state_mutated": False, **_run_entrypoint(item, args.forwarded)}

def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if raw_argv and raw_argv[0] == "--version":
        package = _package_identity()
        payload = {
            "operation": "sdd-version",
            "package": dict(package),
            "schema_version": "1.0",
            "status": "ok",
        }
        print(json.dumps(payload, sort_keys=True) if "--json" in raw_argv else f"sdd {package['id']} {package['version']}")
        return 0
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
    print(json.dumps(payload, sort_keys=True) if args.json else _render_human(payload))
    return 0 if payload["status"] in {"ok", "guided", "confirmation-requested", "created"} else 3 if payload["status"] == "operational-error" else 1
