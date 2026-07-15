"""Synthetic, AI-disabled Phase 2.6 certification fixture checks."""

from __future__ import annotations

from pathlib import Path

import yaml

from process.validators.tech_lead import validate_tech_lead_input


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
FIXTURES = ROOT / "tests" / "fixtures" / "tech-lead"


def _yaml(path: Path):
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_role_instruction_is_bounded_source_linked_and_ai_advisory() -> None:
    instruction = (PROCESS / "roles" / "tech-lead.md").read_text(encoding="utf-8")

    for required in (
        "minor | major | hotfix", "canonical", "AI-disabled", "decision-only",
        "must not approve", "must not resume", "QA", "product", "security",
        "release", "merge", "archive", "tracker",
    ):
        assert required.lower() in instruction.lower()


def test_synthetic_certification_manifest_declares_no_model_certification() -> None:
    manifest = _yaml(FIXTURES / "certification-manifest.yaml")

    assert manifest["mode"] == "ai-disabled"
    assert manifest["actual_model_certification_performed"] is False
    assert manifest["fixtures"] == [
        "valid-review.yaml", "stop-resume.yaml", "ai-resume-invalid.yaml",
    ]
    assert manifest["forbidden_mutations"] == ["control-state", "lifecycle"]


def test_synthetic_review_and_control_fixtures_satisfy_pinned_schemas() -> None:
    for filename in ("valid-review.yaml", "stop-resume.yaml"):
        assert validate_tech_lead_input(_yaml(FIXTURES / filename), PROCESS) == []

    invalid = validate_tech_lead_input(
        _yaml(FIXTURES / "ai-resume-invalid.yaml"), PROCESS
    )
    assert invalid[0]["code"] == "tech-lead.input-schema-invalid"


SCENARIO_COVERAGE = {'test_role_instruction_is_bounded_source_linked_and_ai_advisory': [{'capability': 'tech-lead-workflow',
                                                                     'requirement': 'AI advisory boundary for tech '
                                                                                    'lead automation',
                                                                     'scenario': 'AI may draft analysis',
                                                                     'source_kind': 'delta'},
                                                                    {'capability': 'tech-lead-workflow',
                                                                     'requirement': 'AI advisory boundary for tech '
                                                                                    'lead automation',
                                                                     'scenario': 'AI may not approve',
                                                                     'source_kind': 'delta'}]}
