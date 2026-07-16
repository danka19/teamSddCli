## Context

Adapter `2.0` moved weak-model execution from free-form output to a closed role-specific schema, separated reasoning from final output, prohibited semantic repair, and retained a single structural retry. The 2026-07-16 remediation run then produced ten schema-valid responses and ten semantic failures:

| Failure class | Observed count | Meaning |
|---|---:|---|
| `block` with a non-null completed role artifact | 9/10 | The schema allowed a contradictory state that the normalizer correctly rejected. |
| Wrong `draft`/`block` decision | 5/10 | Models treated missing approval as a ban on advisory drafting or failed to block an authority case. |
| Missing or incorrect required reason codes | 7/10 | Models used plausible synonyms instead of the stable process vocabulary. |
| Missing required role source IDs | 2/10 | Models omitted a required authority or role source despite using related prose. |
| Fabricated successful check | 1/10 | DeepSeek marked a policy/digest check passed while stating the context was absent. |
| Missing unresolved input on a blocked result | 1/10 | The model recognized unsupported evidence but returned an empty unresolved-input list. |

The adapter must reduce representational ambiguity without converting the certification schema into an answer key. Expected decisions, case-specific reason codes, required artifact kinds, and validator results remain launcher-internal. Source IDs are different: the bounded pack is launcher-selected required context, so its available IDs are intentionally visible and the model is tested on faithful attribution rather than hidden source selection.

## Goals / Non-Goals

**Goals:**

- Make `draft` and `block` mutually exclusive structural branches selected by the model's own `decision`.
- Make the draft artifact kind a model-owned value selected from one neutral global vocabulary.
- Make a completed role artifact structurally impossible on the `block` branch.
- Require meaningful draft evidence and meaningful block disposition without case-specific answer leakage.
- Clarify that human approval is required for canonical transition, not for preparation of a bounded non-canonical advisory draft.
- Preserve semantic validation of decision, reason codes, attribution, facts, evidence truth, and role output kind.
- Preserve one structural retry, immutable evidence, exact observed runtime identity, external raw destinations, and byte-compatible adapters `1.0`/`2.0` schema/prompt reconstruction.
- Prevent model-authored checks from becoming passed execution evidence without launcher-bound proof.
- Retain runtime/identity/interrupted-call operational failures and bind runtime-probe result checksums into normalized evidence.
- Re-run Qwen and DeepSeek in new adapter `2.1` artifact roots and keep each matrix gated by five-of-five preflight.

**Non-Goals:**

- Deterministically selecting the decision or artifact kind for the model.
- Exposing case-specific expected decisions, reason codes, required artifact kind, or validator result. Supplied source IDs remain visible because they are launcher-selected required context.
- Adding semantic retries, critique prompts, chain-of-thought inspection, or automatic response correction.
- Weakening authority, safety, source attribution, evidence, runtime-identity, privacy, or canonical-write controls.
- Rewriting the 2026-07-15 or 2026-07-16 raw and normalized evidence.
- Certifying a model on anything less than five-of-five preflight and fifteen-of-fifteen matrix for its exact observed identity.

## Decisions

### 1. Use a version-discriminated decision schema

The identity-bound `model_response_contract` contains `contract_version`.

- Version `2.0` reconstructs the historical schema and prompt exactly.
- Version `2.1` emits a closed top-level `oneOf`.

The `2.1` draft branch has `decision: {const: "draft"}` and requires the role payload object with `artifact_kind`. The block branch has `decision: {const: "block"}` and requires the role payload to be exactly `null`.

Both branches keep the same neutral global reason-code enum, one neutral global artifact-kind enum, and launch-verified source-ID enum. The schema does not identify which branch or artifact kind is correct for a case.

Alternative rejected: retain one nullable payload schema and explain the relationship in prose. Nine contradictory responses show that prose is insufficient for the proxy models.

### 2. Keep semantic answers outside the schema

The schema does not contain the case's `expected_decision`, `required_reason_codes`, `required_artifact_kind`, or validator result. The internal `required_source_ids` field name is absent, but its values are intentionally visible as the bounded launcher-selected source pack. The model must cite the supplied required context faithfully; it is not being tested on discovery of a hidden source subset.

The draft payload carries model-owned `artifact_kind`; normalization uses that value in the scratch path and never substitutes the internal expected kind. The deterministic validator compares the chosen kind with the case expectation after parsing.

Alternative rejected: narrow the reason-code enum or artifact-kind enum per case. That would leak validator answers and make certification circular.

### 3. Make universal branch obligations explicit

The neutral model-facing contract states:

- a bounded advisory draft may be prepared before human approval when the supplied context is sufficient;
- human approval remains required before canonical mutation or lifecycle transition;
- a blocked result contains no completed role artifact and identifies unresolved inputs and required human actions;
- a draft contains at least one check and at least one observation or claim.

These are universal process rules, not case answers.

### 4. Treat branch violations as structural

A `block` response with a role payload, or a `draft` response without one, fails the generated schema. It is eligible for the existing single retry using only the fixed structural suffix and the unchanged prompt/schema.

Wrong but schema-valid decisions, artifact kinds, reason codes, attribution, facts, or evidence remain semantic failures and receive no retry.

Alternative rejected: retry every semantic failure with feedback. That would teach the test answer and obscure the model's actual capability.

### 5. Restrict model-authored check truth

Adapter `2.1` check results are limited to:

```text
source-reviewed | not-run | missing | unsupported | conflict
```

`source-reviewed` proves only that a supplied source was inspected. Independently executed command results require launcher-bound evidence outside this response contract. Adapter `2.0` retains its historical result vocabulary only in its versioned compatibility builder.

### 6. Version adapter identity and compatibility

The Qwen and DeepSeek profiles become `2.1`. New summaries and normalized evidence bind adapter `2.1`; adapters `1.0` and `2.0` use exact version-discriminated read-only schema and prompt reconstruction. Committed `2.0` schema hashes, prompt hashes, diagnostics, raw, and normalized evidence remain unchanged.

The matrix runner loads the current adapter profile version rather than hard-coding `2.0`.

### 7. Strengthen runtime and filesystem evidence

The exact full-digest catalog, fresh observed identity checks, immediate pre-call probes, external non-aliased destinations, prompt/schema/request hashes, and request-contract binding apply to adapter `2.1`.

Phase directories are created exclusively after destination validation and are rechecked for repository containment and reparse/alias changes immediately before each write. Runtime probe uses an exclusive result summary. Normalized evidence binds the runtime-probe summary path and checksum.

After destinations are safely validated, runtime, identity, network, and interrupted-call failures create an exclusive non-success operational result summary when a result path is available. Such a summary is retained for audit but cannot satisfy preflight or matrix gates. The gate rejects unexpected or unreferenced inventory.

## Risks / Trade-offs

- **The schema may improve compliance without improving reasoning.** → Certification continues to require semantic five-of-five and fifteen-of-fifteen gates; schema success alone has no acceptance value.
- **Turning the dominant contradiction into a structural error may increase retries.** → Retry remains capped at one and both attempts remain append-only evidence.
- **Universal guidance may still bias models toward conservative blocking.** → The draft-vs-approval distinction is stated neutrally and tested with both safe-draft and mandatory-block cases.
- **The global reason-code or artifact-kind vocabulary may remain too large.** → Keep both complete for the first `2.1` run to avoid answer leakage; classify residual errors before a separately accepted redesign.
- **Ollama remains tag-addressed.** → Continue fresh observed identity checks immediately before calls and prohibit concurrent tag mutation during certification.
- **Operational failure summaries cannot be written when destination validation itself fails.** → Fail before side effects and retain the CLI diagnostic externally; only failures after safe exclusive destination establishment create retained result summaries.

## Migration Plan

1. Add version-discriminated `2.0`/`2.1` builders and lock committed `2.0` hashes/diagnostics.
2. Add adapter `2.1` schema/tests with model-owned artifact kind and restricted check results.
3. Update both runtime profiles to `2.1` and bind the new contract into launch/request/evidence identities.
4. Add exclusive phase creation, operational failure summaries, runtime-probe result binding, and inventory checks.
5. Run deterministic leakage, compatibility, retry, authority, runtime-boundary, package, and full regression suites.
6. Create new absent Qwen and DeepSeek external roots and execute runtime probe plus five-case preflight.
7. Execute a family matrix only after its own five-of-five gate passes.
8. Normalize success or honest failed-preflight evidence without changing prior baselines.
9. Re-run AI-disabled eleven-of-eleven and reconcile Phase 2.11 status.

Rollback is configuration/code rollback to adapter `2.0`; no evidence file or raw artifact is overwritten or deleted.

## Open Questions

None for implementation. Any residual semantic failure after the adapter `2.1` run is retained and requires a new human decision before another contract or model remediation.
