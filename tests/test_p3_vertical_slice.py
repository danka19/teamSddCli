"""Focused P3 role, readiness, analytics, and preview acceptance tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

import process.guided_workflow as guided_workflow
from process.analytics_artifacts import preview_analytics, validate_analytics_package
from process.guided_process_integrity import build_response_summary, validate_guided_change_package
from process.guided_workflow import confirm_decision_draft, create_decision_draft, guide

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


def _source_event(*, sequence: int = 10, message: str = "Принимаю спецификацию") -> dict[str, object]:
    return {
        "event_ref": "chat://trusted/source",
        "actor_type": "human",
        "sequence": sequence,
        "timestamp": "2026-07-23T10:00:00Z",
        "message": message,
    }


def _card_event(*, sequence: int = 11) -> dict[str, object]:
    return {
        "event_ref": "chat://trusted/card",
        "actor_type": "assistant",
        "sequence": sequence,
        "previous_event_ref": "chat://trusted/source",
        "timestamp": "2026-07-23T10:01:00Z",
    }


def _confirmation_event(*, card_code: str, sequence: int = 12, timestamp: str = "2026-07-23T10:02:00Z") -> dict[str, object]:
    return {
        "event_ref": "chat://trusted/confirmation",
        "actor_type": "human",
        "sequence": sequence,
        "previous_event_ref": "chat://trusted/card",
        "timestamp": timestamp,
        "message": f"Подтверждаю {card_code}",
    }


def _draft(digest: str = "a" * 64) -> dict[str, object]:
    return create_decision_draft(
        change_id="sample",
        decision_type="spec-acceptance",
        revision_digest=digest,
        natural_message="Принимаю спецификацию",
        consequence="Prepare review only.",
        source_event=_source_event(),
        card_event=_card_event(),
        expires_at="2026-07-23T11:00:00Z",
    )


def test_confirmation_requires_trusted_next_human_event_and_bound_card() -> None:
    draft = _draft()
    confirmation = _confirmation_event(card_code=str(draft["card_code"]))

    assert confirm_decision_draft(draft, confirmation) is not None
    assert confirm_decision_draft(draft, {**confirmation, "previous_event_ref": "chat://trusted/other"}) is None
    assert confirm_decision_draft(draft, {**confirmation, "actor_type": "assistant"}) is None
    assert confirm_decision_draft(draft, {**confirmation, "sequence": 13}) is None


def test_confirmation_recomputes_card_code_and_rejects_pre_issuance_or_mixed_times() -> None:
    draft = _draft()
    confirmation = _confirmation_event(card_code=str(draft["card_code"]))

    forged = {**draft, "consequence": "Forged authority."}
    assert confirm_decision_draft(forged, confirmation) is None
    assert confirm_decision_draft(draft, _confirmation_event(card_code=str(draft["card_code"]), timestamp="2026-07-23T10:00:30Z")) is None
    aware_draft = {**draft, "issued_at": "2026-07-23T10:01:00"}
    assert confirm_decision_draft(aware_draft, confirmation) is None


def test_summary_fails_closed_when_confirmation_revision_is_not_current(tmp_path: Path) -> None:
    _ready_package(tmp_path)
    digest = hashlib.sha256((tmp_path / "specs/example/spec.md").read_bytes()).hexdigest()
    report = {"status": "valid", "diagnostics": [], "spec_revision": {"path": "specs/example/spec.md", "sha256": digest}}
    draft = _draft(digest)
    event = confirm_decision_draft(draft, _confirmation_event(card_code=str(draft["card_code"])))

    assert build_response_summary(tmp_path, report, confirmation_event=event)["decision_confirmation"]["status"] == "confirmed"
    stale = {**event, "revision_digest": "b" * 64}
    assert build_response_summary(tmp_path, report, confirmation_event=stale)["decision_confirmation"]["status"] == "unconfirmed"
    forged_provenance = {**event, "confirmation_event_actor_type": "assistant"}
    assert build_response_summary(tmp_path, report, confirmation_event=forged_provenance)["decision_confirmation"]["status"] == "unconfirmed"


def test_confirmation_event_schema_rejects_yes_and_accepts_only_confirmation_forms() -> None:
    schema = json.loads((ROOT / "process/schemas/confirmation-event.schema.json").read_text(encoding="utf-8"))
    draft = _draft()
    event = confirm_decision_draft(draft, _confirmation_event(card_code=str(draft["card_code"])))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    assert list(validator.iter_errors(event)) == []
    assert list(validator.iter_errors({**event, "confirmation_message": "Да"}))
    short = {**event, "confirmation_message": " \nПодтверждаю\t \n"}
    assert list(validator.iter_errors(short)) == []


def test_generated_decision_draft_is_schema_valid() -> None:
    schema = json.loads((ROOT / "process/schemas/decision-draft.schema.json").read_text(encoding="utf-8"))

    assert list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(_decision_draft())) == []


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


def test_packaged_sanitized_analytics_example_validates_and_previews_without_actions() -> None:
    example = ROOT / "process" / "examples" / "analytics" / "sanitized"

    report = validate_analytics_package(example)
    preview = preview_analytics(example, report)

    assert report["status"] == "valid"
    assert preview["status"] == "valid"
    assert preview["integration_actions"] == []
    assert preview["external_state_mutated"] is False

def test_gigacode_start_prompt_uses_only_project_interactive_roles() -> None:
    prompt = (ROOT / "process" / "gigacode" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Analyst, Tech Lead, Developer, QA" in prompt
    assert "Change Owner" not in prompt
    assert "Release Owner" not in prompt


def test_gigacode_companion_discovery_does_not_claim_human_authority() -> None:
    companion = (
        ROOT / "process" / "gigacode" / "skills" / "sdd-process-companion.md"
    ).read_text(encoding="utf-8")

    assert "не подтверждай classification" in companion
    assert "не подставляй `--confirm`" in companion
    assert "не выполняй `next_command`" in companion
    assert "AI подтверждает classification" not in companion


def test_catalog_never_grants_implementation_entry_to_tech_lead() -> None:
    payload = guide(
        "existing-change",
        {"change_id": "sample", "lifecycle_state": "approved", "human_role": "Tech Lead"},
        set(),
    )

    assert payload["status"] == "guided"
    assert payload["cta"] == "monitor-process-status"


def _decision_draft() -> dict[str, object]:
    return guided_workflow.create_decision_draft(
        change_id="sample",
        decision_type="spec-acceptance",
        revision_digest="a" * 64,
        natural_message="Принимаю спецификацию",
        consequence="prepare-role-pr-approval",
        source_event={
            "event_ref": "chat://trusted/100", "actor_type": "human", "sequence": 100,
            "timestamp": "2026-07-23T10:00:00Z", "message": "Принимаю спецификацию",
        },
        card_event={
            "event_ref": "chat://trusted/101", "actor_type": "assistant", "sequence": 101,
            "previous_event_ref": "chat://trusted/100", "timestamp": "2026-07-23T10:00:30Z",
        },
        expires_at="2026-07-23T10:05:00Z",
    )


def _decision_interaction() -> dict[str, object]:
    return {
        "decision": {
            "change_id": "sample",
            "decision_type": "spec-acceptance",
            "revision_digest": "a" * 64,
            "natural_message": "Принимаю спецификацию",
            "consequence": "prepare-role-pr-approval",
            "source_event": {
                "event_ref": "chat://trusted/100", "actor_type": "human", "sequence": 100,
                "timestamp": "2026-07-23T10:00:00Z", "message": "Принимаю спецификацию",
            },
            "card_event": {
                "event_ref": "chat://trusted/101", "actor_type": "assistant", "sequence": 101,
                "previous_event_ref": "chat://trusted/100", "timestamp": "2026-07-23T10:00:30Z",
            },
            "expires_at": "2026-07-23T10:05:00Z",
        },
        "discovery": {
            "mode": "обычно",
            "areas": [{"id": "data-retention", "impact": "changes risk and runtime", "material": True}],
        },
    }


def test_existing_change_guided_route_keeps_natural_text_unconfirmed_until_the_next_trusted_confirmation() -> None:
    facts = {"change_id": "sample", "revision_digest": "a" * 64, "lifecycle_state": "spec_review", "human_role": "Analyst"}
    interaction = _decision_interaction()

    draft_payload = guide("existing-change", facts, set(), interaction=interaction)
    draft = draft_payload["guided_interaction"]["decision_draft"]
    assert draft_payload["status"] == "guided"
    assert draft["authority_recorded"] is False
    assert "confirmation_event" not in draft_payload["guided_interaction"]
    assert draft_payload["guided_interaction"]["discovery_map"]["intake_sufficient"] is False

    trusted = {
        **interaction,
        "confirmation_event": {
            "event_ref": "chat://trusted/102", "actor_type": "human", "sequence": 102,
            "previous_event_ref": "chat://trusted/101", "timestamp": "2026-07-23T10:01:00Z",
            "message": " \nПодтверждаю\t \n",
        },
    }
    confirmed = guide("existing-change", facts, set(), interaction=trusted)
    assert confirmed["guided_interaction"]["confirmation_event"]["decision_card_code"] == draft["card_code"]

    unknown = guide(
        "existing-change", facts, set(),
        interaction={**trusted, "confirmation_event": {**trusted["confirmation_event"], "message": "Да"}},
    )
    silent = guide("existing-change", facts, set(), interaction=interaction)
    assert "confirmation_event" not in unknown["guided_interaction"]
    assert silent["guided_interaction"]["discovery_map"]["areas"][0]["status"] == "blocking"


def test_existing_change_route_rejects_interaction_for_another_change_or_revision() -> None:
    facts = {"change_id": "sample", "revision_digest": "a" * 64, "lifecycle_state": "spec_review", "human_role": "Analyst"}
    interaction = _decision_interaction()

    wrong_change = guide(
        "existing-change", facts, set(),
        interaction={**interaction, "decision": {**interaction["decision"], "change_id": "other-change"}},
    )
    wrong_revision = guide(
        "existing-change", facts, set(),
        interaction={**interaction, "decision": {**interaction["decision"], "revision_digest": "b" * 64}},
    )

    assert wrong_change["status"] == "blocked"
    assert wrong_change["blockers"][0]["code"] == "invalid-guided-interaction"
    assert wrong_revision["status"] == "blocked"
    assert wrong_revision["blockers"][0]["code"] == "invalid-guided-interaction"


def test_natural_language_creates_only_revision_bound_decision_draft() -> None:
    draft = _decision_draft()

    assert draft["record_type"] == "decision_draft"
    assert draft["card_code"].startswith("DEC-")
    assert draft["source_message"] == "Принимаю спецификацию"
    assert draft["revision_digest"] == "a" * 64
    assert draft["authority_recorded"] is False
    assert "acceptance" not in draft
    assert "DoR" not in draft
    assert "lifecycle" not in draft


def test_only_immediate_exact_or_normalized_short_confirmation_creates_event() -> None:
    draft = _decision_draft()
    exact = guided_workflow.confirm_decision_draft(
        draft,
        {"event_ref": "chat://trusted/102", "actor_type": "human", "sequence": 102, "previous_event_ref": "chat://trusted/101", "timestamp": "2026-07-23T10:01:00Z", "message": "Подтверждаю " + str(draft["card_code"])},
    )
    short = guided_workflow.confirm_decision_draft(
        draft,
        {"event_ref": "chat://trusted/103", "actor_type": "human", "sequence": 102, "previous_event_ref": "chat://trusted/101", "timestamp": "2026-07-23T10:01:00Z", "message": "  Подтверждаю\n"},
    )

    assert exact["record_type"] == "confirmation_event"
    assert exact["decision_card_code"] == draft["card_code"]
    assert exact["source_message"] == "Принимаю спецификацию"
    assert exact["confirmation_message"] == "Подтверждаю " + str(draft["card_code"])
    assert exact["trusted_chat_event_ref"] == "chat://trusted/102"
    assert short["confirmation_message"] == "  Подтверждаю\n"


def test_ambiguous_stale_or_interleaved_chat_text_cannot_record_authority() -> None:
    draft = _decision_draft()
    attempts = [
        {"message": "что дальше?"}, {"message": "Да"}, {"message": "продолжай"},
        {"message": "Подтверждаю DEC-wrong"}, {"sequence": 103},
        {"previous_event_ref": "chat://trusted/interleaved"}, {"timestamp": "2026-07-23T10:06:00Z"},
    ]

    for index, change in enumerate(attempts):
        event = {"event_ref": f"chat://trusted/{index + 200}", "actor_type": "human", "sequence": 102, "previous_event_ref": "chat://trusted/101", "timestamp": "2026-07-23T10:01:00Z", "message": "Подтверждаю"}
        result = guided_workflow.confirm_decision_draft(draft, {**event, **change})
        assert result is None


def test_normal_mode_surfaces_material_unknowns_and_requires_explicit_choice() -> None:
    discovery = guided_workflow.build_discovery_map(
        "обычно",
        [
            {"id": "data-retention", "impact": "changes risk and runtime", "material": True},
            {"id": "copy-tone", "impact": "minor wording", "material": False},
        ],
    )

    material = discovery["areas"][0]
    assert material["status"] == "blocking"
    assert discovery["depth_recommendation"]["required"] is True
    assert discovery["depth_recommendation"]["choices"] == [
        "углубиться",
        "принять defaults",
        "подготовить draft с открытыми решениями",
    ]
    assert discovery["intake_sufficient"] is False

    silent = guided_workflow.record_discovery_choice(discovery, "data-retention", None)
    defaulted = guided_workflow.record_discovery_choice(discovery, "data-retention", "принять defaults")
    deferred = guided_workflow.record_discovery_choice(discovery, "data-retention", "подготовить draft с открытыми решениями")

    assert silent["areas"][0]["status"] == "blocking"
    assert silent["intake_sufficient"] is False
    assert defaulted["areas"][0]["status"] == "proposed_default"
    assert deferred["areas"][0]["status"] == "deferred"


def test_response_summary_uses_only_validated_confirmation_records() -> None:
    draft = _decision_draft()
    event = guided_workflow.confirm_decision_draft(
        draft,
        {"event_ref": "chat://trusted/102", "actor_type": "human", "sequence": 102, "previous_event_ref": "chat://trusted/101", "timestamp": "2026-07-23T10:01:00Z", "message": "Подтверждаю"},
    )
    report = {"status": "valid", "diagnostics": [], "spec_revision": {"sha256": "a" * 64}}

    valid_summary = build_response_summary(None, report, confirmation_event=event)
    invalid_summary = build_response_summary(
        None,
        report,
        confirmation_event={**event, "trusted_chat_event_ref": ""},
    )
    ambiguous_summary = build_response_summary(
        None,
        report,
        confirmation_event={**event, "confirmation_message": "Да"},
    )

    assert valid_summary["decision_confirmation"]["status"] == "confirmed"
    assert invalid_summary["decision_confirmation"]["status"] == "unconfirmed"
    assert ambiguous_summary["decision_confirmation"]["status"] == "unconfirmed"
    assert valid_summary["lifecycle_mutated"] is False


SCENARIO_COVERAGE = {
    "test_unknown_role_blocks_role_sensitive_guidance": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Fail-closed role-aware guidance", "scenario": "Unknown role is blocked"},
    ],
    "test_analyst_never_receives_implementation_cta": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Fail-closed role-aware guidance", "scenario": "Analyst cannot receive implementation CTA"},
    ],
    "test_natural_language_creates_only_revision_bound_decision_draft": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Human-confirmed decision card", "scenario": "Natural-language decision prepares but does not record"},
    ],
    "test_only_immediate_exact_or_normalized_short_confirmation_creates_event": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Human-confirmed decision card", "scenario": "Card confirmation records only the active decision"},
    ],
    "test_ambiguous_stale_or_interleaved_chat_text_cannot_record_authority": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Human-confirmed decision card", "scenario": "Ambiguous chat text cannot record a decision"},
    ],
    "test_normal_mode_surfaces_material_unknowns_and_requires_explicit_choice": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Proactive discovery completeness", "scenario": "Material unknowns receive an explicit choice"},
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Proactive discovery completeness", "scenario": "Silence is not default acceptance"},
    ],
    "test_response_summary_uses_only_validated_confirmation_records": [
        {"source_kind": "delta", "capability": "role-aware-guided-workflow", "requirement": "Human-confirmed decision card", "scenario": "Card confirmation records only the active decision"},
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
