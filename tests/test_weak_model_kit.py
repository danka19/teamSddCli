from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

from process.weak_model_kit import (
    ContractError,
    build_read_pack,
    build_role_launch,
    validate_operation_evidence,
    validate_parallel_plan,
)


ROOT = Path(__file__).resolve().parents[1]
PROCESS = ROOT / "process"


def request() -> dict:
    return {
        "schema_version": "1.0",
        "task_id": "TASK-2.9-ANALYST",
        "role": "analyst",
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
        "known_traps": ["Do not infer approval from prose."],
        "unresolved_inputs": [],
    }


def test_build_read_pack_is_authority_labelled_bounded_and_stable() -> None:
    pack = build_read_pack(ROOT, PROCESS, request())
    assert pack["status"] == "ready"
    assert pack["identity"].startswith("sha256:")
    assert [source["authority"] for source in pack["sources"]] == ["canonical", "supporting"]
    assert all(source["stable_id"] and source["path"] and source["sha256"] for source in pack["sources"])
    assert "content" not in pack["sources"][0]


@pytest.mark.parametrize("mutation", ["missing", "escape", "duplicate", "unknown-canonical"])
def test_build_read_pack_blocks_missing_unsafe_or_ambiguous_context(mutation: str) -> None:
    data = request()
    if mutation == "missing":
        data["sources"][0]["path"] = "openspec/specs/does-not-exist.md"
    elif mutation == "escape":
        data["sources"][0]["path"] = "../private.txt"
    elif mutation == "duplicate":
        data["sources"].append(copy.deepcopy(data["sources"][0]))
    else:
        data["sources"][0]["path"] = "docs/README.md"
    pack = build_read_pack(ROOT, PROCESS, data)
    assert pack["status"] == "blocked"
    assert pack["missing_or_invalid_context"]


def test_launcher_selects_instruction_and_stop_point_outside_model(tmp_path: Path) -> None:
    pack = build_read_pack(ROOT, PROCESS, request())
    launch = build_role_launch(PROCESS, pack, "evidence/TASK-2.9-ANALYST.yaml")
    assert launch["role"] == "analyst"
    assert launch["instruction_path"] == "roles/analyst.md"
    assert launch["stage_boundary"] == "proposal"
    assert launch["model_authority"] == "advisory-only"
    assert launch["canonical_mutation_allowed"] is False
    assert launch["human_stop_required"] is True


def test_launcher_blocks_incomplete_read_pack() -> None:
    data = request()
    data["unresolved_inputs"] = ["Product owner must confirm the affected workflow."]
    pack = build_read_pack(ROOT, PROCESS, data)
    assert pack["status"] == "blocked"
    with pytest.raises(ContractError, match="read pack is blocked"):
        build_role_launch(PROCESS, pack, "evidence/x.yaml")


def valid_evidence() -> dict:
    return {
        "schema_version": "1.0",
        "task_id": "TASK-2.9-ANALYST",
        "role": "analyst",
        "stage": "proposal",
        "status": "draft-complete",
        "read_pack_identity": "sha256:" + "1" * 64,
        "sources_read": [{"stable_id": "weak-model-guardrails", "path": "openspec/spec.md"}],
        "artifacts_drafted": [
            {"path": "scratch/proposal.md", "canonical": False, "canonical_references": ["weak-model-guardrails"]}
        ],
        "checks": [{"command": "python scripts/validate_change.py sample", "result": "passed", "evidence": "log:check-1"}],
        "claims": [{"kind": "validation", "value": "change schema passed", "evidence": "log:check-1"}],
        "human_decisions_required": ["Product owner accepts proposal"],
        "unresolved_inputs": [],
        "residual_limitations": ["No model certification performed"],
        "prohibited_actions_attempted": [],
        "lifecycle_transition_requested": False,
        "approval_claimed": False,
    }


def test_operation_evidence_accepts_supported_advisory_completion() -> None:
    assert validate_operation_evidence(valid_evidence()) == []


@pytest.mark.parametrize(
    ("change", "code"),
    [
        ({"approval_claimed": True}, "evidence.forbidden-authority"),
        ({"lifecycle_transition_requested": True}, "evidence.forbidden-transition"),
        ({"status": "approved"}, "evidence.unsupported-completion"),
        ({"checks": [], "claims": [{"kind": "validation", "value": "passed", "evidence": "log:missing"}]}, "evidence.unsupported-claim"),
    ],
)
def test_operation_evidence_rejects_authority_and_unsupported_claims(change: dict, code: str) -> None:
    evidence = valid_evidence()
    evidence.update(change)
    assert code in {item["code"] for item in validate_operation_evidence(evidence)}


def test_operation_evidence_rejects_derived_canonical_artifact_without_source_reference() -> None:
    evidence = valid_evidence()
    evidence["artifacts_drafted"][0] = {"path": "openspec/spec.md", "canonical": True, "canonical_references": []}
    codes = {item["code"] for item in validate_operation_evidence(evidence)}
    assert {"evidence.canonical-draft-forbidden", "evidence.missing-canonical-reference"} <= codes


def valid_parallel_plan() -> dict:
    return {
        "schema_version": "1.0",
        "plan_id": "PAR-001",
        "integration_owner": "tech-lead-1",
        "tasks": [
            {
                "task_id": "TASK-A",
                "owner": "analyst-1",
                "dependencies": [],
                "write_scopes": ["docs/a"],
                "evidence_path": "evidence/a.yaml",
                "stop_condition": "proposal drafted",
                "focused_checks": ["python check-a.py"],
                "policy_or_lifecycle_decision": False,
            },
            {
                "task_id": "TASK-B",
                "owner": "developer-1",
                "dependencies": [],
                "write_scopes": ["src/b"],
                "evidence_path": "evidence/b.yaml",
                "stop_condition": "implementation draft complete",
                "focused_checks": ["python check-b.py"],
                "policy_or_lifecycle_decision": False,
            },
        ],
        "combined_checks": ["integration", "traceability", "review", "conflict"],
    }


def test_parallel_plan_allows_only_independent_scopes_with_complete_gates() -> None:
    report = validate_parallel_plan(valid_parallel_plan())
    assert report["status"] == "parallel-safe"
    assert report["diagnostics"] == []


@pytest.mark.parametrize("mutation", ["overlap", "dependency", "evidence", "combined", "decision"])
def test_parallel_plan_serializes_or_blocks_unsafe_work(mutation: str) -> None:
    plan = valid_parallel_plan()
    if mutation == "overlap":
        plan["tasks"][1]["write_scopes"] = ["docs/a/spec.md"]
    elif mutation == "dependency":
        plan["tasks"][1]["dependencies"] = ["TASK-A"]
    elif mutation == "evidence":
        plan["tasks"][1]["evidence_path"] = "evidence/a.yaml"
    elif mutation == "combined":
        plan["combined_checks"].remove("conflict")
    else:
        plan["tasks"][0]["policy_or_lifecycle_decision"] = True
    report = validate_parallel_plan(plan)
    assert report["status"] in {"serialize", "blocked"}
    assert report["diagnostics"]


def test_package_exposes_all_role_instructions_adapters_and_contract_schemas() -> None:
    package = yaml.safe_load((PROCESS / "package.yaml").read_text(encoding="utf-8"))
    schema = json.loads((PROCESS / "schemas/process-package.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(package)) == []
    assert set(package["role_instructions"]) == {"analyst", "developer", "qa", "tech_lead"}
    assert set(package["adapters"]) == {"qwen_class", "deepseek_class", "gigacode_class"}
    assert {"task_launch", "read_pack", "weak_model_operation_evidence", "parallel_plan"} <= set(package["schemas"])


@pytest.mark.parametrize("role", ["analyst", "developer", "qa", "tech-lead"])
def test_role_instructions_are_bounded_and_reference_canonical_contract(role: str) -> None:
    text = (PROCESS / "roles" / f"{role}.md").read_text(encoding="utf-8")
    for marker in ("1.", "Self-review", "Negative examples", "Human stop point", "Canonical references"):
        assert marker in text
    assert "one stage" in text.lower()


@pytest.mark.parametrize("adapter", ["qwen-class", "deepseek-class", "gigacode-class"])
def test_adapter_templates_are_thin_and_cannot_own_process_rules(adapter: str) -> None:
    data = yaml.safe_load((PROCESS / "adapters" / f"{adapter}.yaml").read_text(encoding="utf-8"))
    assert data["inputs"] == ["instruction_path", "read_pack_path"]
    assert data["authority"] == "none"
    assert data["canonical_write"] is False
    assert "policy" not in data and "transition" not in data
