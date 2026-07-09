## Context

The repository already has `AGENTS.md`, `docs/AI_STEP_VERIFICATION_CHECKLIST.md`, phase plans, audit notes, and active OpenSpec changes. The governance proposal turns those operating habits into testable future requirements without promoting them to accepted specs yet.

## Proposed Design

Documentation governance applies when work changes any of the following:

- SDD workflow behavior
- CLI or future command behavior
- artifact/process contracts
- setup, operations, security, or integration boundaries
- roadmap, phase status, or acceptance gates
- user-visible command/help text
- accepted or proposed OpenSpec behavior

For each change, the worker records whether docs need updates, updates the narrowest relevant docs, and reports verification evidence. Proposed behavior stays in `openspec/changes/`; accepted behavior is written under `openspec/specs/` only after explicit human archive/acceptance approval.

Language convention (revised by the human decision on 2026-07-06): this project's own process specs are written in English; team product analytics specs are written in Russian requirement/scenario prose with English structural keywords (`SHALL`, `WHEN`, `THEN`) so analysts and QA can read the canonical source directly without an AI translation layer; stable IDs are always English and are not translated. A strict-mode OpenSpec validation probe confirmed Russian prose validates. Generated Confluence pages remain read models, not requirement sources; feedback must be dispositioned and, when accepted, converted back into the canonical Git/OpenSpec source. A bilingual glossary is still required for stable IDs and shared terms.

Documentation responsibility is split by content type:

- product behavior and accepted/proposed process behavior belongs in OpenSpec;
- project organization, setup, operations, contribution workflow, integration maps, architecture overviews, legacy notes, AI/agent guidance, and decision rationale belongs in `docs/`;
- temporary execution planning belongs in phase plans or OpenSpec change tasks until accepted.

## Source Ownership And Deduplication

Documentation governance should prevent multiple maintained versions of the same requirement or process rule. The default rule is write once, reference many:

- OpenSpec owns behavior contracts, artifact contracts, lifecycle rules, traceability rules, waiver rules, scenarios, and acceptance criteria.
- `docs/` owns rationale, project organization, repository maps, operating context, phase planning, audit notes, legacy observations, and human decision records.
- `AGENTS.md` plus global skills own agent operating instructions.
- Project memory, role guides, generated Confluence pages, and task read packs are derived or orientation surfaces; they link to canonical sources and should not redefine behavior.
- Jira or another tracker owns workflow/status only after task automation exists; it does not own requirements.

Derived surfaces should carry source IDs, source paths, source commit or generated timestamp where appropriate. When a derived surface disagrees with the canonical source, the derived surface is fixed or regenerated; the project does not patch several copies by hand.

Weak corporate models need explicit authority hints. Generated read packs should mark each file as canonical, supporting context, generated/advisory, or evidence so the model does not infer authority from proximity or recency.

Future deterministic checks should include normative-language linting outside canonical files, duplicate requirement ID detection, source-link checks for memory and role guides, generated-block edit checks, stale-memory checks, and orphan-document checks.

## AI Verification Checklist Evidence

Before claiming completion, the worker records the commands run, blockers, manual checks, documentation updates or a no-documentation-update rationale, residual manual-verification risks, skills used, and subagents used with role names and token counts when available. The AI checklist is evidence of process discipline, not a substitute for deterministic checks or human approval.

## TDD-Style Verification Rules

For deterministic behavior changes, OpenSpec scenarios or acceptance examples are identified before implementation. Tests, schema checks, syntax checks, or manual verification are chosen before code changes where practical. Negative cases are required when the system must not infer too much, accept placeholders, silently skip artifacts, or treat advisory AI output as accepted truth.

## Risks / Trade-offs

- Governance can become busywork if every minor note requires broad documentation updates, so this proposal requires the narrowest relevant durable document.
- Documentation can drift if final reports mention decisions that never reach durable artifacts, so human feedback classification remains required.
- The proposal must not create accepted specs until the final human archive gate.
- Localization and audience adaptation can introduce drift, so generated pages must link back to canonical sources and preserve English stable IDs.
