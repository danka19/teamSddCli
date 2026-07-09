## Context

The architecture says a waiver must have a reason, evidence, and approver. Phase 1 needs a proposed policy before validators can distinguish acceptable exceptions from missing work.

## Proposed Waiver Shape

A waiver should record:

- stable waiver ID
- waiver type, such as `no_new_tests`, `automation_deferred`, `artifact_not_applicable`, or `documentation_deferred`
- affected requirement IDs and scenario IDs
- reason
- evidence
- approver role or group
- date and optional expiry/review point
- replacement verification or follow-up action where applicable

## Approved Human Decisions From Work Item 1.3

Human approval recorded on 2026-07-06: use role-appropriate approvers and require reason, affected requirements/scenarios, approver, substitute evidence, and follow-up/expiry when residual risk remains. Work item 1.8 later updated validator and test behavior against those approved rules, while accepted-spec promotion remains gated by final archive approval.

### Decision: Waiver Approver Model

Approved Option A: Require role-appropriate approval. QA lead or QA owner approves missing test evidence, AT owner approves missing automation evidence, tech lead approves technical risk/design exceptions, and analyst or product owner approves scope/documentation exceptions. This keeps decisions close to accountable owners.

Rejected for the default policy: Require a single process owner approval for all waivers. This is simpler to administer but can bottleneck work and may separate approval from domain expertise.

Rejected for the default policy: Allow change author approval for low-risk thin changes. This is fastest but weakens audit value and risks self-approved quality gaps.

Implementation consequence: validators can later check approver-role fields and required evidence shape, but human review remains responsible for whether the evidence is actually adequate.

### Decision: Minimum Waiver Evidence

Approved Option A: Require reason, affected requirements/scenarios, approver, substitute evidence, and follow-up/expiry when risk remains. This provides auditability without requiring a formal board for every exception.

Rejected for the default policy: Require reason and approver only. This is lightweight but may not prove why the skipped artifact or check is safe.

Rejected for the default policy: Require full risk acceptance records for every waiver. This is rigorous but too heavy for small changes and likely encourages avoidance.

Implementation consequence: archive readiness can later distinguish justified exceptions from missing work by requiring the approved fields and follow-up/expiry when residual risk remains.

### Decision: Waiver Scope

Approved Option A: Allow waivers for missing tests, deferred automation, non-applicable QA/AT artifacts, documentation timing exceptions, or refactor no-behavior-change evidence. Never allow waivers to replace human approval, hide a behavior change, bypass security/compliance review, or make a behavior requirement archive-ready without scenario or acceptance-example coverage. If work is truly not behavior-changing, it must be reclassified or handled through the limited no-spec-change rationale instead of waiving behavior scenario coverage.

Rejected for the default policy: Allow waivers for any deterministic gate with approver evidence. This is flexible but can undermine core SDD guarantees.

Rejected for the default policy: Disallow waivers in the first MVP. This is simple but too rigid for real pilot work.

Implementation consequence: Phase 1 can define negative validator cases for waiver misuse in later validator work.

## Deterministic Gates Versus AI Assistance

Deterministic checks may validate waiver shape, required fields, and links. AI may draft waiver text or point out missing evidence, but only human approval makes a waiver valid.
