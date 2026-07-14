from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


AUTHORITIES = {"canonical", "supporting", "generated-advisory", "evidence"}
ROLES = {"analyst", "developer", "qa", "tech_lead"}
CLASSES = {"minor", "major", "hotfix"}
ROLE_FILES = {
    "analyst": "roles/analyst.md",
    "developer": "roles/developer.md",
    "qa": "roles/qa.md",
    "tech_lead": "roles/tech-lead.md",
}
REQUIRED_COMBINED_CHECKS = {"integration", "traceability", "review", "conflict"}


class ContractError(ValueError):
    pass


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _safe_file(root: Path, relative: str) -> Path | None:
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or ".." in candidate.parts or not candidate.parts:
        return None
    resolved = (root / Path(*candidate.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def build_read_pack(repository_root: Path, process_root: Path, request: dict[str, Any]) -> dict[str, Any]:
    problems: list[dict[str, str]] = []
    role = request.get("role")
    change_class = request.get("change_class")
    if role not in ROLES:
        problems.append({"code": "read-pack.invalid-role", "detail": str(role)})
    if change_class not in CLASSES:
        problems.append({"code": "read-pack.invalid-class", "detail": str(change_class)})

    package = yaml.safe_load((process_root / "package.yaml").read_text(encoding="utf-8"))
    canonical_allowlist = set(package.get("canonical_sources", []))
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    sources: list[dict[str, Any]] = []
    for source in request.get("sources", []):
        authority = source.get("authority")
        stable_id = source.get("stable_id")
        relative = source.get("path")
        if authority not in AUTHORITIES:
            problems.append({"code": "read-pack.invalid-authority", "detail": str(authority)})
            continue
        if not isinstance(stable_id, str) or not stable_id or stable_id in seen_ids:
            problems.append({"code": "read-pack.duplicate-or-missing-id", "detail": str(stable_id)})
            continue
        if not isinstance(relative, str) or relative in seen_paths:
            problems.append({"code": "read-pack.duplicate-or-missing-path", "detail": str(relative)})
            continue
        seen_ids.add(stable_id)
        seen_paths.add(relative)
        path = _safe_file(repository_root, relative)
        if path is None:
            problems.append({"code": "read-pack.unsafe-path", "detail": relative})
            continue
        if authority == "canonical" and relative not in canonical_allowlist:
            problems.append({"code": "read-pack.unconfigured-canonical-source", "detail": relative})
            continue
        if not path.is_file():
            if source.get("required", True):
                problems.append({"code": "read-pack.missing-required-source", "detail": relative})
            continue
        raw = path.read_bytes()
        sources.append(
            {
                "authority": authority,
                "stable_id": stable_id,
                "path": relative,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "sections": list(source.get("sections", [])),
            }
        )

    unresolved = list(request.get("unresolved_inputs", []))
    for item in unresolved:
        problems.append({"code": "read-pack.unresolved-input", "detail": str(item)})
    body = {
        "schema_version": "1.0",
        "task_id": request.get("task_id"),
        "role": role,
        "change_class": change_class,
        "stage": request.get("stage"),
        "status": "blocked" if problems else "ready",
        "sources": sources,
        "known_traps": list(request.get("known_traps", [])),
        "unresolved_inputs": unresolved,
        "missing_or_invalid_context": problems,
        "authority_order": ["canonical", "supporting", "evidence", "generated-advisory"],
    }
    body["identity"] = _digest(body)
    return body


def build_role_launch(process_root: Path, read_pack: dict[str, Any], evidence_path: str) -> dict[str, Any]:
    if read_pack.get("status") != "ready":
        raise ContractError("read pack is blocked; resolve every missing or invalid context item")
    role = read_pack.get("role")
    instruction = ROLE_FILES.get(role)
    if instruction is None or not (process_root / instruction).is_file():
        raise ContractError(f"unsupported or missing role instruction: {role}")
    evidence = _safe_file(Path("."), evidence_path)
    if evidence is None:
        raise ContractError("evidence path must be repository-relative and bounded")
    launch = {
        "schema_version": "1.0",
        "task_id": read_pack.get("task_id"),
        "role": role,
        "change_class": read_pack.get("change_class"),
        "stage_boundary": read_pack.get("stage"),
        "instruction_path": instruction,
        "read_pack_identity": read_pack.get("identity"),
        "output_contract": "schemas/weak-model-operation-evidence.schema.json",
        "evidence_path": evidence_path,
        "model_authority": "advisory-only",
        "canonical_mutation_allowed": False,
        "human_stop_required": True,
        "next_action": "run deterministic checks and obtain the named human review",
    }
    launch["identity"] = _digest(launch)
    return launch


def validate_operation_evidence(evidence: dict[str, Any]) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    if evidence.get("approval_claimed") is not False:
        diagnostics.append({"code": "evidence.forbidden-authority", "detail": "AI approval claims are not evidence"})
    if evidence.get("lifecycle_transition_requested") is not False:
        diagnostics.append({"code": "evidence.forbidden-transition", "detail": "AI cannot request or perform lifecycle transitions"})
    if evidence.get("status") not in {"draft-complete", "blocked", "failed"}:
        diagnostics.append({"code": "evidence.unsupported-completion", "detail": str(evidence.get("status"))})

    check_evidence = {
        check.get("evidence")
        for check in evidence.get("checks", [])
        if check.get("command") and check.get("result") in {"passed", "failed", "not-run"} and check.get("evidence")
    }
    for claim in evidence.get("claims", []):
        if claim.get("kind") in {"validation", "test", "integration", "file-state"} and claim.get("evidence") not in check_evidence:
            diagnostics.append({"code": "evidence.unsupported-claim", "detail": str(claim.get("value"))})

    source_ids = {source.get("stable_id") for source in evidence.get("sources_read", [])}
    for artifact in evidence.get("artifacts_drafted", []):
        references = artifact.get("canonical_references", [])
        if artifact.get("canonical") is True:
            diagnostics.append({"code": "evidence.canonical-draft-forbidden", "detail": str(artifact.get("path"))})
        if not references or not set(references) <= source_ids:
            diagnostics.append({"code": "evidence.missing-canonical-reference", "detail": str(artifact.get("path"))})
    return diagnostics


def _normalized_scope(value: str) -> tuple[str, ...]:
    path = PurePosixPath(value.replace("\\", "/"))
    if path.is_absolute() or ".." in path.parts or not path.parts:
        return ()
    return tuple(part.casefold() for part in path.parts)


def _overlap(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return bool(left and right and (left == right[: len(left)] or right == left[: len(right)]))


def validate_parallel_plan(plan: dict[str, Any]) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    tasks = plan.get("tasks", [])
    task_ids = {task.get("task_id") for task in tasks}
    evidence_paths: set[str] = set()
    scopes: list[tuple[str, tuple[str, ...]]] = []
    for task in tasks:
        task_id = str(task.get("task_id"))
        dependencies = task.get("dependencies", [])
        if dependencies:
            diagnostics.append({"code": "parallel.unresolved-dependency", "detail": f"{task_id}: {dependencies}"})
        if any(dep not in task_ids for dep in dependencies):
            diagnostics.append({"code": "parallel.unknown-dependency", "detail": task_id})
        if task.get("policy_or_lifecycle_decision") is not False:
            diagnostics.append({"code": "parallel.authority-decision", "detail": task_id})
        evidence_path = task.get("evidence_path")
        if not evidence_path or evidence_path in evidence_paths:
            diagnostics.append({"code": "parallel.shared-evidence", "detail": str(evidence_path)})
        evidence_paths.add(evidence_path)
        if not task.get("owner") or not task.get("stop_condition") or not task.get("focused_checks"):
            diagnostics.append({"code": "parallel.incomplete-task-boundary", "detail": task_id})
        for raw_scope in task.get("write_scopes", []):
            scope = _normalized_scope(raw_scope)
            if not scope:
                diagnostics.append({"code": "parallel.unsafe-scope", "detail": str(raw_scope)})
                continue
            for other_id, other_scope in scopes:
                if _overlap(scope, other_scope):
                    diagnostics.append({"code": "parallel.overlapping-scope", "detail": f"{other_id} <-> {task_id}"})
            scopes.append((task_id, scope))
    missing_checks = REQUIRED_COMBINED_CHECKS - set(plan.get("combined_checks", []))
    if missing_checks:
        diagnostics.append({"code": "parallel.missing-combined-gate", "detail": ",".join(sorted(missing_checks))})
    if not plan.get("integration_owner"):
        diagnostics.append({"code": "parallel.missing-integration-owner", "detail": "integration owner is required"})
    serialize_codes = {"parallel.unresolved-dependency", "parallel.overlapping-scope", "parallel.authority-decision"}
    status = "parallel-safe"
    if diagnostics:
        status = "serialize" if any(item["code"] in serialize_codes for item in diagnostics) else "blocked"
    return {"schema_version": "1.0", "plan_id": plan.get("plan_id"), "status": status, "diagnostics": diagnostics}
