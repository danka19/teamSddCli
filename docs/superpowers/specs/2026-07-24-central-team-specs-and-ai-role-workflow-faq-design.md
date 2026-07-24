# Design: central `team-specs` and AI-assisted role workflow in the FAQ

Date: 2026-07-24
Status: proposed for written human review
Source: owner feedback and explicit permission decision from 2026-07-24

## 1. Problem

The FAQ explains the central `team-specs` topology, but not the everyday work
well enough. A first-time reader still cannot confidently answer:

- whether one repository means one project or one functional product area;
- what the central repository is and why it is not a “main project”;
- what belongs in `team-specs` and what remains in code repositories;
- who keeps the central information current;
- how an Analyst, Developer or QA specialist starts from zero;
- how Developer/QA work with specs stored in another repository;
- how AI sees both repositories, chooses context and proposes code or tests;
- where AI may write and when separate human permission is required;
- what happens when one change touches several projects or FP areas;
- what works now and what remains specialist-only or planned.

This is a documentation and verification gap. It does not change the accepted
central topology or implement new orchestration.

## 2. Change intake

```text
Idea: Explain the central team-specs repository, repository/project/FP mapping,
multi-repository role workflow and practical AI-assisted implementation from a
zero-state setup.
Source: Human feedback 2026-07-24 after review of the human-readable FAQ roadmap.
Type: scope_refinement, documentation_change, verification_change
Decision: adopt_now
Reason: Without this explanation, installation and role runbooks do not let a
new analyst, developer or QA specialist use the accepted central topology in
daily work.
Affected specs: product-faq-and-role-runbook; references accepted
repo-topology-config and planned define-fp-analytics-publication-model
requirements without duplicating their normative behavior.
Affected architecture: No topology change. The FAQ documents the accepted
central control-plane model and the planned FP/project many-to-many layer.
Data contract impact: None in this documentation change.
Verification impact: Add required pages/sections/tokens and positive/negative
FAQ tests.
Status: Approved direction; written design awaits final human review before the
implementation plan.
```

## 3. Goals

The updated FAQ must:

1. Explain the topology in ordinary Russian, using English only for stable
   names, commands, file paths and identifiers.
2. State the first supported default precisely: one code repository is
   registered as one technical project ID unless a later accepted topology
   explicitly models a different shape.
3. State that a technical project is not a functional product area (ФП).
4. Explain the planned many-to-many relation: one ФП may use several projects,
   and one project/repository may serve several ФП.
5. Present `team-specs` as a central catalogue and control plane, not as a
   “main project”, code monorepository or owner of all documentation.
6. Give a complete zero-to-work route for Analyst, Developer and QA.
7. Explain both AI context routes: direct access to sibling checkouts and a
   bounded read pack for a restricted environment.
8. Enforce the accepted AI permission model: AI reads `team-specs`, writes only
   to the assigned code/test repository during implementation, and needs
   separate human permission before updating traceability/evidence centrally.
9. Explain cross-project decomposition without suggesting one AI session
   should write freely to several repositories.
10. Preserve honest boundaries: no automatic clone/pull, complete public
    multi-repository orchestration, autonomous approval, release, archive or
    external mutation.

## 4. Non-goals

This FAQ update does not:

- implement `sdd context`, multi-repository orchestration or checkout
  management;
- implement FP registries, release manifests, renderers or Confluence
  publication from `define-fp-analytics-publication-model`;
- change the accepted `central-team-specs` topology;
- make `teamSsdCli` the corporate production `team-specs` repository;
- move code, tests or implementation-local technical docs centrally;
- allow AI to approve classification, requirements, risks, waivers, QA
  conclusions, release or archive;
- duplicate canonical requirements in every role page.

## 5. Terminology

| Term | Human-readable meaning |
| --- | --- |
| Code repository | Git repository containing implementation and local tests |
| Technical project | Registered implementation context identified by `project_id`; in the first supported default it normally corresponds to one code repository |
| Functional product area (ФП) | Independent business/function area with its own analytics and requirement ownership; it is not a repository |
| Change | Reviewed unit of proposed requirement/behavior work in Git/OpenSpec |
| `team-specs` | Central catalogue and control plane for shared requirements, changes, ownership, traceability, releases and publication inputs |
| Project adapter | Small `.sdd-project.yaml` in a code repository that points to central `team-specs` |
| Bounded context/read pack | Task-specific set of canonical sources supplied to a person or AI instead of the whole repository |

The FAQ will state:

> One code repository is normally registered as one technical project ID. A
> technical project is not a ФП. Project ↔ ФП is a many-to-many relationship.

Monorepository or multiple-project-per-repository variants require an explicit
supported topology contract rather than an undocumented local convention.

## 6. Repository model

### 6.1 Recommended local layout

The main documented local route is sibling checkouts:

```text
C:/work/product/
├── team-specs/            # shared requirements and change context
├── client-profile/        # one registered technical project
├── confirmation/          # another technical project
└── common-platform/       # shared project used by several ФП
```

The project repository contains:

```yaml
project_id: client-profile
team_specs:
  reference: sibling:team-specs
  config_path: sdd.config.yaml
```

The documentation will explain:

- `sibling:team-specs` is the recommended everyday local layout;
- `registry:<id>` is the fallback when corporate checkout locations cannot be
  siblings;
- `path:<relative>` is an explicit bounded relative-path option;
- absolute personal paths must not become committed team configuration;
- specification text is not copied into the code repository;
- a developer may open the parent directory or an IDE multi-root workspace;
- an AI tool must have read access to both roots, otherwise it cannot see the
  sibling repository.

### 6.2 Source ownership

`team-specs` owns:

- stable project and FP identifiers;
- project ↔ FP mappings;
- owners and affected zones;
- proposals, Delta Specs and accepted Master Specs;
- cross-project and cross-FP changes;
- release manifests and traceability;
- links to PR, CI, test and decision evidence;
- publication inputs and process/OpenSpec version pins.

Project repositories own:

- source code;
- unit, integration and applicable acceptance-test code;
- implementation-local technical documentation;
- runtime and project build configuration;
- code PRs and implementation revisions.

Confluence is a generated view and does not own canonical requirement text.

### 6.3 Why the central repository is not excessive

The practical rule is:

> Store centrally only what connects several projects, FP areas or releases.
> Keep project-local implementation truth in its project repository.

For one small application and one team, a single-repository pilot may be
simpler. For many projects, shared components, mixed teams and independent
releases, the central catalogue prevents divergent requirement copies.

## 7. Keeping `team-specs` current

Maintenance is event-driven:

1. Project onboarding adds stable ID, repository reference, owner zones and a
   reviewed adapter.
2. Project rename/split/retirement updates the registry through review.
3. FP creation/change updates its catalogue entry and analytics namespace after
   the applicable contract exists.
4. A change records affected project ID, FP ID and zones.
5. A code PR references change and requirement/scenario IDs.
6. Tests attach reproducible result references, not unsupported success claims.
7. A release aggregates included change links without moving requirement
   ownership.
8. Delivery reconciles every affected FP current view; unresolved work remains
   a visible gap.
9. Confluence is generated only from reviewed canonical sources.

| Responsibility | Accountable role |
| --- | --- |
| Repository structure, process/config versions and onboarding rules | Process owner |
| `projects.yaml` | Process owner; affected project Tech Lead approves its entry |
| FP analytics, requirement meaning and change links | Analyst / FP owner |
| Project boundaries, affected zones and technical impact | Project Tech Lead |
| Code PR and implementation evidence | Developer |
| Scenario-to-test mapping and test evidence | QA |
| Release composition | Release owner |
| Dangling IDs, owner gaps, version drift and broken references | Validators/CI |
| Generated publication | Publisher after human-authorized configuration |

No single person manually owns all content.

## 8. AI permission model

### 8.1 Approved implementation-session default

The owner selected:

> AI may read `team-specs`, may write only inside the assigned code/test
> repository, and requires separate human permission before updating
> traceability or evidence in `team-specs`.

| Area | Developer AI | QA AI |
| --- | --- | --- |
| `team-specs` requirements/change | read-only | read-only |
| Project source code | bounded write | read-only by default |
| Project test code | bounded write | bounded write |
| Project commands | separately authorized | separately authorized |
| Central traceability/evidence | separate permission | separate permission |
| Classification, approval, risk, release, archive | prohibited | prohibited |

After implementation or QA checks, a human may authorize a separate
`team-specs` evidence update. It does not permit requirement rewriting or a
lifecycle transition by implication.

### 8.2 Analyst-specific boundary

An Analyst works mainly in `team-specs`, so the implementation-session rule is
adapted:

- AI begins read-only;
- AI may conduct discovery and separate `confirmed`, `proposed`, `unknown` and
  `conflict`;
- writing a non-authoritative draft requires explicit permission for named
  paths;
- the Analyst reviews and confirms meaning;
- AI does not confirm facts, classification, DoR or acceptance;
- an interview summary never becomes delivered/current truth automatically.

The common principle is bounded permission, not blanket ownership.

### 8.3 Direct multi-root context

For a capable local assistant:

1. Update both repositories.
2. Open their parent directory or add both as workspace roots.
3. Supply exact change ID, project ID, role, canonical path and write scope.
4. Mark `team-specs` read-only for Developer/QA.
5. Require an impact/test plan before edits.
6. Authorize command classes separately.
7. Review actual results before any evidence update.

The FAQ will include copyable prompts for Analyst, Developer and QA.

### 8.4 Restricted-AI fallback

If AI cannot access both repositories, use a bounded authority-labelled read
pack.

The FAQ will state:

- lower-level `build_read_pack.py` already exists;
- it identifies role, task, sources, authority, hashes, missing context and
  human stop;
- the pack is a generated temporary view, not a maintained specification copy;
- public `sdd` does not yet offer a complete one-command `sdd context` route;
- lower-level use links to the specialist runbook;
- missing/stale canonical context blocks work instead of being guessed.

## 9. Role journeys from zero

### 9.1 Analyst

The Analyst page will explain how to:

1. Install/verify `sdd` and obtain access to `team-specs`.
2. Clone/update the central repository required for analysis.
3. Locate an FP/change through stable IDs instead of browsing every project.
4. Start a new requirement or continue an existing change.
5. Run discovery with one question at a time.
6. Separate facts, proposals, unknowns and conflicts.
7. Identify affected FP and candidate project IDs without confirming technical
   impact for Tech Lead.
8. Prepare proposal/scenarios as a non-authoritative draft.
9. Obtain Analyst confirmation of meaning and Tech Lead confirmation of
   classification/technical impact.
10. Hand off exact IDs, sources and unresolved questions.

Normally the Analyst needs code access only for verified supporting context,
not to edit implementation.

### 9.2 Developer

The Developer page will explain how to:

1. Clone/update `team-specs` and the assigned code repository as siblings.
2. Verify `.sdd-project.yaml` and project ID through the supported config
   validator route.
3. Open both repositories in one workspace.
4. Obtain the exact change path and run `sdd next`.
5. Read only proposal, design, Delta Specs, tasks, applicable accepted specs,
   class/gate evidence and affected paths.
6. Ask AI for
   `requirement/scenario -> current code -> proposed files -> required tests`.
7. Review the impact plan with Developer/Tech Lead before edits.
8. Grant write permission only to named source/test paths.
9. Run focused and required integration checks.
10. Prepare a code PR referencing change and scenario IDs.
11. Hand actual outputs and gaps to QA.
12. Request separate permission before adding evidence centrally.

The page will say that AI cannot work from a code-only sandbox without sibling
access or a read pack.

### 9.3 QA

The QA page will explain how to:

1. Clone/update `team-specs` and the test-bearing project repository.
2. Verify the adapter and exact implementation revision.
3. Open both repositories in one workspace.
4. Read requirements/scenarios centrally, not from an AI summary or current
   implementation behavior.
5. Build a scenario-to-test matrix.
6. Identify positive, negative, regression and unavailable checks.
7. Give AI read-only source access and bounded test-path write access.
8. Run checks and record expected/actual results.
9. Distinguish implementation defect, requirement ambiguity, missing test and
   unavailable evidence.
10. Retain failed-run history.
11. Hand defects to Developer and ambiguities to Analyst/Tech Lead.
12. Request separate permission before recording QA evidence centrally.

## 10. Cross-project and cross-FP work

```text
Central change
├── bounded task and PR: client-profile
├── bounded task and PR: confirmation-service
└── bounded task and PR: frontend
```

Each task has one project ID, checkout/worktree, non-overlapping write scope,
scenario mapping, focused checks and code PR. A combined integration step then
gathers references and updates central traceability after explicit permission.
One AI session must not make overlapping unreviewed writes across all projects.

A cross-FP release aggregates links in its manifest. It does not copy
normative requirements or transfer their ownership.

## 11. Documentation information architecture

### 11.1 Recommended approach

Create one shared practical page:

```text
docs/faq/multi-repository-workspace.md
```

It owns terminology, central boundaries, sibling/registry/path layouts,
maintenance, direct-AI/read-pack routes, cross-project examples and current
limitations.

Other pages link to it and retain role-specific instructions:

- `installation.md`: short rule and topology link;
- `setup-and-topology.md`: registry/adapter setup and practical scenarios;
- `roles/analyst.md`: complete Analyst zero-start workflow;
- `roles/developer.md`: complete Developer two-repository workflow;
- `roles/qa.md`: complete QA two-repository workflow;
- `roles/process-owner.md`: onboarding and registry maintenance;
- `ai-collaboration.md`: permission matrix and role prompts;
- `glossary.md`: short definitions;
- `index.md`: direct navigation entry.

### 11.2 Alternatives considered

1. Put everything in `setup-and-topology.md`: rejected as monolithic.
2. Repeat topology in every role page: rejected because copies drift.
3. Recommended: one shared page plus role-specific routes and short links from
   installation/setup.

## 12. Human-readable writing rules

The implementation will:

- explain English stable tokens in Russian on first use;
- prefer clear Russian terms such as “центральный каталог”, “технический
  проект”, “область ФП”, “проверяемый результат” and “граница разрешений”;
- keep exact commands, file names, IDs and OpenSpec keywords unchanged;
- explain unavoidable terms such as “bounded context”, “write scope” and
  “evidence” instead of leaving them as jargon;
- give copyable commands only when they work now;
- label planned capabilities;
- place stop points and next actions beside the relevant step;
- use synthetic examples only.

## 13. OpenSpec and verification design

The implementation plan will update active
`add-product-faq-and-role-runbook`:

- proposal: record this intake;
- design: record the shared-page and permission decisions;
- FAQ spec: add scenarios for topology understanding, two-repository
  Developer/QA work and AI write boundaries;
- tasks: add one remediation task after 5.6 while task 4.4 remains open.

Validator/tests will require:

- the new shared page and hub link;
- one-repo/technical-project rule;
- project ≠ FP and project ↔ FP many-to-many wording;
- `team-specs` as central catalogue, not a main project;
- sibling checkout plus registry/read-pack fallback;
- Analyst/Developer/QA zero-start sections;
- Developer/QA write boundaries;
- separate permission before central evidence updates;
- cross-project task/PR decomposition;
- an honest statement that complete self-service orchestration is unavailable.

Negative tests will remove or weaken these elements and require failure.

## 14. Acceptance criteria

Without opening internal OpenSpec artifacts, a new reader can answer:

1. What is the difference between repository, technical project and FP?
2. Why is `team-specs` not a main project?
3. What belongs centrally and what stays beside code?
4. Who updates project, FP, implementation, QA and release information?
5. How are sibling repositories prepared?
6. How does an Analyst start from a raw idea?
7. How does Developer AI turn scenarios into a code/test impact plan?
8. How does QA AI turn scenarios into a test matrix?
9. Which repository may AI modify?
10. How is evidence returned centrally?
11. What happens when a change touches several repositories?
12. What is available now and what remains planned/specialist-only?

Automated checks prove structure and safety boundaries. Existing task 4.4
first-time human walkthrough remains the final proof of usability.

## 15. Risks and mitigations

- **Central repository becomes a dump.** Keep only shared identities,
  requirements, relations and evidence links centrally.
- **Role pages drift.** Own shared topology on one page and validate
  role-specific sections.
- **AI changes requirements and code together.** Keep `team-specs` read-only
  during implementation/test sessions and require separate permission.
- **AI reads every project.** Require task-specific IDs, paths and read packs.
- **Stale sibling checkout misleads AI.** Record revision/source commit and
  require update checks.
- **FAQ promises a missing command.** Link current lower-level tools and label
  missing self-service orchestration.
- **Many-to-many appears delivered.** Mark it planned under
  `define-fp-analytics-publication-model`, currently `0/70`.

## 16. Implementation-plan boundary

After written human review, the detailed plan will contain:

1. Extend the active FAQ OpenSpec contract and intake.
2. Add failing validator/tests for the new page and role boundaries.
3. Add the shared multi-repository workspace page and navigation.
4. Expand installation/setup/process-owner guidance.
5. Expand Analyst, Developer and QA zero-start runbooks.
6. Expand AI prompts and permissions.
7. Reconcile audit evidence, run FAQ/OpenSpec/governance checks, commit and
   push to `main` after successful verification.
