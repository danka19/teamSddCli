# Ежедневная работа: lifecycle, классы и evidence

Канонический источник: [artifact/lifecycle gates](../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md),
[classification](../runbooks/CLASSIFICATION_AND_MIGRATION.md) и
[change lifecycle spec](../../openspec/specs/change-lifecycle/spec.md).

## С чего начинается рабочий день

Для существующего change не выбирайте операцию по памяти:

```text
sdd next --change <path-to-change> --role <role> --json
```

Schema-v2 package хранит lifecycle только в `status`, и `sdd next` читает это
каноническое поле. Не добавляйте второе persisted-поле `lifecycle_state` и не
редактируйте metadata ради другого route: при missing или unsupported `status`
сохраните blocker и следуйте specialist lifecycle runbook.

Проверьте exact change, lifecycle state, missing facts, expected evidence,
human decision и stop point. Затем выполните только разрешённый stage.

<!-- faq-question: lifecycle -->

## Lifecycle простым языком

| State | Что происходит | Что не следует из state |
| --- | --- | --- |
| `draft` | Собираются intent, facts и initial Delta | Реализация ещё не разрешена |
| `spec_review` | Люди проверяют proposed behavior/revision | Review comment не равен acceptance |
| `approved` | Принято конкретное изменение спецификации | Полный DoR ещё нужно доказать |
| `in_implementation` | Выполняется bounded implementation | Код complete не равен DoD |
| `ready_to_archive` | Требуемые gates/evidence готовы к archive review | Release/deployment/Done не подразумеваются |
| `archived` | Delta human-approved образом включена в Master Spec/history | Это не customer acceptance и не tracker Done |

Переходы проверяются детерминированно, но human-owned gate не становится
автоматическим решением.

<!-- faq-question: change-classes -->

## Как читать классы

- `minor` — разрешён только когда все применимые low-impact условия известны и
  подтверждены evidence;
- `major` — используется при material impact/risk либо существенной
  неопределённости;
- `hotfix` — срочный отдельный класс, если задержка увеличивает конкретный
  вред; он сохраняет minimum safety, regression, rollback/hold, traceability и
  reconciliation.

Не выбирайте `minor`, чтобы сократить документы, и не выбирайте `hotfix`, чтобы
обойти gate. Точные criteria принадлежат canonical classification policy.

<!-- faq-question: evidence-ci -->

## Что считается evidence

Хорошая запись evidence отвечает на пять вопросов:

1. Что проверялось: requirement/scenario/task/gate ID?
2. На какой revision/input?
3. Какой exact command или manual procedure выполнены?
4. Каков actual result и где он сохранён?
5. Кто должен интерпретировать результат или принять решение?

CI и local validators доказывают только свой contract. Они не утверждают risk,
release, archive или external delivery.

## Если проверка упала

1. Сохраните command, input identity, output и failure.
2. Свяжите failed-run с change/task/gate.
3. Исправляйте только в разрешённом scope.
4. Повторите проверку и сохраните новый result отдельно.
5. Не удаляйте первый failure и не называйте его «шумом» без review.

## Типичный handoff

```text
Analyst: intent + scenarios + open decisions
→ Tech Lead: class/scope/risk/control decision
→ Developer: bounded implementation + actual checks
→ QA: scenario/regression evidence + defects/gaps
→ applicable human owners: DoD/release/archive decisions
```

Это логическая последовательность, а не универсальное право одной роли
перевести state. Откройте [конкретный role runbook](roles/index.md) перед
действием.

## Что делать при блокировке

Используйте:

```text
sdd start blocked-operation --role <role> --fact failed_run_ref=<safe-evidence-path> --json
```

Route должен назвать retained failed-run, accountable decision и manual
fallback. Если evidence path отсутствует, сначала сохраните failure.
