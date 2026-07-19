# Deterministic Certification Evidence

## Purpose And Boundary

`scripts/certify_process_release.py` runs the versioned synthetic case catalog and builds exact requirement/scenario coverage inventory. This is fixture certification only: normalized evidence always states `evidence_kind: deterministic-fixture`, `actual_model_run: false`, and structured model/adapter fields with `not-executed` values. It is not Qwen/DeepSeek evidence, cross-platform evidence, release acceptance, or pilot evidence. The closed evidence schema can represent later actual-model records, but this runner cannot produce one.

The runner is check-only with `--check`. Without `--check`, a passing run creates one new raw bundle directory outside the repository. It never overwrites a bundle, writes to a symlink/reparse destination, or allows source/output overlap.

## Commands

From any working directory:

```powershell
python <repository>/scripts/certify_process_release.py `
  --root <repository> `
  --raw-output <external-artifact-root>/raw-artifact-v0.2.0 `
  --check
```

Remove `--check` only when intentionally creating the immutable raw artifact. Exit `0` means every case matched its golden semantic result and coverage inventory was valid. Exit `1` means a golden mismatch. Exit `3` means unsafe input/output, privacy failure, unknown selector/evidence, invalid coverage gap, or another contract error.

## Execution Safety

- External dispatch is an allowlist in `process/certification.py`; command vectors use `sys.executable`, argument lists, `shell=False`, repository-root working directory, and a timeout.
- YAML cannot supply an executable or arbitrary arguments. Certification-specific negative families use internal preflight signals and do not execute commands.
- Fixture paths must be repository-relative under `process/certification/`; absolute, traversal, credential-like, URL, and production-looking values fail closed.
- Fixture payloads use the explicit `synthetic | example` namespace allowlist. Email, IP, URL, corporate/internal/production identifiers, and secret-like content fail before dispatch. Canonical OpenSpec paths remain trusted source metadata and may contain domain words without becoming fixture values.
- Canonical files are never mutation targets. Every case records before/after SHA-256 snapshots across process, OpenSpec, templates, scripts, and docs; `canonical_mutated` is derived from those snapshots.

## Evidence Storage

Git stores the case catalog, golden expectations, coverage inventory, schemas, normalized semantic fields, and SHA-256 reference. The raw `bundle.json` contains captured validator streams and belongs only in the immutable versioned release artifact outside Git. Normalized evidence deliberately contains no raw stdout/stderr.

The raw artifact reference contains:

- logical artifact version (normally `raw-artifact-<process-version>`);
- filename;
- SHA-256 calculated over deterministic bundle bytes;
- `stored_in_git: false`.

## Coverage And Residual Gaps

`process/certification/coverage.yaml` composes all accepted capability specs and both active delta trees by exact capability, requirement, and scenario headings. `MODIFIED` replaces the accepted requirement scenarios and `REMOVED` removes them; duplicate change ownership and unknown targets fail closed. `evidence-manifest.yaml` contains one explicit row per applicable effective selector. Exact pytest evidence is independently owned by a literal `SCENARIO_COVERAGE` marker beside the named test function in the configured source file; there is no duplicate binding table. Bare pytest-file references, unrelated node substitution, duplicate or unknown markers, unused markers, missing rows, and marker disagreement fail closed.

There is no aggregate default evidence. An allowed residual gap contains all five non-empty fields: `owner`, `risk`, `reason`, `compensation`, and `follow_up`, wins over any capability rule, increments the gap count, and makes report status `gaps`. Structured future-work selectors remove unperformed 2.11-2.14 scenarios from covered/gap rows and count them separately.

A schema-valid gap row proves only that the selector has no accepted exact evidence binding and that a disposition record exists. It does not by itself prove missing product behavior or an independently reviewed risk rating. Bulk-identical owner/risk/reason/follow-up values must be identified as fallback metadata in acceptance material. Before release acceptance, heterogeneous gaps should be classified as current exact-evidence debt, exact manual/governance evidence, explicit future work, or individually assessed residual risk. Changing a frozen candidate's coverage/evidence rows creates a new candidate identity and requires candidate-bound verification again.

The CLI exposes one canonical JSON representation only; it does not maintain a second human-output projection. Operators may format that JSON externally without changing semantic fields.

The eight NIS feedback/publication-boundary scenarios use `process/feedback_policy.py` and exact nodes in `tests/test_feedback_policy.py`. This pure check validates SLA configuration/defaults, comment dispositions/follow-up, no fabricated core-route evidence, future class-aware ownership, read-only legacy input, and corporate generated-view selection. It does not call Confluence or publish anything.

Concrete analyst/minor, developer/major, QA/hotfix, and Tech Lead/major expected-output goldens live under `process/certification/expected-role-outputs/`. The catalog binds each fixture by path and SHA-256, and every golden binds its repository-bounded OpenSpec canonical source by a recomputed SHA-256. Schema, semantic role/class, path/link/privacy, and both hash checks run before certification. All remain `executed: false`.

## Manual Review

1. Run `--check` twice and compare JSON semantics.
2. Confirm no raw directory was created.
3. Run without `--check` against a new external destination.
4. Recalculate SHA-256 for `bundle.json` and compare it with normalized evidence.
5. Confirm normalized evidence says no actual model run occurred and contains no captured streams.
6. Preserve the raw artifact immutable; a repeated create attempt must fail rather than overwrite it.

## Actual-Model Phase 2.11 Slice

`scripts/run_actual_certification.py` extends the existing certification boundary without creating a parallel authority system. `--phase ai-disabled` executes the allowlisted source-linked pytest nodes in `ai-disabled-walkthroughs.yaml`. `--phase preflight` and `--phase matrix` use the shared frozen cases in `qwen-matrix.yaml`, the selected `--model-family qwen-class|deepseek-class` profile, existing read-pack builder, deterministic role launcher, adapter identity, and operation-evidence validator.

For current adapter `2.2`, the launcher derives an identity-bound operation plan from verified case facts and sources before generation. The prompt exposes only the selected branch and its exact response schema. The model returns source-linked observations for `draft-content`, or a summary and allowed source ID for `blocked-summary`. Trusted code binds plan-owned action, artifact kind, reason codes, source inventory, unresolved inputs, and human route without semantic inference. Historical adapters remain reconstructable through frozen version branches.

`--phase runtime-probe` records the exact observed Ollama version, model tag/full digest, loopback endpoint, adapter version, and package version in both raw and exclusive result files. Adapter `2.1` normalized evidence binds both runtime-probe checksums. `process/certification/runtime-identities.yaml` is the immutable full-digest extension to the existing semantic matrix catalog; it does not duplicate tag or runtime ownership because the historical matrix catalog already owns those fields and intentionally retains the shorter Qwen compatibility identifier used by immutable evidence. Preflight summaries bind the combined fresh observed identity. Before every matrix model call, the runner re-observes the current tag digest and runtime version and requires exact equality to both catalogs and the preflight identity. Ollama does not provide immutable-digest invocation through this runner, so an immediate observation-to-call race remains and is recorded as a residual limitation.

All actual-certification raw and result destinations are validated before directory creation, subprocess/model calls, or output writes. They must be new external paths, outside the repository and canonical sources, with no symlink, junction, or Windows reparse component in the path, no raw/result overlap, and result output under the same external artifact root. Phase directories and result files are created exclusively and revalidated before writes. Runtime, identity, network, or interrupted-call failures after safe destination establishment retain a schema-valid non-success operational result; unsafe destination failures make no write. Exact inventory validation rejects extra, missing, duplicate, or unreferenced files. The supported sibling root `../teamSsdCli-release-artifacts/` remains valid.

`scripts/normalize_actual_certification.py` cross-links each model row to its append-only raw artifact. Normalized validation then cross-checks operation, case, role, class, group identity, observed model/runtime identity, source hashes, token/duration metrics, and deterministic result against raw bytes. Failed and superseded attempts remain immutable. Historical remediation evidence remains validation-compatible without being rewritten; only new phase summaries require the observed-identity fields.

The 2026-07-15 Qwen evidence uses Ollama `0.30.11`, `qwen3.5:9b` digest `6488c96fa5fa`, and adapter `1.0`; it passed 0/5 preflight and 1/15 matrix cases. The DeepSeek evidence uses the same frozen semantics with `deepseek-r1:8b`, full digest `6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763`, architecture `qwen3`, 8.2B profile, `Q4_K_M`, context `131072`, Ollama `0.30.11`, and adapter `1.0`; it passed 0/5 and 0/15. These files remain immutable baseline evidence.

Adapter `2.0` added generated closed role schemas, reasoning/final separation,
mechanical normalization, append-only attempt lineage, and one structural retry
only for empty/invalid/schema-invalid final output. `run_actual_certification.py`
writes phase summaries; `check_actual_certification_gate.py` independently
requires exact identity, raw hashes, adapter version, expected count, and every
case passing. A preflight gate must exit `0` before a matrix command is permitted.
Failed preflight normalization omits `--matrix-result` and records
`matrix_not_run: preflight-gate-failed`.

The adapter `2.0` remediation evidence is stored separately at
`phase-2-11-qwen-remediation-2026-07-16.yaml` and
`phase-2-11-deepseek-remediation-2026-07-16.yaml`. Each family completed five
structurally valid attempts, failed 0/5 with `model-adapter.semantic`, used no
retry, and had gate exit `1`; neither matrix ran. Both normalized documents bind
their adapter `1.0` baseline by SHA-256 and validate one-to-one against their
external raw roots. The fresh AI-disabled remediation artifact passed 11/11.

Adapter `2.1` adds mutually exclusive `draft` and `block` schema branches,
model-owned global artifact kind, restricted model check results, universal
advisory-draft versus approval guidance, version-bound current profiles, runtime
result checksum binding, operational failure summaries, and exact inventory
validation. It retains at most one retry only for structural response failure;
semantic failures are never repaired or retried. Historical adapter `1.0` and
`2.0` schema, prompt, diagnostic, and evidence reconstruction remains exact.

The adapter `2.1` normalized evidence is stored at
`phase-2-11-qwen-adapter-2-1-2026-07-16.yaml` and
`phase-2-11-deepseek-adapter-2-1-2026-07-16.yaml`. Qwen passed 2/5 preflight
cases; DeepSeek passed 0/5. All ten responses were structurally valid on attempt
1, so there were zero retries. Both gates failed and neither matrix ran. The new
AI-disabled artifact
`raw-artifact-v0.2.1-ai-disabled-remediation-2026-07-16` passed 11/11 with
exact catalog command vectors and inventory.

DeepSeek reasoning is retained separately from the final-response boundary and
never becomes authority or a pass. Every failed operation routes to deterministic
validation plus the case-specific catalog-owned human role and concrete
disposition action; generic owner/decision text fails normalized validation. Both
models are local family proxies, not corporate-runtime equivalence proof. Work
item 2.11 was still `in_progress` at this historical checkpoint.
The exact adapter `2.1` result is recorded in
`docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_1_AUDIT_2026-07-16.md`.

Adapter `2.2` adds the deterministic operation-plan identity and branch-only
content contract. Normalized evidence is stored at
`phase-2-11-qwen-adapter-2-2-2026-07-17.yaml` and
`phase-2-11-deepseek-adapter-2-2-2026-07-17.yaml`. Qwen and DeepSeek each
passed 5/5 preflight before passing 15/15 matrix cases; every accepted case used
attempt 1. The AI-disabled artifact
`raw-artifact-v0.2.2-ai-disabled-2026-07-17` passed 11/11. Work item 2.11 is
closed and task 4.9 is complete. This evidence does not establish
corporate-runtime or cross-platform equivalence.

Adapter `2.2` requires at least one canonical citation in every draft branch.
For DeepSeek it also bounds the actual Ollama request to `num_ctx=8192`; the
catalog's 131072 value remains model capability metadata, not the operational
allocation used by certification.

Final work item 2.14 certification is normalized at
`phase-2-14-qwen-adapter-2-2-2026-07-18.yaml` and
`phase-2-14-deepseek-adapter-2-2-2026-07-18.yaml`. Both frozen families again
passed 5/5 preflight and 15/15 matrix cases on attempt 1; the retained
AI-disabled artifact passed 11/11. The release selector points only to these
candidate-specific normalized records and their complete external raw roots.
