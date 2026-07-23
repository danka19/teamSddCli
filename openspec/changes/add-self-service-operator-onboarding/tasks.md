## 1. Installed entrypoint and compatibility

- [ ] 1.1 Choose and implement the supported Windows/POSIX launcher packaging for the versioned `sdd` command.
- [ ] 1.2 Route the installed launcher to the selected package dispatcher and expose package/version diagnostics.
- [ ] 1.3 Preserve and test every documented direct `scripts/*.py` compatibility contract.

## 2. Guided local workflow

- [ ] 2.1 Implement `sdd start` for interactive and structured situation selection without implicit mutations.
- [ ] 2.2 Extend `sdd next` with one canonical continuation result: status, missing facts, role owner, authority boundary, fallback and exact command.
- [ ] 2.3 Add human and JSON renderers derived from the same continuation result.
- [ ] 2.4 Implement confirmation-gated `sdd setup` preflight and central `team-specs` bootstrap delegation.

## 3. Safety and evidence

- [ ] 3.1 Add negative tests for absent confirmation, non-empty target, invalid configuration, missing role/fact and unsupported route.
- [ ] 3.2 Prove that `sdd run`, release operations and every external mutation remain fail-closed through the new entrypoint.
- [ ] 3.3 Add a clean-sandbox e2e walkthrough: setup, first `minor` change, Spec PR preparation and archive preparation.
- [ ] 3.4 Update package metadata, catalog, generated command help and topology/setup runbooks.

## 4. Verification

- [ ] 4.1 Run focused launcher, dispatcher, bootstrap, topology and negative-boundary tests.
- [ ] 4.2 Run the relevant package/release regression suite, `openspec validate --all --strict`, roadmap/OpenSpec validation and `git diff --check`.
- [ ] 4.3 Record the synthetic AI-disabled and human walkthrough evidence without secrets or external calls.
