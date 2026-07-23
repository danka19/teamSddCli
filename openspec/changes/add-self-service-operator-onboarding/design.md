## Context

P3 already has a canonical operation catalog and a thin local dispatcher, but its public entrypoint is `python scripts/sdd.py`; bootstrap is another named script. This exposes implementation topology to an operator and breaks the intended situation-first experience. The design must make the supported path discoverable without transferring authority to AI or enabling P3 mutations.

## Goals / Non-Goals

**Goals:** one installed `sdd` command; explicit `setup`, `start` and `next` routes; stable human/AI-readable response envelope; a clean-sandbox walkthrough; and retained compatibility for direct scripts.

**Non-Goals:** Jira, Confluence, Bitbucket, Jenkins, network calls, credentials, release execution, external mutation, AI auto-approval, or changing the accepted P3 fail-closed boundary.

## Decisions

- Package a small platform launcher named `sdd` that delegates to the versioned dispatcher. This is preferred to asking users to put the repository on `PATH`, because the package remains relocatable and versioned.
- Keep `sdd guide` as the deterministic routing primitive; add `sdd start` as a human-friendly interactive/non-interactive facade, and define `sdd next` as the canonical continuation query. This extends the existing dispatcher instead of creating a second workflow engine.
- Implement `sdd setup` as a local mutation with an explicit confirmation artifact/flag and a preflight. It delegates to the existing bootstrap contract and records only local deterministic evidence. This is safer than implicit creation of a team workspace.
- Return the same structured result to a terminal user and an AI caller: current state, missing context, responsible role, authority boundary, fallback and the next exact `sdd` command. Human rendering is derived from this canonical result to avoid drift.
- Preserve direct `scripts/*.py` contracts and test them as a compatibility surface. The new launcher is the recommended interface, not a breaking replacement.

## Risks / Trade-offs

- [Launcher installation differs by OS] → support explicit Windows and POSIX installation contracts and test both packaging paths where certified.
- [A convenient CLI could imply authority] → every mutation remains confirmation-gated and P3 `run` remains fail-closed.
- [Interactive prompts are hard for AI/CI] → every route also supports non-interactive structured input/output.
- [FAQ may promise unavailable automation] → the CLI result and runbook must state whether an action is local, prepared-only, blocked, or requires a later accepted change.

## Migration Plan

1. Add launcher and commands while retaining direct scripts.
2. Build and validate a clean sandbox through `sdd setup`.
3. Run compatibility and e2e tests before making `sdd` the documented default.
4. Keep old paths documented as internal compatibility only; no destructive migration is required.

## Open Questions

- Select the supported packaging mechanism and installer UX for the first certified Windows release; the proposal requires one installed command but does not preselect a package manager.
