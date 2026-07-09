## Why

The project needs a deterministic foundation before any AI-assisted or CLI-assisted SDD flow can be trusted. A copyable change package template, local validator, and pre-commit hook create the first repeatable artifact gate for Phase 1.

## What Changes

- Add a repository-owned `templates/change/` skeleton for SDD change packages.
- Add `scripts/validate_change.py` to validate required files, metadata shape, OpenSpec delta presence, and basic traceability.
- Add `.pre-commit-config.yaml` so local commits can run the same validator.
- Initialize this repository's own OpenSpec area with an active change describing the artifact contract.
- Keep the gate deterministic and independent from the AI assistant layer.

## Capabilities

### New Capabilities

- `change-package-foundation`: Defines the required template and local validation behavior for the first deterministic SDD change package gate.

### Modified Capabilities

- None.

## Impact

- Adds project OpenSpec artifacts under `openspec/`.
- Adds template, validation script, focused tests, and pre-commit configuration.
- Updates roadmap, audit, and file-structure documentation.
- Does not introduce a custom `sdd` CLI or external Jira/Confluence/Bitbucket/Jenkins integrations.
