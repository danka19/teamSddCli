---
name: teamssd-phase-step-runner
description: Use when executing exactly one accepted roadmap phase work item with focused evidence and status updates.
---

# Phase Step Runner

Confirm the active branch, phase, work item, dependencies, OpenSpec coverage
and acceptance matrix. Run the local status and roadmap/OpenSpec checks before
editing.

Implement only the selected item, preserve unrelated changes, collect focused
verification evidence, update its task/status/docs, then run
`teamssd-doc-sync-audit` and `teamssd-session-report`.

Do not create a remote PR or publish anything. When external integration is the
next step, stop with the exact human action required.
