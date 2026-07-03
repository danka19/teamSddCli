# Phase 1. Discovery And Requirements

Status: in progress.

## Goal

Turn the architecture into concrete deterministic process artifacts for the first thin SDD change flow: copyable change package templates, local validation, pre-commit execution, and OpenSpec-backed artifact contracts.

## Inputs To Read

- `AGENTS.md`
- `docs/README.md`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `sdd_final_architecture.md`
- `docs/IMPLEMENTATION_STRATEGY.md`
- `docs/CURRENT_PROJECT_AUDIT.md`
- `docs/AI_STEP_VERIFICATION_CHECKLIST.md`
- `openspec/` when `sdd CLI` behavior, workflow requirements, proposed changes, artifact contracts, or acceptance criteria are involved
- `docs/CONTEXT.md`

## OpenSpec And Acceptance Mapping

- Affected accepted requirements:
  - None yet; this phase starts the accepted requirement set.
- Active proposed changes:
  - `add-change-template-validation`
- Acceptance scenarios:
  - A valid copied change package with required artifacts, metadata, OpenSpec delta, and traceability passes local validation.
  - A change package missing required artifacts fails validation with actionable errors.
  - A change package with missing requirement-to-scenario traceability fails validation.
  - The pre-commit hook runs the same validator and ignores plain OpenSpec project changes that are not SDD change packages.
  - The template itself remains structurally checkable without treating placeholder values as production-ready metadata.
- Verification evidence expected before completion:
  - Focused `python -m pytest` tests for `scripts/validate_change.py`.
  - Manual `python scripts/validate_change.py --allow-placeholders templates/change`.
  - `openspec list`, `openspec list --specs`, and `openspec validate --all --strict`.
  - `git diff --check`.

## Change Intake

Record new ideas, fixes, scope changes, architecture notes, artifact contract changes, integration changes, or verification requests that appear during the phase.

```text
Idea:
Source:
Type:
Decision:
Reason:
Affected specs:
Affected architecture:
Data contract impact:
Verification impact:
Status:
```

## Work Items

### 1.1 Change Package Template And Local Validation Gate

Objective:

- Create the first deterministic Phase 1 artifact: `templates/change/`, `scripts/validate_change.py`, and `.pre-commit-config.yaml`.

Expected files/modules:

- `openspec/changes/add-change-template-validation/`
- `templates/change/`
- `scripts/validate_change.py`
- `tests/test_validate_change.py`
- `.pre-commit-config.yaml`
- `docs/00_FILE_STRUCTURE.md`
- `docs/ROADMAP.md`
- `docs/CURRENT_PROJECT_AUDIT.md`

Verification:

- `python -m pytest tests/test_validate_change.py -v`
- `python scripts/validate_change.py --allow-placeholders templates/change`
- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- `git diff --check`

Documentation updates:

- Update the repository map for new OpenSpec, templates, scripts, tests, and pre-commit paths.
- Update the roadmap to record Phase 1 as started.
- Update the audit to record OpenSpec initialization and the deterministic validation gate.

Recommended subagents:

- worker: implement the bounded template and validator change.
- reviewer: inspect validation gaps, false positives, and missing tests.
- architecture-checker: verify the deterministic layer stays independent from AI.
- verification-checker: verify command evidence and final report completeness.

Exit criteria:

- The template is copyable and structurally valid in placeholder mode.
- The validator rejects incomplete real change packages.
- The pre-commit hook points to the same validator without validating plain project OpenSpec changes as SDD packages.
- The OpenSpec change validates strictly.

OpenSpec and acceptance evidence:

- `add-change-template-validation` / `change-package-foundation`.

## Phase Gate

- Phase 1 can proceed to broader requirements only after the first deterministic artifact contract is present and locally verifiable.

## Human Decisions

- No new blocking decision for work item 1.1.
- Recommended default for later work: keep Jira, Confluence publication, QA/AT proposal generation, and role inbox automation out of the first deterministic validation gate unless explicitly re-scoped.
