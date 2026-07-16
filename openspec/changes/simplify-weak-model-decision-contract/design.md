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

The adapter must reduce representational ambiguity without converting the certification schema into an answer key. Expected decisions, case-specific reason codes, required artifact kinds, and validator results remain launcher-internal.

## Goals / Non-Goals

**Goals:**

- Make `draft` and `block` mutually exclusive structural branches selected by the model's own `decision`.
- Make a completed role artifact structurally impossible on the `block` branch.
- Require meaningful draft evidence and meaningful block disposition without case-specific answer leakage.
- Clarify that human approval is required for canonical transition, not for preparation of a bounded non-canonical advisory draft.
- Preserve semantic validation of decision, reason codes, sources, evidence truth, and role output kind.
- Preserve one structural retry, immutable evidence, exact observed runtime identity, external raw destinations, and adapters `1.0`/`2.0` compatibility.
- Re-run Qwen and DeepSeek in new adapter `2.1` artifact roots and keep each matrix gated by five-of-five preflight.

**Non-Goals:**

- Deterministically selecting the decision for the model.
- Exposing case-specific expected decisions, reason codes, required sources, or artifact kind.
- Adding semantic retries, critique prompts, chain-of-thought inspection, or automatic response correction.
- Weakening authority, safety, source, evidence, runtime-identity, privacy, or canonical-write controls.
- Rewriting the 2026-07-15 or 2026-07-16 raw and normalized evidence.
- Certifying a model on anything less than five-of-five preflight and fifteen-of-fifteen matrix for its exact observed identity.

## Decisions

### 1. Use a decision-discriminated schema

`build_role_response_schema()` will emit a closed top-level `oneOf`:

- the `draft` branch has `decision: {const: "draft"}` and requires the role payload object;
- the `block` branch has `decision: {const: "block"}` and requires the role payload to be exactly `null`.

Both branches keep the same neutral global reason-code enum and launch-verified source-ID enum. The schema does not identify which branch is correct for a case.

Alternative rejected: retain one nullable payload schema and explain the relationship in prose. Nine contradictory responses show that prose is insufficient for the proxy models.

### 2. Keep semantic answer fields out of the schema

The schema will not contain the case's `expected_decision`, `required_reason_codes`, `required_source_ids`, or `required_artifact_kind`. Those remain in the certification orchestrator and deterministic validator. The model still has to infer the correct decision from facts and canonical source excerpts.

Alternative rejected: narrow the reason-code enum or artifact kind per case. That would leak validator answers and make certification circular.

### 3. Make universal branch obligations explicit

The neutral model-facing contract will state:

- a bounded advisory draft may be prepared before human approval when the supplied context is sufficient;
- human approval remains required before canonical mutation or lifecycle transition;
- a blocked result contains no completed role artifact and must identify unresolved inputs and required human actions;
- a draft must include at least one check and at least one observation or claim.

These are universal process rules, not case answers.

### 4. Treat decision-branch violations as structural

A `block` response with a role payload, or a `draft` response without one, fails the generated schema. It is eligible for the existing single retry using only the fixed structural suffix and the unchanged prompt/schema.

Wrong but schema-valid decisions, reason codes, sources, facts, or evidence remain semantic failures and receive no retry.

Alternative rejected: retry every semantic failure with feedback. That would teach the test answer and obscure the model's actual capability.

### 5. Version adapter identity and evidence

The Qwen and DeepSeek profiles become `2.1`. New summaries and normalized evidence bind adapter `2.1`; adapters `1.0` and `2.0` remain read-only compatibility formats. Raw destinations use new versioned logical IDs and are never reused.

### 6. Keep runtime and filesystem controls unchanged

The exact full-digest catalog, fresh observed identity checks, immediate pre-call probes, external non-aliased destinations, exclusive creation, prompt/schema hashes, and request-contract binding apply unchanged to adapter `2.1`.

## Risks / Trade-offs

- **The schema may improve compliance without improving reasoning.** → Certification continues to require semantic five-of-five and fifteen-of-fifteen gates; schema success alone has no acceptance value.
- **Turning the dominant contradiction into a structural error may increase retries.** → Retry remains capped at one and both attempts remain append-only evidence.
- **Universal guidance may still bias models toward conservative blocking.** → The draft-vs-approval distinction is stated neutrally and tested with both safe-draft and mandatory-block cases.
- **The global reason-code vocabulary may remain too large for weak models.** → Keep it unchanged for the first `2.1` run to avoid answer leakage; classify residual errors before considering a separately accepted vocabulary redesign.
- **Ollama remains tag-addressed.** → Continue fresh observed identity checks immediately before calls and prohibit concurrent tag mutation during certification.

## Migration Plan

1. Add adapter `2.1` schema/tests while preserving `1.0`/`2.0` readers.
2. Update both runtime profiles to `2.1` and bind the new contract into launch/request/evidence identities.
3. Run deterministic leakage, compatibility, retry, authority, runtime-boundary, package, and full regression suites.
4. Create new absent Qwen and DeepSeek external roots and execute runtime probe plus five-case preflight.
5. Execute a family matrix only after its own five-of-five gate passes.
6. Normalize success or honest failed-preflight evidence without changing prior baselines.
7. Re-run AI-disabled eleven-of-eleven and reconcile Phase 2.11 status.

Rollback is configuration/code rollback to adapter `2.0`; no evidence file or raw artifact is overwritten or deleted.

## Open Questions

None for implementation. Any residual semantic failure after the adapter `2.1` run is retained and requires a new human decision before another contract or model remediation.
