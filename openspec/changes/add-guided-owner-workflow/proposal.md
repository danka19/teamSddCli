## Roadmap

- Execution phase: P3
- Related phases: P4, P5
- Lifecycle status: planned

## Why

The externally certified process package has deterministic commands, policies, role instructions, and runbooks, but it lacks one self-service entry point for a colleague who starts with a business situation rather than knowledge of repository internals. A user cannot reliably discover which command applies, what evidence it needs, or which decision remains human-owned without navigating several technical documents.

This gap blocks a credible pre-corporate handoff. The package must be usable by a human or an AI assistant from the same situation-based operating contract before it is installed in a corporate environment.

## What Changes

- Add a versioned, situation-based guided-operation contract that maps a declared business situation and known change state to permitted next commands, inputs, expected evidence, blockers, fallbacks, and human decision boundaries.
- Provide one discoverable guided CLI entry point that reads the contract and returns machine-readable and human-readable next-step guidance without mutating canonical artifacts or deciding human gates.
- Publish one concise human/AI onboarding guide generated from or validated against the same contract; it begins with a business requirement and explains the path through Delta Spec, review, implementation, QA, evidence, release, and archive.
- Add synthetic end-to-end examples and negative cases for missing context, unavailable AI/integrations, forbidden authority delegation, unknown situation, and unsafe state transitions.
- Require installation, bootstrap, guided-operation, and AI-disabled fallback verification before the successor process package is considered ready for corporate adaptation.

## Capabilities

### New Capabilities

- `guided-owner-workflow`: Self-service, situation-based operation of the process package by humans and AI assistants.

### Modified Capabilities

None.

## Impact

- Affects reusable package distribution, command discovery, onboarding documentation, workflow metadata, synthetic fixtures, and deterministic verification.
- Does not change RC6, archived specs, historical certification evidence, corporate configuration, remote integrations, or human approval authority.
- Requires a successor versioned process package and fresh pre-corporate verification before corporate adaptation begins.
