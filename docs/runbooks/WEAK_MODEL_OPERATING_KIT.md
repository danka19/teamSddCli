# Weak-Model Operating Kit And Safe Parallel Work

Status: work item 2.9 is closed after combined review and two TDD hardening rounds. This is not actual Qwen/DeepSeek certification; work item 2.10 is ready but has not started, and actual model certification belongs to 2.11.

## Boundary

The deterministic process, not the model, selects the role, class, one-stage boundary, instruction, read pack, evidence contract, stop point, and allowed write scope. Analyst, developer, QA, and Tech Lead assistants are advisory. They cannot approve, waive, merge, release, archive, resume, set a gate green, mutate lifecycle state, or turn their own draft into canonical evidence.

The three adapter templates only package `instruction_path` plus `read_pack_path`. They contain no process policy or transition rules, have no authority, cannot write canonical data, and preserve existing canonical files if a runtime fails. Actual runtime commands, model identifiers, adapter versions, and certification runs are intentionally deferred.

## Deterministic launch

1. Create a YAML read-pack request with `task_id`, `role`, `change_class`, `stage`, authority-labelled `sources`, stable IDs, known traps, and unresolved inputs.
2. Run `python scripts/build_read_pack.py REQUEST.yaml`. Exit `0` means ready; exit `3` means missing, unsafe, duplicate, unconfigured, oversized, or unresolved context blocked launch. The output embeds only the requested bounded UTF-8 content or named Markdown sections and binds each excerpt to its source hash.
3. Preserve the JSON output inside the repository and run `python scripts/launch_role_task.py READ_PACK.json --repository-root REPOSITORY --evidence evidence/TASK.yaml`. The launcher revalidates the schema, identity, bounded local paths, canonical allowlist, and every content hash before it emits a verified source manifest.
4. Supply the selected role instruction and read pack to the configured adapter. Do not let the model select another role, stage, authority, source hierarchy, or transition.
5. Validate the returned draft record with `python scripts/check_weak_model_evidence.py EVIDENCE.yaml --launch LAUNCH.json --read-pack READ_PACK.json`. Only `draft-complete`, `blocked`, or `failed` is valid. The task, role, stage, pack identity, verified source identity, human stop, checks, and canonical references must match the concrete launch/read pack. A success, validation, integration, or file-state claim needs corresponding command/result evidence; claim text cannot conceal approval or transition authority.
6. At the role instruction's human stop point, run deterministic checks and obtain the named human review before beginning another stage.

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
