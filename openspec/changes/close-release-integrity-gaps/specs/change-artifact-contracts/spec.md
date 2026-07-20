## MODIFIED Requirements

### Requirement: Delta Spec operation vocabulary
The artifact contract SHALL define a reviewable Delta Spec operation vocabulary and the deterministic change validator SHALL enforce its requirement-level `ADDED`, `MODIFIED`, `REMOVED`, and `RENAMED` sections against the accepted capability baseline. Scenario, artifact-section, and typed-record content remains inside the complete requirement block and under its existing schema, traceability, and review checks; it is not treated as a separate OpenSpec operation target.

#### Scenario: Added delta introduces new behavior
- **WHEN** a Delta Spec uses `ADDED Requirements`
- **THEN** deterministic validation confirms that the named behavior does not already exist in the accepted baseline and that the delta includes enough requirement/scenario text for a reviewer to understand the proposed final behavior

#### Scenario: Removed delta includes reason and migration
- **WHEN** a Delta Spec uses `REMOVED Requirements`
- **THEN** deterministic validation requires the removed item to exist and requires explicit removal reason plus migration, replacement, or no-replacement evidence

#### Scenario: Rename does not hide content change
- **WHEN** a Delta Spec uses `RENAMED Requirements`
- **THEN** deterministic validation accepts only an explicit old-name/new-name mapping and rejects embedded behavior or content changes unless they are represented by `MODIFIED` or an explicit remove/add pattern
