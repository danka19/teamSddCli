# Internal OpenSpec Customization ("de-workflow"): Structure Analysis And Recommendations

Status: planning input for Phase 1 work item 1.4 (`define-repo-topology-config`) and gate 1.5. Prepared 2026-07-09 from the full screenshot review. Not an accepted contract.

Source: 25 photos in the git-ignored local folder `arch-screenshots/openspec-de/`, reviewed in full. They show a personal corporate Bitbucket repository with a developer-oriented OpenSpec customization (workflow schema, templates, process flow diagram) plus a corporate Confluence knowledge-base page describing repository topology options. The photos contain corporate URLs, internal system names, and an employee name; this document deliberately abstracts all corporate identifiers. Readability: all key content was legible; the only material not captured is the tail of the workflow schema past the tasks/apply section, the unexpanded "practical repository examples" link, and the "frame selection" section that starts after the topology options on the Confluence page.

## 1. What The Internal Solution Is

A developer-workflow customization of OpenSpec, shown in an engineer/user-scoped repository (develop branch), consisting of:

1. **A declarative workflow schema** (`openspec/schemas/de-workflow/schema.yaml`, ~30 KB, `version: 1`): defines the artifact chain `proposal -> specs -> design -> tasks` as data. Per artifact: `id`, `generates` (file pattern), `template`, `requires` (dependency list), and a long Russian `instruction` prompt. A separate `apply:` section declares `requires: tasks` and `tracks: tasks.md`.
2. **Templates** next to the schema: `proposal.md` (fixed Russian sections: Почему / Что меняется / Границы (в scope, вне scope) / Сценарии / Критерии приёмки / Влияние), `spec.md` (delta operations), `tasks.md` (checkbox groups), `spec-structure.md` (master-spec folder contract), `spec-guide.md` (authoring rules).
3. **Skills** wrapping the schema: explore (free research, no artifacts), propose (fast path: change dir + proposal + specs in one step), new-change (dir only) + continue-change (one artifact per call), apply-change (executes tasks.md checkboxes), verify-change (AI check: completeness/correctness/consistency; outputs CRITICAL/WARNING/SUGGESTION; does not block archive), archive-change (syncs delta into master spec, moves package to `openspec/changes/archive/YYYY-MM-DD-<name>`, dedicated commit `spec: archive <name>`).
4. **A process flow diagram** (PNG committed to the repo): feature branch from develop; optional PR review after proposal+specs and after design+tasks ("no review — continue in the current branch"); apply; verify; archive; final PR into develop with explicit rollback paths (revert archive commit, return to the proposal or design stage depending on what must change).
5. **A master-spec structure** (`openspec/specs/`) organized by technical domains: `data-models/`, `non-functional-requirements/` (admin roles, error lists/handling, status models, CMS docs), `functional-requirements/api/wf/<workflow>/states/<n>-<state>/actions/` and `api/rest/<service>/`, `async/`, `integrations/external|platform/<service>/`. Contract-first artifacts live next to prose: OpenAPI `contract.yaml`, JSON request/response schemas, example JSONs. A margin note questions whether keeping all CSV/docs in one repo is right — asset placement is an open question for them too.
6. **A Confluence knowledge-base page** (hand-written process doc, ~1.5k views) with three repository topology options by team maturity:
   - **Variant 1 (small team, single-capability pilot):** everything in one repo — agent entry file, AI tooling (skills/MCP/agents/hooks), docs, code, tests.
   - **Variant 2 (team pilot):** three repos — requirements repo (docs + AI tooling), code repo, tests/autotests repo; praised for not mixing code and autotest projects; a step toward multi-repo.
   - **Variant 3 (proven effect, scaling; currently in pilots):** a central requirements repo (business requirements + solution architecture, e2e scenarios) plus per-system repos (web app, front platform, process platform) each carrying its own master spec (current description) + increments (delta specs) next to code.

### Workflow behaviors worth noting

- Every artifact instruction starts with a mandatory context-study step ("do not skip silently"; explicit handling for an empty master spec: record "no existing requirements", all operations become [ADDED]).
- After writing each artifact the agent must spawn a **self-review subagent** with a concrete per-artifact quality checklist (completeness, unambiguity, verifiability, consistency, altitude, scope hygiene); the subagent returns "approved" or a problem list; then **STOP** — show the result to the user and wait for explicit confirmation before the next artifact.
- **Document altitude** is enforced by instruction: proposal is business-only (class names, DB fields, API contracts, patterns are forbidden — they belong to design); specs are business scenarios with mandatory error codes in alternative scenarios; design binds requirements to exact code (`path::method(signature)`, "requirement -> code" table per delta operation); tasks are actions + references to design lines (`design.md:34`), never duplicated implementation detail, with anti-example pairs ("Bad: implement enrichment logic / Good: add field X to file Y (design.md:34)").
- Design phase uses a **scout subagent** for codebase recon (main agent must not grep the whole project); explicit empty-project behavior.
- Delta operations vocabulary: **[ADDED] / [MODIFIED] / [REMOVED] / [RENAMED]**, where REMOVED requires reason + migration and RENAMED with content change must be expressed as REMOVED + ADDED. The change unit is a master-spec file; [MODIFIED] must make before/after unambiguous; delta must be stylistically indistinguishable from the master spec it patches.
- tasks.md has a strict machine-parsed checkbox contract (`- [ ]`), group structure: implementation steps -> unit tests -> verify command (build/test) -> one commit per group.
- Small tasks may keep the whole delta in a single `specs/change.md`; large changes mirror the master-spec hierarchy.

## 2. Assessment Against The Work-Item 1.4 Criteria

Criteria from `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md`:

| # | Criterion | Internal solution | Our position |
|---|---|---|---|
| 1 | AI-independence of guarantees | The screenshots show prompts + human PR review + AI verify; deterministic gates are not visible in the captured material; only tasks checkbox parsing is explicitly machine-shaped | Keep deterministic validators/CI as the guarantee layer; borrow their prompt discipline as AI-layer content only |
| 2 | Single source of truth | Aligned: Git master spec + dated archive; Confluence used only for process docs | Same philosophy; no conflict |
| 3 | Topology / content split | Staged variants 1→2→3; variant 3 = central business-requirements repo + specs next to code per system | Our central `team-specs` matches their variant 2; variant 3 is a plausible later stage, not the first supported topology |
| 4 | Authoring ergonomics | Excellent weak-model prompt engineering; but master-spec tree is deep, developer-shaped (OpenAPI/JSON/DTO), loose file-naming in action folders | Borrow instruction patterns; keep our strict ID grammar and typed YAML records |
| 5 | Deterministic validatability | Not confirmed from screenshots; no validator/CI contract is visible in the captured material | Keep ours; encode their `requires:` dependencies as validator rules |
| 6 | Readability without tooling | Good: all Markdown in Bitbucket, Russian prose, committed flow PNG, short fixed templates | Confirms our Russian-canon and template decisions |
| 7 | Reusability by other teams | Workflow definition is one self-contained folder (schema + templates) - copyable; but team-owned distribution, version/upgrade policy, and bootstrap guide are not confirmed by the screenshots | Borrow "process as one versioned folder"; ours must be team-owned with pin/upgrade |
| 8 | Ownership/review contract | Only optional PRs into develop; no owners registry/CODEOWNERS/role approvals | Keep our `owners.yaml` -> generated CODEOWNERS contract |
| 9 | Traceability | Line-number refs (`design.md:34`) + AI verify; no stable IDs, no requirement→test links | Keep stable REQ-/SCEN- ID grammar; line refs acceptable only inside a package as convenience |
| 10 | Corporate approval compatibility | Not addressed: no generated approval views, no unified-document rendering | Our generated-Confluence layer remains necessary for analyst approval |
| 11 | Thin-MVP compatibility | Good: single-file `change.md` thin path, optional reviews | Aligned with our thin/full matrix |
| 12 | Migration path | Explicit empty-baseline handling everywhere; mirrors our on-touch approach | Aligned |
| 13 | Version pin/upgrade | `version: 1` field only; no upgrade policy | Our merged proposal still must define pin/upgrade; schema version field is a candidate pin location |
| 14 | Drift/maintenance | AI verify (non-blocking) + archive sync + PR discipline; CRITICAL findings cannot block archive | Insufficient for us; error-level enforcement stays (2026-07-06 decision) |

## 3. Strengths To Borrow

1. **Workflow-as-data.** One schema file declares artifacts, dependencies, templates, and per-artifact instructions; skills are generic executors. This matches our no-custom-CLI strategy and gives the topology proposal a concrete shape for "shared scripts/templates/skills distributed once": the process definition is a single versioned folder another team can copy.
2. **Weak-model instruction patterns**: mandatory context-study steps with "do not skip silently"; explicit empty-baseline branches; STOP-and-confirm gates between artifacts; per-artifact self-review subagent checklists; scout subagent for code recon; Bad/Good example pairs. Route into role skills and the weak-model guardrails plan.
3. **Document altitude rules** per artifact (business vs design separation with concrete forbidden-content lists) — route into artifact-contract templates/instructions.
4. **Delta operation vocabulary** incl. [RENAMED] and the REMOVED-requires-reason+migration rule — check against our Delta Spec contract and OpenSpec defaults for gaps.
5. **Archive conventions**: dated archive folders and a fixed commit-message grammar (`spec: archive <name>`) — greppable deterministic history; align with our lifecycle proposal.
6. **Maturity-staged topology narrative** (variant 1 → 2 → 3). Presenting our topology options in this staging language will ease corporate adoption because the internal knowledge base already teaches these stages. Our recommended default (central `team-specs` including analytics) is essentially their variant 2; their variant 3 (per-system master specs next to code under a central business-requirements repo) becomes our documented later stage, contingent on per-system generated views and cross-repo traceability.
7. **tasks.md deterministic checkbox contract** with implement → unit-test → verify-command → commit group structure.
8. **Committed process flow diagram** and short fixed-section Russian templates (proposal capped at 1-2 pages).

## 4. What We Deliberately Do Differently

1. **Guarantees stay deterministic.** Their prompts+review model violates our core constraint (process guarantees must survive an AI-free or weak-model environment). Validators enforce artifact matrix/waivers as errors; AI self-review is an additional layer, not the gate.
2. **First supported topology stays central `team-specs`** (analytics + Master/Delta Specs + QA/AT + templates + validators). Their audience is developers writing engineering specs for one system; ours is analysts authoring solution-level requirements matching the corporate approval unit that spans systems. Their own variant 2 (requirements repo separate from code) supports this choice; variant 3 is recorded as a later scaling option, not the pilot default.
3. **Stable ID grammar over line-number references.** `design.md:34` breaks silently on edit; REQ-/SCEN- IDs survive and can anchor tests, traceability, and generated views. Line refs remain allowed inside a change package as a convenience.
4. **Typed YAML records for tabular content** (status models, channel matrices, platform services) stay: their status models are prose Markdown because they never need to render corporate nested-table approval views; we do.
5. **Strict naming/ID grammar everywhere**: their action folders explicitly have no naming requirements, which blocks linting; we keep one grammar validators can check.
6. **Team-owned distribution with version pin/upgrade policy**: the screenshots show `version: 1`, but not a team-owned release, upgrade, compatibility, or rollback policy. The merged 1.4 proposal must define pin location, upgrade trigger, compatibility evidence, and rollback.
7. **QA/AT and approval-view layers remain in scope** (later phases): absent in their solution, mandatory for our process goals.

## 5. Two Storage Models, Reconciled

The reported conflict ("they recommend analytics separate and specs next to code") is softer in reality: the internal guidance is staged, and only its scaling stage (variant 3) moves specs next to code, while still keeping a central repo for business requirements and solution architecture — analytics is not "elsewhere", it is in the central repo of that variant too.

- **Central specs repo (our Model A, their variant 2):** one authoring/approval home for analysts, one process implementation, one bootstrap unit for other teams; solution-level change packages spanning systems; costs: separate spec and code PRs, drift countered by change-ID references and traceability checks.
- **Specs next to code (default OpenSpec, their variant 3 per-system layer):** atomic spec+code PRs, spec versioned with the release, minimal drift; costs: analysts working across developer repos, fragmented solution-level view, per-repo process synchronization, and the corporate approval document has no single source without an aggregation layer.
- **Recommended framing for gate 1.5:** start with Model A (variant-2-equivalent) as the first supported topology; document the variant-3-equivalent hybrid (central business/solution requirements + per-system master specs) as a later stage with explicit preconditions: per-system generated views, cross-repo change-ID traceability, and validator/CI distribution to project repos.

## 6. Follow-Ups Routed To Existing Work Items

- Drafted: the merged `define-repo-topology-config` proposal (work item 1.4) now uses the maturity-staged topology options, the process-as-versioned-folder distribution model, and the proposed version-pin location/policy.
- Routed: instruction patterns (context-study, STOP gates, self-review checklists, scout subagent, Bad/Good pairs, altitude rules) are recorded in `docs/planning/PROJECT_MEMORY_AND_WEAK_MODEL_GUARDRAILS.md` for future role skills and guardrail work.
- Routed: Delta Spec operation vocabulary, including `REMOVED`/`RENAMED`, is accepted in `openspec/specs/change-artifact-contracts/spec.md`.
- Routed: dated archive folders and archive commit-message grammar are accepted in `openspec/specs/change-lifecycle/spec.md`.
- Keep the open asset-placement decision informed by their unresolved "all CSV in one repo?" note — the pain is real in their practice too.
