## ADDED Requirements

### Requirement: User-facing documentation is a governed view
The project SHALL maintain product FAQ and role runbooks as user-facing views that link to canonical OpenSpec requirements, operation catalog records and detailed runbooks for policy-sensitive claims. They SHALL identify their generated or maintained status and SHALL NOT independently redefine lifecycle, authority, validation or integration rules.

#### Scenario: FAQ references a governed policy
- **WHEN** a FAQ page describes a mandatory gate, role boundary or unavailable integration
- **THEN** it links to the applicable canonical contract or runbook and does not contain a conflicting duplicate rule
