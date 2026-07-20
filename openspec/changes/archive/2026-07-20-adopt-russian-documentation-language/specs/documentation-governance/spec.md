## MODIFIED Requirements

### Requirement: Canonical language and localized generated views
The SDD process SHALL keep Russian as the canonical language for newly created
project documentation and OpenSpec requirement/scenario prose, while preserving
technical tokens required for stable references and tooling.

#### Scenario: New documentation and specs use Russian prose
- **WHEN** an analyst or another project participant creates a new requirement,
  scenario, proposal, design, task list, runbook, audit, or project document
- **THEN** its human-readable prose is written in Russian; stable IDs, file
  paths, CLI/API tokens, and structural OpenSpec keywords (`Requirement`,
  `Scenario`, `SHALL`, `WHEN`, `THEN`) remain English where tooling or a stable
  cross-reference requires them

#### Scenario: Historical evidence is preserved without bulk translation
- **WHEN** a historical accepted artifact, immutable release candidate, raw
  evidence, or checksum-bound document is encountered
- **THEN** it is preserved as historical evidence and is not translated in bulk;
  a later substantive change follows the normal OpenSpec/change workflow

#### Scenario: Generated view follows the canonical Russian source
- **WHEN** a Confluence or other generated view is created for readers
- **THEN** it uses the Russian canonical Git/OpenSpec source and links back to
  that source rather than creating a separate translated requirement authority

#### Scenario: Feedback changes the Russian canonical source
- **WHEN** feedback on documentation or a generated view changes accepted or
  proposed behavior
- **THEN** the change is recorded in the canonical Russian Git/OpenSpec source
  through the applicable approval workflow rather than as an untracked manual
  translation
