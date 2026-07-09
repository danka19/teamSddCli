## Why

Phase 1 needs one merged platform-assumptions proposal before templates, validators, shared skills, setup docs, or future CI checks can assume repository paths, configuration files, process-package distribution, owner assignment, or the OpenSpec CLI version.

The internal OpenSpec-DE screenshot review confirmed useful maturity-staged topology language, but the first pilot still needs a deterministic, analyst-owned default that keeps Git/OpenSpec canonical and does not depend on AI gates.

## Evidence Boundary

- Observed from screenshots: maturity-staged topology options, workflow-as-data shape, artifact dependencies, prompt/skill patterns, delta operation vocabulary, task checkbox discipline, dated archive folders, and archive commit grammar.
- Architecture inference: these patterns can support deterministic templates, validators, read packs, and role skills, but the screenshots do not prove an owners registry, generated `CODEOWNERS`, validator/CI contract, or OpenSpec upgrade policy.
- Recommended product decision: use central `team-specs` as the first supported topology and treat specs-next-to-code as a later/federated topology with prerequisites.
- Human gate: topology/config/version/owner defaults were approved by the human owner at gate 1.5 on 2026-07-09; they remain proposed OpenSpec behavior until the final archive/accepted-spec gate.

## What Changes

- Define a proposed repository-topology maturity ladder with central `team-specs` as the recommended first supported topology.
- Define the proposed split between `team-specs` and project repositories.
- Define the proposed configuration shape: central team process config plus optional project adapter config.
- Define the proposed OpenSpec CLI version pin and upgrade policy.
- Define process distribution as one versioned process package folder containing schema, templates, role skills, and deterministic validation entry points.
- Define how project repositories consume the shared process package without maintaining manual forks.
- Define the proposed `owners.yaml` -> generated or validated `CODEOWNERS` reviewer-assignment contract.
- Explain the practical workflow difference between central specs and specs-next-to-code, including how a developer and AI agent work when specs live in `team-specs`.
- Prepare the human-readable decision packet for gate 1.5.

## Capabilities

### New Capabilities

- `repo-topology-config`: Proposed repository topology, configuration, process distribution, OpenSpec version, and owner/reviewer assignment contract for the SDD process.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not create accepted specs.
- Does not change `templates/change/`, `scripts/validate_change.py`, tests, pre-commit behavior, or CI behavior.
- Records the human-approved gate 1.5 defaults for topology/config/OpenSpec-version policy, while keeping the change unarchived until the final Phase 1 acceptance gate.
- Fed work item 1.8 validator/template expansion and still feeds the future production `team-specs` setup.
