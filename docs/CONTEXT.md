# Context

This is the active glossary and domain-boundary file for teamSddCli.

## Canonical Terms

| Term | Meaning | Notes |
|---|---|---|
| SDD | Spec-driven development workflow where requirements, design, tasks, tests, and traceability are driven from structured spec artifacts. | In this project the SDD workflow is OpenSpec/Markdown-first. |
| OpenSpec/Markdown-first | Architecture choice where structured OpenSpec and Markdown files in Git are canonical. | Confluence is generated from this source, not edited as the source. |
| `team-specs` | Central repository expected to store requirements, OpenSpec changes, living specs, QA/AT plans, traceability, registry, templates, publishing config, and schemas. | It is described by current docs and OpenSpec proposals; this repository currently contains the CLI project foundation, not the real `team-specs` repo. |
| `sdd CLI` | Team-owned command-line process interface over OpenSpec, Git, Bitbucket, Jenkins, Jira/tracker, Confluence, and local AI tools. | It should automate workflow transitions, not replace OpenSpec CLI entirely. |
| Change package | Per-change folder under `team-specs/openspec/changes/<change-id>/` with metadata, proposal, design, tasks, spec deltas, QA artifacts, automation plan, and traceability. | Central process object. |
| Thin change | Lightweight change path for small bugfixes, refactors, and small behavior patches. | Future requirements must define the minimum artifacts; the first MVP uses this mode. |
| Full change package | Complete change path for new features, API/mobile impact, cross-repo work, or high-risk behavior changes. | Requires broader proposal/design/QA/AT/traceability artifacts. |
| Living specs | Accepted current requirements after a change is archived. | Updated from approved changes, not manually edited in generated Confluence blocks. |
| Traceability | Explicit links between requirement, scenario, dev task, QA task, test case, and automated test. | A change should not close while required links are missing without a waiver. |
| Role inbox | CLI view of relevant work for a role such as analyst, developer, QA, API AT, or mobile AT. | Local AI sessions do not monitor background state; `sdd inbox` does. |
| Context pack | Focused local bundle of relevant change/task/spec/design/test context prepared for a local AI tool. | One task or change should map to one context pack. |
| Waiver | Reviewed exception to a required artifact or verification rule with reason, evidence, and approver. | Not free text without owner/evidence. |
| Generated Confluence page | Readable publication built from OpenSpec/Markdown artifacts. | Comments are allowed; requirement edits must be moved back into Git/OpenSpec. |
| Publication model | Intermediate generated representation that turns OpenSpec/change packages/living specs into audience-oriented Markdown pages before Confluence publication. | Raw OpenSpec is not published 1:1 for business readers. |
| MasterSpec view set | Generated set of views over living specs, not a separate canonical source. | Avoids one giant manually maintained MasterSpec. |
| Capability page | Generated page showing a capability summary, status, requirements, scenarios, screens, journey coverage, traceability, and open risks. | Future Confluence publication view. |
| Change page | Generated page showing what changes, why, affected systems, before/after, requirements/scenarios, approval and verification state, unresolved feedback, and evidence links. | Future Confluence publication view. |
| Customer journey page | Generated page linking journey steps to screens, requirements, scenarios, and test/evidence. | Future publication and traceability view. |
| Journey step | Stable step within a customer journey that can link to requirements, scenarios, screens, and evidence. | May start as metadata and become a stricter `journey.yaml` contract later. |
| Screen asset | Versioned UI screenshot, Figma export, or prototype image stored near specs and referenced by stable screen ID. | Not a loose Confluence attachment. |
| Screen catalog | Structured index such as `screens.yaml` linking screen assets to capability, journey, step, state, source, requirements, and scenarios. | Planned for UI-impacting full packages, not first thin MVP. |
| Legacy baseline | Gradual documentation mode for already-written behavior. | Records observed behavior, gaps, risks, and regression scenarios without retroactively requiring full historical packages. |
| Approval gate | Human-owned decision point that may be displayed in generated views but is not approved by Confluence or AI. | Bitbucket/PR review and recorded human decisions are approval truth. |
| Verification evidence | Link or recorded result proving a requirement/scenario was checked. | May be CI, test output, manual QA, PR, committed note, or approved waiver depending on contract. |
| Feedback disposition | Recorded outcome for stakeholder feedback, such as accepted, rejected, deferred, or duplicate. | Required before Confluence feedback becomes implementation input. |
| Canonical spec language | Language used for canonical OpenSpec and stable IDs. | Current default: English for canonical sources. |
| Localized generated view | Generated page translated or adapted for readers while linking back to canonical source. | Russian Confluence pages are localized views, not requirement source. |

## Boundary Rules

- Raw source artifacts such as specs, tracker exports, Confluence comments, repository metadata, and CI results must be preserved separately from derived values.
- Review-required proposals are not accepted decisions.
- LLM or heuristic output is proposal evidence only unless the project explicitly defines a reviewed acceptance workflow.
- Git/OpenSpec is the canonical engineering source; Confluence is a generated view.
- Jira or another tracker is workflow/status, not the source of product requirements.
- Bitbucket PRs are review/audit surfaces; Jenkins owns deterministic validation/automation gates.
- AI may draft proposals, checks, skeletons, and context packs; humans remain responsible for approve, merge, correctness, and final decisions.
- The first CLI MVP must stay focused on the thin change flow before adding Jira task automation, QA/AT proposal generation, Confluence publication, or role inbox automation.
- Mutating CLI/integration commands should support dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- Every accepted requirement needs at least a testable scenario; Gherkin is required only when a scenario is intended to be executable or exported to AT.
- Confluence comment handling must be modeled as an explicit feedback loop with owner, service expectation, unresolved-feedback handling, and accepted/rejected comment outcomes before publication automation is implemented.
- Avoid bidirectional synchronization between Confluence and Git unless a later accepted decision explicitly changes the architecture.
- Do not infer real corporate repository URLs, owners, credentials, Confluence spaces, Jira projects, or Jenkins jobs from examples in docs, OpenSpec proposals, or historical drafts.
- Canonical OpenSpec sources and stable IDs should be written in English; generated Confluence pages may be localized for the team and must link back to Git/OpenSpec.
- Stable identifiers such as requirement, scenario, journey, and screen IDs are not translated.
- Manual edits to generated Confluence content are not accepted as requirement changes; accepted feedback must become a Git/OpenSpec change or PR update.
- If content describes product behavior, it belongs in OpenSpec; if it describes project organization, operations, contribution workflow, architecture rationale, or temporary phase planning, it belongs in `docs/`.
- Existing legacy behavior is documented gradually through legacy baseline notes or baseline changes; the process must not pretend unsupported legacy areas are fully specified.
