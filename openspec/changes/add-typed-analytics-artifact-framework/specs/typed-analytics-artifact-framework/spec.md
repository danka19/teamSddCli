## ADDED Requirements

### Requirement: Typed analytics package
The process package SHALL provide typed YAML schemas, templates, and deterministic validation for analytics manifest, status model, channel support, data model, platform services, journey, screens/assets, and integration descriptors.

#### Scenario: Complete typed package validates
- **WHEN** a sanitized package contains all eight fixed-name artifacts with valid IDs and required fields
- **THEN** local validation SHALL return valid without mutation or network access

#### Scenario: Manifest misses an artifact
- **WHEN** a manifest omits a required typed artifact
- **THEN** validation SHALL return `analytics.manifest-incomplete`

### Requirement: Stable analytics traceability
Typed journey and screen records SHALL reference stable requirement and scenario IDs; screen records SHALL retain a stable asset path and source metadata.

#### Scenario: Screen remains traceable
- **WHEN** a screen record is rendered in a local preview
- **THEN** its stable screen ID, asset path, source, requirement IDs, and scenario IDs SHALL remain visible

### Requirement: Passive integration boundary
P3 integration descriptors SHALL represent Jira, Confluence, Bitbucket, and Jenkins only as passive stable references with manual evidence points.

#### Scenario: Preview never invokes integration
- **WHEN** a local preview reads integration descriptors
- **THEN** it SHALL return no integration actions and SHALL report `external_state_mutated: false`

### Requirement: Local P3 preview boundary
The P3 package SHALL provide deterministic read-only preview for analytics, screens, and integrations without creating product payment screens or generated corporate views.

#### Scenario: Synthetic analytics walkthrough
- **WHEN** the sanitized example is validated and previewed with AI disabled
- **THEN** the output SHALL show typed artifacts only and SHALL not request MCP, credentials, or live integration configuration
