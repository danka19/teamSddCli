# Phase 2 Work Item 2.12 Intake And Preflight Audit

Date: 2026-07-17.

Status: complete for implementation intake; product implementation remains in progress.

## Boundary And Criteria

Target: Phase 2 work item 2.12, transfer tasks 5.1-5.4, and NIS task 8.4.

Criteria:

- prerequisite and branch readiness;
- Roadmap/OpenSpec governance consistency;
- exact platform acceptance scope;
- reusable bootstrap/update/rollback/migration implementation evidence;
- manifest and acceptance-automation gaps;
- Windows and Linux/WSL2 rehearsal feasibility;
- test-economy constraint: focused checks during stabilization and one full suite afterward.

Severity scale: Critical blocks safe implementation; Important must be resolved before work-item closure; Minor is non-blocking debt. This audit does not certify a release candidate.

## Reproducible Evidence

Commands executed from the repository root:

```powershell
git status --short
git branch --show-current
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root "C:\Users\danoc\Documents\projects\teamSsdCli" --json
openspec list
openspec list --specs
openspec validate --all --strict
wsl --status
wsl -l -v
python --version
node --version
git --version
openspec --version
```

Observed results:

- branch `codex/phase-2-transfer-readiness-plan` contains the closed 2.1-2.11 sequence and is the correct dependency base;
- user-owned untracked `.claude/` and `.vite/` exist and were not modified;
- roadmap/OpenSpec validator: 0 errors, 2 historical completed-but-not-accepted warnings;
- OpenSpec strict validation: 12 passed, 0 failed;
- Windows inventory: Python 3.13.14, Node 24.16.0, Git 2.54.0.windows.1, OpenSpec 1.4.1;
- WSL2 Ubuntu 24.04 is available; Linux Python 3.12.3 and Git 2.43.0 were observed, while native Linux Node/OpenSpec remain unprovisioned;
- the complete pytest suite was intentionally not run during intake.

## Findings

### P2-12-INTAKE-001: Previous three-host contract contradicted the human verification scope

Classification: verified contract conflict. Severity: Critical before implementation.

Evidence: `D-015`, `D-017`, the transfer-readiness delta, task 5.4, the phase plan, and release-manifest schema required Windows/Linux/macOS, while the human explicitly required Windows, Linux through WSL, and no macOS verification.

Root cause: the earlier platform decision had not yet been superseded.

Remediation: completed through `D-018` and synchronized OpenSpec/roadmap/phase-plan changes. Historical decisions remain unchanged as audit history. Work item 2.12 moved from `planned` to `in_progress`.

### P2-12-INTAKE-002: No real release-candidate generator or semantic acceptance validator exists

Classification: verified implementation gap. Severity: Critical for work-item exit.

Evidence: the repository contains a schema and synthetic manifest fixture, but no generator, immutable candidate builder, semantic freshness/success/privacy/authority validator, platform evidence schema, or acceptance packet.

Root cause: these capabilities are intentionally owned by transfer tasks 5.1-5.4, which were open at intake.

Recommended action: execute Tasks 1-3 in `docs/superpowers/plans/2026-07-17-phase-2-12-release-candidate.md` with TDD and High-risk review gates.

### P2-12-INTAKE-003: Existing process package is not a self-contained transfer artifact

Classification: verified implementation gap. Severity: Important.

Evidence: `process/package.yaml` distributes `process/` content, while required bootstrap entry points and `templates/team-specs/` live at repository root.

Root cause: the existing package was designed for in-repository execution, not frozen external transfer.

Recommended action: build an allowlisted immutable candidate containing the versioned process, required thin scripts, synthetic team template, and transfer runbooks; reject unsafe archive names and links before extraction.

### P2-12-INTAKE-004: Existing reusable operations substantially reduce implementation scope

Classification: verified pass/reuse opportunity. Severity: none.

Evidence: `process/workflow_operations.py` already provides deterministic bootstrap, compatibility, update, and rollback; classification migration already provides check/apply/idempotency behavior; focused tests cover transactional restoration and no-history-rewrite behavior.

Recommended action: orchestrate public operations rather than duplicate policy or import private helpers.

### P2-12-INTAKE-005: Linux rehearsal prerequisite is incomplete

Classification: verified environment limitation. Severity: Important before Linux evidence.

Evidence: WSL2 Ubuntu 24.04 is present, but native Node.js/OpenSpec were not available during intake.

Root cause: host provisioning has not yet been performed.

Residual uncertainty: MCP availability inside WSL and the exact clean-Windows isolation strength remain to be recorded by rehearsal inventory.

Recommended action: provision native Node 20+ and OpenSpec 1.4.1 inside WSL without committing machine-local state, then copy the already-built candidate into the native WSL filesystem and verify its digest.

## Accepted Verification Sequence

1. Focused manifest/bootstrap/integration TDD.
2. One full Windows rehearsal from a fresh isolated workspace with recorded inventory.
3. One shorter Linux/WSL2 portability smoke plus negative acceptance cases from the same candidate bytes.
4. Negative acceptance cases for missing, stale, failed, private, checksum-invalid, candidate-mismatched, and AI-only evidence.
5. One complete pytest suite after implementation and rehearsals stabilize.
6. Final OpenSpec, roadmap, diff, privacy, review, and status gates.

## Residual Risks

- WSL2 proves the accepted Linux portability scope, not an independent physical Linux desktop host.
- A fresh isolated Windows workspace is weaker evidence than a disposable Windows VM; rehearsal inventory must state the actual boundary without calling it stronger than observed.
- No production implementation or host rehearsal was completed in this intake session.
- The High-risk Task 1 architecture subagent did not return a verdict within two bounded attempts. Production implementation must not begin until that gate succeeds or an equivalent documented architecture review is completed.
