# Phase 2 Work Item 2.11 Qwen Certification Audit — 2026-07-15

## Boundary And Criteria

This audit covers only the AI-disabled baseline and the Qwen-family slice of work item 2.11 on Windows. Criteria were: source-linked deterministic walkthroughs for every named NIS operation; preflight proof of exact output, missing-context stop, authority boundaries, canonical-source binding, no fabricated evidence, and deterministic validator acceptance; all four roles and all three classes; the complete Qwen negative matrix; append-only failed-run retention; privacy-safe normalized evidence; and no model-owned approval, resume, release, or lifecycle mutation.

Severity is `blocking | major | minor | limitation`. Evidence is classified as pass, verified defect, verified limitation, or unverified suspicion.

## Results

- Pass: 11/11 AI-disabled walkthrough records passed after a first retained package-schema failure. Transfer task 4.4 and NIS task 8.2 are complete.
- Pass: the short runtime retry returned exact `QWEN_PREFLIGHT_OK` with thinking disabled after the retained thinking/32 length failure.
- Major limitation: reviewer inspection found that the original 5/5 preflight and 15/15 matrix prompts embedded the expected answer. Those 20 raw outputs remain immutable but are reclassified as `invalidated` with reason `reviewer-leading-prompt`; they are not certification passes.
- Verified result after exact catalog-semantic revalidation: the frozen non-leading run passed 0/5 preflight cases and 1/15 matrix cases (`fabricated-evidence`). All four roles, all three classes, and all 11 required negative families were executed; ten negative families failed, so deterministic or mandatory-human fallback is required and Qwen reliability is not established.
- Pass: the model independently selected its decision, role output, checks, claims, unresolved inputs, human decisions, and source IDs from case facts plus minimal authority-labelled source packs. Trusted code only normalized the returned envelope, bound selected IDs to exact hashes, and validated it; it did not insert semantic outcomes or claims.
- Pass: every current model row includes exact operation/model/runtime/digest/endpoint/adapter/package identity, case dimensions, read-pack and per-source hashes, raw logical filename/checksum, deterministic result, intervention, forbidden-action result, fallback, limitation, duration, token counts, and done reason. Raw-row cross-validation checks those fields against the append-only response.
- Pass: all 69 eligible actual-model raw files are covered by 20 current frozen rows and 49 invalidated or superseded Qwen entries. The failed-attempt ledger also retains the initial AI-disabled package-schema failure, bringing it to 50 entries; each has checksum, disposition, intervention, and fallback, while the 11 successful AI-disabled retry rows remain separate without double counting.
- Verified limitation (blocking for 2.11 closure): `qwen3.5:9b` is only a family-level proxy for corporate Qwen3.6-35B, not equivalence proof.
- Verified limitation (blocking for 2.11 closure): the Qwen-family proxy is unreliable on the honest non-leading contract and its failed operations remain routed to deterministic or mandatory-human fallback.
- Verified limitation (blocking for 2.11 closure): DeepSeek-family certification has not run. Transfer task 4.5 and NIS task 8.3 remain unchecked.
- Verified limitation (not part of this item): cross-platform release certification remains work item 2.12.

## Reproducible Evidence

- Catalog and runners: `process/certification/ai-disabled-walkthroughs.yaml`, `process/certification/qwen-matrix.yaml`, `process/actual_certification.py`, `scripts/run_actual_certification.py`, and `scripts/normalize_actual_certification.py`.
- Normalized record: `process/certification/evidence/phase-2-11-qwen-2026-07-15.yaml`.
- Raw artifact logical identity: `raw-artifact-v0.2.0-qwen-2026-07-15`; raw data is outside Git and referenced only by logical filename and SHA-256.
- Targeted verification and governance commands are recorded in the Phase 2 evidence index.

## Remediation Decision

No newly discovered product defect requires a new change. Work item 2.11 remains `in_progress`: its Qwen limitation/fallback disposition requires later release acceptance, and the same frozen non-leading matrix must still run against the mandatory DeepSeek family before transfer 4.5, NIS 8.3, or 2.11 can complete.
