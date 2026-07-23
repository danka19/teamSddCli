## Context

The product is currently documented through specialist runbooks, OpenSpec artifacts and evidence packages. They are authoritative for implementation, but not an approachable orientation layer. The FAQ must provide a stable entry point without creating a competing source of truth for workflow policy or requirements.

## Goals / Non-Goals

**Goals:** a concise start page; linked FAQ pages; role-oriented first-run guides; plain-language roadmap; complete AI usage rules; tested navigation; and canonical references to OpenSpec and runbooks.

**Non-Goals:** duplicating every OpenSpec requirement, publishing to Confluence, replacing training, inventing corporate integration behavior, or representing an unfinished future capability as available.

## Decisions

- Use a documentation hub plus short focused pages, rather than one monolithic guide. The hub is the only required entrypoint and links to concepts, setup, roles, daily workflow, AI, troubleshooting and roadmap.
- Write the FAQ in plain Russian. Keep command tokens, IDs and file paths in English where they are executable or stable.
- Treat the FAQ as an orientation/operating view. Each policy-sensitive assertion links to the canonical OpenSpec requirement, process catalog or detailed runbook rather than copying it.
- Include an explicit “available now / planned / intentionally blocked” status table. This prevents the FAQ from overstating automation readiness.
- Put AI guidance on its own page and distinguish: AI can read context, invoke allowed `sdd` commands and prepare drafts; AI cannot grant authority, infer missing facts, bypass gates, execute forbidden mutations or replace human acceptance.
- Treat the accepted `add-self-service-operator-onboarding` change as the canonical CLI source: setup pages use `sdd setup`, situation pages use `sdd start`, continuation pages use `sdd next`, and every command example identifies whether it is human-readable or `--json` for an AI caller.

## Risks / Trade-offs

- [Pages drift from contracts] → add a deterministic link/content coverage check and require canonical references.
- [Too much detail recreates the existing docs] → keep the hub and FAQ answer-oriented; link to detailed sources.
- [Too little detail leaves first-time users blocked] → every role page includes prerequisites, first command, expected result and escalation/fallback.
- [AI wording implies autonomy] → use an explicit permission matrix with positive and prohibited examples.
- [Documentation gets ahead of shipped CLI] → cite only the accepted `sdd` command set and label later external/release automation as intentionally blocked.

## Migration Plan

1. Add the hub and focused pages while preserving existing runbook URLs.
2. Link legacy README/runbooks to the hub instead of deleting specialist evidence.
3. Validate links and role/AI question coverage.
4. Update the plain-language roadmap after each accepted capability change through the same documentation governance process.
