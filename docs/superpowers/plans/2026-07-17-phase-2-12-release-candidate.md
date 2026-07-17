# Phase 2.12 Release Candidate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify one immutable transfer candidate with deterministic manifest/acceptance behavior, one full Windows rehearsal, and one bounded equivalent Linux/WSL2 smoke plus negative cases.

**Architecture:** Add one focused `process.release_candidate` domain module and one thin CLI. A candidate contains an immutable `payload/` plus a pre-rehearsal `release-manifest.yaml`; the manifest is excluded from the canonical payload digest and records `payload_sha256`. Host rehearsal evidence remains external, binds to that digest, and never mutates the consumed candidate. Reuse existing bootstrap, compatibility, migration, update, rollback, and actual-certification validators without duplicating policy logic.

**Tech Stack:** Python 3.11+, PyYAML 6.0.3, jsonschema 4.26.0, pytest, PowerShell 7+, Bash on WSL2 Ubuntu 24.04, OpenSpec 1.4.1, Node 20+, Git 2.40+.

## Global Constraints

- Windows is `full-clean-rehearsal`; Linux on WSL2 is `portability-smoke`; macOS is `not-certified` and must never be inferred.
- Manifest generation and validation are deterministic, non-interactive, AI-disabled, and fail closed.
- Candidate construction is single-owner; both rehearsals consume byte-identical `payload/` and manifest content, while external host evidence binds to `payload_sha256`.
- Missing, stale, failed, private, checksum-invalid, candidate-mismatched, or AI-only evidence blocks acceptance with stable operator-safe codes.
- Update/rollback and migration must preserve accepted OpenSpec/archive history byte-for-byte.
- Focused tests run while stabilizing; the complete suite runs exactly once after implementation and rehearsals stabilize.
- Do not rerun Qwen/DeepSeek certification; consume existing committed normalized evidence and external raw-artifact checksums.
- Do not touch user-owned untracked `.claude/` or `.vite/`.

---

### Task 1: Deterministic manifest and immutable candidate

**Files:**
- Create: `process/release_candidate.py`
- Create: `process/errors.py`
- Create: `process/release-allowlist.yaml`
- Create: `process/schemas/release-allowlist.schema.json`
- Create: `docs/runbooks/TRANSFER_RELEASE_CANDIDATE.md`
- Create: `scripts/manage_release_candidate.py`
- Create: `tests/test_release_candidate.py`
- Modify: `process/schemas/release-manifest.schema.json`
- Modify: `process/package.yaml`
- Modify: `process/workflow_operations.py`
- Modify: `tests/test_process_package.py`
- Modify: `tests/fixtures/process-package/valid/release-manifest.yaml`
- Modify: `tests/fixtures/process-package/invalid/incomplete-release-manifest/release-manifest.yaml`

**Interfaces:**
- `ReleaseInputs(release_id: str, known_limitations: tuple[str, ...], raw_artifact_root: Path)` is the only caller-supplied manifest input; package/config/OpenSpec identity, host matrix, inventory, checksums, certification references, evidence requirements, and rollback reference are derived from committed contracts and inspected bytes.
- `build_release_candidate(repository_root: Path, destination: Path, inputs: ReleaseInputs) -> dict[str, Any]`
- `generate_release_manifest(payload_root: Path, inputs: ReleaseInputs) -> dict[str, Any]`
- `validate_release_manifest(candidate_root: Path, manifest: Mapping[str, Any], *, now: datetime | None = None) -> dict[str, Any]`
- CLI modes: `build --root --destination --inputs`, `validate --candidate --manifest`; JSON stdout, stable exit `1` for acceptance rejection and `3` for malformed/missing input.

- [ ] Write RED tests that require byte-stable generation, sorted portable paths, canonical `payload_sha256` binding with the manifest excluded, two explicit host evidence levels, and self-contained inclusion from schema-validated `process/release-allowlist.yaml`. That contract must enumerate `requirements-test.txt`; `templates/team-specs/`; the package distribution declared by `process/package.yaml`; runbooks `ARTIFACT_AND_LIFECYCLE_GATES.md`, `CERTIFICATION_EVIDENCE.md`, `CLASSIFICATION_AND_MIGRATION.md`, `CORPORATE_FLOW_CONTROLS.md`, `PACKAGED_GOVERNED_FLOW.md`, `PROCESS_PACKAGE_SETUP.md`, `TECH_LEAD_GOVERNANCE.md`, `TRANSFER_RELEASE_CANDIDATE.md`, and `WEAK_MODEL_OPERATING_KIT.md`; and exactly these root entry points: `bootstrap_team_specs.py`, `check_corporate_flow.py`, `check_lifecycle_transition.py`, `check_tech_lead_control.py`, `classify_change.py`, `create_change.py`, `evaluate_change_gates.py`, `manage_release_candidate.py`, `manual_fallback.py`, `migrate_change_classification.py`, `prepare_archive.py`, `prepare_spec_pr.py`, `review_tech_lead.py`, `update_process_package.py`, `validate_change.py`, `validate_external_mapping.py`, `validate_process_config.py`, and `validate_traceability.py`. Reject undeclared extras, mutable release/dev evidence, and unsafe assets.
- [ ] Run `python -m pytest tests/test_release_candidate.py tests/test_process_package.py -q` and confirm failures are caused by the missing module/schema `2.0` behavior.
- [ ] Implement schema `2.0`, exact allowlist construction, full file inventory, payload-only deterministic digest, atomic destination creation, generator, semantic validator, and thin CLI. Extract the stable public error contract to `process/errors.py` and re-export it through `workflow_operations.py` for compatibility. Implement release-owned public path/inventory primitives; do not import private helpers.
- [ ] Portable-path RED/GREEN coverage must reject drive-qualified, UNC, absolute, `.`/`..`, ADS/colon, control-character, trailing-dot/space, Windows reserved-device basenames including extensions, Unicode-normalization/casefold collisions, symlink/reparse, source/destination overlap, and pre-existing destination cases.
- [ ] `release-allowlist.yaml` must declare a non-interactive smoke command for every public entry point above. Prove the candidate is standalone by invoking every declared command from a copied payload with the source repository removed from `PYTHONPATH`; help or an expected stable missing-input exit is sufficient when mutation would otherwise occur. Task 1 covers `manage_release_candidate.py validate`; Task 2 extends the same contract test to `accept` and `rehearse`.
- [ ] Re-run the same focused command until green, then run `python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py tests/test_packaged_flow_cli.py -q` once for shared-operation regression.
- [ ] Commit only Task 1 files with `feat: build deterministic release candidate`.

### Task 2: Acceptance semantics, migration/update/rollback rehearsal, and runbooks

**Files:**
- Modify: `process/release_candidate.py`
- Modify: `scripts/manage_release_candidate.py`
- Modify: `tests/test_release_candidate.py`
- Modify: `docs/runbooks/TRANSFER_RELEASE_CANDIDATE.md`
- Modify: `docs/runbooks/PROCESS_PACKAGE_SETUP.md`
- Modify: `docs/runbooks/PACKAGED_GOVERNED_FLOW.md`

**Interfaces:**
- `evaluate_release_acceptance(candidate_root: Path, manifest: Mapping[str, Any], evidence_root: Path, *, now: datetime | None = None) -> dict[str, Any]`; it independently validates evidence schema, required IDs/catalog membership, checksums, freshness, privacy, AI-disabled semantics, human-authority boundaries, and `payload_sha256`, never trusting caller-supplied status or paths.
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

- [ ] Build the candidate once on Windows into a new empty destination; freeze its payload and pre-rehearsal manifest, then record exact runtime inventory and `payload_sha256` externally.
- [ ] Run the full Windows rehearsal and required negative acceptance cases in a fresh isolated workspace; validate the evidence and manifest.
- [ ] Provision native Node 20+ and OpenSpec 1.4.1 in WSL2 Ubuntu 24.04 without committing machine-local state; copy the immutable candidate into the native WSL filesystem and verify its digest before execution.
- [ ] Run the bounded Linux smoke: inventory, bootstrap/config, migration check/apply/idempotency/no-archive-rewrite, update/rollback, one incompatible-dependency rejection, and missing/failed/private/AI-only evidence rejections.
- [ ] Compare required cross-host fields and require identical `payload_sha256`, manifest checksum, canonical fixture IDs, acceptance codes, update/rollback outcome, and archive-history digest; record platform-specific inventory separately and never insert it into the frozen candidate.
- [ ] After stabilization, run the complete suite exactly once: `python -m pytest -q`. Do not repeat it unless code changes afterward invalidate this evidence.
- [ ] Run final gates once: `openspec list`, `openspec list --specs`, `openspec validate --all --strict`, roadmap/OpenSpec validator JSON, `git diff --check`, and a focused secret/private-value scan.
- [ ] Update tasks/status/evidence/audit documents only from observed results. Keep 2.12 `in_progress` or `blocked` if either host evidence fails; close it only when every acceptance row passes.
- [ ] Commit reconciliation with `docs: record phase 2.12 release evidence` and request high-risk task review plus final branch review.

## Self-Review

- Spec coverage: transfer tasks 5.1-5.4 and NIS task 8.4 map to Tasks 1-3.
- No task rebuilds policy logic or reruns actual-model certification.
- The only full-suite step is Task 3 after stabilization.
- macOS remains explicitly not certified in schema, manifest, evidence, and audit.
