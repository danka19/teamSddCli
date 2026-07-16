from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator


AUTHORITIES = {"canonical", "supporting", "generated-advisory", "evidence"}
ROLES = {"analyst", "developer", "qa", "tech_lead"}
ROLE_PAYLOAD_KEYS = {
    "analyst": "requirements_note",
    "developer": "implementation_prep_note",
    "qa": "qa_review_note",
    "tech_lead": "advisory_review_note",
}
GLOBAL_ALLOWED_REASON_CODES = (
    "authority-required",
    "bounded-draft",
    "conflicting-context",
    "failed-run-missing",
    "human-stop-required",
    "lifecycle-authority-required",
    "missing-context",
    "qa-evidence-insufficient",
    "reconciliation-missing",
    "unsafe-resume",
    "unsupported-evidence",
)
GLOBAL_ALLOWED_ARTIFACT_KINDS = (
    "evidence-boundary-note",
    "implementation-prep-note",
    "qa-review-note",
    "requirements-note",
    "tech-lead-review-note",
)
CLASSES = {"minor", "major", "hotfix"}
ROLE_FILES = {
    "analyst": "roles/analyst.md",
    "developer": "roles/developer.md",
    "qa": "roles/qa.md",
    "tech_lead": "roles/tech-lead.md",
}
REQUIRED_COMBINED_CHECKS = {"integration", "traceability", "review", "conflict"}
MAX_SOURCES = 16
MAX_SOURCE_BYTES = 65_536
MAX_PACK_BYTES = 262_144

_AUTHORITY_LANGUAGE = re.compile(
    r"\b(?:decision|approv(?:e|ed|es|al)|authoriz(?:e|ed|es|ation)|waiv(?:e|ed|er)|"
    r"transition(?:ed|s)?|merg(?:e|ed|es)|releas(?:e|ed|es)|archiv(?:e|ed|es)|"
    r"resum(?:e|ed|es)|gate[- ]?green)\b",
    re.IGNORECASE,
)
_LEGACY_AUTHORITY_TERMS = re.compile(
    r"\b(decision|approv(?:e|ed|al)|authoriz(?:e|ed|ation)|waiv(?:e|ed|er)|"
    r"transition|merge|release|archive|resume|gate[- ]?green)\b",
    re.IGNORECASE,
)
_SAFE_AUTHORITY_CONTEXTS = (
    re.compile(
        r"\b(?:human(?:\s+(?:owner|approver))?|tech\s+lead|qa\s+owner|"
        r"configured\s+(?:decision\s+)?(?:owner|approver)|decision\s+owner|accountable\s+owner)\s+"
        r"(?:approval|authorization|decision)\s+(?:is|are|remains?)\s+"
        r"(?:required|pending|absent|missing)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:decision|approval|authorization|transition|release|archive|merge|resume)\s+"
        r"(?:is|are|was|were|remains?)\s+not\s+"
        r"(?:approved|authorized|requested|performed|completed?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:is|are|was|were|do|does|did|can|could|may|must|should|will|would|has|have|had)\s+"
        r"not\s+(?:approv\w*|authoriz\w*|transition\w*|merg\w*|releas\w*|archiv\w*|resum\w*)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:no|without)\s+(?:\w+\s+){0,2}"
        r"(?:decision|approval|authorization|transition|merge|release|archive|resume)\b",
        re.IGNORECASE,
    ),
)


class ContractError(ValueError):
    pass


def contains_forbidden_authority_claim(value: Any) -> bool:
    """Detect positive authority semantics while preserving explicit stops and negation."""
    if isinstance(value, dict):
        return any(contains_forbidden_authority_claim(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return any(contains_forbidden_authority_claim(item) for item in value)
    if not isinstance(value, str):
        return False
    candidate = value
    for safe_context in _SAFE_AUTHORITY_CONTEXTS:
        candidate = safe_context.sub(" ", candidate)
    return _AUTHORITY_LANGUAGE.search(candidate) is not None


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _schema_errors(process_root: Path, name: str, document: Any) -> list[str]:
    try:
        schema = json.loads((process_root / "schemas" / name).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return ["schema-unavailable"]
    return sorted(error.json_path for error in Draft202012Validator(schema).iter_errors(document))


def _without_identity(document: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in document.items() if key != "identity"}


def _extract_sections(text: str, requested: list[str]) -> str | None:
    if not requested:
        return text
    lines = text.splitlines()
    chunks: list[str] = []
    for wanted in requested:
        start = None
        level = None
        for index, line in enumerate(lines):
            stripped = line.lstrip()
            if stripped.startswith("#"):
                hashes = len(stripped) - len(stripped.lstrip("#"))
                title = stripped[hashes:].strip()
                if title.casefold() == wanted.casefold():
                    start, level = index, hashes
                    break
        if start is None or level is None:
            return None
        end = len(lines)
        for index in range(start + 1, len(lines)):
            stripped = lines[index].lstrip()
            if stripped.startswith("#"):
                hashes = len(stripped) - len(stripped.lstrip("#"))
                if hashes <= level:
                    end = index
                    break
        chunks.append("\n".join(lines[start:end]).strip())
    return "\n\n".join(chunks) + "\n"


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
    request_errors = _schema_errors(process_root, "read-pack-request.schema.json", request)
    for location in request_errors:
        problems.append({"code": "read-pack.request-schema", "detail": location})
    if request_errors:
        blocked = {
            "schema_version": "1.0",
            "task_id": request.get("task_id"),
            "role": request.get("role"),
            "change_class": request.get("change_class"),
            "stage": request.get("stage"),
            "status": "blocked",
            "sources": [],
            "known_traps": [],
            "unresolved_inputs": [],
            "missing_or_invalid_context": problems,
            "authority_order": ["canonical", "supporting", "evidence", "generated-advisory"],
            "resolver": "repository-relative-verified-content",
        }
        blocked["identity"] = _digest(blocked)
        return blocked
    role = request.get("role")
    change_class = request.get("change_class")
    if role not in ROLES:
        problems.append({"code": "read-pack.invalid-role", "detail": str(role)})
    if change_class not in CLASSES:
        problems.append({"code": "read-pack.invalid-class", "detail": str(change_class)})

    package = yaml.safe_load((process_root / "package.yaml").read_text(encoding="utf-8"))
    canonical_allowlist = set(package.get("canonical_sources", []))
    if not request.get("sources"):
        problems.append({"code": "read-pack.empty-context", "detail": "at least one source is required"})
    if not any(source.get("authority") == "canonical" for source in request.get("sources", []) if isinstance(source, dict)):
        problems.append({"code": "read-pack.missing-canonical-context", "detail": "at least one canonical source is required"})
    if len(request.get("sources", [])) > MAX_SOURCES:
        problems.append({"code": "read-pack.source-limit", "detail": str(MAX_SOURCES)})
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    sources: list[dict[str, Any]] = []
    total_bytes = 0
    for source in request.get("sources", [])[:MAX_SOURCES]:
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
        if len(raw) > MAX_SOURCE_BYTES:
            problems.append({"code": "read-pack.source-too-large", "detail": relative})
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            problems.append({"code": "read-pack.source-not-utf8", "detail": relative})
            continue
        content = _extract_sections(text, list(source.get("sections", [])))
        if content is None or not content.strip():
            problems.append({"code": "read-pack.missing-section", "detail": relative})
            continue
        content_bytes = content.encode("utf-8")
        total_bytes += len(content_bytes)
        if total_bytes > MAX_PACK_BYTES:
            problems.append({"code": "read-pack.pack-too-large", "detail": str(MAX_PACK_BYTES)})
            continue
        sources.append(
            {
                "authority": authority,
                "stable_id": stable_id,
                "path": relative,
                "sha256": hashlib.sha256(content_bytes).hexdigest(),
                "sections": list(source.get("sections", [])),
                "content": content,
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
        "resolver": "repository-relative-verified-content",
    }
    body["identity"] = _digest(body)
    return body


def build_role_launch(
    repository_root: Path,
    process_root: Path,
    read_pack: dict[str, Any],
    read_pack_path: str,
    evidence_path: str,
    model_response_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if _schema_errors(process_root, "read-pack.schema.json", read_pack):
        raise ContractError("read pack schema is invalid")
    if read_pack.get("identity") != _digest(_without_identity(read_pack)):
        raise ContractError("read pack identity does not match its content")
    if read_pack.get("status") != "ready":
        raise ContractError("read pack is blocked; resolve every missing or invalid context item")
    if not any(source.get("authority") == "canonical" for source in read_pack.get("sources", [])):
        raise ContractError("read pack must contain at least one canonical source")
    role = read_pack.get("role")
    instruction = ROLE_FILES.get(role)
    if instruction is None or not (process_root / instruction).is_file():
        raise ContractError(f"unsupported or missing role instruction: {role}")
    for label, relative in (("read pack", read_pack_path), ("evidence", evidence_path)):
        if _safe_file(repository_root, relative) is None:
            raise ContractError(f"{label} path must be repository-relative and bounded")
    package = yaml.safe_load((process_root / "package.yaml").read_text(encoding="utf-8"))
    canonical_allowlist = set(package.get("canonical_sources", []))
    manifest: list[dict[str, str]] = []
    for source in read_pack.get("sources", []):
        path = _safe_file(repository_root, source["path"])
        if path is None or not path.is_file():
            raise ContractError("read pack source path is missing or unsafe")
        if source["authority"] == "canonical" and source["path"] not in canonical_allowlist:
            raise ContractError("read pack canonical source is not allowlisted")
        content_hash = hashlib.sha256(source["content"].encode("utf-8")).hexdigest()
        if content_hash != source["sha256"]:
            raise ContractError("read pack source content hash does not match")
        try:
            actual_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ContractError("read pack canonical source bytes are unavailable") from error
        actual_content = _extract_sections(actual_text, list(source.get("sections", [])))
        if actual_content != source["content"]:
            raise ContractError("read pack canonical source bytes do not match embedded content")
        manifest.append({key: source[key] for key in ("authority", "stable_id", "path", "sha256")})
    launch = {
        "schema_version": "1.0",
        "task_id": read_pack.get("task_id"),
        "role": role,
        "change_class": read_pack.get("change_class"),
        "stage_boundary": read_pack.get("stage"),
        "instruction_path": instruction,
        "read_pack_path": read_pack_path,
        "read_pack_identity": read_pack.get("identity"),
        "verified_source_manifest": manifest,
        "output_contract": "schemas/weak-model-operation-evidence.schema.json",
        "evidence_path": evidence_path,
        "model_authority": "advisory-only",
        "canonical_mutation_allowed": False,
        "human_stop_required": True,
        "next_action": "run deterministic checks and obtain the named human review",
    }
    if model_response_contract is not None:
        legacy_fields = {
            "case_id",
            "operation",
            "role_payload_key",
            "required_artifact_kind",
            "allowed_reason_codes",
        }
        adapter_2_1_fields = {
            *legacy_fields,
            "contract_version",
            "allowed_artifact_kinds",
        }
        contract_fields = frozenset(model_response_contract)
        if contract_fields not in {frozenset(legacy_fields), frozenset(adapter_2_1_fields)}:
            raise ContractError("model response contract fields are invalid")
        if contract_fields == adapter_2_1_fields and model_response_contract.get("contract_version") != "2.1":
            raise ContractError("model response contract version is invalid")
        if model_response_contract.get("role_payload_key") != ROLE_PAYLOAD_KEYS.get(role):
            raise ContractError("model response contract does not match launch role")
        if model_response_contract.get("allowed_reason_codes") != list(GLOBAL_ALLOWED_REASON_CODES):
            raise ContractError("model response contract reason-code vocabulary is invalid")
        if (
            contract_fields == adapter_2_1_fields
            and model_response_contract.get("allowed_artifact_kinds")
            != list(GLOBAL_ALLOWED_ARTIFACT_KINDS)
        ):
            raise ContractError("model response contract artifact-kind vocabulary is invalid")
        launch["model_response_contract"] = copy.deepcopy(model_response_contract)
    launch["identity"] = _digest(launch)
    if _schema_errors(process_root, "task-launch.schema.json", launch):
        raise ContractError("generated task launch is invalid")
    return launch


def validate_operation_evidence(
    evidence: dict[str, Any], launch: dict[str, Any], read_pack: dict[str, Any], process_root: Path | None = None
) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    process_root = process_root or Path(__file__).resolve().parent
    evidence_schema_errors = _schema_errors(process_root, "weak-model-operation-evidence.schema.json", evidence)
    if evidence_schema_errors:
        return [{"code": "evidence.schema", "detail": location} for location in evidence_schema_errors]
    launch_schema_errors = _schema_errors(process_root, "task-launch.schema.json", launch)
    read_pack_schema_errors = _schema_errors(process_root, "read-pack.schema.json", read_pack)
    if launch_schema_errors or read_pack_schema_errors:
        return [
            *({"code": "evidence.invalid-launch", "detail": location} for location in launch_schema_errors),
            *({"code": "evidence.invalid-read-pack", "detail": location} for location in read_pack_schema_errors),
        ]
    if launch.get("identity") != _digest(_without_identity(launch)):
        diagnostics.append({"code": "evidence.invalid-launch", "detail": "launch identity is invalid"})
    if read_pack.get("identity") != _digest(_without_identity(read_pack)):
        diagnostics.append({"code": "evidence.invalid-read-pack", "detail": "read-pack identity is invalid"})
    expected_manifest = [
        {key: source[key] for key in ("authority", "stable_id", "path", "sha256")}
        for source in read_pack.get("sources", [])
    ]
    if launch.get("read_pack_identity") != read_pack.get("identity") or launch.get("verified_source_manifest") != expected_manifest:
        diagnostics.append({"code": "evidence.invalid-launch-binding", "detail": "launch does not bind the supplied read pack"})
    for field, launch_field in (("task_id", "task_id"), ("role", "role"), ("stage", "stage_boundary"), ("read_pack_identity", "read_pack_identity")):
        if evidence.get(field) != launch.get(launch_field):
            diagnostics.append({"code": "evidence.launch-mismatch", "detail": field})
    if evidence.get("approval_claimed") is not False:
        diagnostics.append({"code": "evidence.forbidden-authority", "detail": "AI approval claims are not evidence"})
    if evidence.get("lifecycle_transition_requested") is not False:
        diagnostics.append({"code": "evidence.forbidden-transition", "detail": "AI cannot request or perform lifecycle transitions"})
    if evidence.get("status") not in {"draft-complete", "blocked", "failed"}:
        diagnostics.append({"code": "evidence.unsupported-completion", "detail": str(evidence.get("status"))})
    if evidence.get("prohibited_actions_attempted"):
        diagnostics.append({"code": "evidence.prohibited-action", "detail": "a prohibited action was attempted"})
    if evidence.get("human_stop_reached") is not True or evidence.get("human_review_status") != "pending":
        diagnostics.append({"code": "evidence.human-stop-missing", "detail": "human stop must remain pending"})
    if launch.get("model_response_contract") is not None:
        forbidden_authority = any(
            contains_forbidden_authority_claim(claim.get("value", {}))
            for claim in evidence.get("claims", [])
        )
    else:
        forbidden_authority = any(
            _LEGACY_AUTHORITY_TERMS.search(json.dumps(claim.get("value", {}), sort_keys=True))
            for claim in evidence.get("claims", [])
        )
    if forbidden_authority:
        diagnostics.append({"code": "evidence.forbidden-authority", "detail": "claim value contains human-authority semantics"})

    verified_sources = {
        (source["stable_id"], source["path"], source["sha256"], source["authority"])
        for source in read_pack.get("sources", [])
    }
    for source in evidence.get("sources_read", []):
        key = tuple(source.get(name) for name in ("stable_id", "path", "sha256", "authority"))
        if key not in verified_sources:
            diagnostics.append({"code": "evidence.unverified-source", "detail": str(source.get("stable_id"))})

    check_evidence = {
        check.get("evidence")
        for check in evidence.get("checks", [])
        if check.get("command") and check.get("result") in {"passed", "failed", "not-run"} and check.get("evidence")
    }
    for claim in evidence.get("claims", []):
        if claim.get("kind") in {"validation", "test", "integration", "file-state"} and claim.get("evidence") not in check_evidence:
            diagnostics.append({"code": "evidence.unsupported-claim", "detail": str(claim.get("value"))})

    source_refs = {
        (source.get("stable_id"), source.get("sha256"))
        for source in evidence.get("sources_read", []) if source.get("authority") == "canonical"
    }
    for artifact in evidence.get("artifacts_drafted", []):
        references = artifact.get("canonical_references", [])
        if artifact.get("canonical") is True:
            diagnostics.append({"code": "evidence.canonical-draft-forbidden", "detail": str(artifact.get("path"))})
        reference_keys = {(item.get("stable_id"), item.get("sha256")) for item in references if isinstance(item, dict)}
        if not reference_keys or not reference_keys <= source_refs:
            diagnostics.append({"code": "evidence.missing-canonical-reference", "detail": str(artifact.get("path"))})
    return diagnostics


def _normalized_scope(value: str) -> tuple[str, ...]:
    normalized = value.replace("\\", "/")
    if normalized.startswith("//") or normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return ()
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        return ()
    return tuple(part.casefold() for part in path.parts)


def _overlap(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    return bool(left and right and (left == right[: len(left)] or right == left[: len(right)]))


def validate_parallel_plan(plan: dict[str, Any]) -> dict[str, Any]:
    diagnostics: list[dict[str, str]] = []
    process_root = Path(__file__).resolve().parent
    schema_errors = _schema_errors(process_root, "parallel-plan.schema.json", plan)
    if schema_errors:
        return {
            "schema_version": "1.0", "plan_id": plan.get("plan_id"), "status": "blocked",
            "promotion_allowed": False,
            "diagnostics": [{"code": "parallel.schema", "detail": location} for location in schema_errors],
        }
    tasks = plan.get("tasks", [])
    raw_task_ids = [task.get("task_id") for task in tasks if isinstance(task, dict)]
    task_ids = set(raw_task_ids)
    if len(raw_task_ids) != len(task_ids):
        diagnostics.append({"code": "parallel.duplicate-task-id", "detail": "task IDs must be unique"})
    evidence_paths: set[tuple[str, ...]] = set()
    scopes: list[tuple[str, tuple[str, ...]]] = []
    declared_check_ids: list[str] = []
    for task in tasks:
        task_id = str(task.get("task_id"))
        dependencies = task.get("dependencies", [])
        if dependencies:
            diagnostics.append({"code": "parallel.unresolved-dependency", "detail": f"{task_id}: {dependencies}"})
        if any(dep not in task_ids for dep in dependencies):
            diagnostics.append({"code": "parallel.unknown-dependency", "detail": task_id})
        if task.get("policy_or_lifecycle_decision") is not False:
            diagnostics.append({"code": "parallel.authority-decision", "detail": task_id})
        evidence_path = _normalized_scope(str(task.get("evidence_path", "")))
        if not evidence_path:
            diagnostics.append({"code": "parallel.unsafe-evidence-path", "detail": task_id})
        elif evidence_path in evidence_paths:
            diagnostics.append({"code": "parallel.shared-evidence", "detail": task_id})
        evidence_paths.add(evidence_path)
        if not task.get("owner") or not task.get("stop_condition") or not task.get("focused_checks"):
            diagnostics.append({"code": "parallel.incomplete-task-boundary", "detail": task_id})
        declared_check_ids.extend(row.get("check_id") for row in task.get("focused_checks", []))
        for raw_scope in task.get("write_scopes", []):
            scope = _normalized_scope(raw_scope)
            if not scope:
                diagnostics.append({"code": "parallel.unsafe-scope", "detail": str(raw_scope)})
                continue
            for other_id, other_scope in scopes:
                if _overlap(scope, other_scope):
                    diagnostics.append({"code": "parallel.overlapping-scope", "detail": f"{other_id} <-> {task_id}"})
            scopes.append((task_id, scope))
    combined = [row for row in plan.get("combined_checks", []) if isinstance(row, dict)]
    declared_check_ids.extend(row.get("check_id") for row in combined)
    if len(declared_check_ids) != len(set(declared_check_ids)):
        diagnostics.append({"code": "parallel.duplicate-check-id", "detail": "declared check IDs must be globally unique"})
    missing_checks = REQUIRED_COMBINED_CHECKS - {row.get("kind") for row in combined}
    if missing_checks:
        diagnostics.append({"code": "parallel.missing-combined-gate", "detail": ",".join(sorted(missing_checks))})
    if not plan.get("integration_owner"):
        diagnostics.append({"code": "parallel.missing-integration-owner", "detail": "integration owner is required"})
    serialize_codes = {"parallel.unresolved-dependency", "parallel.overlapping-scope", "parallel.authority-decision"}
    status = "parallel-safe"
    if diagnostics:
        status = "serialize" if any(item["code"] in serialize_codes for item in diagnostics) else "blocked"
    promotion_allowed = False
    if plan.get("promotion_requested") is True:
        evidence = plan.get("promotion_evidence")
        if not isinstance(evidence, dict):
            diagnostics.append({"code": "parallel.missing-promotion-evidence", "detail": "structured results required"})
        else:
            task_result_rows = [row for row in evidence.get("task_results", []) if isinstance(row, dict)]
            task_result_ids = [row.get("task_id") for row in task_result_rows]
            task_results = {row.get("task_id"): row for row in task_result_rows}
            all_result_rows = [
                result
                for task_result in task_result_rows
                for result in task_result.get("checks", [])
                if isinstance(result, dict)
            ]
            for task in tasks:
                expected = {row.get("check_id") for row in task.get("focused_checks", []) if isinstance(row, dict)}
                actual_rows = task_results.get(task.get("task_id"), {}).get("checks", [])
                passed = {
                    row.get("check_id") for row in actual_rows
                    if isinstance(row, dict) and row.get("result") == "passed" and row.get("evidence")
                }
                if not expected or not expected <= passed:
                    diagnostics.append({"code": "parallel.focused-evidence-incomplete", "detail": str(task.get("task_id"))})
            combined_result_rows = [row for row in evidence.get("combined_results", []) if isinstance(row, dict)]
            combined_results = {row.get("check_id"): row for row in combined_result_rows}
            all_result_rows.extend(combined_result_rows)
            result_ids = [row.get("check_id") for row in all_result_rows]
            result_evidence = [row.get("evidence") for row in all_result_rows]
            declared_ids = set(declared_check_ids)
            if (
                len(task_result_ids) != len(set(task_result_ids))
                or set(task_result_ids) != task_ids
                or len(result_ids) != len(set(result_ids))
                or set(result_ids) != declared_ids
                or len(result_evidence) != len(set(result_evidence))
            ):
                diagnostics.append({"code": "parallel.reused-result", "detail": "each declared check needs one distinct result and evidence"})
            for check in combined:
                result = combined_results.get(check.get("check_id"), {})
                if result.get("result") != "passed" or not result.get("evidence"):
                    diagnostics.append({"code": "parallel.combined-evidence-incomplete", "detail": str(check.get("check_id"))})
        promotion_allowed = not diagnostics
    if diagnostics and status == "parallel-safe":
        status = "blocked"
    return {
        "schema_version": "1.0",
        "plan_id": plan.get("plan_id"),
        "status": status,
        "promotion_allowed": promotion_allowed,
        "diagnostics": diagnostics,
    }
