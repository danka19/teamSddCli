## ADDED Requirements

### Requirement: Canonical operator continuation result
The dispatcher SHALL expose one canonical continuation result for `start` and `next` that carries the selected situation or change, current state, missing facts, role owner, human-decision boundary, fallback and exactly one next public command.

#### Scenario: Terminal and JSON render the same route
- **WHEN** a supported route is requested in human and JSON formats
- **THEN** both formats describe the same action, role, boundary and command without independently maintained routing text
