## 1. Proposal Draft

- [x] 1.1 Draft lifecycle proposal, design, tasks, and spec delta.
- [x] 1.2 Reference work item 1.1 commit evidence where relevant.
- [x] 1.3 Keep the proposal as proposed behavior only.
- [x] 1.4 Add explicit allowed-transition table and negative skipped-state/archive-approval scenarios from reviewer feedback.
- [x] 1.5 Clarify that generated Confluence views may display lifecycle/approval/testing state but do not own approval or transition truth.

## 2. Later Decision And Implementation

- [ ] 2.1 Review lifecycle states during the Phase 1 acceptance readiness review.
- [x] 2.2 Decide whether accepted specs use the simpler public lifecycle names or the more explicit internal `in_implementation` / `ready_to_archive` split. Decided 2026-07-06: the internal six-state split is canonical for accepted specs and deterministic validation; simplified names appear only in generated business-facing views.
- [ ] 2.3 Decide which lifecycle transitions become deterministic validator or CI gates.
- [ ] 2.4 Do not archive this change until the final human OpenSpec archive gate.
