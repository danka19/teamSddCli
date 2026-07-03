## Context

The accepted implementation strategy says the first delivery layer must be deterministic: templates, validation scripts, pre-commit, and CI-friendly checks must carry process guarantees without relying on AI. The repository currently has documentation only; no `openspec/`, templates, scripts, tests, or pre-commit gate exist.

## Goals / Non-Goals

**Goals:**

- Provide a copyable SDD change package skeleton under `templates/change/`.
- Provide a Python validator that works as a local command and as a pre-commit hook.
- Validate the template itself in placeholder mode while rejecting placeholder values for real change packages.
- Avoid false positives against this project's own OpenSpec changes, which do not contain `change.yaml`.

**Non-Goals:**

- Build a custom `sdd` CLI.
- Publish to Confluence, create Jira tasks, assign Bitbucket reviewers, or run Jenkins.
- Fully validate every OpenSpec semantic rule; OpenSpec CLI remains responsible for OpenSpec-native validation.
- Require Gherkin for every QA scenario.

## Decisions

- Use a standalone Python script with no mandatory third-party runtime dependency because the corporate target environment is not verified yet.
- Keep pre-commit as a thin wrapper over `scripts/validate_change.py` so local and CI behavior can share the same gate.
- Discover SDD change packages by the presence of `change.yaml`; this prevents the hook from treating plain project OpenSpec changes as SDD change packages.
- Require a simple traceability row from requirement to scenario and allow task/test/automation links to be filled later or waived by future policy.
- Include `--allow-placeholders` only for validating the template skeleton; real package validation rejects placeholder values.

## Risks / Trade-offs

- Limited YAML support without a dependency can miss advanced YAML constructs -> keep `change.yaml` and `traceability.yaml` templates simple and document the expected shape.
- The first validator is intentionally narrow -> later Phase 1 work must expand requirements for thin/full modes, waivers, and archive readiness.
- Pre-commit is not installed on the current machine -> verify config shape and validator behavior now, then run `pre-commit run --all-files` after the tool is installed.

## Migration Plan

- Add the template and validator in this repository.
- Use the template by copying `templates/change/` into the target `team-specs/openspec/changes/<change-id>/` folder and replacing placeholders.
- Add the pre-commit hook to local clones once `pre-commit` is installed.

## Open Questions

- The exact OpenSpec CLI version pin location for team repositories still needs a later Phase 1 decision.
- The final thin/full artifact matrix and waiver policy still need dedicated OpenSpec specs.
