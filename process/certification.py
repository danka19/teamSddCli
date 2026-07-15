"""Deterministic synthetic certification runner and coverage inventory.

This module certifies fixtures only.  It never invokes a model, grants human
authority, or mutates canonical project state.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator


class CertificationError(ValueError):
    """Stable fail-closed certification contract error."""


ALLOWED_OPERATIONS = {
    "validate-change": ("scripts/validate_change.py", "--allow-placeholders"),
    "certification-preflight": None,
}
PRIVATE = re.compile(
    r"(?i)(?:password|secret|api[_-]?key|access[_-]?token|private[_-]?key|"
    r"\bprod(?:uction)?\b|https?://|git@|[A-Za-z]:[\\/])"
)
FIXTURE_PRIVATE = re.compile(
    r"(?i)(?:\bcorp(?:orate)?\b|\binternal\b|\bprod(?:uction)?\b|https?://|"
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b)"
)
SYNTHETIC_NAMESPACES = {"synthetic", "example"}
HEADING = re.compile(r"^(#{3,4}) (Requirement|Scenario): (.+)$", re.MULTILINE)


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise CertificationError("certification.invalid-input") from error
    if not isinstance(value, dict):
        raise CertificationError("certification.invalid-input")
    return value


def _safe_relative(value: str, *, prefix: str | None = None) -> PurePosixPath:
    if not isinstance(value, str) or PRIVATE.search(value):
        raise CertificationError("certification.privacy")
    normalized = value.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or not path.parts or ".." in path.parts or normalized.startswith("//"):
        raise CertificationError("certification.privacy")
    if prefix and path.parts[0] != prefix:
        raise CertificationError("certification.privacy")
    return path


def _is_link_or_reparse(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        return bool(path.stat(follow_symlinks=False).st_file_attributes & 0x400)
    except (AttributeError, OSError):
        return False


def _validate_output(repository_root: Path, catalog_path: Path, output: Path, check: bool) -> None:
    root = repository_root.resolve()
    catalog = catalog_path.resolve()
    candidate = output.absolute()
    if _is_link_or_reparse(output) or any(_is_link_or_reparse(parent) for parent in output.parents if parent.exists()):
        raise CertificationError("certification.unsafe-output")
    try:
        resolved = candidate.resolve(strict=False)
    except OSError as error:
        raise CertificationError("certification.unsafe-output") from error
    protected = root / "process"
    if resolved == root or root in resolved.parents or resolved in root.parents or resolved == protected or protected in resolved.parents or resolved == catalog:
        raise CertificationError("certification.unsafe-output")
    if not check and output.exists():
        raise CertificationError("certification.output-exists")


def _artifact_digest(path: Path) -> str:
    digest = hashlib.sha256()
    files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    for item in files:
        digest.update(item.relative_to(path if path.is_dir() else path.parent).as_posix().encode())
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _canonical_snapshot(root: Path) -> str:
    digest = hashlib.sha256()
    for name in ("process", "openspec", "templates", "scripts", "docs"):
        base = root / name
        for path in sorted(item for item in base.rglob("*") if item.is_file()):
            relative = path.relative_to(root)
            if "__pycache__" in relative.parts or path.suffix == ".pyc":
                continue
            digest.update(relative.as_posix().encode())
            digest.update(b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _preflight(payload: dict[str, Any]) -> list[str]:
    diagnostics: list[str] = []
    context = payload.get("context", {})
    if not set(context.get("required", [])) <= set(context.get("present", [])):
        diagnostics.append("certification.missing-context")
    sources = payload.get("sources", [])
    by_id: dict[str, set[str]] = {}
    for source in sources:
        by_id.setdefault(str(source.get("id")), set()).add(str(source.get("sha256")))
    if any(len(hashes) > 1 for hashes in by_id.values()):
        diagnostics.append("certification.conflicting-sources")
    evidence_ids = set(payload.get("evidence_ids", []))
    if any(claim.get("evidence_id") not in evidence_ids for claim in payload.get("claims", [])):
        diagnostics.append("certification.fabricated-evidence")
    if payload.get("authority", {}).get("approval_claimed") is not False:
        diagnostics.append("certification.forbidden-approval")
    stop = payload.get("human_stop", {})
    if stop.get("expected") is True and stop.get("reached") is not True:
        diagnostics.append("certification.skipped-stop")
    if payload.get("lifecycle", {}).get("transition_requested") is not False:
        diagnostics.append("certification.invalid-lifecycle-transition")
    if payload.get("adapter", {}).get("result") != "available":
        diagnostics.append("certification.adapter-failure")
    if context.get("bytes", 0) > context.get("limit", 0):
        diagnostics.append("certification.context-limit")
    return diagnostics


def _case_result(root: Path, case: dict[str, Any], process_version: str) -> tuple[dict[str, Any], dict[str, Any]]:
    case_id = str(case.get("id", ""))
    operation = case.get("operation")
    if operation not in ALLOWED_OPERATIONS:
        raise CertificationError("certification.operation-not-allowed")
    fixture_rel = _safe_relative(str(case.get("fixture", "")), prefix="process")
    if len(fixture_rel.parts) < 3 or fixture_rel.parts[1] != "certification":
        raise CertificationError("certification.privacy")
    fixture = root / Path(*fixture_rel.parts)
    if not fixture.exists() or _is_link_or_reparse(fixture):
        raise CertificationError("certification.privacy")
    fixture_files = [fixture] if fixture.is_file() else sorted(path for path in fixture.rglob("*") if path.is_file())
    for path in fixture_files:
        if _is_link_or_reparse(path):
            raise CertificationError("certification.privacy")
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise CertificationError("certification.privacy") from error
        if PRIVATE.search(text):
            raise CertificationError("certification.privacy")
        if FIXTURE_PRIVATE.search(text):
            raise CertificationError("certification.privacy")

    snapshot_before = _canonical_snapshot(root)
    input_hash = _artifact_digest(fixture)
    raw: dict[str, Any] = {"case_id": case_id, "operation": operation}
    if operation == "certification-preflight":
        payload = _load_yaml(fixture)
        if payload.get("namespace") not in SYNTHETIC_NAMESPACES:
            raise CertificationError("certification.privacy")
        codes = _preflight(payload)
        observed = "blocked" if codes else "passed"
        raw.update({"payload_sha256": input_hash, "diagnostics": codes})
    else:
        script, flag = ALLOWED_OPERATIONS[operation]  # type: ignore[misc]
        command = [sys.executable, str(root / script), flag, str(fixture)]
        completed = subprocess.run(
            command, cwd=root, shell=False, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=30, check=False,
        )
        observed = "passed" if completed.returncode == 0 else "blocked"
        codes = [] if completed.returncode == 0 else ["certification.validator-failed"]
        raw.update({"argv": ["<python>", script, flag, str(fixture_rel)], "exit_code": completed.returncode,
                    "stdout": completed.stdout, "stderr": completed.stderr})
    expected = case.get("expected", {})
    matches = isinstance(expected, dict) and expected.get("status") == observed and set(expected.get("codes", [])) == set(codes)
    snapshot_after = _canonical_snapshot(root)
    output_hash = hashlib.sha256(json.dumps({"observed": observed, "codes": sorted(codes)}, sort_keys=True).encode()).hexdigest()
    family = str(case.get("family"))
    normalized = {
        "evidence_id": f"evidence-{case_id}", "run_id": f"fixture-{process_version}-{case_id}",
        "case_id": case_id, "family": family,
        "role": case.get("role", "not-applicable"), "change_class": case.get("change_class", "not-applicable"),
        "expected_output": case.get("expected_output", "deterministic semantic result"),
        "execution_mode": "deterministic-fixture",
        "observed": observed,
        "diagnostic_codes": sorted(codes),
        "matches_golden": matches,
        "canonical_snapshot_before": snapshot_before, "canonical_snapshot_after": snapshot_after,
        "canonical_mutated": snapshot_before != snapshot_after,
        "read_pack": {"not_applicable_reason": "deterministic validator fixture has no model context"},
        "operation": {"name": operation, "input_fixture": str(fixture_rel),
                      "input_artifact_sha256": input_hash, "output_artifact_sha256": output_hash},
        "validation": {"result": observed, "codes": sorted(codes)},
        "human_intervention": {"required": False, "performed": False, "type": "none"},
        "forbidden_action": {"expected": family in {"forbidden-approval", "invalid-lifecycle-transition"},
                             "detected": any(code in {"certification.forbidden-approval", "certification.invalid-lifecycle-transition"} for code in codes)},
        "human_stop": {"expected": family == "skipped-stop", "reached": family != "skipped-stop" or "certification.skipped-stop" not in codes},
        "limitations": ["synthetic deterministic fixture; no model or adapter runtime executed"],
    }
    return normalized, raw


def certify_release(
    repository_root: Path, catalog_path: Path, raw_output: Path, *, check: bool = False
) -> dict[str, Any]:
    """Run the immutable synthetic catalog and return normalized evidence.

    ``check`` executes and compares but does not create the raw artifact.
    """
    root = repository_root.resolve()
    catalog_path = catalog_path.resolve()
    _validate_output(root, catalog_path, raw_output, check)
    catalog = _load_yaml(catalog_path)
    case_schema = json.loads((root / "process/schemas/certification-case.schema.json").read_text(encoding="utf-8"))
    if list(Draft202012Validator(case_schema).iter_errors(catalog)):
        raise CertificationError("certification.invalid-input")
    if catalog.get("schema_version") != "1.0" or not isinstance(catalog.get("cases"), list):
        raise CertificationError("certification.invalid-input")
    identifiers = [case.get("id") for case in catalog["cases"] if isinstance(case, dict)]
    if len(identifiers) != len(catalog["cases"]) or len(set(identifiers)) != len(identifiers):
        raise CertificationError("certification.invalid-input")
    process_version = (root / "process/VERSION").read_text(encoding="utf-8").strip()
    results: list[dict[str, Any]] = []
    raw_cases: list[dict[str, Any]] = []
    for case in catalog["cases"]:
        normalized, raw = _case_result(root, case, process_version)
        results.append(normalized)
        raw_cases.append(raw)
    bundle = {
        "schema_version": "1.0", "evidence_kind": "deterministic-fixture",
        "actual_model_run": False, "model": {"family": "not-executed", "id": "not-executed", "runtime": "not-executed"},
        "cases": raw_cases,
    }
    bundle_bytes = (json.dumps(bundle, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
    logical_version = raw_output.name
    evidence = {
        "schema_version": "1.0",
        "status": "passed" if all(row["matches_golden"] for row in results) else "failed",
        "evidence_kind": "deterministic-fixture", "actual_model_run": False,
        "model": {"family": "not-executed", "id": "not-executed", "runtime": "not-executed"},
        "adapter": {"family": "not-executed", "version": "not-executed"},
        "process_package_version": process_version,
        "planned_dimensions": catalog.get("planned_dimensions", {}),
        "canonical_mutated": any(row["canonical_mutated"] for row in results),
        "cases": results,
        "raw_artifact": {"logical_version": logical_version, "filename": "bundle.json",
                         "sha256": hashlib.sha256(bundle_bytes).hexdigest(), "stored_in_git": False},
    }
    evidence["normalized_sha256"] = hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    evidence_schema = json.loads((root / "process/schemas/certification-evidence.schema.json").read_text(encoding="utf-8"))
    if list(Draft202012Validator(evidence_schema).iter_errors(evidence)):
        raise CertificationError("certification.invalid-evidence")
    if not check and evidence["status"] == "passed":
        raw_output.mkdir(parents=True, exist_ok=False)
        (raw_output / "bundle.json").write_bytes(bundle_bytes)
    return evidence


def _selectors(path: Path, source_kind: str, capability: str) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    requirement = ""
    rows: list[dict[str, str]] = []
    for _marks, kind, title in HEADING.findall(text):
        if kind == "Requirement":
            requirement = title
        elif requirement:
            rows.append({"source_kind": source_kind, "capability": capability,
                         "requirement": requirement, "scenario": title})
    return rows


def _delta_selector_groups(path: Path, capability: str) -> list[tuple[str, str, list[dict[str, str]]]]:
    mode = ""
    requirement = ""
    groups: list[tuple[str, str, list[dict[str, str]]]] = []
    scenarios: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        mode_match = re.match(r"^## (ADDED|MODIFIED|REMOVED) Requirements$", line)
        if mode_match:
            if requirement:
                groups.append((mode, requirement, scenarios))
            mode, requirement, scenarios = mode_match.group(1), "", []
            continue
        requirement_match = re.match(r"^### Requirement: (.+)$", line)
        if requirement_match:
            if requirement:
                groups.append((mode, requirement, scenarios))
            requirement, scenarios = requirement_match.group(1), []
            continue
        scenario_match = re.match(r"^#### Scenario: (.+)$", line)
        if scenario_match and requirement:
            scenarios.append({"source_kind": "delta", "capability": capability,
                              "requirement": requirement, "scenario": scenario_match.group(1)})
    if requirement:
        groups.append((mode, requirement, scenarios))
    return groups


def _delta_targets(path: Path, capability: str, change: str) -> set[tuple[str, str, str, str]]:
    mode = ""
    targets: set[tuple[str, str, str, str]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        mode_match = re.match(r"^## (ADDED|MODIFIED|REMOVED) Requirements$", line)
        if mode_match:
            mode = mode_match.group(1)
            continue
        requirement_match = re.match(r"^### Requirement: (.+)$", line)
        if requirement_match and mode in {"MODIFIED", "REMOVED"}:
            targets.add((change, mode, capability, requirement_match.group(1)))
    return targets


def _pytest_node_exists(root: Path, node: str) -> bool:
    target = node.removeprefix("pytest:")
    filename, separator, test_name = target.partition("::")
    path = root / filename
    if not path.is_file():
        return False
    return not separator or bool(re.search(rf"^def {re.escape(test_name)}\b", path.read_text(encoding="utf-8"), re.MULTILINE))


def build_coverage_report(repository_root: Path, inventory_path: Path) -> dict[str, Any]:
    root = repository_root.resolve()
    inventory = _load_yaml(inventory_path.resolve())
    catalog = _load_yaml(root / "process/certification/cases.yaml")
    case_ids = {row.get("id") for row in catalog.get("cases", []) if isinstance(row, dict)}
    effective: dict[tuple[str, str], list[dict[str, str]]] = {}
    delta_sources: list[dict[str, Any]] = []
    for source in inventory.get("sources", []):
        if not isinstance(source, dict):
            raise CertificationError("coverage.invalid-source")
        rel = _safe_relative(str(source.get("path", "")))
        path = root / Path(*rel.parts)
        if source.get("kind") == "accepted":
            for row in _selectors(path, "accepted", str(source.get("capability"))):
                effective.setdefault((row["capability"], row["requirement"]), []).append(row)
        elif source.get("kind") == "delta":
            delta_sources.append({**source, "resolved": path})
        else:
            raise CertificationError("coverage.invalid-source")
    touched: set[tuple[str, str]] = set()
    for source in delta_sources:
        for operation, requirement, scenarios in _delta_selector_groups(source["resolved"], source["capability"]):
            key = (source["capability"], requirement)
            if key in touched:
                raise CertificationError("coverage.delta-collision")
            touched.add(key)
            if operation == "ADDED":
                if key in effective:
                    raise CertificationError("coverage.delta-collision")
                effective[key] = scenarios
            elif operation == "MODIFIED":
                if key not in effective:
                    raise CertificationError("coverage.unknown-delta-target")
                effective[key] = scenarios
            elif operation == "REMOVED":
                if key not in effective:
                    raise CertificationError("coverage.unknown-delta-target")
                del effective[key]
    all_rows = [row for key in sorted(effective) for row in effective[key]]
    discovered_keys = [(row["source_kind"], row["capability"], row["requirement"], row["scenario"]) for row in all_rows]
    if len(discovered_keys) != len(set(discovered_keys)):
        raise CertificationError("coverage.duplicate-selector")
    overrides = inventory.get("coverage", [])
    override_keys = [(r.get("source_kind"), r.get("capability"), r.get("requirement"), r.get("scenario")) for r in overrides]
    if len(override_keys) != len(set(override_keys)):
        raise CertificationError("coverage.duplicate-selector")
    by_key = {(r["source_kind"], r["capability"], r["requirement"], r["scenario"]): r for r in overrides}
    evidence_rules = inventory.get("evidence_rules", [])
    gap_rules = inventory.get("gap_rules", [])
    if len({row.get("capability") for row in evidence_rules}) != len(evidence_rules) or len({row.get("capability") for row in gap_rules}) != len(gap_rules):
        raise CertificationError("coverage.duplicate-rule")
    evidence_by_capability = {row["capability"]: row["evidence"] for row in evidence_rules}
    gap_by_capability = {row["capability"]: row["gap"] for row in gap_rules}
    future_declarations = inventory.get("future_work", [])
    future_matches = [0] * len(future_declarations)
    coverage: list[dict[str, Any]] = []
    for row in all_rows:
        key = (row["source_kind"], row["capability"], row["requirement"], row["scenario"])
        declared = by_key.pop(key, {})
        matched_future = False
        for index, future in enumerate(future_declarations):
            if (future.get("capability") == row["capability"] and future.get("requirement") == row["requirement"]
                    and (not future.get("scenario") or future.get("scenario") == row["scenario"])):
                future_matches[index] += 1
                matched_future = True
                break
        if matched_future:
            continue
        evidence = declared.get("evidence")
        gap = declared.get("gap")
        if gap is None and evidence is None:
            if row["capability"] in gap_by_capability:
                gap = gap_by_capability[row["capability"]]
            else:
                evidence = evidence_by_capability.get(row["capability"])
        if gap is not None:
            if not isinstance(gap, dict) or set(gap) != {"owner", "risk", "reason", "compensation", "follow_up"} or not all(gap.values()):
                raise CertificationError("coverage.invalid-gap")
        elif not evidence:
            raise CertificationError("coverage.unmapped-scenario")
        if isinstance(evidence, str) and evidence.startswith("case:") and evidence[5:] not in case_ids:
            raise CertificationError("coverage.unknown-case")
        if isinstance(evidence, str) and evidence.startswith("pytest:") and not _pytest_node_exists(root, evidence):
            raise CertificationError("coverage.unknown-pytest")
        coverage.append({**row, **({"evidence": evidence} if evidence else {"gap": gap})})
    if by_key:
        raise CertificationError("coverage.unknown-selector")
    if any(count == 0 for count in future_matches):
        raise CertificationError("coverage.unknown-future-selector")

    accepted_requirements: dict[str, set[str]] = {}
    for source in inventory.get("sources", []):
        if source.get("kind") == "accepted":
            rows = _selectors(root / source["path"], "accepted", source["capability"])
            accepted_requirements[source["capability"]] = {row["requirement"] for row in rows}
    declared_targets: set[tuple[str, str, str, str]] = set()
    for target in inventory.get("delta_targets", []):
        if target.get("kind") in {"MODIFIED", "REMOVED"} and target.get("requirement") not in accepted_requirements.get(target.get("capability"), set()):
            raise CertificationError("coverage.unknown-delta-target")
        declared_targets.add((target.get("change"), target.get("kind"), target.get("capability"), target.get("requirement")))
    actual_targets: set[tuple[str, str, str, str]] = set()
    for source in inventory.get("sources", []):
        if source.get("kind") != "delta":
            continue
        relative = str(source["path"])
        parts = PurePosixPath(relative).parts
        change = parts[2] if len(parts) > 2 and parts[:2] == ("openspec", "changes") else ""
        actual_targets |= _delta_targets(root / relative, source["capability"], change)
    if actual_targets != declared_targets:
        raise CertificationError("coverage.delta-target-inventory")
    gap_count = sum("gap" in row for row in coverage)
    covered_count = len(coverage) - gap_count
    future_count = sum(future_matches)
    report = {"schema_version": "1.0", "status": "gaps" if gap_count else "complete", "coverage": coverage,
              "future_work": list(future_declarations),
              "summary": {"effective_scenarios": len(all_rows), "covered": covered_count,
                          "gaps": gap_count, "future_work": future_count}}
    report_schema = json.loads((root / "process/schemas/coverage-report.schema.json").read_text(encoding="utf-8"))
    if list(Draft202012Validator(report_schema).iter_errors(report)):
        raise CertificationError("coverage.invalid-report")
    return report
