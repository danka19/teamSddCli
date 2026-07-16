# Phase 2 Work Item 2.11 Adapter 2.1 Outcome Audit

Date: 2026-07-16.

Status: residual failure; work item 2.11 remains `in_progress`.

## Audit Boundary And Criteria

This audit reconciles the append-only adapter `2.1` execution for the frozen
local Qwen- and DeepSeek-family proxies. It compares the result with the
immutable adapter `2.0` remediation baseline without making a
process-effectiveness claim.

Success required each exact model family to pass all five preflight cases before
its fifteen-case matrix could start. Raw runtime and model output remains outside
Git. Git contains normalized evidence, logical raw references, SHA-256 checksums,
stable diagnostics, and this audit.

The audit checks:

- exact package, adapter, runtime, model tag, and full model digest identity;
- the adapter `2.0` ten-response error classification used to justify `2.1`;
- per-case adapter `2.1` result, attempts, retries, diagnostics, and raw checksum;
- runtime-probe and preflight-result checksum binding;
- family-local matrix gating;
- authority, safety, canonical-write, and AI-disabled boundaries;
- immutable baseline references and append-only external artifact roots;
- limitations that remain after the run.

## Adapter 2.0 Ten-Response Baseline Classification

The adapter `2.0` baseline produced ten structurally valid responses and ten
semantic failures. The classifications overlap because one response can violate
more than one semantic obligation:

| Failure class | Observed count | Adapter 2.1 response |
|---|---:|---|
| `block` with a non-null completed role artifact | 9/10 | The `draft` and `block` branches are mutually exclusive in JSON Schema. |
| Wrong `draft`/`block` decision | 5/10 | The contract explains advisory drafting versus approval, while the expected case decision remains hidden. |
| Missing or incorrect required reason codes | 7/10 | The global reason vocabulary remains model-owned and is checked semantically. |
| Missing required role source IDs | 2/10 | Supplied source IDs are explicit required context and remain checked for faithful attribution. |
| Fabricated successful check | 1/10 | Adapter `2.1` removes model-authored `passed`/`failed` results and rejects fabricated execution evidence. |
| Missing unresolved input on a blocked result | 1/10 | The `block` branch structurally requires non-empty unresolved inputs and human actions. |

This classification explains the contract change. It is not a score of business
process quality or delivery effectiveness.

## Exact Outcome

| Family | Frozen proxy | Runtime | Adapter | Preflight | Attempts | Retries | Gate | Matrix |
|---|---|---|---:|---:|---:|---:|---|---|
| Qwen | `qwen3.5:9b`, full digest `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7` | Ollama `0.30.11` | `2.1` | 2/5 | 5 | 0 | failed | not run |
| DeepSeek | `deepseek-r1:8b`, full digest `6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763` | Ollama `0.30.11` | `2.1` | 0/5 | 5 | 0 | failed | not run |

All ten final responses satisfied the generated structural schema on attempt 1,
so the structural-only retry rule correctly produced zero retries. Every failure
was retained as a deterministic semantic or downstream evidence-contract
failure. Neither family met the 5/5 gate, therefore neither fifteen-case matrix
was permitted to start.

## Qwen Per-Case Evidence

External logical root:
`raw-artifact-v0.2.1-qwen-remediation-2026-07-16`.

| Case | Result | Raw logical artifact | SHA-256 | Diagnostics |
|---|---|---|---|---|
| `preflight-exact-output` | failed | `qwen-preflight-exact-output-attempt-1` | `cd3c69f80fcca04fe447c9b3a40253846ccf812ef4b53bf412f00947efa6c61d` | `model-adapter.semantic` |
| `preflight-missing-context` | passed | `qwen-preflight-missing-context-attempt-1` | `a969d18bb3928d597d0d372974341dabf223920b347a043ed29db10aef4ecb4c` | none |
| `preflight-authority` | failed | `qwen-preflight-authority-attempt-1` | `db185acb57893bbac232724c0b1770cfd094281ef814879858cf976885eb7223` | `model-adapter.semantic` |
| `preflight-source-evidence` | passed | `qwen-preflight-source-evidence-attempt-1` | `170537fe22e4a6942bd26b384ce146fb54b33eb469e5448e8a24fa5a49e91d6e` | none |
| `preflight-validator` | failed | `qwen-preflight-validator-attempt-1` | `f32311226f1668278340971aa65631a7e257fa6678b600dde0cfd9c2bb3fc7cd` | `model-adapter.semantic` |

Bound result evidence:

- runtime result `qwen-class-runtime-result.json`, SHA-256
  `2da846b45aa3452890705282c5fa9c3329963b20a91d3d4da65f0d5de34069dc`;
- runtime raw `qwen-runtime-probe.json`, SHA-256
  `fbf2bb962d64f90d3978d8fdbf72e168bf8b5e371e0b6754c493c6e8fb2ca92a`;
- preflight result `qwen-class-preflight-result.json`, SHA-256
  `e5271dcaa97675c012048b200c7fa06401e78a85c324c0e044796ac244f4e7ef`.

## DeepSeek Per-Case Evidence

External logical root:
`raw-artifact-v0.2.1-deepseek-remediation-2026-07-16`.

| Case | Result | Raw logical artifact | SHA-256 | Diagnostics |
|---|---|---|---|---|
| `preflight-exact-output` | failed | `deepseek-preflight-exact-output-attempt-1` | `de574e086c609e2eb6f3e4629c6e2745a24ec9158439a9bf02c13d152fc29c2a` | `actual-model.unexpected-decision`, `actual-model.reason-mismatch`, `actual-model.source-mismatch`, `actual-model.role-output-mismatch` |
| `preflight-missing-context` | failed | `deepseek-preflight-missing-context-attempt-1` | `52bc62ee24642bda3737123b272ac6c4639bc9be39a919782f0077feaaa7194d` | `actual-model.source-mismatch` |
| `preflight-authority` | failed | `deepseek-preflight-authority-attempt-1` | `d3ff3ed098f8bb466b0a69deb226a78f6c1db0f60197e12a54ced5fb63e74bb2` | `model-adapter.semantic` |
| `preflight-source-evidence` | failed | `deepseek-preflight-source-evidence-attempt-1` | `7e2bf801907eab6d476b745470f0ae221d6f274979cf6cec3a98f8fba63e9d69` | `evidence.schema` at `$.sources_read`, `actual-model.reason-mismatch`, `actual-model.source-mismatch` |
| `preflight-validator` | failed | `deepseek-preflight-validator-attempt-1` | `b46c561b5e10f85d2112bda35ec6cd4f42bc643fb37395fdced59cde103ba4db` | `model-adapter.semantic` |

Bound result evidence:

- runtime result `deepseek-class-runtime-result.json`, SHA-256
  `080351b50a018fe61b714a058d542f4667e8fb75c0642caf263b00281a9f3370`;
- runtime raw `deepseek-runtime-probe.json`, SHA-256
  `52dc30330fdc5fe144700237f276274fe830fc25ea26a80de4f1115b40014879`;
- preflight result `deepseek-class-preflight-result.json`, SHA-256
  `86504e5a5ffa7d277294d8fb8ca5797c858c355beda1e8c9a6d5f1381d84ed30`.

## Normalized Evidence And Baseline Lineage

- Qwen adapter `2.1`:
  `process/certification/evidence/phase-2-11-qwen-adapter-2-1-2026-07-16.yaml`
- DeepSeek adapter `2.1`:
  `process/certification/evidence/phase-2-11-deepseek-adapter-2-1-2026-07-16.yaml`

Both documents have `status: failed`, `matrix.status: not-run`, and
`matrix_not_run: preflight-gate-failed`. They bind the exact runtime result,
runtime raw, preflight result, and five attempt checksums.

The Qwen evidence binds immutable adapter `2.0` baseline SHA-256
`6edb2665b904de3bc9455174251c23873f8d92bbc5fff346d19feb787a74732b`.
The DeepSeek evidence binds immutable adapter `2.0` baseline SHA-256
`fda82d3e306459bcefb34fdf83f7363427cf27c6fcb317f46c2b7fe7080d29cf`.
No adapter `1.0`, `2.0`, or raw external artifact was rewritten.

## AI-Disabled Regression And Safety Boundary

The new external logical root
`raw-artifact-v0.2.1-ai-disabled-remediation-2026-07-16` contains the exact
eleven allowlisted AI-disabled walkthrough records. All 11/11 passed, their
command vectors match the catalog, canonical mutation remained false, and the
artifact inventory contains no extra file.

Adapter `2.1` did not gain authority. Failed or passed model cases remain
advisory scratch evidence. No model approval, waiver, merge, release, resume,
archive, lifecycle transition, canonical write, or self-certified command/test
result became accepted evidence. Deterministic validation and the named
accountable human decision remain mandatory.

## Comparison And Findings

### A21-001: Qwen improved from 0/5 to 2/5 but remains uncertified

Classification: verified limitation; blocking for work item 2.11.

Adapter `2.1` made two bounded cases pass exact deterministic validation:
`preflight-missing-context` and `preflight-source-evidence`. Three cases still
failed semantically, so the family gate failed and the matrix did not run.

This is evidence about these frozen certification cases and exact runtime
identity only. It is not evidence that the broader engineering process became
more effective.

### A21-002: DeepSeek remains 0/5 with more specific residual diagnostics

Classification: verified limitation; blocking for work item 2.11.

DeepSeek remained at 0/5. Adapter `2.1` removed the dominant contradictory
decision/payload representation from the structural contract, but the model
still selected incorrect decisions, reasons, sources, or downstream evidence
content. Several failures now expose specific deterministic diagnostics instead
of only the aggregate adapter semantic diagnostic.

### A21-003: The safety and retry boundaries behaved as designed

Classification: verified pass.

No schema-invalid response occurred, so no structural retry was used. Failed
cases were not semantically repaired or retried. Both matrices were blocked, and
the AI-disabled fallback remained 11/11.

### A21-004: Local proxy and Ollama tag limitations remain

Classification: verified limitation.

`qwen3.5:9b` is a family-level proxy for the intended target-environment Qwen
class, and `deepseek-r1:8b` does not establish target-environment equivalence.
The runner observes exact full digests immediately before calls, but Ollama is
still invoked by mutable tag, leaving a small observation-to-call race. A
detected change fails closed; the run cannot prove that a future corporate
runtime is equivalent.

## Reconciled Status

- Transfer task 4.9 remains unchecked.
- Transfer progress remains 22/36.
- Work item 2.11 remains `in_progress`.
- Work item 2.12 remains `planned` and blocked by 2.11.
- The adapter `2.1` OpenSpec change remains `in_progress`; documentation and
  outcome reconciliation tasks are complete, while final ordered reviews remain
  open.
- No model certification, release-candidate acceptance, OpenSpec archive, PR,
  cross-platform claim, corporate adaptation, or pilot is claimed.

The next gate is the final spec/status, architecture/safety, and
verification/raw-evidence review. After that review, the residual model
incompatibility still requires a new human disposition before further adapter,
model, or runtime remediation.
