---
name: phase-full-runner
description: Execute a complete roadmap phase end-to-end by coordinating one work item at a time, optionally with worker, reviewer, architecture-checker, and verification-checker subagents. Use when the user asks to run a whole phase, execute all phase items, loop through a phase plan, or coordinate phase work with subagents/reviewers.
---

# Phase Full Runner

Coordinate full phase execution while preserving the one-work-item verification and commit rhythm.

## Workflow

1. State that this project-local skill is being used.
2. Read required docs from `AGENTS.md`, including the phase plan and verification checklist.
3. Verify branch and phase status.
4. For each work item:
   - map OpenSpec requirements/deltas to acceptance evidence;
   - assign or locally perform worker implementation;
   - run reviewer and architecture checks when available;
   - run verification checks;
   - route new feedback through `phase-change-intake`;
   - update documentation;
   - commit before moving to the next item when project rules require it.
5. At the phase gate, summarize evidence, remaining risks, manual checks, and human decisions.

If subagent tools are unavailable, execute locally and record that limitation in the final report.
