## ADDED Requirements

### Requirement: Process package carries operation-dispatch assets
Versioned process package SHALL включать canonical operation catalog, его schema, loader, validator, generated documentation contract и thin dispatcher как shared reusable assets alongside existing scripts and role instructions.

#### Scenario: Bootstrap carries one coherent operation contract
- **WHEN** команда bootstrap'ит поддерживаемый process package
- **THEN** package содержит catalog/validator/dispatcher assets, которые ссылаются только на assets той же package version и не требуют ручного копирования отдельного operation registry
