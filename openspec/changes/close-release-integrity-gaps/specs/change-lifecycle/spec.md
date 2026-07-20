## MODIFIED Requirements

### Requirement: Archive history convention
The SDD process SHALL enforce a deterministic, human-authorized archive history convention for changes archived into accepted specs.

#### Scenario: Archive uses dated history path
- **WHEN** a change package passes deterministic archive readiness and an explicit human archive-approval record authorizes the local archive operation for a stated date
- **THEN** the operation moves the change only to `openspec/changes/archive/YYYY-MM-DD-<change-id>` or an explicitly configured OpenSpec-compatible dated equivalent and rejects collisions, already archived sources, or paths outside the archive root

#### Scenario: Archive commit is greppable
- **WHEN** archive movement is prepared or its result is validated
- **THEN** the operation emits and the validator accepts only the stable commit subject `spec: archive <change-id>` for that archived change

#### Scenario: Archive convention does not replace approval
- **WHEN** the archive path and commit grammar are satisfied
- **THEN** the operation still requires final deterministic checks and an explicit human archive-approval record and does not create approval, commit, merge, release, or deployment authority
