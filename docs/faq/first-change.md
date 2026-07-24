# Первый `minor` change: сквозной учебный маршрут

Канонический источник: [guided workflow](../runbooks/GUIDED_OWNER_WORKFLOW.md),
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md) и
[accepted dispatcher contract](../../openspec/specs/guided-operation-dispatcher/spec.md).

Этот tutorial показывает, что увидит команда на безопасном synthetic-примере.
Он не выдаёт tutorial за human acceptance, release или external operation.
Текущая исполнимая часть заканчивается перед human-owned решениями, mutation,
release и external operation; `sdd next` даёт только read-only continuation.

## Сценарий

Команда хочет добавить небольшую проверяемую подсказку в локальный продукт.
Tech Lead предварительно допускает, что изменение может быть `minor`, но
окончательная классификация остаётся человеческим решением после evidence.

Используйте только synthetic IDs и пустое тестовое workspace. Не добавляйте
corporate exports, credentials или private prompts.

## Шаг 1. Владелец процесса готовит workspace

Если workspace ещё нет:

```text
sdd setup C:/work/faq-walkthrough --confirm --json
```

Ожидаемый результат: `status: created`, локальные `process/` и `team-specs/`,
следующая команда для Analyst. Evidence: сохранённый JSON setup без секретов.

## Шаг 2. Analyst начинает новое требование

```text
sdd start new-requirement --role Analyst --fact classification=minor --json
```

Проверьте:

- `status` равен `guided`;
- `missing_facts` пуст;
- `expected_evidence` содержит proposed change package и classification evidence;
- `human_decision.owner` равен `Tech Lead`;
- `authority_boundary` сообщает, что классификация pending;
- `next_command` равен
  `sdd request create-change --role Analyst --json`.

Analyst сохраняет intent и известные факты отдельно от предположений. Он не
начинает реализацию.

## Шаг 3. Analyst формирует неавторитетный запрос

```text
sdd request create-change --role Analyst --json
```

Ожидаемый результат: локальный request/intent с
`authority_granted: false` и указанием, что trusted human event metadata
требуется. Это evidence подготовки, а не созданный change и не одобрение.

Передача: Tech Lead получает intent, classification evidence, unresolved facts
и ссылку на synthetic requirement.

## Шаг 4. Tech Lead проверяет класс и границы

Tech Lead использует свой [role runbook](roles/tech-lead.md), проверяет
minor-условия, риски, scope и обязательные gates. Если данных недостаточно,
он фиксирует hold вместо угадывания.

Для hotfix используется отдельная ситуация:

```text
sdd start urgent-incident --role "Tech Lead" --fact incident_ref=<safe-evidence-path> --json
```

Срочность не превращает change в hotfix автоматически и не отменяет regression,
rollback/hold, traceability или reconciliation.

## Шаг 5. Ответственный оператор создаёт change package

На этом шаге текущая публичная команда намеренно не выполняет mutation. `sdd run`
даже с confirmation artifact возвращает `confirmation-contract-pending`.

Технический оператор продолжает только по
[packaged governed flow](../runbooks/PACKAGED_GOVERNED_FLOW.md), где
compatibility entrypoint, schema-v2 template и human-owned decision описаны
полностью. Обычному участнику не нужно самостоятельно искать скрипт или
придумывать аргументы.

Результатом отдельного разрешённого шага должен стать путь вида:

```text
C:/work/faq-walkthrough/team-specs/openspec/changes/sample-minor-001/
```

До появления реального change path переходить к `sdd next` нельзя.

## Шаг 6. Developer получает canonical continuation

Когда `change.yaml` существует и содержит реальный lifecycle state:

```text
sdd next --change C:/work/faq-walkthrough/team-specs/openspec/changes/sample-minor-001 --role Developer --json
```

Schema-v2 template хранит lifecycle только в top-level поле `status`, и
`sdd next` читает именно его. На реально созданном package ожидается guided
continuation без lifecycle или external mutation:

```json
{
  "operation": "sdd-next",
  "status": "guided",
  "lifecycle_mutated": false,
  "external_state_mutated": false
}
```

Не добавляйте второе persisted-поле `lifecycle_state` и не меняйте schema ради
обхода. `next_command` — рекомендация для human review, а не approval, DoR/DoD
или разрешение выполнить mutation. При missing или unsupported `status`
сохраните blocker и используйте [artifact/lifecycle](../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md)
и [packaged flow](../runbooks/PACKAGED_GOVERNED_FLOW.md).

Developer проверяет returned route и DoR; route сам по себе не доказывает готовность.
`next_command` останется рекомендацией, а не доказательством готовности.
Реализация допускается только в bounded scope, после scenario mapping и с
фактическими test results.

Evidence: изменённые paths, команды и реальные результаты tests/review,
unresolved inputs и residual limitations.

Передача: QA получает exact change/revision, applicable scenarios, environment
и implementation evidence.

## Шаг 7. QA продолжает после исправления blocker

```text
sdd next --change C:/work/faq-walkthrough/team-specs/openspec/changes/sample-minor-001 --role QA --json
```

До исправления шага 6 QA использует specialist runbook и не заявляет, что
`sdd next` прошёл. После исправления QA не принимает `passed` из текста Developer или AI. Он связывает positive и
negative cases со stable scenario IDs, выполняет доступные проверки, сохраняет
actual output и оставляет missing/unavailable evidence видимым.

Передача: Tech Lead и остальные применимые владельцы получают QA findings,
blocking defects, evidence references и остаточный риск. QA не выполняет
release/archive decision.

## Шаг 8. Подготовка review/archive остаётся локальной

Когда соответствующие gates и человеческие решения действительно существуют,
`sdd prepare <operation>` может подготовить локальный результат. Preparation:

- не меняет lifecycle;
- не создаёт PR или commit;
- не публикует в Confluence/Jira;
- не подтверждает DoD, release или archive.

Точные arguments и readiness requirements находятся в
[artifact/lifecycle runbook](../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md) и
[packaged flow](../runbooks/PACKAGED_GOVERNED_FLOW.md).

## Где текущая автоматизация останавливается

В текущей версии команда останавливается перед mutation через `sdd run`, перед
external system action и перед каждым human-owned decision. Она не меняет
lifecycle и не заменяет обязательные gates.
Полный путь от первого `sdd start` до автоматически созданного и архивированного
change через один public CLI пока недоступен.

Это не ошибка tutorial. Это честная текущая граница продукта. Planned layers
описаны в [roadmap](roadmap.md).

## Что считать успешным walkthrough

- новый пользователь нашёл нужный маршрут без чтения source code;
- он смог установить/проверить `sdd` и создать synthetic workspace;
- Analyst получил guided result и понял pending decision;
- участники правильно назвали свои evidence и stop points;
- никто не принял `request`, `prepare` или successful validation за approval;
- неизвестный факт привёл к block/escalation, а не к догадке;
- AI-disabled маршрут остался понятным.

Дальше откройте [роль](roles/index.md), [ежедневный lifecycle](daily-workflow.md)
или [troubleshooting](troubleshooting-and-boundaries.md).
