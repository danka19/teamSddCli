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
| `docs/DECISIONS.md` | Canonical human decision log with stable decision IDs and evidence pointers |
| `docs/ROADMAP.md` | Phase-level roadmap and gates |
| `docs/CURRENT_PROJECT_AUDIT.md` | Current setup/repository audit and known risks |
| `docs/IMPLEMENTATION_STRATEGY.md` | Accepted delivery strategy: no custom CLI upfront, success metrics, and CLI-build triggers |
| `docs/AI_STEP_VERIFICATION_CHECKLIST.md` | Mandatory self-check for AI agents |
| `docs/CONTEXT.md` | Active glossary and domain boundaries |
| `docs/planning/` | Cross-phase planning notes and decision drafts |
| `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` | Planning input for project memory, Graphify-like navigation, documentation quality, weak-model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability |
| `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md` | Consolidated target-architecture picture and staged execution plan draft from the 2026-07-06 documentation review |
| `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md` | Abstracted structure analysis of the corporate analytics approval template and the plan for mapping it to SDD artifacts (typed YAML records instead of nested tables) |
| `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md` | Evaluation criteria and topology comparison frame for the internal OpenSpec customization screenshots and work item 1.4 |
| `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md` | Abstracted analysis of the internal developer-oriented OpenSpec customization (workflow schema, skills, staged repo topology) with borrow/differ recommendations for work item 1.4 |
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
| `openspec/specs/change-package-foundation/spec.md` | Accepted spec for the deterministic change-package template, local validator, pre-commit entrypoint, and placeholder validation mode |
| `openspec/specs/change-lifecycle/spec.md` | Accepted spec for SDD change lifecycle states, deterministic transition gates, human approval ownership, MVP lifecycle boundaries, derived status display, and archive history convention |
| `openspec/specs/change-artifact-contracts/spec.md` | Accepted spec for thin/full artifact contracts, waiver eligibility, artifact matrix acceptance, future journey/screen artifacts, legacy baseline mode, Delta Spec operation vocabulary, and artifact-height rules |
| `openspec/specs/traceability-contract/spec.md` | Accepted spec for review-minimum traceability, archive-readiness traceability, waived links, AI advisory suggestions, journey/screen traceability, and legacy baseline traceability |
| `openspec/specs/waiver-policy/spec.md` | Accepted spec for waiver records, role-appropriate human waiver approval, negative cases, and waiver-policy acceptance status |
| `openspec/specs/documentation-governance/spec.md` | Accepted spec for documentation source ownership, AI verification evidence, TDD-style checks, canonical language, localized generated views, write-once/reference-many rules, and weak-model read packs |
| `openspec/specs/repo-topology-config/spec.md` | Accepted spec for the first supported repository topology, config files, process package distribution, OpenSpec version pin/upgrade policy, and owner/reviewer registry |
| `openspec/specs/confluence-feedback-loop/spec.md` | Accepted spec for Confluence as generated publication/read model, feedback dispositions, blocker handling, configurable SLA, publication pipeline boundaries, and evidence-backed status display |
| `openspec/changes/archive/2026-07-09-*/` | Archived Phase 1 OpenSpec change packages promoted into accepted specs by the 2026-07-09 Option A batch archive |

## Deterministic Process Artifacts

| Path | Purpose |
|---|---|
| `templates/change/` | Copyable SDD change package skeleton |
| `templates/change/waivers.yaml` | Example structured waiver registry showing the deterministic waiver shape for optional artifact exceptions |
| `scripts/validate_change.py` | Dependency-free Python validator for SDD change package structure, metadata, OpenSpec scenarios, and basic traceability |
| `tests/test_validate_change.py` | Focused validator tests covering thin/full artifact rules, canonical statuses, waiver validation, traceability gaps, staged discovery, and placeholder mode |

## Expected Future Project Structure

These paths are expected by the documented SDD workflow but do not exist yet in this folder:

| Path | Purpose |
|---|---|
| `src/` | Future CLI implementation source |
| `schemas/` | Future schemas for `change.yaml`, registries, traceability, and config |

## Skills

Workflow skills are global (`~/.codex/skills`): architecture-planner, phase-planner, phase-step-runner, phase-full-runner, phase-change-intake, openspec-*, handoff-to-claude, session-report, doc-sync-audit. This repository intentionally has no `.codex/skills/` directory.
