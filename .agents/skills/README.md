# Repo-Local Agent Skills

`process/agent-skills/` is the canonical, editable source. `.agents/skills/` is
the tracked Codex discovery projection and must match it exactly.

These skills work with repository files, local Git, local project commands and
OpenSpec. They stop before network access, connectors, remote Git, package
installation, PR creation, publication or deployment.

To change a skill:

1. Edit its canonical `process/agent-skills/teamssd-*/SKILL.md`.
2. Copy the complete directory to `.agents/skills/`.
3. Compare the canonical and projected file hashes.
4. Record any remaining manual risk in the session report.

Another runtime must use its own reviewed projection, for example
`.gigacode/skills/`. Keep runtime-specific syntax in that projection and keep
the canonical skill tool-agnostic. Do not create an empty adapter directory or
claim support before its format is verified.

Automated and behavioral tests were excluded from the initial package by the
owner. Static inspection does not prove identical interpretation by every
agent and does not replace a runtime network sandbox.
