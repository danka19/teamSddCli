from pathlib import Path
import sys
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts import validate_change


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def build_valid_package(root: Path) -> Path:
    package = root / "AUTH-2026-071-add-remember-me"
    write_file(
        package / "change.yaml",
        """
        id: AUTH-2026-071-add-remember-me
        title: Add Remember Me option
        mode: thin
        type: new_feature
        status: draft
        capability: auth-session
        systems:
          code_repos:
            - backend-auth
        review:
          analyst_owner_group: auth-ba
        quality:
          scenarios: required
        """,
    )
    write_file(
        package / "proposal.md",
        """
        # Proposal

        ## Problem

        Users need persistent sessions on trusted devices.
        """,
    )
    write_file(
        package / "design.md",
        """
        # Design

        Store Remember Me sessions separately from short-lived sessions.
        """,
    )
    write_file(
        package / "tasks.md",
        """
        # Tasks

        - [ ] TASK-AUTH-001 Implement Remember Me session storage.
        """,
    )
    write_file(
        package / "specs/auth-session/spec.md",
        """
        ## ADDED Requirements

        ### Requirement: Remember Me session
        The system SHALL support an optional Remember Me mode during login.

        #### Scenario: Login with Remember Me enabled
        - **WHEN** the user logs in with Remember Me enabled
        - **THEN** the system creates an extended session
        """,
    )
    write_file(
        package / "qa/test-plan.md",
        """
        # Test Plan

        Verify session duration and revocation behavior.
        """,
    )
    write_file(
        package / "qa/automation-plan.md",
        """
        # Automation Plan

        API coverage is planned after the spec review.
        """,
    )
    write_file(
        package / "traceability.yaml",
        """
        requirements:
          - id: REQ-AUTH-001
            requirement: Remember Me session
            scenario: Login with Remember Me enabled
            tasks:
              - TASK-AUTH-001
            tests:
              - TC-AUTH-001
            automated_tests: []
        """,
    )
    return package


def test_valid_change_package_passes_validation(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path)

    errors = validate_change.validate_change_package(package)

    assert errors == []


def test_missing_required_artifacts_are_reported(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path)
    (package / "design.md").unlink()

    errors = validate_change.validate_change_package(package)

    assert any("design.md" in error for error in errors)


def test_missing_requirement_scenario_traceability_is_reported(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path)
    write_file(
        package / "traceability.yaml",
        """
        requirements:
          - id: REQ-AUTH-001
            requirement: Remember Me session
            scenario: Wrong scenario
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert any(
        "Remember Me session" in error
        and "Login with Remember Me enabled" in error
        for error in errors
    )


def test_staged_discovery_ignores_plain_project_openspec_changes(tmp_path: Path) -> None:
    project_root = tmp_path / "repo"
    write_file(
        project_root / "openspec/changes/add-change-template-validation/proposal.md",
        "## Why\n\nProject OpenSpec change without change.yaml.",
    )
    sdd_package = build_valid_package(project_root / "team-specs/openspec/changes")

    roots = validate_change.discover_change_roots_from_paths(
        project_root,
        [
            "openspec/changes/add-change-template-validation/proposal.md",
            "team-specs/openspec/changes/AUTH-2026-071-add-remember-me/proposal.md",
        ],
    )

    assert roots == [sdd_package]


def test_template_skeleton_validates_in_placeholder_mode() -> None:
    template = REPO_ROOT / "templates/change"

    errors = validate_change.validate_change_package(template, allow_placeholders=True)

    assert errors == []
