---
name: teamssd-roadmap-openspec-validator
description: Use when roadmap phases, OpenSpec specs, active changes, lifecycle metadata, or inverse tables are created, changed, or audited.
---

# Roadmap OpenSpec Validator

Compare `docs/ROADMAP.md` with accepted specs and active changes. Every accepted
capability and active change must have one primary execution phase and one
matching inverse row. Related phases never replace the primary owner.

Run `openspec validate --all --strict`, then inspect lifecycle and phase
metadata. Errors block completion; report warnings separately. Never infer
human acceptance from tasks, commits or archives.

This skill is read-only except for an explicitly requested documentation
repair and uses no external service.
