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
- [ ] Add failing tests that natural decision text only creates a card; exact/short active-card confirmation records it; `что дальше?`, `Да`, `продолжай`, stale code and interleaved messages cannot record authority.
- [x] Implement deterministic card creation/confirmation and derive summary status from validated records; prohibit AI-authored acceptance/DoR/lifecycle claims.
- [ ] Add discovery-map contract and tests for `обычно`: relevant material unknowns trigger proactive depth recommendation, explicit default/defer choices are recorded, and silence remains unresolved.
- [x] Synchronize schemas, templates, validator, package manifest, root/GigaCode instructions, read-packs, runbook, phase plan and sandbox transfer guidance.
- [ ] Run focused/final relevant tests, OpenSpec/roadmap gates, one AI-disabled transcript walkthrough, package update check/update and separate source/sandbox commits.
