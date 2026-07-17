## Context

Phase 1 produced an accepted OpenSpec baseline plus a project-local deterministic template and validator. The accepted topology already requires central `team-specs`, a versioned process package, central configuration, optional project adapters, an OpenSpec version pin, and an owner registry, but those production artifacts do not yet exist.

The target corporate environment has weaker Qwen/DeepSeek-class assistants, unknown runtime and network constraints, and real integration details that cannot be verified externally. The reusable process must therefore be completed and certified outside that environment while all gates remain executable without AI. Corporate work must be limited to environment inventory, real configuration, approved integration wiring, a thin model adapter, and a monitored pilot.

Stakeholders are the process owner, analysts, developers, QA, repository and CI owners, and future teams consuming the process package.

## Goals / Non-Goals

**Goals:**

- Produce a reusable release candidate that installs the deterministic minor/major/hotfix process and bounded legacy migration from a versioned package.
- Make configuration, validation, setup, upgrade, rollback, and transfer evidence reproducible.
- Prove the reference class-aware flow, Tech Lead authority, and negative safety cases both without AI and with Qwen/DeepSeek-class assistants.
- Keep weak-model work bounded through deterministic launchers, authority-labelled read packs, role instructions, stop points, and evidence checks.
- Provide a full clean Windows rehearsal and a bounded equivalent Linux portability smoke on WSL2 with documented provisioned prerequisites and MCP; record macOS as not certified.
- Increase reliability through broader risk-oriented test coverage and requirement/scenario-to-evidence traceability.
- Increase delivery speed through AI-assisted decomposition and safe parallel execution of independent tasks with deterministic integration checks.
- Restrict corporate work to real environment adaptation and pilot evidence.
- Return reusable gaps to the external canonical source instead of creating an internal fork.

**Non-Goals:**

- Jira task automation, Confluence publication, QA/AT proposal generation, role inboxes, deploy, or Zephyr integration.
- A graph database, broad project-memory automation, or a complete repeated-error knowledge system.
- A custom monolithic `sdd` CLI before an accepted strategy trigger fires.
- AI approval, merge, archive, waiver approval, lifecycle ownership, or gate execution.
- Corporate credentials, internal URLs, private specifications, or concrete production values in this repository.

## Decisions

### 1. Treat the release candidate as a versioned process package, not a machine image

The reusable unit is one versioned folder containing config schemas, templates, validators, entry points, role instructions, examples, package metadata, and compatibility information. A release manifest records package version, OpenSpec pin, required runtime, included assets, checksums where practical, and verification evidence.

This follows the accepted topology and allows consumption through a pinned copy, subtree/submodule, or CI-fetched artifact. A preconfigured machine image was rejected because corporate runtime and distribution policy are unknown and image maintenance would couple the core process to one workstation environment.

### 2. Keep deterministic core, workflow launch, and AI adapters separate

The implementation is divided into these boundaries:

- configuration and schemas: parse and validate central/project settings;
- deterministic process core: validate packages, versions, evidence, and release readiness;
- workflow entry points: bootstrap, create/copy, validate, prepare PR evidence, archive support, update, and rollback;
- weak-model operating kit: role instructions, task cards, read-pack contract, stop points, and evidence-output format;
- tool adapters: thin packaging for the available AI CLI without owning workflow rules;
- certification fixtures: reference repositories, golden inputs, expected outputs, negative cases, and run records;
- transfer runbook: external release evidence, corporate inventory, adaptation, rollback, and pilot steps.

This prevents Qwen/DeepSeek packaging details from leaking into process rules and permits deterministic execution with AI disabled.

### 3. Use deterministic launchers instead of model-selected skills

A user chooses a concrete role and operation. The launcher selects the relevant instruction and bounded read pack, labels source authority, supplies explicit output and evidence requirements, and stops after one artifact stage. The model never decides which process applies or whether the next lifecycle transition is allowed.

A single free-form system prompt was rejected because weak models are less reliable at retrieving rules, managing long context, and recognizing missing inputs.

### 4. Separate external release acceptance from corporate pilot acceptance

External release acceptance requires a clean bootstrap, package/config validation, classification migration rehearsal, reference minor/major/hotfix walkthroughs, AI-disabled walkthrough, weak-model/Tech Lead certification, negative safety cases, upgrade/rollback evidence, and a complete transfer manifest.

Corporate pilot acceptance begins only from an externally accepted release candidate. It verifies actual runtime, paths, registries, policies, workflow mappings, integration wiring, adapter behavior, and one real minor, major, or hotfix change selected through approved criteria. Corporate evidence may identify compatibility gaps, but it does not silently redefine the reusable contract.

Combining release and pilot into one gate was rejected because it would hide whether a failure belongs to the reusable product or to environment-specific adaptation.

### 5. Keep corporate configuration as data, not code forks

Real repository paths, project IDs, owner groups, integration endpoints, enabled adapters, and policy overrides live in approved local or corporate configuration. Secrets remain in ignored or managed secret storage and never enter templates, fixtures, manifests, or committed read packs.

If a corporate finding requires reusable behavior, it becomes a new change in the external canonical source and a later package release. Direct long-lived edits to an internal package copy are not an accepted maintenance model.

### 6. Certify safety and process compliance, not prose quality alone

Weak-model certification uses actual Qwen/DeepSeek-class runs against role workflows and negative cases. Evidence records the model/runtime identifier, package version, read-pack identity, inputs, deterministic validation result, human intervention, forbidden-action result, and residual limitations.

Draft quality may be assessed for usability, but release acceptance requires deterministic validity, correct stop behavior, visible uncertainty, and absence of AI-owned approvals or mutations. This avoids treating fluent output as correctness evidence.

### 7. Permit parallel AI execution only across explicit independent boundaries

Concurrent work requires separate task IDs, owners, dependency declarations, non-overlapping write scopes, read packs, evidence records, and stop conditions. Tasks that share a canonical artifact, depend on unfinished output, or can make conflicting policy/lifecycle decisions are serialized. Every parallel output passes focused checks and one combined deterministic integration, traceability, review, and conflict gate before promotion.

Unbounded multi-agent execution was rejected because throughput without ownership and integration controls would reduce reliability and make failures harder to reconstruct.

### 8. Certify one shared core on Windows and Linux/WSL2

The package uses shared schemas, policy, workflow, and evidence contracts with thin platform launch/path/shell adapters. Clean hosts provision documented Python, Node.js/OpenSpec, Git, MCP, shell, and package dependencies, then execute the same fixtures, deterministic flow, update, rollback, and evidence checks.

The candidate has an immutable `payload/` plus a pre-rehearsal `release-manifest.yaml`. The manifest is excluded from the canonical payload digest and records `payload_sha256`; Windows and Linux consume byte-identical payload and manifest content. Host evidence remains external, is schema-validated, binds to `payload_sha256`, and never mutates the candidate after the first rehearsal begins. Generator inputs cannot override derived package/config/OpenSpec identity, host requirements, inventory, checksums, certification references, or rollback source.

Treating one workstation as proof of portability was rejected. Under `D-018`, Windows receives the full clean rehearsal, Linux/WSL2 receives a bounded equivalent smoke and negative matrix, and macOS is explicitly not certified.

### 9. Remediate weak-model generation through a bounded family adapter

The approved remediation flow is:

```text
deterministic launcher
  -> model-family adapter with a generated role-specific schema
  -> separate reasoning and final-response channels
  -> strict role-response parser
  -> mechanical normalizer
  -> existing deterministic operation-evidence validator
```

The launcher owns the selected workflow, role, verified sources, authority boundary, and response-contract projection. The Qwen or DeepSeek family adapter owns only runtime request formation and response-envelope handling. Only the final-response channel enters the parser; reasoning remains separate append-only evidence. The normalizer may add launch-owned identity and invariant authority fields, but it cannot change or invent model semantics. The existing validator remains unchanged as the fail-closed control plane.

Task 4.5 records the completed 2026-07-15 baseline execution. It is not reopened, unchecked, or rewritten; remediation and recertification are new tasks 4.7-4.9, and all new attempts remain append-only alongside that historical evidence.

## Risks / Trade-offs

- [Corporate runtime differs from the external certification environment] -> Keep adapters thin, publish compatibility assumptions, and require an internal environment inventory before pilot entry.
- [Weak models still produce low-quality drafts] -> Make draft quality a usability concern while deterministic checks and human review preserve correctness.
- [The process package grows into a custom CLI platform] -> Implement only the accepted class-aware core and use scripts/standard tools until a strategy trigger is evidenced.
- [Read packs become duplicate sources of truth] -> Generate or validate them from canonical paths and require authority labels plus source metadata.
- [Certification fixtures accidentally contain private data] -> Use synthetic reference content and add secret/private-path checks to release validation.
- [Corporate fixes diverge from the external package] -> Require a recorded compatibility finding, upstream change, new package version, and controlled upgrade.
- [Unknown integrations block the pilot] -> Treat integration inventory and wiring as corporate adaptation inputs; keep Jira/Confluence automation outside this release candidate.
- [Parallel workers race on canonical state] -> Require dependency/write-scope analysis, serialize conflicts, isolate evidence, and run a combined integration gate.
- [Platform adapters drift into separate behavior forks] -> Keep policy/evidence shared, adapters thin, run the full matrix on Windows and a bounded equivalent smoke/negative matrix on Linux/WSL2, and do not infer macOS support.
- [Aggregate coverage hides untested requirements] -> Generate requirement/scenario-to-test/evidence mapping and record residual gaps with owner, risk, compensation, and follow-up.

## Migration Plan

1. Create the accepted central configuration and process-package skeleton in this repository using synthetic defaults.
2. Add deterministic schemas, validation entry points, package metadata, and compatibility reporting.
3. Move or consume the existing change template and validator through the versioned package without changing accepted artifact behavior.
4. Add role instructions, task launcher inputs, bounded read-pack format, safe-parallel task/evidence contracts, evidence-output format, and synthetic certification fixtures.
5. Expand positive/negative coverage, generate requirement/scenario evidence mapping, and prove clean bootstrap, legacy migration, reference minor/major/hotfix flows, AI-disabled operation, actual weak-model/Tech Lead runs, negative cases, and upgrade/rollback behavior.
6. Rehearse the same immutable candidate through one full clean Windows run and one bounded equivalent Linux/WSL2 smoke plus negative cases, record macOS as not certified, then produce a release manifest and transfer runbook and freeze an externally accepted release candidate.
7. In the corporate environment, inventory capabilities and restrictions, populate real non-secret configuration, install secrets through approved storage, configure standard-tool and AI adapters, and re-run deterministic checks.
8. Execute one monitored real governed-change pilot selected through the approved class, risk, safety, and bounded-scope criteria and record compatibility, usability, flow, quality, and follow-up evidence.
9. Roll back by restoring the previous pinned process-package/config version; route reusable gaps into the external change workflow before publishing a replacement release.

## Open Questions

No architecture decision is blocking proposal readiness. Corporate runtime versions, network policy, artifact distribution, MCP availability, and exact Qwen/DeepSeek adapter format are mandatory adaptation inputs and must remain configurable rather than being guessed in the external package.
