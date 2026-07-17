# Phase 2 Work Item 2.11 Adapter 2.2 Certification Audit

Date: 2026-07-17
Status: passed; work item 2.11 closed
Scope: deterministic operation planning, bounded weak-model content, actual Qwen/DeepSeek certification, and AI-disabled regression

## Result

Adapter `2.2` passed the accepted operational gate without changing either
model. Frozen `qwen3.5:9b` and `deepseek-r1:8b` each passed 5/5 preflight before
their own 15/15 matrix, and each matrix passed 15/15. Every accepted model row
completed on attempt 1. The AI-disabled walkthrough passed 11/11. No accepted
row contained unsafe continuation, fabricated verification, model-owned
authority, canonical mutation, or operation-plan override.

| Family | Frozen identity | Preflight | Matrix | Retry |
|---|---|---:|---:|---:|
| Qwen | `qwen3.5:9b`, digest `6488c96f...93ea7`, Ollama `0.30.11` | 5/5 | 15/15 | 0 |
| DeepSeek | `deepseek-r1:8b`, digest `6995872b...f5763`, Ollama `0.30.11` | 5/5 | 15/15 | 0 |
| AI-disabled | deterministic package `0.2.0` | 11/11 | not applicable | 0 |

Normalized evidence is stored in
`process/certification/evidence/phase-2-11-qwen-adapter-2-2-2026-07-17.yaml`
and
`process/certification/evidence/phase-2-11-deepseek-adapter-2-2-2026-07-17.yaml`.
Their external append-only raw logical roots are
`raw-artifact-v0.2.2-qwen-2026-07-17-certified-policy-v3` and
`raw-artifact-v0.2.2-deepseek-2026-07-17-certified-policy-v9`. The AI-disabled logical
root is `raw-artifact-v0.2.2-ai-disabled-2026-07-17`. Local absolute paths are
not stored in Git.

## What Changed

The launcher now computes an identity-bound operation plan before generation.
It owns the action (`draft-content` or `blocked-summary`), artifact kind, reason
codes, verified source inventory, unresolved inputs, and accountable human
action codes. Unknown or contradictory inputs fail closed before a model call.

The model receives one branch, not a policy choice. A draft response contains
only source-linked observations; a blocked response contains only a concise
summary and an allowed source ID. Trusted normalization attaches the verified
plan metadata mechanically. Adapter `2.0` and `2.1` remain frozen compatibility
paths for historical evidence.

The draft schema makes downstream provenance explicit: at least one
observation must cite a canonical source ID visible in the supplied manifest.
Case facts and supporting sources remain available for their own claims but
cannot silently satisfy the canonical-reference obligation.

Authority validation was narrowed to model-authored content and distinguishes
safe descriptions of pending human action from positive model-owned authority
claims. Positive claims such as model approval or release remain rejected with
the stable `model-adapter.authority-claim` diagnostic.

## Operational Error Analysis

Adapter `2.1` proved that valid JSON was not sufficient: Qwen passed 2/5 and
DeepSeek 0/5 because the model still selected policy disposition, exact reason
codes, source subsets, and artifact routing. Adapter `2.2` removes those
deterministic choices from generation instead of teaching them through a
larger prompt.

Intermediate append-only runs exposed two bounded system problems: an
over-complex draft envelope and false authority positives on negated or
human-boundary phrases. Final critic review additionally caught certification
oracle fields in the first operation-plan implementation and launcher inventory
being reported as model-read provenance. The final evaluator derives policy
from operation facts while ignoring validator expectations; case facts have an
independent hash; and `sources_read` contains only citations actually returned
by the model. The authority corpus accepts observed safe phrases such as
`approved scope` while retaining explicit positive-state and direct-action
rejection. No semantic
retry, self-critique loop, classifier agent, embedding check, expanded reason
taxonomy, generic rules engine, or new role-document hierarchy was added.

## System Clarity Assessment

The supported path is operationally unambiguous at the generation boundary:

- one verified input produces one deterministic branch and byte-stable policy metadata;
- every required model field is present in the supplied response schema;
- source citations are checked against the visible plan inventory;
- the model cannot change action, artifact kind, reason codes, human route, or lifecycle state;
- diagnostics identify schema, source, authority, or plan-identity failure locally.

The strongest property is error containment: weak prose can be rejected or
reviewed without becoming a process decision. The main remaining weakness is
that passing certification proves contract compliance for the frozen catalog,
not factual usefulness or completeness of every future draft.

## Limitations And Residual Risk

- These local models are family-level proxies, not equivalence proof for the corporate runtime.
- Execution was on Windows; Windows/Linux/macOS equivalence belongs to work item 2.12.
- Qwen and DeepSeek were run sequentially. DeepSeek materially loads the workstation; operators should unload the other model first and avoid concurrent test/model work.
- The frozen DeepSeek model advertises a 131072-token maximum, but adapter `2.2`
  bounds the actual request to `num_ctx=8192`. The certification prompts and
  output budget fit that window; this prevents the unnecessary 25 GB runtime
  allocation observed with the maximum context and does not change model
  identity or process semantics.
- The catalog is intentionally finite. Unsupported or contradictory operations fail to the named human rather than being guessed.
- Human review still owns correctness, approvals, waivers, merge, release, archive, risk acceptance, and canonical changes.
- Ollama tag invocation is not digest-addressed; the runner mitigates the observation-to-call race with immediate identity re-probes but cannot eliminate it.

## Verification

- Actual Qwen: 5/5 preflight, then 15/15 matrix.
- Actual DeepSeek: 5/5 preflight, then 15/15 matrix.
- AI-disabled: 11/11.
- Complete project suite after final critic fixes and package reconciliation: `610 passed, 3 skipped`.
- Normalized evidence validates against its exact external raw root and immutable adapter `2.1` baseline reference.

Work item 2.11 is closed and transfer task 4.9 is complete. This does not claim
cross-platform release-candidate acceptance, corporate-runtime equivalence,
Phase 3 adaptation, or pilot acceptance; those remain later gates.
