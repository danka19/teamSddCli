## MODIFIED Requirements

### Requirement: Delta Spec operation vocabulary
The artifact contract SHALL define and the deterministic change validator SHALL enforce a reviewable Delta Spec operation vocabulary against the accepted capability baseline.

#### Scenario: Added delta introduces new behavior
- **WHEN** a Delta Spec uses `ADDED` for a requirement, scenario, artifact section, or typed record
- **THEN** deterministic validation confirms that the named behavior does not already exist in the accepted baseline and that the delta includes enough requirement/scenario text for a reviewer to understand the proposed final behavior

#### Scenario: Removed delta includes reason and migration
- **WHEN** a Delta Spec uses `REMOVED` for an existing requirement, scenario, artifact section, or typed record
- **THEN** deterministic validation requires the removed item to exist and requires explicit removal reason plus migration, replacement, or no-replacement evidence

#### Scenario: Rename does not hide content change
- **WHEN** a Delta Spec uses `RENAMED` for a requirement, scenario, file, section, or typed record
- **THEN** deterministic validation accepts only an explicit old-name/new-name mapping and rejects embedded behavior or content changes unless they are represented by `MODIFIED` or an explicit remove/add pattern
