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
    release_entries = data.get("release_entrypoints")
    if not isinstance(release_entries, list):
        raise OperationError("operations-catalog-invalid", "release entry points are missing")
    release_paths: set[str] = set()
    for item in release_entries:
        if not isinstance(item, dict) or set(item) not in ({"entrypoint", "smoke", "expected_exit_codes"}, {"entrypoint", "smoke", "expected_exit_codes", "additional_smokes"}):
            raise OperationError("operations-catalog-invalid", "release entry point has an unsupported shape")
        entrypoint = item.get("entrypoint")
        if not isinstance(entrypoint, str) or entrypoint in release_paths or item.get("smoke") != [entrypoint, "--help"]:
            raise OperationError("operations-catalog-invalid", "release entry point is malformed")
        exits = item.get("expected_exit_codes")
        if not isinstance(exits, list) or not exits or any(type(code) is not int or code not in {0, 1, 2, 3} for code in exits):
            raise OperationError("operations-catalog-invalid", "release entry point exit contract is malformed")
        additional = item.get("additional_smokes", [])
        if not isinstance(additional, list) or any(not isinstance(command, list) or not command or not all(isinstance(part, str) and part for part in command) for command in additional):
            raise OperationError("operations-catalog-invalid", "release entry point additional smoke is malformed")
        release_paths.add(entrypoint)
    if release_paths != entrypoints:
        raise OperationError("operations-catalog-invalid", "release entry points do not cover the catalog")
    return data


def operation_by_id(identifier: str, path: Path = DEFAULT_CATALOG) -> dict[str, Any] | None:
    return next((item for item in load_operations_catalog(path)["operations"] if item["id"] == identifier), None)


def generate_operation_table(root: Path) -> str:
    """Render the committed, situation-first README view from the canonical catalog."""
    catalog = load_operations_catalog(root / "process" / "catalogs" / "operations.yaml")
    rows = ["| Operation | Role | Situation | Boundary | Runbook |", "| --- | --- | --- | --- | --- |"]
    for item in catalog["operations"]:
        if item["visibility"] not in {"public", "deprecated"}:
            continue
        runbook = item["runbook"]
        runbook_path = Path(runbook)
        target = (
            runbook_path.relative_to("docs").as_posix()
            if runbook_path.parts and runbook_path.parts[0] == "docs"
            else f"../{runbook_path.as_posix()}"
        )
        rows.append("| {id} | {roles} | {situations} | {mutation}/{risk} | [{runbook}]({target}) |".format(
            id=item["id"], roles=", ".join(item["allowed_roles"]),
            situations=", ".join(item["situations"]) or "on demand",
            mutation=item["mutation_level"], risk=item["risk_level"],
            runbook=runbook, target=target,
        ))
    return "\n".join(rows) + "\n"


def validate_operations_catalog(root: Path) -> list[str]:
    """Return deterministic catalog/derived-view errors without external effects."""
    try:
        catalog = load_operations_catalog(root / "process" / "catalogs" / "operations.yaml")
    except OperationError as error:
        return [error.code]
    errors: list[str] = []
    scripts = {
        path.relative_to(root).as_posix()
        for path in (root / "scripts").glob("*.py")
        if path.name != "__init__.py"
    }
    records = [item["entrypoint"] for item in catalog["operations"]]
    if len(records) != len(set(records)) or set(records) != scripts:
        errors.append("catalog-script-coverage-invalid")
    for item in catalog["operations"]:
        for reference in (item["entrypoint"], item["runbook"], *item["tests"]):
            if not (root / reference).is_file(): errors.append(f"catalog-reference-missing:{reference}")
    allowlist = yaml.safe_load((root / "process" / "release-allowlist.yaml").read_text(encoding="utf-8"))
    expected = [{"name": Path(item["entrypoint"]).name, **{key: value for key, value in item.items() if key != "entrypoint"}} for item in catalog["release_entrypoints"]]
    if not isinstance(allowlist, dict) or allowlist.get("entry_points") != expected: errors.append("catalog-release-allowlist-drift")
    routes = yaml.safe_load((root / "process" / "catalogs" / "guided-owner-workflow.yaml").read_text(encoding="utf-8"))
    ids = {item["id"] for item in catalog["operations"]}
    if any(command not in ids for route in routes.get("routes", []) for command in route.get("commands", [])): errors.append("catalog-guided-route-drift")
    read_pack = yaml.safe_load((root / "process" / "read-packs" / "p3-role-and-analytics.yaml").read_text(encoding="utf-8"))
    if "../../process/catalogs/operations.yaml" not in read_pack.get("canonical_sources", []): errors.append("catalog-read-pack-drift")
    readme = root / "docs" / "README.md"; begin, end = "<!-- operation-table:begin -->", "<!-- operation-table:end -->"
    content = readme.read_text(encoding="utf-8")
    if begin not in content or end not in content: errors.append("catalog-readme-markers-missing")
    elif content.split(begin, 1)[1].split(end, 1)[0].strip() + "\n" != generate_operation_table(root): errors.append("catalog-readme-drift")
    return errors
