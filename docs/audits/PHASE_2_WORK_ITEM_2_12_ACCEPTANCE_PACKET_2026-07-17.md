# Phase 2 Work Item 2.12 Acceptance Packet

Date: 2026-07-17
Packet status: `evidence-complete`
Human acceptance decision: pending

This packet assembles the exact machine evidence offered to the human release owner. It can become `evidence-complete`; it cannot record or imply the human acceptance decision.

## Immutable Candidate

- Release ID: `phase-2-12-rc7`.
- External logical candidate: `<external-release-root>/phase-2-12-rc7-20260717`.
- Payload SHA-256: `f0fb1d7c6478fd3eedcaa6de26242870478ebfdbc2ca6b76356dc094f1d6f63f`.
- Manifest SHA-256: `9a27a2ef036ac90774b60265b39fdc298fead01170437fff0d131aa70f38b301`.
- Prior passing candidate `phase-2-12-rc6` remains preserved as release history and is superseded only for this review-fix candidate.

## Evidence References

- Release manifest: `process/release/release-manifest.yaml` (SHA-256 `9a27a2ef036ac90774b60265b39fdc298fead01170437fff0d131aa70f38b301`).
- Windows evidence: `process/release/evidence/phase-2-12-windows-2026-07-17.yaml` (SHA-256 `d3f81ae48cfdeeda8fb3dacccdc7867d4cb765f0e976e74c347e22258334c44b`).
- Linux/WSL2 evidence: `process/release/evidence/phase-2-12-linux-wsl2-2026-07-17.yaml` (SHA-256 `a29ad8a3364f0ccde6b62a1051cbda33ca29598bb7001d1f667cff6f0504ae7c`).
- Raw selector snapshot: `<external-raw-acceptance-root>/phase-2-12-raw-acceptance-20260717`.
- Selected Qwen normalized evidence: `process/certification/evidence/phase-2-11-qwen-adapter-2-2-2026-07-17.yaml`.
- Selected Qwen raw logical root: `raw-artifact-v0.2.2-qwen-2026-07-17-certified-policy-v3`.
- Selected DeepSeek normalized evidence: `process/certification/evidence/phase-2-11-deepseek-adapter-2-2-2026-07-17.yaml`.
- Selected DeepSeek raw logical root: `raw-artifact-v0.2.2-deepseek-2026-07-17-certified-policy-v9`.

## Commands And Results

- Targeted verification: `python -m pytest tests/test_certification.py tests/test_release_candidate.py tests/test_process_package.py -q` -> `140 passed, 3 skipped in 70.26s`.
- Candidate build and validation -> `phase-2-12-rc7`, payload and manifest hashes above, `status: valid`.
- Windows full clean rehearsal -> `rehearsal-complete`; Windows 11 `10.0.26200`, AMD64, Python 3.13.14, Node 24.16.0, OpenSpec 1.4.1, Git 2.54.0.windows.1, PowerShell, MCP explicitly unavailable.
- Native WSL2 portability smoke -> `rehearsal-complete`; Ubuntu 24.04 / WSL2 kernel 6.6.114.1, OS probe x86_64, Python 3.12.3, Node 22.23.1, OpenSpec 1.4.1, Git 2.43.0, Bash, MCP explicitly unavailable.
- Final exact-host/raw-root acceptance -> `evidence-complete`, diagnostics `[]`, `human_acceptance_required: true`.
- Windows junction plus WSL2 root and descendant links -> `release.link-forbidden`, exit 1.

## Negative Acceptance Matrix

Both host records passed all seven required cases: missing, stale, failed, private, AI-only, checksum mismatch, and payload mismatch.

## Rollback And Archive Parity

Windows and WSL2 both report rollback `passed`. Archive digest before and after on both hosts is `50b61ec58babe87726d2af58995c13f7f58007ef3691854f6ab2a0045ab7f635`.

## Limitations

- macOS is not certified.
- WSL2 portability smoke is not native bare-metal Linux certification.
- MCP availability is recorded from each host and does not weaken AI-disabled fallback requirements.
- Machine `evidence-complete` status is not human acceptance.

## Human Decision Gate

- `human_acceptance_required`: `true`.
- Final human decision: pending.
- Phase 3 may not treat this packet as acceptance until the authorized human owner records a separate explicit decision.
