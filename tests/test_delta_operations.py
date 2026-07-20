from pathlib import Path
import sys
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from process.validators.legacy_change import validate_delta_operations


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).strip() + "\n", encoding="utf-8")
    return path


def accepted_spec(root: Path) -> Path:
    return write(
        root / "sample-capability" / "spec.md",
        """
        # sample-capability Specification

        ## Requirements

        ### Requirement: Existing behavior
        The system SHALL preserve existing behavior.

        #### Scenario: Existing path
        - **WHEN** the existing path is used
        - **THEN** the behavior remains available
        """,
    )


def delta_spec(root: Path, content: str) -> Path:
    return write(root / "sample-capability" / "spec.md", content)


def test_added_delta_must_introduce_new_behavior(tmp_path: Path) -> None:
    accepted = tmp_path / "accepted"
    accepted_spec(accepted)
    delta = delta_spec(
        tmp_path / "delta",
        """
        ## ADDED Requirements

        ### Requirement: Existing behavior
        The system SHALL silently replace the existing behavior.

        #### Scenario: Replacement path
        - **WHEN** the delta is applied
        - **THEN** existing behavior changes
        """,
    )

    errors = validate_delta_operations([delta], accepted)

    assert any("delta.added-existing" in error for error in errors)


def test_removed_delta_requires_reason_and_migration(tmp_path: Path) -> None:
    accepted = tmp_path / "accepted"
    accepted_spec(accepted)
    delta = delta_spec(
        tmp_path / "delta",
        """
        ## REMOVED Requirements

        ### Requirement: Existing behavior
        **Reason**: The behavior is obsolete.
        """,
    )

    errors = validate_delta_operations([delta], accepted)

    assert any("delta.removed-migration-missing" in error for error in errors)


def test_rename_cannot_hide_content_change(tmp_path: Path) -> None:
    accepted = tmp_path / "accepted"
    accepted_spec(accepted)
    delta = delta_spec(
        tmp_path / "delta",
        """
        ## RENAMED Requirements

        - FROM: `Existing behavior`
        - TO: `Renamed behavior`
        The renamed behavior SHALL also change its outcome.
        """,
    )

    errors = validate_delta_operations([delta], accepted)

    assert any("delta.renamed-content" in error for error in errors)


def test_valid_delta_operations_pass_semantic_validation(tmp_path: Path) -> None:
    accepted = tmp_path / "accepted"
    accepted_spec(accepted)
    delta_root = tmp_path / "deltas"
    deltas = [
        delta_spec(
            delta_root / "add",
            """
            ## ADDED Requirements

            ### Requirement: New behavior
            The system SHALL add a new behavior.

            #### Scenario: New path
            - **WHEN** the new path is used
            - **THEN** the new behavior is available
            """,
        ),
        delta_spec(
            delta_root / "remove",
            """
            ## REMOVED Requirements

            ### Requirement: Existing behavior
            **Reason**: The behavior is obsolete.
            **Migration**: Use New behavior instead.
            """,
        ),
        delta_spec(
            delta_root / "rename",
            """
            ## RENAMED Requirements

            - FROM: `Existing behavior`
            - TO: `Renamed behavior`
            """,
        ),
    ]

    assert validate_delta_operations(deltas, accepted) == []


def test_delta_validation_fails_closed_without_baseline_and_on_ambiguous_shape(tmp_path: Path) -> None:
    delta = delta_spec(
        tmp_path / "delta",
        """
        ## ADDED Requirements
        """,
    )
    errors = validate_delta_operations([delta], tmp_path / "missing-accepted")
    assert errors == ["delta.accepted-baseline-missing: accepted specs root is required"]

    accepted = tmp_path / "accepted"
    accepted_spec(accepted)
    assert any(
        "delta.operation-empty" in error
        for error in validate_delta_operations([delta], accepted)
    )

    duplicate = delta_spec(
        tmp_path / "duplicate",
        """
        ## RENAMED Requirements

        - FROM: `Existing behavior`
        - TO: `Renamed behavior`
        - FROM: `Existing behavior`
        - TO: `Another behavior`
        """,
    )
    assert any(
        "delta.renamed-duplicate" in error
        for error in validate_delta_operations([duplicate], accepted)
    )

    header_only = delta_spec(
        tmp_path / "header-only",
        """
        ## ADDED Requirements

        ### Requirement: Header only
        #### Scenario: Heading only
        """,
    )
    header_errors = validate_delta_operations([header_only], accepted)
    assert any("delta.added-content-missing" in error for error in header_errors)
    assert any("delta.added-scenario-incomplete" in error for error in header_errors)

    non_adjacent = delta_spec(
        tmp_path / "non-adjacent",
        """
        ## RENAMED Requirements

        - FROM: `Existing behavior`
        - FROM: `Another behavior`
        - TO: `Renamed behavior`
        - TO: `Another renamed behavior`
        """,
    )
    assert any(
        "delta.renamed-shape" in error
        for error in validate_delta_operations([non_adjacent], accepted)
    )


SCENARIO_COVERAGE = {
    "test_added_delta_must_introduce_new_behavior": [
        {
            "source_kind": "delta",
            "capability": "change-artifact-contracts",
            "requirement": "Delta Spec operation vocabulary",
            "scenario": "Added delta introduces new behavior",
        }
    ],
    "test_removed_delta_requires_reason_and_migration": [
        {
            "source_kind": "delta",
            "capability": "change-artifact-contracts",
            "requirement": "Delta Spec operation vocabulary",
            "scenario": "Removed delta includes reason and migration",
        }
    ],
    "test_rename_cannot_hide_content_change": [
        {
            "source_kind": "delta",
            "capability": "change-artifact-contracts",
            "requirement": "Delta Spec operation vocabulary",
            "scenario": "Rename does not hide content change",
        }
    ],
}
