"""Validate deterministic SDD change package artifacts.

The validator intentionally supports a small YAML subset used by this
repository's templates. Keeping the gate dependency-free makes the first
process layer easier to transfer into constrained corporate environments.
"""

from __future__ import annotations

import argparse
import subprocess
import re
import sys
from pathlib import Path
from typing import Any, Iterable


BASE_REQUIRED_FILES = (
    "change.yaml",
    "proposal.md",
    "tasks.md",
    "traceability.yaml",
)

FULL_REQUIRED_FILES = (
    "design.md",
    "qa/test-plan.md",
    "qa/automation-plan.md",
)

OPTIONAL_VALIDATION_FILES = ("waivers.yaml",)

REQUIRED_CHANGE_FIELDS = (
    "id",
    "title",
    "mode",
    "type",
    "status",
    "capability",
)

REQUIRED_CHANGE_SECTIONS = ("systems", "quality")
REQUIRED_QUALITY_FIELDS = (
    "behavior_scope",
    "public_api",
    "mobile_at",
    "data_risk",
    "security_review",
    "rollback_cost",
)

ALLOWED_MODES = {"thin", "full"}
ALLOWED_TYPES = {
    "new_feature",
    "behavior_change",
    "bugfix",
    "refactor",
    "removal",
    "config_ops",
    "docs_only",
}
ALLOWED_STATUSES = {
    "draft",
    "spec_review",
    "approved",
    "in_implementation",
    "ready_to_archive",
    "archived",
}
ALLOWED_SPEC_CHANGE = {"required", "none"}
ALLOWED_BEHAVIOR_SCOPES = {"focused", "broad"}
ALLOWED_IMPACT_VALUES = {"impacted", "not_impacted"}
ALLOWED_SECURITY_REVIEW = {"required", "not_required"}
ALLOWED_ROLLBACK_COSTS = {"low", "high"}
ALLOWED_WAIVER_TYPES = {
    "no_spec_change",
    "test_plan_deferred",
    "test_case_deferred",
    "automation_deferred",
    "artifact_not_applicable",
    "documentation_deferred",
    "design_exception",
}
ALLOWED_NO_SPEC_CHANGE_TYPES = {"docs_only", "refactor", "config_ops"}
FULL_MODE_TYPES = {"new_feature"}
ARCHIVE_READY_STATUSES = {"ready_to_archive", "archived"}
CHANGE_ID_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9]+-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
PLACEHOLDER_PATTERN = re.compile(
    r"(<[^>\n]+>|TODO|TBD|REPLACE|CHANGE[-_]ID|AUTH-YYYY|YOUR[-_ ])",
    re.IGNORECASE,
)
FORBIDDEN_APPROVER_PATTERN = re.compile(r"(^|[-_ ])(?:ai|bot|assistant)(?:[-_ ]|$)", re.IGNORECASE)


def validate_change_package(
    package_dir: str | Path,
    *,
    allow_placeholders: bool = False,
) -> list[str]:
    """Return validation errors for one SDD change package directory."""

    package_path = Path(package_dir)
    errors: list[str] = []

    if not package_path.exists():
        return [f"{package_path}: package directory does not exist"]
    if not package_path.is_dir():
        return [f"{package_path}: expected a directory"]

    change_path = package_path / "change.yaml"
    if not change_path.is_file():
        return [f"{package_path}: missing required artifact change.yaml"]

    metadata = read_change_metadata(change_path)
    errors.extend(validate_change_metadata(change_path, metadata, allow_placeholders))

    mode = scalar_value(metadata.get("mode"))
    change_type = scalar_value(metadata.get("type"))
    status = scalar_value(metadata.get("status"))
    spec_change = scalar_value(metadata.get("spec_change")) or "required"

    waivers = parse_named_records(package_path / "waivers.yaml", "waivers")
    waiver_errors = validate_waivers(
        package_path / "waivers.yaml",
        waivers,
        metadata,
        allow_placeholders=allow_placeholders,
    )
    errors.extend(f"{package_path}: {error}" for error in waiver_errors)
    waivers_by_artifact = index_waivers_by_artifact(waivers)
    waivers_by_id = {scalar_value(waiver.get("id")): waiver for waiver in waivers if scalar_value(waiver.get("id"))}

    for relative_path in BASE_REQUIRED_FILES:
        file_path = package_path / relative_path
        if not file_path.is_file():
            errors.append(f"{package_path}: missing required artifact {relative_path}")
            continue
        if not file_path.read_text(encoding="utf-8").strip():
            errors.append(f"{package_path}: artifact {relative_path} must not be empty")

    if mode == "full":
        for relative_path in FULL_REQUIRED_FILES:
            file_path = package_path / relative_path
            if file_path.is_file():
                if not file_path.read_text(encoding="utf-8").strip():
                    errors.append(f"{package_path}: artifact {relative_path} must not be empty")
                continue
            if not has_artifact_waiver(waivers_by_artifact, relative_path):
                errors.append(f"{package_path}: missing required artifact {relative_path}")

        test_case_files = sorted((package_path / "qa" / "test-cases").glob("**/*.md"))
        if test_case_files:
            for test_case in test_case_files:
                if not test_case.read_text(encoding="utf-8").strip():
                    errors.append(
                        f"{package_path}: artifact {test_case.relative_to(package_path)} must not be empty"
                    )
        elif not has_artifact_waiver(waivers_by_artifact, "qa/test-cases"):
            errors.append(f"{package_path}: missing required artifact qa/test-cases")

    spec_files = sorted((package_path / "specs").glob("**/spec.md"))
    has_no_spec_change = spec_change == "none"
    valid_no_spec_change = has_valid_no_spec_change_exception(
        change_type, spec_change, spec_files, waivers_by_artifact
    )

    if has_no_spec_change and not valid_no_spec_change:
        errors.append(
            f"{package_path}: no-spec-change rationale is allowed only for "
            f"{sorted(ALLOWED_NO_SPEC_CHANGE_TYPES)} with reviewer approval and replacement evidence"
        )

    if spec_change == "required" and not spec_files:
        errors.append(f"{package_path}: missing at least one specs/**/spec.md file")
    elif spec_change == "none" and spec_files:
        errors.append(f"{package_path}: spec_change 'none' cannot include specs/**/spec.md files")

    requirement_scenarios: set[tuple[str, str]] = set()
    if spec_files:
        for spec_file in spec_files:
            if not spec_file.read_text(encoding="utf-8").strip():
                errors.append(
                    f"{package_path}: artifact {spec_file.relative_to(package_path)} must not be empty"
                )
        requirement_scenarios, spec_errors = extract_requirement_scenarios(spec_files)
        errors.extend(f"{package_path}: {error}" for error in spec_errors)
        if not requirement_scenarios:
            errors.append(f"{package_path}: specs must contain at least one requirement scenario")

    traceability_path = package_path / "traceability.yaml"
    traceability_records = (
        parse_named_records(traceability_path, "requirements")
        if traceability_path.is_file()
        else []
    )

    if requirement_scenarios:
        for requirement, scenario in requirement_scenarios:
            if not any(
                scalar_value(record.get("requirement")) == requirement
                and scalar_value(record.get("scenario")) == scenario
                for record in traceability_records
            ):
                errors.append(
                    f"{package_path}: traceability.yaml missing link for "
                    f"requirement '{requirement}' scenario '{scenario}'"
                )

    errors.extend(
        validate_traceability(
            package_path,
            traceability_records,
            mode=mode,
            status=status,
            waivers_by_id=waivers_by_id,
        )
    )
    errors.extend(validate_mode_contracts(package_path, metadata, mode, change_type))

    if not allow_placeholders:
        errors.extend(find_placeholder_errors(package_path))

    return errors


def validate_change_metadata(
    path: Path,
    metadata: dict[str, Any],
    allow_placeholders: bool,
) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_CHANGE_FIELDS:
        value = scalar_value(metadata.get(field))
        if value is None or value == "":
            errors.append(f"{path}: missing required field '{field}'")

    for section in REQUIRED_CHANGE_SECTIONS:
        if section not in metadata or not isinstance(metadata.get(section), dict):
            errors.append(f"{path}: missing required section '{section}'")

    quality = metadata.get("quality")
    quality_map = quality if isinstance(quality, dict) else {}
    for field in REQUIRED_QUALITY_FIELDS:
        value = scalar_value(quality_map.get(field))
        if value is None or value == "":
            errors.append(f"{path}: quality.{field} is required")

    change_id = scalar_value(metadata.get("id"))
    if change_id and not allow_placeholders and not CHANGE_ID_PATTERN.match(change_id):
        errors.append(f"{path}: id '{change_id}' must match PROJECT-YYYY-NNN-short-name")

    mode = scalar_value(metadata.get("mode"))
    if mode and mode not in ALLOWED_MODES:
        errors.append(f"{path}: mode '{mode}' must be one of {sorted(ALLOWED_MODES)}")

    change_type = scalar_value(metadata.get("type"))
    if change_type and change_type not in ALLOWED_TYPES:
        errors.append(f"{path}: type '{change_type}' must be one of {sorted(ALLOWED_TYPES)}")

    status = scalar_value(metadata.get("status"))
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"{path}: status '{status}' must be one of {sorted(ALLOWED_STATUSES)}")

    spec_change = scalar_value(metadata.get("spec_change")) or "required"
    if spec_change not in ALLOWED_SPEC_CHANGE:
        errors.append(
            f"{path}: spec_change '{spec_change}' must be one of {sorted(ALLOWED_SPEC_CHANGE)}"
        )

    for field, allowed_values in (
        ("behavior_scope", ALLOWED_BEHAVIOR_SCOPES),
        ("public_api", ALLOWED_IMPACT_VALUES),
        ("mobile_at", ALLOWED_IMPACT_VALUES),
        ("data_risk", ALLOWED_IMPACT_VALUES),
        ("security_review", ALLOWED_SECURITY_REVIEW),
        ("rollback_cost", ALLOWED_ROLLBACK_COSTS),
    ):
        value = scalar_value(quality_map.get(field))
        if value and value not in allowed_values:
            errors.append(
                f"{path}: quality.{field} '{value}' must be one of {sorted(allowed_values)}"
            )

    return errors


def read_change_metadata(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_section: str | None = None
    current_list_key: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if indent == 0 and ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                data[key] = {}
                current_section = key
                current_list_key = None
            else:
                data[key] = normalize_scalar(value)
                current_section = None
                current_list_key = None
            continue

        if current_section and indent == 2 and ":" in stripped:
            section = data.setdefault(current_section, {})
            if not isinstance(section, dict):
                continue
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                section[key] = []
                current_list_key = key
            else:
                section[key] = normalize_scalar(value)
                current_list_key = None
            continue

        if current_section and current_list_key and indent >= 4 and stripped.startswith("- "):
            section = data.get(current_section)
            if isinstance(section, dict):
                section.setdefault(current_list_key, [])
                values = section[current_list_key]
                if isinstance(values, list):
                    values.append(normalize_scalar(stripped[2:].strip()) or "")

    return data


def normalize_scalar(value: str) -> str | None:
    value = value.strip()
    if value == "":
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def scalar_value(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    return None


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        if value == "[]":
            return []
        return [value]
    return []


def parse_named_records(path: Path, root_key: str) -> list[dict[str, Any]]:
    if not path.is_file():
        return []

    records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    current_list_key: str | None = None
    in_root = False
    root_indent = 0

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()

        if not in_root:
            if stripped == f"{root_key}:":
                in_root = True
                root_indent = indent
            continue

        if indent <= root_indent and stripped != f"{root_key}:":
            break

        if stripped.startswith("- ") and indent == root_indent + 2:
            if current:
                records.append(current)
            current = {}
            current_list_key = None
            remainder = stripped[2:].strip()
            if remainder and ":" in remainder:
                key, value = remainder.split(":", 1)
                value = normalize_scalar(value)
                current[key.strip()] = value if value is not None else ""
            continue

        if current is None:
            continue

        if stripped.startswith("- ") and current_list_key and indent >= root_indent + 4:
            current.setdefault(current_list_key, [])
            values = current[current_list_key]
            if isinstance(values, list):
                values.append(normalize_scalar(stripped[2:].strip()) or "")
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            current[key] = []
            current_list_key = key
        else:
            current[key] = normalize_scalar(value)
            current_list_key = None

    if current:
        records.append(current)

    return records


def extract_requirement_scenarios(spec_files: Iterable[Path]) -> tuple[set[tuple[str, str]], list[str]]:
    pairs: set[tuple[str, str]] = set()
    errors: list[str] = []

    for spec_file in spec_files:
        current_requirement: str | None = None
        requirement_has_scenario = False

        for line_number, line in enumerate(spec_file.read_text(encoding="utf-8").splitlines(), start=1):
            if line.startswith("### Requirement:"):
                if current_requirement and not requirement_has_scenario:
                    errors.append(
                        f"{spec_file}:{line_number}: requirement '{current_requirement}' has no scenario"
                    )
                current_requirement = line.split(":", 1)[1].strip()
                requirement_has_scenario = False
                continue

            if line.startswith("#### Scenario:"):
                scenario = line.split(":", 1)[1].strip()
                if not current_requirement:
                    errors.append(f"{spec_file}:{line_number}: scenario appears before a requirement")
                    continue
                pairs.add((current_requirement, scenario))
                requirement_has_scenario = True

        if current_requirement and not requirement_has_scenario:
            errors.append(f"{spec_file}: requirement '{current_requirement}' has no scenario")

    return pairs, errors


def validate_traceability(
    package_path: Path,
    records: list[dict[str, Any]],
    *,
    mode: str | None,
    status: str | None,
    waivers_by_id: dict[str | None, dict[str, Any]],
) -> list[str]:
    errors: list[str] = []

    if not records:
        errors.append(f"{package_path}: traceability.yaml must contain at least one requirement entry")
        return errors

    for index, record in enumerate(records, start=1):
        requirement = scalar_value(record.get("requirement"))
        scenario = scalar_value(record.get("scenario"))
        row_prefix = f"{package_path}: traceability.yaml requirement row {index}"

        if not requirement:
            errors.append(f"{row_prefix} missing requirement")
        if not scenario:
            errors.append(f"{row_prefix} missing scenario")

        tasks = list_value(record.get("tasks"))
        tests = list_value(record.get("tests"))
        automated_tests = list_value(record.get("automated_tests"))
        verification = list_value(record.get("verification"))
        waivers = list_value(record.get("waivers"))

        if not tasks:
            errors.append(f"{row_prefix} missing tasks evidence")

        waiver_records = [waivers_by_id[waiver_id] for waiver_id in waivers if waiver_id in waivers_by_id]

        if not (tests or automated_tests or verification or waivers):
            errors.append(f"{row_prefix} missing verification evidence")
        elif not (tests or automated_tests or verification):
            errors.extend(
                validate_traceability_waivers(
                    row_prefix,
                    waiver_records,
                    requirement,
                    scenario,
                    evidence_kind="verification",
                )
            )

        for waiver_id in waivers:
            if waiver_id not in waivers_by_id:
                errors.append(f"{row_prefix} references unknown waiver '{waiver_id}'")

        if status in ARCHIVE_READY_STATUSES:
            for label, values in (
                ("tasks", tasks),
                ("tests", tests),
                ("automated_tests", automated_tests),
                ("verification", verification),
            ):
                if any(value.lower() == "pending" for value in values):
                    errors.append(f"{row_prefix} has pending {label} in archive-ready status")

            if mode == "full" and not automated_tests:
                automation_errors = validate_traceability_waivers(
                    row_prefix,
                    waiver_records,
                    requirement,
                    scenario,
                    evidence_kind="automation",
                )
                if not waiver_records:
                    errors.append(f"{row_prefix} missing automation evidence or waiver for full package")
                elif automation_errors:
                    errors.extend(automation_errors)

    return errors


def validate_traceability_waivers(
    row_prefix: str,
    waivers: list[dict[str, Any]],
    requirement: str | None,
    scenario: str | None,
    *,
    evidence_kind: str,
) -> list[str]:
    if not waivers:
        return []

    mismatch_errors: list[str] = []
    for waiver in waivers:
        waiver_id = scalar_value(waiver.get("id")) or "<missing-id>"
        matches, reason = waiver_matches_traceability_requirement(
            waiver,
            requirement,
            scenario,
            evidence_kind=evidence_kind,
        )
        if matches:
            return []
        mismatch_errors.append(f"{row_prefix} waiver '{waiver_id}' {reason}")

    return mismatch_errors


def waiver_matches_traceability_requirement(
    waiver: dict[str, Any],
    requirement: str | None,
    scenario: str | None,
    *,
    evidence_kind: str,
) -> tuple[bool, str]:
    waiver_type = scalar_value(waiver.get("type")) or ""
    artifact = scalar_value(waiver.get("artifact")) or ""
    requirements = list_value(waiver.get("requirements"))
    scenarios = list_value(waiver.get("scenarios"))

    if requirement and requirement not in requirements:
        return False, f"does not cover requirement '{requirement}'"
    if scenario and scenario not in scenarios:
        return False, f"does not cover scenario '{scenario}'"

    allowed_artifacts = {
        "verification": {"qa/test-plan.md", "qa/test-cases", "qa/automation-plan.md"},
        "automation": {"qa/automation-plan.md"},
    }
    allowed_types = {
        "verification": {
            "test_plan_deferred",
            "test_case_deferred",
            "automation_deferred",
            "artifact_not_applicable",
        },
        "automation": {"automation_deferred", "artifact_not_applicable"},
    }

    if artifact not in allowed_artifacts[evidence_kind] or waiver_type not in allowed_types[evidence_kind]:
        return (
            False,
            "does not cover missing "
            f"{evidence_kind} evidence with a matching artifact/type "
            f"(artifact '{artifact}', type '{waiver_type}')",
        )

    return True, ""


def validate_waivers(
    path: Path,
    waivers: list[dict[str, Any]],
    metadata: dict[str, Any],
    *,
    allow_placeholders: bool,
) -> list[str]:
    if not path.is_file():
        return []

    errors: list[str] = []
    seen_ids: set[str] = set()
    review = metadata.get("review")
    review_map = review if isinstance(review, dict) else {}

    for index, waiver in enumerate(waivers, start=1):
        prefix = f"waiver row {index}"
        waiver_id = scalar_value(waiver.get("id"))
        waiver_type = scalar_value(waiver.get("type"))
        artifact = scalar_value(waiver.get("artifact"))
        requirements = list_value(waiver.get("requirements"))
        scenarios = list_value(waiver.get("scenarios"))
        reason = scalar_value(waiver.get("reason"))
        evidence = list_value(waiver.get("evidence"))
        approver = scalar_value(waiver.get("approver"))
        date = scalar_value(waiver.get("date"))
        follow_up = scalar_value(waiver.get("follow_up"))
        expiry = scalar_value(waiver.get("expiry"))
        residual_risk = (scalar_value(waiver.get("residual_risk")) or "").lower()

        if not waiver_id:
            errors.append(f"{prefix} missing id")
        elif waiver_id in seen_ids:
            errors.append(f"{prefix} duplicates waiver id '{waiver_id}'")
        else:
            seen_ids.add(waiver_id)

        if not waiver_type:
            errors.append(f"{prefix} missing type")
        elif waiver_type not in ALLOWED_WAIVER_TYPES:
            errors.append(
                f"{prefix} type '{waiver_type}' must be one of {sorted(ALLOWED_WAIVER_TYPES)}"
            )

        if not artifact:
            errors.append(f"{prefix} missing artifact")
        if not requirements:
            errors.append(f"{prefix} missing requirements")
        if not scenarios:
            errors.append(f"{prefix} missing scenarios")
        if not reason:
            errors.append(f"{prefix} missing reason")
        if not evidence:
            errors.append(f"{prefix} missing evidence")
        if not approver:
            errors.append(f"{prefix} missing approver")
        if not date:
            errors.append(f"{prefix} missing date")

        if residual_risk in {"true", "yes", "1"} and not (follow_up or expiry):
            errors.append(f"{prefix} must include follow_up or expiry when residual_risk is true")

        if (
            artifact
            and approver
            and not (allow_placeholders and PLACEHOLDER_PATTERN.search(approver))
            and not approver_matches_artifact(
            artifact,
            approver,
            waiver_type,
            review_map,
            )
        ):
            errors.append(
                f"{prefix} approver '{approver}' is not valid for artifact '{artifact}'"
            )

    return [f"{path}: {error}" for error in errors]


def approver_matches_artifact(
    artifact: str,
    approver: str,
    waiver_type: str | None,
    review_map: dict[str, Any],
) -> bool:
    if FORBIDDEN_APPROVER_PATTERN.search(approver):
        return False

    category = waiver_approval_category(artifact, waiver_type)
    allowed = allowed_approvers_for_category(category, review_map)
    return approver in allowed


def waiver_approval_category(artifact: str, waiver_type: str | None) -> str:
    artifact = artifact.lower()

    if waiver_type == "no_spec_change" or artifact == "specs":
        return "documentation"
    if waiver_type == "design_exception" or artifact == "design.md":
        return "design"
    if artifact.startswith("qa/automation") or "automation" in artifact or waiver_type == "automation_deferred":
        return "automation"
    if artifact.startswith("qa/test") or artifact == "qa/test-cases" or waiver_type in {
        "test_plan_deferred",
        "test_case_deferred",
    }:
        return "qa"
    if waiver_type == "documentation_deferred" or artifact in {
        "change.yaml",
        "proposal.md",
        "tasks.md",
        "traceability.yaml",
    } or "doc" in artifact:
        return "documentation"
    return "unknown"


def allowed_approvers_for_category(category: str, review_map: dict[str, Any]) -> set[str]:
    allowed: set[str] = set()

    if category == "qa":
        allowed.add("qa_owner_group")
        qa_owner = scalar_value(review_map.get("qa_owner_group"))
        if qa_owner:
            allowed.add(qa_owner)
        return allowed

    if category == "automation":
        allowed.add("at_owner_group")
        allowed.update(list_value(review_map.get("at_owner_group")))
        allowed.update(list_value(review_map.get("at_owner_groups")))
        return allowed

    if category == "design":
        allowed.add("tech_lead")
        tech_lead = scalar_value(review_map.get("tech_lead"))
        if tech_lead:
            allowed.add(tech_lead)
        return allowed

    if category == "documentation":
        allowed.update({"analyst_owner_group", "product_owner"})
        analyst_owner = scalar_value(review_map.get("analyst_owner_group"))
        product_owner = scalar_value(review_map.get("product_owner"))
        if analyst_owner:
            allowed.add(analyst_owner)
        if product_owner:
            allowed.add(product_owner)
        return allowed

    return allowed


def index_waivers_by_artifact(waivers: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    indexed: dict[str, list[dict[str, Any]]] = {}
    for waiver in waivers:
        artifact = scalar_value(waiver.get("artifact"))
        if not artifact:
            continue
        indexed.setdefault(artifact, []).append(waiver)
    return indexed


def has_artifact_waiver(
    waivers_by_artifact: dict[str, list[dict[str, Any]]],
    artifact: str,
) -> bool:
    return artifact in waivers_by_artifact


def has_valid_no_spec_change_exception(
    change_type: str | None,
    spec_change: str | None,
    spec_files: list[Path],
    waivers_by_artifact: dict[str, list[dict[str, Any]]],
) -> bool:
    if spec_change != "none":
        return False
    if spec_files:
        return False
    if change_type not in ALLOWED_NO_SPEC_CHANGE_TYPES:
        return False
    return any(
        scalar_value(waiver.get("type")) == "no_spec_change"
        for waiver in waivers_by_artifact.get("specs", [])
    )


def validate_mode_contracts(
    package_path: Path,
    metadata: dict[str, Any],
    mode: str | None,
    change_type: str | None,
) -> list[str]:
    errors: list[str] = []

    if mode != "thin":
        return errors

    quality = metadata.get("quality")
    systems = metadata.get("systems")
    quality_map = quality if isinstance(quality, dict) else {}
    systems_map = systems if isinstance(systems, dict) else {}

    reasons: list[str] = []
    if change_type in FULL_MODE_TYPES:
        reasons.append(f"type '{change_type}' requires a full package")
    if scalar_value(quality_map.get("behavior_scope")) == "broad":
        reasons.append("quality.behavior_scope 'broad' requires a full package")
    if scalar_value(quality_map.get("public_api")) == "impacted":
        reasons.append("quality.public_api 'impacted' requires a full package")
    if scalar_value(quality_map.get("mobile_at")) == "impacted":
        reasons.append("quality.mobile_at 'impacted' requires a full package")
    if scalar_value(quality_map.get("data_risk")) == "impacted":
        reasons.append("quality.data_risk 'impacted' requires a full package")
    if scalar_value(quality_map.get("security_review")) == "required":
        reasons.append("quality.security_review 'required' requires a full package")
    if scalar_value(quality_map.get("rollback_cost")) == "high":
        reasons.append("quality.rollback_cost 'high' requires a full package")

    code_repos = list_value(systems_map.get("code_repos"))
    at_repos = list_value(systems_map.get("at_repos"))
    repo_count = len(code_repos) + len(at_repos)
    if repo_count > 1:
        reasons.append("cross-repo scope requires a full package")

    for reason in reasons:
        errors.append(f"{package_path}: {reason}")

    return errors


def find_placeholder_errors(package_path: Path) -> list[str]:
    errors: list[str] = []
    for file_path in iter_validation_files(package_path):
        text = file_path.read_text(encoding="utf-8")
        match = PLACEHOLDER_PATTERN.search(text)
        if match:
            errors.append(
                f"{file_path}: placeholder value '{match.group(0)}' must be replaced"
            )
    return errors


def iter_validation_files(package_path: Path) -> Iterable[Path]:
    for relative_path in BASE_REQUIRED_FILES + FULL_REQUIRED_FILES + OPTIONAL_VALIDATION_FILES:
        file_path = package_path / relative_path
        if file_path.is_file():
            yield file_path

    specs_dir = package_path / "specs"
    if specs_dir.is_dir():
        yield from sorted(specs_dir.glob("**/spec.md"))

    qa_test_cases = package_path / "qa" / "test-cases"
    if qa_test_cases.is_dir():
        yield from sorted(qa_test_cases.glob("**/*.md"))


def discover_change_roots_from_paths(
    project_root: str | Path,
    changed_paths: Iterable[str | Path],
) -> list[Path]:
    root = Path(project_root).resolve()
    roots: set[Path] = set()

    for changed_path in changed_paths:
        candidate = Path(changed_path)
        absolute = candidate if candidate.is_absolute() else root / candidate
        current = absolute if absolute.is_dir() else absolute.parent

        while True:
            if (current / "change.yaml").is_file():
                roots.add(current.resolve())
                break
            if current == root or current.parent == current:
                break
            current = current.parent

    return sorted(roots)


def git_root(cwd: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    return Path(result.stdout.strip())


def staged_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Change package directories to validate. Defaults to current directory.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow template placeholder values while still checking structure.",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        help="Discover SDD change packages from staged git paths.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    cwd = Path.cwd()

    if args.staged:
        root = git_root(cwd)
        packages = discover_change_roots_from_paths(root, staged_paths(root))
        if not packages:
            print("No staged SDD change packages found.")
            return 0
    else:
        packages = [Path(path) for path in (args.paths or [cwd])]

    all_errors: list[str] = []
    for package in packages:
        all_errors.extend(
            validate_change_package(package, allow_placeholders=args.allow_placeholders)
        )

    if all_errors:
        for error in all_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for package in packages:
        print(f"OK: {package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
