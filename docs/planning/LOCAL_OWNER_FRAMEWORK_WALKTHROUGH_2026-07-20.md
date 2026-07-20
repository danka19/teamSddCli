# Local Owner Framework Walkthrough

Date: 2026-07-20

Status: planned entry gate before corporate adaptation.

## Intake Decision

Type: verification change and scope refinement.

Route: adopt now as a Phase 3 entry gate. This does not change product behavior, reopen Phase 2, mutate immutable candidate `phase-2-14-rc6`, or create a successor candidate.

## Purpose

The human owner will exercise the accepted framework locally before any corporate configuration, approved integration wiring, or monitored pilot. The walkthrough must use synthetic data and cover deterministic and AI-assisted operation without transferring approval authority to AI.

## Required Coverage

- orientation, configuration, immutable-candidate identity, and AI-disabled fallback;
- `minor`, `major`, and `hotfix` flows, including under-classification and unsafe-hotfix negative cases;
- analyst, developer, QA, and Tech Lead AI role operations, plus human change-owner, release, support, architecture, and security responsibilities where applicable;
- DoR, implementation, DoD, stop/hold/escalate/resume, waiver, release, traceability, hotfix reconciliation, archive, failed-run retention, update, rollback, and reviewed-upgrade evidence;
- missing context, conflicting sources, fabricated evidence, forbidden approval, unsafe resume, unavailable integration, privacy, and secret-handling cases;
- local Qwen-class and DeepSeek-class exercises when the runtimes are available, always checked by deterministic validation;
- a final coverage matrix and owner judgment: `ready`, `ready with conditions`, or `not ready` for corporate adaptation.

## Operating Rules

- The facilitator advances one mechanism at a time and waits for the owner to perform or confirm each human action.
- Use only local synthetic identifiers and data. Do not access corporate systems or place credentials, endpoints, or internal artifacts in the repository.
- Do not modify immutable release candidates, certification artifacts, accepted OpenSpec archives, or canonical product behavior during the walkthrough.
- Do not commit, push, publish, install dependencies, use network access, or write outside an explicitly agreed disposable location without separate human approval.
- Record mismatches as product, documentation, usability, environment, or expected-scope findings and route proposed remediation through `phase-change-intake`.

## Completion Gate

The entry gate closes only when the human owner has personally completed the planned modules, reviewed the evidence matrix and unresolved findings, and explicitly authorizes bounded Phase 3 corporate-environment intake. Completing the walkthrough does not accept the future pilot result.
