# Weak-Model Adapter 2.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the ambiguous adapter `2.0` decision/payload contract with a non-leading decision-discriminated adapter `2.1`, then re-run exact-identity Qwen and DeepSeek certification in new append-only artifact roots.

**Architecture:** The deterministic launcher continues to own identity, role, allowed global vocabulary, verified sources, and the internal required artifact kind. The model receives a closed JSON Schema with two mutually exclusive branches selected by its own `decision`: `draft` requires a role payload, while `block` requires `null`. Semantic correctness remains exclusively in the deterministic validator; runtime identity, destination, evidence, and human-authority boundaries remain unchanged.

**Tech Stack:** Python 3, `jsonschema` Draft 2020-12, PyYAML, pytest, Ollama `0.30.11`, OpenSpec `1.4.1`, PowerShell.

## Global Constraints

- Adapter identity is exactly `2.1` for new Qwen and DeepSeek executions.
- Both `draft` and `block` branches are present in every model-facing response schema.
- Case-specific expected decision, expected reason codes, required source IDs, required artifact kind, validator result, and internal sentinel values are absent from schema, prompt, initial request, retry prompt, and retry request.
- `draft` requires a non-null role payload, at least one check, and at least one observation or claim.
- `block` requires a null role payload, at least one unresolved input, and at least one required human action.
- Human approval is not required to prepare a bounded non-canonical advisory draft; it remains required for canonical mutation and lifecycle transition.
- One retry is permitted only for empty final output, invalid JSON, or generated-schema failure. No semantic retry or repair is permitted.
- Adapter `1.0` and `2.0` raw and normalized evidence remains immutable and read-only compatible.
- Exact observed full model digest and Ollama runtime are checked before execution and immediately before model calls.
- Raw and result destinations are new, external, non-aliased, non-reparse, non-overlapping, append-only paths outside Git.
- Matrix execution requires the same family's deterministic five-of-five preflight gate.
- AI authority, approvals, waivers, merges, releases, resumes, archive decisions, transitions, and canonical writes remain forbidden.
- Work item 2.11 remains `in_progress` unless both exact model families pass five-of-five plus fifteen-of-fifteen and the human owner later accepts the evidence.

---

### Task 1: Implement The Decision-Discriminated Response Contract

**Files:**
- Modify: `tests/test_model_adapter.py`
- Modify: `process/model_adapter.py`
- Modify: `tests/test_actual_certification.py`

**Interfaces:**
- Consumes: verified launcher `model_response_contract`, verified source manifest, global reason-code vocabulary.
- Produces: `build_role_response_schema(launch) -> dict[str, Any]` with two closed top-level branches and unchanged `parse_role_response()`/`normalize_role_response()` APIs.

- [ ] **Step 1: Write failing schema branch tests**

Add tests that construct valid draft/block responses and contradictory variants:

```python
def test_adapter_2_1_schema_discriminates_draft_and_block(launch):
    schema = build_role_response_schema(launch)
    draft = role_response(launch, decision="draft", payload=valid_payload())
    blocked = role_response(
        launch,
        decision="block",
        payload=None,
        unresolved_inputs=["environment_evidence"],
        human_decisions_required=["provide-and-review-evidence"],
    )
    assert list(Draft202012Validator(schema).iter_errors(draft)) == []
    assert list(Draft202012Validator(schema).iter_errors(blocked)) == []
    assert list(Draft202012Validator(schema).iter_errors({**blocked, role_payload_key(launch): valid_payload()}))
    assert list(Draft202012Validator(schema).iter_errors({**draft, role_payload_key(launch): None}))
```

Also assert `block` rejects empty `unresolved_inputs` or `human_decisions_required`, and `draft` rejects empty checks plus empty observations/claims.

- [ ] **Step 2: Run RED**

Run:

```powershell
python -m pytest tests/test_model_adapter.py -k "discriminates or branch or blocked" -q
```

Expected: failures because adapter `2.0` uses one nullable payload property independent of `decision`.

- [ ] **Step 3: Implement closed `oneOf` branches**

Refactor shared property definitions, then return:

```python
common_required = [
    "case_id",
    "decision",
    "reason_codes",
    "source_ids",
    "unresolved_inputs",
    "human_decisions_required",
    payload_key,
]

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
```

Draft payload `checks` has `minItems: 1`; the payload uses `anyOf` requiring non-empty `observations` or non-empty `claims`.

- [ ] **Step 4: Preserve semantic normalization**

Keep the explicit defensive decision/payload check in `normalize_role_response()` even though the schema now rejects the contradiction. Do not add inferred fields or response correction. Ensure forbidden authority detection still examines unresolved inputs, human actions, and the selected payload.

- [ ] **Step 5: Run GREEN and compatibility**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_weak_model_kit.py -q
python -m compileall -q process/model_adapter.py
```

Expected: zero failures; adapter `1.0` conservative diagnostics remain unchanged.

- [ ] **Step 6: Commit**

```powershell
git add process/model_adapter.py tests/test_model_adapter.py tests/test_actual_certification.py
git commit -m "feat: discriminate weak-model decisions"
```

---

### Task 2: Add Neutral Draft-vs-Approval Guidance And Leakage Proof

**Files:**
- Modify: `process/actual_certification.py`
- Modify: `tests/test_actual_certification.py`
- Modify: `tests/test_model_adapter.py`

**Interfaces:**
- Consumes: `build_model_prompt(case, launch, read_pack)`.
- Produces: one neutral adapter `2.1` contract explanation and byte-level leakage evidence over all model-facing surfaces.

- [ ] **Step 1: Write failing prompt-contract tests**

Assert the prompt contains universal rules:

```python
assert "A bounded advisory draft may be prepared before human approval" in prompt
assert "Human approval is still required before canonical mutation or lifecycle transition" in prompt
assert "A blocked response contains no completed role artifact" in prompt
```

Construct unique sentinels in:

- expected decision;
- required reason codes;
- required source IDs;
- required artifact kind;
- expected validator diagnostics.

Assert each sentinel and validator-only field name is absent independently from:

1. generated schema;
2. initial prompt;
3. complete initial request;
4. retry prompt;
5. complete retry request.

- [ ] **Step 2: Run RED**

```powershell
python -m pytest tests/test_actual_certification.py -k "draft_approval or validator_answer or leakage" -q
```

Expected: missing neutral guidance assertions fail.

- [ ] **Step 3: Add neutral branch guidance**

Add a stable adapter instruction object to the prompt context:

```python
"decision_contract": {
    "draft": (
        "Prepare one bounded non-canonical advisory artifact when supplied facts "
        "and sources are sufficient. Human review remains pending."
    ),
    "block": (
        "Return no completed role artifact when required facts, evidence, or "
        "accountable authority are missing. Identify unresolved inputs and human actions."
    ),
    "authority": (
        "Human approval is required before canonical mutation or lifecycle transition; "
        "it is not automatically required to prepare a bounded advisory draft."
    ),
}
```

Do not copy case expectations into this object.

- [ ] **Step 4: Verify retry prompt remains append-only**

Assert attempt 2 equals:

```python
retry_prompt == initial_prompt + STRUCTURAL_RETRY_SUFFIX
```

and the suffix remains exactly:

```text
Return only one JSON object matching the unchanged supplied schema.
```

- [ ] **Step 5: Run GREEN**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_actual_certification.py -q
```

- [ ] **Step 6: Commit**

```powershell
git add process/actual_certification.py tests/test_actual_certification.py tests/test_model_adapter.py
git commit -m "feat: clarify advisory draft boundary"
```

---

### Task 3: Version Runtime, Gate, And Evidence To Adapter 2.1

**Files:**
- Modify: `process/adapters/qwen-class.yaml`
- Modify: `process/adapters/deepseek-class.yaml`
- Modify: `process/actual_certification.py`
- Modify: `scripts/normalize_actual_certification.py`
- Modify: `process/schemas/process-package.schema.json`
- Modify: `process/package.yaml` only if package inventory changes
- Modify: `tests/test_actual_certification.py`
- Modify: `tests/test_process_package.py`

**Interfaces:**
- Consumes: adapter profile loader, execution summary/gate, normalization validator, historical compatibility branches.
- Produces: adapter `2.1` runtime identity and read-only `1.0`/`2.0` compatibility.

- [ ] **Step 1: Write failing adapter-version tests**

Add assertions:

```python
assert load_adapter_profile(process_root, "qwen-class")["schema_version"] == "2.1"
assert load_adapter_profile(process_root, "deepseek-class")["schema_version"] == "2.1"
```

Synthetic `2.1` summaries must validate; changing summary/raw/request adapter identity to `2.0` must fail. Existing committed adapter `2.0` normalized evidence must still validate through the historical read path.

- [ ] **Step 2: Run RED**

```powershell
python -m pytest tests/test_actual_certification.py tests/test_process_package.py -k "adapter or remediation or compatibility" -q
```

- [ ] **Step 3: Update profiles and closed loader**

Change only:

```yaml
schema_version: "2.1"
```

Keep generation settings:

```yaml
format: json-schema
think: false
num_predict: 1200  # Qwen
num_predict: 2400  # DeepSeek
technical_retries: 1
```

Update `load_adapter_profile()` to accept exactly `2.1` for current execution. Historical evidence validators branch on recorded evidence version; they do not load `2.0` as the current runtime profile.

- [ ] **Step 4: Bind `2.1` through execution and normalization**

Ensure runtime probe, raw attempt, phase summary, gate input, request contract, normalized evidence, and evidence validator all require consistent adapter `2.1` for new runs.

Retain:

- exact observed digest/runtime;
- prompt/schema/request hashes;
- structural retry lineage;
- honest failed-preflight normalization;
- external destination validation;
- privacy and baseline-family binding.

- [ ] **Step 5: Run focused and full deterministic verification**

```powershell
python -m pytest tests/test_model_adapter.py tests/test_actual_certification.py tests/test_weak_model_kit.py tests/test_process_package.py -q
python -m pytest -q
python -m compileall -q process scripts
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root .
git diff --check
```

- [ ] **Step 6: Complete implementation reviews**

Run:

1. task/spec review over Tasks 1-3;
2. architecture review of non-leading schema, authority, retry, compatibility, observed identity, and destination boundaries.

Fix and re-review all Critical or Important findings before any model execution.

- [ ] **Step 7: Mark OpenSpec implementation tasks 1.1-3.3 complete and commit**

```powershell
git add process scripts tests openspec/changes/simplify-weak-model-decision-contract/tasks.md
git commit -m "feat: version weak-model adapter 2.1"
```

---

### Task 4: Execute New Qwen And DeepSeek Certification

**Files:**
- Create outside Git: `../teamSsdCli-release-artifacts/raw-artifact-v0.2.1-qwen-remediation-2026-07-16/`
- Create outside Git: `../teamSsdCli-release-artifacts/raw-artifact-v0.2.1-deepseek-remediation-2026-07-16/`
- Create outside Git: `../teamSsdCli-release-artifacts/raw-artifact-v0.2.1-ai-disabled-remediation-2026-07-16/`
- Create: `process/certification/evidence/phase-2-11-qwen-adapter-2-1-2026-07-16.yaml`
- Create: `process/certification/evidence/phase-2-11-deepseek-adapter-2-1-2026-07-16.yaml`
- Modify: `tests/test_actual_certification.py`

**Interfaces:**
- Consumes: committed adapter `2.1`, exact identity catalog, external destination guard, gate/normalizer.
- Produces: append-only raw and normalized certification evidence.

- [ ] **Step 1: Verify identities and absent destinations**

```powershell
ollama --version
ollama list
ollama show qwen3.5:9b
ollama show deepseek-r1:8b
ollama ps
```

Require:

- Ollama `0.30.11`;
- Qwen full digest `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7`;
- DeepSeek full digest `6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763`;
- all three planned roots absent.

Any mismatch or existing destination is a hard stop.

- [ ] **Step 2: Run runtime probes and preflights**

For each family:

```powershell
python scripts/run_actual_certification.py --raw-output <root>\runtime-probe --phase runtime-probe --model-family <family>
python scripts/run_actual_certification.py --raw-output <root>\preflight --phase preflight --model-family <family> --result-output <root>\<family>-preflight-result.json
python scripts/check_actual_certification_gate.py <root>\<family>-preflight-result.json --artifact-root <root> --phase preflight --model-family <family> --adapter-version 2.1 --expected-count 5
```

- [ ] **Step 3: Run matrix only after gate exit 0**

```powershell
python scripts/run_actual_certification.py --raw-output <root>\matrix --phase matrix --model-family <family> --preflight-result <root>\<family>-preflight-result.json --result-output <root>\<family>-matrix-result.json
```

Never run a family matrix after preflight exit 1 or 3.

- [ ] **Step 4: Normalize actual outcome**

Passing path uses preflight plus matrix. Honest failure path omits matrix and records:

```yaml
status: failed
matrix:
  status: not-run
matrix_not_run: preflight-gate-failed
```

Do not edit prior `1.0` or `2.0` evidence.

- [ ] **Step 5: Run AI-disabled eleven-case walkthrough**

```powershell
python scripts/run_actual_certification.py --raw-output ..\teamSsdCli-release-artifacts\raw-artifact-v0.2.1-ai-disabled-remediation-2026-07-16 --phase ai-disabled
```

Expected: 11/11.

- [ ] **Step 6: Bind evidence tests and privacy**

Add guarded external-artifact tests that skip cleanly when roots are absent and fully validate exact roots when present.

```powershell
python -m pytest tests/test_actual_certification.py -q
git ls-files | rg "raw-artifact|attempt-[12]\.json$"
rg -n -i "(?:[A-Z]:\\Users\\|/Users/|api[_-]?key|password|secret|bearer\\s+|private[_-]?token)" process/certification/evidence
git diff --check
```

- [ ] **Step 7: Commit normalized evidence only**

```powershell
git add process/certification/evidence tests/test_actual_certification.py openspec/changes/simplify-weak-model-decision-contract/tasks.md
git commit -m "test: record weak-model adapter 2.1 certification"
```

---

### Task 5: Reconcile Outcome And Complete Reviews

**Files:**
- Create: `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_1_AUDIT_2026-07-16.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/ROADMAP.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `docs/00_FILE_STRUCTURE.md`
- Modify: `docs/runbooks/WEAK_MODEL_OPERATING_KIT.md`
- Modify: `docs/runbooks/CERTIFICATION_EVIDENCE.md`
- Modify: `openspec/changes/simplify-weak-model-decision-contract/tasks.md`
- Modify: `openspec/changes/define-transfer-ready-process-package/tasks.md` only according to the actual acceptance path.

**Interfaces:**
- Consumes: exact model results, raw checksums, normalized validation, AI-disabled result, reviews.
- Produces: truthful Phase 2 status and one dated adapter `2.1` audit.

- [ ] **Step 1: Write the outcome audit**

Include:

- adapter `2.0` ten-error classification;
- exact adapter `2.1` identities and results;
- per-case decision, structural/semantic outcome, retries, diagnostics;
- whether each matrix ran;
- raw logical IDs/checksums and normalized evidence;
- authority/safety results;
- AI-disabled 11/11;
- residual tag race and model limitations.

- [ ] **Step 2: Reconcile status**

Success path, only if both families pass 5/5 and 15/15:

```text
new change tasks 15/15 checked
transfer task 4.9 checked
transfer progress 23/36
work item 2.11 pending_acceptance
work item 2.12 blocked until explicit human acceptance
```

Failure path if either family fails:

```text
implementation and executed-evidence tasks checked as actually complete
transfer task 4.9 unchecked
transfer progress 22/36
work item 2.11 in_progress
work item 2.12 blocked
```

- [ ] **Step 3: Run final verification**

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

- [ ] **Step 4: Run ordered final reviews**

1. spec/status review;
2. architecture/safety review;
3. verification/raw-evidence review with fresh commands.

Fix and re-review every Critical or Important finding.

- [ ] **Step 5: Commit reconciliation**

```powershell
git add docs openspec/changes/simplify-weak-model-decision-contract openspec/changes/define-transfer-ready-process-package/tasks.md
git commit -m "docs: reconcile weak-model adapter 2.1 evidence"
```

Do not archive either active Phase 2 change, start Phase 2.12, open a PR, or claim model certification unless the exact gates and human acceptance requirements are satisfied.
