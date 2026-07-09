from pathlib import Path
import sys
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts import validate_change


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def build_change_yaml(
    *,
    change_type: str,
    mode: str,
    status: str = "draft",
    spec_change: str = "required",
    quality_overrides: dict[str, str] | None = None,
) -> str:
    quality = {
        "scenarios": "required",
        "manual_cases": "impacted",
        "api_at": "not_impacted",
        "mobile_at": "not_impacted",
        "security_review": "not_required",
    }
    if quality_overrides:
        quality.update(quality_overrides)

    quality_lines = "\n".join(
        f"  {key}: {value}" for key, value in quality.items()
    )

    return "\n".join(
        [
            "id: AUTH-2026-071-add-remember-me",
            "title: Add Remember Me option",
            f"mode: {mode}",
            f"type: {change_type}",
            f"status: {status}",
            "capability: auth-session",
            f"spec_change: {spec_change}",
            "systems:",
            "  code_repos:",
            "    - backend-auth",
            "  at_repos: []",
            "review:",
            "  analyst_owner_group: auth-ba",
            "  dev_owner_groups:",
            "    - auth-dev",
            "  qa_owner_group: qa-auth",
            "  at_owner_groups:",
            "    - at-auth",
            "quality:",
            *quality_lines.splitlines(),
            "publication:",
            "  confluence_space: generated",
            "  page_id: null",
            "  mode: generated",
        ]
    )


def build_valid_package(
    root: Path,
    *,
    change_type: str = "behavior_change",
    mode: str = "thin",
    status: str = "draft",
    spec_change: str = "required",
    include_specs: bool = True,
    include_design: bool | None = None,
    include_test_plan: bool | None = None,
    include_test_case: bool | None = None,
    include_automation_plan: bool | None = None,
    quality_overrides: dict[str, str] | None = None,
    traceability_content: str | None = None,
    waivers_content: str | None = None,
) -> Path:
    package = root / "AUTH-2026-071-add-remember-me"
    write_file(
        package / "change.yaml",
        build_change_yaml(
            change_type=change_type,
            mode=mode,
            status=status,
            spec_change=spec_change,
            quality_overrides=quality_overrides,
        ),
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
        package / "tasks.md",
        """
        # Tasks

        - [ ] TASK-AUTH-001 Draft and review the spec delta.
        - [ ] TASK-AUTH-002 Implement Remember Me session storage.
        - [ ] TASK-AUTH-003 Verify the requirement scenario and update traceability.
        """,
    )

    if include_specs:
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

    include_design = mode == "full" if include_design is None else include_design
    include_test_plan = mode == "full" if include_test_plan is None else include_test_plan
    include_test_case = mode == "full" if include_test_case is None else include_test_case
    include_automation_plan = (
        mode == "full" if include_automation_plan is None else include_automation_plan
    )

    if include_design:
        write_file(
            package / "design.md",
            """
            # Design

            ## Context

            Remember Me changes the session strategy and token lifetime.
            """,
        )

    if include_test_plan:
        write_file(
            package / "qa/test-plan.md",
            """
            # Test Plan

            ## Strategy

            Verify session duration and revocation behavior.
            """,
        )

    if include_test_case:
        write_file(
            package / "qa/test-cases/example-scenario.md",
            """
            # Example Scenario

            Requirement: Remember Me session

            Scenario: Login with Remember Me enabled

            - WHEN the user logs in with Remember Me enabled
            - THEN the system creates an extended session
            """,
        )

    if include_automation_plan:
        write_file(
            package / "qa/automation-plan.md",
            """
            # Automation Plan

            ## Target

            backend-api

            ## Planned Coverage

            - AT-AUTH-001 API session coverage
            """,
        )

    write_file(
        package / "traceability.yaml",
        traceability_content
        or """
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

    if waivers_content is not None:
        write_file(package / "waivers.yaml", waivers_content)

    return package


def test_valid_thin_change_package_passes_validation(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path, mode="thin", change_type="behavior_change")

    errors = validate_change.validate_change_package(package)

    assert errors == []


def test_valid_full_change_package_with_waiver_passes_validation(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        mode="full",
        change_type="new_feature",
        include_automation_plan=False,
        traceability_content="""
        requirements:
          - id: REQ-AUTH-001
            requirement: Remember Me session
            scenario: Login with Remember Me enabled
            tasks:
              - TASK-AUTH-001
            tests:
              - TC-AUTH-001
            automated_tests:
              - pending
            waivers:
              - WVR-AUTH-001
        """,
        waivers_content="""
        waivers:
          - id: WVR-AUTH-001
            type: automation_deferred
            artifact: qa/automation-plan.md
            requirements:
              - Remember Me session
            scenarios:
              - Login with Remember Me enabled
            reason: Automation is deferred until the API stabilizes.
            evidence:
              - docs/evidence/manual-auth-check.md
            approver: at_owner_group
            date: 2026-07-09
            residual_risk: true
            follow_up: Add AT coverage before archive approval.
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert errors == []


def test_missing_full_package_artifacts_are_reported_without_waiver(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        mode="full",
        change_type="new_feature",
        include_test_plan=False,
        include_test_case=False,
        include_automation_plan=False,
    )

    errors = validate_change.validate_change_package(package)

    assert any("qa/test-plan.md" in error for error in errors)
    assert any("qa/test-cases" in error for error in errors)
    assert any("qa/automation-plan.md" in error for error in errors)


def test_missing_requirement_scenario_traceability_is_reported(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        traceability_content="""
        requirements:
          - id: REQ-AUTH-001
            requirement: Remember Me session
            scenario: Wrong scenario
            tasks:
              - TASK-AUTH-001
            tests:
              - TC-AUTH-001
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert any(
        "Remember Me session" in error
        and "Login with Remember Me enabled" in error
        for error in errors
    )


def test_historical_status_is_rejected(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path, status="implemented")

    errors = validate_change.validate_change_package(package)

    assert any("status 'implemented'" in error for error in errors)


def test_unsupported_mode_is_rejected(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path, mode="expedited")

    errors = validate_change.validate_change_package(package)

    assert any("mode 'expedited'" in error for error in errors)


def test_placeholder_values_are_rejected_in_production_mode(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path)
    write_file(
        package / "proposal.md",
        """
        # Proposal

        ## Problem

        TODO replace this placeholder before review.
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert any("placeholder value" in error for error in errors)


def test_invalid_waiver_shape_is_reported(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        mode="full",
        change_type="new_feature",
        include_automation_plan=False,
        traceability_content="""
        requirements:
          - id: REQ-AUTH-001
            requirement: Remember Me session
            scenario: Login with Remember Me enabled
            tasks:
              - TASK-AUTH-001
            tests:
              - TC-AUTH-001
            automated_tests:
              - pending
            waivers:
              - WVR-AUTH-001
        """,
        waivers_content="""
        waivers:
          - id: WVR-AUTH-001
            type: automation_deferred
            artifact: qa/automation-plan.md
            requirements:
              - Remember Me session
            scenarios: []
            reason: Automation is deferred until the API stabilizes.
            evidence:
              - docs/evidence/manual-auth-check.md
            approver: backend-team
            date: 2026-07-09
            residual_risk: true
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert any("waiver" in error and "scenarios" in error for error in errors)
    assert any("waiver" in error and "approver" in error for error in errors)
    assert any("waiver" in error and ("follow_up" in error or "expiry" in error) for error in errors)


def test_behavior_change_rejects_no_spec_change_rationale(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        change_type="behavior_change",
        include_specs=False,
        spec_change="none",
        waivers_content="""
        waivers:
          - id: WVR-AUTH-002
            type: no_spec_change
            artifact: specs
            requirements:
              - Remember Me session
            scenarios:
              - Login with Remember Me enabled
            reason: The author tried to skip the Delta Spec for a behavior change.
            evidence:
              - docs/evidence/existing-tests.md
            approver: analyst_owner_group
            date: 2026-07-09
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert any("no-spec-change" in error or "spec delta" in error for error in errors)


def test_refactor_can_use_no_spec_change_rationale(tmp_path: Path) -> None:
    package = build_valid_package(
        tmp_path,
        change_type="refactor",
        include_specs=False,
        spec_change="none",
        traceability_content="""
        requirements:
          - id: REQ-AUTH-001
            requirement: Existing session behavior remains unchanged
            scenario: Existing login session still works
            tasks:
              - TASK-AUTH-001
            tests:
              - TC-AUTH-001
        """,
        waivers_content="""
        waivers:
          - id: WVR-AUTH-003
            type: no_spec_change
            artifact: specs
            requirements:
              - Existing session behavior remains unchanged
            scenarios:
              - Existing login session still works
            reason: Internal refactor with no behavior change.
            evidence:
              - docs/evidence/existing-tests.md
            approver: analyst_owner_group
            date: 2026-07-09
        """,
    )

    errors = validate_change.validate_change_package(package)

    assert errors == []


def test_thin_package_rejects_full_only_type_combination(tmp_path: Path) -> None:
    package = build_valid_package(tmp_path, mode="thin", change_type="new_feature")

    errors = validate_change.validate_change_package(package)

    assert any("new_feature" in error and "full" in error for error in errors)


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
