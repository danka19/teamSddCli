---
name: phase-planner
description: Create or update detailed phase implementation plans from roadmap intent, current docs, implementation evidence, audit findings, verification requirements, human decisions, and queued change-intake items. Use when the user asks to plan a phase, make a phase checklist, break roadmap work into work items, handle new ideas during planning, or prepare implementation steps.
---

# Phase Planner

Planning from `docs/ROADMAP.md` alone is forbidden.

## Workflow

1. State that this project-local skill is being used.
2. Read the required docs from `AGENTS.md`.
3. Read the target phase plan if it exists; otherwise use `docs/phases/PHASE_PLAN_TEMPLATE.md`.
4. Search code/tests/docs for implemented evidence related to the phase.
5. Reconcile roadmap intent, current implementation, audit risks, OpenSpec specs/changes, queued change-intake records, human decisions, and verification checklist requirements.
6. Write work items with objective, affected OpenSpec requirements or deltas, expected files, verification, documentation updates, recommended subagents, exit criteria, and human decisions.
7. Update `docs/CURRENT_PROJECT_AUDIT.md` or `docs/ROADMAP.md` if the plan changes status, gates, or risks.
