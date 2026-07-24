---
name: teamssd-using-git-worktrees
description: Use before implementation when branch or workspace isolation must be checked or created locally.
---

# Using Git Worktrees

Inspect Git directory, common directory, superproject and current branch. Reuse
a matching isolated worktree. Otherwise use the project-declared worktree
location, verify it is ignored and create a local branch/worktree from the
available stable local branch.

Do not fetch, pull, clone or install dependencies. If the required base or
dependencies are unavailable locally, report the blocker. Run only existing
local baseline checks authorized by the task.
