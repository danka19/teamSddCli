# 00. File Structure

This document is the repository map for agents and humans. Keep it current whenever files or folders are added, removed, or repurposed.

## Root

| Path | Purpose |
|---|---|
| `AGENTS.md` | Canonical operating guide for Codex and future agents |
| `sdd_final_architecture.md` | Initial Russian source architecture for local team SDD automation |
| `.env.example` | Versioned environment template with placeholders only |
| `.gitignore` | Excludes secrets, local config, generated artifacts, and private data |
| `.codex/skills/` | Project-local skills for architecture planning and phase execution |
| `docs/` | Product, architecture, operations, roadmap, audit, glossary, and phase documentation |

## Documentation

| Path | Purpose |
|---|---|
| `docs/README.md` | Documentation home and product overview |
| `docs/00_FILE_STRUCTURE.md` | Repository and documentation map |
| `docs/ROADMAP.md` | Phase-level roadmap and gates |
| `docs/CURRENT_PROJECT_AUDIT.md` | Current setup/repository audit and known risks |
| `docs/IMPLEMENTATION_STRATEGY.md` | Accepted delivery strategy: no custom CLI upfront, success metrics, and CLI-build triggers |
| `docs/AI_STEP_VERIFICATION_CHECKLIST.md` | Mandatory self-check for AI agents |
| `docs/CONTEXT.md` | Active glossary and domain boundaries |
| `docs/planning/` | Cross-phase planning notes and decision drafts |
| `docs/audits/` | Focused audit reports |
| `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md` | Architecture critique, external comparison, recommendations, and alternative solution paths |
| `docs/phases/` | Detailed phase plans and templates |

## Expected Future Project Structure

These paths are expected by the documented SDD workflow but do not exist yet in this folder:

| Path | Purpose |
|---|---|
| `openspec/` | CLI project's own accepted/proposed behavior specs and requirements |
| `openspec/specs/` | Accepted living specs for teamSddCli behavior |
| `openspec/changes/` | Proposed behavior changes before acceptance |
| `src/` | Future CLI implementation source |
| `tests/` | Future automated tests |
| `templates/` | Future change/package templates used by `sdd CLI` |
| `schemas/` | Future schemas for `change.yaml`, registries, traceability, and config |

## Project-Local Skills

| Path | Purpose |
|---|---|
| `.codex/skills/architecture-planner/SKILL.md` | Plan or revise architecture decisions from current docs and implementation evidence |
| `.codex/skills/phase-change-intake/SKILL.md` | Triage new ideas, fixes, scope changes, and verification requests during active phase work |
| `.codex/skills/phase-planner/SKILL.md` | Create detailed phase plans |
| `.codex/skills/phase-step-runner/SKILL.md` | Execute one phase work item |
| `.codex/skills/phase-full-runner/SKILL.md` | Coordinate full phase execution with worker/reviewer/checker roles |
