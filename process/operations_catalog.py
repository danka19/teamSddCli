"""Strict local operation catalog loader used by P3 discovery surfaces."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .errors import OperationError


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_CATALOG = PACKAGE_ROOT / "catalogs" / "operations.yaml"
_REQUIRED = {
    "id", "title", "entrypoint", "visibility", "allowed_roles", "situations",
    "inputs", "outputs", "mutation_level", "risk_level", "human_decision",
    "confirmation_required", "evidence", "fallback", "runbook", "tests",
    "lifecycle_status",
}
_VISIBILITY = {"public", "internal", "deprecated", "forbidden"}
_MUTATIONS = {"read_only", "prepare", "mutate_local", "mutate_release", "mutate_external"}
_RISKS = {"none", "low", "medium", "high"}
_AUTOMATION = {"ai_auto", "ai_prepare", "ai_request", "human_only"}


def load_operations_catalog(path: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    """Load a versioned catalog and reject incomplete or unsafe records."""
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("operations-catalog-invalid", "operation catalog is unavailable") from error
    if not isinstance(data, dict) or data.get("schema_version") != "1.0" or not isinstance(data.get("operations"), list):
        raise OperationError("operations-catalog-invalid", "operation catalog has an unsupported shape")
    ids: set[str] = set()
    entrypoints: set[str] = set()
    for item in data["operations"]:
        if not isinstance(item, dict) or set(item) != _REQUIRED | {"automation_class"}:
            raise OperationError("operations-catalog-invalid", "operation record has an unsupported shape")
        identifier, entrypoint = item.get("id"), item.get("entrypoint")
        if not isinstance(identifier, str) or not identifier or identifier in ids or not isinstance(entrypoint, str) or entrypoint in entrypoints:
            raise OperationError("operations-catalog-invalid", "operation id or entrypoint is duplicate")
        if item["visibility"] not in _VISIBILITY or item["mutation_level"] not in _MUTATIONS or item["risk_level"] not in _RISKS or item["automation_class"] not in _AUTOMATION:
            raise OperationError("operations-catalog-invalid", "operation record has an unsupported policy value")
        if not all(isinstance(item[key], list) and all(isinstance(value, str) and value for value in item[key]) for key in ("allowed_roles", "situations", "inputs", "outputs", "evidence", "tests")):
            raise OperationError("operations-catalog-invalid", "operation record has malformed list metadata")
        if not all(isinstance(item[key], str) and item[key] for key in ("title", "fallback", "runbook", "lifecycle_status")):
            raise OperationError("operations-catalog-invalid", "operation record has malformed text metadata")
        mutating = item["mutation_level"].startswith("mutate_")
        if mutating and (not isinstance(item["human_decision"], str) or not item["human_decision"] or not item["confirmation_required"] or item["automation_class"] == "ai_auto"):
            raise OperationError("operations-catalog-invalid", "mutating operation lacks a human authority boundary")
        if item["mutation_level"] == "mutate_external":
            raise OperationError("operations-catalog-invalid", "external mutation is outside the P3 catalog")
        ids.add(identifier)
        entrypoints.add(entrypoint)
    return data


def operation_by_id(identifier: str, path: Path = DEFAULT_CATALOG) -> dict[str, Any] | None:
    return next((item for item in load_operations_catalog(path)["operations"] if item["id"] == identifier), None)
