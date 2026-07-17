# Phase 2 Work Item 2.12 Release Audit

Date: 2026-07-17
Status: passed with remediated findings
Scope: immutable external release candidate, Windows full rehearsal, Linux/WSL2 portability smoke, negative acceptance, update/rollback, archive preservation, privacy, and repository reconciliation.

## Boundary And Criteria

This audit evaluates the accepted work item 2.12 contract only. It does not certify macOS, a native bare-metal Linux distribution, a corporate runtime, MCP provisioning, or human release acceptance.

Pass criteria:

1. one candidate is built into a new external destination and validated before rehearsal;
2. Windows executes the full clean rehearsal and Linux on native WSL2 storage executes the bounded portability smoke from byte-identical candidate content;
3. missing, stale, failed, private, AI-only, checksum-mismatched, and candidate-mismatched evidence is rejected with stable codes;
4. migration check/apply/idempotency, update, failed-update hold, rollback, and accepted archive history preservation pass;
5. Windows reparse/junction and POSIX root/descendant links are rejected;
6. both host evidence records bind the same payload and manifest and produce `evidence-complete` without substituting human acceptance;
7. the complete repository suite and final OpenSpec/governance/privacy/diff gates pass after reconciliation.

Severity scale: Critical blocks the accepted safety or authority contract; High blocks transfer readiness; Medium requires correction before work-item closure; Low is a non-blocking follow-up.

## Final Candidate

- Release ID: `phase-2-12-rc6`.
- External Windows path: `<external-release-root>/phase-2-12-rc6-20260717`.
- Native WSL2 copy: `/root/teamSsdCli-release-artifacts/phase-2-12-rc6-20260717`.
- Payload SHA-256: `232e3da5737f569fe90cb32901f876103ec4a9fb0091abe46fe005502e1e4d43`.
- Manifest SHA-256: `e1b362bb2dad779e7c3a6ebe2657a356f75ce2bd3f544510e491d74873b69e2c`.
- The native WSL2 manifest checksum and semantic payload validation matched the Windows candidate before execution.
- Repository copies: `process/release/release-manifest.yaml` and `process/release/evidence/phase-2-12-*.yaml`.

Earlier `rc1` through `rc5` directories remain external rejected/diagnostic history. They are not accepted candidates and were not deleted or silently reused.

## Raw Certification Closure

The supplied `<user-documents>/certifications` directory actually contained 21 intermediate v0.2.2 roots, not only the final selected roots. No source directory was deleted or rewritten. A new external snapshot named `phase-2-12-raw-acceptance-20260717` was created under the ignored release-artifact root containing exactly:

- `raw-artifact-v0.2.2-qwen-2026-07-17-certified-policy-v3`;
- `raw-artifact-v0.2.2-deepseek-2026-07-17-certified-policy-v9`.

Each root contained 24 files. All 48 destination SHA-256 values matched their source bytes. The selector-owned normalized evidence revalidated against those exact roots from the packaged candidate.

## Host Evidence

### Windows Full Rehearsal

- Windows 11 `10.0.26200`, AMD64.
- Python `3.13.14`; Node `24.16.0`; OpenSpec `1.4.1`; Git `2.54.0.windows.1`; PowerShell.
- MCP: `explicitly-unavailable`, with no fabricated reference.
- Result: `passed`.
- Negative acceptance: 7/7 expected rejection cases passed.
- Rollback: `passed`.
- Archive digest before/after: `50b61ec58babe87726d2af58995c13f7f58007ef3691854f6ab2a0045ab7f635`.
- A real NTFS junction reported `ReparsePoint` and validation rejected it with `release.link-forbidden`, exit `1`.

### Linux/WSL2 Portability Smoke

- Ubuntu 24.04 on WSL2 kernel `6.6.114.1-microsoft-standard-WSL2`, x86_64.
- Python `3.12.3` in a native venv with PyYAML `6.0.3` and jsonschema `4.26.0`; native Node `22.23.1`; native OpenSpec `1.4.1`; Git `2.43.0`; Bash.
- `python3.12-venv` was provisioned locally in WSL2; no machine-local state was committed.
- MCP: `explicitly-unavailable`, with no fabricated reference.
- Result: `passed`.
- Negative acceptance: 7/7 expected rejection cases passed.
- Rollback: `passed`.
- Archive digest before/after: `50b61ec58babe87726d2af58995c13f7f58007ef3691854f6ab2a0045ab7f635`.
- Real POSIX root and descendant symlinks were rejected with `release.link-forbidden`, exit `1`.

### Cross-Host Acceptance

The exact host roots contained only `windows.yaml` and `linux-wsl2.yaml`. Windows and WSL2 acceptance each returned:

```text
status=evidence-complete
diagnostics=[]
human_acceptance_required=true
```

The records matched on payload SHA-256, manifest SHA-256, package/config identity, scenario codes, negative-case IDs/codes/results, update/failed-hold/rollback outcomes, privacy and AI-disabled flags, human-authority boundary, and archive digest. Platform inventory remained separate as required.

## Findings And Remediation

### F-001: Windows OpenSpec shim was not executable with shell disabled

- Classification: verified defect, High.
- Evidence: the first Windows rehearsal returned `release.inventory-failed`; direct Python execution could not launch the PowerShell shim, while `openspec.cmd --version` passed.
- Root cause: fixed logical argv was passed directly instead of resolving its executable with `PATHEXT`.
- Remediation: resolve only the executable through `shutil.which`, preserve the canonical recorded argv, and keep `shell=False`.
- Verification: RED Windows-shim regression, then focused GREEN.

### F-002: Archive fixture bytes differed across hosts

- Classification: verified defect, Critical for cross-host archive equivalence.
- Evidence: Windows archive digest `a6eb3518...` differed from Linux `50b61ec5...`; hex inspection showed CRLF versus LF.
- Root cause: the synthetic accepted-history file used platform-default newline translation.
- Remediation: force `newline="\n"` and assert exact LF bytes.
- Verification: RED byte assertion, focused GREEN, then identical rc6 archive digest on both hosts.

### F-003: Candidate omitted declared canonical certification sources

- Classification: verified defect, High.
- Evidence: packaged `validate_normalized_evidence` returned `actual-model.gate-raw-evidence-missing`; four source-manifest paths were absent from payload.
- Root cause: `process/package.yaml` declared `canonical_sources`, but the candidate builder and closure validator ignored them.
- Remediation: copy and close exactly the already-declared canonical files.
- Verification: RED inclusion test, focused GREEN, then both selected model-family records revalidated from rc6.

### F-004: Privacy scanner misclassified allowed localhost endpoints

- Classification: verified defect, High.
- Evidence: the drive-path alternative matched `p:/` inside `http://127.0.0.1:11434`.
- Root cause: an unbounded drive-letter regular-expression alternative.
- Remediation: require a non-alphanumeric token boundary before a drive letter while retaining Windows user-path rejection.
- Verification: RED localhost-versus-Windows-path regression, focused GREEN, and rc6 acceptance with no privacy diagnostics.

### F-005: Initial full suite exposed incomplete reconciliation

- Classification: verified defect, Medium.
- Evidence: `681 passed, 4 skipped, 5 failed in 205.02s`; four failures shared one unmapped new OpenSpec scenario, and one exact schema inventory test omitted the two Task 2 release schemas.
- Root cause: Task 3 coverage reconciliation and Task 2 schema test registration were incomplete.
- Remediation: map `Supported hosts produce proportionate governed evidence` to both platform evidence paths, remove its obsolete future-work row, and register both schemas.
- Verification: all five failing nodes passed in `3.80s`; the necessary final full-suite rerun passed `686 passed, 4 skipped in 200.47s`.

## Residual Risks And Limitations

- macOS is explicitly `not-certified`.
- WSL2 proves the accepted Linux portability contour, not native bare-metal Linux certification.
- MCP was explicitly unavailable on both hosts; the runbook defines the provisioned path, but this run does not certify a live MCP integration.
- The Linux inventory records architecture as `unknown` because the cross-platform evidence implementation reads the Windows-specific `PROCESSOR_ARCHITECTURE` environment variable. The OS probe independently records x86_64. This is a Low follow-up and does not alter candidate identity, required scenario results, dependency compatibility, or acceptance.
- `evidence-complete` is machine evidence closure only. Human release acceptance remains mandatory before Phase 3.

## Remediation Decision

All Critical, High, and Medium findings within the accepted 2.12 contract were remediated before rc6. The Linux architecture display improvement is recorded as a non-blocking follow-up rather than expanding the stable candidate after final verification.
