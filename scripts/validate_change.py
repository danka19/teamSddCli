"""Validate deterministic SDD change package artifacts.

The validator intentionally supports a small YAML subset used by this
repository's templates. Keeping the gate dependency-free makes the first
process layer easier to transfer into constrained corporate environments.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = (
    "change.yaml",
    "proposal.md",
    "design.md",
    "tasks.md",
    "qa/test-plan.md",
    "qa/automation-plan.md",
    "traceability.yaml",
)

REQUIRED_CHANGE_FIELDS = (
    "id",
    "title",
    "mode",
    "type",
    "status",
    "capability",
)

REQUIRED_CHANGE_SECTIONS = ("systems", "quality")

ALLOWED_MODES = {"thin", "full"}
ALLOWED_TYPES = {
    "new_feature",
    "behavior_change",
    "bugfix",
    "refactor",
    "removal",
    "config_ops",
}
ALLOWED_STATUSES = {
    "draft",
    "spec_review",
    "approved",
    "tasks_created",
    "in_dev",
    "ready_for_qa",
    "implemented",
    "archived",
}

CHANGE_ID_PATTERN = re.compile(
    r"^[A-Z][A-Z0-9]+-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
PLACEHOLDER_PATTERN = re.compile(
    r"(<[^>\n]+>|TODO|TBD|REPLACE|CHANGE[-_]ID|AUTH-YYYY|YOUR[-_ ])",
    re.IGNORECASE,
)


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

    for relative_path in REQUIRED_FILES:
        file_path = package_path / relative_path
        if not file_path.is_file():
            errors.append(f"{package_path}: missing required artifact {relative_path}")
            continue
        if not file_path.read_text(encoding="utf-8").strip():
            errors.append(f"{package_path}: artifact {relative_path} must not be empty")

    spec_files = sorted((package_path / "specs").glob("**/spec.md"))
    if not spec_files:
        errors.append(f"{package_path}: missing at least one specs/**/spec.md file")
    else:
        for spec_file in spec_files:
            if not spec_file.read_text(encoding="utf-8").strip():
                errors.append(f"{package_path}: artifact {spec_file.relative_to(package_path)} must not be empty")

    if (package_path / "change.yaml").is_file():
        errors.extend(validate_change_metadata(package_path / "change.yaml", allow_placeholders))

    requirement_scenarios, spec_errors = extract_requirement_scenarios(spec_files)
    errors.extend(f"{package_path}: {error}" for error in spec_errors)
    if spec_files and not requirement_scenarios:
        errors.append(f"{package_path}: specs must contain at least one requirement scenario")

    if (package_path / "traceability.yaml").is_file():
        traceability_links = extract_traceability_links(package_path / "traceability.yaml")
        for requirement, scenario in requirement_scenarios:
            if (requirement, scenario) not in traceability_links:
                errors.append(
                    f"{package_path}: traceability.yaml missing link for "
                    f"requirement '{requirement}' scenario '{scenario}'"
                )

    if not allow_placeholders:
        errors.extend(find_placeholder_errors(package_path))

    return errors


def validate_change_metadata(path: Path, allow_placeholders: bool) -> list[str]:
    metadata = read_top_level_yaml(path)
    errors: list[str] = []

    for field in REQUIRED_CHANGE_FIELDS:
        value = metadata.get(field)
        if value is None or value == "":
            errors.append(f"{path}: missing required field '{field}'")

    for section in REQUIRED_CHANGE_SECTIONS:
        if section not in metadata:
            errors.append(f"{path}: missing required section '{section}'")

    change_id = metadata.get("id")
    if change_id and not allow_placeholders and not CHANGE_ID_PATTERN.match(change_id):
        errors.append(f"{path}: id '{change_id}' must match PROJECT-YYYY-NNN-short-name")

    mode = metadata.get("mode")
    if mode and not allow_placeholders and mode not in ALLOWED_MODES:
        errors.append(f"{path}: mode '{mode}' must be one of {sorted(ALLOWED_MODES)}")

    change_type = metadata.get("type")
    if change_type and not allow_placeholders and change_type not in ALLOWED_TYPES:
        errors.append(f"{path}: type '{change_type}' must be one of {sorted(ALLOWED_TYPES)}")

    status = metadata.get("status")
    if status and not allow_placeholders and status not in ALLOWED_STATUSES:
        errors.append(f"{path}: status '{status}' must be one of {sorted(ALLOWED_STATUSES)}")

    return errors


def read_top_level_yaml(path: Path) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith((" ", "\t")):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        values[key.strip()] = normalize_scalar(value)
    return values


def normalize_scalar(value: str) -> str | None:
    value = value.strip()
    if value == "":
        return None
    if value in {"[]", "{}"}:
        return value
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


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


def extract_traceability_links(path: Path) -> set[tuple[str, str]]:
    links: set[tuple[str, str]] = set()
    current: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            if current and current.get("requirement") and current.get("scenario"):
                links.add((current["requirement"], current["scenario"]))
            current = {}
            stripped = stripped[2:].strip()

        if current is None:
            continue

        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        if key in {"requirement", "scenario"}:
            scalar = normalize_scalar(value)
            if scalar:
                current[key] = scalar

    if current and current.get("requirement") and current.get("scenario"):
        links.add((current["requirement"], current["scenario"]))

    return links


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
    for relative_path in REQUIRED_FILES:
        file_path = package_path / relative_path
        if file_path.is_file():
            yield file_path
    specs_dir = package_path / "specs"
    if specs_dir.is_dir():
        yield from sorted(specs_dir.glob("**/spec.md"))


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
