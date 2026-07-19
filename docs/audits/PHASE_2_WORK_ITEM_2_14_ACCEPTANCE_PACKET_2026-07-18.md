# Phase 2 Work Item 2.14 Human Acceptance Packet

Date: 2026-07-18

Decision status: pending human owner.

## Candidate Identity

| Field | Value |
|---|---|
| Release | `phase-2-14-rc4` |
| Payload SHA-256 | `4159e43961c5c59005d63fb6f305f9b0b5bac18517f8fd02d3e6b27e711ed6e1` |
| Manifest SHA-256 | `33aa240261ed0a660a3fc6b7ef85d847215cf5a3cd1f5afb423f28ca45cd02cb` |
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
- complete coverage inventory: `process/certification/coverage.yaml`;
- scenario-to-evidence and residual-risk rows: `process/certification/evidence-manifest.yaml`.
- residual-gap provenance and routing: `docs/audits/PHASE_2_RESIDUAL_GAPS_PROVENANCE_AND_ROUTING_AUDIT_2026-07-19.md`.

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

## Source-Linked Role And Security Readiness

- Tech Lead evidence: both normalized model documents contain the `tech-lead-major`, authority-boundary, unsafe-resume, and forbidden-lifecycle results with deterministic validation, accountable human routes, source manifests, and no forbidden action. The AI-disabled 11/11 result independently proves the fallback path.
- QA evidence: both normalized model documents contain `qa-hotfix` and insufficient-QA-evidence results with deterministic validation, configured human QA ownership, source manifests, and no authority substitution. Windows and WSL2 host records independently bind negative and rollback evidence to rc4.
- Security applicability: a separate security approval is not required for this external synthetic candidate because it contains no real corporate values, credentials, endpoints, integrations, or private datasets. Security evidence is nevertheless present through package secret/privacy validation, host privacy scans, raw-output exclusion, negative credential cases, and the corporate-adaptation no-secret/no-fork checks. Real data classification, secrets, endpoints, integrations, retention, and security approver routing become mandatory Phase 3 inputs.
- These records support the human decision; they are evidence, not AI approval. The human owner still accepts or rejects rc4 and its 110 explicit missing-evidence rows. The 2026-07-19 audit confirms that the rows use mechanically uniform fallback metadata and are not 110 independently assessed risks.

## Residual-Gap Clarification (2026-07-19)

The 110 rows were created when broad default/file-level coverage was replaced with exact source-local scenario evidence. They prove that rc4 has no accepted exact evidence binding for those selectors; by themselves they do not prove missing product behavior or equal risk.

The complete 46-requirement inventory routes the rows as follows:

- 75 to Phase 2 exact-evidence review;
- 22 to historical/ongoing governance and manual evidence;
- 2 to real Phase 3 corporate adaptation/pilot evidence;
- 10 to the explicitly later Phase 4 Confluence/publication layer;
- 1 to the Phase 2 accepted scope-boundary decision.

Rc4 is immutable, so this clarification does not rewrite its manifest. Acceptance carries the unresolved exact-evidence debt and coarse fallback metadata into a monitored Phase 3 pilot. Requiring corrected row-level evidence means rejecting rc4 and creating a fully recertified successor candidate.

## Review Decision Needed

The owner should choose one outcome:

1. **Accept rc4 for entry into Phase 3 corporate adaptation.** Recommended only if the listed limitations, unresolved exact-evidence debt, and mechanically coarse gap metadata are acceptable for a monitored pilot. Acceptance authorizes real configuration and approved wiring; it does not approve production deployment, independently validate all 110 risk levels, or waive Phase 3 gates.
2. **Reject rc4 and require additional evidence.** Name the specific residual gap, platform, integration, privacy classification, or proxy-equivalence concern that must be closed. Phase 3 remains blocked and no model rerun is implied unless the requested correction changes a model-bound contract.

## Risks Requiring Explicit Awareness

- macOS and native bare-metal Linux are not certified.
- Qwen/DeepSeek are local family proxies, not corporate-runtime equivalence proof.
- MCP was unavailable in the external rehearsal.
- Real corporate secrets, endpoints, mappings, owners, privacy/retention values, and pilot evidence are intentionally absent.
- 110 scenarios have no accepted exact evidence binding in rc4. Their stored `risk: medium` value is a bulk fallback rather than an individual assessment; the 2026-07-19 audit provides the five-way phase/evidence routing.
- Derived NIS/PPRB summaries need human data-classification confirmation before external publication.

Phase 3 and any corporate pilot remain blocked until the owner records an explicit acceptance decision.
