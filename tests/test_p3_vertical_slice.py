"""Focused P3 role, readiness, analytics, and preview acceptance tests."""

from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from process.analytics_artifacts import preview_analytics, validate_analytics_package
from process.guided_process_integrity import build_response_summary, validate_guided_change_package
from process.guided_workflow import guide

ROOT = Path(__file__).resolve().parents[1]


def _write(root: Path, name: str, content: str) -> None:
    target = root / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def _ready_package(root: Path) -> None:
    _write(root, "proposal.md", "# Proposal\n")
    _write(root, "design.md", "# Design\n")
    _write(
        root,
        "specs/example/spec.md",
        "## ADDED Requirements\n\n### Requirement: REQ-EXAMPLE-001\nSystem SHALL work.\n\n#### Scenario: SCEN-EXAMPLE-001-01\n- **WHEN** input is present\n- **THEN** output is present\n",
    )
    _write(root, "tasks.md", "# Tasks\n\n- [ ] Implement the approved work.\n")
    _write(root, "traceability.yaml", "requirements:\n  - requirement: REQ-EXAMPLE-001\n    scenarios: [SCEN-EXAMPLE-001-01]\n")
    _write(root, "status.md", "# Status\n\nDoR: passed\n")


def test_unknown_role_blocks_role_sensitive_guidance() -> None:
    payload = guide("existing-change", {"change_id": "sample", "lifecycle_state": "spec_review"}, set())

    assert payload["status"] == "blocked"
    assert payload["blockers"][0]["code"] == "unknown-role"


def test_analyst_never_receives_implementation_cta() -> None:
    payload = guide(
        "existing-change",
        {"change_id": "sample", "lifecycle_state": "approved", "human_role": "Analyst"},
        set(),
    )

    assert payload["status"] == "guided"
    assert payload["cta"] != "begin-approved-implementation"


def test_ui_yes_is_not_trusted_acceptance_and_dor_cannot_be_skipped(tmp_path: Path) -> None:
    _ready_package(tmp_path)
    _write(tmp_path, "status.md", "# Status\n\nDoR is pending\n")
    digest = hashlib.sha256((tmp_path / "specs/example/spec.md").read_bytes()).hexdigest()
    _write(
        tmp_path,
        "decisions/spec-acceptance.yaml",
        yaml.safe_dump(
            {
                "schema_version": "2.0",
                "change_id": "sample",
                "spec_revision": {"path": "specs/example/spec.md", "sha256": digest},
                "shown_summary": {"path": "status.md", "spec_sha256": digest},
                "event": {"actor_type": "human", "human_role": "Analyst", "timestamp": "2026-07-21T10:00:00Z", "reference": "chat://trusted/1", "literal_message": "Да"},
            },
            allow_unicode=True,
            sort_keys=False,
        ),
    )

    report = validate_guided_change_package(tmp_path)

    assert report["status"] == "invalid"
    assert {item["code"] for item in report["diagnostics"]} >= {
        "guided-process.acceptance-message-invalid",
        "guided-process.dor-not-passed",
    }


def test_trusted_revision_bound_acceptance_exposes_single_safe_cta(tmp_path: Path) -> None:
    _ready_package(tmp_path)
    digest = hashlib.sha256((tmp_path / "specs/example/spec.md").read_bytes()).hexdigest()
    _write(
        tmp_path,
        "decisions/spec-acceptance.yaml",
        yaml.safe_dump(
            {
                "schema_version": "2.0",
                "change_id": "sample",
                "spec_revision": {"path": "specs/example/spec.md", "sha256": digest},
                "shown_summary": {"path": "status.md", "spec_sha256": digest},
                "event": {"actor_type": "human", "human_role": "Analyst", "timestamp": "2026-07-21T10:00:00Z", "reference": "chat://trusted/2", "literal_message": "Спека принята, реализуй"},
            },
            allow_unicode=True,
            sort_keys=False,
        ),
    )

    report = validate_guided_change_package(tmp_path)
    summary = build_response_summary(tmp_path, report, human_role="Analyst")

    assert report["status"] == "valid"
    assert summary["spec_revision"]["sha256"] == digest
    assert summary["next_permitted_action"] == "prepare-role-pr-approval"
    assert build_response_summary(tmp_path, report, human_role="Tech Lead")["next_permitted_action"] == "monitor-process-status"


def test_typed_analytics_fixture_validates_and_previews_without_external_actions(tmp_path: Path) -> None:
    _write(tmp_path, "analytics-manifest.yaml", "schema_version: '1.0'\ncapability_id: SAMPLE\nartifacts: [status-model.yaml, channel-support.yaml, data-model.yaml, platform-services.yaml, journey.yaml, screens.yaml, integrations.yaml]\n")
    _write(tmp_path, "status-model.yaml", "schema_version: '1.0'\nstatuses: [{id: DRAFT, transitions: [PUBLISHED]}]\n")
    _write(tmp_path, "channel-support.yaml", "schema_version: '1.0'\nchannels: [{id: WEB, supported: true}]\n")
    _write(tmp_path, "data-model.yaml", "schema_version: '1.0'\nentities: [{id: APPLICATION, attributes: [{id: amount, classification: internal}]}]\n")
    _write(tmp_path, "platform-services.yaml", "schema_version: '1.0'\nservices: [{id: LIMITS, kind: internal, operations: [check-limit]}]\n")
    _write(tmp_path, "journey.yaml", "schema_version: '1.0'\njourney_id: JOURNEY-SAMPLE\nsteps: [{id: STEP-1, requirements: [REQ-SAMPLE-001], scenarios: [SCEN-SAMPLE-001-01]}]\n")
    _write(tmp_path, "screens.yaml", "schema_version: '1.0'\nscreens: [{id: SCR-SAMPLE-001, asset: assets/screens/SCR-SAMPLE-001.png, source: synthetic, requirements: [REQ-SAMPLE-001], scenarios: [SCEN-SAMPLE-001-01]}]\n")
    _write(tmp_path, "integrations.yaml", "schema_version: '1.0'\nintegrations: [{id: JIRA, system: Jira, mode: passive, stable_reference: JIRA:PROJECT, manual_evidence: evidence/manual.md}]\n")

    report = validate_analytics_package(tmp_path)
    preview = preview_analytics(tmp_path, report)

    assert report["status"] == "valid"
    assert preview["external_state_mutated"] is False
    assert preview["integration_actions"] == []
    assert preview["screens"][0]["id"] == "SCR-SAMPLE-001"

def test_gigacode_start_prompt_uses_only_project_interactive_roles() -> None:
    prompt = (ROOT / "process" / "gigacode" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Analyst, Tech Lead, Developer, QA" in prompt
    assert "Change Owner" not in prompt
    assert "Release Owner" not in prompt

def test_catalog_never_grants_implementation_entry_to_tech_lead() -> None:
    payload = guide(
        "existing-change",
        {"change_id": "sample", "lifecycle_state": "approved", "human_role": "Tech Lead"},
        set(),
    )

    assert payload["status"] == "guided"
    assert payload["cta"] == "monitor-process-status"


SCENARIO_COVERAGE = {
    "test_unknown_role_blocks_role_sensitive_guidance": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Fail-closed role-aware guidance", "scenario": "Unknown role is blocked"},
    ],
    "test_analyst_never_receives_implementation_cta": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Fail-closed role-aware guidance", "scenario": "Analyst cannot receive implementation CTA"},
    ],
    "test_ui_yes_is_not_trusted_acceptance_and_dor_cannot_be_skipped": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Trusted revision-bound human acceptance", "scenario": "UI confirmation is rejected"},
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Readiness preserves DoR", "scenario": "Incomplete package remains blocked"},
    ],
    "test_typed_analytics_fixture_validates_and_previews_without_external_actions": [
        {"source_kind": "delta", "capability": "typed-analytics-artifact-framework", "requirement": "Typed analytics package", "scenario": "Complete typed package validates"},
        {"source_kind": "delta", "capability": "typed-analytics-artifact-framework", "requirement": "Stable analytics traceability", "scenario": "Screen remains traceable"},
        {"source_kind": "delta", "capability": "typed-analytics-artifact-framework", "requirement": "Passive integration boundary", "scenario": "Preview never invokes integration"},
        {"source_kind": "delta", "capability": "typed-analytics-artifact-framework", "requirement": "Local P3 preview boundary", "scenario": "Synthetic analytics walkthrough"},
    ],
}
