---
name: phase-step-runner
description: Execute exactly one roadmap phase work item at a time with implementation, focused verification, documentation updates, change-intake handling for new ideas, and a commit when project rules require it. Use when the user asks to continue a phase, complete the next phase item, do one phase step, or work through a detailed phase plan incrementally.
---

# Phase Step Runner

Execute one work item, not a whole phase, unless the user explicitly asks otherwise.

## Workflow

1. State that this project-local skill is being used.
2. Read required docs from `AGENTS.md`, including the relevant phase plan and verification checklist.
3. Verify the current branch matches the active phase or record the human-approved exception.
4. Map affected OpenSpec requirements or proposed deltas to acceptance scenarios and verification evidence.
5. Route any new phase feedback through `phase-change-intake` before changing scope.
6. Implement the smallest complete slice for the selected work item.
7. Run focused checks first; run broader checks when shared behavior changes.
8. Update docs for behavior, architecture, setup, operations, security, roadmap status, data contracts, OpenSpec artifacts, or verification rules.
9. Commit intentional changes when project rules require it.
10. Report task, decisions, important details, changes, checks, manual verification, risks, skills, subagents, unresolved decisions, and next step.
