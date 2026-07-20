## 1. Lock Selector-Level RED Evidence

- [x] 1.1 Map the six release-integrity selectors to the three modified requirements and named focused pytest nodes without changing their gap bindings.
- [x] 1.2 Add failing Delta validation tests for reused `ADDED` names, missing `REMOVED` reason or migration, and `RENAMED` content changes.
- [x] 1.3 Add failing archive tests for missing human approval, unsafe or colliding dated targets, non-dated results, and non-greppable commit subjects.
- [x] 1.4 Add failing upgrade tests for missing, stale, mismatched, unreviewed, incomplete, or AI-only upgrade evidence and unchanged installed-state hold behavior.

## 2. Enforce Delta Operation Semantics

- [x] 2.1 Implement bounded Delta parsing and accepted-baseline comparison with stable diagnostics for `ADDED`, `REMOVED`, and `RENAMED` semantics.
- [x] 2.2 Integrate Delta semantic validation into the deterministic change-validation entry point without changing ordinary strict OpenSpec behavior.
- [x] 2.3 Add positive fixtures for legitimate add, remove-with-migration, pure rename, modified behavior, and explicit remove/add flows and make the Delta focused suite green.

## 3. Enforce Archive History Convention

- [x] 3.1 Extend archive preparation with an explicit date, bounded target, approval reference, and required `spec: archive <change-id>` commit subject.
- [x] 3.2 Implement guarded local archive movement and direct result validation while preserving human approval, Git commit, merge, release, and deployment authority.
- [x] 3.3 Prove successful dated movement, convention validation, collision rejection, already-archived rejection, path containment, and pre-mutation failure safety.

## 4. Govern Process-Package Upgrades

- [x] 4.1 Add a versioned local reviewed-upgrade evidence schema and synthetic valid and invalid fixtures.
- [x] 4.2 Require identity-bound reviewed evidence in compatibility check and transactional update interfaces before any staging write.
- [x] 4.3 Prove passing strict OpenSpec and applicable validator/template evidence, explicit non-applicability, rollback-or-hold instructions, stable rejection diagnostics, and unchanged installation on failure.

## 5. Reconcile Package And Working Evidence

- [x] 5.1 Update affected package schemas, inventory, version, templates, scripts, and compatibility wrappers without editing any historical file under `process/release/`.
- [x] 5.2 Update operator runbooks and current project documentation with the Delta, archive, and upgrade contracts and human-authority boundaries.
- [x] 5.3 Bind all six selectors to exact passing pytest evidence and update current working-source counts to `295 covered / 7 gaps / 32 future_work` only after GREEN verification.

## 6. Verify, Review, And Certify A Successor

- [x] 6.1 Run focused suites, complete pytest, strict OpenSpec validation, roadmap/OpenSpec validation, package closure, privacy checks, and immutable-release diff checks.
- [x] 6.2 Complete independent product, architecture, security/authority, verification, and documentation review of the implemented release-integrity change.
- [ ] 6.3 Freeze a new immutable successor candidate only after implementation and review findings are closed.
- [ ] 6.4 Run candidate-bound deterministic, AI-disabled, Qwen, DeepSeek, Windows, WSL2, rollback, privacy, source-coverage, and independent-review certification without reusing rc4 evidence as successor proof.
- [ ] 6.5 Reconcile the roadmap, phase plan, current audit, evidence index, acceptance packet, checksums, limitations, and final human accept/reject gate from the new candidate evidence.
