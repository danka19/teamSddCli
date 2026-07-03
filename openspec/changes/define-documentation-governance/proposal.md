## Why

The project relies on documentation and OpenSpec artifacts as the process source of truth. Phase 1 needs proposed governance rules before accepted specs, templates, scripts, and future workflow automation start depending on those documents.

Work item 1.1 commit `6fbde43` provides implementation evidence for the first deterministic gate and shows the need to keep docs, OpenSpec proposals, tests, and verification evidence synchronized.

## What Changes

- Define documentation update discipline for behavior, workflow, artifact contract, setup, security, roadmap, and user-visible command changes.
- Define required AI verification checklist evidence before completion reports.
- Define TDD-style verification behavior: scenarios first, focused tests or manual checks next, implementation last when code or deterministic behavior changes.
- Preserve the boundary between proposed OpenSpec changes and accepted living specs.
- Keep human approval required before archiving changes into accepted specs.

## Capabilities

### New Capabilities

- `documentation-governance`: Proposed documentation, verification, and acceptance discipline for SDD process work.

### Modified Capabilities

- None.

## Impact

- Adds proposed OpenSpec requirements only.
- Does not create `openspec/specs/documentation-governance/spec.md`.
- Does not modify scripts, tests, templates, or accepted specs.
