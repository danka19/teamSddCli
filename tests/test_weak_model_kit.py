from __future__ import annotations

import copy
import json
import subprocess
import sys
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
    assert "weak-model" in pack["sources"][0]["content"].lower()
    assert pack["resolver"] == "repository-relative-verified-content"


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
    launch = build_role_launch(ROOT, PROCESS, pack, "scratch/read-pack.json", "evidence/TASK-2.9-ANALYST.yaml")
    assert launch["role"] == "analyst"
    assert launch["instruction_path"] == "roles/analyst.md"
    assert launch["stage_boundary"] == "proposal"
    assert launch["model_authority"] == "advisory-only"
    assert launch["canonical_mutation_allowed"] is False
    assert launch["human_stop_required"] is True
    assert launch["verified_source_manifest"] == [
        {key: source[key] for key in ("authority", "stable_id", "path", "sha256")}
        for source in pack["sources"]
    ]


def test_launcher_blocks_incomplete_read_pack() -> None:
    data = request()
    data["unresolved_inputs"] = ["Product owner must confirm the affected workflow."]
    pack = build_read_pack(ROOT, PROCESS, data)
    assert pack["status"] == "blocked"
    with pytest.raises(ContractError, match="read pack is blocked"):
        build_role_launch(ROOT, PROCESS, pack, "scratch/read-pack.json", "evidence/x.yaml")


def test_launcher_rejects_forged_ready_pack_and_tampered_source() -> None:
    pack = build_read_pack(ROOT, PROCESS, request())
    forged = copy.deepcopy(pack)
    forged["identity"] = "sha256:" + "0" * 64
    with pytest.raises(ContractError, match="identity"):
        build_role_launch(ROOT, PROCESS, forged, "scratch/read-pack.json", "evidence/x.yaml")
    forged = copy.deepcopy(pack)
    forged["sources"][0]["content"] += "forged"
    forged["identity"] = _pack_identity(forged)
    with pytest.raises(ContractError, match="source content hash"):
        build_role_launch(ROOT, PROCESS, forged, "scratch/read-pack.json", "evidence/x.yaml")
    forged = copy.deepcopy(pack)
    forged["sources"][0]["content"] = "fabricated canonical contract\n"
    import hashlib
    forged["sources"][0]["sha256"] = hashlib.sha256(forged["sources"][0]["content"].encode()).hexdigest()
    forged["identity"] = _pack_identity(forged)
    with pytest.raises(ContractError, match="canonical source bytes"):
        build_role_launch(ROOT, PROCESS, forged, "scratch/read-pack.json", "evidence/x.yaml")


def test_recomputed_pack_still_requires_canonical_source_and_evidence_binding() -> None:
    pack = build_read_pack(ROOT, PROCESS, request())
    supporting_only = copy.deepcopy(pack)
    supporting_only["sources"] = [source for source in pack["sources"] if source["authority"] == "supporting"]
    supporting_only["identity"] = _pack_identity(supporting_only)
    with pytest.raises(ContractError, match="canonical source"):
        build_role_launch(ROOT, PROCESS, supporting_only, "scratch/read-pack.json", "evidence/x.yaml")

    evidence, launch, pack = evidence_context()
    supporting = next(source for source in pack["sources"] if source["authority"] == "supporting")
    evidence["artifacts_drafted"][0]["canonical_references"] = [
        {key: supporting[key] for key in ("stable_id", "sha256")}
    ]
    foreign_launch = copy.deepcopy(launch)
    foreign_launch["read_pack_identity"] = "sha256:" + "2" * 64
    foreign_launch["verified_source_manifest"] = foreign_launch["verified_source_manifest"][1:]
    foreign_launch["identity"] = _pack_identity(foreign_launch)
    codes = {item["code"] for item in validate_operation_evidence(evidence, foreign_launch, pack)}
    assert {"evidence.invalid-launch-binding", "evidence.missing-canonical-reference"} <= codes


def test_read_pack_request_rejects_empty_or_unbounded_context() -> None:
    data = request()
    data["sources"] = []
    assert build_read_pack(ROOT, PROCESS, data)["status"] == "blocked"
    data = request()
    data["sources"][0]["sections"] = ["missing heading"]
    assert build_read_pack(ROOT, PROCESS, data)["status"] == "blocked"
    data = request()
    data["sources"] = [data["sources"][1]]
    assert build_read_pack(ROOT, PROCESS, data)["status"] == "blocked"


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
        "claims": [{"kind": "validation", "value": {"subject": "change-schema", "summary": "check passed"}, "evidence": "log:check-1"}],
        "human_decisions_required": ["Product owner accepts proposal"],
        "unresolved_inputs": [],
        "residual_limitations": ["No model certification performed"],
        "prohibited_actions_attempted": [],
        "human_stop_reached": True,
        "human_review_status": "pending",
        "lifecycle_transition_requested": False,
        "approval_claimed": False,
    }


def evidence_context() -> tuple[dict, dict]:
    pack = build_read_pack(ROOT, PROCESS, request())
    launch = build_role_launch(ROOT, PROCESS, pack, "scratch/read-pack.json", "evidence/TASK.yaml")
    evidence = valid_evidence()
    evidence["read_pack_identity"] = pack["identity"]
    evidence["sources_read"] = [
        {key: source[key] for key in ("authority", "stable_id", "path", "sha256")}
        for source in pack["sources"]
    ]
    evidence["artifacts_drafted"][0]["canonical_references"] = [
        {key: pack["sources"][0][key] for key in ("stable_id", "sha256")}
    ]
    return evidence, launch, pack


def _pack_identity(pack: dict) -> str:
    import hashlib

    payload = {key: value for key, value in pack.items() if key != "identity"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def test_operation_evidence_accepts_supported_advisory_completion() -> None:
    evidence, launch, pack = evidence_context()
    assert validate_operation_evidence(evidence, launch, pack) == []


@pytest.mark.parametrize(
    ("change", "code"),
    [
        ({"approval_claimed": True}, "evidence.schema"),
        ({"lifecycle_transition_requested": True}, "evidence.schema"),
        ({"status": "approved"}, "evidence.schema"),
        ({"checks": [], "claims": [{"kind": "validation", "value": {"subject": "schema", "summary": "passed"}, "evidence": "log:missing"}]}, "evidence.unsupported-claim"),
    ],
)
def test_operation_evidence_rejects_authority_and_unsupported_claims(change: dict, code: str) -> None:
    evidence, launch, pack = evidence_context()
    evidence.update(change)
    assert code in {item["code"] for item in validate_operation_evidence(evidence, launch, pack)}


def test_operation_evidence_rejects_derived_canonical_artifact_without_source_reference() -> None:
    evidence, launch, pack = evidence_context()
    evidence["artifacts_drafted"][0] = {"path": "openspec/spec.md", "canonical": True, "canonical_references": []}
    codes = {item["code"] for item in validate_operation_evidence(evidence, launch, pack)}
    assert codes == {"evidence.schema"}


def test_evidence_rejects_lie_in_claims_forbidden_actions_or_wrong_launch_binding() -> None:
    evidence, launch, pack = evidence_context()
    evidence["claims"].append({"kind": "fact", "value": {"subject": "change", "summary": "approved"}, "evidence": "log:check-1"})
    evidence["prohibited_actions_attempted"] = ["archive"]
    evidence["task_id"] = "OTHER"
    codes = {item["code"] for item in validate_operation_evidence(evidence, launch, pack)}
    assert {"evidence.forbidden-authority", "evidence.prohibited-action", "evidence.launch-mismatch"} <= codes


def test_claims_use_closed_safe_kinds_and_reject_decision_semantics_in_values() -> None:
    evidence, launch, pack = evidence_context()
    evidence["claims"] = [
        {"kind": "fact", "value": {"subject": "review", "summary": "waiver approved and transition authorized"}, "evidence": "log:check-1"},
    ]
    codes = {item["code"] for item in validate_operation_evidence(evidence, launch, pack)}
    assert "evidence.forbidden-authority" in codes

    evidence["claims"][0]["kind"] = "decision"
    assert {item["code"] for item in validate_operation_evidence(evidence, launch, pack)} == {"evidence.schema"}


def test_evidence_rejects_unverified_source_reference_even_when_id_matches() -> None:
    evidence, launch, pack = evidence_context()
    evidence["sources_read"][0]["sha256"] = "0" * 64
    codes = {item["code"] for item in validate_operation_evidence(evidence, launch, pack)}
    assert "evidence.unverified-source" in codes


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
                "focused_checks": [{"check_id": "focused-a", "command": "python check-a.py"}],
                "policy_or_lifecycle_decision": False,
            },
            {
                "task_id": "TASK-B",
                "owner": "developer-1",
                "dependencies": [],
                "write_scopes": ["src/b"],
                "evidence_path": "evidence/b.yaml",
                "stop_condition": "implementation draft complete",
                "focused_checks": [{"check_id": "focused-b", "command": "python check-b.py"}],
                "policy_or_lifecycle_decision": False,
            },
        ],
        "combined_checks": [
            {"check_id": kind, "kind": kind, "command": f"python check-{kind}.py"}
            for kind in ("integration", "traceability", "review", "conflict")
        ],
        "promotion_requested": False,
        "promotion_evidence": None,
    }


def test_parallel_plan_allows_only_independent_scopes_with_complete_gates() -> None:
    report = validate_parallel_plan(valid_parallel_plan())
    assert report["status"] == "parallel-safe"
    assert report["diagnostics"] == []
    assert report["promotion_allowed"] is False


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
        plan["combined_checks"] = [row for row in plan["combined_checks"] if row["kind"] != "conflict"]
    else:
        plan["tasks"][0]["policy_or_lifecycle_decision"] = True
    report = validate_parallel_plan(plan)
    assert report["status"] in {"serialize", "blocked"}
    assert report["diagnostics"]


def test_parallel_plan_rejects_duplicate_ids_windows_equivalent_paths_and_promotion_without_results() -> None:
    plan = valid_parallel_plan()
    plan["tasks"][1]["task_id"] = "TASK-A"
    plan["tasks"][1]["write_scopes"] = ["DOCS\\A\\child"]
    plan["tasks"][1]["evidence_path"] = "evidence\\a.yaml"
    plan["promotion_requested"] = True
    report = validate_parallel_plan(plan)
    codes = {item["code"] for item in report["diagnostics"]}
    assert {"parallel.duplicate-task-id", "parallel.overlapping-scope", "parallel.shared-evidence", "parallel.missing-promotion-evidence"} <= codes
    assert report["promotion_allowed"] is False


def test_parallel_rejects_drive_unc_paths_and_reused_check_or_result_ids() -> None:
    plan = valid_parallel_plan()
    plan["tasks"][0]["write_scopes"] = ["C:\\repo\\src"]
    plan["tasks"][1]["evidence_path"] = "\\\\server\\share\\evidence.yaml"
    plan["tasks"][1]["focused_checks"][0]["check_id"] = "focused-a"
    plan["combined_checks"][1]["check_id"] = plan["combined_checks"][0]["check_id"]
    plan["promotion_requested"] = True
    plan["promotion_evidence"] = {
        "task_results": [
            {"task_id": "TASK-A", "checks": [{"check_id": "focused-a", "result": "passed", "evidence": "log:a"}]},
            {"task_id": "TASK-B", "checks": [{"check_id": "focused-a", "result": "passed", "evidence": "log:a"}]},
        ],
        "combined_results": [
            {"check_id": "integration", "result": "passed", "evidence": "log:one"}
        ],
    }
    codes = {item["code"] for item in validate_parallel_plan(plan)["diagnostics"]}
    assert {"parallel.unsafe-scope", "parallel.unsafe-evidence-path", "parallel.duplicate-check-id", "parallel.reused-result"} <= codes


def test_parallel_promotion_requires_each_focused_and_combined_pass_evidence() -> None:
    plan = valid_parallel_plan()
    plan["promotion_requested"] = True
    plan["promotion_evidence"] = {
        "task_results": [
            {"task_id": task["task_id"], "checks": [{"check_id": task["focused_checks"][0]["check_id"], "result": "passed", "evidence": f"log:{task['task_id']}"}]}
            for task in plan["tasks"]
        ],
        "combined_results": [
            {"check_id": row["check_id"], "result": "passed", "evidence": f"log:{row['kind']}"}
            for row in plan["combined_checks"]
        ],
    }
    assert validate_parallel_plan(plan)["promotion_allowed"] is True
    plan["promotion_evidence"]["combined_results"][0]["result"] = "failed"
    assert validate_parallel_plan(plan)["promotion_allowed"] is False


def test_parallel_promotion_rejects_extra_or_duplicate_result_rows() -> None:
    plan = valid_parallel_plan()
    plan["promotion_requested"] = True
    plan["promotion_evidence"] = {
        "task_results": [
            {"task_id": task["task_id"], "checks": [{"check_id": task["focused_checks"][0]["check_id"], "result": "passed", "evidence": f"log:{task['task_id']}"}]}
            for task in plan["tasks"]
        ],
        "combined_results": [
            {"check_id": row["check_id"], "result": "passed", "evidence": f"log:{row['kind']}"}
            for row in plan["combined_checks"]
        ],
    }
    plan["promotion_evidence"]["task_results"].append(copy.deepcopy(plan["promotion_evidence"]["task_results"][0]))
    plan["promotion_evidence"]["combined_results"].append(
        {"check_id": "undeclared", "result": "passed", "evidence": "log:undeclared"}
    )
    report = validate_parallel_plan(plan)
    assert "parallel.reused-result" in {item["code"] for item in report["diagnostics"]}
    assert report["promotion_allowed"] is False


def test_package_exposes_all_role_instructions_adapters_and_contract_schemas() -> None:
    package = yaml.safe_load((PROCESS / "package.yaml").read_text(encoding="utf-8"))
    schema = json.loads((PROCESS / "schemas/process-package.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(package)) == []
    assert set(package["role_instructions"]) == {"analyst", "developer", "qa", "tech_lead"}
    assert set(package["adapters"]) == {"qwen_class", "deepseek_class", "gigacode_class"}
    assert {"read_pack_request", "task_launch", "read_pack", "weak_model_operation_evidence", "parallel_plan"} <= set(package["schemas"])


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


def test_clis_reject_malformed_nested_documents_without_traceback_from_other_cwd(tmp_path: Path) -> None:
    malformed = tmp_path / "malformed.yaml"
    malformed.write_text("schema_version: '1.0'\ntask_id: x\nsources: [{authority: canonical, extra: secret}]\n", encoding="utf-8")
    for script, extra in (
        ("build_read_pack.py", []),
        ("check_parallel_plan.py", []),
    ):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), str(malformed), *extra],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode in {2, 3}
        assert "Traceback" not in result.stderr + result.stdout
        assert "secret" not in result.stdout


def test_schema_failure_stops_semantics_and_evidence_parallel_clis_exit_three(tmp_path: Path) -> None:
    evidence, launch, pack = evidence_context()
    evidence["claims"] = ["not-a-mapping"]
    diagnostics = validate_operation_evidence(evidence, launch, pack)
    assert {item["code"] for item in diagnostics} == {"evidence.schema"}
    plan = valid_parallel_plan()
    plan["tasks"][0]["focused_checks"] = ["not-a-mapping"]
    report = validate_parallel_plan(plan)
    assert {item["code"] for item in report["diagnostics"]} == {"parallel.schema"}

    evidence_path = tmp_path / "evidence.json"
    launch_path = tmp_path / "launch.json"
    pack_path = tmp_path / "pack.json"
    plan_path = tmp_path / "plan.json"
    for path, value in ((evidence_path, evidence), (launch_path, launch), (pack_path, pack), (plan_path, plan)):
        path.write_text(json.dumps(value), encoding="utf-8")
    commands = [
        [sys.executable, str(ROOT / "scripts/check_weak_model_evidence.py"), str(evidence_path), "--launch", str(launch_path), "--read-pack", str(pack_path)],
        [sys.executable, str(ROOT / "scripts/check_parallel_plan.py"), str(plan_path)],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, check=False)
        assert result.returncode == 3
        assert "Traceback" not in result.stdout + result.stderr


def test_evidence_stops_before_semantics_when_launch_or_pack_schema_is_invalid(tmp_path: Path) -> None:
    evidence, launch, pack = evidence_context()
    malformed_launch = copy.deepcopy(launch)
    malformed_launch["verified_source_manifest"] = ["private-launch-value"]
    malformed_pack = copy.deepcopy(pack)
    malformed_pack["sources"] = ["private-pack-value"]

    launch_diagnostics = validate_operation_evidence(evidence, malformed_launch, pack)
    pack_diagnostics = validate_operation_evidence(evidence, launch, malformed_pack)
    assert {item["code"] for item in launch_diagnostics} == {"evidence.invalid-launch"}
    assert {item["code"] for item in pack_diagnostics} == {"evidence.invalid-read-pack"}

    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    for label, launch_value, pack_value in (
        ("launch", malformed_launch, pack),
        ("pack", launch, malformed_pack),
    ):
        launch_path = tmp_path / f"{label}-launch.json"
        pack_path = tmp_path / f"{label}-pack.json"
        launch_path.write_text(json.dumps(launch_value), encoding="utf-8")
        pack_path.write_text(json.dumps(pack_value), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_weak_model_evidence.py"), str(evidence_path), "--launch", str(launch_path), "--read-pack", str(pack_path)],
            cwd=tmp_path, capture_output=True, text=True, check=False,
        )
        assert result.returncode == 3
        assert "Traceback" not in result.stdout + result.stderr
        assert "private-" not in result.stdout


def test_launch_and_evidence_clis_bind_concrete_documents_with_stable_errors(tmp_path: Path) -> None:
    pack = build_read_pack(ROOT, PROCESS, request())
    pack_path = tmp_path / "read-pack.json"
    pack_path.write_text(json.dumps(pack), encoding="utf-8")
    relative_pack = pack_path.resolve().relative_to(ROOT.resolve()).as_posix()
    launch = build_role_launch(ROOT, PROCESS, pack, relative_pack, "evidence/TASK.yaml")
    launch_path = tmp_path / "launch.json"
    launch_path.write_text(json.dumps(launch), encoding="utf-8")
    evidence, _, _ = evidence_context()
    evidence_path = tmp_path / "evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_weak_model_evidence.py"), str(evidence_path), "--launch", str(launch_path), "--read-pack", str(pack_path)],
        cwd=tmp_path, capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["status"] == "accepted-draft"

    malformed = tmp_path / "secret-malformed.yaml"
    malformed.write_text("schema_version: '1.0'\nextra: secret-value\n", encoding="utf-8")
    for script, args in (
        ("launch_role_task.py", [str(malformed), "--repository-root", str(ROOT), "--evidence", "evidence/x.yaml"]),
        ("check_weak_model_evidence.py", [str(malformed), "--launch", str(malformed), "--read-pack", str(malformed)]),
    ):
        failed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *args], cwd=tmp_path,
            capture_output=True, text=True, check=False,
        )
        assert failed.returncode in {2, 3}
        assert "Traceback" not in failed.stdout + failed.stderr
        assert "secret-value" not in failed.stdout


@pytest.mark.parametrize(
    "script",
    ["build_read_pack.py", "launch_role_task.py", "check_weak_model_evidence.py", "check_parallel_plan.py"],
)
def test_weak_model_clis_have_stable_redacted_usage_exit(script: str, tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script)], cwd=tmp_path,
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["status"] == "usage" or payload["status"] == "blocked"
    assert "Traceback" not in result.stderr + result.stdout
