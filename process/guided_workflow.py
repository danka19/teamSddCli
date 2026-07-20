"""Read-only, catalog-backed guidance for a process-package owner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import OperationError


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_CATALOG = PACKAGE_ROOT / "catalogs" / "guided-owner-workflow.yaml"
ALLOWED_COMMANDS = {
    "scripts/create_change.py",
    "scripts/classify_change.py",
    "scripts/prepare_spec_pr.py",
    "scripts/evaluate_change_gates.py",
    "scripts/prepare_archive.py",
    "scripts/manual_fallback.py",
}
ALLOWED_OWNERS = {"Tech Lead", "Change Owner"}


def load_catalog(path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    """Load a small, explicit catalog and reject authority or command drift."""
    try:
        catalog = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("catalog-invalid", "guided workflow catalog is unavailable") from error
    if not isinstance(catalog, dict) or catalog.get("schema_version") != "1.0":
        raise OperationError("catalog-invalid", "guided workflow catalog has an unsupported shape")
    routes = catalog.get("routes")
    if not isinstance(routes, list) or not routes:
        raise OperationError("catalog-invalid", "guided workflow catalog has no routes")
    ids: set[str] = set()
    for route in routes:
        if not isinstance(route, dict):
            raise OperationError("catalog-invalid", "guided workflow route is malformed")
        identifier = route.get("id")
        required = route.get("required_facts")
        allowed_values = route.get("allowed_values", {})
        commands = route.get("commands")
        decision = route.get("human_decision")
        fallbacks = route.get("fallbacks")
        if (
            not isinstance(identifier, str) or not identifier or identifier in ids
            or route.get("situation") != identifier
            or not isinstance(required, list) or not all(isinstance(item, str) and item for item in required)
            or not isinstance(allowed_values, dict)
            or any(
                key not in required or not isinstance(values, list) or not values
                or not all(isinstance(value, str) and value for value in values)
                for key, values in allowed_values.items()
            )
            or not isinstance(commands, list) or not commands or not set(commands) <= ALLOWED_COMMANDS
            or not isinstance(decision, dict) or not isinstance(decision.get("id"), str)
            or decision.get("owner") not in ALLOWED_OWNERS
            or not isinstance(decision.get("consequence"), str)
            or not isinstance(fallbacks, list)
        ):
            raise OperationError("catalog-invalid", "guided workflow catalog violates the safe route contract")
        for fallback in fallbacks:
            if not isinstance(fallback, dict) or not isinstance(fallback.get("surface"), str) or not isinstance(fallback.get("command"), str):
                raise OperationError("catalog-invalid", "guided workflow fallback is malformed")
        ids.add(identifier)
    return catalog


def guide(situation: str, facts: dict[str, str], unavailable: set[str], *, catalog_path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    """Return guidance only; callers must invoke each command and gate explicitly."""
    catalog = load_catalog(catalog_path)
    route = next((item for item in catalog["routes"] if item["id"] == situation), None)
    if route is None:
        return _blocked("situation-unknown", [])
    missing = [key for key in route["required_facts"] if not facts.get(key)]
    if missing:
        return _blocked("missing-context", missing)
    invalid = sorted(
        key for key, values in route.get("allowed_values", {}).items()
        if facts[key] not in values
    )
    if invalid:
        return _blocked("invalid-context", invalid)
    fallbacks = [
        {"surface": item["surface"], "command": item["command"]}
        for item in route["fallbacks"] if item["surface"] in unavailable
    ]
    return {
        "operation": "guided-owner-workflow",
        "status": "guided",
        "schema_version": "1.0",
        "route_id": route["id"],
        "known_facts": {key: facts[key] for key in route["required_facts"]},
        "commands": route["commands"],
        "expected_evidence": route["evidence"],
        "human_decision": route["human_decision"],
        "unavailable": sorted(unavailable),
        "fallbacks": fallbacks,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }


def _blocked(code: str, required_facts: list[str]) -> dict[str, Any]:
    return {
        "operation": "guided-owner-workflow",
        "status": "blocked",
        "schema_version": "1.0",
        "blockers": [{"code": code, "required_facts": required_facts}],
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }
