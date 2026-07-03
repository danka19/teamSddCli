# Phase 0. Project Foundation

Status: in progress.

## Goal

Prepare repository operating rules, documentation structure, initial roadmap, audit, verification checklist, and local Codex skills from the starter kit and `sdd_final_architecture.md`.

## Work Items

### 0.1 Documentation Foundation

Objective:

- Establish `AGENTS.md`, `docs/`, roadmap, audit, glossary, phase template, and project-local skills.
- Preserve the source architecture document as the initial product reference.
- Record the OpenSpec/Markdown-first workflow, artifact boundaries, and AI/human responsibility split.

Verification:

- Confirm required files exist.
- Confirm `docs/00_FILE_STRUCTURE.md` matches the generated structure.
- Confirm OpenSpec expectations and change-intake rules are documented.
- Run project-starter-kit `--check`.
- Run `git status --short` when `.git/` exists; if not, record that git is not initialized.

Exit criteria:

- Another Codex session can start from `AGENTS.md` and continue without chat history.

### 0.2 Open Decisions For Phase 1

Objective:

- Decide the implementation stack/runtime for `sdd CLI`.
- Decide whether this folder should become the CLI repository or whether starter docs should be moved into another git repository.
- Decide the first pilot target: one real project/team flow or a local synthetic example.
- Record the accepted 2026-07-03 architecture critique decisions in the Phase 1 plan:
  - first MVP is the thin change flow, not the full integration platform;
  - future requirements must distinguish `thin change` and `full change package`;
  - first OpenSpec specs should cover change lifecycle, artifact contracts, traceability, and waiver behavior;
  - Confluence feedback handling must be specified before publication automation;
  - mutating CLI/integration commands need dry-run, idempotency, JSON output, and audit logging contracts;
  - Gherkin is only required for executable or AT-exported scenarios.

Verification:

- Open decisions are either answered by the human owner or recorded in the Phase 1 plan.

## Phase Gate

- Project rules are clear.
- Secret and private-data handling is documented.
- Initial open decisions and risks are recorded.
- The starter documentation is verified with the bootstrap script.
- Git repository status is explicitly known.
