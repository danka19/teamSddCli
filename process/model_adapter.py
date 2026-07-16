"""Closed model-response boundary for role-specific advisory work."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from process.weak_model_kit import (
    _digest,
    _schema_errors,
    _without_identity,
    contains_forbidden_authority_claim,
)


class ModelAdapterError(ValueError):
    """Stable model-adapter contract failure."""


STRUCTURAL_RETRY_CODES = {
    "model-adapter.empty-final",
    "model-adapter.invalid-json",
    "model-adapter.schema",
}


def _verified_contract(launch: dict[str, Any]) -> dict[str, Any]:
    process_root = Path(__file__).resolve().parent
    if (
        _schema_errors(process_root, "task-launch.schema.json", launch)
        or launch.get("identity") != _digest(_without_identity(launch))
    ):
        raise ModelAdapterError("model-adapter.invalid-launch")
    contract = launch.get("model_response_contract")
    if not isinstance(contract, dict):
        raise ModelAdapterError("model-adapter.missing-contract")
    return contract


def _build_role_response_schema_2_0(
    launch: dict[str, Any], contract: dict[str, Any]
) -> dict[str, Any]:
    payload_key = contract["role_payload_key"]
    source_ids = [source["stable_id"] for source in launch["verified_source_manifest"]]
    source_ids.append("case-facts")
    source_id = {"type": "string", "enum": source_ids}
    nonempty_string = {"type": "string", "minLength": 1}
    payload = {
        "oneOf": [
            {"type": "null"},
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["summary", "observations", "claims", "checks"],
                "properties": {
                    "summary": nonempty_string,
                    "observations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["summary", "source_id"],
                            "properties": {"summary": nonempty_string, "source_id": source_id},
                        },
                    },
                    "claims": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["subject", "summary", "source_id"],
                            "properties": {
                                "subject": nonempty_string,
                                "summary": nonempty_string,
                                "source_id": source_id,
                            },
                        },
                    },
                    "checks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["command", "result", "evidence", "source_id"],
                            "properties": {
                                "command": nonempty_string,
                                "result": {
                                    "enum": [
                                        "passed",
                                        "failed",
                                        "not-run",
                                        "missing",
                                        "unsupported",
                                        "conflict",
                                        "source-reviewed",
                                    ]
                                },
                                "evidence": nonempty_string,
                                "source_id": source_id,
                            },
                        },
                    },
                },
            },
        ]
    }
    required = [
        "case_id",
        "decision",
        "reason_codes",
        "source_ids",
        "unresolved_inputs",
        "human_decisions_required",
        payload_key,
    ]
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": {
            "case_id": {"const": contract["case_id"]},
            "decision": {"enum": ["draft", "block"]},
            "reason_codes": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": {"enum": contract["allowed_reason_codes"]},
            },
            "source_ids": {
                "type": "array",
                "minItems": 1,
                "uniqueItems": True,
                "items": source_id,
            },
            "unresolved_inputs": {"type": "array", "items": {"type": "string"}},
            "human_decisions_required": {"type": "array", "items": {"type": "string"}},
            payload_key: payload,
        },
    }


def _build_role_response_schema_2_1(
    launch: dict[str, Any], contract: dict[str, Any]
) -> dict[str, Any]:
    payload_key = contract["role_payload_key"]
    source_ids = [source["stable_id"] for source in launch["verified_source_manifest"]]
    source_ids.append("case-facts")
    source_id = {"type": "string", "enum": source_ids}
    nonempty_string = {"type": "string", "minLength": 1}
    string_array = {"type": "array", "items": nonempty_string}
    observations = {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["summary", "source_id"],
            "properties": {"summary": nonempty_string, "source_id": source_id},
        },
    }
    claims = {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["subject", "summary", "source_id"],
            "properties": {
                "subject": nonempty_string,
                "summary": nonempty_string,
                "source_id": source_id,
            },
        },
    }
    draft_payload_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["artifact_kind", "summary", "observations", "claims", "checks"],
        "properties": {
            "artifact_kind": {"enum": contract["allowed_artifact_kinds"]},
            "summary": nonempty_string,
            "observations": observations,
            "claims": claims,
            "checks": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["command", "result", "evidence", "source_id"],
                    "properties": {
                        "command": nonempty_string,
                        "result": {
                            "enum": [
                                "source-reviewed",
                                "not-run",
                                "missing",
                                "unsupported",
                                "conflict",
                            ]
                        },
                        "evidence": nonempty_string,
                        "source_id": source_id,
                    },
                },
            },
        },
        "anyOf": [
            {"properties": {"observations": {"minItems": 1}}},
            {"properties": {"claims": {"minItems": 1}}},
        ],
    }
    common_required = [
        "case_id",
        "decision",
        "reason_codes",
        "source_ids",
        "unresolved_inputs",
        "human_decisions_required",
        payload_key,
    ]
    common_properties = {
        "case_id": {"const": contract["case_id"]},
        "reason_codes": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": {"enum": contract["allowed_reason_codes"]},
        },
        "source_ids": {
            "type": "array",
            "minItems": 1,
            "uniqueItems": True,
            "items": source_id,
        },
    }
    draft_branch = {
        "type": "object",
        "additionalProperties": False,
        "required": common_required,
        "properties": {
            **common_properties,
            "decision": {"const": "draft"},
            "unresolved_inputs": string_array,
            "human_decisions_required": string_array,
            payload_key: draft_payload_schema,
        },
    }
    block_branch = {
        "type": "object",
        "additionalProperties": False,
        "required": common_required,
        "properties": {
            **common_properties,
            "decision": {"const": "block"},
            "unresolved_inputs": {**string_array, "minItems": 1},
            "human_decisions_required": {**string_array, "minItems": 1},
            payload_key: {"type": "null"},
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "oneOf": [draft_branch, block_branch],
    }


def build_role_response_schema(launch: dict[str, Any]) -> dict[str, Any]:
    """Return one closed, non-leading Draft 2020-12 response schema."""
    contract = _verified_contract(launch)
    if contract.get("contract_version") == "2.1":
        return _build_role_response_schema_2_1(launch, contract)
    return _build_role_response_schema_2_0(launch, contract)


def split_reasoning_final(response: str, thinking: str) -> tuple[str, str]:
    """Separate reasoning envelopes without ever treating reasoning as final output."""
    reasoning_parts = [thinking.strip()] if thinking.strip() else []
    final = response.strip()
    if final.startswith("<think>"):
        closing = final.find("</think>", len("<think>"))
        if closing < 0:
            embedded = final[len("<think>") :].strip()
            if embedded:
                reasoning_parts.append(embedded)
            return "\n\n".join(reasoning_parts), ""
        embedded = final[len("<think>") : closing].strip()
        if embedded:
            reasoning_parts.append(embedded)
        final = final[closing + len("</think>") :].strip()
    return "\n\n".join(reasoning_parts), final


def parse_role_response(text: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Parse one exact JSON response and enforce its closed role schema."""
    if not text.strip():
        raise ModelAdapterError("model-adapter.empty-final")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ModelAdapterError("model-adapter.invalid-json") from error
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda item: item.json_path)
    if errors:
        raise ModelAdapterError("model-adapter.schema")
    return value


def is_structural_retry(code: str) -> bool:
    """Return whether one stable adapter failure permits a structural retry."""
    return code in STRUCTURAL_RETRY_CODES


CHECK_RESULT_MAP = {
    "passed": "passed",
    "failed": "failed",
    "missing": "failed",
    "unsupported": "failed",
    "conflict": "failed",
    "not-run": "not-run",
    "source-reviewed": "passed",
}


def normalize_role_response(
    response: dict[str, Any], launch: dict[str, Any], read_pack: dict[str, Any]
) -> dict[str, Any]:
    """Mechanically map one verified role response into advisory operation evidence."""
    contract = _verified_contract(launch)
    process_root = Path(__file__).resolve().parent
    if (
        _schema_errors(process_root, "read-pack.schema.json", read_pack)
        or read_pack.get("identity") != _digest(_without_identity(read_pack))
        or launch.get("read_pack_identity") != read_pack.get("identity")
    ):
        raise ModelAdapterError("model-adapter.invalid-read-pack")
    expected_manifest = [
        {key: source[key] for key in ("authority", "stable_id", "path", "sha256")}
        for source in read_pack.get("sources", [])
    ]
    if launch.get("verified_source_manifest") != expected_manifest:
        raise ModelAdapterError("model-adapter.invalid-launch")
    schema = build_role_response_schema(launch)
    if list(Draft202012Validator(schema).iter_errors(response)):
        raise ModelAdapterError("model-adapter.semantic")

    payload_key = contract["role_payload_key"]
    payload = response[payload_key]
    decision = response["decision"]
    if (decision == "draft" and payload is None) or (decision == "block" and payload is not None):
        raise ModelAdapterError("model-adapter.semantic")
    if decision == "draft" and (not payload["checks"] or not (payload["observations"] or payload["claims"])):
        raise ModelAdapterError("model-adapter.semantic")

    referenced_ids: set[str] = set()
    if payload is not None:
        referenced_ids = {
            item["source_id"]
            for group in (payload["observations"], payload["claims"], payload["checks"])
            for item in group
        }
        if not referenced_ids <= set(response["source_ids"]):
            raise ModelAdapterError("model-adapter.semantic")
    authority_surface = {
        "unresolved_inputs": response["unresolved_inputs"],
        "human_decisions_required": response["human_decisions_required"],
        payload_key: payload,
    }
    if contains_forbidden_authority_claim(authority_surface):
        raise ModelAdapterError("model-adapter.semantic")

    manifest_by_id = {source["stable_id"]: source for source in launch["verified_source_manifest"]}
    sources_read = [
        dict(manifest_by_id[source_id])
        for source_id in response["source_ids"]
        if source_id != "case-facts"
    ]
    claims: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    if payload is not None:
        claims.extend(
            {
                "kind": "fact",
                "value": {"subject": "observation", "summary": item["summary"]},
                "evidence": f"source:{item['source_id']}",
            }
            for item in payload["observations"]
        )
        claims.extend(
            {
                "kind": "fact",
                "value": {"subject": item["subject"], "summary": item["summary"]},
                "evidence": f"source:{item['source_id']}",
            }
            for item in payload["claims"]
        )
        checks.extend(
            {
                "command": item["command"],
                "result": (
                    "not-run"
                    if (
                        contract.get("contract_version") == "2.1"
                        and item["result"] == "source-reviewed"
                    )
                    else CHECK_RESULT_MAP[item["result"]]
                ),
                "evidence": "model-check:"
                + json.dumps(
                    {
                        "result": item["result"],
                        "source_id": item["source_id"],
                        "evidence": item["evidence"],
                    },
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ),
            }
            for item in payload["checks"]
        )
        canonical_references = [
            {key: manifest_by_id[source_id][key] for key in ("stable_id", "sha256")}
            for source_id in response["source_ids"]
            if source_id != "case-facts" and manifest_by_id[source_id]["authority"] == "canonical"
        ]
        artifacts.append(
            {
                "path": (
                    f"scratch/model-adapter/{contract['case_id']}/"
                    f"{payload['artifact_kind'] if contract.get('contract_version') == '2.1' else contract['required_artifact_kind']}.json"
                ),
                "canonical": False,
                "canonical_references": canonical_references,
            }
        )
    return {
        "schema_version": "1.0",
        "task_id": launch["task_id"],
        "role": launch["role"],
        "stage": launch["stage_boundary"],
        "status": "draft-complete" if decision == "draft" else "blocked",
        "read_pack_identity": launch["read_pack_identity"],
        "sources_read": sources_read,
        "artifacts_drafted": artifacts,
        "checks": checks,
        "claims": claims,
        "human_decisions_required": list(response["human_decisions_required"]),
        "unresolved_inputs": list(response["unresolved_inputs"]),
        "residual_limitations": [f"model-reason:{code}" for code in response["reason_codes"]],
        "prohibited_actions_attempted": [],
        "human_stop_reached": True,
        "human_review_status": "pending",
        "lifecycle_transition_requested": False,
        "approval_claimed": False,
    }
