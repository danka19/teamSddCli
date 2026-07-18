# Phase 2 Work Item 2.14.2 Final Technical Audit

Date: 2026-07-18

Status: passed; evidence-only review gates remain required before human acceptance.

## Certified Candidate

- Release ID: `phase-2-14-rc2`.
- Source commit at candidate construction: `08b4732434e69312c53a7c0bf22868f82a4522ab`.
- Payload SHA-256: `c6efeb177f9e4a02a7590a34b2658f398e048cc3e8d5cb9bfe2083c2aaa55ccf`.
- Manifest SHA-256: `97cccd5d360a47135b092a6de7451f9b800bbf9a996839640502b8475051ae7f`.
- Payload inventory: 194 files; Python bytecode/cache entries: 0.
- Raw manifest references: 48 files across the complete Qwen and DeepSeek roots.
- Machine acceptance: `evidence-complete`, no diagnostics, `human_acceptance_required: true`.

Candidate `phase-2-14-rc1` is retained as diagnostic history. It was not rehearsed or accepted because pre-rehearsal inspection found that host evidence IDs were still hard-coded to the historical Phase 2.12 series. Rc2 contains the corrected release-series binding.

## Deterministic Verification

| Gate | Result |
|---|---|
| Bytecode TDD | RED reproduced for `__pycache__`, `.pyc`, and `.pyo`; builder now excludes source bytecode and payload validation rejects it |
| Release-candidate focused tests | `80 passed, 1 skipped`; later selection/package regression `96 passed, 1 skipped` |
| Package/config/corporate-adaptation tests | `84 passed` |
| Actual-certification focused tests | `109 passed, 1 skipped` after context-binding correction |
| Coverage reconciliation tests | `48 passed, 2 skipped`; 334 effective scenarios = 204 covered + 110 explicit gaps + 20 later-work scenarios |
| Legacy template | `python scripts/validate_change.py --allow-placeholders templates/change` passed |
| Package validator | `python scripts/validate_corporate_adaptation.py --package --json` returned `valid` |
| Complete suite | `716 passed, 4 skipped in 241.87s` |
| OpenSpec | `openspec list` reports 33/36 transfer and 40/43 NIS tasks; `openspec validate --all --strict` passed 12/12 |
| Roadmap/OpenSpec consistency | Validator passed with 0 errors and two expected historical complete-but-unaccepted warnings |
| Privacy scan | Zero tracked raw-artifact paths, zero personal workspace paths, and no non-test high-confidence credential material; seven credential-like values are intentional fail-closed negative samples |

The 110 residual scenario gaps are not hidden or relabelled as passing. Each is routed to `phase-2.14-human-acceptance` with the compensation that the owner must accept the explicit residual risk or require exact evidence before Phase 3.

## AI-Disabled And Actual-Model Evidence

- AI-disabled: 11/11 passed; no canonical mutation or human-authority substitution.
- Qwen `qwen3.5:9b`, digest `6488c96f...893ea7`, Ollama `0.30.11`: 5/5 preflight and 15/15 matrix, all on attempt 1.
- DeepSeek `deepseek-r1:8b`, digest `6995872b...f5763`, Ollama `0.30.11`, `num_ctx=8192`: 5/5 preflight and 15/15 matrix, all on attempt 1.
- One normalization phase produced the two candidate-specific normalized documents.
- One aggregate gate-validation pass returned no diagnostics for AI-disabled, both normalized documents, both preflights, and both matrices.

Raw roots are external, append-only, and absent from Git:

| Root | Files | Canonical inventory digest |
|---|---:|---|
| `raw-artifact-v0.2.0-qwen-phase-2-14-2026-07-18` | 24 | `6f5a6b87f52f978ad5393352a21bc22e9401850c09e7736f99e925f11bb46500` |
| `raw-artifact-v0.2.0-deepseek-phase-2-14-2026-07-18` | 24 | `88278542b979f97c399eb037614f46d64f02a923b8c784ae19c6bce181fc97a2` |

## Platform Evidence

Windows 11 full rehearsal passed 14 scenarios, seven negative acceptance cases, update/failed-update hold/rollback, archive preservation, privacy, and AI-disabled operation. Linux/WSL2 passed the seven-scenario portability contour with the same payload and manifest, seven negative cases, rollback, archive preservation, privacy, and AI-disabled operation. MCP was explicitly unavailable on both hosts and no reference was fabricated.

The first WSL invocation retained a useful fail-closed diagnostic: executing the packaged entry point without `PYTHONDONTWRITEBYTECODE=1` created bytecode in its native candidate copy, which the new validator rejected. A fresh byte-identical copy with bytecode writes disabled then exposed missing venv activation in `PATH`; after explicit environment wiring, the accepted smoke passed. Neither failed setup produced passing host evidence.

## Findings Closed During The Gate

1. Release builder/validator admitted generated Python bytecode. Fixed with exclusion plus fail-closed validation and regression tests.
2. Adapter `2.2` gate revalidation omitted adapter-owned `num_ctx` when the model catalog did not duplicate `context_length`. Fixed without repeating the already valid Qwen preflight; saved raw bytes then passed revalidation.
3. Host evidence IDs were hard-coded to Phase 2.12. Fixed by deriving the release series from the manifest release ID; rc1 was superseded by rc2 rather than mutated.

No prompt, response schema, operation plan, authority/source semantics, model identity, or runtime profile changed after the actual-model sequence. No model was rerun.

## Remaining Limitations

- macOS is not certified.
- WSL2 is portability evidence, not native bare-metal Linux certification.
- The local Qwen and DeepSeek proxies do not prove corporate-runtime equivalence.
- MCP was explicitly unavailable during both host rehearsals.
- WSL2 architecture remains `unknown` in the structured field, while the OS probe independently records `x86_64`.
- Real corporate values, approved integration wiring, privacy/retention decisions, and the monitored pilot remain Phase 3 work.
- External publication classification of derived NIS/PPRB summaries remains a human decision.
- 110 explicit medium residual gaps require human risk acceptance or additional exact evidence before Phase 3.
