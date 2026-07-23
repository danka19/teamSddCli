## ADDED Requirements

### Requirement: Self-service topology bootstrap
The supported central `team-specs` topology SHALL define a self-service bootstrap path that validates package/config compatibility and creates only the declared local workspace after explicit human confirmation.

#### Scenario: New team adopts the supported topology
- **WHEN** a team runs the supported `sdd setup` route with a valid package and destination
- **THEN** it receives a coherent central workspace and a project-adapter next step without copying the framework source repository
