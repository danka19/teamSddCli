# Weak-Model Operating Kit And Safe Parallel Work

Status: work items 2.9-2.11 are closed. Adapter `2.2` passed Qwen and DeepSeek 5/5 preflight and 15/15 matrix gates; AI-disabled passed 11/11.

## Boundary

The deterministic process, not the model, selects the role, class, one-stage boundary, instruction, read pack, evidence contract, stop point, and allowed write scope. Analyst, developer, QA, and Tech Lead assistants are advisory. They cannot approve, waive, merge, release, archive, resume, set a gate green, mutate lifecycle state, or turn their own draft into canonical evidence.

The three family templates contain no process policy or transition rules, have no authority, cannot write canonical data, and preserve existing canonical files if a runtime fails. Adapter `2.2` uses `process/operation_plan.py` before generation to select one deterministic `draft-content` or `blocked-summary` branch and bind artifact kind, reason codes, verified source inventory, unresolved inputs, and accountable human route. The model returns only source-linked observations or a concise blocked summary with one allowed source ID. `process/model_adapter.py` validates that content and mechanically expands it into the existing operation-evidence contract. The model never selects the process decision, artifact route, reason code, human action, or lifecycle result. Adapter `1.0`, `2.0`, and `2.1` builders remain read-only compatibility paths for historical evidence.

## Deterministic launch

1. Create a YAML read-pack request with `task_id`, `role`, `change_class`, `stage`, authority-labelled `sources`, stable IDs, known traps, and unresolved inputs.
2. Run `python scripts/build_read_pack.py REQUEST.yaml`. Exit `0` means ready; exit `3` means missing, unsafe, duplicate, unconfigured, oversized, or unresolved context blocked launch. The output embeds only the requested bounded UTF-8 content or named Markdown sections and binds each excerpt to its source hash.
3. Preserve the JSON output inside the repository and run `python scripts/launch_role_task.py READ_PACK.json --repository-root REPOSITORY --evidence evidence/TASK.yaml`. The launcher revalidates the schema, identity, bounded local paths, canonical allowlist, and every content hash before it emits a verified source manifest.
4. Supply the selected role instruction and read pack to the configured adapter. Do not let the model select another role, stage, authority, source hierarchy, or transition.
5. Validate the returned draft record with `python scripts/check_weak_model_evidence.py EVIDENCE.yaml --launch LAUNCH.json --read-pack READ_PACK.json`. Only `draft-complete`, `blocked`, or `failed` is valid. The task, role, stage, pack identity, verified source identity, human stop, checks, and canonical references must match the concrete launch/read pack. A success, validation, integration, or file-state claim needs corresponding command/result evidence; claim text cannot conceal approval or transition authority.
6. At the role instruction's human stop point, run deterministic checks and obtain the named human review before beginning another stage.

For actual-model certification, run a new append-only phase destination and then
gate its summary:

```powershell
python scripts/run_actual_certification.py --raw-output <new-root>\runtime-probe --phase runtime-probe --model-family qwen-class --result-output <new-root>\qwen-class-runtime-result.json
python scripts/run_actual_certification.py --raw-output <new-root>\preflight --phase preflight --model-family qwen-class --result-output <new-root>\qwen-preflight-result.json
python scripts/check_actual_certification_gate.py <new-root>\qwen-preflight-result.json --artifact-root <new-root> --phase preflight --model-family qwen-class --adapter-version 2.2 --expected-count 5
```

Repeat with `deepseek-class`. A family matrix may start only after its same-root,
same-family, same-adapter preflight gate exits `0`. Gate exit `1` blocks the
matrix; exit `3` means evidence is unverifiable. Do not infer a pass from fluent
output or from the runner having completed all cases.

Run local model families sequentially. Unload Qwen before DeepSeek, do not run
pytest or another model beside the DeepSeek slice, and leave a short pause
between preflight and matrix. DeepSeek can materially load the workstation;
the current adapter therefore requests `num_ctx=8192` rather than the model's
advertised 131072-token maximum. Do not raise this operational bound for the
certification catalog without new resource and contract evidence. A
runtime failure receives a new append-only root after the local service is
healthy, never a reused destination.

Use only a new external artifact root such as
`../teamSsdCli-release-artifacts/<new-versioned-artifact>/`. The runner rejects
repository-contained paths, existing destinations, traversal/alias paths,
symlink/junction/reparse components, raw/result overlap, and result output
outside the selected artifact root before any model call or directory creation.
Runtime, preflight, and matrix phase directories and result files are created
exclusively and rechecked before writes. After safe destination establishment,
runtime, identity, network, or interrupted-call failures retain a closed
non-success operational result; destination-validation failures remain
side-effect free.

The runner binds preflight to a fresh full-digest/runtime observation from
`process/certification/runtime-identities.yaml`. Immediately before every matrix
model call it probes the current tag again and requires exact equality to both
that immutable allowlist and the preflight observation. Ollama tag invocation is
not immutable-digest addressed here, so a small observation-to-call race remains;
the safe response to any detected change is exit `3` with no matrix model call.

Canonical sources must be listed by the package and present under the repository root. Supporting, evidence, and generated/advisory sources remain explicitly labelled. Read packs contain stable paths and hashes, not private exports or an unbounded repository dump. Missing canonical context stays in `missing_or_invalid_context`; unresolved inputs block launch instead of being invented.

Derived artifacts cite the stable canonical IDs they summarize. Model drafts remain non-canonical scratch output until deterministic checks, human review, and the normal Git/OpenSpec process accept them. If an adapter is unavailable, exceeds context, or fails, use the same instruction, read-pack manifest, templates, deterministic commands, and human-authored evidence without weakening a gate.

## Safe parallel plan

Run `python scripts/check_parallel_plan.py PLAN.yaml` before concurrent AI-assisted tasks. `parallel-safe` requires:

- unique task IDs, owners, evidence paths, stop conditions, and focused checks;
- no unfinished dependency between concurrent tasks;
- normalized repository-relative write scopes with no equal, parent, or child overlap;
- no policy or lifecycle decision delegated to a parallel task;
- a named integration owner;
- declared combined `integration`, `traceability`, `review`, and `conflict` checks.

An unfinished dependency, shared canonical path, or authority decision returns `serialize`. Missing evidence isolation, owner, task boundary, or combined gate returns `blocked`. Windows and POSIX separator/case equivalents are normalized before overlap checks. Each task retains separate focused evidence; `promotion_allowed` becomes true only when structured results bind every declared focused and combined check to a `passed` result and non-empty evidence reference.

## Evidence and recovery

Operation evidence separates sources read, artifacts drafted, actual checks, claims, human decisions still required, unresolved inputs, residual limitations, and prohibited actions. Unsupported completion, fabricated evidence, approval, transition, or a derived artifact without canonical references is rejected. Rejected or partial output remains scratch data and does not change canonical state.

All committed examples and tests are synthetic. They prove deterministic contracts and the AI-disabled path, not model quality, corporate compatibility, real integration availability, or transfer readiness.

Adapter `2.2` may make one retry only when the final response is empty, invalid
JSON, or fails its generated schema. The retry keeps identical facts, sources,
role, case, and schema and adds only the fixed structural instruction. A
structurally valid semantic failure is never retried. Every attempt is written to
a separate immutable raw file with its own checksum and lineage.

Normalization is mechanical: it may add operation-plan identity, verified source
inventory, policy metadata, and invariant authority fields, but it cannot repair
model-authored observations or a blocked summary. Model checks are recorded as
not run unless independently supplied by deterministic evidence. Historical
adapter `1.0`, `2.0`, and `2.1` evidence remains immutable; adapter `2.2` lives
in separate raw roots and normalized documents with hashed adapter `2.1`
baseline references and runtime-probe checksums.

The 2026-07-16 adapter `2.1` execution produced Qwen 2/5 and DeepSeek 0/5.
All ten responses were structurally valid on attempt 1, so zero retries were
allowed. Both gates failed and neither matrix ran. The exact evidence and
diagnostics are recorded in
`docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_1_AUDIT_2026-07-16.md`.

The 2026-07-17 adapter `2.2` execution produced Qwen 5/5 then 15/15 and
DeepSeek 5/5 then 15/15. Every accepted response used attempt 1. AI-disabled
passed 11/11. See
`docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_2_AUDIT_2026-07-17.md`.

Recovery procedure:

1. Stop after any gate failure; do not run that family's matrix.
2. Preserve the raw destination exactly as written. Never delete, rename,
   overwrite, or reuse it for a retry.
3. Normalize the completed failed preflight without `--matrix-result`; require
   `status: failed` and `matrix_not_run: preflight-gate-failed`.
4. Recalculate every referenced checksum and confirm each eligible attempt is
   referenced exactly once.
5. Record the exact diagnostics and route the result to the catalog-owned human
   owner. Do not relax schemas, semantic validation, authority checks, or retry
   rules to obtain a pass.
6. Continue through templates, deterministic commands, checklists, and
   human-authored evidence while the AI path remains unusable.
