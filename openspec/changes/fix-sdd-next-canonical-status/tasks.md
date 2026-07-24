## 1. Producer-consumer regression

- [ ] 1.1 Replace handcrafted `lifecycle_state` continuation fixtures with a real schema-v2 `create_change -> sdd next` test and observe the expected RED failure.
- [ ] 1.2 Add fail-closed negatives for a file containing only `lifecycle_state` and for an unsupported canonical `status`.

## 2. Canonical status adapter

- [ ] 2.1 Make `sdd next` read only top-level `status`, preserve guided catalog validation and return a status-specific blocker when the field is absent.
- [ ] 2.2 Verify role-aware continuation, exact next command, and both no-mutation flags on the real created package.

## 3. Documentation and walkthrough

- [ ] 3.1 Remove the temporary `status`/`lifecycle_state` limitation from affected FAQ pages and document canonical `status` behavior.
- [ ] 3.2 Run the real first-change continuation smoke and update the FAQ acceptance evidence and blocked task status.

## 4. Completion gates

- [ ] 4.1 Run focused dispatcher/self-service/FAQ tests and the full relevant regression suite.
- [ ] 4.2 Run FAQ validation, strict OpenSpec validation, roadmap/OpenSpec validation and diff checks; record residual warnings without inferring human acceptance.
