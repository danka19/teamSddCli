## 1. Role and acceptance contract

- [x] Define the role-aware proposal, design, and acceptance scenarios linked to `D-024` and `D-026`.
- [x] Add failing focused tests for unknown role, Analyst CTA, untrusted UI response, revision mismatch, and DoR preservation.
- [x] Implement the catalog/schema/module role gate, trusted evidence schema/template, summary, and readiness validator.
- [x] Synchronize role/read-pack/GigaCode instructions and remove only the P3 MCP fallback.

## 2. Verification and package integration

- [x] Register assets in package manifest, run focused tests, and execute a synthetic GigaCode/AI-disabled walkthrough.
- [x] Update roadmap, phase plan, audit intake, and package/version documentation without claiming human acceptance.

## 3. Human-confirmed chat decisions and proactive discovery

- [x] Define typed `decision_draft` and immutable confirmation-event schemas, including card code, change/revision binding, two verbatim messages, expiry and trusted chat-event reference.
- [x] Add failing tests that natural decision text only creates a card; exact/short active-card confirmation records it; `что дальше?`, `Да`, `продолжай`, stale code and interleaved messages cannot record authority.
- [x] Implement deterministic card creation/confirmation and derive summary status from validated records; prohibit AI-authored acceptance/DoR/lifecycle claims.
- [x] Add discovery-map contract and tests for `обычно`: relevant material unknowns trigger proactive depth recommendation, explicit default/defer choices are recorded, and silence remains unresolved.
- [x] Synchronize schemas, templates, validator, package manifest, root/GigaCode instructions, read-packs, runbook, phase plan and sandbox transfer guidance.
- [x] Run focused/final relevant tests, OpenSpec/roadmap gates, one AI-disabled transcript walkthrough, and package update pre-transfer check; perform the real update and separate sandbox commit only in P3.3 after both P3 changes are human accepted.

## 4. Operation-confirmation contract extension

- [ ] Define the operation-confirmation request/event schemas and canonical role/operation/input/revision/expiry binding semantics without changing v1 decision evidence.
- [ ] Add failing tests for missing, role/operation/input/revision mismatch, expiry, altered argv, and proof that a valid event never enables `sdd run` or `mutate_external`.
- [ ] Implement deterministic request/event builders and validators; extend `sdd request` to emit only a non-authoritative operation confirmation request.
- [ ] Register assets and synchronize package/read-pack/GigaCode/runbook/phase/audit documentation without claiming execution authority.
- [ ] Run focused/final relevant tests, OpenSpec/roadmap gates, AI-disabled request walkthrough, and final security review; prepare the exact final human acceptance packet.
