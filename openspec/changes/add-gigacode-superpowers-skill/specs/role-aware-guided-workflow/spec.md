## ADDED Requirements

### Requirement: Обязательный общий workflow для GigaCode

Поставляемая конфигурация GigaCode SHALL применять общий Superpowers workflow
до специализированного SDD companion. Общий workflow SHALL требовать
обнаружить применимые инструкции, проверить branch/status/scoped diff,
отделить факты от предположений, ограничить scope, выполнить пропорциональную
проверку до и после edit и показать свежий evidence перед заявлением о
завершении.

Он SHALL NOT превращать срочность, молчание, общий вопрос, неограниченное
«продолжай» или прошлый зелёный тест в разрешение на невидимый scope, human
decision, merge, release или external mutation.

#### Scenario: GigaCode начинает SDD-задачу

- **WHEN** GigaCode получает задачу, затрагивающую SDD workflow
- **THEN** он сначала применяет общий Superpowers workflow, затем role-aware SDD companion и сохраняет более строгую human-authority границу

#### Scenario: Срочность не отменяет общий workflow

- **WHEN** пользователь просит «быстро поправить одну строку» и не даёт точного разрешения на дополнительный scope
- **THEN** GigaCode проверяет branch/status/scoped diff, не затрагивает чужие изменения и не объявляет completion без свежей проверки
