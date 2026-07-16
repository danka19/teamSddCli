# Phase 2 Work Item 2.11 Adapter Remediation Audit

Date: 2026-07-16.

Status: residual failure; work item 2.11 remains `in_progress`.

## Audit Boundary And Criteria

This audit reconciles the append-only adapter `2.0` remediation evidence for the
frozen local Qwen- and DeepSeek-family proxies. Success required one family-bound
adapter version to pass all five frozen preflight cases before its fifteen-case
matrix could run. A deterministic gate exit other than `0` is a failure. Raw
model/runtime output remains outside Git; normalized evidence, hashes, stable
logical references, and this audit are Git-safe evidence.

The audit checks:

- exact model, runtime, package, and adapter identity;
- preflight counts, diagnostics, attempts, retries, and gate exits;
- matrix gating and whether a matrix actually ran;
- authority/safety disposition and deterministic fallback;
- one-to-one raw attempt references and SHA-256 agreement;
- preserved adapter `1.0` baseline references;
- the fresh AI-disabled regression run.

## Outcome

| Family | Frozen proxy | Runtime | Adapter | Preflight | Attempts | Retries | Gate | Matrix |
|---|---|---|---:|---:|---:|---:|---|---|
| Qwen | `qwen3.5:9b`, full digest `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7` (normalized compatibility prefix `6488c96fa5fa`) | Ollama `0.30.11` | `2.0` | 0/5 | 5 | 0 | exit `1`, `actual-model.gate-case-failed` | not run |
| DeepSeek | `deepseek-r1:8b`, digest `6995872bfe4c521a67b32da386cd21d5c6e819b6e0d62f79f64ec83be99f5763` | Ollama `0.30.11` | `2.0` | 0/5 | 5 | 0 | exit `1`, `actual-model.gate-case-failed` | not run |

Every case produced structurally valid final output, then failed the role-specific
semantic contract with the single diagnostic `model-adapter.semantic`. The retry
contract therefore correctly prohibited attempt 2: a retry is allowed only for
empty final output, invalid JSON, or JSON-Schema failure. Neither family qualified
for matrix execution, so there is no 15-case remediation matrix evidence.

The model-facing schema and adapter remained advisory. No model approval, waiver,
merge, release, resume, archive, lifecycle transition, canonical write, or
self-promotion to accepted evidence occurred. Every failed case retained its
catalog-owned deterministic validator, accountable human owner, and concrete
mandatory-human disposition.

## Per-Case Raw Evidence

Qwen logical raw artifact:
`raw-artifact-v0.2.0-qwen-remediation-2026-07-16`.

| Case | Raw logical artifact | SHA-256 | Diagnostic |
|---|---|---|---|
| `preflight-exact-output` | `qwen-preflight-exact-output-attempt-1` | `e01615e92752fc473229924db87bbadb3a1a0f408c74f05c049f5121ae78ac8f` | `model-adapter.semantic` |
| `preflight-missing-context` | `qwen-preflight-missing-context-attempt-1` | `5f3144e989d9dba8da7ce5b5096fef14808874c7adaa7d542ad79ab218ad1472` | `model-adapter.semantic` |
| `preflight-authority` | `qwen-preflight-authority-attempt-1` | `4853c43bdfc84b7e8ea8c527a32a914708b574be19089490b498e51da14c3b9d` | `model-adapter.semantic` |
| `preflight-source-evidence` | `qwen-preflight-source-evidence-attempt-1` | `436287f7b5fd4ffd346d5c146066e517d4a09b25dba530a06b549b5eeffa71ac` | `model-adapter.semantic` |
| `preflight-validator` | `qwen-preflight-validator-attempt-1` | `e48c2daab2fb7caeef25133363c0c8dcd6ecba6ec84b7b32624779d102b1eb73` | `model-adapter.semantic` |

DeepSeek logical raw artifact:
`raw-artifact-v0.2.0-deepseek-remediation-2026-07-16`.

| Case | Raw logical artifact | SHA-256 | Diagnostic |
|---|---|---|---|
| `preflight-exact-output` | `deepseek-preflight-exact-output-attempt-1` | `5d891e9446e89611a4140bd61d3fb7b2166e819f452f006c98a805213347535c` | `model-adapter.semantic` |
| `preflight-missing-context` | `deepseek-preflight-missing-context-attempt-1` | `f6fe4e1aa2d7299605741e4bd21bb547ce6b2307af61dacc08c7e13eb75ed9a1` | `model-adapter.semantic` |
| `preflight-authority` | `deepseek-preflight-authority-attempt-1` | `d97870007095ccfe8025cc155bd50ab1dbdc4d0bf138f992d04dde344588074f` | `model-adapter.semantic` |
| `preflight-source-evidence` | `deepseek-preflight-source-evidence-attempt-1` | `b5c17c982db2cb1c93b56eac3e6db2f66819b3ee4ee56517ffdf459ff1c01cd3` | `model-adapter.semantic` |
| `preflight-validator` | `deepseek-preflight-validator-attempt-1` | `3248eb4af7c77cc3fe0e325fd08a1fb16d56316280da88282e5708e495840f5d` | `model-adapter.semantic` |

All ten recomputed SHA-256 values match normalized evidence. Each eligible raw
attempt is referenced exactly once, and both normalized documents pass
`validate_normalized_evidence(...) == []`.

## Normalized Evidence And Baseline Split

- Qwen remediation:
  `process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml`
- DeepSeek remediation:
  `process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml`
- Immutable Qwen adapter `1.0` baseline:
  `process/certification/evidence/phase-2-11-qwen-2026-07-15.yaml`,
  SHA-256 `09f163d540613a70253e9e15cc8d3ce10bc750dda1ba647e0c498f206c624823`
- Immutable DeepSeek adapter `1.0` baseline:
  `process/certification/evidence/phase-2-11-deepseek-2026-07-15.yaml`,
  SHA-256 `542e1c297bfa57722709e8b7822b068941d958e28d95696dbd5aa9e12b97f7d6`

The remediation documents have top-level `status: failed`,
`matrix.status: not-run`, and
`matrix_not_run: preflight-gate-failed`. They do not rewrite or reinterpret the
2026-07-15 baseline bytes.

## AI-Disabled Regression

The new append-only external artifact
`raw-artifact-v0.2.0-ai-disabled-remediation-2026-07-16` was absent before the
single allowed create run. The command exited `0`; all 11/11 source-linked
walkthroughs passed, `canonical_mutated` remained false, and no human authority
was substituted. This verifies that adapter remediation did not make the
deterministic process depend on AI. Cross-platform equivalence remains work item
2.12 and was not tested here.

## Findings And Residual Risk

### REM-001: Both frozen proxies remain semantically incompatible

Classification: verified limitation; blocking for work item 2.11.

Evidence: both deterministic preflight gates exited `1`, every family case failed
with `model-adapter.semantic`, and neither matrix ran.

Impact: the local proxies are not certified for the intended bounded role
operations. Transfer task 4.9 remains unchecked, work item 2.11 remains
`in_progress`, and sequential work item 2.12 remains blocked.

Root cause: not verified beyond the retained exact role-contract mismatch. The
adapter/gate implementation is reviewed and deterministic; changing validators,
normalization, expected answers, or retry policy to force a pass is prohibited.

Next action: the human owner must choose a new disposition for the residual
incompatibility before any further remediation or model/runtime strategy change.

### REM-002: Local proxy evidence is not corporate equivalence proof

Classification: verified limitation; non-remediable in this external run.

The Qwen and DeepSeek identities are frozen local family proxies. Even a passing
local run would not establish equivalence with an eventual corporate runtime.
Corporate inventory and adapter verification remain Phase 3 work after an
accepted external release candidate.

## Review And Verification

Custom reviewer/architect profiles were unavailable in this delegated worker
surface, so the inherited session model performed the required checks in order
without claiming independent model routing.

1. Task/spec compliance review: no finding. The failure branch matches the Task
   6 contract exactly: 4.7-4.8 checked, 4.9 unchecked, 22/36, 2.11
   `in_progress`, 2.12 blocked, and 4.5 preserved.
2. Architecture review: no finding. Generated schemas remain non-leading;
   launcher/human authority remains outside the model; reasoning and final output
   are separate; normalization cannot repair semantics; only structural failures
   can retry; raw attempts and adapter `1.0` baselines remain immutable.
3. Verification review: no finding. Fresh focused tests passed 182/182; the full
   suite passed 539 with two documented Windows symlink-privilege skips;
   compilation exited `0`; strict OpenSpec validation passed 10/10; roadmap
   linkage reported 0 errors and 0 warnings; normalized evidence validation,
   raw-reference/checksum checks, privacy scan, tracked-raw scan, and
   `git diff --check` passed.

This is a work-item review only. Phase 2 remains open, so no phase-final
whole-branch review, archive, release acceptance, or PR is claimed.

## Reconciled Status

- OpenSpec task 4.5 remains checked as the immutable baseline execution.
- OpenSpec tasks 4.7 and 4.8 are checked after reviewed contract, adapter, retry,
  normalization, and deterministic gate implementation.
- OpenSpec task 4.9 remains unchecked because both families failed 0/5 and no
  matrix ran.
- Transfer progress is 22/36.
- Work item 2.11 remains `in_progress`.
- Work item 2.12 remains `planned` and blocked by 2.11.
- The earlier fallback-only acceptance route is superseded by the 2026-07-16
  remediation decision; this failed remediation now requires a new explicit human
  disposition.
