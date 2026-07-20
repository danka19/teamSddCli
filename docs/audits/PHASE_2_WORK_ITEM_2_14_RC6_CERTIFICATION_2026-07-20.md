# Phase 2 Work Item 2.14 Rc6 Certification Audit

Date: 2026-07-20

Status: technically complete; pending explicit human acceptance

## Scope

This audit records the ordered successor remediation and certification requested after the `phase-2-14-rc4` residual-gap review. It covers the accepted first-MVP boundary, four focused tests, six-group product-gap intake, the three prioritized release-integrity contracts, successor freeze, fresh AI-disabled and actual-model execution, Windows/WSL2 rehearsal, aggregate acceptance evaluation, and independent review.

It does not record human release acceptance, corporate configuration, approved integration wiring, a real pilot, native bare-metal Linux certification, macOS certification, or corporate-runtime equivalence.

## Source Boundary

- Release-integrity implementation commit: `5f92fc6`.
- Fresh certification-selector commit: `4ffc44a`.
- Process package: `0.3.0`.
- Working and candidate coverage: `295 covered / 7 gaps / 32 future_work`.
- Complete repository verification: `736 passed, 4 skipped in 266.67s`.
- Focused actual-certification and release-candidate verification: `190 passed, 2 skipped`.
- Strict OpenSpec validation: 13 passed, 0 failed.
- Historical `process/release/` rc4 evidence was not rewritten.

## First-MVP Boundary And Product-Gap Disposition

Human decision `D-019` confirms that Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, real corporate wiring, and real pilot evidence do not block first-MVP transfer readiness. This is valid only because deterministic and AI-disabled operation remains complete, unavailable integrations are reported rather than fabricated, human gates remain mandatory, and the deferred work retains named Phase 3/4 ownership.

The selector review and remediation produced:

- 68 Phase 2 selectors with exact test evidence;
- 22 governance rows linked to primary audits and decisions;
- 12 Phase 3/4 rows classified as `future_work`;
- seven explicit later-phase product gaps retained in the candidate;
- six selected release-integrity selectors closed by Delta, archive-history, and reviewed-upgrade enforcement.

## Implemented Release-Integrity Contracts

### Delta operation semantics

Deterministic change validation now compares bounded Delta operations with the accepted capability baseline. It fails closed on reused `ADDED` names, non-substantive added requirements, `REMOVED` requirements without reason and migration, malformed or non-adjacent rename pairs, and renames that hide content changes. Stable diagnostics and positive remove/add, pure rename, modified, and legitimate addition cases are covered by exact tests.

### Archive history convention

Archive execution requires canonical `ready_to_archive` gate input, complete traceability, matching human approval, zero deterministic blockers, a dated sibling archive target, and the greppable subject `spec: archive <change-id>`. Path containment, collision, already-archived state, symlink/junction/reparse paths, and pre-mutation failures are rejected. Automation performs only the guarded local move; it receives no commit, merge, release, deployment, waiver, or approval authority.

### Reviewed upgrade evidence

Process-package update requires schema-v2, identity-bound reviewed evidence before any staging write. Evidence binds the change package, confirmed or corrected decision, proposal/tasks/delta topology, exact references and SHA-256 digests, strict OpenSpec outcome, applicable validator/template checks, and rollback-or-hold instructions. Derived result kind, status, producer, from/to versions, and change identity are validated. Missing, stale, mismatched, incomplete, unreviewed, or AI-only records leave the installed state unchanged.

## Fresh AI-Disabled And Model Evidence

AI-disabled execution produced 11 append-only scenario records; every command exited 0.

| Family | Runtime identity | Adapter | Preflight | Matrix | Gate diagnostics |
|---|---|---:|---:|---:|---|
| Qwen | `qwen3.5:9b`, Ollama `0.30.11` | `2.2` | 5/5 | 15/15 | none |
| DeepSeek | `deepseek-r1:8b`, Ollama `0.30.11` | `2.2` | 5/5 | 15/15 | none |

The models remain advisory-only. Qwen is a family proxy rather than proof of Qwen3.6-35B equivalence. DeepSeek is a frozen local family proxy rather than proof of target corporate runtime equivalence. Runtime, preflight, matrix, normalized result, raw logical root, source catalog, operation plan, and source hashes are recorded in the new evidence files.

## Candidate Freeze History

### Diagnostic rc5

`phase-2-14-rc5` was built from the reviewed source and passed manifest validation and both host rehearsals. Aggregate evaluation then rejected its model evidence with `actual-model.result-inventory-mismatch`. Root cause was exact: the derived raw bundle copied one superseded top-level runtime-probe file in addition to the declared `runtime-probe/` evidence. The file was checksum-bound by the release manifest but not declared by either normalized evidence document.

Rc5 was not edited or presented as accepted. It remains diagnostic rejected history.

### Final rc6

Rc6 was built from the same tracked source and normalized model evidence, using a new bundle containing only the declared 48 raw references.

| Field | Value |
|---|---|
| Release ID | `phase-2-14-rc6` |
| Payload SHA-256 | `172707ba159e1e060561d6d02ad67dcaf2fa4ce64a58c23bd9c55613713fd951` |
| Manifest SHA-256 | `0c7670637f1f59f82a6cae3bea48c53edfa3453d5fcf0c599bf013bd301c3146` |
| Payload inventory | 199 files |
| Raw closure | 48 exact checksum-bound references in two selected logical roots |
| Manifest validation | `valid` |
| Aggregate evaluation | `evidence-complete`, no diagnostics |
| Human acceptance | required and not yet recorded |

Independent review verified that all 199 payload inventory hashes equal tracked source bytes at `4ffc44a` and that no payload file is missing or different.

## Host Certification

### Windows

- Windows 11 `10.0.26200`, AMD64, PowerShell.
- Python `3.13.14`, Node `24.16.0`, OpenSpec `1.4.1`, Git `2.54.0.windows.1`.
- Full clean rehearsal passed.

### Linux/WSL2

- Ubuntu/WSL2 kernel `6.6.114.1`, Bash.
- Python `3.12.3`, Node `22.23.1`, OpenSpec `1.4.1`, Git `2.43.0`.
- Portability smoke passed.
- The distro lacked `pip`, `venv`, `referencing`, `rpds`, and a `python` command alias. Exact Linux wheels derived from the frozen `requirements-test.txt` were downloaded externally, expanded only into ephemeral `/tmp`, and exposed through `PYTHONPATH`; a temporary `/tmp` `python -> /usr/bin/python3` shim satisfied the fixed inventory argv. No system package or candidate byte was changed.

Both host records bind the same payload and manifest hashes and report:

- `result: passed`;
- `ai_disabled: true`;
- `human_authority_substituted: false`;
- `privacy_scan: passed`;
- rollback passed;
- identical archive digest before and after;
- every negative acceptance case passed.

## Independent Candidate Review

Final verdict: `READY`.

- Critical findings: none.
- Important findings: none.
- Minor findings: none.
- Specification compliance: ready.
- Code quality: ready.

The reviewer independently revalidated the manifest, payload inventory, tracked-source equality, raw closure, selected normalized evidence, host evidence, aggregate evaluator, release-integrity selectors, human-authority boundaries, and rc5 diagnostic disposition.

## Remaining Limitations And Gate

- `evidence-complete` and reviewer `READY` do not accept the release.
- The human owner must accept or reject exact rc6 at transfer task 7.4, NIS task 8.7, and Phase gate 2.14.4.
- No corporate configuration, approved integration wiring, or pilot has run.
- macOS is not certified.
- WSL2 is portability evidence, not native bare-metal Linux certification.
- Local Qwen and DeepSeek proxies do not establish corporate-runtime equivalence.
- Seven Phase 3/4 product gaps remain visible under `D-019`.

## Durable Evidence

- `process/release/phase-2-14-rc6-release-manifest.yaml`
- `process/release/evidence/phase-2-14-rc6-windows-2026-07-20.yaml`
- `process/release/evidence/phase-2-14-rc6-linux-wsl2-2026-07-20.yaml`
- `process/certification/evidence/phase-2-14-rc5-qwen-adapter-2-2-2026-07-20.yaml`
- `process/certification/evidence/phase-2-14-rc5-deepseek-adapter-2-2-2026-07-20.yaml`
- `docs/audits/PHASE_2_PRODUCT_GAP_CHANGE_INTAKE_2026-07-20.md`
- `docs/audits/PHASE_2_WORK_ITEM_2_14_RC6_ACCEPTANCE_PACKET_2026-07-20.md`

