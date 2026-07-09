# 00. File Structure

This document is the repository map for agents and humans. Keep it current whenever files or folders are added, removed, or repurposed.

## Root

| Path | Purpose |
|---|---|
| `AGENTS.md` | Canonical operating guide for Codex and future agents |
| `CLAUDE.md` | Claude entry point; pointer to `AGENTS.md` and the active handoff only |
| `.env.example` | Versioned environment template with placeholders only |
| `.gitignore` | Excludes secrets, local config, generated artifacts, and private data |
| `.pre-commit-config.yaml` | Local pre-commit hook configuration for deterministic SDD change validation |
| `pytest.ini` | Pytest configuration; uses a repository-local temp folder for this Windows workspace |
| `docs/handoffs/` | Bounded task handoffs to Claude (global `handoff-to-claude` skill) |
| `openspec/` | Project OpenSpec changes and accepted specs for teamSddCli behavior |
| `templates/` | Copyable SDD process templates |
| `scripts/` | Deterministic local validation and process scripts |
| `tests/` | Focused automated tests for deterministic scripts |
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
| `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` | Planning input for project memory, Graphify-like navigation, documentation quality, weak-model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability |
| `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md` | Consolidated target-architecture picture and staged execution plan draft from the 2026-07-06 documentation review |
| `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md` | Abstracted structure analysis of the corporate analytics approval template and the plan for mapping it to SDD artifacts (typed YAML records instead of nested tables) |
| `arch-screenshots/analytic-template/` | Local-only photos of the corporate analytics template (git-ignored; contains corporate content; never commit) |
| `arch-screenshots/openspec-de/` | Local-only screenshots of an internal OpenSpec customization approach for Phase 1 topology analysis (git-ignored; contains corporate content; never commit) |
| `docs/audits/` | Focused audit reports |
| `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md` | Architecture critique, external comparison, recommendations, and alternative solution paths |
| `docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md` | Documentation/architecture audit: findings F1-F6, drift records, and the open human decision batch |
| `docs/phases/` | Detailed phase plans and templates |
| `docs/phases/PHASE_0_PROJECT_FOUNDATION.md` | Completed Phase 0 foundation plan and evidence |
| `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md` | Phase 1 plan for requirements and deterministic SDD artifact contracts |
| `docs/phases/PHASE_PLAN_TEMPLATE.md` | Mandatory template for detailed phase plans |

## OpenSpec

| Path | Purpose |
|---|---|
| `openspec/changes/add-change-template-validation/` | Active OpenSpec change for the first deterministic change-template and validation gate |
| `openspec/changes/add-change-template-validation/proposal.md` | Motivation, scope, capabilities, and impact for the first deterministic gate |
| `openspec/changes/add-change-template-validation/design.md` | Technical design and tradeoffs for the template, validator, and pre-commit hook |
| `openspec/changes/add-change-template-validation/specs/change-package-foundation/spec.md` | Proposed requirements and scenarios for the deterministic gate |
| `openspec/changes/add-change-template-validation/tasks.md` | Trackable implementation checklist for the OpenSpec change |
| `openspec/changes/define-change-lifecycle/` | Draft Phase 1 proposal for change lifecycle states, transition gates, and human/AI/CI ownership boundaries |
| `openspec/changes/define-change-artifact-contracts/` | Draft Phase 1 proposal for thin and full change artifact contracts; Phase 1 default matrix approved, pending final archive/accepted-spec gate |
| `openspec/changes/define-traceability-contract/` | Draft Phase 1 proposal for requirement, scenario, task, test, automation, waiver, and archive-readiness traceability |
| `openspec/changes/define-waiver-policy/` | Draft Phase 1 proposal for waiver shape, approval, evidence, audit trail, and negative cases |
| `openspec/changes/define-documentation-governance/` | Draft Phase 1 proposal for documentation update discipline, AI verification evidence, and TDD-style verification rules |
| `openspec/changes/define-confluence-feedback-loop/` | Draft Phase 1 proposal for generated Confluence publication, feedback dispositions, unresolved comments, source metadata, and evidence-backed status display |

## Deterministic Process Artifacts

| Path | Purpose |
|---|---|
| `templates/change/` | Copyable SDD change package skeleton |
| `scripts/validate_change.py` | Dependency-free Python validator for SDD change package structure, metadata, OpenSpec scenarios, and basic traceability |
| `tests/test_validate_change.py` | Focused validator tests covering valid packages, missing artifacts, traceability gaps, staged discovery, and placeholder mode |

## Expected Future Project Structure

These paths are expected by the documented SDD workflow but do not exist yet in this folder:

| Path | Purpose |
|---|---|
| `openspec/specs/` | Accepted living specs for teamSddCli behavior |
| `src/` | Future CLI implementation source |
| `schemas/` | Future schemas for `change.yaml`, registries, traceability, and config |

## Skills

Workflow skills are global (`~/.codex/skills`): architecture-planner, phase-planner, phase-step-runner, phase-full-runner, phase-change-intake, openspec-*, handoff-to-claude, session-report, doc-sync-audit. This repository intentionally has no `.codex/skills/` directory.
