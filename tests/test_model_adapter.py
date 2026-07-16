from __future__ import annotations

import json
from pathlib import Path

import pytest

from process.model_adapter import (
    ModelAdapterError,
    build_role_response_schema,
    is_structural_retry,
    normalize_role_response,
    parse_role_response,
    split_reasoning_final,
)
from process.weak_model_kit import (
    GLOBAL_ALLOWED_REASON_CODES,
    build_read_pack,
    build_role_launch,
    validate_operation_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"
ROLE_PAYLOAD_KEYS = {
    "analyst": "requirements_note",
    "developer": "implementation_prep_note",
    "qa": "qa_review_note",
    "tech_lead": "advisory_review_note",
}
FORBIDDEN_VALIDATOR_FIELD_NAMES = {
    "contract",
    "risk_case",
    "required_source_ids",
    "expected_decision",
    "required_reason_codes",
    "required_output_kind",
    "expected_role_output",
    "golden_output",
}
VALIDATOR_ONLY_SENTINELS = [f"validator-only-{name.replace('_', '-')}" for name in FORBIDDEN_VALIDATOR_FIELD_NAMES]
REQUIRED_ARTIFACT_KIND_SENTINEL = "evidence-boundary-note"


def adapter_context(role: str = "analyst") -> tuple[dict, dict, dict]:
    payload_key = ROLE_PAYLOAD_KEYS[role]
    case = {
        "id": f"{role.replace('_', '-')}-case",
        "operation": "bounded-role-review",
        **dict(zip(sorted(FORBIDDEN_VALIDATOR_FIELD_NAMES), VALIDATOR_ONLY_SENTINELS, strict=True)),
    }
    request = {
        "schema_version": "1.0",
        "task_id": f"TASK-{role.upper()}",
        "role": role,
        "change_class": "minor",
        "stage": "proposal",
        "sources": [
            {
                "authority": "canonical",
                "stable_id": "weak-model-guardrails",
                "path": "openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md",
                "required": True,
            },
            {
                "authority": "supporting",
                "stable_id": "change-template",
                "path": "process/templates/change/change.yaml",
                "required": True,
            },
        ],
        "known_traps": [],
        "unresolved_inputs": [],
    }
    pack = build_read_pack(ROOT, PROCESS, request)
    launch = build_role_launch(
        ROOT,
        PROCESS,
        pack,
        "scratch/read-pack.json",
        "evidence/model-adapter.yaml",
        model_response_contract={
            "case_id": case["id"],
            "operation": case["operation"],
            "role_payload_key": payload_key,
            "required_artifact_kind": REQUIRED_ARTIFACT_KIND_SENTINEL,
            "allowed_reason_codes": list(GLOBAL_ALLOWED_REASON_CODES),
        },
    )
    return case, pack, launch


@pytest.mark.parametrize(
    ("role", "payload_key"),
    [
        ("analyst", "requirements_note"),
        ("developer", "implementation_prep_note"),
        ("qa", "qa_review_note"),
        ("tech_lead", "advisory_review_note"),
    ],
)
def test_role_schema_is_closed_non_leading_and_role_specific(role: str, payload_key: str) -> None:
    _, _, launch = adapter_context(role=role)
    schema = build_role_response_schema(launch)
    serialized = json.dumps(schema, sort_keys=True)
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "case_id",
        "decision",
        "reason_codes",
        "source_ids",
        "unresolved_inputs",
        "human_decisions_required",
        payload_key,
    }
    assert payload_key in schema["properties"]
    assert not (FORBIDDEN_VALIDATOR_FIELD_NAMES & set(serialized.split('"')))
    assert all(sentinel not in serialized for sentinel in VALIDATOR_ONLY_SENTINELS)
    assert REQUIRED_ARTIFACT_KIND_SENTINEL not in serialized
    assert set(schema["properties"]["source_ids"]["items"]["enum"]) == {
        *(source["stable_id"] for source in launch["verified_source_manifest"]),
        "case-facts",
    }


def test_role_schema_requires_an_identity_verified_certification_projection() -> None:
    _, _, launch = adapter_context()
    launch["model_response_contract"]["case_id"] = "changed-case"
    with pytest.raises(ModelAdapterError, match="model-adapter.invalid-launch"):
        build_role_response_schema(launch)


def valid_role_response(launch: dict, payload_key: str | None = None) -> dict:
    payload_key = payload_key or launch["model_response_contract"]["role_payload_key"]
    source_ids = [source["stable_id"] for source in launch["verified_source_manifest"]]
    source_id = source_ids[0]
    return {
        "case_id": launch["model_response_contract"]["case_id"],
        "decision": "draft",
        "reason_codes": ["bounded-draft"],
        "source_ids": [*source_ids, "case-facts"],
        "unresolved_inputs": [],
        "human_decisions_required": ["Named human reviews the advisory draft."],
        payload_key: {
            "summary": "Bounded role-specific draft.",
            "observations": [{"summary": "The source defines the advisory boundary.", "source_id": source_id}],
            "claims": [{"subject": "boundary", "summary": "Canonical mutation remains disabled.", "source_id": source_id}],
            "checks": [{"command": "deterministic-check", "result": "not-run", "evidence": "not-run:adapter", "source_id": source_id}],
        },
    }


def test_parser_rejects_wrapper_unknown_source_and_wrong_role_payload() -> None:
    _, _, launch = adapter_context(role="qa")
    schema = build_role_response_schema(launch)
    valid = valid_role_response(launch, payload_key="qa_review_note")
    assert parse_role_response(json.dumps(valid), schema) == valid
    wrong_role = {key: value for key, value in valid.items() if key != "qa_review_note"}
    wrong_role["implementation_prep_note"] = valid["qa_review_note"]
    for invalid_text in (
        "```json\n" + json.dumps(valid) + "\n```",
        "Model response: " + json.dumps(valid),
        json.dumps({**valid, "source_ids": ["unknown-source"]}),
        json.dumps({**valid, "reason_codes": ["validator-only-reason"]}),
        json.dumps(wrong_role),
    ):
        with pytest.raises(ModelAdapterError):
            parse_role_response(invalid_text, schema)


def test_reasoning_is_separated_and_never_promoted_to_final_output() -> None:
    final = '{"case_id":"analyst-case"}'
    assert split_reasoning_final(final, "existing reasoning") == ("existing reasoning", final)
    assert split_reasoning_final(f"<think>embedded reasoning</think>{final}", "") == ("embedded reasoning", final)
    assert split_reasoning_final("<think>unclosed reasoning", "") == ("unclosed reasoning", "")
    assert split_reasoning_final("", "reasoning only") == ("reasoning only", "")


def test_parser_returns_stable_structural_retry_codes() -> None:
    _, _, launch = adapter_context()
    schema = build_role_response_schema(launch)
    for text, code in (("", "model-adapter.empty-final"), ("not json", "model-adapter.invalid-json")):
        with pytest.raises(ModelAdapterError, match=code):
            parse_role_response(text, schema)
        assert is_structural_retry(code) is True
    assert is_structural_retry("model-adapter.schema") is True
    assert is_structural_retry("model-adapter.semantic") is False


@pytest.mark.parametrize("role", ["analyst", "developer", "qa", "tech_lead"])
def test_normalizer_preserves_model_semantics_and_adds_only_launch_invariants(role: str) -> None:
    _, pack, launch = adapter_context(role=role)
    response = valid_role_response(launch)
    evidence = normalize_role_response(response, launch, pack)
    assert evidence["status"] == ("draft-complete" if response["decision"] == "draft" else "blocked")
    assert evidence["approval_claimed"] is False
    assert evidence["lifecycle_transition_requested"] is False
    assert evidence["human_stop_reached"] is True
    assert evidence["human_review_status"] == "pending"
    assert [item["stable_id"] for item in evidence["sources_read"]] == response["source_ids"][:-1]
    assert response["reason_codes"] == [
        value.removeprefix("model-reason:") for value in evidence["residual_limitations"]
    ]
    payload = response[launch["model_response_contract"]["role_payload_key"]]
    assert [item["value"]["summary"] for item in evidence["claims"]] == [
        *(item["summary"] for item in payload["observations"]),
        *(item["summary"] for item in payload["claims"]),
    ]
    assert [item["result"] for item in evidence["checks"]] == ["not-run"]
    artifact = evidence["artifacts_drafted"][0]
    assert REQUIRED_ARTIFACT_KIND_SENTINEL in artifact["path"]
    assert artifact["canonical"] is False
    assert validate_operation_evidence(evidence, launch, pack) == []


@pytest.mark.parametrize(
    "mutation",
    ["missing-source", "draft-null", "block-payload", "empty-checks", "empty-claims", "authority-language"],
)
def test_normalizer_rejects_semantic_repairs_and_forbidden_authority(mutation: str) -> None:
    _, pack, launch = adapter_context()
    response = valid_role_response(launch)
    payload_key = launch["model_response_contract"]["role_payload_key"]
    if mutation == "missing-source":
        response["source_ids"].remove(response[payload_key]["claims"][0]["source_id"])
    elif mutation == "draft-null":
        response[payload_key] = None
    elif mutation == "block-payload":
        response["decision"] = "block"
    elif mutation == "empty-checks":
        response[payload_key]["checks"] = []
    elif mutation == "empty-claims":
        response[payload_key]["claims"] = []
        response[payload_key]["observations"] = []
    else:
        response[payload_key]["summary"] = "The model approved the release transition."
    with pytest.raises(ModelAdapterError, match="model-adapter.semantic"):
        normalize_role_response(response, launch, pack)


def test_normalizer_block_is_mechanical_and_has_no_artifact() -> None:
    _, pack, launch = adapter_context(role="qa")
    response = valid_role_response(launch)
    payload_key = launch["model_response_contract"]["role_payload_key"]
    response.update(
        decision="block",
        reason_codes=["missing-context"],
        unresolved_inputs=["A required QA result is absent."],
        human_decisions_required=["QA owner supplies or rejects the missing result."],
    )
    response[payload_key] = None
    evidence = normalize_role_response(response, launch, pack)
    assert evidence["status"] == "blocked"
    assert evidence["artifacts_drafted"] == []
    assert evidence["claims"] == []
    assert evidence["checks"] == []


@pytest.mark.parametrize(
    ("model_result", "evidence_result"),
    [
        ("missing", "failed"),
        ("unsupported", "failed"),
        ("conflict", "failed"),
        ("not-run", "not-run"),
        ("source-reviewed", "passed"),
    ],
)
def test_normalizer_preserves_check_result_semantics_and_source_provenance(
    model_result: str, evidence_result: str
) -> None:
    _, pack, launch = adapter_context()
    response = valid_role_response(launch)
    payload_key = launch["model_response_contract"]["role_payload_key"]
    check = response[payload_key]["checks"][0]
    check.update(result=model_result, evidence="original model evidence")
    evidence = normalize_role_response(response, launch, pack)
    assert evidence["checks"] == [
        {
            "command": "deterministic-check",
            "result": evidence_result,
            "evidence": (
                'model-check:{"evidence":"original model evidence","result":"'
                + model_result
                + '","source_id":"weak-model-guardrails"}'
            ),
        }
    ]
    if model_result in {"missing", "unsupported", "conflict"}:
        assert evidence["checks"][0]["result"] != "passed"


def test_authority_classifier_allows_required_human_decision_and_negated_claim() -> None:
    _, pack, launch = adapter_context()
    response = valid_role_response(launch)
    payload_key = launch["model_response_contract"]["role_payload_key"]
    response["human_decisions_required"] = ["Tech Lead approval is required"]
    response[payload_key]["claims"][0]["summary"] = "release is not approved"
    evidence = normalize_role_response(response, launch, pack)
    assert validate_operation_evidence(evidence, launch, pack) == []


@pytest.mark.parametrize(
    "claim",
    [
        "The model approved release.",
        "I authorize resume.",
        "I transition the change.",
        "I release the artifact.",
        "I archive the change.",
        "I merge the change.",
    ],
)
def test_authority_classifier_rejects_positive_model_authority_claims(claim: str) -> None:
    _, pack, launch = adapter_context()
    response = valid_role_response(launch)
    payload_key = launch["model_response_contract"]["role_payload_key"]
    response[payload_key]["claims"][0]["summary"] = claim
    with pytest.raises(ModelAdapterError, match="model-adapter.semantic"):
        normalize_role_response(response, launch, pack)


def test_evidence_validator_allows_negated_authority_claim_but_not_positive_claim() -> None:
    _, pack, launch = adapter_context()
    evidence = normalize_role_response(valid_role_response(launch), launch, pack)
    evidence["claims"][0]["value"]["summary"] = "release is not approved"
    assert validate_operation_evidence(evidence, launch, pack) == []
    evidence["claims"][0]["value"]["summary"] = "The model approved release"
    assert "evidence.forbidden-authority" in {
        item["code"] for item in validate_operation_evidence(evidence, launch, pack)
    }
