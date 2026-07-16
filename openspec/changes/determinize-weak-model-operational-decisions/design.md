## Context

Adapter `2.1` closed the structural ambiguity between `draft` and `block`.
Qwen then passed 2/5 and DeepSeek 0/5 preflight cases, with all ten responses
schema-valid on attempt 1. The remaining failures are not one homogeneous model
reasoning problem:

- safe draft cases do not define precisely when unresolved detail still permits
  a bounded draft;
- the model sees a global reason-code and artifact-kind vocabulary without
  definitions, but the validator expects exact case-specific values;
- the prompt asks for relevant citations while the validator may require the
  complete launcher-selected source inventory;
- the authority regex examines natural-language human-handoff text and can
  reject safe statements that an authorized human must approve or resume work;
- aggregate `model-adapter.semantic` diagnostics hide which model-visible
  obligation failed.

The supported product goal is safe operational assistance, not autonomous model
interpretation of process policy. The deterministic control plane already owns
workflow state, authority, evidence, and the certification catalog, so it is the
correct owner for decisions that can be derived before generation.

## Goals / Non-Goals

**Goals:**

- Make every supported model task have one explicit action before generation.
- Keep policy, authority, required-source, reason-code, and artifact-routing
  decisions deterministic and reproducible.
- Test the model on bounded content generation, source-grounded claims, and
  evidence honesty.
- Eliminate validator requirements that are hidden from the model or expressed
  only through fragile natural-language heuristics.
- Preserve AI-disabled operation, append-only evidence, exact runtime identity,
  and one structural-only retry.
- Keep documentation proportional: reuse canonical specs and role guides, and
  project only the task-specific rules needed for one operation.

**Non-Goals:**

- Increasing or replacing the model.
- Letting the model choose approvals, lifecycle actions, policy state, or
  canonical writes.
- Adding semantic retries, self-critique chains, voting, agent loops, vector
  search, or a new documentation hierarchy.
- Relaxing source, evidence, privacy, runtime, or human-authority controls.
- Rewriting adapter `1.0`, `2.0`, or `2.1` evidence.

## Decisions

### 1. Add a deterministic operation plan before the model call

The launcher creates an identity-bound plan containing:

```text
action: draft-artifact | explain-block
artifact_kind: <configured kind> | null
reason_codes: <deterministically derived codes>
required_source_ids: <launcher-bound inventory>
human_action_codes: <configured accountable handoff>
content_requirements: <small branch-specific checklist>
```

If policy inputs are missing or contradictory and the deterministic evaluator
cannot select one action, execution fails closed to the named human owner
without calling the model.

Alternative rejected: improve the prompt while leaving the same choices with
the model. The `2.1` evidence shows that exact taxonomy and policy inference,
not JSON syntax, now dominate failures.

### 2. Let the model generate content, not policy metadata

For `draft-artifact`, the model supplies only bounded summary, observations,
claims, and check notes. For `explain-block`, it supplies only a concise
source-grounded explanation of the missing or forbidden condition. Artifact
kind, reason codes, source inventory, and human action codes are copied from the
verified operation plan into normalized evidence.

Model-authored claims still cite allowed source IDs. The model is not asked to
echo every source merely to prove that it read the pack; source inventory is
launcher evidence, while citations are claim evidence.

If the model notices an additional possible gap that is not represented by the
verified operation plan, it may report an advisory finding. That finding cannot
change the planned action or policy metadata; deterministic validation or the
named human owner must disposition it.

Alternative rejected: keep exact reason and artifact selection model-owned as a
proxy for process understanding. That measures taxonomy recall and creates
avoidable operational failure without adding authority or safety.

### 3. Replace broad authority scanning with field-scoped validation

Structured fields continue to prohibit model-owned approval, transition,
resume, release, archive, merge, waiver, and gate decisions. Natural-language
human-handoff descriptions are allowed to name those actions because describing
the required human decision is not claiming it.

Authority-language checks apply only to model-authored claims or artifact
content where the model could impersonate authority. Each rejection returns a
stable field-specific diagnostic.

Alternative rejected: expand the safe-context regex. More phrases would remain
language-order dependent and would continue to create false positives.

### 4. Project one compact task card from canonical sources

The model receives:

- the explicit operation action;
- the relevant facts and bounded source excerpts;
- a short `may do / must not do / stop after` card;
- the branch-specific content schema.

Role guides and OpenSpec remain canonical. The task card is generated input,
not another maintained documentation source. Contrastive examples are deferred
unless the first implementation still fails content grounding after policy
projection.

### 5. Separate operational certification from diagnostic model understanding

The release gate certifies the configured operational path:

- deterministic operation plan is correct;
- model content is schema-valid and source-grounded;
- no evidence or authority is fabricated;
- normalized output exactly preserves launcher-owned policy metadata;
- AI-disabled fallback still passes.

The old adapter `2.1` preflight remains immutable diagnostic evidence that the
models cannot reliably infer the policy unaided. It is not rewritten into a
pass, and no new free-form reasoning benchmark is required for initial
implementation.

### 6. Use risk-weighted ambiguity and acceptance criteria

The system is operationally unambiguous only when:

1. every semantic gate obligation is either explicitly visible in the task card
   or owned by deterministic code;
2. identical verified inputs produce one operation action and one policy
   metadata set;
3. no validator requires an undefined synonym, hidden source subset, or hidden
   artifact mapping;
4. safe human-handoff language cannot be mistaken for model authority;
5. each failure identifies one field and one correction owner;
6. unsafe continuation, fabricated evidence, and model-owned authority have
   zero accepted cases;
7. model failure degrades to deterministic or named-human execution without
   canonical mutation.

## Risks / Trade-offs

- **Less autonomous process reasoning is tested.** → This is intentional for the
  supported operational path; policy remains deterministic and auditable.
- **Operation evaluators add code.** → Implement only predicates already present
  in the frozen certification catalog and supported role flows; unknown cases
  fail to a human rather than growing a general rules engine.
- **A model may still produce poor draft content.** → Keep exact source/claim and
  fabricated-evidence checks, then require 5/5 preflight before the matrix.
- **Mechanically bound sources do not prove model attention.** → Claim-level
  citations remain model-authored and validated; source inventory is correctly
  treated as launcher provenance, not a cognitive claim.
- **The new path can appear to make certification easier.** → Acceptance still
  requires exact deterministic planning, no forbidden claims, grounded content,
  full matrix success, immutable evidence, and AI-disabled regression.

## Migration Plan

1. Record ambiguity findings and freeze adapter `2.1` as the comparison
   baseline.
2. Add the operation-plan schema and deterministic evaluator for the existing
   five preflight cases, with RED tests for all identified ambiguities.
3. Add the smaller branch-specific content schema and field-scoped authority
   validation.
4. Rebuild the frozen twenty-case catalog through operation plans without
   changing its facts or expected safety outcomes.
5. Run deterministic and synthetic tests, then new append-only Qwen and
   DeepSeek preflights; run a family matrix only after 5/5.
6. Re-run AI-disabled 11/11 and reconcile Phase 2.11 from the actual result.

Rollback selects adapter `2.1` code while retaining all new failed or successful
evidence append-only. No prior raw or normalized artifact is deleted.

## Open Questions

None for planning. Implementation must stop and create a new intake record if an
existing certification case cannot be expressed by a small deterministic
predicate without inventing a general policy engine.
