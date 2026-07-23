"""Acceptance tests for the read-only guided owner workflow."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from process.errors import OperationError
from process.guided_workflow import load_catalog
from scripts.guided_owner_workflow import main as guided_main
from scripts.validate_guided_owner_workflow import main as validate_main


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
GUIDE = ROOT / "docs" / "runbooks" / "GUIDED_OWNER_WORKFLOW.md"


def _payload(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


@pytest.mark.parametrize("classification", ["minor", "major"])
def test_new_requirement_route_is_read_only_and_names_classification_decision(
    classification: str, capsys,
) -> None:
    assert guided_main([
        "new-requirement", "--fact", f"classification={classification}", "--fact", "human_role=Analyst", "--json",
    ]) == 0

    payload = _payload(capsys)

    assert payload["status"] == "guided"
    assert payload["route_id"] == "new-requirement"
    assert payload["lifecycle_mutated"] is False
    assert payload["known_facts"] == {"classification": classification, "human_role": "Analyst"}
    assert payload["commands"] == [
        "create-change",
        "classify-change",
    ]
    assert payload["human_decision"]["id"] == "classification-confirmation"
    assert payload["human_decision"]["owner"] == "Tech Lead"


def test_existing_change_requires_known_lifecycle_state_and_never_guesses(capsys) -> None:
    assert guided_main([
        "existing-change", "--fact", "change_id=sample-minor-001", "--fact", "human_role=Analyst", "--json",
    ]) == 1
    payload = _payload(capsys)
    assert payload["status"] == "blocked"
    assert payload["blockers"] == [{
        "code": "missing-context",
        "required_facts": ["lifecycle_state"],
    }]


@pytest.mark.parametrize(
    ("situation", "facts", "expected_code"),
    [
        ("new-requirement", ["classification=unclassified", "human_role=Analyst"], "invalid-context"),
        (
            "existing-change",
            ["change_id=sample-minor-001", "lifecycle_state=delivered", "human_role=Analyst"],
            "invalid-context",
        ),
    ],
)
def test_declared_context_values_are_validated_before_routing(
    situation: str, facts: list[str], expected_code: str, capsys,
) -> None:
    args = [situation, *[item for fact in facts for item in ("--fact", fact)], "--json"]
    assert guided_main(args) == 1
    payload = _payload(capsys)
    assert payload["status"] == "blocked"
    assert payload["blockers"][0]["code"] == expected_code


def test_unavailable_surface_returns_catalog_fallback_without_weakening_gate(capsys) -> None:
    assert guided_main([
        "urgent-incident", "--fact", "incident_ref=evidence/INC-001.md", "--fact", "human_role=Tech Lead",
        "--unavailable", "model-runtime", "--json",
    ]) == 0
    payload = _payload(capsys)

    assert payload["status"] == "guided"
    assert payload["unavailable"] == ["model-runtime"]
    assert payload["fallbacks"] == [{
        "surface": "model-runtime",
        "command": "manual-fallback --unavailable model-runtime",
    }]
    assert payload["human_decision"]["id"] == "hotfix-eligibility-confirmation"
    assert payload["route_id"] == "urgent-incident"


def test_unknown_situation_is_a_structured_safe_block(capsys) -> None:
    assert guided_main(["invent-a-route", "--json"]) == 1
    payload = _payload(capsys)
    assert payload["status"] == "blocked"
    assert payload["blockers"][0]["code"] == "situation-unknown"


def test_catalog_rejects_undocumented_commands_and_ai_owned_decisions(tmp_path: Path) -> None:
    catalog = tmp_path / "catalog.yaml"
    catalog.write_text(
        "schema_version: '1.0'\n"
        "routes:\n"
        "  - id: unsafe\n"
        "    situation: unsafe\n"
        "    required_facts: []\n"
        "    commands: [not-published-operation]\n"
        "    evidence: []\n"
        "    human_decision: {id: release, owner: AI}\n"
        "    fallbacks: []\n",
        encoding="utf-8",
    )

    with pytest.raises(OperationError, match="catalog-invalid"):
        load_catalog(catalog)


def test_onboarding_guide_is_synchronized_with_catalog(capsys) -> None:
    assert validate_main(["--json"]) == 0
    payload = _payload(capsys)
    assert payload == {
        "operation": "validate-guided-owner-workflow",
        "status": "valid",
        "guide": "docs/runbooks/GUIDED_OWNER_WORKFLOW.md",
        "catalog": "process/catalogs/guided-owner-workflow.yaml",
    }
    assert GUIDE.is_file()


def test_guide_validator_is_cwd_independent(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_guided_owner_workflow.py"), "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert json.loads(completed.stdout)["status"] == "valid"
    assert completed.stderr == ""


def test_legacy_catalog_owner_label_is_migratable_but_not_an_interactive_role(tmp_path: Path) -> None:
    catalog = tmp_path / "legacy-catalog.yaml"
    catalog.write_text(
        (PROCESS / "catalogs" / "guided-owner-workflow.yaml").read_text(encoding="utf-8").replace(
            "owner: Analyst", "owner: Change Owner"
        ),
        encoding="utf-8",
    )

    loaded = load_catalog(catalog)

    assert loaded["routes"][1]["human_decision"]["owner"] == "Change Owner"
