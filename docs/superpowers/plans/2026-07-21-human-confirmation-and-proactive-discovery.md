# Human Confirmation and Proactive Discovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent GigaCode from inventing human words or authority while keeping chat decisions and adaptive specification discovery convenient for colleagues.

**Architecture:** A natural-language decision creates only a typed `decision_draft`; a distinct active-card confirmation creates an immutable confirmation event bound to the shown revision. A discovery map records only explicit human confirmations, defaults or deferrals and drives a deterministic readiness summary.

**Tech Stack:** Python 3, YAML/JSON Schema, existing local package validators, pytest, OpenSpec Markdown.

## Global Constraints

- P3 remains local, deterministic and MCP-free.
- AI must not create human acceptance, DoR, lifecycle or implementation authority from its own text or files.
- The only accepted short confirmation is `Подтверждаю` immediately after the active `DEC-…` card.
- A future form/command must emit the same confirmation-event contract and is outside this plan.

---

### Task 1: Typed decision-card contracts

**Files:**
- Modify: `process/schemas/spec-acceptance.schema.json`
- Create: `process/schemas/decision-draft.schema.json`
- Create: `process/schemas/confirmation-event.schema.json`
- Modify: `process/package.yaml`
- Test: `tests/test_p3_vertical_slice.py`

- [ ] Write failing schema tests for a card with code, change id, revision digest, quoted source message and expiry; reject missing/changed binding.
- [ ] Implement schemas and register them in the package manifest.
- [ ] Run the focused schema tests and confirm they pass.

### Task 2: Deterministic confirmation transition

**Files:**
- Modify: `process/guided_process_integrity.py`
- Create: `process/chat_decisions.py`
- Modify: `scripts/guided_process_summary.py`
- Test: `tests/test_p3_vertical_slice.py`

- [ ] Write failing transcript tests: natural decision creates only a draft; active exact code and immediate short confirmation record a decision; `Да`, `что дальше?`, `продолжай`, stale code and interleaved text cannot.
- [ ] Implement card issue/confirm functions with no lifecycle mutation and a derived status summary.
- [ ] Run focused decision tests and confirm they pass.

### Task 3: Proactive discovery map

**Files:**
- Create: `process/schemas/discovery-map.schema.json`
- Create: `process/discovery.py`
- Modify: `process/guided_workflow.py`
- Modify: `process/gigacode/AGENTS.md`
- Modify: `process/gigacode/skills/sdd-process-companion.md`
- Test: `tests/test_p3_vertical_slice.py`

- [ ] Write failing tests for a material unresolved area in `обычно`, explicit default/defer recording, and silence retaining unresolved status.
- [ ] Implement change-specific area classification and the three permitted choices without a fixed questionnaire.
- [ ] Run focused discovery tests and confirm they pass.

### Task 4: Documentation, package transfer and verification

**Files:**
- Modify: OpenSpec design/spec/tasks, phase plan, runbook/read-pack and current audit
- Modify: templates and package version files as required by registered assets
- Test: `tests/test_process_package.py`, `tests/test_packaged_flow.py`

- [ ] Update source documentation and package templates to describe the decision card and proactive depth contract.
- [ ] Run one final relevant pytest suite, `openspec validate --all --strict`, roadmap/OpenSpec validation, `git diff --check` and one AI-disabled transcript walkthrough.
- [ ] Update sandbox only through package `check`/`update`; exclude its unrelated untracked paths; create separate source and sandbox commits without push.

## Self-Review

- Every authority-changing record is bound to an explicit, verifiable human message pair.
- No requirement treats silence or an AI-authored file as a decision.
- `обычно` proactively surfaces material unknowns without becoming a universal questionnaire.
- The future form reuses, rather than bypasses, the confirmation-event contract.