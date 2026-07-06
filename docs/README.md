# teamSddCli

## Summary

teamSddCli is a local SDD automation project for a team workflow based on OpenSpec/Markdown, Git, Bitbucket, Jenkins, Confluence, Jira or another task tracker, local CLI commands, and local AI tools.

The project goal is to automate the end-to-end transition from analysis to development tasks, QA test cases, automated-test skeletons, verification, and archived living specs without introducing one centralized autonomous agent.

Current checkpoint:

> Project foundation has moved into Phase 1. The first deterministic process artifact exists: a copyable change package template, a local validation script, pre-commit configuration, and a project OpenSpec change. Current Phase 1 work is synchronizing proposed OpenSpec contracts and human decisions before expanding templates or validators. No custom `sdd` CLI exists yet.

## Scope

In scope:

- OpenSpec/Markdown-first workflow where Git/OpenSpec is the canonical engineering source.
- `sdd CLI` process commands for change creation, validation, PR support, publication, task planning, QA/AT proposals, role inboxes, AI context packs, and archiving.
- Integration boundaries for Bitbucket, Jenkins, Confluence, Jira or an equivalent tracker, code repositories, QA repositories, and AT repositories.
- Change packages with proposal, design, tasks, spec deltas, QA plans, test cases, automation plans, and traceability.
- Local AI support for drafts, reviews, context packs, and test or automation skeletons.
- Phase-based delivery of a minimal pilot, task automation, QA/AT automation, and process hardening.

Out of scope:

- Treating Confluence as the editable source of truth for requirements.
- Bidirectional Git/Confluence synchronization.
- Letting AI approve, merge, own process state, or replace human accountability.
- Building a centralized background autonomous agent as the first architecture.
- Assuming concrete corporate credentials, project owners, repository URLs, or production deployment details before they are verified.

## Key Decisions

- 2026-07-03: Use the historical architecture draft as the initial bootstrap input.
- 2026-07-03: Use OpenSpec/Markdown in Git as the canonical source and Confluence as a generated publication layer.
- 2026-07-03: Automate artifact state transitions through CLI/CI rather than centralizing control in one autonomous agent.
- 2026-07-03: Keep human ownership over approvals, merges, business decisions, correctness, and review outcomes.
- 2026-07-03: Use this starter-kit documentation set as the durable operating system for future Codex work.
- 2026-07-03: Narrow the first implemented MVP to a thin change flow: `sdd change new`, `sdd change validate`, `sdd change pr`, `sdd change archive`, and basic `traceability.yaml`; Jira task automation, QA/AT proposal commands, Confluence publication, and role inboxes are later layers unless explicitly re-scoped.
- 2026-07-03: Support two change modes in future requirements: a lightweight `thin change` path for small bugfix/refactor/small behavior patches and a `full change package` path for feature, API, mobile, cross-repo, or high-risk changes.
- 2026-07-03: The first product OpenSpec specs should focus on change lifecycle, artifact contracts, traceability, and waiver behavior before broad CLI/integration coverage.
- 2026-07-03: Confluence feedback handling must be explicitly specified before implementation: owner, service expectation, unresolved-feedback handling, and how comments become accepted deltas or rejected notes.
- 2026-07-03: Future mutating CLI/integration commands should be designed with dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- 2026-07-03: Gherkin is not mandatory for every QA artifact; every requirement needs at least a testable scenario, while Gherkin should be required only when a scenario is executable or exported to AT.
- 2026-07-03: Deliver the SDD process without a custom `sdd` CLI first: deterministic base (templates + validation scripts + pre-commit + Jenkins in `team-specs`) + standard tool features (Bitbucket default reviewers, Jira Automation, markdown->Confluence publisher, OpenSpec CLI) + AI role skills as a convenience layer. A custom CLI is built only when the trigger criteria in `docs/IMPLEMENTATION_STRATEGY.md` fire.
- 2026-07-03: OpenSpec means Fission-AI/OpenSpec; the team reference documentation is <https://lzw.me/docs/openspec> (community multilingual mirror; upstream docs win on discrepancy); the CLI version is pinned.
- 2026-07-03: Jira and Confluence access from AI tooling goes through MCP servers, not hand-written REST integrations; MCP was tested by the human owner and works. Automating local MCP server provisioning for employees is a planned experiment.
- 2026-07-03: Development happens in an external environment (Claude Code available) and is later transferred to the internal corporate environment where only GigaCode CLI is available; all process guarantees must live in the deterministic layer, skills must be tool-agnostic markdown, and an environment adaptation review is required before transfer.
- 2026-07-03: Start Phase 1 with the deterministic base artifact `templates/change/` + `scripts/validate_change.py` + `.pre-commit-config.yaml`, tracked as project OpenSpec change `add-change-template-validation`.
- 2026-07-06: Approve the risk-oriented thin/full artifact matrix as the Phase 1 default: thin behavior-changing SDD changes need intent, OpenSpec delta, scenario, traceability, and verification evidence; full packages are required for new feature, public API, mobile, cross-repo, data/security, high-risk, or broad behavior changes.
- 2026-07-06: Approve role-appropriate waiver ownership: QA owners approve test evidence gaps, AT owners approve automation gaps, tech leads approve design/risk exceptions, and analyst/product owners approve scope or documentation exceptions, with reason, affected requirement/scenario, approver, substitute evidence, and follow-up/expiry when risk remains.
- 2026-07-06: Reconfirm the first MVP boundary: Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes remain outside the first MVP and are planned as later layers.
- 2026-07-06: Treat Confluence publication as generated audience views, not raw OpenSpec 1:1 and not a separate MasterSpec source; generated pages must carry source commit, change/PR ID, timestamp, source warning, and links back to canonical Git/OpenSpec files.
- 2026-07-06: Use English for canonical OpenSpec sources and stable IDs by default; generated Confluence views may be localized in Russian and must route accepted feedback back into English Git/OpenSpec sources.
- 2026-07-06: Add a future legacy baseline mode for already-written code so the team records observed behavior, gaps, risks, and regression scenarios gradually instead of retroactively creating full historical change packages.
- 2026-07-06: Remove the stale historical architecture draft from the repository; current architecture decisions and product contracts live in `docs/`, `openspec/`, and accepted human decisions.
- 2026-07-06: Plan a project memory triad for agent and team orientation: constitution/quality policy for rules and boundaries, project map for topology/config/repository map, and OpenSpec changes/living specs for behavior contracts.
- 2026-07-06: Formalize existing-code onboarding as a future `scan -> baseline -> map -> validate` flow: scan is read-only, baseline records observed behavior/gaps/risks, map updates project memory, and validate checks memory against real code.
- 2026-07-06: Plan `sync` and `upgrade` as deterministic maintenance, not agent magic: `sync` checks drift across project map, specs, traceability, and code evidence; `upgrade` migrates templates/spec-package versions only after the OpenSpec version policy is approved.
- 2026-07-06: Use a PDLC narrative when explaining the process to the team: the goal is shared context from analysis through tasks, tests, verification, and publication, not merely faster code generation.
- 2026-07-06: Keep deploy, Zephyr/test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP unless the human owner explicitly re-scopes the pilot.
- 2026-07-06: Use source ownership and write-once/reference-many documentation rules: OpenSpec owns behavior and acceptance, while docs, memory, role guides, and generated views reference canonical source IDs or metadata instead of carrying divergent copies.

## Architecture Sources

The historical architecture draft was removed on 2026-07-06 after its useful decisions had been captured in durable project documentation and Phase 1 OpenSpec proposals.

A recorded critique of that now-removed draft, with evaluation criteria, external comparison, recommendations (REC-001..REC-007), and alternative lightweight solution paths, lives in `docs/audits/ARCHITECTURE_CRITIQUE_2026-07-03.md`. Its recommendations are historical planning inputs; only items already listed under Key Decisions or accepted OpenSpec specs/changes are accepted.

Current architecture sources:

- `docs/README.md` for product summary, scope, key decisions, and first valuable outcome.
- `docs/CONTEXT.md` for canonical terms and boundary rules.
- `docs/IMPLEMENTATION_STRATEGY.md` for the accepted no-custom-CLI-upfront delivery strategy.
- `docs/ROADMAP.md` and `docs/phases/` for phase scope, gates, and current work.
- `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` for the queued planning input on project memory, Graphify-like navigation, weak-model guardrails, repeated-error memory, spec-questioning, and analyst/QA usability.
- `openspec/changes/` and later `openspec/specs/` for proposed and accepted SDD workflow, artifact, traceability, waiver, documentation, and publication contracts.

Important concepts preserved in current docs:

- Canonical source: `team-specs` repository with `openspec/` artifacts.
- Publication: generated Confluence pages from Markdown/OpenSpec.
- Review and audit: Bitbucket PRs with reviewer assignment from owners registry.
- Validation and automation: Jenkins pipelines.
- Workflow status: Jira or another task tracker.
- Local process interface: `sdd CLI`.
- Traceability path: requirement -> scenario -> dev task -> test case -> automated test.
- Project memory triad: constitution/quality policy, project map, and OpenSpec changes/living specs.
- Existing-code onboarding path: read-only scan -> legacy baseline -> project map update -> validation against real code.
- Maintenance path: deterministic sync and upgrade checks after the related topology/config and OpenSpec version policies are approved.
- Historical broad pilot picture: `team-specs`, OpenSpec CLI, core `sdd` commands, Jenkins Spec PR pipeline, Bitbucket reviewer assignment, Confluence preview, Jira task creation, and `traceability.yaml`.

The accepted MVP is narrower than the historical broad pilot picture. Per the accepted 2026-07-03/2026-07-06 decisions, the first MVP proves the thin change flow and basic traceability before Jira task automation, Confluence publication, QA/AT proposal generation, or role inboxes become implementation scope.

## First Valuable Outcome

The first useful delivery should prove the smallest thin SDD change flow at pilot scale:

1. Create a change package from templates.
2. Validate structure, policy, and basic traceability locally.
3. Create a Spec PR.
4. Archive the completed change into living specs.
5. Preserve enough traceability to show requirement -> scenario -> change evidence.

Confluence publication, Jira task creation, QA/AT proposal generation, and role inboxes remain important, but they are not required for the first MVP unless the human owner explicitly re-scopes the pilot.

Future publication layers should generate audience-oriented views from canonical OpenSpec sources, including change pages, capability pages, customer journey pages, release/change summaries, technical appendices, and screen galleries where useful. Those generated views must preserve traceability back to requirements, scenarios, source commits, and verification evidence.

## Documentation Rules

- `AGENTS.md` is the canonical agent operating guide.
- `docs/00_FILE_STRUCTURE.md` is the repository map and must be updated when files or folders are added.
- `docs/CURRENT_PROJECT_AUDIT.md` is an active planning input and must be updated when findings are fixed or invalidated by evidence.
- Detailed phase plans live under `docs/phases/` and must use `docs/phases/PHASE_PLAN_TEMPLATE.md`.
- New human feedback that affects `sdd CLI` behavior, safety, command usability, SDD workflow, acceptance, or verification must be persisted in the correct durable document.
- Behavior and acceptance text should not be duplicated across specs, docs, project memory, generated views, or role guides; derived surfaces link to the canonical owner and are fixed or regenerated when they drift.
