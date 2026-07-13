# Documentation And Architecture Review (Fable 5)

Status: recorded audit output. Findings are planning input; scope and contract decisions remain with the human owner.

Date: 2026-07-06.

Reviewer: Claude (Fable 5), acting as documentation/process auditor.

Scope reviewed: `AGENTS.md`, `docs/README.md`, `docs/00_FILE_STRUCTURE.md`, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_STRATEGY.md`, `docs/CONTEXT.md`, `docs/CURRENT_PROJECT_AUDIT.md`, `docs/AI_STEP_VERIFICATION_CHECKLIST.md`, `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`, `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`, `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`, all 7 active OpenSpec changes, `templates/change/`, `scripts/validate_change.py`, `tests/test_validate_change.py`, `.pre-commit-config.yaml`.

Verification baseline at review time: `openspec validate --all --strict` passed 7/7; `openspec list --specs` shows no accepted specs; `python -m pytest tests/test_validate_change.py -v` passed 5/5; `python scripts/validate_change.py --allow-placeholders templates/change` passed; `git diff --check` clean; latest commit `41114fa`.

## 1. Overall Verdict

The direction is coherent. Git/OpenSpec-canonical, deterministic-gates-first, no-custom-CLI-upfront, human-owned approvals, and the thin-MVP boundary are stated consistently across the durable docs, and the 2026-07-06 source-ownership decision gives the project an explicit conflict-resolution order. The OpenSpec proposal set is testable, appropriately negative-case-heavy, and correctly stopped before acceptance.

The three dominant risks are not conceptual but operational:

1. The deterministic layer (validator, template) already lags behind the approved Phase 1 contracts and the proposed lifecycle vocabulary (finding F1).
2. Accepted human decisions are hand-maintained in four to five places each, which contradicts the project's own write-once/reference-many rule (finding F3).
3. The `sdd CLI` command naming used for the MVP creates a standing ambiguity against the accepted no-CLI-upfront strategy that a weak corporate model will not resolve correctly (finding F2).

None of these require re-deciding anything already approved. They require reconciliation edits, one naming clarification, and one small set of new human decisions listed in section 5.

## 2. Findings

### F1. Deterministic layer diverges from approved contracts and proposed lifecycle (high)

Evidence:

- `scripts/validate_change.py` `ALLOWED_STATUSES` accepts `tasks_created`, `in_dev`, `ready_for_qa`, `implemented` — vocabulary inherited from the removed historical architecture draft. The proposed `define-change-lifecycle` states are `draft`, `spec_review`, `approved`, `in_implementation`, `ready_to_archive`, `archived`. The two vocabularies overlap but do not match: the validator accepts statuses the proposed lifecycle forbids and would reject `in_implementation`/`ready_to_archive`.
- `scripts/validate_change.py` `REQUIRED_FILES` requires `design.md`, `qa/test-plan.md`, and `qa/automation-plan.md` for every package, including `mode: thin`. The approved Option A matrix says thin changes do not require QA/AT plans or mandatory design by default.
- `templates/change/change.yaml` defaults to `mode: thin` with `type: new_feature`. Under the approved matrix, `new_feature` is a full-package trigger, so the template's default combination is self-contradictory and is exactly the kind of trap a weak model copies verbatim.

Assessment: this is expected staging (the validator was built in work item 1.1 before the matrix and lifecycle proposals existed), and the phase plan already routes enforcement changes to work item 1.8. But no durable document recorded the divergence, so a future agent could treat the validator's status list or required-file list as approved behavior. The lifecycle status reconciliation is additionally blocked by the open lifecycle-naming decision (`define-change-lifecycle/tasks.md` item 2.2), which was missing from the phase plan's open Human Decisions list.

Action taken in this review: recorded as `AUDIT-016`; drift note added to `define-change-lifecycle/design.md`; lifecycle-naming decision added to the phase plan's open decisions.

Action still required: reconcile statuses, required-file matrix, and template defaults in work item 1.8 after the lifecycle-naming and enforcement-staging decisions (section 5, questions 1 and 2).

### F2. `sdd CLI` naming contradicts the accepted no-CLI-upfront strategy in three docs (high)

Evidence:

- `docs/ROADMAP.md` Phase 2 said "Decide implementation language/runtime for `sdd CLI`" and Phase 3 listed the MVP as bare `sdd change ...` commands, with no mention that the accepted strategy delivers the thin flow via templates/scripts/skills and builds CLI parts only when `docs/IMPLEMENTATION_STRATEGY.md` triggers fire.
- `docs/README.md` Scope listed the full `sdd CLI` command surface (publication, task planning, QA/AT proposals, role inboxes) as "in scope" with no staging qualifier, while Key Decisions in the same file narrow the MVP and defer the CLI.
- `docs/CONTEXT.md` defined `sdd CLI` without stating that it does not exist and is trigger-gated.

Assessment: humans reading the whole file resolve this correctly; a weak model reading one section does not. The worst concrete failure mode: a corporate-environment agent tries to run `sdd change new` (nonexistent binary) instead of copying `templates/change/`, or plans Phase 2 as a CLI build.

Action taken in this review: minimal clarifying edits to all three files aligning them with the already-accepted 2026-07-03 strategy (no new decision made; contradicting derived text was fixed per the source-ownership rule).

### F3. Accepted decisions are quadruplicated, violating the project's own write-once rule (medium, growing)

Evidence: every accepted human decision is separately hand-maintained in (a) `docs/README.md` Key Decisions (29 bullets), (b) `docs/CURRENT_PROJECT_AUDIT.md` Accepted Human Decisions table (23 rows), (c) `docs/ROADMAP.md` Current Roadmap Validation bullets, (d) `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md` decision records, plus (e) decision sections inside change `design.md` files. There are no stable decision IDs, so cross-references are by date and paraphrase.

Assessment: this is the same divergent-copies failure the documentation-governance proposal exists to prevent, applied to decision records instead of behavior text. Each new decision currently costs 4-5 manual edits and each paraphrase is a future contradiction. The copies have not materially diverged yet — this review found only wording drift — which makes now the cheap moment to consolidate.

Recommendation (human decision, section 5 question 3): create one canonical decision log (`docs/DECISIONS.md`, stable IDs `D-001..`) at Phase 1 acceptance readiness; README keeps only a short pointer plus the current-direction summary; audit/roadmap/phase plans reference decision IDs. Not done in this review because it is a visible docs-architecture restructure mid-phase and mechanical churn across every durable doc.

### F4. Missing or unrecorded decisions (medium)

1. OpenSpec version pin: the accepted decision says "the CLI version is pinned", and audit evidence shows `openspec 1.4.1` installed, but no pin is recorded anywhere (no pin file, no version statement in strategy or proposals). Until `define-openspec-version-policy` exists, the pin is a statement without a location. Recorded as `AUDIT-017`.
2. Lifecycle public-vs-internal naming: open in `define-change-lifecycle/tasks.md` 2.2 but was absent from the phase plan's Human Decisions list (fixed in this review). It blocks validator status reconciliation (F1).
3. Enforcement staging for work item 1.8: the exit criteria say the approved matrix is "enforced or explicitly staged as warnings according to the accepted gate decision", but no gate question for warnings-vs-errors staging exists anywhere. Added to section 5, question 2.
4. Historical process-evaluation ownership question: superseded by the 2026-07-13 human decision to remove process-effectiveness evaluation from the target process.

### F5. Proposal-set shape (low)

- `define-confluence-feedback-loop` carries substantial publication-model content (generated view types, publication pipeline, status display) beyond what its change-id advertises. The content is good and intentionally consolidated, but at archive time it should either be renamed/split or the capability name should be accepted as covering publication basics. Flag for the archive gate; no churn now.
- The planned Phase 1 set is nine proposals before any pilot use. `define-repo-topology-config` and `define-openspec-version-policy` (both not yet drafted) are small and mutually coupled: the pin location depends on the topology/config decision. Merging them into one platform-assumptions proposal would remove one proposal and one human gate. Section 5, question 4.

### F6. Minor hygiene (low; fixed in this review where cheap)

- `AGENTS.md` Required Read Order had a stranded item `11.` after the scaling-rule paragraph (list formatting bug). Fixed.
- `docs/00_FILE_STRUCTURE.md` was missing rows for `CLAUDE.md`, `docs/phases/PHASE_0_PROJECT_FOUNDATION.md`, and `docs/phases/PHASE_PLAN_TEMPLATE.md`. Fixed; new audit/planning files from this review added.
- `docs/CURRENT_PROJECT_AUDIT.md` referenced `cde51ef` as the latest known commit; updated to `41114fa`.
- Historical evaluation-data note: superseded by the 2026-07-13 removal of the process-effectiveness evaluation layer.

## 3. Answers To The Audit Questions

1. Coherent direction? Yes. All durable docs agree on canonical source, layer ownership, human approval, and MVP boundary. The contradictions found (F1, F2) are staging lag and naming residue, not conflicting intent.
2. Contradictions? Three material ones: validator/template vs approved matrix and proposed lifecycle (F1); roadmap/README/context CLI wording vs accepted strategy (F2, fixed); minor stale audit references (F6, fixed).
3. Duplicated/divergent rule copies? Yes: decision records (F3) and the source-ownership rule itself, which currently lives in near-identical prose in `docs/CONTEXT.md`, `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`, `define-documentation-governance` design/spec, and README/audit decision entries. Acceptable while the governance spec is proposed; on acceptance, the spec becomes the single normative copy and the others must be reduced to references.
4. Missing decisions? Section 5: lifecycle naming, 1.8 enforcement staging, decision-log consolidation, proposal merge, plus the already-tracked open gates (topology/config, version policy, Confluence owner/SLA, memory schema, final archive).
5. First MVP boundary clean? Yes. Every proposal contains explicit first-MVP-exclusion scenarios; no proposal or doc silently broadens the pilot. The only boundary blur is the template shipping QA artifacts and full-package fields by default (F1), which pressures thin changes toward full-package burden.
6. Memory/guardrails/Graphify/failure-memory/spec-questioning/role-guide placement? Correct layer: recorded as planning input in `docs/planning/`, explicitly non-accepted, explicitly outside MVP, with a designated future proposal (`define-project-memory-and-weak-model-guardrails`) queued after the current set synchronizes. No action needed beyond keeping it out of MVP.
7. Too heavy / too vague / missing deterministic checks? The contract content is proportionate. The Phase 1 process machinery (11 work items, 4-role gates each, 5+ human gates) is heavy for a documentation phase but is Codex's chosen execution discipline and produces small artifacts; not worth changing mid-phase. Deterministic checks are correctly planned but almost all still future (AUDIT-014/015 remain accurate); the only implemented gate is the work-item-1.1 validator, which now needs the F1 reconciliation.
8. Final architecture and staged plan: see `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md`.
9. Human decisions required: section 5.

## 4. Edits Made By This Review

Documentation-only; no template, validator, test, or pre-commit behavior changed; no OpenSpec change archived or promoted.

- `docs/ROADMAP.md`: Phase 2/3 wording aligned with the accepted no-CLI-upfront strategy.
- `docs/README.md`: Scope bullet qualified with staged delivery and trigger-gated CLI.
- `docs/CONTEXT.md`: `sdd CLI` term now states the CLI does not exist yet and is trigger-gated.
- `AGENTS.md` read-order numbering fixed (stranded item 11).
- `openspec/changes/define-change-lifecycle/design.md`: risk note recording the validator status-vocabulary drift and its reconciliation dependency.
- `docs/phases/PHASE_1_DISCOVERY_AND_REQUIREMENTS.md`: lifecycle-naming and 1.8 enforcement-staging added to open Human Decisions.
- `docs/CURRENT_PROJECT_AUDIT.md`: `AUDIT-016` (deterministic-layer drift), `AUDIT-017` (unrecorded version pin) added; stale commit reference updated; this review linked.
- `docs/00_FILE_STRUCTURE.md`: missing rows added; this file and the planning draft registered.
- New: this file; `docs/planning/FABLE5_FINAL_ARCHITECTURE_AND_PLAN_DRAFT_2026-07-06.md`.

## 5. Human Decisions Required Before Implementation Continues

Update 2026-07-06 (same day, later session): the human owner approved the recommended option for questions 1-4. Decisions are recorded in `docs/README.md` Key Decisions, `docs/CURRENT_PROJECT_AUDIT.md`, `docs/ROADMAP.md`, the Phase 1 plan, and the lifecycle proposal. Questions 1-4 below are kept for historical context; only the question-5 gates remain open.

Full Russian decision packets are delivered in the session report; summary for durable record:

1. Lifecycle state naming (blocks F1 status reconciliation in 1.8): adopt the six internal states as canonical with simplified names only in generated views (recommended), or adopt the five simplified public names as canonical.
2. Work item 1.8 enforcement staging: enforce the approved matrix as errors immediately (recommended for a green-field repo with no legacy packages), or stage as warnings for one pilot iteration.
3. Decision-record consolidation: create `docs/DECISIONS.md` as the single canonical decision log with stable IDs at Phase 1 acceptance readiness (recommended), or keep the current multi-file convention.
4. Merge `define-openspec-version-policy` into `define-repo-topology-config` as one platform-assumptions proposal with one human gate (recommended), or keep two separate proposals as planned.
5. Already-tracked open gates (unchanged, listed for completeness): repo topology/config format; Confluence feedback owner/SLA/unresolved comments; project memory folder/schema; final OpenSpec archive/acceptance.
