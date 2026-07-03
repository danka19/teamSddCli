# Agent Operating Guide

This file is the shared entry point for Codex and future agent tools. Keep it short; detailed project context lives in `docs/`.

## Current Mode

- Active implementation agent: Codex.
- Future subagents may be used for bounded worker, reviewer, architecture-checker, and verification-checker tasks when tooling supports them.
- The human owner keeps final CLI/process scope, usability, integration, security, and business-workflow decisions.

## Required Read Order

1. `AGENTS.md`
2. `docs/README.md`
3. `docs/00_FILE_STRUCTURE.md`
4. `docs/ROADMAP.md`
5. `sdd_final_architecture.md` before changing product scope, SDD workflow, CLI behavior, integration boundaries, or roadmap phases.
6. Relevant `docs/phases/PHASE_*.md` when working by roadmap phase.
7. `openspec/` before SDD/OpenSpec workflow changes, CLI behavior changes, process contract changes, or acceptance planning.
8. Relevant `openspec/changes/<change-id>/` folder when working on an active proposed change.
9. `docs/CURRENT_PROJECT_AUDIT.md` before trusting existing implementation or setup state.
10. `docs/AI_STEP_VERIFICATION_CHECKLIST.md` before implementation, verification, or completion reporting.
11. Only topic documents related to the current task.

## Project Rules

1. Quality, thoughtful design, safety, and architecture are more important than rushing.
2. Project documentation must be written in English unless the human explicitly changes the project language.
3. User-facing replies must be written in Russian unless the user explicitly asks for another language.
4. The source architecture document is currently Russian; preserve its meaning and do not translate or rewrite it unless explicitly asked.
5. At the end of every work session, before replying to the user, create a git commit when the project repository has intentional changes and `.git/` exists.
6. After completing work, update documentation if the change affects CLI behavior, SDD workflow behavior, architecture, setup, operations, security, roadmap status, process contracts, or user-visible command/help text.
7. If work follows roadmap steps, verify before changes that the current branch matches the active roadmap phase when the project is a git repository.
8. User-facing reports must include: task, what was done, decisions and judgments, important details, project changes, end-user changes, checks, manual verification, manual-verification risks, skills used, and subagents used with role names and token counts when available.
9. Reports must be self-contained enough that the human understands the result without opening changed files.
10. Treat human feedback as durable project knowledge. Persist product rules, rejected behavior, acceptance criteria, verification habits, and open decisions in the correct docs.
11. Before implementation, map affected OpenSpec requirements or change deltas to acceptance scenarios and verification evidence for the relevant CLI command, workflow transition, integration, or artifact schema. If automated tests do not exist, record manual verification steps and residual risk.
12. When the next project step requires a human decision or mandatory verification, say so explicitly and explain why it matters, relevant options or tradeoffs, expected evidence, and the consequence or risk of leaving it unresolved.
13. User-facing reports must always include next steps. If there is no active required action, state the recommended next step and why it is next.
14. When the human asks for advice, asks "how is it better", asks a conceptual question, or asks for an opinion/recommendation, answer with a detailed explanation first and do not silently convert the question into implementation. Make changes only when the human explicitly asks to record, implement, update, or continue work, or when the question is inseparable from a requested documentation update.
15. When several open questions or decisions remain, ask them in one clear batch with recommended defaults and tradeoffs. Ask one-by-one only when a single answer is required to safely proceed.

## User-Facing Report Style

- Final reports must be more detailed than a terse status note when work involved decisions, tradeoffs, verification, documentation, architecture, or code changes.
- Use clear Markdown section headers in Russian so the answer does not read as one plain-text block.
- Prefer Russian section headers equivalent to: Task, What was done, Decisions and judgments, Important details, Project changes, End-user changes, Checks, Manual verification, Risks and limitations, Documentation, Commit, Skills, Subagents, and Next step.
- In the Decisions and judgments section, explain why the chosen path was taken, what alternatives were implicitly rejected, and what assumptions mattered.
- In the Important details section, call out constraints, safety rules, branch state, remote-deployment status, data/privacy boundaries, and anything the human should remember later.
- Do not hide ambiguity. If documentation is missing, stale, contradictory, or only partially verified, state that in its own block and update the relevant durable document when appropriate.
- Always include a `Next step` section in substantive final reports. For quick no-change answers, include at least a concise next-step sentence.
- If the human asked for a recommendation or "what is better", the answer must compare the practical options, give the recommended path, explain tradeoffs and risks, and clearly separate advice from any actions taken.

## Project-Local Skills

- For architecture planning, use `.codex/skills/architecture-planner/`.
- For new ideas, fixes, scope changes, architecture notes, artifact/process contract changes, integration changes, or verification requests that appear during an active phase, use `.codex/skills/phase-change-intake/` before changing the plan.
- For phase planning, use `.codex/skills/phase-planner/`.
- For one phase work item at a time, use `.codex/skills/phase-step-runner/`.
- For full phase execution with worker/reviewer/checker roles, use `.codex/skills/phase-full-runner/`.
- At the start of planning or phase execution work, state which project-local skill is being used and why.
- When creating a phase implementation plan, follow `docs/phases/PHASE_PLAN_TEMPLATE.md`.
- Planning from `docs/ROADMAP.md` alone is forbidden.
- OpenSpec artifacts under `openspec/` are the source of truth for accepted/proposed `sdd CLI` behavior, SDD workflow requirements, artifact contracts, and acceptance criteria.
- Documentation governance and TDD-style verification rules should live in `openspec/specs/documentation-governance/spec.md` once that spec exists.
- New feedback during a phase must be routed as adopt now, queue current phase, create OpenSpec change, defer, or reject before it changes active scope.
- For SDD/OpenSpecs work, run `openspec list`, `openspec list --specs`, and `openspec validate --all --strict` before completion when relevant.

## Product Direction

- The project is a local SDD automation CLI/process toolkit for team workflows.
- The target architecture is OpenSpec/Markdown-first: Git/OpenSpec is canonical, Confluence is generated publication, Jira/tracker is workflow/status, Bitbucket PR is review/audit, and Jenkins is validation/automation.
- The central domain object is a `change package` under `team-specs/openspec/changes/<change-id>/`.
- The CLI should automate state transitions between artifacts rather than act as one autonomous central agent.
- AI tools are local assistants that generate drafts, checks, context packs, and skeletons; humans keep decisions, approvals, merges, and correctness ownership.

## Branching Guidance

For roadmap work, use a branch whose name clearly identifies the phase or workstream, for example:

```text
phase-0/project-foundation
phase-1/sdd-requirements
phase-2/cli-architecture
phase-3/change-flow-pilot
```

If a task does not belong to a roadmap step, use a short descriptive branch. Use `main` only for stable integration or initial repository setup.

## Secrets And Config

- Credential and secret values must live in local-only files ignored by git.
- The default local secret file is `.env.local`.
- Keep `.env.example` in git as the documented template with placeholders only.
- Never commit API keys, corporate project exports, production credentials, private specs, tracker dumps, Confluence exports, database dumps, or generated local context packs that may contain internal data.

## Command Execution Rules

- Always run shell commands with explicit timeouts where the tool supports them.
- Prefer non-interactive commands.
- For commands that can produce large output, inspect focused output instead of flooding the conversation.
- If a command appears blocked, stop it, record the exact command and blocker, then retry narrower or report the required human action.

## Before Claiming Work Is Done

- Run the narrowest meaningful verification command.
- If verification cannot run, record the exact command and blocker.
- Verify that documentation is still correct and complete for the task.
- Create a git commit before replying when the repository has intentional changes and local rules require commits.
