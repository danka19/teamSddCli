## Why

P3 guided workflow currently allows role-sensitive routes without a known human role and treats a YAML phrase as acceptance evidence. This violates the fail-closed, human-owned transition boundary recorded in `D-024`.

## What Changes

- Add a fail-closed role-aware guided route contract with an explicit Analyst role and role-scoped CTAs.
- Add trusted, revision-bound human acceptance evidence and a deterministic readiness gate that cannot bypass DoR.
- Remove the P3 MCP fallback from guided catalog, runbook, and read-pack while retaining historical and P4 corporate MCP contracts.
- Provide a read-only response summary that binds the shown revision, gate result, and next permitted action.

## Capabilities

### New Capabilities

- `role-aware-guided-workflow`: deterministic role, acceptance, and readiness controls for the P3 guided workflow.

### Modified Capabilities

- `change-lifecycle`: implementation entry requires trusted revision-bound acceptance and a passing DoR/readiness result.
- `traceability-contract`: guided acceptance evidence links the accepted revision, scenario traceability, and deterministic checks.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress

## Impact

Changes the local process-package catalog, guided workflow code and schemas, integrity validator, templates, role/read-pack instructions, runbook, package registry, and focused tests. It adds no network, MCP, credentials, or external mutation.

## Принятые уточнения 2026-07-21

- Добавить двухшаговую карточку решения `DEC-…`: первое естественное решение человека создаёт только карточку, а второе сообщение `Подтверждаю DEC-…` либо короткое `Подтверждаю` в следующем сообщении подтверждает именно показанную карточку.
- Добавить proactive depth recommendation: в режиме `обычно` агент сам выявляет существенные неизвестные и предлагает углубить обсуждение, принять safe defaults либо отложить решение; молчание не является согласием.
- Локальная форма использует тот же confirmation-event contract позже и не входит в P3 implementation.
