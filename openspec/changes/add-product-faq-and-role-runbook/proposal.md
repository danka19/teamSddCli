## Why

Проект уже содержит корректные, но специализированные runbooks, OpenSpec contracts и certification evidence. Человек, впервые открывший продукт, не получает короткого объяснения его пользы, отличий от обычного OpenSpec, практического маршрута по ролям и безопасных правил совместной работы с AI.

## What Changes

- Создать навигационный product FAQ с короткой стартовой страницей и отдельными связанными страницами вместо одной длинной инструкции.
- Объяснить назначение фреймворка, его отличие от OpenSpec и OpenSpec DE, границы пользы, статус простым языком и ближайшие планы без внутреннего жаргона.
- Добавить полноформатный runbook «Начать работу» для Analyst, Tech Lead, Developer, QA и владельца процесса.
- Описать совместную работу с AI: AI может пользоваться `sdd` от имени человека в разрешённых границах и может объяснять процесс без CLI, но не заменяет команды, deterministic gates или human authority.
- Зафиксировать правила пользователя: канонические источники, обязательные решения человека, evidence, запрет на обход подтверждений и порядок действий при недоступном AI/интеграции.
- Добавить FAQ об установке, `team-specs`, существующем коде, change lifecycle, minor/major/hotfix, CI, privacy, failures, release и corporate pilot.

## Capabilities

### New Capabilities

- `product-faq-and-role-runbook`: версия управляемого, навигационного и role-oriented пользовательского объяснения продукта, его режима работы и безопасного использования с AI.

### Modified Capabilities

- `documentation-governance`: product documentation получает canonical FAQ/runbook information architecture и правила недублирования требований из OpenSpec.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: planned

## Impact

Затрагиваются `docs/README.md`, новые страницы в `docs/runbooks/` и/или `docs/faq/`, generated/validated navigation, роль-инструкции и documentation checks. Изменение не включает изменение process policy, внешние интеграции или автоматическое исполнение операций.
