# Weak-Model Operating Kit And Safe Parallel Work

Status: work items 2.9-2.10 are closed after review and TDD hardening. Work item 2.11 is `in_progress`: adapter `2.0` is implemented, but both frozen proxy families failed 0/5 semantic preflight and neither matrix ran.

## Boundary

The deterministic process, not the model, selects the role, class, one-stage boundary, instruction, read pack, evidence contract, stop point, and allowed write scope. Analyst, developer, QA, and Tech Lead assistants are advisory. They cannot approve, waive, merge, release, archive, resume, set a gate green, mutate lifecycle state, or turn their own draft into canonical evidence.

The three family templates contain no process policy or transition rules, have no authority, cannot write canonical data, and preserve existing canonical files if a runtime fails. For Qwen/DeepSeek certification, adapter `2.0` uses `process/model_adapter.py` to generate a closed role-specific response schema from the verified launch manifest, keep reasoning separate from final output, parse the exact final JSON object, and mechanically expand it into the existing operation-evidence contract. Schema generation may expose supplied source IDs and global reason codes, but never validator-only expected decisions, required answers, or internal classifications.

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
python scripts/run_actual_certification.py --raw-output <new-root>\preflight --phase preflight --model-family qwen-class --result-output <new-root>\qwen-preflight-result.json
python scripts/check_actual_certification_gate.py <new-root>\qwen-preflight-result.json --artifact-root <new-root> --phase preflight --model-family qwen-class --adapter-version 2.0 --expected-count 5
```

Repeat with `deepseek-class`. A family matrix may start only after its same-root,
same-family, same-adapter preflight gate exits `0`. Gate exit `1` blocks the
matrix; exit `3` means evidence is unverifiable. Do not infer a pass from fluent
output or from the runner having completed all cases.

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

Adapter `2.0` may make one retry only when the final response is empty, invalid
JSON, or fails its generated schema. The retry keeps identical facts, sources,
role, case, and schema and adds only the fixed structural instruction. A
structurally valid semantic failure is never retried. Every attempt is written to
a separate immutable raw file with its own checksum and lineage.

Normalization is mechanical: it may add launch-owned identity and invariant
authority fields, but it cannot repair a model decision, reason, source,
observation, claim, check, unresolved input, or required human decision. The
2026-07-15 adapter `1.0` evidence remains the immutable baseline; adapter `2.0`
remediation evidence lives in separate raw roots and normalized documents with a
hashed `baseline_reference`.

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
