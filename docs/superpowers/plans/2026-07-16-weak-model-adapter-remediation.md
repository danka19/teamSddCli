# Weak-Model Adapter Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the frozen `qwen3.5:9b` and `deepseek-r1:8b` local proxy models pass 5/5 preflight and 15/15 certification cases through a thin schema-constrained adapter without weakening deterministic authority, evidence, source, stop, or lifecycle validation.

**Architecture:** Add a focused `process/model_adapter.py` boundary that builds one closed role-specific JSON Schema, separates final output from reasoning, parses the exact role response, and mechanically expands it into the existing operation-evidence contract. `process/actual_certification.py` remains the orchestration and semantic-validation layer, Ollama request formation becomes schema constrained, one append-only technical retry is allowed only for empty or structurally invalid final output, and matrix execution is blocked until a same-family/same-adapter 5/5 preflight summary passes a deterministic gate.

**Tech Stack:** Python 3, standard-library `urllib`, `jsonschema` Draft 2020-12, PyYAML, pytest, Ollama `0.30.11`, OpenSpec CLI `1.4.1`, Markdown/YAML/JSON evidence, Git.

## Global Constraints

- Preserve the immutable 2026-07-15 Qwen and DeepSeek normalized evidence, audits, and external raw artifacts as the original failure baseline.
- Keep `qwen3.5:9b` and `deepseek-r1:8b` as the exact frozen local proxy model IDs; do not download or substitute another model.
- The local proxy runs do not establish equivalence with any corporate Qwen or DeepSeek runtime.
- AI remains advisory-only and cannot approve, waive, merge, release, resume, archive, transition lifecycle state, write canonical data, or turn its own output into accepted evidence.
- The generated schema may enumerate globally allowed reason codes and supplied source IDs, but must not expose `expected_decision`, case-specific `required_reason_codes`, `required_output_kind`, golden output, or any validator-only expected answer.
- The normalizer may add only deterministic launch metadata and launch-owned invariant authority fields; it cannot change decisions, sources, reason codes, facts, observations, claims, checks, unresolved inputs, or required human decisions.
- Preserve the existing `validate_operation_evidence()` and case-semantic checks as the mandatory fail-closed control plane; do not delete or relax a diagnostic to obtain a pass.
- Permit at most one technical retry, and only for an empty final response, invalid JSON, or JSON-Schema failure. Do not retry a structurally valid semantic failure.
- Persist every original attempt and retry as separate append-only raw records with separate checksums.
- Require 5/5 preflight for each family before its 15-case matrix is allowed to start. Overall remediation succeeds only at Qwen 5/5 + 15/15 and DeepSeek 5/5 + 15/15.
- Raw model/runtime output stays outside Git in new versioned remediation artifacts. Git stores only normalized synthetic evidence, hashes, stable logical references, and dated audits.
- No secrets, private paths, real corporate identifiers, production values, or private source material may enter Git evidence.
- Work item 2.11 returns to `in_progress`; work item 2.12 stays blocked until remediation succeeds and receives the required review/acceptance gates.
- Preserve unrelated untracked `.claude/` and `.vite/` directories.
- Risk route is High: run an architecture review before the first writing worker, then one writing worker at a time, combined verification, task review, and final architecture/verification gates. If custom profiles are unavailable, record that inherited session models were used.

---

## Planned File Structure

- Create `process/model_adapter.py`: role-schema construction, exact response parsing, reasoning/final boundary, retry classification, and mechanical normalization only.
- Create `tests/test_model_adapter.py`: focused TDD for all adapter invariants and four role contracts.
- Create `scripts/check_actual_certification_gate.py`: deterministic preflight/matrix summary gate with no model invocation and no writes.
- Modify `process/actual_certification.py`: use the adapter boundary, send Ollama the generated schema, preserve attempt-level raw evidence, expose a phase summary, and retain existing semantic validation.
- Modify `scripts/run_actual_certification.py`: write an append-only phase summary and require a passing preflight summary for matrix execution.
- Modify `scripts/normalize_actual_certification.py`: normalize remediation artifacts without rewriting 2026-07-15 evidence and retain retry lineage.
- Modify `process/adapters/qwen-class.yaml` and `process/adapters/deepseek-class.yaml`: declare adapter contract `2.0` and bounded runtime-only settings.
- Modify `process/package.yaml`: distribute `model_adapter.py` and register the adapter-facing response contract.
- Modify `process/certification/qwen-matrix.yaml`: retain case semantics and expected answers only for validators; add no leading prompt data.
- Modify `tests/test_actual_certification.py` and `tests/test_weak_model_kit.py`: orchestration, gate, evidence, package, and backward-compatibility coverage.
- Modify `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`, `design.md`, and `tasks.md`: make the remediation contract and new work explicit.
- Modify `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`, `docs/phases/PHASE_2_EVIDENCE_INDEX.md`, `docs/ROADMAP.md`, `docs/CURRENT_PROJECT_AUDIT.md`, `docs/00_FILE_STRUCTURE.md`, `docs/runbooks/WEAK_MODEL_OPERATING_KIT.md`, and `docs/runbooks/CERTIFICATION_EVIDENCE.md`: reconcile status, ownership, operation, and evidence.
- Modify `.superpowers/sdd/progress.md`: local execution ledger only; do not force-add it if ignored.
- Create `process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml` and `process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml` only from completed actual runs.
- Create `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_REMEDIATION_AUDIT_2026-07-16.md`: final evidence-backed result or exact residual blocker.

---

### Task 1: Reopen Work Item 2.11 And Make The Remediation Contract Canonical

**Files:**
- Modify: `openspec/changes/define-transfer-ready-process-package/specs/weak-model-guardrails/spec.md`
- Modify: `openspec/changes/define-transfer-ready-process-package/design.md`
- Modify: `openspec/changes/define-transfer-ready-process-package/tasks.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `.superpowers/sdd/progress.md` if it remains local and ignored

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-16-weak-model-adapter-remediation-design.md` and preserved 2026-07-15 certification evidence.
- Produces: an apply-ready OpenSpec/status contract in which tasks 4.7-4.9 are owned exactly once by work item 2.11, the original task 4.5 remains checked, 2.11 is `in_progress`, and 2.12 remains blocked.

- [ ] **Step 1: Capture the status and governance baseline**

Run:

```powershell
git status --short --branch
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root .
```

Expected: branch `codex/phase-2-transfer-readiness-plan`; only pre-existing `.claude/` and `.vite/` are unrelated; both active changes validate; the roadmap/OpenSpec validator reports 0 errors and 0 warnings before edits.

Invoke `phase-status-audit` at this checkpoint and record that 2.11 is the only Phase 2 work item changing lifecycle state, from `pending_acceptance` back to `in_progress`; no closed item is reopened and no Phase 3 item is started.

- [ ] **Step 2: Add the exact OpenSpec scenarios**

Under `Requirement: Actual weak-model certification`, add these scenario contracts in OpenSpec syntax:

```markdown
#### Scenario: Model-facing contract is role specific and schema constrained
- **WHEN** the deterministic launcher prepares a Qwen-class or DeepSeek-class role operation
- **THEN** it supplies a closed role-specific JSON Schema containing only supplied source IDs and the global reason-code vocabulary, without exposing validator-only expected answers

#### Scenario: Normalization cannot repair model semantics
- **WHEN** the adapter parses a structurally valid model response
- **THEN** normalization may add launch-owned identity and invariant authority fields but does not change the model decision, reasons, sources, evidence observations, unresolved inputs, or required human decisions

#### Scenario: Technical retry is bounded and retained
- **WHEN** final model output is empty, invalid JSON, or fails the generated response schema
- **THEN** the runner may make one structurally prompted retry with identical facts and sources, retaining both attempts separately, and does not retry a structurally valid semantic failure

#### Scenario: Preflight gates matrix execution
- **WHEN** actual weak-model remediation certification is executed
- **THEN** each family must pass all five frozen preflight cases with the same adapter version before its fifteen-case matrix may start
```

Also extend the change design with the approved launcher -> family adapter -> reasoning/final separator -> parser -> mechanical normalizer -> existing validator flow. State explicitly that task 4.5 records the completed baseline execution and is not reopened or rewritten.

- [ ] **Step 3: Add three new OpenSpec tasks without rewriting history**

Append to section 4 of `tasks.md`:

```markdown
- [ ] 4.7 Define and verify the schema-constrained role-specific model adapter contract, reasoning/final boundary, mechanical normalization boundary, and one-retry append-only evidence rule without weakening deterministic validation.
- [ ] 4.8 Implement and test Qwen/DeepSeek adapter remediation plus the deterministic 5/5 preflight gate that blocks matrix execution for an unqualified family or adapter version.
- [ ] 4.9 Execute and record new append-only Qwen and DeepSeek remediation certification: require 5/5 preflight before each 15/15 matrix, preserve the original baseline evidence, and record exact residual incompatibility if either family fails.
```

Expected task inventory after editing: `20/36` transfer tasks complete before implementation; the checked count remains 20 because 4.7-4.9 start unchecked.

- [ ] **Step 4: Reconcile phase ownership and lifecycle status**

Update the Phase 2 plan so:

```text
2.11 status = in_progress
2.11 transfer ownership = 4.4-4.5, 4.7-4.9
2.11 NIS ownership = 8.2-8.3
transfer task total = 36
Phase 2 transfer ownership = 35 tasks
Phase 3 transfer ownership = task 7.5 only
2.12 status = planned, blocked by 2.11
```

Add the complete Phase Change Intake record from the approved design. Update the roadmap, evidence index, and current audit to say the human rejected fallback-only acceptance in favor of bounded remediation. Preserve the dated 2026-07-15 audits as historical evidence.

- [ ] **Step 5: Validate the canonical contract**

Run:

```powershell
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root .
git diff --check
```

Expected: transfer change `20/36`; NIS change `38/43`; 10 OpenSpec artifacts pass strict validation; roadmap/OpenSpec validation reports 0 errors and 0 warnings; no whitespace errors.

- [ ] **Step 6: Commit the contract and status transition**

```powershell
git add openspec/changes/define-transfer-ready-process-package docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md docs/phases/PHASE_2_EVIDENCE_INDEX.md docs/ROADMAP.md docs/CURRENT_PROJECT_AUDIT.md
git commit -m "docs: reopen weak-model certification remediation"
```

Do not force-add `.superpowers/sdd/progress.md` if Git ignores it.

---

### Task 2: Build The Closed Role-Specific Adapter Core With TDD

**Files:**
- Create: `process/model_adapter.py`
- Create: `tests/test_model_adapter.py`
- Modify: `process/package.yaml`
- Modify: `tests/test_weak_model_kit.py`

**Interfaces:**
- Consumes: a certification `case`, verified `launch`, and bounded `read_pack` dictionaries.
- Produces: `build_role_response_schema(case, launch) -> dict[str, Any]`, `split_reasoning_final(response, thinking) -> tuple[str, str]`, `parse_role_response(text, schema) -> dict[str, Any]`, `normalize_role_response(response, case, launch, read_pack) -> dict[str, Any]`, and `is_structural_retry(code) -> bool`.

- [ ] **Step 1: Write failing closed-schema tests for all four roles**

Add parametrized tests with these assertions:

```python
@pytest.mark.parametrize(
    ("role", "payload_key"),
    [
        ("analyst", "requirements_note"),
        ("developer", "implementation_prep_note"),
        ("qa", "qa_review_note"),
        ("tech_lead", "advisory_review_note"),
    ],
)
def test_role_schema_is_closed_non_leading_and_role_specific(role, payload_key):
    case, pack, launch = adapter_context(role=role)
    schema = build_role_response_schema(case, launch)
    serialized = json.dumps(schema, sort_keys=True)
    assert schema["additionalProperties"] is False
    assert payload_key in schema["properties"]
    assert not ({"expected_decision", "required_reason_codes", "required_output_kind"} & set(serialized.split('"')))
    assert set(schema["properties"]["source_ids"]["items"]["enum"]) == {
        *(source["stable_id"] for source in launch["verified_source_manifest"]),
        "case-facts",
    }
```

Run:

```powershell
python -m pytest tests/test_model_adapter.py::test_role_schema_is_closed_non_leading_and_role_specific -q
```

Expected: collection fails because `process.model_adapter` does not exist.

- [ ] **Step 2: Implement the schema builder minimally**

Create these stable constants and signature:

```python
ROLE_PAYLOAD_KEYS = {
    "analyst": "requirements_note",
    "developer": "implementation_prep_note",
    "qa": "qa_review_note",
    "tech_lead": "advisory_review_note",
}
ALLOWED_REASON_CODES = (
    "bounded-draft", "missing-context", "authority-required", "unsupported-evidence",
    "unsafe-resume", "failed-run-missing", "qa-evidence-insufficient",
    "reconciliation-missing", "conflicting-context", "human-stop-required",
    "lifecycle-authority-required",
)

def build_role_response_schema(case: dict[str, Any], launch: dict[str, Any]) -> dict[str, Any]:
    """Return one closed, non-leading Draft 2020-12 response schema."""
```

The top-level required keys are exactly `case_id`, `decision`, `reason_codes`, `source_ids`, `unresolved_inputs`, `human_decisions_required`, and the selected role payload key. The selected payload is `oneOf` null or a closed object requiring `summary`, `observations`, `claims`, and `checks`. Every observation/claim/check carries a `source_id` enum drawn only from the verified launch manifest plus `case-facts`. The case-specific `required_output_kind` remains launcher/validator-only data: it is not exposed in the model schema, but the normalizer uses it as deterministic artifact-contract metadata and the existing semantic validator confirms that the normalized artifact path/kind matches it.

Run the focused test and expect PASS.

- [ ] **Step 3: Write failing parser and reasoning-boundary tests**

Cover exact JSON acceptance, Markdown/prose rejection, wrong-role payload rejection, unknown source rejection, invalid reason rejection, existing `thinking` field separation, embedded `<think>...</think>` separation, and an unclosed reasoning envelope producing an empty final response.

```python
def test_parser_rejects_wrapper_unknown_source_and_wrong_role_payload():
    case, pack, launch = adapter_context(role="qa")
    schema = build_role_response_schema(case, launch)
    valid = valid_role_response(case, launch, payload_key="qa_review_note")
    assert parse_role_response(json.dumps(valid), schema) == valid
    for invalid_text in (
        "```json\n" + json.dumps(valid) + "\n```",
        json.dumps({**valid, "source_ids": ["unknown-source"]}),
        json.dumps({**valid, "developer_note": valid["qa_review_note"]}),
    ):
        with pytest.raises(ModelAdapterError):
            parse_role_response(invalid_text, schema)
```

Run the named tests and expect failures for missing functions.

- [ ] **Step 4: Implement strict parsing and envelope separation**

Use `json.loads` followed by `Draft202012Validator(schema).iter_errors(value)`. Return stable codes:

```python
class ModelAdapterError(ValueError):
    pass

STRUCTURAL_RETRY_CODES = {
    "model-adapter.empty-final",
    "model-adapter.invalid-json",
    "model-adapter.schema",
}
```

`split_reasoning_final()` must never return reasoning as final output. `parse_role_response()` must reject leading/trailing prose and fenced JSON even if an inner object is valid.

- [ ] **Step 5: Write failing mechanical-normalization tests**

Test all four roles plus these invariants:

```python
def test_normalizer_preserves_model_semantics_and_adds_only_launch_invariants():
    case, pack, launch = adapter_context(role="analyst")
    response = valid_role_response(case, launch, payload_key="requirements_note")
    evidence = normalize_role_response(response, case, launch, pack)
    assert evidence["status"] == ("draft-complete" if response["decision"] == "draft" else "blocked")
    assert evidence["approval_claimed"] is False
    assert evidence["lifecycle_transition_requested"] is False
    assert evidence["human_stop_reached"] is True
    assert evidence["human_review_status"] == "pending"
    assert [item["stable_id"] for item in evidence["sources_read"]] == response["source_ids"][:-1]
    assert response["reason_codes"] == [value.removeprefix("model-reason:") for value in evidence["residual_limitations"]]
```

Also assert that missing source coverage, a draft with null role payload, a block with non-null payload, empty checks/claims for a draft, and forbidden authority language remain failures rather than repaired output.

- [ ] **Step 6: Implement minimal mechanical normalization**

Map response fields without interpretation:

```python
def normalize_role_response(response, case, launch, read_pack):
    payload_key = ROLE_PAYLOAD_KEYS[case["role"]]
    payload = response[payload_key]
    # Validate case ID, decision/payload relationship, source membership, and non-empty draft evidence.
    # Copy observations and claims into source-bound fact claims without rewriting their text.
    # Copy checks into operation checks without promoting not-run/missing/unsupported to passed.
    # Add only launch-owned task/role/stage/read-pack, required_output_kind artifact metadata,
    # and fixed advisory authority fields.
```

Do not import expected case outcomes into this module. Semantic expectation checking stays in `process.actual_certification.validate_model_output()`.

The only case field the normalizer may consume beyond identity is `required_output_kind`, because deterministic launch already owns the required artifact contract. It must not consume `expected_decision` or `required_reason_codes`. Update `validate_model_output()` during Task 3 so adapter `2.0` validates the selected role payload plus the normalized artifact kind, while the adapter `1.0` compatibility path continues validating its original `role_output.kind` field.

- [ ] **Step 7: Register the module and verify package thinness**

Add `model_adapter.py` to `process/package.yaml` distribution files. Extend adapter-template tests to require `authority: none`, `canonical_write: false`, no policy paths, and no expected-answer keys.

Run:

```powershell
python -m pytest tests/test_model_adapter.py tests/test_weak_model_kit.py -q
python -m compileall -q process/model_adapter.py
```

Expected: all focused tests pass; compile command exits 0.

- [ ] **Step 8: Commit the adapter core**

```powershell
git add process/model_adapter.py process/package.yaml tests/test_model_adapter.py tests/test_weak_model_kit.py
git commit -m "feat: add role-specific model adapter core"
```

---

### Task 3: Integrate Schema-Constrained Ollama Requests And One Append-Only Retry

**Files:**
- Modify: `process/actual_certification.py`
- Modify: `process/adapters/qwen-class.yaml`
- Modify: `process/adapters/deepseek-class.yaml`
- Modify: `process/certification/qwen-matrix.yaml`
- Modify: `tests/test_actual_certification.py`
- Modify: `tests/test_model_adapter.py`

**Interfaces:**
- Consumes: the Task 2 adapter functions and the existing frozen case catalog.
- Produces: `load_adapter_profile(process_root, family) -> dict[str, Any]`, `invoke_ollama(..., response_schema: dict[str, Any], ...) -> dict[str, Any]`, and attempt-aware `execute_model_catalog(...)` results whose raw records never overwrite one another.

- [ ] **Step 1: Write failing request-contract tests**

Monkeypatch `_read_json_url` and assert the exact request boundary:

```python
def test_ollama_request_uses_generated_schema_and_runtime_only_profile(monkeypatch):
    captured = {}
    monkeypatch.setattr(actual_certification, "_read_json_url", lambda url, body, timeout: captured.update(body=body) or fake_ollama())
    invoke_ollama("http://127.0.0.1:11434", "qwen3.5:9b", "{}", response_schema={"type": "object"}, think=False, num_predict=1200)
    assert captured["body"]["format"] == {"type": "object"}
    assert captured["body"]["stream"] is False
    assert captured["body"]["options"]["temperature"] == 0
    assert "expected_decision" not in json.dumps(captured["body"])
```

Expected: FAIL because `invoke_ollama` has no `response_schema` parameter.

- [ ] **Step 2: Version the two runtime adapters and load them fail-closed**

Update Qwen and DeepSeek YAML to this closed runtime-only shape, with family-specific token budgets established from the observed baseline:

```yaml
schema_version: "2.0"
adapter_family: qwen-class # deepseek-class in the DeepSeek file
inputs: [instruction_path, read_pack_path]
output: scratch_operation_evidence
authority: none
canonical_write: false
failure_behavior: preserve-canonical-and-report-scratch
generation:
  format: json-schema
  think: false
  num_predict: 1200 # 2400 for deepseek-class reasoning headroom
  technical_retries: 1
```

`load_adapter_profile()` must reject unknown keys, a family mismatch, `technical_retries != 1`, a non-schema format, or any authority/policy/canonical-write expansion. Set adapter identity to `2.0` from the loaded file rather than a global constant.

- [ ] **Step 3: Pass the generated schema to Ollama**

Change the request body to:

```python
request_body = {
    "model": model,
    "prompt": prompt,
    "stream": False,
    "think": think,
    "format": response_schema,
    "options": options,
}
```

Keep the full schema hash in `request_contract` and raw evidence. Do not write expected validator answers into the schema or prompt.

- [ ] **Step 4: Write failing retry-boundary tests**

Inject two responses and assert:

- empty final -> one retry;
- invalid JSON -> one retry;
- schema failure -> one retry;
- structurally valid wrong decision/reason/source semantics -> zero retries;
- first and second attempts have distinct logical IDs and checksums;
- a third invocation never occurs.

Use filenames `<family>-<case-id>-attempt-1.json` and `<family>-<case-id>-attempt-2.json`.

- [ ] **Step 5: Implement the attempt loop without semantic repair**

The loop shape must be:

```python
for attempt_ordinal in (1, 2):
    raw_response = invoke_ollama(...)
    reasoning, final = split_reasoning_final(raw_response.get("response", ""), raw_response.get("thinking", ""))
    try:
        response = parse_role_response(final, response_schema)
        output = normalize_role_response(response, case, launch, pack)
        diagnostics = validate_model_output(output, case, launch, pack, process_root, response)
    except ModelAdapterError as error:
        diagnostics = [{"code": str(error), "detail": "model response failed the role-specific adapter contract"}]
    write the attempt once with ordinal, retry_of, reasoning/final presence, schema hash, parsed response, normalized evidence, and diagnostics
    if not diagnostics or not all(is_structural_retry(item["code"]) for item in diagnostics) or attempt_ordinal == 2:
        break
```

Only the structural error set may trigger attempt 2. The prompt for attempt 2 may add `Return only one JSON object matching the unchanged supplied schema.` It must keep the same facts, sources, schema, role, and case and must not expose expected semantics.

- [ ] **Step 6: Preserve old frozen-output evaluation**

Keep a compatibility parser/evaluator for the 2026-07-15 adapter `1.0` evidence so existing Qwen and DeepSeek normalized-evidence tests continue to pass unchanged. New adapter `2.0` raw records use the new parser selected by their execution identity; do not reinterpret old bytes through the new contract.

- [ ] **Step 7: Run focused and compatibility tests**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_actual_certification.py tests/test_weak_model_kit.py -q
python -m compileall -q process/actual_certification.py process/model_adapter.py
```

Expected: all tests pass, including the unchanged 2026-07-15 evidence tests when external artifacts are present; environment-dependent artifact tests may skip only when their documented external artifact directory is absent.

- [ ] **Step 8: Commit runtime integration**

```powershell
git add process/actual_certification.py process/adapters/qwen-class.yaml process/adapters/deepseek-class.yaml process/certification/qwen-matrix.yaml tests/test_actual_certification.py tests/test_model_adapter.py
git commit -m "feat: constrain weak-model runtime responses"
```

---

### Task 4: Add Deterministic Preflight Gating And Remediation Evidence Normalization

**Files:**
- Create: `scripts/check_actual_certification_gate.py`
- Modify: `scripts/run_actual_certification.py`
- Modify: `scripts/normalize_actual_certification.py`
- Modify: `process/actual_certification.py`
- Modify: `tests/test_actual_certification.py`
- Modify: `process/package.yaml`

**Interfaces:**
- Consumes: one append-only phase summary plus its raw artifact root.
- Produces: `validate_phase_gate(summary, artifact_root, expected_phase, model_family, adapter_version, expected_count) -> list[str]`; CLI exit 0 only for complete same-family/same-adapter passing evidence; remediation normalization that links but does not rewrite the baseline.

- [ ] **Step 1: Write failing preflight-gate tests**

Cover the exact positive and negative cases:

```python
def test_preflight_gate_requires_exact_five_same_identity_passes(tmp_path):
    summary, artifact = build_phase_summary(tmp_path, phase="preflight", count=5, status="passed", adapter_version="2.0")
    assert validate_phase_gate(summary, artifact, "preflight", "qwen-class", "2.0", 5) == []
    for mutation, code in (
        (lambda value: value["cases"].pop(), "actual-model.gate-case-count"),
        (lambda value: value["adapter"].update(version="1.0"), "actual-model.gate-adapter-mismatch"),
        (lambda value: value["cases"][0].update(deterministic_validation_result="failed"), "actual-model.gate-case-failed"),
    ):
        broken = copy.deepcopy(summary)
        mutation(broken)
        assert code in validate_phase_gate(broken, artifact, "preflight", "qwen-class", "2.0", 5)
```

Also test duplicate case IDs, missing raw files, checksum mismatch, retry lineage mismatch, wrong phase/family/model digest, privacy-unsafe normalized values, and matrix count 15.

- [ ] **Step 2: Add append-only phase-summary output**

Extend `run_actual_certification.py`:

```text
--result-output PATH        required for preflight and matrix; created with exclusive create
--preflight-result PATH     required for matrix; must pass the deterministic 5-case gate
```

Before invoking a matrix model call, validate `--preflight-result` against the same family, frozen model identity, adapter `2.0`, source catalog hash, and supplied artifact root. A failed gate exits 3 with `actual-model.preflight-gate` and performs zero model calls.

- [ ] **Step 3: Implement the read-only gate CLI**

`scripts/check_actual_certification_gate.py` accepts:

```powershell
python scripts/check_actual_certification_gate.py RESULT.json --artifact-root RAW_ROOT --phase preflight --model-family qwen-class --adapter-version 2.0 --expected-count 5
```

Exit 0 prints one JSON object with `status: passed`; exit 1 means a completed but failed gate; exit 3 means malformed, mismatched, missing, unsafe, or unverifiable evidence. The command must not invoke a model or write files.

- [ ] **Step 4: Normalize remediation evidence separately from baseline**

Extend `normalize_actual_certification.py` with:

```text
--baseline-evidence PATH
--remediation-artifact-root PATH
--preflight-result PATH
--matrix-result PATH
--output PATH
```

The new normalized document records a `baseline_reference` containing the preserved baseline evidence path, SHA-256, raw logical artifact ID, and adapter `1.0`, while active preflight/matrix rows point only to the new remediation artifact and adapter `2.0`. Retry rows include `attempt_ordinal`, `retry_of`, `response_schema_sha256`, `thinking_present`, `final_response_present`, raw checksum, and exact diagnostics.

- [ ] **Step 5: Add backward-compatible validation tests**

Run validation against both unchanged 2026-07-15 documents and synthetic adapter `2.0` remediation evidence. Assert that changing a baseline digest, removing attempt 1, forging `retry_of`, or referencing a raw file twice fails.

- [ ] **Step 6: Run the complete deterministic gate suite**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_actual_certification.py tests/test_weak_model_kit.py tests/test_process_package.py -q
python -m compileall -q process scripts/run_actual_certification.py scripts/check_actual_certification_gate.py scripts/normalize_actual_certification.py
git diff --check
```

Expected: all focused tests pass; compilation and diff checks exit 0.

- [ ] **Step 7: Commit gate and normalization support**

```powershell
git add process/actual_certification.py process/package.yaml scripts/run_actual_certification.py scripts/check_actual_certification_gate.py scripts/normalize_actual_certification.py tests/test_actual_certification.py
git commit -m "feat: gate weak-model matrix on preflight"
```

---

### Task 5: Execute Qwen And DeepSeek Remediation Certification

**Files:**
- Create outside Git: `../teamSsdCli-release-artifacts/raw-artifact-v0.2.0-qwen-remediation-2026-07-16/`
- Create outside Git: `../teamSsdCli-release-artifacts/raw-artifact-v0.2.0-deepseek-remediation-2026-07-16/`
- Create: `process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml`
- Create: `process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml`
- Modify: `tests/test_actual_certification.py`

**Interfaces:**
- Consumes: committed adapter `2.0`, deterministic gate, frozen case catalog, local Ollama `0.30.11`, and exact frozen model tags/digests.
- Produces: new append-only raw artifacts and normalized Git evidence; matrix evidence exists only for a family whose preflight gate passed 5/5.

- [ ] **Step 1: Verify exact local runtime identities**

```powershell
ollama list
ollama show qwen3.5:9b
ollama show deepseek-r1:8b
ollama ps
```

Expected: both exact tags are present; Qwen digest begins `6488c96fa5fa`; DeepSeek digest is `6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763`; runtime probe later confirms Ollama `0.30.11`. If identity differs, stop without model execution and record the exact blocker.

- [ ] **Step 2: Create new runtime probes**

```powershell
$qwen = Resolve-Path '..\teamSsdCli-release-artifacts' | ForEach-Object { Join-Path $_ 'raw-artifact-v0.2.0-qwen-remediation-2026-07-16' }
$deepseek = Resolve-Path '..\teamSsdCli-release-artifacts' | ForEach-Object { Join-Path $_ 'raw-artifact-v0.2.0-deepseek-remediation-2026-07-16' }
python scripts/run_actual_certification.py --raw-output "$qwen\runtime-probe" --phase runtime-probe --model-family qwen-class
python scripts/run_actual_certification.py --raw-output "$deepseek\runtime-probe" --phase runtime-probe --model-family deepseek-class
```

Expected: both commands return a passing runtime identity. Every destination must be new; an existing destination is a hard stop, not an overwrite prompt.

- [ ] **Step 3: Run Qwen preflight and gate it**

```powershell
python scripts/run_actual_certification.py --raw-output "$qwen\preflight" --phase preflight --model-family qwen-class --result-output "$qwen\qwen-preflight-result.json"
python scripts/check_actual_certification_gate.py "$qwen\qwen-preflight-result.json" --artifact-root "$qwen" --phase preflight --model-family qwen-class --adapter-version 2.0 --expected-count 5
```

Expected success criterion: 5/5 pass and gate exit 0. If the gate fails, do not run Qwen matrix; normalize the preflight-only evidence, record exact diagnostics, and continue only with the independent DeepSeek preflight.

- [ ] **Step 4: Run Qwen matrix only after its gate**

```powershell
python scripts/run_actual_certification.py --raw-output "$qwen\matrix" --phase matrix --model-family qwen-class --preflight-result "$qwen\qwen-preflight-result.json" --result-output "$qwen\qwen-matrix-result.json"
python scripts/check_actual_certification_gate.py "$qwen\qwen-matrix-result.json" --artifact-root "$qwen" --phase matrix --model-family qwen-class --adapter-version 2.0 --expected-count 15
```

Expected success criterion: 15/15 pass and gate exit 0.

- [ ] **Step 5: Run DeepSeek preflight and gate it**

```powershell
python scripts/run_actual_certification.py --raw-output "$deepseek\preflight" --phase preflight --model-family deepseek-class --result-output "$deepseek\deepseek-preflight-result.json"
python scripts/check_actual_certification_gate.py "$deepseek\deepseek-preflight-result.json" --artifact-root "$deepseek" --phase preflight --model-family deepseek-class --adapter-version 2.0 --expected-count 5
```

Expected success criterion: 5/5 pass and gate exit 0. If the gate fails, do not run DeepSeek matrix.

- [ ] **Step 6: Run DeepSeek matrix only after its gate**

```powershell
python scripts/run_actual_certification.py --raw-output "$deepseek\matrix" --phase matrix --model-family deepseek-class --preflight-result "$deepseek\deepseek-preflight-result.json" --result-output "$deepseek\deepseek-matrix-result.json"
python scripts/check_actual_certification_gate.py "$deepseek\deepseek-matrix-result.json" --artifact-root "$deepseek" --phase matrix --model-family deepseek-class --adapter-version 2.0 --expected-count 15
```

Expected success criterion: 15/15 pass and gate exit 0.

- [ ] **Step 7: Normalize each completed family without touching baseline files**

For each family, run the normalizer with its 2026-07-15 baseline evidence, new raw root, and completed phase result files. When a preflight gate failed, omit `--matrix-result`; the output must state `matrix_not_run: preflight-gate-failed`.

Success-path commands:

```powershell
python scripts/normalize_actual_certification.py --baseline-evidence process/certification/evidence/phase-2-11-qwen-2026-07-15.yaml --remediation-artifact-root "$qwen" --preflight-result "$qwen\qwen-preflight-result.json" --matrix-result "$qwen\qwen-matrix-result.json" --output process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml --model-family qwen-class
python scripts/normalize_actual_certification.py --baseline-evidence process/certification/evidence/phase-2-11-deepseek-2026-07-15.yaml --remediation-artifact-root "$deepseek" --preflight-result "$deepseek\deepseek-preflight-result.json" --matrix-result "$deepseek\deepseek-matrix-result.json" --output process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml --model-family deepseek-class
```

- [ ] **Step 8: Bind fresh evidence tests and run privacy checks**

Add tests that load each new normalized file, resolve its exact external remediation artifact, and require `validate_normalized_evidence(...) == []`. Assert 5 preflight rows and, only on success, 15 matrix rows; all rows use adapter `2.0`; every retry lineage is complete; original evidence hashes match `baseline_reference`.

Run:

```powershell
python -m pytest tests/test_actual_certification.py -q
rg -n -i "(?:[A-Z]:\\Users\\|/Users/|api[_-]?key|password|secret|token)" process/certification/evidence/phase-2-11-*-remediation-2026-07-16.yaml
rg -n -i "https?://" process/certification/evidence/phase-2-11-*-remediation-2026-07-16.yaml | rg -v "127\.0\.0\.1"
git diff --check
```

Expected: tests pass; privacy scan has no match except the explicitly normalized loopback endpoint if the regex implementation reports it; diff check exits 0.

- [ ] **Step 9: Commit normalized evidence only**

```powershell
git add process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml tests/test_actual_certification.py
git commit -m "test: record weak-model adapter remediation"
```

Never add the external raw-artifact directories to Git.

---

### Task 6: Reconcile Outcome, Documentation, Reviews, And Final Verification

**Files:**
- Create: `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_REMEDIATION_AUDIT_2026-07-16.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `docs/00_FILE_STRUCTURE.md`
- Modify: `docs/runbooks/WEAK_MODEL_OPERATING_KIT.md`
- Modify: `docs/runbooks/CERTIFICATION_EVIDENCE.md`
- Modify: `openspec/changes/define-transfer-ready-process-package/tasks.md`
- Modify: `.superpowers/sdd/progress.md` if ignored/local

**Interfaces:**
- Consumes: focused/full test evidence, actual Qwen/DeepSeek gate results, normalized/raw hashes, review findings, and OpenSpec/status contract.
- Produces: one truthful dated outcome audit and a reconciled phase state. A failed family leaves 2.11 `in_progress`; complete 5/5 + 15/15 for both families moves 2.11 to `pending_acceptance`, never directly to `closed` without the required human acceptance.

- [ ] **Step 1: Write the dated evidence audit from actual results**

Record exact counts for each family, adapter/runtime identity, attempt/retry counts, every remaining diagnostic, authority/safety outcome, raw logical artifact IDs and checksums, normalized evidence paths, model-proxy limitation, and whether each matrix ran. Do not describe a gate as passing unless the deterministic gate command exited 0.

- [ ] **Step 2: Reconcile the success or residual-failure path exactly**

If both families pass 5/5 and 15/15:

```text
OpenSpec tasks 4.7, 4.8, and 4.9 = checked
transfer progress = 23/36
work item 2.11 = pending_acceptance
work item 2.12 = still blocked until explicit human acceptance of remediation evidence
```

If either family fails:

```text
OpenSpec task 4.7 = checked after reviewed contract implementation
OpenSpec task 4.8 = checked after reviewed adapter/gate implementation
OpenSpec task 4.9 = unchecked
transfer progress = 22/36
work item 2.11 = in_progress
work item 2.12 = blocked
```

In both paths, preserve task 4.5 as checked baseline execution and state that fallback-only acceptance was superseded by the remediation decision.

- [ ] **Step 3: Update operator and structure documentation**

Document adapter `2.0`, generated role schemas, reasoning/final separation, one structural retry, preflight summary/gate commands, matrix blocking, mechanical normalization boundary, baseline/remediation evidence split, and recovery procedure. `docs/00_FILE_STRUCTURE.md` must list `process/model_adapter.py`, `scripts/check_actual_certification_gate.py`, and the new evidence/audit files.

- [ ] **Step 4: Run focused and full deterministic verification**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_actual_certification.py tests/test_weak_model_kit.py tests/test_process_package.py -q
python -m pytest -q
python -m compileall -q process scripts
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root .
git diff --check
```

Expected: focused and full tests have zero failures; only documented environment-dependent skips are allowed; compile exits 0; OpenSpec reports 10 passed and 0 failed; roadmap/OpenSpec reports 0 errors and 0 warnings; diff check exits 0.

Invoke `phase-status-audit` again after documentation reconciliation. Expected: 2.1-2.10 remain `closed`; 2.11 matches the actual remediation outcome; 2.12 remains blocked; no stale `pending_acceptance` wording survives on a failure path and no stale `in_progress` wording survives on a success path.

- [ ] **Step 5: Re-run the AI-disabled baseline**

Use a new external raw directory:

```powershell
python scripts/run_actual_certification.py --raw-output ..\teamSsdCli-release-artifacts\raw-artifact-v0.2.0-ai-disabled-remediation-2026-07-16 --phase ai-disabled
```

Expected: 11/11 pass. This verifies the adapter changes did not make deterministic operation depend on AI.

- [ ] **Step 6: Run privacy and raw-reference verification**

Recalculate every remediation raw checksum referenced by normalized evidence, confirm each eligible raw attempt is referenced exactly once as active or failed, confirm no raw file is in Git, and run:

```powershell
git ls-files | rg "raw-artifact|attempt-[12]\.json$"
rg -n -i "(?:[A-Z]:\\Users\\|/Users/|api[_-]?key|password|secret|bearer\s+|private[_-]?token)" process/certification/evidence docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_REMEDIATION_AUDIT_2026-07-16.md
```

Expected: no tracked raw artifact/attempt files and no privacy/secret match.

- [ ] **Step 7: Complete the required High-risk review route**

Run, in order:

1. task/spec compliance review over the implementation range;
2. architecture review focused on authority ownership, non-leading schemas, semantic-normalization prohibition, retry boundary, and evidence immutability;
3. verification review using fresh command output and raw/normalized cross-checks.

Any finding is fixed through a new TDD cycle and re-reviewed. Do not perform a phase-final whole-branch review because Phase 2 remains open.

- [ ] **Step 8: Commit reconciliation and documentation**

```powershell
git add docs openspec/changes/define-transfer-ready-process-package/tasks.md
git commit -m "docs: reconcile weak-model remediation evidence"
```

Do not stage `.claude/`, `.vite/`, ignored scratch ledgers, or external raw artifacts.

- [ ] **Step 9: Prepare the full session report**

Report risk route and actual agent profiles/models, OpenSpec change/schema, task progress before/after, exact Qwen/DeepSeek preflight and matrix counts, retry counts, AI-disabled 11/11 result, model/runtime/adapter identities, raw and normalized evidence locations, verification commands/results, review findings, proxy limitations, commit hashes, current 2.11/2.12 status, and the single next human decision. Do not claim 2.11 closed or start 2.12.
