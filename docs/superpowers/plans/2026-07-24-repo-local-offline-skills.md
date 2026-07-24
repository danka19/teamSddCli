# Repo-Local Offline Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить самодостаточный versioned набор регулярно используемых workflow-skills, доступный Codex из `.agents/skills/` без глобальных skills и внешней сети.

**Architecture:** Канонические инструкции хранятся в `process/agent-skills/`, а `.agents/skills/` содержит отслеживаемую Git проекцию с теми же файлами. Имена получают префикс `teamssd-`; runtime-specific проекции отделены от общей tool-agnostic логики.

**Tech Stack:** Markdown, OpenSpec CLI 1.4.1, Git, PowerShell для ручных статических проверок.

## Global Constraints

- Не создавать автоматические или поведенческие тесты по прямому решению владельца.
- Не добавлять внешние URL, web/browser search, MCP, connectors или API-клиенты.
- Не добавлять `git push`, `pull`, `fetch`, `clone`, `gh`, package installation, публикацию или deployment.
- Не ссылаться на `~/.codex/skills` и другие файлы вне репозитория.
- Канонические skills редактируются только в `process/agent-skills/`; `.agents/skills/` остаётся точной проекцией.
- Внешние действия заменяются явной остановкой и передачей действия человеку.

---

### Task 1: OpenSpec-контракт и roadmap ownership

**Files:**
- Create: `openspec/changes/add-repo-local-offline-skills/proposal.md`
- Create: `openspec/changes/add-repo-local-offline-skills/design.md`
- Create: `openspec/changes/add-repo-local-offline-skills/tasks.md`
- Create: `openspec/changes/add-repo-local-offline-skills/specs/repo-topology-config/spec.md`
- Modify: `docs/ROADMAP.md`

**Interfaces:**
- Consumes: принятый `openspec/specs/repo-topology-config/spec.md` и дизайн `docs/superpowers/specs/2026-07-24-repo-local-offline-skills-design.md`.
- Produces: change `add-repo-local-offline-skills` с primary phase `P3`, related phase `P4` и статусом `in_progress`.

- [ ] **Step 1: Создать change через OpenSpec CLI**

```powershell
openspec new change "add-repo-local-offline-skills"
openspec status --change "add-repo-local-offline-skills" --json
```

Expected: CLI возвращает `planningHome`, `changeRoot`, `artifactPaths` и порядок artifact dependencies.

- [ ] **Step 2: Создать proposal, design, delta spec и tasks**

Зафиксировать требования:

```text
Execution phase: P3
Related phases: P4
Lifecycle status: in_progress

REQUIREMENT: versioned repo-local agent skill package
SCENARIO: clean clone exposes Codex skills without global skill directories
SCENARIO: runtime adapters use separate projection directories
SCENARIO: offline skills stop before external state mutation
SCENARIO: owner-approved no-test exception is reported as residual risk
```

- [ ] **Step 3: Добавить одну inverse-row в roadmap**

```markdown
| `add-repo-local-offline-skills` | P3 | P4 | in_progress |
```

- [ ] **Step 4: Проверить OpenSpec и roadmap linkage**

```powershell
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
```

Expected: 0 validation errors; существующие lifecycle warnings разрешено только явно перечислить.

### Task 2: Канонический offline skill package

**Files:**
- Create: `process/agent-skills/README.md`
- Create: `process/agent-skills/teamssd-*/SKILL.md`
- Modify: `process/package.yaml`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: одноимённые личные skills из `%USERPROFILE%\.codex\skills\` как исходный текст для локальной адаптации.
- Produces: 23 самодостаточных `teamssd-*` skills и короткое руководство по runtime-проекциям.

- [ ] **Step 1: Создать 23 канонических каталога**

```text
teamssd-architecture-planner
teamssd-phase-change-intake
teamssd-phase-planner
teamssd-phase-status-audit
teamssd-phase-step-runner
teamssd-phase-full-runner
teamssd-roadmap-openspec-validator
teamssd-openspec-explore
teamssd-openspec-propose
teamssd-openspec-apply-change
teamssd-openspec-sync-specs
teamssd-openspec-archive-change
teamssd-brainstorming
teamssd-writing-plans
teamssd-executing-plans
teamssd-using-git-worktrees
teamssd-subagent-driven-development
teamssd-systematic-debugging
teamssd-test-driven-development
teamssd-requesting-code-review
teamssd-verification-before-completion
teamssd-evidence-audit
teamssd-doc-sync-audit
teamssd-session-report
```

Примечание: список содержит 24 каталога; это исправляет ошибочный счёт `23` в устном дизайне без удаления согласованного skill.

- [ ] **Step 2: Адаптировать frontmatter и cross-references**

Каждый `SKILL.md` использует форму:

```yaml
---
name: teamssd-<skill-name>
description: Use when <локальный trigger без описания workflow>
---
```

Все обязательные sub-skill ссылки переводятся на существующий
`teamssd-*` skill. Ссылки на не включённые skills удаляются или заменяются
полной локальной инструкцией.

- [ ] **Step 3: Удалить внешние операции**

Применить ко всем skills:

```text
remote Git / PR / external publication -> stop and report required human action
package installation -> use existing local environment or report blocker
MCP / connector / web -> unavailable and outside this package
global skill path -> repo-local relative path
browser companion -> text-only workflow
```

- [ ] **Step 4: Написать короткий README**

README содержит:

```markdown
# Repo-Local Agent Skills

- Canonical source: `process/agent-skills/`
- Codex projection: `.agents/skills/`
- Offline boundary and forbidden operations
- How to edit a skill and refresh its projection
- How another runtime creates `.gigacode/skills/` or another separate adapter
- Why `.agents/skills/` is not edited directly
- Manual verification commands and the no-test residual risk
```

- [ ] **Step 5: Зарегистрировать пакет и изменить project guidance**

Добавить `agent-skills` в `process/package.yaml` distribution roots. В
`AGENTS.md` заменить утверждение, что все workflow-skills глобальны, на правило:
`teamssd-*` берутся из versioned repo-local package; личные общие skills могут
оставаться глобальными, но не являются зависимостью проекта.

### Task 3: Codex discovery projection

**Files:**
- Create: `.agents/skills/teamssd-*/SKILL.md`
- Modify: `docs/00_FILE_STRUCTURE.md`
- Modify: `docs/README.md`
- Modify: `docs/CURRENT_PROJECT_AUDIT.md`

**Interfaces:**
- Consumes: полный набор из `process/agent-skills/`.
- Produces: точную repo-local Codex-проекцию и короткую пользовательскую документацию.

- [ ] **Step 1: Скопировать канонические каталоги**

Для каждого `process/agent-skills/teamssd-<name>/` создать совпадающий
`.agents/skills/teamssd-<name>/`. Не добавлять runtime-specific различия в
Codex-проекцию этой версии.

- [ ] **Step 2: Обновить карту и README проекта**

Документировать:

```text
process/agent-skills/ = canonical editable package
.agents/skills/ = tracked Codex discovery projection
other runtimes = separate future adapter folders
automated tests = intentionally absent by owner decision
```

- [ ] **Step 3: Обновить audit**

Записать фактическое состояние: каталоги существуют, автоматические тесты
отсутствуют по решению владельца, поведенческая совместимость остаётся ручным
риском.

### Task 4: Ручная статическая проверка и завершение

**Files:**
- Modify: `openspec/changes/add-repo-local-offline-skills/tasks.md`
- Modify: `docs/ROADMAP.md`

**Interfaces:**
- Consumes: канонический пакет, Codex-проекцию и документы.
- Produces: проверенное локальное состояние, завершённые tasks и статус `pending_acceptance`.

- [ ] **Step 1: Проверить запрещённые строки**

```powershell
rg -n -i '(https?://|curl|wget|Invoke-WebRequest|MCP|connector|git (push|pull|fetch|clone)|\bgh\b|npm install|pip install|~/.codex/skills)' process/agent-skills .agents/skills
```

Expected: no matches, кроме локально объяснённого перечня запретов в README; каждый такой match просматривается вручную.

- [ ] **Step 2: Проверить frontmatter и набор каталогов**

```powershell
Get-ChildItem process/agent-skills -Directory | ForEach-Object {
  Select-String -Path (Join-Path $_.FullName 'SKILL.md') -Pattern '^name: teamssd-'
}
```

Expected: одна строка `name:` для каждого из 24 skills.

- [ ] **Step 3: Проверить совпадение проекции**

```powershell
$canonical = Get-ChildItem process/agent-skills -File -Recurse |
  Where-Object Name -eq 'SKILL.md'
foreach ($file in $canonical) {
  $relative = $file.FullName.Substring((Resolve-Path process/agent-skills).Path.Length + 1)
  $projection = Join-Path (Resolve-Path .agents/skills).Path $relative
  if ((Get-FileHash $file.FullName).Hash -ne (Get-FileHash $projection).Hash) {
    throw "Projection drift: $relative"
  }
}
```

Expected: exit 0 without `Projection drift`.

- [ ] **Step 4: Выполнить проектные consistency checks**

```powershell
openspec list
openspec list --specs
openspec validate --all --strict
node "$env:USERPROFILE\.codex\skills\roadmap-openspec-validator\scripts\validate-roadmap-openspec.mjs" --root . --json
git diff --check
```

Expected: 0 errors; lifecycle warnings перечислены в итоговом отчёте.

- [ ] **Step 5: Закрыть tasks, но не принимать change за человека**

Отметить выполненные tasks и синхронно изменить lifecycle status на
`pending_acceptance` в proposal и roadmap inverse row.

- [ ] **Step 6: Создать implementation commit**

```powershell
git add AGENTS.md .agents process docs openspec
git commit -m "feat: add repo-local offline skills"
```

Expected: один implementation commit поверх design/plan commits; push, PR и merge не выполняются.
