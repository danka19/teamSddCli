## Why

Регулярно используемые workflow-skills доступны только из личного
`~/.codex/skills`, поэтому чистый clone не воспроизводит рабочий процесс
проекта. Репозиторию нужен самодостаточный versioned skill package, который
обнаруживается Codex локально и не требует внешней сети или внешних действий.

## What Changes

- Добавить канонические `teamssd-*` skills в `process/agent-skills/`.
- Добавить отслеживаемую Codex-проекцию в `.agents/skills/`.
- Удалить из repo-local вариантов внешние URL, web/MCP/connectors, remote Git,
  package installation, автоматические PR, публикацию и deployment.
- Добавить короткий README для сопровождения skills и будущих отдельных
  runtime-проекций, например `.gigacode/skills/`.
- Изменить проектное правило о глобальных skills: глобальные личные skills
  разрешены, но не являются зависимостью репозитория.
- По прямому решению владельца не добавлять автоматические или поведенческие
  тесты; сохранить это как явный остаточный риск и выполнить ручную статическую
  проверку.

## Capabilities

### New Capabilities

Нет.

### Modified Capabilities

- `repo-topology-config`: добавить контракт versioned repo-local agent skill
  package, отдельной runtime-проекции и offline-границы.

## Impact

Затрагиваются `process/package.yaml`, новый `process/agent-skills/`,
`.agents/skills/`, `AGENTS.md`, проектная документация, roadmap и инструкции
агентов. Продуктовые CLI/API и внешние интеграции не изменяются.

## Roadmap

Execution phase: P3
Related phases: P4
Lifecycle status: pending_acceptance
