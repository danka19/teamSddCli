## Context

The accepted strategy delivers SDD without a custom `sdd` CLI upfront. Process guarantees must live in templates, validation scripts, CI/pre-commit, standard tool features, and human approvals; AI role skills are convenience only.

The current project is not the production `team-specs` repository. It is the planning and foundation repository for the process. The real pilot still needs a topology/config contract that another team can understand and adopt.

Supporting inputs:

- `docs/planning/OPENSPEC_DE_INTERNAL_SOLUTION_ANALYSIS_2026-07-09.md`
- `docs/planning/REPO_TOPOLOGY_EVALUATION_CRITERIA_2026-07-09.md`
- `docs/planning/ANALYTIC_TEMPLATE_STRUCTURE_AND_MIGRATION_PLAN_2026-07-06.md`
- `docs/IMPLEMENTATION_STRATEGY.md`
- `docs/CONTEXT.md`

## Goals / Non-Goals

**Goals:**

- Give Phase 1 one merged proposal for topology, config, OpenSpec version pin/upgrade, shared process distribution, and owner/reviewer assignment.
- Make the first supported topology practical for analysts and solution-level approval across multiple systems.
- Keep project repositories ergonomic for developers and agents even when canonical specs live outside the code repo.
- Preserve a later path to specs-next-to-code only after cross-repo traceability and generated views exist.
- Avoid duplicating requirements between analytics, OpenSpec, project docs, Confluence, and code comments.

**Non-Goals:**

- Do not implement validators, templates, setup scripts, CI, or a custom CLI in this proposal.
- Do not make Confluence publication, Jira task automation, QA/AT proposal generation, role inboxes, deploy, or Zephyr/test-management integration first-MVP requirements.
- Do not require every thin change to use full-package design/tasks artifacts.
- Do not archive accepted specs before the final human gate.

## Human-Approved Gate 1.5 Decisions

Approved by the human owner on 2026-07-09:

- First supported topology: central `team-specs` with project repositories referencing change/spec IDs.
- Config shape: central `team-specs/sdd.config.yaml`, `projects.yaml`, `owners.yaml`, plus optional project-repo `.sdd-project.yaml`.
- OpenSpec version policy: pin the verified OpenSpec CLI version `1.4.1` centrally and upgrade only through a reviewed change package.
- Process reuse: one versioned process package consumed at a pinned version.
- Reviewer assignment: `owners.yaml` is the source registry and generates or validates `CODEOWNERS`.

Practical meaning of the OpenSpec pin:

- deterministic Spec PR and archive checks must compare the running `openspec --version` with the configured pin before trusting validation output;
- a developer with another OpenSpec version must either switch to the pinned version or explicitly run inside the approved tool environment;
- upgrading OpenSpec is a normal SDD change, not an ad-hoc local update: it needs compatibility evidence, strict OpenSpec validation, focused validator/template tests when available, and rollback or hold instructions;
- the OpenSpec CLI version pin and the process package version are separate pins, so process templates can evolve without pretending the OpenSpec binary changed.

## Decisions

### Decision 1: First Supported Topology

Approved gate 1.5 default: central `team-specs` plus project repositories with references.

```text
team-specs/
  sdd.config.yaml
  owners.yaml
  projects.yaml
  process/
    VERSION
    workflow.yaml
    templates/
    validators/
    skills/
  openspec/
    changes/
    specs/
  traceability/
  publication/
  analytics-assets/

project-repo/
  .sdd-project.yaml
  CODEOWNERS
  src/
  tests/
  docs/
```

`team-specs` owns the product/process truth. Project repositories own implementation truth and link back to change/spec IDs.

Alternative considered: specs next to code as the first default. This improves local developer review but fragments cross-system analytics and makes analysts work across many code repositories. It remains a later/federated topology.

Alternative considered: everything in one repository. This is useful for a small single-system pilot, but it does not match the intended multi-repo corporate process.

### Decision 2: Maturity Ladder Language

Use the internal knowledge-base ladder as the human-facing explanation:

1. **Small single-repo pilot:** docs, process, code, and tests together.
2. **Team pilot, recommended first supported topology:** central requirements/process repo plus separate code and test repositories.
3. **Federated scaling:** central business/solution requirements plus per-system Master Specs and Delta Specs near code.

Our first supported topology is step 2. Step 3 is future scope and requires:

- generated per-system views from canonical sources;
- cross-repo change-ID and requirement/scenario traceability;
- versioned process package distribution to project repos;
- validator/CI coverage in project repositories;
- a sync rule proving central analytics and per-repo specs do not diverge.

### Decision 3: Config Shape

Approved gate 1.5 default:

- `team-specs/sdd.config.yaml`: team-wide process config, including process package version, OpenSpec CLI version pin, paths, validation policy, and supported topology.
- `team-specs/projects.yaml`: registered project repositories and their roles in the topology.
- `team-specs/owners.yaml`: source owner registry.
- `project-repo/.sdd-project.yaml`: optional adapter pointer to `team-specs`, project ID, consumed process package version, and local path mapping.

The names are approved gate 1.5 defaults. They remain proposed OpenSpec behavior until the final Phase 1 archive/accepted-spec gate.

### Decision 4: Process Distribution As One Versioned Folder

The shared process package should be one versioned folder under `team-specs/process/`.

It contains:

- workflow schema, including artifact dependencies such as `requires`;
- templates;
- deterministic validators or validator entry points;
- role skill instructions;
- examples and schema fragments;
- a `VERSION` or equivalent package-version field.

Project repos consume this package by pinned copy, subtree/submodule, or CI fetch. Manual per-repo forks are not supported as the default because they create drift.

Validator design implication: the same `requires` dependencies used by role skills must be readable by deterministic validation, so AI convenience and CI rules share one artifact dependency contract.

### Decision 5: OpenSpec Version Pin And Upgrade

Approved gate 1.5 default:

- Pin the verified OpenSpec CLI version `1.4.1` in `team-specs/sdd.config.yaml`.
- Validate the running OpenSpec CLI version before Spec PR/archive checks.
- Treat process package version and OpenSpec CLI version as separate pins.
- Upgrade through a reviewed change package with compatibility evidence.

Upgrade evidence should include:

- `openspec list`
- `openspec list --specs`
- `openspec validate --all --strict`
- focused validator/template tests once work item 1.8 expands them;
- compatibility review against active changes;
- rollback/hold plan if the upgrade breaks current proposals or package validation.

### Decision 6: Owner And Reviewer Assignment

Approved gate 1.5 default:

- `owners.yaml` in `team-specs` is the source owner registry.
- Ownership zones are keyed by stable path prefixes, capability IDs, project IDs, or artifact types.
- Owner entries reference groups or roles, not personal names where possible.
- Per-repo `CODEOWNERS` is generated from or validated against `owners.yaml`.
- Multi-zone changes require approval from each touched owner zone.
- Unowned paths fall back to default reviewers and produce at least a validator warning until the owner map is fixed.
- Full packages use role approvals from `change.yaml` and validate them against `owners.yaml` for QA, security, tech lead, or product/analyst ownership.

## Practical Workflow Difference

### Central `team-specs`: how a developer and agent work

1. Analyst opens or updates a change package in `team-specs/openspec/changes/<change-id>/`.
2. Spec PR is reviewed and approved in `team-specs`.
3. Developer checks out the project repo and reads a context pack generated from `team-specs`, or opens both repositories side by side.
4. The developer/agent receives exact inputs: change ID, affected requirement/scenario IDs, spec delta paths, design/tasks if the package is full, and traceability expectations.
5. The code PR references the change ID and affected REQ/SCEN IDs. It does not copy the requirement text.
6. Project-repo CI or PR checks verify the reference format and, later, can call the central validator or fetch the pinned process package.
7. Archive readiness is checked in `team-specs`: implementation evidence, test evidence, traceability, and waivers must point back to PR/CI/manual evidence.

Practical effect: the agent working in the code repo needs a read pack or local path pointer to `team-specs`. That is extra wiring, but it keeps solution-level requirements in one place and avoids asking the analyst to edit several code repos.

### Specs next to code: how work changes

1. Analyst or developer edits specs in the same repository as code.
2. One PR can carry spec, code, and tests together.
3. The agent has local access to both requirements and implementation without cross-repo context setup.
4. Cross-system changes require multiple repo-local spec deltas plus an aggregation layer to produce the business approval view.

Practical effect: this is excellent for developer-owned, single-repo behavior, but costly when one analyst-owned change spans multiple systems and must match a corporate unified approval document.

## Risks / Trade-offs

- Central specs create a two-PR workflow for some changes. Mitigation: require code PR references and traceability evidence; later add context-pack generation.
- Specs-next-to-code may be needed later for release-local system contracts. Mitigation: record it as a future federated topology with strict preconditions.
- A single process package can become a bottleneck if every team needs custom behavior. Mitigation: support versioned package releases and team-local config, not manual forks.
- `owners.yaml` can become stale. Mitigation: generated/validated `CODEOWNERS` and drift checks.
- OpenSpec upgrades can break active proposals. Mitigation: reviewed upgrade change package with rollback/hold plan.

## Human Decision Packet For Gate 1.5

### Question 1: Where should the canonical specs live for the first pilot?

Recommended default: **Option A - central `team-specs`**.

Option A - central `team-specs` with project-repo references:

- Best when analysts own requirements and one business change can affect several systems.
- Developers work from a context pack or sibling checkout and reference change/spec IDs in code PRs.
- Risk: requires cross-repo links and traceability discipline.

Option B - specs next to code:

- Best when each team owns one code repo and developers own most specs.
- One PR can update spec, code, and tests together.
- Risk: solution-level approval becomes fragmented and analytics can diverge.

Option C - start single-repo for the pilot only:

- Best for a very small demo.
- Lowest setup cost.
- Risk: proves less about the real multi-repo corporate workflow.

Blocked if unresolved: template paths, validator discovery, project setup docs, and work item 1.8 enforcement.

### Question 2: Which config file shape should become the first supported format?

Recommended default: **Option A - central team config plus small project adapter**.

Option A - `team-specs/sdd.config.yaml`, `projects.yaml`, `owners.yaml`, plus optional `project-repo/.sdd-project.yaml`:

- Clear source ownership and easy validation.
- Slightly more setup, but explicit.

Option B - one central config only:

- Minimal project-repo footprint.
- Harder for project repos and agents to discover the central process without conventions.

Option C - config copied into every project repo:

- Easy local discovery.
- High drift risk unless distribution tooling is strong from day one.

Blocked if unresolved: config validation requirements, OpenSpec pin location, owner registry location, project-repo adapter behavior.

### Question 3: How should OpenSpec version upgrades work?

Recommended default: **Option A - pin `1.4.1` centrally and upgrade only through a reviewed change package**.

Option A - central pin plus reviewed upgrade:

- Most deterministic and auditable.
- Slower upgrades, but safe.

Option B - allow local newer patch versions within a range:

- More flexible for developers.
- Higher risk of version-specific validation differences.

Option C - do not pin until pilot:

- Fastest setup.
- Leaves AUDIT-017 open and makes validator behavior less reproducible.

Blocked if unresolved: version checks, upgrade workflow, template/validator compatibility, work item 1.8.

### Question 4: How should shared process assets be reused by project repos?

Recommended default: **Option A - one versioned process package consumed at a pinned version**.

Option A - versioned package folder from `team-specs/process/`:

- One source for schema, templates, skills, and validators.
- Requires a documented bootstrap and update command/process.

Option B - subtree/submodule:

- Git-native pinning and diff visibility.
- Can be harder for less technical contributors.

Option C - copy files manually:

- Easy once.
- Drift-prone and not acceptable as the long-term default.

Blocked if unresolved: other-team bootstrap, project-repo CI consumption, skill/template upgrade path.

### Question 5: How should reviewers be assigned?

Recommended default: **Option A - `owners.yaml` generates or validates `CODEOWNERS`**.

Option A - `owners.yaml` as source registry:

- One owner map for specs, code zones, QA/security roles, and generated reviewer rules.
- Requires drift checks.

Option B - per-repo `CODEOWNERS` only:

- Native to Git hosting.
- Harder to coordinate solution-level ownership across repos.

Option C - default reviewers only:

- Fastest to start.
- Weak traceability and high risk of missing the right role owner.

Blocked if unresolved: reviewer assignment contract, full-package role approvals, multi-zone PR requirements.
