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
| `process/` | Versioned deterministic process package, policies, schemas, templates, certification metadata/evidence, and historical release evidence |
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
| `docs/superpowers/specs/` | Approved design documents that precede implementation planning; OpenSpec remains the canonical proposed behavior contract |
| `docs/superpowers/plans/` | Detailed reviewed implementation plans; they guide execution but do not replace OpenSpec requirements |
| `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` | Planning input for project memory, Graphify-like navigation, documentation quality, weak-model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability |
| `docs/planning/NIS_CORPORATE_PROCESS_ADOPTION_PLAN_2026-07-13.md` | Accepted source-to-target adoption plan for NIS minor/major/hotfix classification, DoR/DoD, Tech Lead automation, corporate flow controls, failed-run retention, migration, and Phase 2/3 sequencing |
| `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md` | Consolidated target-architecture picture and staged execution plan draft from the 2026-07-06 documentation review |
| `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md` | Abstracted structure analysis of the corporate analytics approval template and the plan for mapping it to SDD artifacts (typed YAML records instead of nested tables) |
| `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md` | Согласованный дизайн AI companion для аналитического интервью: простой вход из идеи, вопросы по одному, truth statuses, human-confirmed summary, drafts и отдельные остановки перед файлами/командами |
| `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md` | Evaluation criteria and topology comparison frame for the internal OpenSpec customization screenshots and work item 1.4 |
| `docs/planning/PHASE_2_FOCUSED_COVERAGE_TESTS_IMPLEMENTATION_PLAN_2026-07-20.md` | Approved bounded RED/GREEN plan for the first-MVP boundary evidence and four exact residual-gap tests before product-gap intake |
| `docs/planning/LOCAL_OWNER_FRAMEWORK_WALKTHROUGH_2026-07-20.md` | Local synthetic owner walkthrough and completion gate required before Phase 3 corporate adaptation begins |
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
| `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_REMEDIATION_AUDIT_2026-07-16.md` | Dated adapter `2.0` remediation outcome, exact Qwen/DeepSeek failure evidence, AI-disabled regression, raw checksums, and residual human decision |
| `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_1_AUDIT_2026-07-16.md` | Dated adapter `2.1` outcome with the adapter `2.0` ten-response classification, Qwen 2/5 and DeepSeek 0/5 evidence, zero retries, runtime/result checksums, AI-disabled 11/11, and residual limitations |
| `docs/audits/PHASE_2_WORK_ITEM_2_11_ADAPTER_2_2_AUDIT_2026-07-17.md` | Dated passing adapter `2.2` audit covering deterministic operation planning, Qwen/DeepSeek 5/5 and 15/15 gates, AI-disabled 11/11, simplicity review, and residual limitations |
| `docs/audits/PHASE_2_WORK_ITEM_2_11_OPERATIONAL_AMBIGUITY_AUDIT_2026-07-17.md` | Root-cause audit that separates model limitations from hidden validator/operation-plan ambiguity and motivates adapter `2.2` |
| `docs/audits/PHASE_2_WORK_ITEM_2_12_ACCEPTANCE_PACKET_2026-07-17.md` | Immutable historical acceptance packet for `phase-2-12-rc7`; it must not be rewritten for the final 2.14 candidate |
| `docs/audits/PHASE_2_WORK_ITEM_2_12_RELEASE_AUDIT_2026-07-17.md` | Windows/WSL2 release rehearsal, rollback, negative acceptance, and release evidence audit for rc7 |
| `docs/audits/PHASE_2_WORK_ITEM_2_13_CORPORATE_ADAPTATION_AUDIT_2026-07-18.md` | Deterministic corporate-adaptation schema/template/privacy/no-fork evidence; no real corporate values, pilot, or model execution |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_DOCUMENTATION_RECONCILIATION_AUDIT_2026-07-18.md` | Dated 2.14.1 audit of status, roadmap/OpenSpec, repository map, manifest/evidence links, privacy, and residual release-readiness work |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_FINAL_TECHNICAL_AUDIT_2026-07-18.md` | Final candidate-bound deterministic, AI-disabled, Qwen/DeepSeek, Windows/WSL2, rollback, privacy, and limitation evidence for gate 2.14.2 |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_ACCEPTANCE_PACKET_2026-07-18.md` | Human decision packet for immutable candidate `phase-2-14-rc4`, including checksums, source-linked role evidence, risks, and residual gaps |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_REVIEW_GATES_2026-07-18.md` | Worker, reviewer, architecture, and verification gate results, correction batch, fallback limitation, and final rc4 review judgment |
| `docs/audits/PHASE_2_RESIDUAL_GAPS_PROVENANCE_AND_ROUTING_AUDIT_2026-07-19.md` | Provenance, exact counts, 46-requirement inventory, five-way routing, and acceptance consequences for rc4's 110 mechanically uniform residual-gap rows |
| `docs/audits/PHASE_2_PRODUCT_GAP_CHANGE_INTAKE_2026-07-20.md` | Six-group intake for the 13 genuine product gaps, with Phase 2 release-integrity routing, Phase 3/4 deferrals, and the successor-candidate execution gate |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_RC6_CERTIFICATION_2026-07-20.md` | Successor certification audit covering rc5 fail-closed history, immutable rc6 identity, fresh model/AI-disabled/platform evidence, exact raw closure, verification, and independent review |
| `docs/audits/PHASE_2_WORK_ITEM_2_14_RC6_ACCEPTANCE_PACKET_2026-07-20.md` | Accepted human-decision record for exact immutable candidate rc6, including checksums, evidence, limits, and consequences |
| `docs/audits/P3_TYPED_ANALYTICS_ACCEPTANCE_PACKET_2026-07-23.md` | Human review packet for the active typed analytics framework change and its verified `0.3.6` sandbox transfer; it is not acceptance evidence |
| `docs/audits/PHASE_3_GUIDED_OWNER_WORKFLOW_IMPLEMENTATION_AUDIT_2026-07-20.md` | Evidence-backed checkpoint for the implemented guided-operation slice, its verification, status reconciliation, and remaining successor-release gates |
| `docs/audits/SELF_SERVICE_OPERATOR_ONBOARDING_WALKTHROUGH_2026-07-23.md` | Synthetic AI-disabled and human-readable local walkthrough evidence for the proposed installed `sdd` onboarding route |
| `docs/audits/GIGACODE_ROLE_ACCEPTANCE_AND_FRAMEWORK_READINESS_AUDIT_2026-07-21.md` | Read-only sandbox audit of GigaCode role resolution, role-scoped UI, literal human evidence, premature acceptance paths, validator/template drift, retained analytics inputs, and missing framework-ready schemas/integration/screen contracts |
| `docs/audits/ANALYTIC_TEMPLATE_AND_CONFLUENCE_PUBLICATION_GAP_AUDIT_2026-07-24.md` | Повторная проверка всех 38 снимков корпоративного шаблона: границы ФП/change/release, полнота typed analytics, вложенные таблицы, человекочитаемая навигация и пробелы будущей Confluence publication model |
| `docs/audits/GIGACODE_SUPERPOWERS_SKILL_PRESSURE_TEST_2026-07-24.md` | RED→GREEN→REFACTOR pressure-test evidence для отдельного общего GigaCode workflow skill и сохранения SDD role/authority boundaries |
| `docs/phases/` | Detailed phase plans and templates |
| `docs/phases/PHASE_0_PROJECT_FOUNDATION.md` | Completed Phase 0 foundation plan and evidence |
| `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md` | Phase 1 plan for requirements and deterministic SDD artifact contracts |
| `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md` | Closed Phase 2 plan for the accepted external process-package release candidate, Qwen/DeepSeek certification, transfer evidence, and corporate adaptation package |
| `docs/phases/PHASE_2_EVIDENCE_INDEX.md` | Phase 2 work-item source, implementation, verification, and independent-review evidence index |
| `docs/phases/PHASE_3_GUIDED_ROLE_AND_ANALYTICS_VERTICAL_SLICE.md` | Active P3 plan for role-aware guided operation, trusted human acceptance, typed analytics artifacts, local previews, and successor-package transfer |
| `docs/phases/PHASE_PLAN_TEMPLATE.md` | Mandatory template for detailed phase plans |
| `docs/runbooks/PROCESS_PACKAGE_SETUP.md` | Minimal setup and test procedure for the synthetic central topology and versioned process-package contract |
| `docs/faq/` | Навигационный FAQ: отдельный self-service entrypoint, назначение продукта, настройка, ежедневная работа, роли, AI-границы, поддержка и понятный статус развития |
| `docs/runbooks/CORPORATE_FLOW_CONTROLS.md` | Check-only corporate-flow, release handoff, role/WIP/pilot safety, and immutable failed-run operating contract |
| `docs/runbooks/CORPORATE_ADAPTATION_AND_PILOT.md` | Phase 3 environment inventory, local configuration, pilot-entry, pilot-evidence, rollback/hold, privacy, and no-fork operating procedure |

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
| `openspec/changes/define-transfer-ready-process-package/` | Active apply-ready change proposing transfer-readiness and weak-model-guardrail capabilities, technical design, and 36 implementation tasks; 34/36 are complete after review gate 2.14.3 |
| `openspec/changes/adopt-nis-corporate-process-governance/` | Active apply-ready change proposing NIS-aligned minor/major/hotfix classification, schema migration, DoR/DoD, Tech Lead workflow, corporate flow controls, release handoff, pilot safety, failed-run retention, and affected accepted-capability deltas |
| `openspec/changes/close-release-integrity-gaps/` | In-progress Phase 2 implementation for deterministic Delta operation semantics, human-authorized dated archive convention, and reviewed process-package/OpenSpec upgrade evidence before successor-candidate freeze |
| `openspec/changes/determinize-weak-model-operational-decisions/` | In-progress Phase 2.11 remediation change with all 13 implementation tasks complete; it moves operation action, policy reason codes, required source inventory, artifact routing, and human action codes into an identity-bound deterministic plan while limiting the model to source-grounded draft or block explanation content |
| openspec/changes/simplify-weak-model-decision-contract/ | Blocked, unarchived historical adapter 2.1 remediation change for decision-discriminated role responses, non-leading guidance, structural-only retry, compatibility, runtime/evidence hardening, and append-only recertification; all 15 technical tasks are complete, but its own failed certification gate prevents accepted-spec promotion/archive. Its former work-item blocker was superseded by passing adapter 2.2; work item 2.11 is closed |
| `openspec/changes/define-fp-analytics-publication-model/` | Planned P5 proposal for one full current analytics page per FP and separate release-increment pages, including FP topology, cross-FP traceability, typed nested renderers, publication manifests, reconciliation, local preview and corporate capability-probe boundaries |
| `openspec/changes/archive/2026-07-23-add-operation-catalog-and-dispatcher/` | Archived accepted P3 change for the canonical operation catalog, generated script documentation, derived route/allowlist validation, and thin local `sdd` dispatcher; its requirements live in `openspec/specs/operation-catalog/` and `openspec/specs/guided-operation-dispatcher/` |
| `openspec/changes/archive/2026-07-09-*/` | Archived Phase 1 OpenSpec change packages promoted into accepted specs by the 2026-07-09 Option A batch archive |
| `docs/audits/P3_STATUS_RECONCILIATION_AUDIT_2026-07-23.md` | Dated evidence audit reconciling P3.1/P3.4 accepted archive/spec status with the phase plan, Roadmap, current audit, and remaining active analytics gate |

## Deterministic Process Artifacts

| Path | Purpose |
|---|---|
| `templates/change/` | Copyable SDD change package skeleton |
| `templates/change/waivers.yaml` | Example structured waiver registry showing the deterministic waiver shape for optional artifact exceptions |
| `scripts/validate_change.py` | Dependency-free Python validator for SDD change package structure, metadata, OpenSpec scenarios, and basic traceability |
| `tests/test_validate_change.py` | Focused validator tests covering thin/full artifact rules, canonical statuses, waiver validation, traceability gaps, staged discovery, and placeholder mode |
| `process/VERSION` | Current working source process-package semantic version (`0.3.6`); immutable externally accepted Phase 2 candidate rc6 remains package `0.3.0` under `D-020` |
| `process/package.yaml` | Process-package metadata, OpenSpec and policy-set pins, workflow/policy manifest references, local schema inventory, and canonical source references |
| `process/workflow.yaml` | Minimal reusable artifact dependency contract for the accepted central topology |
| `process/policies/` | Manifest-driven `sdd-core` policy set with nine versioned static catalogs, including immutable Tech Lead views/actions/authority boundaries |
| `process/schemas/` | Local Draft 2020-12 schemas for package/workflow metadata, schema-v2 changes, gate, Tech Lead, and corporate-flow inputs, policy documents/manifest, central registries/config, optional project adapter, and release manifest |
| `process/validators/config_discovery.py` | Bounded repository/config discovery, duplicate-safe YAML loading, explicit reference resolution, package/schema/policy loading, and final OpenSpec runtime probe |
| `process/validators/config_validation.py` | Structured redacted diagnostics plus pure schema, compatibility, secret, and cross-registry integrity checks |
| `process/validators/policy_validation.py` | Static policy identity/reference/override validation and immutable effective-value snapshots with provenance |
| `process/validators/artifact_gates.py`, `process/validators/lifecycle.py` | Pure immutable-snapshot class-aware report evaluation and read-only six-state forward-transition decisions |
| `process/validators/gate_input.py` | Versioned gate-input schema boundary with stable redacted diagnostics and duplicate-evidence rejection |
| `process/validators/owners.py`, `process/validators/tech_lead.py` | Versioned owner/delegate/zone authority resolution plus immutable-snapshot, check-only Tech Lead views and control-state evaluation |
| `process/roles/*.md` | Bounded analyst, developer, QA, and Tech Lead one-stage instructions with canonical references, negative examples, self-review, and human stop points |
| `process/adapters/*.yaml` | Thin Qwen/DeepSeek/GigaCode-class packaging templates with no policy, transition, canonical-write, or human authority |
| `process/gigacode/` | Управляемые GigaCode instructions: общий `superpowers.md` workflow применяется перед role-aware `sdd-process-companion.md` и устанавливается через package manifest |
| `process/weak_model_kit.py` | Pure authority-labelled read-pack, deterministic launch, operation-evidence, and safe-parallel contract logic |
| `process/certification.py` | Pure deterministic fixture runner, allowlisted validator dispatch, normalized/raw evidence boundary, and exact OpenSpec coverage inventory |
| `process/model_adapter.py` | Generated closed role-specific response schemas, reasoning/final separation, exact parsing, structural retry classification, and mechanical normalization |
| `process/certification/` | Synthetic reference repository, role-output goldens, golden case catalog, eight fail-closed negative families, explicit selector evidence manifest, and accepted/active scenario inventory |
| `process/release/release-manifest.yaml` | Frozen Phase 2.12 release manifest for immutable candidate `phase-2-12-rc7` |
| `process/release/evidence/phase-2-12-*.yaml` | External Windows full-rehearsal and Linux/WSL2 portability-smoke evidence bound to the frozen candidate |
| `process/release/phase-2-14-release-manifest.yaml` | Frozen final Phase 2 release manifest for immutable candidate `phase-2-14-rc4` |
| `process/release/evidence/phase-2-14-*.yaml` | Windows full-rehearsal and Linux/WSL2 portability evidence bound to final candidate `phase-2-14-rc4` |
| `process/release/phase-2-14-rc6-release-manifest.yaml` | Frozen successor manifest for immutable candidate `phase-2-14-rc6`; rc4 manifest remains historical and unchanged |
| `process/release/evidence/phase-2-14-rc6-*.yaml` | Fresh Windows full-rehearsal and Linux/WSL2 portability evidence bound to immutable rc6 |
| `process/certification/evidence/phase-2-11-qwen-remediation-2026-07-16.yaml` | Normalized Qwen adapter `2.0` failed-preflight evidence with immutable adapter `1.0` baseline reference and external raw checksums |
| `process/certification/evidence/phase-2-11-deepseek-remediation-2026-07-16.yaml` | Normalized DeepSeek adapter `2.0` failed-preflight evidence with immutable adapter `1.0` baseline reference and external raw checksums |
| `process/certification/evidence/phase-2-11-qwen-adapter-2-1-2026-07-16.yaml` | Normalized Qwen adapter `2.1` failed-preflight evidence: 2/5, zero retries, matrix not run, runtime/preflight/attempt checksums, and immutable adapter `2.0` baseline reference |
| `process/certification/evidence/phase-2-11-deepseek-adapter-2-1-2026-07-16.yaml` | Normalized DeepSeek adapter `2.1` failed-preflight evidence: 0/5, zero retries, matrix not run, runtime/preflight/attempt checksums, and immutable adapter `2.0` baseline reference |
| `process/certification/evidence/phase-2-11-qwen-adapter-2-2-2026-07-17.yaml` | Normalized Qwen adapter `2.2` certification evidence: 5/5 preflight, 15/15 matrix, attempt-1 results, operation-plan identities, raw checksums, and immutable adapter `2.1` baseline reference |
| `process/certification/evidence/phase-2-11-deepseek-adapter-2-2-2026-07-17.yaml` | Normalized DeepSeek adapter `2.2` certification evidence: 5/5 preflight, 15/15 matrix, attempt-1 results, operation-plan identities, raw checksums, and immutable adapter `2.1` baseline reference |
| `process/certification/evidence/phase-2-14-*-adapter-2-2-2026-07-18.yaml` | Final candidate-specific Qwen and DeepSeek normalized evidence: 5/5 preflight, 15/15 matrix, full external raw-root binding, launch provenance, and adapter `2.1` baseline references |
| `process/certification/evidence/phase-2-14-rc5-*-adapter-2-2-2026-07-20.yaml` | Fresh package-0.3.0 Qwen and DeepSeek evidence selected by rc6: runtime identity, 5/5 preflight, 15/15 matrix, exact raw references, and advisory-only authority |
| `process/certification/runtime-identities.yaml` | Immutable full-digest extension to the semantic matrix catalog, used by fresh preflight and per-matrix-call runtime probes without duplicating tag/runtime ownership or rewriting historical evidence |
| `process/operation_plan.py` | Minimal deterministic case evaluator that binds weak-model action, artifact kind, reason codes, verified source inventory, unresolved inputs, and accountable human route before generation |
| `process/catalogs/guided-owner-workflow.yaml`, `process/guided_workflow.py` | Versioned situation-to-command catalog and read-only deterministic guidance boundary; it never makes a human decision or invokes a mutation |
| `pyproject.toml`, `process/operation_dispatcher.py` | Portable Python console-script package for the installed public `sdd` entrypoint, including version diagnostics, confirmed local setup, and canonical continuation guidance |
| `process/read-packs/guided-owner-workflow.yaml` | Bounded AI route instruction: it permits explanation and missing-context checks only, with explicit stop points and no mutation/approval authority |
| `scripts/guided_owner_workflow.py`, `scripts/validate_guided_owner_workflow.py` | Human/JSON guidance entry point and guide/catalog drift check |
| `docs/runbooks/GUIDED_OWNER_WORKFLOW.md` | Situation-first onboarding for humans and AI assistants, pinned to the catalog checksum |
| `process/schemas/weak-model-operation-plan.schema.json` | Closed identity-bound adapter `2.2` operation-plan contract |
| `process/feedback_policy.py` | Pure check-only NIS feedback/SLA/disposition/publication-boundary evaluator with no Confluence integration |
| `process/corporate_adaptation.py` | Pure closed-schema, secret/privacy, green-checklist, pilot-evidence decision-reference, package-completeness, and no-fork validation |
| `process/templates/corporate-adaptation/` | Non-secret unresolved templates for environment inventory, configuration, pilot entry, pilot evidence, and no-fork assessment |
| `process/examples/corporate-adaptation/` | Fully synthetic pilot-evidence and routed no-fork examples; never real pilot or corporate configuration evidence |
| `scripts/validate_corporate_adaptation.py` | Read-only human/JSON validator for one adaptation document or the closed shipped template/example package |
| `tests/test_corporate_adaptation.py`, `tests/fixtures/corporate-adaptation/` | Scenario-first positive/negative schema, privacy, readiness, no-fork, CLI, and package-completeness evidence for work item 2.13 |
| `tests/test_*.py` `SCENARIO_COVERAGE` markers | Test-source-owned exact selector-to-pytest-node bindings used to reject duplicate, unknown, unused, or unrelated evidence substitution |
| `tests/test_feedback_policy.py` | Eight exact deterministic scenarios for the modified NIS feedback/publication-boundary requirement |
| `scripts/build_read_pack.py`, `scripts/launch_role_task.py`, `scripts/check_weak_model_evidence.py`, `scripts/check_parallel_plan.py` | Stable AI-disabled weak-model kit entry points |
| `scripts/certify_process_release.py` | Thin CWD-independent fixture-certification and coverage entry point; actual model/cross-platform execution remains later work |
| `scripts/check_actual_certification_gate.py` | Read-only observed-identity/hash/count/status gate that blocks a model-family matrix until its same-adapter 5/5 preflight passes |
| `tests/test_weak_model_kit.py` | Scenario-first launch, missing context, authority, derived-output, adapter, role, and parallel-safety evidence |
| `docs/runbooks/WEAK_MODEL_OPERATING_KIT.md` | Operator launch, evidence, adapter-failure, AI-disabled, and safe-parallel procedure |
| `docs/runbooks/CERTIFICATION_EVIDENCE.md` | Fixture certification, raw/normalized storage boundary, privacy controls, coverage gaps, and future-work disclosure |
| `templates/team-specs/` | Placeholder-only synthetic central topology with approved config names and canonical directory roots |
| `templates/project-adapter/.sdd-project.yaml` | Optional synthetic project-repository pointer to central `team-specs` and package/config versions |
| `tests/fixtures/process-package/` | Positive release-manifest and negative schema/reference/privacy fixture families for work item 2.1 |
| `tests/test_process_package.py` | Test-only YAML/schema, local-reference, cross-file-integrity, and bounded sensitive-value harness |
| `scripts/validate_process_config.py` | Thin non-mutating human/JSON entry point for production configuration discovery and compatibility validation |
| `tests/test_validate_process_config.py` | Focused central/adapter discovery, compatibility, integrity, secret-redaction, diagnostics, exit-code, and CWD-independence evidence |
| `tests/fixtures/policy-v2/` | Synthetic minor/major/hotfix, decision-input, corporate-value, and override fixture families for work item 2.3 |
| `tests/test_policy_schema_v2.py` | Scenario-first static schema-v2, policy manifest, integrity, override, provenance, and no-premature-verdict evidence |
| `process/validators/classification.py` | Pure policy-snapshot-driven minor/major/hotfix classifier and stable human/JSON report model |
| `process/validators/classification_migration.py` | Non-mutating legacy migration planning and plan-digest-guarded, backup-first idempotent apply behavior |
| `scripts/classify_change.py` | Thin deterministic human/JSON classification entry point |
| `scripts/migrate_change_classification.py` | Thin check/apply legacy classification migration entry point |
| `process/templates/change-v2/`, `process/examples/classification/` | Current schema-v2 authoring surface and synthetic examples offering only minor/major/hotfix |
| `process/read-packs/classification.yaml` | Authority-labelled bounded classifier read pack referencing canonical policy rule IDs |
| `tests/test_classification.py`, `tests/test_classification_migration.py` | Scenario-first work item 2.4 classifier, authority, report, CLI, and migration safety evidence |
| `docs/runbooks/CLASSIFICATION_AND_MIGRATION.md` | Operator procedure for classification, compatibility window, check-before-apply, rollback/hold, and historical exclusion |
| `scripts/evaluate_change_gates.py`, `scripts/check_lifecycle_transition.py` | Thin non-mutating human/JSON entry points for six gate reports and forward-adjacent lifecycle decisions |
| `tests/test_artifact_gates.py`, `tests/test_lifecycle_gates.py`, `tests/test_gate_cli.py` | Scenario-first artifact, gate, lifecycle, authority, freshness, schema-boundary, CLI, and non-mutation evidence |
| `docs/runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md` | Operator input contract, commands, exit codes, authority boundary, and manual decision guidance for work item 2.5 |
| `docs/runbooks/TECH_LEAD_GOVERNANCE.md` | Work item 2.6 owner/review/control inputs, commands, stable exits, non-mutation boundary, and synthetic AI-disabled evidence |
| `tests/fixtures/tech-lead/` | Synthetic event/checkpoint, stop/resume, and forbidden-AI cases; explicitly not actual Qwen/DeepSeek certification |

## Phase 2 External Evidence

The reusable package, templates, schemas, fixtures, release candidate, and corporate-adaptation package now exist in the repository. Raw model and rehearsal output remains outside Git by policy:

| Path | Purpose |
|---|---|
| External versioned `raw-artifact-v0.2.*-*-2026-07-*` roots | Immutable AI-disabled and actual Qwen/DeepSeek raw evidence outside Git for adapters `1.0`-`2.2`; normalized evidence and checksums are committed. Adapter `2.2` certified both model families and closed work item 2.11 |

## Skills

Workflow skills are global (`~/.codex/skills`): architecture-planner, phase-planner, phase-step-runner, phase-full-runner, phase-change-intake, openspec-*, handoff-to-claude, session-report, doc-sync-audit. This repository intentionally has no `.codex/skills/` directory.
