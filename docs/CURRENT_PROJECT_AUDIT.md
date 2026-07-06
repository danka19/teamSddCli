# Current Project Audit

Status: active.

Last updated: 2026-07-06.

## Repository Baseline

| Item | Current State |
|---|---|
| Repository root | `C:\Users\danoc\Documents\projects\teamSsdCli` |
| Git repository | Initialized locally on 2026-07-03 |
| Current branch | `phase-1/change-template-validation` |
| Remote | `origin` -> `https://github.com/danka19/teamSddCli.git` |
| Latest known commit before this audit update | `cde51ef` (`Consolidate workflow: global skills, thin CLAUDE.md, session-report rule`) |
| GitHub repository rename | Repository was renamed from `danka19/teamSsdCli` to `danka19/teamSddCli`; local folder path still uses `teamSsdCli` |
| Architecture source of truth | Current decisions live in `docs/` and `openspec/`; stale historical architecture draft removed on 2026-07-06 |
| Implementation source code | No custom `sdd` CLI source exists; deterministic script `scripts/validate_change.py` is present |
| OpenSpec project artifacts | Present; 7 active proposed changes cover the deterministic artifact gate plus Phase 1 lifecycle, artifact, traceability, waiver, documentation-governance, and Confluence feedback/publication contracts |

## Useful Starting Points

- Documentation starts in `docs/`.
- Roadmap exists at `docs/ROADMAP.md`.
- Agent work rules are recorded in `AGENTS.md`.
- Project memory and weak-model planning input is recorded in `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md`.
- Workflow skills are global (`~/.codex/skills`); this repository intentionally has no `.codex/skills/` directory.
- Current architecture and implementation planning are in `docs/`, `openspec/`, and accepted human decisions.

## Verified Environment Evidence

| Check | Evidence |
|---|---|
| Git installed | `git version 2.54.0.windows.1` |
| Repository initialized | Yes; `git init -b main` completed |
| Git remote configured | `origin https://github.com/danka19/teamSddCli.git` |
| First push | `git push -u origin main` published `main` to `danka19/teamSddCli` |
| Runtime installed | Python 3.13.14 is available for deterministic validation scripts and tests |
| Tests available | Focused validator tests are present under `tests/`; no custom `sdd` CLI test suite exists yet |
| Focused validator tests | `python -m pytest tests/test_validate_change.py -v` passed 5 tests; `pytest.ini` uses repository-local `.pytest-tmp` because the default Windows temp pytest directory is not accessible in this environment |
| Template validation | `python scripts/validate_change.py --allow-placeholders templates/change` passed; `python scripts/validate_change.py templates/change` rejected placeholder values as expected |
| OpenSpec CLI installed | `openspec --version` returned `1.4.1` |
| OpenSpec validation | `openspec list` showed 7 active changes; `openspec list --specs` showed no accepted specs yet; `openspec validate --all --strict` passed 7 items and failed 0 |
| Pre-commit installed | Not available on PATH during Phase 1 artifact work; config is present but end-to-end hook execution still needs tool installation |
| Local app/server available | No local app/server found; this work item is script/template based |
| Documentation bootstrap | `project-starter-kit` created `AGENTS.md`, `docs/`, `.codex/skills/`, `.gitignore`, and `.env.example` |
| Starter structure check | `python C:/Users/danoc/.codex/skills/project-starter-kit/scripts/bootstrap_project.py --target C:/Users/danoc/Documents/projects/teamSsdCli --check` passed |
| Markdown/code whitespace check | `rg -n "[ \t]+$" AGENTS.md docs openspec templates scripts tests .pre-commit-config.yaml pytest.ini .gitignore` returned no matches |

## Known Risks And Gaps

| ID | Risk | Owner | Status |
|---|---|---|---|
| AUDIT-001 | Product scope is described at architecture level, and the 2026-07-03 accepted critique narrowed the first MVP, but accepted CLI requirements and acceptance criteria are only beginning to be captured as OpenSpec changes; no accepted living specs exist yet. | Phase 1 | open |
| AUDIT-002 | Environment and verification commands for the future CLI runtime are not recorded because the implementation stack is undecided. | Phase 1/2 | open |
| AUDIT-003 | Historical architecture draft was removed after current decisions were captured in `docs/` and active OpenSpec proposals; accepted living specs are still pending Phase 1 archive/acceptance. | Phase 1/2 | closed |
| AUDIT-004 | This folder was initialized as a git repository, connected to `danka19/teamSddCli`, committed, and pushed to `origin/main`. | Human/Phase 0 | closed |
| AUDIT-005 | OpenSpec folder structure for this CLI project's own requirements is initialized with active change `add-change-template-validation`. | Phase 1 | closed |
| AUDIT-006 | Placeholder corporate repo/owner/Jira/Confluence/Jenkins examples from the removed historical draft must not be treated as real configuration. Current docs still forbid inferring real corporate configuration from examples. | Phase 1/2 | closed |
| AUDIT-007 | Corporate environment specifics are unverified: GigaCode CLI capability against skill flows, MCP policy inside the corporate network, Bitbucket/Jenkins/Jira/Confluence versions, and network/artifact restrictions. Must be checked in the pre-transfer adaptation review. | Transfer phase | open |
| AUDIT-008 | Automated local MCP server provisioning for employees is an untested experiment; manual setup remains the documented fallback until proven. | Later phase | open |
| AUDIT-009 | `pre-commit` is not installed on the current machine, so the hook config cannot yet be executed end-to-end locally. | Phase 1/local environment | open |
| AUDIT-010 | The generated Confluence publication model is planned, but feedback-loop ownership, SLA, unresolved-comment behavior, localization, and source-warning contracts are not accepted yet; publication automation must remain blocked until those contracts are approved. | Phase 1/4 | open |
| AUDIT-011 | Journey and screen artifacts are now planned future contracts, but `journey.yaml`, `screens.yaml`, screen asset storage, and generated gallery views are not implemented or validated. | Phase 1/4 | open |
| AUDIT-012 | Legacy baseline mode is planned for already-written code, but no accepted workflow or template exists yet for baseline changes, observed behavior, known gaps, or legacy coverage risk reporting. | Phase 1/4 | open |
| AUDIT-013 | Canonical OpenSpec language is now English by default and generated Confluence may be localized to Russian, but no bilingual glossary or translation review process exists yet. | Phase 1/4 | open |
| AUDIT-014 | Project memory, documentation quality controls, weak-model guardrails, repeated-error memory, spec-questioning workflow, and analyst/QA onboarding are captured as planning input, but not yet specified as accepted OpenSpec contracts or deterministic checks. | Phase 1/4 | open |
| AUDIT-015 | Source ownership and write-once/reference-many documentation rules are captured as proposed governance, but deterministic linting for duplicate normative text, source links, generated blocks, stale memory, and orphan docs is not implemented yet. | Phase 1/4 | open |

## Accepted Human Decisions

| Date | Decision | Impact |
|---|---|---|
| 2026-07-03 | Narrow the first MVP to `sdd change new`, `sdd change validate`, `sdd change pr`, `sdd change archive`, and basic `traceability.yaml`. | Phase 1/3 plans must not require Jira, QA/AT, Confluence publication, or role inboxes for the first usable workflow unless explicitly re-scoped. |
| 2026-07-03 | Use two future change modes: `thin change` and `full change package`. | Phase 1 must define artifact requirements and validation behavior for both modes. |
| 2026-07-03 | Formalize product OpenSpec specs first for change lifecycle, artifact contracts, traceability, and waiver behavior. | Phase 1 OpenSpec work should prioritize these specs before broad integration specs. |
| 2026-07-03 | Specify the Confluence feedback loop before implementing publication automation. | Future Confluence work must define owner, service expectation, unresolved-feedback handling, and accepted/rejected comment outcomes. |
| 2026-07-03 | Design mutating CLI/integration commands with dry-run, idempotency, JSON output, and audit logs. | Phase 2 architecture and later tests must cover these command contracts. |
| 2026-07-03 | Do not require Gherkin for every QA artifact; require at least a testable scenario, with Gherkin only for executable/exported scenarios. | Phase 1/QA artifact contracts must avoid unnecessary Gherkin bureaucracy. |
| 2026-07-03 | Deliver the SDD process without a custom `sdd` CLI first (deterministic scripts/templates in `team-specs` + standard tool features + AI role skills); build CLI parts only on the triggers in `docs/IMPLEMENTATION_STRATEGY.md`. | Phase plans must target templates, validation scripts, skills, and pipelines instead of CLI source code until a trigger fires. |
| 2026-07-03 | OpenSpec = Fission-AI/OpenSpec with team reference docs at <https://lzw.me/docs/openspec>; pin the CLI version. | Phase 1 must record the pinned version; upstream docs win over the mirror on discrepancy. |
| 2026-07-03 | Jira/Confluence access from AI tooling via MCP only (verified working by the human owner); no custom REST clients; automating local MCP server provisioning is a planned experiment. | Integration specs must define MCP usage boundaries, not API client contracts. |
| 2026-07-03 | Develop in the external environment (Claude Code) first, then transfer to the corporate environment where only GigaCode CLI is available. | Gates must never depend on the AI layer; skills stay tool-agnostic; an environment adaptation review is required before transfer. |
| 2026-07-03 | The first Phase 1 artifact is `templates/change/` + `scripts/validate_change.py` + `.pre-commit-config.yaml`, on branch `phase-1/change-template-validation`, tracked by OpenSpec change `add-change-template-validation`. | Phase 1 starts with deterministic templates and validation before broader specs, integrations, or custom CLI work. |
| 2026-07-06 | Approve the Phase 1 risk-oriented thin/full artifact matrix default. | Thin behavior-changing SDD changes require intent, OpenSpec delta, scenarios, basic traceability, and verification evidence; full packages are required for new features, public API, mobile, cross-repo, data/security, high-risk, or broad behavior changes. |
| 2026-07-06 | Approve role-appropriate waiver approvers and minimum evidence. | Waivers require the responsible role owner, affected requirement/scenario, reason, substitute evidence, and follow-up/expiry when residual risk remains. |
| 2026-07-06 | Reconfirm Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP, with the rest planned as later layers. | Phase 1/3 must not implement those integrations in the thin MVP; Phase 1 may define proposals and future contracts for them. |
| 2026-07-06 | Treat Confluence as generated publication/read model with audience-oriented pages, source metadata, warnings, and links back to Git/OpenSpec; do not create a separate canonical MasterSpec. | Confluence publication proposals must generate views from living specs/change packages and route accepted feedback back through Git/OpenSpec. |
| 2026-07-06 | Use English for canonical OpenSpec sources and stable IDs by default; generated Confluence views may be localized in Russian. | Documentation governance must preserve stable IDs, route Russian feedback back into English source changes, and plan a bilingual glossary. |
| 2026-07-06 | Plan legacy baseline mode for already-written code. | Old behavior is documented gradually; full retroactive change packages are not required for historical changes, but touched legacy behavior needs observed/current behavior, proposed change, regression scenario, known gaps, and UI screenshots when affected. |
| 2026-07-06 | Remove stale historical architecture draft from the repository. | Current architecture truth is `docs/`, `openspec/`, and accepted human decisions; agents must not use a parallel architecture file as a source of truth. |
| 2026-07-06 | Adopt the project memory triad as the future orientation model: constitution/quality policy, project map, and OpenSpec changes/living specs. | Phase 1/2 should plan memory boundaries and validation so project memory helps agents and humans orient without becoming a second behavior source of truth. |
| 2026-07-06 | Formalize existing-code onboarding as `scan -> baseline -> map -> validate`. | Future legacy onboarding should keep scan read-only, record observed behavior/gaps/risks, update project memory, and validate memory against real code evidence. |
| 2026-07-06 | Plan `sync` and `upgrade` as deterministic maintenance, not AI-only skills. | Sync should detect drift across project map, specs, traceability, and code evidence; upgrade should migrate templates/spec-package versions only after the OpenSpec version policy is approved. |
| 2026-07-06 | Use a PDLC narrative when presenting the process to the team. | The process should be explained as shared context from analysis through tasks, tests, verification, and publication, not merely faster code generation. |
| 2026-07-06 | Keep deploy, Zephyr/test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes outside the first MVP. | Phase 1/3 must not make those integrations first-MVP blockers unless the human owner explicitly re-scopes the pilot. |
| 2026-07-06 | Record Graphify-like navigation, documentation boundary, weak-model support, repeated-error memory, spec-questioning, and QA/analyst usability as mandatory planning input. | Future project-memory or weak-model proposals must start from `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` before choosing schemas, tools, skills, or implementation scope. |
| 2026-07-06 | Use source ownership and write-once/reference-many rules to prevent OpenSpec/docs/memory drift. | OpenSpec owns behavior and acceptance; `docs/` owns context, rationale, phase planning, and audit; `AGENTS.md` owns agent operating rules; derived views, role guides, read packs, and project memory must reference canonical sources and be fixed or regenerated when they drift. |

## Audit Rules

- Update this file when a finding is fixed, invalidated by evidence, or moved.
- Do not mark a finding closed without verification evidence.
