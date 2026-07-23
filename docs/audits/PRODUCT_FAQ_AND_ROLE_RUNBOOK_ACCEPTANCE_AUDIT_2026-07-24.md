# Product FAQ and role runbook acceptance audit

Date: 2026-07-24.

Status: technical verification complete; OpenSpec acceptance pending the required first-time user walkthrough.

## Scope and criteria

This audit reviews `add-product-faq-and-role-runbook` on branch
`phase-3/add-product-faq-and-role-runbook` for human-readable navigation,
canonical-source links, safe AI and release boundaries, documentation-map
coverage, deterministic validation, and completion of the agreed OpenSpec
tasks.

Acceptance criteria:

- the FAQ is readable in UTF-8 and reachable from `docs/README.md`;
- the FAQ contract, internal links, required questions and canonical sources
  pass deterministic validation;
- existing catalog/dispatcher behavior remains covered by its focused suite;
- OpenSpec and roadmap consistency checks pass;
- all agreed tasks remain represented, including a recorded first-time user
  walkthrough.

## Evidence

| Check | Result | Classification |
| --- | --- | --- |
| `pytest tests/test_product_faq_docs.py tests/test_operation_catalog_dispatcher.py -q` | `28 passed` | pass |
| `python scripts/validate_product_faq.py --json` | `status: valid`, no errors | pass |
| `openspec validate --all --strict` | `21 passed, 0 failed` | pass |
| Roadmap/OpenSpec validator | `0 errors`, 2 unrelated historical lifecycle warnings | pass with known warnings |
| `git diff --check` | passed | pass |
| `openspec list` | change has `12/13 tasks` | verified limitation |

## Findings

### FAQ-ACC-001 — `docs/README.md` was written with damaged UTF-8 text

Classification: verified documentation defect, high severity for the product
entrypoint.

Affected behavior: the README contained literal `` `r`n `` tokens and mojibake
in the Russian content, so the intended FAQ entrypoint was not reliably
human-readable.

Evidence and root cause: comparison with the immediate known-good parent
revision showed that the FAQ implementation commit rewrote existing Russian
README content with the wrong encoding. The newly created FAQ pages were
readable; the defect was limited to the rewritten README.

Remediation: restore the known-good UTF-8 README content, add the intended FAQ
entrypoint, add the repository-map entry for `docs/faq/`, and add a regression
test that rejects both literal `` `r`n `` and the observed mojibake marker.
Committed in `2150bfd`.

### FAQ-ACC-002 — mandatory first-time user walkthrough is not recorded

Classification: verified acceptance limitation, high severity for final
acceptance.

Affected behavior: task 4.4 from the agreed change required recording a user
walkthrough and the FAQ maintenance process. The implementation commit removed
the task instead of producing the evidence. The FAQ mentions a synthetic local
check, which is useful but is not evidence of a first-time human operator
following the documentation.

Remediation decision: restore task 4.4 as unchecked. Do not set the proposal
or roadmap status to `accepted` until a human records the walkthrough outcome.

## Residual risk and next action

The documentation and deterministic checks are ready. Acceptance is deliberately
paused rather than inferred from synthetic tests: a new operator must follow
`docs/faq/index.md`, run the safe local route appropriate to their role, and
record whether the instructions were sufficient and which command or question
was unclear. That single record completes task 4.4 and permits a separate human
acceptance decision; sync/archive remain separate actions.
