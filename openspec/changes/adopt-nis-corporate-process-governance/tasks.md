## 1. Policy and schema foundation

- [x] 1.1 Define schema-version-2 `change.yaml` fields for `classification`, separate work `type`, lifecycle `status`, classification evidence, decision ownership, and compatibility metadata; validate against `corporate-change-classification` and `change-package-foundation` scenarios.
- [x] 1.2 Define canonical, versioned policy schemas for classification rules, class artifact matrices, readiness/completion gates, regression rules, stop/escalation records, release packages, pilot safety, and failed-run evidence.
- [x] 1.3 Add synthetic valid and invalid minor, major, and hotfix fixtures, including unknown inputs, conflicting legacy metadata, under-classification, major-impact hotfix, and non-urgent pseudo-hotfix cases.
- [x] 1.4 Add deterministic policy/config discovery from the central process package and project adapter, including clear failure for missing corporate values and attempts to weaken non-configurable minimums.

## 2. Classification and legacy migration

- [x] 2.1 Implement the deterministic classifier with all-conditions minor eligibility, any-trigger major routing, harm-based hotfix eligibility, and complete triggered-rule output.
- [x] 2.2 Implement stable human-readable and JSON classification reports containing source inputs, unknowns, blockers, required artifacts/reviewers, policy version, and human-decision state.
- [x] 2.3 Implement human classification confirmation, audited source-evidence correction and recalculation, stricter-route selection, and negative tests proving waiver, Tech Lead, AI, or free text cannot lower a major-trigger change to minor.
- [x] 2.4 Implement non-mutating migration check mode for `mode: thin -> classification: minor` and `mode: full -> classification: major`, with no automatic hotfix mapping.
- [x] 2.5 Implement idempotent migration apply mode that preserves unrelated metadata, refuses conflicts/ambiguity, excludes archived history, and emits rollback/hold evidence.
- [x] 2.6 Replace target templates, diagnostics, examples, tests, read packs, and generated views so new user-facing behavior no longer offers `thin` or `full`; retain explicit historical/migration references only.

## 3. Artifact matrices and business gates

- [x] 3.1 Implement the minor, major, and hotfix artifact/evidence matrices with substantive-content checks, conditional not-applicable results, waiver eligibility, and restricted hotfix deferrals.
- [x] 3.2 Implement review-ready and common/class-specific Definition of Ready reports, including blocking versus advisory gaps and required human approvals.
- [x] 3.3 Implement implementation-complete and common/class-specific Definition of Done reports without treating an AI completion statement as evidence.
- [x] 3.4 Implement separate release/transfer readiness and archive-readiness reports, including not-applicable rationale and external delivered/Done distinction.
- [x] 3.5 Update lifecycle transition validation so DoR guards `spec_review -> approved`, DoD plus applicable release evidence guards `in_implementation -> ready_to_archive`, and archive remains explicitly human-approved.
- [x] 3.6 Add negative tests for skipped states, placeholder artifacts, unresolved hotfix reconciliation, invalid waivers, stale evidence, and attempts to infer Jira Done or deployment from archive.

## 4. Tech lead workflow support

- [x] 4.1 Extend `owners.yaml` and config schemas with tech-lead zones, delegates, escalation routes, decision authority, and conflict/missing-owner validation.
- [x] 4.2 Build the bounded tech-lead review pack from canonical requirements, scenarios, design decisions, affected repositories/zones, dependencies, risks, regression obligations, blockers, and waivers.
- [x] 4.3 Implement tech-lead classification, readiness, architecture-decision, owner/dependency, and scope-drift reports with source links and deterministic policy versions.
- [x] 4.4 Implement tech-lead stop/hold/escalation/resume records and validation, including proof that AI cannot resume work or clear a hold.
- [x] 4.5 Implement configurable scheduled/event-driven Tech Lead control reports plus completion, release-readiness, waiver-expiry, and hotfix-follow-up views without replacing QA, product, security, release, merge, archive, or tracker approvals.
- [x] 4.6 Add tech-lead role instructions and certification scenarios covering positive decisions, under-classification, missing context, unsafe continuation, authority limits, and AI-disabled operation.

## 5. Corporate flow-control records

- [x] 5.1 Implement preliminary initiative triage and approved-input baseline records with proceed/hold/split/redirect/reject outcomes.
- [x] 5.2 Implement material scope-drift detection inputs and reassessment of classification, readiness, owners, regression, estimates, and approval.
- [x] 5.3 Implement class-aware quality-strategy and regression-matrix schemas, configured QA-owner sufficiency/result decisions, and deterministic coverage-gap reporting.
- [x] 5.4 Implement structured deviation, waiver, deferral, stop, hold, escalation, resume, human-decision, and AI-execution evidence records with expiry/follow-up behavior plus non-disableable canonical production stop triggers.
- [x] 5.5 Implement the versioned release/transfer-package manifest, tracker/Git/OpenSpec/PR/CI/artifact-repository evidence chain, and consumer acceptance/deviation record using synthetic external-contour fixtures.
- [x] 5.6 Implement the portable human role map and role-understanding walkthrough evidence for business/product, analyst, developer, QA, Tech Lead, release/support, and architecture/security when applicable; reject missing-owner AI substitution and checklist-only certification.
- [x] 5.7 Define the portfolio WIP and pilot-selection record, with explicit prioritization/hold behavior when an approved WIP limit is exceeded.

## 6. Pilot safety and failed-run integrity

- [x] 6.1 Implement source-linked failed-run evidence for validation, AI, adapter, integration, and workflow attempts; prove that a successful retry cannot erase or overwrite the failed attempt.
- [x] 6.2 Build a monitored-pilot safety template and risk register covering data/privacy, secrets, access, accidental delivery, rollback/hold, adapters/MCPs, model/runtime, logging, dependencies, support, evidence corruption, and bypass risks.

## 7. Traceability, publication, and integration boundaries

- [x] 7.1 Extend traceability schemas and validators to link classification confirmation/correction, DoR/DoD, stop/resume, release, waiver/deferral, and hotfix reconciliation evidence to requirements and scenarios.
- [x] 7.2 Update read packs, reports, role guides, and future Confluence views to display canonical record IDs and policy versions instead of duplicating normative rules.
- [x] 7.3 Implement validated external workflow mapping that keeps OpenSpec archive, release readiness, deployment, acceptance, and corporate tracker Done distinct and stops on unknown mappings.
- [x] 7.4 Document and test the manual, AI-disabled fallback for every core gate when Jira, Confluence, model runtime, MCP, or role inbox integration is unavailable.

## 8. Certification, migration rehearsal, and release acceptance

- [ ] 8.1 Add deterministic unit/integration coverage for all positive and negative requirement scenarios and keep fixtures free of corporate identifiers and secrets.
- [ ] 8.2 Run minor, major, hotfix, migration, tech-lead, hold/resume, release-package, failed-run-retention, and pilot-safety walkthroughs in AI-disabled mode and record source-linked results.
- [ ] 8.3 Run the approved Qwen-class and DeepSeek-class certification matrix, including authority-boundary, failed-run, manual-intervention, and QA-review cases.
- [ ] 8.4 Rehearse check/apply migration, idempotency, process-package version rollback/hold, and no-archive-rewrite behavior on synthetic legacy and current packages.
- [ ] 8.5 Update the transfer manifest, adaptation checklist, operating runbook, phase evidence index, and release-candidate acceptance packet with all new schemas, reports, role evidence, limitations, and follow-ups.
- [ ] 8.6 Run `openspec validate --all --strict`, project verification, secret/privacy scans, documentation-sync audit, and a source-linked human acceptance-readiness review before requesting human acceptance for the transfer-ready release.
- [ ] 8.7 Stop at the external release-candidate human-owner gate with mandatory Tech Lead and QA evidence plus security evidence when applicable; do not begin corporate configuration or the pilot before acceptance.
- [ ] 8.8 After external acceptance, configure real corporate values and run one monitored Phase 3 change without creating an internal behavior fork.
