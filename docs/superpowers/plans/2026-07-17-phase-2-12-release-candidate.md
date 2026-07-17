# Phase 2.12 Release Candidate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify one immutable transfer candidate with deterministic manifest/acceptance behavior, one full Windows rehearsal, and one bounded equivalent Linux/WSL2 smoke plus negative cases.

**Architecture:** Add one focused `process.release_candidate` domain module and one thin CLI. Reuse existing bootstrap, compatibility, migration, update, rollback, and actual-certification validators; do not duplicate policy logic or introduce a framework. Build candidate bytes once, bind every evidence row to its digest, and consume the same candidate on both hosts.

**Tech Stack:** Python 3.11+, PyYAML 6.0.3, jsonschema 4.26.0, pytest, PowerShell 7+, Bash on WSL2 Ubuntu 24.04, OpenSpec 1.4.1, Node 20+, Git 2.40+.

## Global Constraints

- Windows is `full-clean-rehearsal`; Linux on WSL2 is `portability-smoke`; macOS is `not-certified` and must never be inferred.
- Manifest generation and validation are deterministic, non-interactive, AI-disabled, and fail closed.
- Candidate construction is single-owner; both rehearsals consume byte-identical candidate content.
- Missing, stale, failed, private, checksum-invalid, candidate-mismatched, or AI-only evidence blocks acceptance with stable operator-safe codes.
- Update/rollback and migration must preserve accepted OpenSpec/archive history byte-for-byte.
- Focused tests run while stabilizing; the complete suite runs exactly once after implementation and rehearsals stabilize.
- Do not rerun Qwen/DeepSeek certification; consume existing committed normalized evidence and external raw-artifact checksums.
- Do not touch user-owned untracked `.claude/` or `.vite/`.

---

### Task 1: Deterministic manifest and immutable candidate

**Files:**
- Create: `process/release_candidate.py`
- Create: `scripts/manage_release_candidate.py`
- Create: `tests/test_release_candidate.py`
- Modify: `process/schemas/release-manifest.schema.json`
- Modify: `process/package.yaml`
- Modify: `tests/test_process_package.py`
- Modify: `tests/fixtures/process-package/valid/release-manifest.yaml`
- Modify: `tests/fixtures/process-package/invalid/incomplete-release-manifest/release-manifest.yaml`

**Interfaces:**
- `build_release_candidate(repository_root: Path, destination: Path, manifest_inputs: Mapping[str, Any]) -> dict[str, Any]`
- `generate_release_manifest(candidate_root: Path, manifest_inputs: Mapping[str, Any]) -> dict[str, Any]`
- `validate_release_manifest(candidate_root: Path, manifest: Mapping[str, Any], *, now: datetime | None = None) -> dict[str, Any]`
- CLI modes: `build --root --destination --inputs`, `validate --candidate --manifest`; JSON stdout, stable exit `1` for acceptance rejection and `3` for malformed/missing input.

- [ ] Write RED tests that require byte-stable generation, sorted portable paths, candidate SHA-256 binding, two explicit host evidence levels, self-contained inclusion of `process/`, required root scripts, `templates/team-specs/`, runbooks, and rejection of missing/extra/symlink/reparse/case-colliding/reserved-name assets.
- [ ] Run `python -m pytest tests/test_release_candidate.py tests/test_process_package.py -q` and confirm failures are caused by the missing module/schema `2.0` behavior.
- [ ] Implement schema `2.0`, candidate allowlist construction, portable archive-name checks, deterministic hashes, atomic destination creation, generator, semantic validator, and thin CLI. Reuse `OperationError` and existing safe-root/copy conventions; do not import private helpers across modules.
- [ ] Re-run the same focused command until green, then run `python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py tests/test_packaged_flow_cli.py -q` once for shared-operation regression.
- [ ] Commit only Task 1 files with `feat: build deterministic release candidate`.

### Task 2: Acceptance semantics, migration/update/rollback rehearsal, and runbooks

**Files:**
- Modify: `process/release_candidate.py`
- Modify: `scripts/manage_release_candidate.py`
- Modify: `tests/test_release_candidate.py`
- Create: `docs/runbooks/TRANSFER_RELEASE_CANDIDATE.md`
- Modify: `docs/runbooks/PROCESS_PACKAGE_SETUP.md`
- Modify: `docs/runbooks/PACKAGED_GOVERNED_FLOW.md`

**Interfaces:**
- `evaluate_release_acceptance(candidate_root: Path, manifest: Mapping[str, Any], evidence_root: Path, *, now: datetime | None = None) -> dict[str, Any]`
- `rehearse_release_candidate(candidate_root: Path, workspace: Path, *, platform_id: str, evidence_level: str) -> dict[str, Any]`
- CLI modes: `accept --candidate --manifest --evidence-root`, `rehearse --candidate --workspace --platform-id --evidence-level --output`.

- [ ] Write parametrized RED cases for `evidence-missing`, `evidence-stale`, `evidence-failed`, `evidence-private`, `evidence-ai-only`, `evidence-checksum-mismatch`, `candidate-digest-mismatch`, incompatible dependency, failed migration/update hold, and archive-history rewrite.
- [ ] Write RED positive integration covering clean bootstrap, config compatibility, minor/major/hotfix creation, migration `check -> apply -> second apply no-op`, update, forced failed update/hold, rollback, and identical before/after archive-tree digest.
- [ ] Run only `python -m pytest tests/test_release_candidate.py -q` and confirm expected RED diagnostics.
- [ ] Implement acceptance and rehearsal orchestration by calling existing workflow/migration/config functions. Evidence must include platform inventory, exact commands, candidate digest, result, negative-case codes, archive digest, package/config versions, and rollback result; it must never record a human acceptance decision.
- [ ] Write platform-neutral installation, inventory, approved-secret-reference, MCP/adapter configuration, update, rollback/hold, and no-fork feedback procedures with exact Windows PowerShell and Linux Bash commands.
- [ ] Run `python -m pytest tests/test_release_candidate.py tests/test_classification_migration.py tests/test_validate_process_config.py tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py -q` once after stabilization.
- [ ] Commit Task 2 files with `feat: enforce release acceptance and rollback rehearsal`.

### Task 3: Real Windows and WSL2 evidence, one final suite, and reconciliation

**Files:**
- Create: `process/release/evidence/phase-2-12-windows-2026-07-17.yaml`
- Create: `process/release/evidence/phase-2-12-linux-wsl2-2026-07-17.yaml`
- Create: `process/release/release-manifest.yaml`
- Create: `docs/audits/PHASE_2_WORK_ITEM_2_12_RELEASE_AUDIT_2026-07-17.md`
- Modify: `process/certification/coverage.yaml`
- Modify: `process/certification/evidence-manifest.yaml`
- Modify: `openspec/changes/define-transfer-ready-process-package/tasks.md`
- Modify: `openspec/changes/adopt-nis-corporate-process-governance/tasks.md`
- Modify: `docs/phases/PHASE_2_EVIDENCE_INDEX.md`
- Modify: `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`
- Modify: `docs/README.md`

- [ ] Build the candidate once on Windows into a new empty destination; record exact runtime inventory and candidate digest.
- [ ] Run the full Windows rehearsal and required negative acceptance cases in a fresh isolated workspace; validate the evidence and manifest.
- [ ] Provision native Node 20+ and OpenSpec 1.4.1 in WSL2 Ubuntu 24.04 without committing machine-local state; copy the immutable candidate into the native WSL filesystem and verify its digest before execution.
- [ ] Run the bounded Linux smoke: inventory, bootstrap/config, migration check/apply/idempotency/no-archive-rewrite, update/rollback, one incompatible-dependency rejection, and missing/failed/private/AI-only evidence rejections.
- [ ] Compare required cross-host fields and require identical candidate digest, canonical fixture IDs, acceptance codes, update/rollback outcome, and archive-history digest; record platform-specific inventory separately.
- [ ] After stabilization, run the complete suite exactly once: `python -m pytest -q`. Do not repeat it unless code changes afterward invalidate this evidence.
- [ ] Run final gates once: `openspec list`, `openspec list --specs`, `openspec validate --all --strict`, roadmap/OpenSpec validator JSON, `git diff --check`, and a focused secret/private-value scan.
- [ ] Update tasks/status/evidence/audit documents only from observed results. Keep 2.12 `in_progress` or `blocked` if either host evidence fails; close it only when every acceptance row passes.
- [ ] Commit reconciliation with `docs: record phase 2.12 release evidence` and request high-risk task review plus final branch review.

## Self-Review

- Spec coverage: transfer tasks 5.1-5.4 and NIS task 8.4 map to Tasks 1-3.
- No task rebuilds policy logic or reruns actual-model certification.
- The only full-suite step is Task 3 after stabilization.
- macOS remains explicitly not certified in schema, manifest, evidence, and audit.
