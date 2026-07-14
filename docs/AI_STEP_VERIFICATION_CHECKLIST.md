# AI Step Verification Checklist

Purpose: define the minimum self-check an AI agent must run before claiming a roadmap step, phase work item, architecture change, CLI command change, SDD workflow change, artifact contract change, code change, or documentation update is complete.

Status: mandatory for future implementation work. If this checklist conflicts with a phase-specific plan, stop and document the conflict instead of guessing.

## Required Pre-Work Check

Before changing code or product documentation, confirm:

- Current branch matches the active phase branch or the user approved a different branch.
- `AGENTS.md`, `docs/README.md`, `docs/00_FILE_STRUCTURE.md`, `docs/ROADMAP.md`, `docs/IMPLEMENTATION_STRATEGY.md`, `docs/CONTEXT.md`, the relevant phase plan, `openspec/` when SDD applies, `docs/CURRENT_PROJECT_AUDIT.md`, and this checklist were read when changing SDD workflow, CLI behavior, product scope, or architecture.
- The active `openspec/changes/<change-id>/` folder was read when work implements or plans a proposed change.
- Phase 2 implementation reads `openspec/changes/define-transfer-ready-process-package/` and `docs/phases/PHASE_2_TRANSFER_READY_PROCESS_PACKAGE.md` before changing package, config, weak-model, certification, release, or transfer behavior.
- Task-specific audit, acceptance-gap, handoff, or planning documents were read.
- Existing code and tests were searched for the concepts being changed.
- The work was classified as CLI behavior, SDD workflow behavior, architecture, setup, operations, security, roadmap status, artifact/process contract, user-visible command/help text, or docs-only.
- Affected OpenSpec requirements, proposed deltas, acceptance scenarios, and expected verification evidence are known before implementation starts.
- New human feedback received during the phase was routed through `phase-change-intake` before changing the active plan.

If documentation is ambiguous, incomplete, or contradictory, say so in the user-facing report and update the relevant work log or audit note instead of silently guessing.

## Human Feedback Memory

Whenever the human owner explains how the product should work, rejects behavior, adds an edge case, corrects terminology, or asks for a verification habit, classify it before finishing:

- `glossary_term`: update `docs/CONTEXT.md`.
- `cli_or_workflow_behavior_rule`: update `openspec/specs/` when accepted current `sdd CLI` or SDD workflow behavior changes, or `openspec/changes/` when the behavior is still proposed.
- `acceptance_criterion`: update the active `openspec/changes/` artifact and relevant phase plan; promote it to `openspec/specs/` only after acceptance.
- `verification_step`: update this checklist.
- `rejected_behavior`: update an audit/acceptance-gap document and this checklist when it affects future verification.
- `open_decision`: record it in the phase plan, audit, or roadmap and state it in the final report.
- `implementation_detail`: document it only where it affects behavior, architecture, setup, operations, security, or future work.
- `reporting_preference`: update `AGENTS.md` and this checklist when the human asks for a different answer style, level of detail, or report structure.

## Advice-Versus-Action Check

- If the human asks "what is next", include a concrete next-step recommendation and explain why it is next.
- If the human asks "how is it better", asks for advice, or asks a conceptual/architecture question, provide a detailed answer first and do not silently implement.
- If the human also explicitly asks to "record", "write", "update", "fix", "continue", or otherwise change project artifacts, make the requested documentation/code change after answering or while clearly separating the action from the advice.
- When there is ambiguity between "answer" and "do", prefer answering and ask for confirmation before implementation unless project safety, durable documentation, or an explicit "record this" request makes the action clear.
- When multiple open questions remain, ask them in one concise batch with recommended defaults and tradeoffs. Ask one-by-one only when one blocking answer is required before any useful next step can happen.
- Human decision-gate questions must be plain and readable for a process owner, not written as terse internal labels. For each blocking decision, state what is being chosen, why it matters, 2-3 concrete options, the recommended default, examples of what changes in day-to-day work, risks/tradeoffs, and what remains blocked if the decision is not made.

## Domain And Architecture Check

- Use canonical terms from `docs/CONTEXT.md`.
- Preserve boundaries between raw input, derived data, review-required proposals, and accepted decisions.
- Do not treat heuristic or LLM output as source-of-truth data.
- Record architecture decisions that affect module boundaries, persistence, integrations, security, deployment, or operations.
- Preserve the deterministic-base boundary while applying `D-013`: first implement and certify the class-aware create/classify/validate/Spec Review/DoR/implementation/DoD/release/archive/traceability flow before adding Jira task automation, generated QA/AT proposals, Confluence publication, or broad role inbox automation. Treat Phase 1 thin/full as legacy migration input, not the target vocabulary.
- New target artifacts and diagnostics use only `minor|major|hotfix`; `thin -> minor` and `full -> major` are migration rules, and no legacy value maps to hotfix automatically.
- Minor is allowed only when every required low-impact condition is known; any material trigger requires major unless an approved urgent hotfix route retains the triggered obligations.
- Hotfix acceleration must not bypass required human ownership, testable scenarios, minimum verification/regression, security/compliance decisions, rollback or hold evidence, traceability, or reconciliation follow-up.
- Keep implementation complete, DoD, release/transfer ready, archive ready, archived, and external delivered/Done distinct in schemas, reports, tests, and integration mappings.
- Tech Lead automation may prepare source-linked reports, questions, packs, and recommendations but must not confirm classification, mark DoR/DoD green, approve waivers/residual risk, resume held work, or approve release/archive state through AI.
- Do not move reusable package, schema, validator, workflow, role-instruction, read-pack, certification, update/rollback, or release-manifest design into the corporate environment. Phase 2 completes and externally certifies that core; Phase 3 supplies only verified real configuration, approved wiring, thin adapters, and pilot evidence.
- Weak models do not select their own workflow or authority. A deterministic launcher or explicit non-AI procedure must supply the role instruction, bounded authority-labelled read pack, output/evidence contract, and stop point.
- Every weak-model-assisted gate must have an AI-disabled fallback, and reusable corporate findings must return to the external OpenSpec workflow rather than create an internal fork.
- Treat the AI-disabled path as the reliability foundation, not the final automation ceiling: later AI automation must be introduced through accepted OpenSpec changes, remain bounded and evidence-backed, and continue to pass deterministic checks.
- Do not require Gherkin for every QA artifact; require a testable scenario first, and require Gherkin only when the scenario is executable or exported to AT.

## Test And Evidence Check

- Treat OpenSpec scenarios as the acceptance starting point for TDD-style work.
- Before writing code, identify whether the change can be covered by CLI tests, schema validation, syntax checks, integration contract checks, or manual verification.
- Add or update tests proportional to risk.
- Cover negative cases where the system must not infer too much.
- Run the narrowest meaningful tests first, then broader tests when shared behavior changes.
- Run `git diff --check` before completion when files changed.
- For SDD/OpenSpecs changes, run `openspec list`, `openspec list --specs`, and `openspec validate --all --strict`.
- For every Delta Spec `MODIFIED` or `REMOVED` requirement, independently verify that the exact requirement heading exists in the accepted capability; for `MODIFIED`, compare the complete replacement block and preserved/replaced scenarios because OpenSpec CLI `1.4.1` validation does not detect every wrong target name.
- For mutating CLI or integration behavior, verify dry-run behavior, idempotency, machine-readable JSON output, and audit logging whenever those contracts are in scope.
- Before claiming Phase 2 release readiness, verify clean bootstrap, packaged minor/major/hotfix flow, configuration/package/OpenSpec compatibility, legacy migration, secret/private-data checks, update/rollback, AI-disabled operation, and actual Qwen-class plus DeepSeek-class analyst/developer/QA/Tech Lead certification with exact model/runtime evidence.
- Before claiming the `D-013` governance implementation complete, verify minor/major/hotfix fixtures, legacy migration preview/apply/idempotency/no-archive-rewrite, under-classification rejection, pseudo-hotfix rejection, DoR/DoD separation, Tech Lead authority limits, stop/resume, release-package, hotfix reconciliation, failed-run retention, pilot safety, AI-disabled execution, and Qwen/DeepSeek role evidence.
- For starter-kit documentation changes, run the project-starter-kit bootstrap script with `--check`.
- If a test or check cannot run, record the exact command and blocker.
- If automated tests do not exist for the affected CLI/workflow behavior, record manual verification steps and remaining manual-verification risk.
- When the next step requires a human decision, explicitly state that it is a required decision and explain the question, why it matters, relevant options or tradeoffs, and the consequence of leaving it unresolved.
- Human decision sections must use clear Russian question text and practical examples instead of shorthand such as "approve matrix" or "confirm MVP boundary".
- When the next step requires mandatory verification, explicitly state that it is required and describe exactly what must be checked, how to check it where known, expected evidence, and residual risk if it is not performed.

## Documentation Check

Before reporting completion, ask:

- Does `docs/00_FILE_STRUCTURE.md` need an update?
- Does `docs/ROADMAP.md` need a phase status, gate, or acceptance update?
- Does `docs/CURRENT_PROJECT_AUDIT.md` need a finding added, updated, or closed?
- Does `openspec/` need a CLI-native spec or change update?
- Does `openspec/specs/documentation-governance/spec.md` still describe the documentation and TDD workflow accurately?
- Does the relevant phase plan need implementation evidence or blockers?
- Does `docs/CONTEXT.md` need a glossary term?
- Does this checklist need an update because the human introduced a new verification habit or rejected behavior?
- Did any new phase idea need an intake record, OpenSpec change, audit note, or deferred backlog entry?
- For Phase 2/3 planning, does the roadmap preserve the external-release versus corporate-adaptation boundary and avoid delivery dates or calendar deadlines?
- For target process docs, do all current choices use `minor|major|hotfix`, while every remaining `thin/full` occurrence is clearly historical, accepted-baseline, implementation-state, or migration evidence?
- Do role guides and generated views reference canonical classification/gate/policy sources instead of copying NIS thresholds or creating another normative rule set?
- Does this change duplicate requirement, scenario, acceptance, lifecycle, traceability, waiver, or artifact-contract behavior outside OpenSpec instead of linking to canonical IDs or source paths?
- If docs, specs, memory, role guides, or generated views disagree, was the canonical owner identified and the derived surface corrected?
- Do generated or role-facing summaries include source links, source metadata, or a clear pointer back to the canonical artifact?
- Does any weak-model read pack identify which files are canonical and which are supporting, generated, advisory, or evidence?

## Final Report Check

The final Russian report must use clear Markdown sections rather than one undifferentiated plain-text block. It must be detailed enough to explain important decisions, judgments, evidence, and consequences without requiring the human to open changed files.

The final Russian report must state:

- what the task was, in plain language;
- what was done;
- which decisions and judgments were made, including the reason for the chosen approach and important rejected alternatives when relevant;
- which important details, constraints, assumptions, branch state, remote-deployment status, or privacy boundaries the human should know;
- what changed in the project;
- what changed for the end user;
- what checks were performed;
- how to verify manually;
- which changes require manual verification;
- which skills were used;
- which subagents were used, including role names and token counts when available;
- ambiguous or missing documentation found;
- which new human feedback, if any, was persisted into documentation.
- if the next step requires a human decision or mandatory verification, a detailed explanation of the decision or verification task rather than a terse label.
- a Next step section or concise next-step sentence in every final report.
- when the user asked for advice or "what is better", a clear recommendation with tradeoffs, risks, and any alternatives considered.

Recommended Russian section labels should be equivalent to:

- Task
- What was done
- Decisions and judgments
- Important details
- Project changes
- End-user changes
- Checks
- Manual verification
- Risks and limitations
- Documentation
- Commit
- Skills
- Subagents
- Next step
