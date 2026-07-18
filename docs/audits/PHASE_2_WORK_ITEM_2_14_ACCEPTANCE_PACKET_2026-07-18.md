# Phase 2 Work Item 2.14 Human Acceptance Packet

Date: 2026-07-18

Decision status: pending human owner.

## Candidate Identity

| Field | Value |
|---|---|
| Release | `phase-2-14-rc2` |
| Payload SHA-256 | `c6efeb177f9e4a02a7590a34b2658f398e048cc3e8d5cb9bfe2083c2aaa55ccf` |
| Manifest SHA-256 | `97cccd5d360a47135b092a6de7451f9b800bbf9a996839640502b8475051ae7f` |
| Package/config | `0.2.0` / `1.1` |
| Manifest inventory | 194 files, zero bytecode/cache entries |
| Raw model evidence | 48 checksum-bound files in two complete external roots |
| Machine status | `evidence-complete`; human acceptance still required |

Tracked review artifacts:

- manifest: `process/release/phase-2-14-release-manifest.yaml`;
- Windows: `process/release/evidence/phase-2-14-windows-2026-07-18.yaml`;
- Linux/WSL2: `process/release/evidence/phase-2-14-linux-wsl2-2026-07-18.yaml`;
- Qwen: `process/certification/evidence/phase-2-14-qwen-adapter-2-2-2026-07-18.yaml`;
- DeepSeek: `process/certification/evidence/phase-2-14-deepseek-adapter-2-2-2026-07-18.yaml`;
- technical audit: `docs/audits/PHASE_2_WORK_ITEM_2_14_FINAL_TECHNICAL_AUDIT_2026-07-18.md`.

## Acceptance Evidence

- Windows full clean rehearsal: passed, including all three change classes, migration, update, failed-update hold, rollback, archive preservation, 7/7 negative cases, privacy, and AI-disabled execution.
- Linux/WSL2 portability smoke: passed against the byte-identical manifest, including migration/update/rollback, archive preservation, 7/7 negative cases, privacy, and AI-disabled execution.
- AI-disabled certification: 11/11 passed.
- Qwen: 5/5 preflight, then 15/15 matrix, all attempt 1.
- DeepSeek with `num_ctx=8192`: 5/5 preflight, then 15/15 matrix, all attempt 1.
- Deterministic model-evidence gate: all normalized/preflight/matrix bindings passed with no diagnostics.
- Final repository verification: focused regression `322 passed, 4 skipped`; complete suite `716 passed, 4 skipped`; strict OpenSpec validation 12/12; roadmap/OpenSpec validator 0 errors.
- Rollback evidence: passed on both hosts; accepted archive digest was unchanged.
- Human authority: no model or AI-disabled path approved, resumed, released, archived, mutated canonical state, or substituted a named human decision.

## Review Decision Needed

The owner should choose one outcome:

1. **Accept rc2 for entry into Phase 3 corporate adaptation.** Recommended only if the listed limitations and 110 explicit residual scenario gaps are acceptable for a monitored pilot. Acceptance authorizes real configuration and approved wiring; it does not approve production deployment or waive Phase 3 gates.
2. **Reject rc2 and require additional evidence.** Name the specific residual gap, platform, integration, privacy classification, or proxy-equivalence concern that must be closed. Phase 3 remains blocked and no model rerun is implied unless the requested correction changes a model-bound contract.

## Risks Requiring Explicit Awareness

- macOS and native bare-metal Linux are not certified.
- Qwen/DeepSeek are local family proxies, not corporate-runtime equivalence proof.
- MCP was unavailable in the external rehearsal.
- Real corporate secrets, endpoints, mappings, owners, privacy/retention values, and pilot evidence are intentionally absent.
- 110 medium residual scenarios have no exact executable evidence; they remain visible in the coverage report and route to this human gate.
- Derived NIS/PPRB summaries need human data-classification confirmation before external publication.

Phase 3 and any corporate pilot remain blocked until the owner records an explicit acceptance decision.
