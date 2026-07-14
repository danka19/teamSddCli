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
| `requirements-test.txt` | Reproducible PyYAML and JSON Schema dependencies for process-package contract tests |
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
| `docs/IMPLEMENTATION_STRATEGY.md` | Accepted delivery strategy: no custom CLI upfront, mandatory gates, usability checks, and CLI-build triggers |
| `docs/AI_STEP_VERIFICATION_CHECKLIST.md` | Mandatory self-check for AI agents |
| `docs/CONTEXT.md` | Active glossary and domain boundaries |
| `docs/planning/` | Cross-phase planning notes and decision drafts |
| `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` | Planning input for project memory, Graphify-like navigation, documentation quality, weak-model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability |
| `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md` | Accepted source-to-target adoption plan for NIS minor/major/hotfix classification, DoR/DoD, Tech Lead automation, corporate flow controls, failed-run retention, migration, and Phase 2/3 sequencing |
| `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md` | Consolidated target-architecture picture and staged execution plan draft from the 2026-07-06 documentation review |
| `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md` | Abstracted structure analysis of the corporate analytics approval template and the plan for mapping it to SDD artifacts (typed YAML records instead of nested tables) |
| `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md` | Evaluation criteria and topology comparison frame for the internal OpenSpec customization screenshots and work item 1.4 |
| `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md` | Abstracted analysis of the internal developer-oriented OpenSpec customization (workflow schema, skills, staged repo topology) with borrow/differ recommendations for work item 1.4 |
| `arch-screenshots/analytic-template/` | Local-only photos of the corporate analytics template (git-ignored; contains corporate content; never commit) |
| `arch-screenshots/openspec-de/` | Local-only screenshots of an internal OpenSpec customization approach for Phase 1 topology analysis (git-ignored; contains corporate content; never commit) |
| `docs/audits/` | Focused audit reports |
| `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md` | Architecture critique, external comparison, recommendations, and alternative solution paths |
| `docs/audits/FABLE5_DOCUMENTATION_ARCHITECTURE_REVIEW_2026-07-06.md` | Documentation/architecture audit: findings F1-F6, drift records, and the open human decision batch |
| `docs/audits/NIS_V1_6_ARCHITECTURE_COMPATIBILITY_AUDIT_2026-07-13.md` | Evidence-backed comparison of the local NIS v1.6 reference package against accepted architecture, including alignments, useful additions, conflicts, internal inconsistencies, and adoption boundaries |
| `docs/audits/NIS_V1_6_PRESENTATION_COMPARISON_REPORT_2026-07-13.md` | Presentation-ready summary of what matches NIS, what the project borrows, what is adapted or rejected, the failed-run rule, current acceptance status, and suggested slide structure |
| `docs/audits/PROCESS_EFFECTIVENESS_DOCUMENTATION_REMOVAL_AUDIT_2026-07-13.md` | Reproducible verification that process-effectiveness evaluation was removed from current tracked docs/OpenSpec while failed-run retention and ordinary QA/safety controls remain |
| `docs/audits/TRANSFER_READINESS_STATUS_2026-07-13.md` | Evidence-backed audit of phase status, deterministic baseline, weak-model readiness, transfer gaps, and the accepted remediation boundary |
| `docs/audits/PHASE_2_PLAN_COMPLETENESS_AUDIT_2026-07-13.md` | Evidence-backed audit of Phase 2 scope coverage, statuses, task ownership, dependency cycles, OpenSpec mapping, verification specificity, and planning drift |
| `docs/audits/PHASE_2_EXECUTION_PREFLIGHT_AUDIT_2026-07-14.md` | Reproducible Phase 2 execution-entry audit covering statuses, dependency gates, OpenSpec readiness, baseline tests, branch safety, and later certification limitations |
| `docs/phases/` | Detailed phase plans and templates |
| `docs/phases/PHASE_0_PROJECT_FOUNDATION.md` | Completed Phase 0 foundation plan and evidence |
| `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md` | Phase 1 plan for requirements and deterministic SDD artifact contracts |
| `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md` | Ready Phase 2 plan for the external process-package release candidate, Qwen/DeepSeek certification, transfer evidence, and corporate adaptation package |
| `docs/phases/PHASE_2_EVIDENCE_INDEX.md` | Phase 2 work-item source, implementation, verification, and independent-review evidence index |
| `docs/phases/PHASE_PLAN_TEMPLATE.md` | Mandatory template for detailed phase plans |
| `docs/runbooks/PROCESS_PACKAGE_SETUP.md` | Minimal setup and test procedure for the synthetic central topology and versioned process-package contract |

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
| `openspec/changes/define-transfer-ready-process-package/` | Active apply-ready change proposing transfer-readiness and weak-model-guardrail capabilities, technical design, and 33 implementation tasks |
| `openspec/changes/adopt-nis-corporate-process-governance/` | Active apply-ready change proposing NIS-aligned minor/major/hotfix classification, schema migration, DoR/DoD, Tech Lead workflow, corporate flow controls, release handoff, pilot safety, failed-run retention, and affected accepted-capability deltas |
| `openspec/changes/archive/2026-07-09-*/` | Archived Phase 1 OpenSpec change packages promoted into accepted specs by the 2026-07-09 Option A batch archive |

## Deterministic Process Artifacts

| Path | Purpose |
|---|---|
| `templates/change/` | Copyable SDD change package skeleton |
| `templates/change/waivers.yaml` | Example structured waiver registry showing the deterministic waiver shape for optional artifact exceptions |
| `scripts/validate_change.py` | Dependency-free Python validator for SDD change package structure, metadata, OpenSpec scenarios, and basic traceability |
| `tests/test_validate_change.py` | Focused validator tests covering thin/full artifact rules, canonical statuses, waiver validation, traceability gaps, staged discovery, and placeholder mode |
| `process/VERSION` | Reusable process-package semantic version (`0.2.0` for the policy/schema-v2 foundation) |
| `process/package.yaml` | Process-package metadata, OpenSpec and policy-set pins, workflow/policy manifest references, local schema inventory, and canonical source references |
| `process/workflow.yaml` | Minimal reusable artifact dependency contract for the accepted central topology |
| `process/policies/` | Manifest-driven `sdd-core` policy set with eight versioned static policy catalogs; later work items consume these records to implement behavior |
| `process/schemas/` | Local Draft 2020-12 schemas for package/workflow metadata, schema-v2 changes, policy documents/manifest, central registries/config, optional project adapter, and release manifest |
| `process/validators/config_discovery.py` | Bounded repository/config discovery, duplicate-safe YAML loading, explicit reference resolution, package/schema/policy loading, and final OpenSpec runtime probe |
| `process/validators/config_validation.py` | Structured redacted diagnostics plus pure schema, compatibility, secret, and cross-registry integrity checks |
| `process/validators/policy_validation.py` | Static policy identity/reference/override validation and immutable effective-value snapshots with provenance |
| `templates/team-specs/` | Placeholder-only synthetic central topology with approved config names and canonical directory roots |
| `templates/project-adapter/.sdd-project.yaml` | Optional synthetic project-repository pointer to central `team-specs` and package/config versions |
| `tests/fixtures/process-package/` | Positive release-manifest and negative schema/reference/privacy fixture families for work item 2.1 |
| `tests/test_process_package.py` | Test-only YAML/schema, local-reference, cross-file-integrity, and bounded sensitive-value harness |
| `scripts/validate_process_config.py` | Thin non-mutating human/JSON entry point for production configuration discovery and compatibility validation |
| `tests/test_validate_process_config.py` | Focused central/adapter discovery, compatibility, integrity, secret-redaction, diagnostics, exit-code, and CWD-independence evidence |
| `tests/fixtures/policy-v2/` | Synthetic minor/major/hotfix, decision-input, corporate-value, and override fixture families for work item 2.3 |
| `tests/test_policy_schema_v2.py` | Scenario-first static schema-v2, policy manifest, integrity, override, provenance, and no-premature-verdict evidence |

## Planned Phase 2 Project Structure

The base `process/`, central-topology templates, schemas, and fixtures now exist. The following later-work-item paths remain planned:

| Path | Purpose |
|---|---|
| `process/templates/`, additional behavioral `process/validators/`, `process/roles/`, `process/adapters/`, `process/certification/` | Later packaged flow, classifier/gate behavior, role-kit, adapter, and certification assets; work items 2.2-2.3 provide config and static policy/schema validation only |
| Additional `docs/runbooks/` files | Classification migration, update/rollback, governed minor/major/hotfix flow, Tech Lead, release, corporate adaptation, and pilot runbooks |
| `scripts/bootstrap_team_specs.py` | Planned deterministic central-topology bootstrap entry point |
| `scripts/build_read_pack.py` | Planned deterministic authority-labelled bounded read-pack builder |
| `scripts/certify_process_release.py` | Planned AI-disabled and weak-model release certification entry point |

## Skills

Workflow skills are global (`~/.codex/skills`): architecture-planner, phase-planner, phase-step-runner, phase-full-runner, phase-change-intake, openspec-*, handoff-to-claude, session-report, doc-sync-audit. This repository intentionally has no `.codex/skills/` directory.
