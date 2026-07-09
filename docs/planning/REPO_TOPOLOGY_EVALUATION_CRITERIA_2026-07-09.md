# Internal OpenSpec Customization Screenshots: Evaluation Criteria And Topology Comparison Frame

Status: planning input for Phase 1 work item 1.4 (`define-repo-topology-config`). Prepared 2026-07-09; updated after the screenshot review. Not an accepted contract.

Full review: `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md`.

## 1. Input Status

- The human owner moved the corporate analytics template photos from the earlier local `/analytic-template/` folder to `arch-screenshots/analytic-template/`.
- The internal OpenSpec customization screenshots were re-added to the git-ignored local folder `arch-screenshots/openspec-de/` and reviewed on 2026-07-09.
- The full review covered 25 photos. The key process, templates, topology options, and master-spec structure were readable enough for work item 1.4 planning.
- Readability limits remain: the tail of the workflow schema, the unexpanded practical repository examples, and the beginning of the frame-selection section were not fully visible. Any future transfer of exact template text requires original files or exported docs, not photos.

Evidence levels for later proposal work:

- **Observed on screenshots:** staged topology variants, workflow schema shape, artifact chain, PR review points, AI verify output classes, and developer-shaped master-spec tree.
- **Architecture inference:** implications for our deterministic-gates-first process, analyst authoring, and cross-repo traceability.
- **Recommendation:** central `team-specs` as first supported topology with project-repo references; specs-next-to-code as later/federated option.

## 2. Evaluation Criteria

Each criterion references the accepted product goal: deterministic OpenSpec/Markdown-first SDD process, Git as canonical source, Confluence as generated publication/read model, standard tool features plus validators for gates, and AI as draft/review convenience only.

1. **AI-independence of process guarantees.** Do gates work when AI is disabled or weaker than the external development assistant?
2. **Approval unit and authoring role.** Is the source model designed for analyst-owned, solution-level changes or for developer-owned, repo-local changes?
3. **Single source of truth.** Does the model avoid splitting behavior truth across analytics docs, per-repo specs, Confluence, and code comments?
4. **Repository topology and content split.** Which artifacts live in `team-specs`, and which live next to code?
5. **Config ownership.** Where do team-wide process config, per-project pointers, version pins, path mappings, and owners live?
6. **Human readability without tooling.** Can analysts, reviewers, and developers understand the raw Git/Bitbucket source?
7. **Deterministic validatability.** Can required files, IDs, links, states, versions, owners, and evidence be checked by scripts/CI?
8. **Thin-MVP compatibility.** Does the model preserve small thin changes, or does it force full-package burden on every change?
9. **Traceability.** Can requirement -> scenario -> design/task -> test/evidence -> waiver links be checked or reported?
10. **Other-team reuse.** Can another team consume templates, validators, and role skills through a versioned bootstrap path instead of copying history?
11. **Owners and reviewer assignment.** Are reviewers derived from an explicit registry or generated rules rather than tribal memory?
12. **Corporate approval compatibility.** Can the source model later generate the familiar approval view without manual dual truth?
13. **OpenSpec version and upgrade policy.** Is the OpenSpec CLI/process package pinned, and is upgrade compatibility reviewed?
14. **Maintenance and drift cost.** What prevents copied skills, generated views, repo-local specs, and code references from drifting?

## 3. Screenshot Findings Relevant To Topology

The screenshots do not show a single universal recommendation. They show a maturity-staged model:

- **Variant 1:** small/single-capability pilot in one repository with docs, AI tooling, code, and tests together.
- **Variant 2:** team pilot with separate requirements, code, and tests/autotests repositories.
- **Variant 3:** scaling/pilot model with a central requirements repository for business requirements, solution architecture, and e2e scenarios, plus per-system repositories that carry master specs and delta specs next to code.

This matters for our comparison: "specs next to code" appears as a later scaling option, not as the only recommended topology. The screenshots also do not confirm an owners registry, generated `CODEOWNERS`, deterministic validator/CI contract, or OpenSpec upgrade policy; those must be designed in our proposal.

## 4. Storage Models To Explain At Gate 1.5

### Model A - central `team-specs` repo

Analytics sources, Master Specs, Delta Specs/change packages, QA/AT plans, traceability, templates, validation scripts, publishing config, owner registry, and future typed analytics records live in one central analyst-facing repository. Project repositories keep code, tests, AT code, code-local technical docs, and references to change IDs or requirement/scenario IDs instead of copying requirements.

Why this fits our first pilot:

- Analysts author in one place.
- The approval unit is solution-level and can span multiple systems.
- Generated Confluence publication later has one canonical source.
- Shared process assets evolve once.
- Another team can bootstrap from one process repository.

Costs:

- Spec PRs and code PRs are separate.
- Code PRs need explicit change/spec references.
- Cross-repo CI and traceability checks matter for full packages.

Daily developer/agent workflow:

1. The analyst works in `team-specs/openspec/changes/<change-id>/` and keeps analytics, Delta Specs, traceability, and approval notes together.
2. The developer opens the code repository and receives a bounded read pack: change ID, affected REQ/SCEN IDs, spec delta paths, design/tasks if present, and expected evidence.
3. The agent reads `team-specs` through a sibling checkout such as `../team-specs/...` or through a configured project adapter path. It does not copy requirement text into the code repo.
4. The code PR references the change ID and stable requirement/scenario IDs; implementation evidence, tests, manual checks, and waivers link back to the central package.
5. Archive readiness is checked in `team-specs`, where solution-level evidence can be reviewed across several project repositories.

### Model B - specs next to code with separate analytics

Each project repository carries its own `openspec/` state near code. Analytics or business/solution docs live centrally or elsewhere.

Why this works for some teams:

- Spec, code, and tests can be reviewed atomically in one repo.
- Code owners review the requirements nearest to implementation.
- The model matches default developer-local OpenSpec usage.

Why it is risky as our first default:

- Cross-system business changes fragment into per-repo spec slices.
- Analysts must understand and work across developer repositories.
- Unified approval views require aggregation from many repositories.
- Shared validators/templates/skills need distribution and upgrade discipline from day one.
- If analytics and specs are both editable sources, dual truth returns.

Daily developer/agent workflow:

1. The developer opens one project repository and sees requirements/spec deltas next to code.
2. The agent can update spec, code, and tests in one PR with minimal cross-repo context setup.
3. For a cross-system change, the analyst or tech lead must coordinate several repo-local spec deltas and a central analytics/approval view.
4. Generated corporate approval views need an aggregation layer that proves all per-repo specs match the central business change.
5. Drift checks become mandatory early, because analytics and per-repo specs can otherwise disagree.

### Recommended hybrid for the first supported topology

Use Model A first, with lightweight project-repo references:

- `team-specs` is canonical for analytics, change packages, Master Specs, Delta Specs, traceability, shared process assets, owners, config, and publication config.
- Project repos own implementation artifacts and reference change/spec IDs.
- A small project config file can point back to the central process config and supported OpenSpec/process version.
- Specs-next-to-code is documented as a future/federated topology only after cross-repo traceability, generated views, and shared asset distribution are proven.

## 5. Recommendation Frame

Borrow from the internal solution:

- artifact height rules: proposal = why/what, specs = requirement deltas, design = code bridge, tasks = executable checklist;
- staged workflow: explore/propose/spec/design/task/apply/verify/archive;
- STOP-and-confirm and self-review checklists as AI-layer guardrails;
- `ADDED` / `MODIFIED` / `REMOVED` / `RENAMED` delta vocabulary to review against our Delta Spec contract;
- `tasks.md` checkbox contract with implementation, unit-test, verify, and commit grouping;
- topology maturity narrative for the human decision packet.

Do not borrow as first-MVP defaults:

- AI-only gates;
- rich developer-shaped master-spec tree as mandatory thin-change structure;
- copied AI tooling in every project repo without versioned distribution;
- `develop` as the only branch model;
- non-blocking critical verification findings;
- specs-next-to-code as the first canonical topology.

Routed result: `openspec/changes/define-repo-topology-config/` is now the canonical proposed contract for work item 1.4. This criteria file remains supporting evidence and the practical comparison frame for gate 1.5.
