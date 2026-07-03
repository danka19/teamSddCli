## Context

The repository already has `AGENTS.md`, `docs/AI_STEP_VERIFICATION_CHECKLIST.md`, phase plans, audit notes, and active OpenSpec changes. The governance proposal turns those operating habits into testable future requirements without promoting them to accepted specs yet.

## Proposed Design

Documentation governance applies when work changes any of the following:

- SDD workflow behavior
- CLI or future command behavior
- artifact/process contracts
- setup, operations, security, or integration boundaries
- roadmap, phase status, or acceptance gates
- user-visible command/help text
- accepted or proposed OpenSpec behavior

For each change, the worker records whether docs need updates, updates the narrowest relevant docs, and reports verification evidence. Proposed behavior stays in `openspec/changes/`; accepted behavior is written under `openspec/specs/` only after explicit human archive/acceptance approval.

## AI Verification Checklist Evidence

Before claiming completion, the worker records the commands run, blockers, manual checks, documentation updates or a no-documentation-update rationale, residual manual-verification risks, skills used, and subagents used with role names and token counts when available. The AI checklist is evidence of process discipline, not a substitute for deterministic checks or human approval.

## TDD-Style Verification Rules

For deterministic behavior changes, OpenSpec scenarios or acceptance examples are identified before implementation. Tests, schema checks, syntax checks, or manual verification are chosen before code changes where practical. Negative cases are required when the system must not infer too much, accept placeholders, silently skip artifacts, or treat advisory AI output as accepted truth.

## Risks / Trade-offs

- Governance can become busywork if every minor note requires broad documentation updates, so this proposal requires the narrowest relevant durable document.
- Documentation can drift if final reports mention decisions that never reach durable artifacts, so human feedback classification remains required.
- The proposal must not create accepted specs until the final human archive gate.
