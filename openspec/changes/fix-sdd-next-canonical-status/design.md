## Context

Schema-v2 change writers and `change-v2.schema.json` use the required field
`status` with the six accepted lifecycle values. The public `sdd next` handler
currently reads `lifecycle_state`, while its handcrafted tests write the same
noncanonical field. The handler then passes the value to the conceptual guided
fact named `lifecycle_state`.

The storage contract and guided fact name are different boundaries: fixing the
storage adapter does not require renaming the guided catalog or changing its
allowed-values policy.

## Goals / Non-Goals

**Goals:**

- Continue a change created by the real schema-v2 writer.
- Keep `status` as the only lifecycle field in `change.yaml`.
- Reuse the guided catalog as the source of accepted lifecycle values.
- Preserve structured fail-closed output and the no-mutation boundary.
- Replace synthetic evidence with a writer-to-dispatcher regression test.

**Non-Goals:**

- Adding `lifecycle_state` to schema-v2 packages.
- Supporting both storage fields or inventing a compatibility window.
- Renaming the internal guided fact.
- Performing full change-package validation inside `sdd next`.
- Enabling lifecycle, release or external mutations.

## Decisions

### 1. Read only `status` at the storage boundary

The dispatcher reads the top-level `status` value and passes it to
`guide(..., {"lifecycle_state": status})`. This keeps the canonical persisted
contract and the existing guided route isolated from each other.

Accepting both fields was rejected because it would preserve an undocumented
second contract and make conflicting values possible. Renaming the guided fact
was rejected because it expands a one-line adapter defect into catalog/API
churn without changing user value.

### 2. Reuse guided-route validation

Missing, empty or non-string `status` is blocked at the parser boundary with a
status-specific diagnostic. A nonempty but unsupported value is passed to
`guide`, whose canonical `allowed_values` contract returns a structured block.
The dispatcher does not duplicate the six-value enum.

Full schema validation was rejected because `sdd next` only needs change
identity, role and lifecycle to explain the next action; package validation
remains a separate deterministic operation.

### 3. Test the real producer-consumer path

The regression test creates a change through `create_change`, confirms that the
result contains `status` and no `lifecycle_state`, and invokes the public
`sdd next` entrypoint. Separate negatives cover a file containing only
`lifecycle_state` and an unsupported `status`.

## Risks / Trade-offs

- [An old handcrafted file contains only `lifecycle_state`] → block clearly;
  do not silently normalize or mutate it.
- [The guided status enum changes] → continue to consume the guided catalog
  validation instead of copying the enum into the dispatcher.
- [A valid status exists in an otherwise invalid package] → `sdd next` remains
  guidance-only; deterministic validation is still required before governed
  work or a transition.

## Migration Plan

1. Add failing producer-consumer and invalid-field regression tests.
2. Change the dispatcher storage lookup from `lifecycle_state` to `status`.
3. Update FAQ limitations and run the real first-change continuation smoke.
4. Roll back by reverting the change; no persisted data migration is required.

## Open Questions

None.
