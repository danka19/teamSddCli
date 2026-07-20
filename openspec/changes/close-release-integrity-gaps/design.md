## Context

The accepted specifications already describe Delta operation semantics, dated archive history, a greppable archive commit, and reviewed upgrade evidence. The working certification source correctly leaves six scenarios uncovered because the current implementation only composes Delta sections, prepares archive review without moving or validating history, and performs transactional package compatibility/update without a reviewed upgrade record.

These controls sit on the release-integrity path: malformed deltas can corrupt the accepted-spec view, ambiguous archive history weakens auditability, and an unreviewed compatibility update can replace the process package despite technically valid files. The implementation must remain local, deterministic, AI-disabled, safe on Windows and WSL2, and subordinate to explicit human approval.

## Goals / Non-Goals

**Goals:**

- Enforce the three accepted Delta operation scenarios against the accepted-spec baseline.
- Provide a guarded local archive operation and direct convention validation for the dated path and commit subject.
- Make reviewed upgrade evidence a required input to compatibility acceptance and transactional update.
- Produce exact RED/GREEN tests and selector bindings for all six release-integrity scenarios.
- Preserve failure evidence, rollback/hold behavior, human authority, and immutable historical release snapshots.

**Non-Goals:**

- Implement feedback disposition, CODEOWNERS derivation, AI traceability suggestions, or legacy baseline onboarding.
- Add Jira, Confluence, Bitbucket, Jenkins, deployment, or other remote integration.
- Let a script approve a change, create an approval record, merge, release, or decide that a candidate is acceptable.
- Rewrite `phase-2-14-rc4` or reuse its certification as evidence for a successor.

## Decisions

### Keep one candidate-blocking change with three isolated enforcement surfaces

The three groups share one release-integrity acceptance boundary and all must close before candidate freeze, so they use one OpenSpec change. Implementation remains separated by contract: Delta validation belongs with change validation, archive behavior belongs with workflow operations, and upgrade evidence belongs with package compatibility/update. This avoids three partially accepted candidate states without creating a generic policy engine.

Alternative considered: three independent OpenSpec changes. Rejected for this remediation because it would allow partial candidate-freeze ambiguity and duplicate the same verification/certification closure work.

### Validate Delta semantics against the accepted baseline

The deterministic validator will parse operation sections and compare affected names with the corresponding accepted capability spec. `ADDED` fails when it reuses an existing requirement name; `REMOVED` requires explicit `Reason` and `Migration` fields; `RENAMED` accepts only `FROM:`/`TO:` name pairs and rejects embedded behavior text, which must be expressed as `MODIFIED` or remove/add. Diagnostics use stable codes and bounded paths.

Alternative considered: rely on OpenSpec strict validation alone. Rejected because current strict validation accepts structurally valid deltas without enforcing these project-specific semantic rules.

### Separate archive authorization, filesystem mutation, and Git commit authority

Archive preparation will resolve the approved change ID, explicit archive date, dated target path, and required commit subject `spec: archive <change-id>`. A guarded archive operation may move the local change only after deterministic readiness checks and an explicit human archive-approval record are supplied; it fails if the source is already archived, the target exists, or the target escapes the configured archive root. The operation does not create a Git commit or infer approval. A direct validator checks the resulting path and supplied commit subject so both conventions are independently testable.

Alternative considered: have the tool create and commit the archive automatically. Rejected because commit and final archive actions remain explicitly user-authorized workflow steps and because hiding Git mutation inside a helper weakens recovery and review.

### Require a versioned reviewed-upgrade record at check and update boundaries

A local schema-bound upgrade record will identify the reviewed change package, from/to package and OpenSpec compatibility versions, review decision reference, compatibility evidence, strict OpenSpec result, validator/template results or explicit non-applicability, and rollback-or-hold instructions. Compatibility check validates and reports this record without mutation; update accepts only the same validated record and binds it to the candidate identity before any staging write. Failure retains the normal installed package and returns a stable hold diagnostic.

Alternative considered: infer review from a version bump or passing compatibility probe. Rejected because neither proves that the behavioral/template impact was reviewed or that rollback/hold instructions exist.

### Re-certify only after source remediation is complete

The six selector bindings change from product gaps to exact pytest evidence only after their focused tests pass. The expected working inventory then becomes `295 covered / 7 gaps / 32 future_work`. A successor candidate is frozen afterward and receives new candidate-bound deterministic, AI-disabled, model, platform, and independent-review evidence.

## Risks / Trade-offs

- [Delta comparison can reject legitimate complex changes] -> Keep rules narrow, emit stable selector-specific diagnostics, and require explicit `MODIFIED` or remove/add when behavior changes.
- [Archive movement can strand a working tree] -> Require a bounded source and target, fail before mutation on collision or missing approval, and add failure/rollback tests around the move boundary.
- [A syntactically valid upgrade record can still contain a poor human judgment] -> Validate identity and evidence completeness deterministically while keeping the accountable review decision human-owned and source-referenced.
- [One combined change is larger than the prior focused-test slice] -> Keep three independent RED/GREEN task groups, separate write surfaces, and a combined full-suite/candidate gate.
- [Process-package interfaces change] -> Version the new evidence schema and package contract, update templates/runbooks, and prove update/rollback compatibility before candidate freeze.

## Migration Plan

1. Add failing tests and fixtures for all six selectors without changing the evidence manifest.
2. Implement Delta validation, then archive convention enforcement, then reviewed upgrade evidence as separate RED/GREEN slices.
3. Update schemas, templates, scripts, package inventory/version, and runbooks required by those contracts.
4. Run focused and full deterministic verification, update selector bindings to `295/7/32`, and obtain independent review.
5. Freeze a new successor candidate and run the complete candidate-bound certification sequence.
6. On any remediation or certification failure, keep rc4 and failed evidence immutable, do not promote the successor, and return to the failing slice with a recorded hold.

## Open Questions

None for proposal readiness. Exact schema field names and diagnostic codes are implementation details constrained by the requirements and will be locked by RED tests before production changes.
