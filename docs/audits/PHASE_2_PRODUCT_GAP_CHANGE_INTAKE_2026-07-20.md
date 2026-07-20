# Phase 2 Product-Gap Change Intake

Date: 2026-07-20

Status: complete; prioritized release-integrity proposal is apply-ready

Source: human-accepted residual-gap remediation sequence

## Outcome

The 13 genuine product-gap selectors are preserved as six normalized intake groups. The earlier selector audit said “six groups” but listed seven proposed change IDs; this intake resolves that discrepancy by treating the two later capability-expansion proposals as one group with two independently owned future changes. No selector is removed, downgraded to documentation evidence, or treated as covered.

| Intake group | Selectors | Decision | Primary phase | Durable destination | Candidate effect |
|---|---:|---|---|---|---|
| Delta operation contract | 3 | `create_openspec_change` | P2 | `close-release-integrity-gaps` | blocks successor freeze |
| Archive history convention | 2 | `create_openspec_change` | P2 | `close-release-integrity-gaps` | blocks successor freeze |
| Reviewed upgrade evidence | 1 | `create_openspec_change` | P2 | `close-release-integrity-gaps` | blocks successor freeze |
| Feedback disposition records | 3 | `defer` | P4 | future `strengthen-feedback-disposition-records` | visible residual gap; does not block first MVP under `D-019` |
| CODEOWNERS derivation/validation | 1 | `defer` | P3 | future `derive-codeowners-from-owner-registry` | visible residual gap; evaluated with real repository wiring |
| Later capability expansion | 3 | `defer` | P4 | future `add-advisory-traceability-suggestions` and `implement-existing-code-baseline` | visible residual gaps; outside first-MVP enforcement |

The three Phase 2 groups are combined into one bounded release-integrity change because partial completion would make candidate-freeze readiness ambiguous. The implementation surfaces remain separate and independently tested. The other three groups stay as explicit residual gaps until their owning phases create and accept their own OpenSpec changes.

## Intake 1 — Delta operation contract

```text
Idea: Deterministically enforce that ADDED introduces new behavior, REMOVED carries reason and migration evidence, and RENAMED does not hide a content change.
Source: Three exact product-gap selectors from the 2026-07-20 selector review and human priority direction on 2026-07-20.
Type: data_contract_change, verification_change
Decision: create_openspec_change
Reason: Certification currently parses Delta operations for scenario composition, but no product validator enforces the accepted semantic vocabulary. A malformed delta can alter the accepted-spec view and is therefore a release-integrity risk.
Affected specs: change-artifact-contracts / Delta Spec operation vocabulary.
Affected architecture: Deterministic change validation compares a bounded delta with its accepted capability baseline; Git/OpenSpec remains canonical and AI has no gate authority.
Data contract impact: Operation-section shape and validation diagnostics become enforceable; REMOVED reason/migration and pure RENAMED mappings are required.
Verification impact: RED/GREEN positive and negative fixtures for all three scenarios, stable diagnostics, selector-level bindings, full regression, strict OpenSpec validation, and later candidate-bound certification.
Status: routed to apply-ready Phase 2 change close-release-integrity-gaps; blocks successor candidate freeze until implemented and reviewed.
```

## Intake 2 — Archive history convention

```text
Idea: Enforce a human-authorized dated archive path and stable greppable archive commit subject without giving automation approval or Git authority.
Source: Two exact product-gap selectors from the 2026-07-20 selector review and human priority direction on 2026-07-20.
Type: new_feature, data_contract_change, verification_change
Decision: create_openspec_change
Reason: The current packaged flow prepares archive-review evidence and protects accepted history, but it neither performs a guarded dated archive move nor validates the resulting path and commit convention.
Affected specs: change-lifecycle / Archive history convention.
Affected architecture: A bounded local archive operation separates human approval, filesystem movement, convention validation, and the user-authorized Git commit.
Data contract impact: Archive preparation/result evidence gains explicit date, target, approval reference, and required commit subject.
Verification impact: RED/GREEN tests cover authorization, target containment, collision/already-archived rejection, dated movement, commit grammar, and pre-mutation failure safety.
Status: routed to apply-ready Phase 2 change close-release-integrity-gaps; blocks successor candidate freeze until implemented and reviewed.
```

## Intake 3 — Reviewed upgrade evidence

```text
Idea: Require reviewed change-package evidence before process-package or OpenSpec compatibility checks can authorize an update.
Source: One exact product-gap selector from the 2026-07-20 selector review and human priority direction on 2026-07-20.
Type: data_contract_change, verification_change
Decision: create_openspec_change
Reason: Transactional update and rollback protect files but do not prove that compatibility, templates, validators, and rollback/hold consequences were reviewed before replacement.
Affected specs: repo-topology-config / OpenSpec version pin and upgrade policy.
Affected architecture: Local schema-bound evidence is checked before staging; update remains transactional and AI-disabled, and the human review decision remains authoritative.
Data contract impact: A versioned upgrade record binds change/review evidence, from/to identities, strict validation, applicable checks, and rollback or hold instructions.
Verification impact: RED/GREEN valid, missing, stale, mismatched, incomplete, and AI-only evidence tests plus unchanged-installation failure assertions and update/rollback regression.
Status: routed to apply-ready Phase 2 change close-release-integrity-gaps; blocks successor candidate freeze until implemented and reviewed.
```

## Intake 4 — Feedback disposition records

```text
Idea: Require accepted feedback to name its canonical source change, rejected feedback to record a reason, and duplicate feedback to link the original disposition.
Source: Three exact product-gap selectors from the 2026-07-20 selector review.
Type: data_contract_change, verification_change
Decision: defer
Reason: The accepted feedback semantics are useful, but the first MVP explicitly excludes generated Confluence publication and its operational feedback loop. Implementing a stronger publication-facing record now would expand the accepted first-MVP boundary rather than protect the selected local release-integrity path.
Affected specs: confluence-feedback-loop / Feedback loop disposition.
Affected architecture: Future generated-publication feedback returns to Git/OpenSpec; no remote Confluence integration is authorized by this intake.
Data contract impact: Future disposition schema will require source-change, rejection-reason, or duplicate-source fields according to outcome.
Verification impact: Future Phase 4 schema and evaluator RED/GREEN tests plus publication-boundary regression; the three selectors remain explicit product gaps meanwhile.
Status: deferred to primary phase P4 under future change strengthen-feedback-disposition-records; does not block first-MVP transfer readiness under D-019.
```

## Intake 5 — CODEOWNERS derivation or validation

```text
Idea: Generate or validate project CODEOWNERS from the canonical owners registry when a real repository uses CODEOWNERS.
Source: One exact product-gap selector from the 2026-07-20 selector review.
Type: new_feature, architecture_change, verification_change
Decision: defer
Reason: The current first topology already defines owners.yaml and deterministic reviewer assignment, while CODEOWNERS is conditional on a project repository using it. Correct path semantics and repository boundaries should be proven during real corporate repository wiring rather than guessed in the reusable core.
Affected specs: repo-topology-config / Owner registry and reviewer assignment.
Affected architecture: owners.yaml remains canonical; any future generator is a derived adapter and cannot become a second owner source.
Data contract impact: Future repository adapter mapping and consistency diagnostics for CODEOWNERS paths and owner groups.
Verification impact: Phase 3 synthetic plus real-repository consistency tests, stale/manual-fork rejection, and no-secret/path-leak checks; the selector remains an explicit product gap meanwhile.
Status: deferred to primary phase P3 under future change derive-codeowners-from-owner-registry; it is evaluated after an accepted successor is transferred for configuration.
```

## Intake 6 — Later capability expansion

```text
Idea: Add bounded AI suggestions for missing traceability links and a read-only existing-code baseline that keeps known gaps visible.
Source: Three exact product-gap selectors from the 2026-07-20 selector review, represented historically by two proposed change IDs.
Type: new_feature, data_contract_change, verification_change
Decision: defer
Reason: Both capabilities are accepted direction but neither is required to enforce the deterministic first-MVP change flow. AI suggestions belong to the progressive automation horizon, and legacy baseline onboarding is a separate read-only scan/baseline/map/validate workflow. Combining either with release-integrity remediation would enlarge scope and candidate risk.
Affected specs: traceability-contract / AI advisory suggestions and Legacy baseline traceability; change-artifact-contracts / Legacy baseline mode where implementation requires it.
Affected architecture: Deterministic traceability remains authoritative; AI output stays advisory; legacy discovery remains read-only and may not hide gaps in generated views.
Data contract impact: Future suggestion records and legacy baseline artifacts with source, confidence/review, known-gap, risk, and regression fields.
Verification impact: Separate Phase 4 OpenSpec changes and RED/GREEN suites for advisory authority boundaries and baseline gap visibility; all three selectors remain explicit product gaps meanwhile.
Status: deferred to primary phase P4 under future changes add-advisory-traceability-suggestions and implement-existing-code-baseline; does not block first-MVP transfer readiness under D-019.
```

## Execution Gate

`close-release-integrity-gaps` is apply-ready but not implemented. The next permitted work item is its ordered RED/GREEN implementation. Candidate freeze is prohibited until all six release-integrity selectors have exact passing evidence, the working inventory reaches the expected `295/7/32`, complete verification and independent review pass, and documentation agrees. Only then may a new immutable candidate be frozen and receive fresh candidate-bound deterministic, AI-disabled, Qwen, DeepSeek, Windows, WSL2, rollback/privacy, source-coverage, and independent-review certification.

## Status Reconciliation

- Roadmap phases: P0 `closed`, P1 `closed`, P2 `in_progress`, P3 `planned`, P4 `planned`.
- Phase 2: work items 2.1-2.13 and historical rc4 gates 2.14.1-2.14.3 remain closed; 2.14.4 is `blocked` by the named successor remediation and certification evidence.
- OpenSpec change: `close-release-integrity-gaps` is `in_progress`, owned by P2, related to P3, and apply-ready with 4/4 planning artifacts; no implementation task is marked complete.
- Machine governance: roadmap/OpenSpec validator reports zero errors. Its two warnings are pre-existing lifecycle warnings for completed adapter changes that remain unaccepted or blocked; they do not authorize acceptance and are not blockers introduced by this intake.
- No phase or gate is implicitly accepted, and no parallel successor freeze is safe while the release-integrity change is unimplemented.
