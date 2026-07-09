# Context

This is the active glossary and domain-boundary file for teamSddCli.

## Canonical Terms

| Term | Meaning | Notes |
|---|---|---|
| SDD | Spec-driven development workflow where requirements, design, tasks, tests, and traceability are driven from structured spec artifacts. | In this project the SDD workflow is OpenSpec/Markdown-first. |
| OpenSpec/Markdown-first | Architecture choice where structured OpenSpec and Markdown files in Git are canonical. | Confluence is generated from this source, not edited as the source. |
| `team-specs` | Central repository expected to store requirements, OpenSpec changes, living specs, QA/AT plans, traceability, registry, templates, publishing config, and schemas. | It is described by current docs and OpenSpec proposals; this repository currently contains the CLI project foundation, not the real `team-specs` repo. |
| Project repository | Repository that owns implementation truth for one product/system/component, such as code, tests, AT code, implementation-local docs, and PR evidence. | Under the proposed first topology it references canonical change/spec IDs from `team-specs` rather than copying requirement text. |
| Process package | Versioned folder of reusable SDD process assets, such as workflow schema, templates, validator entry points, role skill instructions, examples, and package metadata. | Proposed by `define-repo-topology-config`; exact path and bootstrap/update method remain gate 1.5 decisions. |
| Project adapter config | Small optional config in a project repository that points to central `team-specs`, project ID, consumed process package version, and local path mappings. | Proposed by `define-repo-topology-config`; exact filename remains gate 1.5 decision. |
| Federated specs-next-to-code topology | Future topology where central business/solution requirements stay central while per-system Master Specs and Delta Specs live near code. | Not the proposed first supported topology; requires generated views, cross-repo traceability, process-package distribution, and drift checks. |
| `sdd CLI` | Team-owned command-line process interface over OpenSpec, Git, Bitbucket, Jenkins, Jira/tracker, Confluence, and local AI tools. | It does not exist yet and is built only when a `docs/IMPLEMENTATION_STRATEGY.md` trigger fires; until then `sdd change ...` names denote thin-flow capabilities delivered by templates, scripts, and skills. It should automate workflow transitions, not replace OpenSpec CLI entirely. |
| Change package | Per-change folder under `team-specs/openspec/changes/<change-id>/` with metadata, proposal, design, tasks, spec deltas, QA artifacts, automation plan, and traceability. | Central process object. |
| Project memory | Agent-readable project orientation material that helps local AI and humans understand rules, topology, current specs, risks, and proven workflows. | It supports work, but does not replace OpenSpec as behavior truth or PR/CI as approval and validation truth. |
| Project memory triad | Planned orientation model: constitution/quality policy, project map, and OpenSpec changes/living specs. | Accepted as the future organizing idea on 2026-07-06; exact folder/schema remains future work. |
| Constitution / quality policy | Stable project rules, boundaries, quality expectations, human ownership rules, and non-negotiable process constraints. | In this repository, the current equivalent is spread across `AGENTS.md`, `docs/CONTEXT.md`, `docs/IMPLEMENTATION_STRATEGY.md`, and accepted OpenSpec specs. |
| Project map | Maintained map of repository topology, configuration, relevant modules, integrations, owners, and reusable assets. | It should be generated or validated where practical so it does not become stale narrative documentation. |
| Navigation index | Future deterministic index over docs, OpenSpec artifacts, traceability, code references, owners, and evidence links. | A Graphify-like or Pangolin-backed tool may produce it later, but it is not a source of truth. |
| Source ownership matrix | Map that declares which artifact owns each information type and which surfaces may only reference, summarize, or generate from it. | Prevents OpenSpec, docs, role guides, generated views, and project memory from carrying divergent copies of the same rule. |
| Read pack | Task-specific list of canonical and supporting files a local AI model must inspect before work. | Should state which file is canonical for each topic, especially for weaker corporate models. |
| Failure memory | Structured record of repeated mistakes, triggers, root causes, verified resolutions, and prevention checks. | It is a prevention layer, not a blame log or replacement for validators. |
| Spec-questioning gate | A planned workflow that asks targeted questions against existing docs/specs before implementation planning. | Similar in spirit to Grill With Docs; open questions must be answered or dispositioned. |
| Role guide | Short role-specific workflow guide for analyst, QA, developer, or other process participants. | It supports onboarding and must link back to canonical sources instead of duplicating behavior truth. |
| Thin change | Lightweight change path for small bugfixes, refactors, and small behavior patches. | Future requirements must define the minimum artifacts; the first MVP uses this mode. |
| Full change package | Complete change path for new features, API/mobile impact, cross-repo work, or high-risk behavior changes. | Requires broader proposal/design/QA/AT/traceability artifacts. |
| Living specs | Accepted current requirements after a change is archived. | Updated from approved changes, not manually edited in generated Confluence blocks. Team-facing name: `Master Spec` (adopted 2026-07-06). |
| Master Spec | Team-facing name for the accepted living spec of a capability stored in Git (`openspec/specs/<capability>/`). | Adopted 2026-07-06 so the company understands the concept; OpenSpec tooling still calls these specs. It is the same artifact as living specs, not a separate document. |
| Delta Spec | Team-facing name for the proposed spec delta inside a change package (`openspec/changes/<change-id>/specs/`). | Adopted 2026-07-06; OpenSpec tooling calls these change spec deltas. A Delta Spec becomes part of the Master Spec only after human-approved archive. |
| Traceability | Explicit links between requirement, scenario, dev task, QA task, test case, and automated test. | A change should not close while required links are missing without a waiver. |
| Role inbox | CLI view of relevant work for a role such as analyst, developer, QA, API AT, or mobile AT. | Local AI sessions do not monitor background state; `sdd inbox` does. |
| Context pack | Focused local bundle of relevant change/task/spec/design/test context prepared for a local AI tool. | One task or change should map to one context pack. |
| Waiver | Reviewed exception to a required artifact or verification rule with reason, evidence, and approver. | Not free text without owner/evidence. |
| Generated Confluence page | Readable publication built from OpenSpec/Markdown artifacts. | Comments are allowed; requirement edits must be moved back into Git/OpenSpec. |
| Publication model | Intermediate generated representation that turns OpenSpec/change packages/living specs into audience-oriented Markdown pages before Confluence publication. | Raw OpenSpec is not published 1:1 for business readers. |
| Master Spec views | Generated set of publication views over Master Specs (living specs), not a separate canonical source. | Renamed from "MasterSpec view set" on 2026-07-06 to avoid collision with the new `Master Spec` term; still avoids one giant manually maintained document. |
| Capability page | Generated page showing a capability summary, status, requirements, scenarios, screens, journey coverage, traceability, and open risks. | Future Confluence publication view. |
| Change page | Generated page showing what changes, why, affected systems, before/after, requirements/scenarios, approval and verification state, unresolved feedback, and evidence links. | Future Confluence publication view. |
| Customer journey page | Generated page linking journey steps to screens, requirements, scenarios, and test/evidence. | Future publication and traceability view. |
| Journey step | Stable step within a customer journey that can link to requirements, scenarios, screens, and evidence. | May start as metadata and become a stricter `journey.yaml` contract later. |
| Screen asset | Versioned UI screenshot, Figma export, or prototype image stored near specs and referenced by stable screen ID. | Not a loose Confluence attachment. |
| Screen catalog | Structured index such as `screens.yaml` linking screen assets to capability, journey, step, state, source, requirements, and scenarios. | Planned for UI-impacting full packages, not first thin MVP. |
| Legacy baseline | Gradual documentation mode for already-written behavior. | Records observed behavior, gaps, risks, and regression scenarios without retroactively requiring full historical packages. |
| Existing-code onboarding | Future onboarding flow for repositories that already have code: `scan -> baseline -> map -> validate`. | `scan` is read-only; `baseline` records observed behavior and gaps; `map` updates project memory; `validate` checks memory against code evidence. |
| Memory sync | Future deterministic maintenance check that detects drift between project map, specs, traceability, and code or repository evidence. | It should be script/CI-backed where practical, not dependent on an AI model remembering to update docs. |
| Template/spec upgrade | Future deterministic migration path for templates, specs, package versions, or OpenSpec compatibility updates. | It is blocked until the OpenSpec version pin and upgrade policy are approved. |
| Approval gate | Human-owned decision point that may be displayed in generated views but is not approved by Confluence or AI. | Bitbucket/PR review and recorded human decisions are approval truth. |
| Verification evidence | Link or recorded result proving a requirement/scenario was checked. | May be CI, test output, manual QA, PR, committed note, or approved waiver depending on contract. |
| Feedback disposition | Recorded outcome for stakeholder feedback, such as accepted, rejected, deferred, or duplicate. | Required before Confluence feedback becomes implementation input. |
| Canonical spec language | Language convention for canonical OpenSpec sources. | Decided 2026-07-06: team product analytics specs use Russian requirement/scenario prose with English structural keywords (`SHALL`, `WHEN`, `THEN`); stable IDs are always English; this project's own process specs stay English. |
| Localized generated view | Generated page translated or adapted for readers while linking back to canonical source. | Russian Confluence pages are localized views, not requirement source. |

## Boundary Rules

- Raw source artifacts such as specs, tracker exports, Confluence comments, repository metadata, and CI results must be preserved separately from derived values.
- Review-required proposals are not accepted decisions.
- The first supported topology, config format, OpenSpec version pin/upgrade policy, process package reuse, and owner/reviewer assignment are accepted in `openspec/specs/repo-topology-config/spec.md` after gate 1.5 and the 2026-07-09 archive batch.
- LLM or heuristic output is proposal evidence only unless the project explicitly defines a reviewed acceptance workflow.
- Git/OpenSpec is the canonical engineering source; Confluence is a generated view.
- Jira or another tracker is workflow/status, not the source of product requirements.
- Bitbucket PRs are review/audit surfaces; Jenkins owns deterministic validation/automation gates.
- AI may draft proposals, checks, skeletons, and context packs; humans remain responsible for approve, merge, correctness, and final decisions.
- The first CLI MVP must stay focused on the thin change flow before adding Jira task automation, QA/AT proposal generation, Confluence publication, or role inbox automation.
- Deploy automation, Zephyr or other test-management integration, Jira task automation, Confluence publication, QA/AT proposal generation, and role inboxes are not first-MVP requirements unless the human owner explicitly re-scopes the pilot.
- Mutating CLI/integration commands should support dry-run behavior, idempotency, machine-readable JSON output, and auditable action logs.
- Every accepted requirement needs at least a testable scenario; Gherkin is required only when a scenario is intended to be executable or exported to AT.
- Confluence comment handling must be modeled as an explicit feedback loop with owner, service expectation, unresolved-feedback handling, and accepted/rejected comment outcomes before publication automation is implemented.
- Avoid bidirectional synchronization between Confluence and Git unless a later accepted decision explicitly changes the architecture.
- Do not infer real corporate repository URLs, owners, credentials, Confluence spaces, Jira projects, or Jenkins jobs from examples in docs, OpenSpec proposals, or historical drafts.
- Team product analytics specs are written in Russian prose with English structural keywords and English stable IDs; this project's own process specs are written in English; generated Confluence pages remain localized views and must link back to Git/OpenSpec.
- Stable identifiers such as requirement, scenario, journey, and screen IDs are not translated.
- Manual edits to generated Confluence content are not accepted as requirement changes; accepted feedback must become a Git/OpenSpec change or PR update.
- If content describes product behavior, it belongs in OpenSpec; if it describes project organization, operations, contribution workflow, architecture rationale, or temporary phase planning, it belongs in `docs/`.
- Project memory should stay evidence-backed, concise, and routed to the right source of truth: behavior contracts in OpenSpec, operating and architecture context in `docs/`, and generated/validated maps where possible.
- Do not duplicate normative behavior text outside OpenSpec; derived docs, memory notes, role guides, and generated views should reference stable source IDs, source paths, or source metadata.
- If two artifacts disagree, resolve the conflict by source ownership first: OpenSpec wins for behavior and acceptance, `docs/CONTEXT.md` wins for terms, `AGENTS.md` wins for agent operating rules, and phase plans win for temporary phase execution rules.
- Generated views, role guides, and project memory are read models or orientation aids; they must not become parallel sources of truth.
- Weak-model read packs must identify canonical files and supporting files explicitly rather than asking the model to read every document and infer authority.
- Existing legacy behavior is documented gradually through legacy baseline notes or baseline changes; the process must not pretend unsupported legacy areas are fully specified.
