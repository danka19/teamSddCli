---
name: teamssd-subagent-driven-development
description: Use when an approved plan contains multiple independent local tasks with declared dependencies and non-overlapping write scopes.
---

# Subagent-Driven Development

Classify task risk, declare dependencies, owner and write scope, and dispatch
only truly independent work. Each result needs its own local evidence. Review
medium/high-risk changes and run one combined integration check after all
accepted results are assembled.

Subagents may read and edit only the shared local workspace placed in scope.
They must not browse, use connectors, mutate remote Git, publish or deploy.
Human approval and risk acceptance never transfer to a subagent.
