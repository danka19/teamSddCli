## ADDED Requirements

### Requirement: Versioned repo-local agent skill package
The SDD process SHALL provide a versioned repo-local package of project workflow
skills whose canonical source is part of the process package and whose runtime
projections do not depend on personal global skill directories.

#### Scenario: Clean clone exposes Codex skills
- **WHEN** Codex opens a clean clone of the repository
- **THEN** `.agents/skills/` exposes uniquely named `teamssd-*` skills whose complete instructions and required local files are present in the clone

#### Scenario: Canonical source and Codex projection are separate
- **WHEN** a maintainer changes a project workflow skill
- **THEN** the canonical edit is made under `process/agent-skills/` and the tracked `.agents/skills/` projection is refreshed without an untracked manual fork

#### Scenario: Another runtime needs an adapter
- **WHEN** another supported agent runtime requires a directory such as `.gigacode/skills/`
- **THEN** it receives a separate reviewed runtime projection while the canonical tool-agnostic skill remains under `process/agent-skills/`

### Requirement: Offline agent skill boundary
Repo-local workflow skills MUST operate on local repository state and MUST stop
before network access, external integration access, remote Git mutation, package
installation, publication, deployment, or another external-state change.

#### Scenario: Workflow reaches an external action
- **WHEN** a repo-local skill reaches a step that would require web, MCP, a connector, remote Git, PR creation, package installation, publication, or deployment
- **THEN** it reports the required human or separately authorized action and does not execute the external operation

#### Scenario: Skill resolves its dependencies
- **WHEN** a repo-local skill invokes another workflow skill or reads supporting instructions
- **THEN** it uses a `teamssd-*` skill or a repo-local relative path and does not require `~/.codex/skills`

#### Scenario: Owner accepts manual-only verification
- **WHEN** this initial repo-local skill package is prepared
- **THEN** documentation records that automated and behavioral tests were explicitly excluded by the owner, manual static inspection is performed, and behavioral interpretation remains a residual risk
