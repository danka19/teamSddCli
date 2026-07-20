## Roadmap

- Execution phase: P2
- Related phases: P4
- Lifecycle status: accepted

## Why

The working successor source still has six high-risk release-integrity scenarios without deterministic product enforcement. Freezing another candidate before closing them would certify a process that describes Delta operations, archive history, and reviewed upgrades but does not reliably enforce those contracts.

## What Changes

- Enforce the accepted Delta Spec operation vocabulary so `ADDED` cannot silently modify existing behavior, `REMOVED` carries reason and migration evidence, and `RENAMED` cannot hide content changes.
- Add a deterministic, human-authorized archive operation or equivalent validator that uses a dated history path and produces a stable greppable archive commit convention without transferring approval authority to automation.
- Require reviewed change-package evidence, compatibility checks, strict OpenSpec validation, validator/template verification when applicable, and rollback or hold instructions before a process-package or OpenSpec compatibility upgrade is accepted.
- Preserve failed-run evidence, deterministic and AI-disabled operation, explicit human approval, and the immutable `phase-2-14-rc4` snapshot.
- Require RED/GREEN selector-level tests for all six scenarios before successor-candidate freeze.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `change-artifact-contracts`: Make the existing Delta Spec vocabulary deterministically enforceable for added, removed, and renamed behavior.
- `change-lifecycle`: Make the existing archive history convention an executable or directly validated contract after explicit human approval.
- `repo-topology-config`: Make reviewed upgrade evidence a required deterministic input to compatibility upgrade acceptance.

## Impact

- Affects change-package validation, archive preparation/execution, update compatibility gates, templates or schemas used by those flows, and their focused tests.
- Adds no Jira, Confluence publication, deployment, QA/AT generation, or role-inbox integration.
- Does not freeze or certify a candidate; candidate creation remains a later step after this change is implemented, verified, and independently reviewed.
