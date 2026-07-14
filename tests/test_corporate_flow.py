"""Scenario-first acceptance tests for Phase 2 work item 2.7."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from process.validators.corporate_flow import (
    evaluate_corporate_flow,
    governance_record_digest,
    validate_corporate_flow_input,
)
from process.validators.policy_validation import validate_policy_bundle
from process.validators.tech_lead import policy_snapshot_digest
from scripts.check_corporate_flow import main as corporate_flow_main
from tests.test_tech_lead_review import _control, _owners, projects


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
CONFIG = ROOT / "tests" / "fixtures" / "policy-v2" / "config" / "valid-central.yaml"


def _yaml(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _snapshot():
    result = validate_policy_bundle(
        PROCESS,
        _yaml(PROCESS / "policies" / "manifest.yaml"),
        _yaml(CONFIG),
        None,
    )
    assert result.snapshot is not None, result.diagnostics
    return result.snapshot


def _policy() -> dict[str, str]:
    snapshot = _snapshot()
    return {
        "id": snapshot.policy_set_id,
        "version": snapshot.policy_set_version,
        "digest": policy_snapshot_digest(snapshot),
    }


def _evidence(identifier: str, *scopes: str, kind: str = "document") -> dict[str, object]:
    return {
        "id": identifier,
        "kind": kind,
        "ref": f"evidence/{identifier}.json",
        "sha256": hashlib.sha256(identifier.encode()).hexdigest(),
        "scope_ids": list(scopes or ("sample-change",)),
    }


def _record(
    identifier: str,
    record_type: str,
    payload: dict[str, object],
    *,
    minute: int,
    evidence: list[str] | None = None,
) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "record_id": identifier,
        "record_type": record_type,
        "scope_ids": ["sample-change"],
        "recorded_at": f"2026-07-14T08:{minute:02d}:00Z",
        "source_ref": f"records/{identifier}.yaml",
        "policy_snapshot": _policy(),
        "evidence_refs": evidence or ["ev-source"],
        "accountable_decision": {
            "actor_type": "human",
            "actor_id": "sample-primary",
            "role": "tech_lead",
            "decision_ref": "decisions/D-1.yaml",
        },
        "payload": payload,
    }


def valid_bundle() -> dict[str, object]:
    roles = ["product", "analyst", "developer", "qa", "tech_lead", "release_support"]
    records = [
        _record("triage-1", "initiative-triage", {
            "problem_or_opportunity": "Reduce unsafe handoffs.",
            "expected_value": "Reproducible delivery.",
            "sponsor_or_owner": "sample-primary",
            "affected_contour": ["sample-app"],
            "urgency": "normal",
            "dependencies": ["sample-dependency"],
            "constraints": ["synthetic-only"],
            "initial_class_hypothesis": "minor",
            "unanswered_questions": [],
            "outcome": "proceed",
        }, minute=0),
        _record("baseline-1", "approved-baseline", {
            "requirements": ["REQ-1"], "scenarios": ["SC-1"],
            "scope": ["sample-app"], "exclusions": ["deployment"],
            "dependencies": ["sample-dependency"], "classification": "minor",
            "quality_strategy_ref": "quality-1", "decision_version": "D-1:v1",
            "approved": True,
        }, minute=1),
        _record("quality-1", "quality-strategy", {
            "classification": "minor",
            "scenario_levels": ["unit", "manual"], "static_checks": ["schema"],
            "developer_tests": ["tests/test_sample.py"], "qa_manual_evidence": ["ev-qa"],
            "automation": ["pytest"], "data_environment": ["synthetic"],
            "regression_scope": ["REQ-1:SC-1"], "negative_cases": ["missing-row"],
            "responsible_roles": ["developer", "qa"], "allowed_waivers": [],
            "qa_decision_ref": "qa-1",
        }, minute=2),
        _record("regression-1", "regression-row", {
            "product_or_module": "sample-app", "requirement_scenario": "REQ-1:SC-1",
            "change_class": "minor", "risk_trigger": "behavior-change",
            "required_check": "pytest tests/test_sample.py", "test_data_environment": "synthetic",
            "evidence_type": "test-result", "owner": "sample-qa", "current_result": "passed",
            "evidence_ref": "ev-qa",
        }, minute=3),
        _record("qa-1", "qa-decision", {
            "decision_kind": "strategy-and-regression", "decision": "sufficient",
            "material_failures": [], "missing_evidence": [], "gate_may_proceed": True,
        }, minute=4),
        _record("human-1", "human-decision", {
            "decision_type": "baseline-approval", "source_evidence": ["ev-source"],
            "decision": "approved", "follow_up": "none",
        }, minute=5),
        _record("ai-1", "ai-execution", {
            "model_runtime": "synthetic-disabled", "prompt_or_skill_version": "flow-check-v1",
            "input_scope": ["sample-change"], "tool_config_version": "sdd-core/1.0.0",
            "output_ref": "ev-ai", "reviewer_disposition": "accepted-as-advisory",
            "failures": [], "manual_interventions": ["human-review"],
        }, minute=6),
        _record("release-1", "release-handoff", {
            "artifact_version": "sample-app/1.0.0", "included_changes": ["sample-change"],
            "requirements_scenarios": ["REQ-1:SC-1"], "verification_evidence": ["ev-qa"],
            "known_limitations": ["synthetic contour"], "configuration_assumptions": ["offline"],
            "installation_transfer_steps": ["verify checksum"], "rollback_or_hold": ["hold import"],
            "operations_support_contacts": ["sample-release"], "unresolved_follow_ups": [],
            "chain": {
                "tracker": "ev-tracker", "canonical_spec": "ev-spec", "implementation": "ev-git",
                "ci_test": "ev-ci", "artifact_repository": "ev-artifact", "release": "ev-release",
                "external_delivery": "ev-delivery",
            },
            "artifact_repository_status": "available",
        }, minute=7),
        _record("acceptance-1", "consumer-acceptance", {
            "package_ref": "release-1", "package_version": "sample-app/1.0.0",
            "receiver": "sample-consumer", "compatibility_result": "compatible",
            "deviations": [], "decision": "accepted",
        }, minute=8),
        _record("roles-1", "role-map", {
            "roles": [{"role": role, "owner_type": "human", "owner_id": f"sample-{role.replace('_', '-')}"} for role in roles],
            "architecture_applicable": False, "security_applicable": False,
        }, minute=9),
        *[
            _record(f"walkthrough-{index}", "role-walkthrough", {
                "role": role, "positive_cases": ["valid-input"], "negative_cases": ["forbidden-approval"],
                "required_inputs": ["canonical-records"], "outputs": ["source-linked-report"],
                "approvals": ["human-only"], "forbidden_actions": ["ai-approval"],
                "stop_escalation": ["hold-on-unsafe"], "ai_disabled": True,
                "scenario_evidence": ["ev-role"], "reviewer_disposition": "passed",
            }, minute=10 + index)
            for index, role in enumerate(roles)
        ],
        _record("wip-1", "portfolio-wip", {
            "limit": 2, "limit_source": "policy/sample-wip", "active_change_ids": ["sample-change"],
            "decision": "within-limit", "decision_owner": "sample-primary",
        }, minute=16),
        _record("pilot-1", "pilot-selection", {
            "candidate_id": "synthetic-pilot", "representativeness": "covers governed handoff",
            "classification": "minor", "systems": ["sample-app"], "dependencies": ["sample-dependency"],
            "data_security_constraints": ["synthetic-only"], "team_readiness": "ready",
            "rollback_feasibility": "verified", "exclusion_risks": ["no real integration"],
            "selected": True,
        }, minute=17),
        _record("attempt-1", "failed-run", {
            "run_id": "run-1", "attempt_kind": "validation", "attempt_ordinal": 1,
            "outcome": "failed", "input_refs": ["ev-source"], "output_refs": ["ev-failed"],
            "version_or_configuration": "sdd-core/1.0.0", "failure": "expected synthetic failure",
            "owner_disposition": "retry-approved", "operational_flags": [],
        }, minute=18),
        _record("attempt-2", "failed-run", {
            "run_id": "run-1", "attempt_kind": "validation", "attempt_ordinal": 2,
            "outcome": "succeeded", "input_refs": ["ev-source"], "output_refs": ["ev-success"],
            "version_or_configuration": "sdd-core/1.0.0", "failure": "none",
            "owner_disposition": "reviewed", "retry_of": "attempt-1", "predecessor_digest": "pending",
            "operational_flags": [],
        }, minute=19),
        _record("safety-1", "pilot-safety", {
            "risks": [{
                "risk": risk, "control": "synthetic bounded control", "owner": "sample-primary",
                "evidence_ref": "ev-safety", "status": "controlled",
            } for risk in (
                "data-privacy", "secrets", "access", "accidental-delivery", "rollback-or-hold",
                "adapters-and-mcps", "model-runtime-behavior", "logging", "external-dependencies",
                "support-ownership", "evidence-corruption", "process-bypass",
            )],
            "ai_disabled_path": True,
        }, minute=20),
    ]
    attempt = next(row for row in records if row["record_id"] == "attempt-2")
    predecessor = next(row for row in records if row["record_id"] == "attempt-1")
    qa_decision = next(row for row in records if row["record_id"] == "qa-1")
    qa_decision["accountable_decision"].update({
        "actor_id": "sample-qa-owner", "role": "qa",
    })
    attempt["payload"]["predecessor_digest"] = governance_record_digest(predecessor)
    evidence_ids = {
        "ev-source", "ev-qa", "ev-ai", "ev-tracker", "ev-spec", "ev-git", "ev-ci",
        "ev-artifact", "ev-release", "ev-delivery", "ev-role", "ev-failed", "ev-success", "ev-safety",
    }
    return {
        "schema_version": "1.0", "change_id": "sample-change", "evaluation_date": "2026-07-14",
        "scope_ids": ["sample-change"],
        "evidence_catalog": [_evidence(identifier, "sample-change") for identifier in sorted(evidence_ids)],
        "records": records, "tech_lead_control_records": [],
    }


def _evaluate(bundle: dict[str, object]):
    return evaluate_corporate_flow(
        bundle, _owners(), projects(), _snapshot(), as_of="2026-07-14"
    )


def test_valid_governance_bundle_is_check_only_and_may_continue() -> None:
    bundle = valid_bundle()
    assert validate_corporate_flow_input(bundle, PROCESS) == []

    payload = _evaluate(bundle).as_dict()

    assert payload["status"] == "may_continue"
    assert payload["may_continue"] is True
    assert payload["active_record_ids"] == []
    assert payload["control_state_mutated"] is False
    assert payload["lifecycle_mutated"] is False
    assert payload["external_state_mutated"] is False
    assert payload["policy_snapshot"] == _policy()
    assert payload["proceed_is_not_dor"] is True


@pytest.mark.parametrize("outcome", ["proceed", "hold", "split", "redirect", "reject"])
def test_triage_supports_all_outcomes_but_only_proceed_requires_baseline(outcome: str) -> None:
    bundle = valid_bundle()
    triage = next(row for row in bundle["records"] if row["record_type"] == "initiative-triage")
    triage["payload"]["outcome"] = outcome
    if outcome != "proceed":
        bundle["records"] = [row for row in bundle["records"] if row["record_type"] != "approved-baseline"]

    report = _evaluate(bundle)

    assert report.as_dict()["triage_outcome"] == outcome
    assert report.as_dict()["proceed_is_not_dor"] is True


def test_material_scope_drift_requires_complete_human_reassessment() -> None:
    bundle = valid_bundle()
    bundle["records"].append(_record("drift-1", "scope-drift", {
        "changed_dimensions": ["business-behavior", "release-outcome"],
        "material": True, "baseline_ref": "baseline-1",
        "reassessments": ["classification", "readiness", "owners"],
        "approval_decision_ref": "human-1",
    }, minute=21))

    payload = _evaluate(bundle).as_dict()

    assert payload["status"] == "blocked"
    assert "flow.scope-reassessment-incomplete" in {row["code"] for row in payload["findings"]}


def test_regression_gap_stale_or_wrong_qa_authority_blocks() -> None:
    bundle = valid_bundle()
    qa = next(row for row in bundle["records"] if row["record_type"] == "qa-decision")
    qa["accountable_decision"]["actor_id"] = "assistant"
    regression = next(row for row in bundle["records"] if row["record_type"] == "regression-row")
    regression["payload"]["current_result"] = "not-run"

    payload = _evaluate(bundle).as_dict()
    codes = {row["code"] for row in payload["findings"]}

    assert "quality.qa-authority-invalid" in codes
    assert "quality.regression-result-blocking" in codes


def test_existing_control_ledger_is_authoritative_and_exception_cannot_clear_hold() -> None:
    bundle = valid_bundle()
    bundle["tech_lead_control_records"] = [_control("hold")]
    bundle["records"].append(_record("waiver-1", "exception", {
        "kind": "waiver", "affected_obligations": ["hold"], "reason": "continue anyway",
        "substitute_controls": ["manual review"], "expires_on": "2026-07-15",
        "follow_up": "review later", "decision": "approved",
    }, minute=21))

    payload = _evaluate(bundle).as_dict()

    assert payload["status"] == "blocked"
    assert "control-hold-1" in payload["active_record_ids"]
    assert "flow.active-control" in {row["code"] for row in payload["findings"]}


def test_release_chain_requires_real_or_approved_substitute_artifact_evidence() -> None:
    bundle = valid_bundle()
    release = next(row for row in bundle["records"] if row["record_type"] == "release-handoff")
    release["payload"]["artifact_repository_status"] = "unavailable"
    release["payload"]["chain"].pop("artifact_repository")

    payload = _evaluate(bundle).as_dict()
    assert "release.artifact-substitute-missing" in {row["code"] for row in payload["findings"]}

    release["payload"]["artifact_repository_substitute"] = "ev-artifact"
    release["payload"]["substitute_decision_ref"] = "human-1"
    assert "release.artifact-substitute-missing" not in {
        row["code"] for row in _evaluate(bundle).as_dict()["findings"]
    }


def test_role_map_wip_and_pilot_selection_fail_closed() -> None:
    bundle = valid_bundle()
    role_map = next(row for row in bundle["records"] if row["record_type"] == "role-map")
    role_map["payload"]["roles"][0]["owner_type"] = "ai"
    wip = next(row for row in bundle["records"] if row["record_type"] == "portfolio-wip")
    wip["payload"]["active_change_ids"] = ["sample-change", "change-2", "change-3"]
    wip["payload"]["decision"] = "within-limit"
    pilot = next(row for row in bundle["records"] if row["record_type"] == "pilot-selection")
    pilot["payload"]["rollback_feasibility"] = "unavailable"

    codes = {row["code"] for row in _evaluate(bundle).as_dict()["findings"]}

    assert {"roles.ai-substitution-forbidden", "portfolio.wip-decision-required", "pilot.rollback-unavailable"} <= codes


def test_failed_retry_cannot_erase_or_forge_predecessor() -> None:
    bundle = valid_bundle()
    failed = next(row for row in bundle["records"] if row["record_id"] == "attempt-1")
    bundle["records"].remove(failed)

    payload = _evaluate(bundle).as_dict()
    assert "failed-run.retry-predecessor-missing" in {row["code"] for row in payload["findings"]}

    bundle = valid_bundle()
    retry = next(row for row in bundle["records"] if row["record_id"] == "attempt-2")
    retry["payload"]["predecessor_digest"] = "0" * 64
    assert "failed-run.predecessor-digest-mismatch" in {
        row["code"] for row in _evaluate(bundle).as_dict()["findings"]
    }


def test_pilot_safety_locked_risks_and_failed_operational_flags_block() -> None:
    bundle = valid_bundle()
    safety = next(row for row in bundle["records"] if row["record_type"] == "pilot-safety")
    safety["payload"]["risks"].pop()
    failed = next(row for row in bundle["records"] if row["record_id"] == "attempt-1")
    failed["payload"]["operational_flags"] = ["canonical-evidence-corruption"]

    codes = {row["code"] for row in _evaluate(bundle).as_dict()["findings"]}

    assert "pilot.required-risk-missing" in codes
    assert "failed-run.operational-stop-required" in codes


def test_envelope_integrity_rejects_bad_scope_future_equal_time_and_duplicate_ids() -> None:
    bundle = valid_bundle()
    duplicate = copy.deepcopy(bundle["records"][0])
    duplicate["payload"]["expected_value"] = "different content"
    bundle["records"].append(duplicate)
    bundle["records"][1]["recorded_at"] = bundle["records"][0]["recorded_at"]
    bundle["records"][2]["recorded_at"] = "2026-07-15T00:00:00Z"
    bundle["records"][3]["scope_ids"] = ["other-change"]

    codes = {row["code"] for row in _evaluate(bundle).as_dict()["findings"]}

    assert {
        "governance.record-id-duplicate", "governance.record-time-tie",
        "governance.record-future", "governance.scope-mismatch",
    } <= codes


def test_valid_correction_appends_and_supersedes_semantics_without_overwrite() -> None:
    bundle = valid_bundle()
    expired = _record("waiver-old", "exception", {
        "kind": "waiver", "affected_obligations": ["optional-evidence"], "reason": "temporary",
        "substitute_controls": ["manual-review"], "expires_on": "2026-07-13",
        "follow_up": "renew or close", "decision": "approved",
    }, minute=21)
    corrected = _record("waiver-current", "exception", {
        "kind": "waiver", "affected_obligations": ["optional-evidence"], "reason": "corrected source",
        "substitute_controls": ["manual-review"], "expires_on": "2026-07-15",
        "follow_up": "close after evidence", "decision": "approved",
    }, minute=22)
    corrected["supersedes"] = "waiver-old"
    bundle["records"].extend([expired, corrected])

    codes = {row["code"] for row in _evaluate(bundle).as_dict()["findings"]}

    assert "flow.exception-expired" not in codes


def test_cli_has_stable_human_json_parity_and_never_mutates(tmp_path: Path, capsys) -> None:
    bundle_path = tmp_path / "flow.yaml"
    owners_path = tmp_path / "owners.yaml"
    projects_path = tmp_path / "projects.yaml"
    bundle_path.write_text(yaml.safe_dump(valid_bundle(), sort_keys=False), encoding="utf-8")
    owners_path.write_text(yaml.safe_dump(_owners(), sort_keys=False), encoding="utf-8")
    projects_path.write_text(yaml.safe_dump(projects(), sort_keys=False), encoding="utf-8")
    before = bundle_path.read_bytes()
    common = [
        str(bundle_path), "--owners", str(owners_path), "--projects", str(projects_path),
        "--config", str(CONFIG), "--as-of", "2026-07-14",
    ]

    assert corporate_flow_main([*common, "--json"]) == 0
    json_payload = json.loads(capsys.readouterr().out)
    assert corporate_flow_main(common) == 0
    human = capsys.readouterr().out

    assert f"Corporate flow: {json_payload['status']}" in human
    assert f"May continue: {str(json_payload['may_continue']).lower()}" in human
    assert f"Findings: {len(json_payload['findings'])}" in human
    assert bundle_path.read_bytes() == before


def test_cli_rejects_and_redacts_inline_secret_material(tmp_path: Path, capsys) -> None:
    bundle = valid_bundle()
    triage = next(row for row in bundle["records"] if row["record_type"] == "initiative-triage")
    triage["payload"]["constraints"] = ["AKIAABCDEFGHIJKLMNOP"]
    bundle_path = tmp_path / "flow.yaml"
    owners_path = tmp_path / "owners.yaml"
    projects_path = tmp_path / "projects.yaml"
    bundle_path.write_text(yaml.safe_dump(bundle, sort_keys=False), encoding="utf-8")
    owners_path.write_text(yaml.safe_dump(_owners(), sort_keys=False), encoding="utf-8")
    projects_path.write_text(yaml.safe_dump(projects(), sort_keys=False), encoding="utf-8")

    code = corporate_flow_main([
        str(bundle_path), "--owners", str(owners_path), "--projects", str(projects_path),
        "--config", str(CONFIG), "--as-of", "2026-07-14", "--json",
    ])
    output = capsys.readouterr().out

    assert code == 3
    assert "secret.recognizable-token" in output
    assert "AKIAABCDEFGHIJKLMNOP" not in output
