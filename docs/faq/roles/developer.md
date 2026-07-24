# Developer: реализовать одобренный bounded change

Канонический источник: [artifact/lifecycle gates](../../runbooks/ARTIFACT_AND_LIFECYCLE_GATES.md),
[packaged flow](../../runbooks/PACKAGED_GOVERNED_FLOW.md) и
[bounded Developer instruction](../../../process/roles/developer.md).

## Когда использовать

Используйте runbook только для change с утверждённым bounded scope и
проверяемым readiness evidence. Developer реализует один явно назначенный
этап/задачу, выполняет фактические проверки и останавливается для review.

## Что нужно до начала

- роль подтверждена как `Developer`;
- существует точный change path и current revision;
- classification подтверждена ответственным человеком;
- applicable DoR evidence доступно и не содержит blocker;
- requirement/scenario/task/design IDs определены;
- dependencies завершены;
- write scope не пересекается с чужой активной задачей;
- secrets/private data не входят в read/write pack.

Строка `status: approved` сама по себе не доказывает весь DoR.

## Пошаговый маршрут

1. Убедитесь, что real schema-v2 change содержит канонический top-level `status`.
   `sdd next` читает только это поле. Не добавляйте вручную второе persisted-поле
   `lifecycle_state` и не меняйте status ради другого route.
2. Получите каноническое continuation:

   ```text
   sdd next --change <path-to-change> --role Developer --json
   ```

3. Проверьте `status`, `missing_facts`, `expected_evidence`,
   `authority_boundary` и `next_command`.
4. Прочитайте только bounded sources: accepted/Delta requirements, scenarios,
   design, task, class/gate evidence и затронутые code paths.
5. Сопоставьте каждое изменение с acceptance scenario до редактирования.
6. Реализуйте только declared write scope. Не меняйте process policy, lifecycle,
   approvals или соседние tasks.
7. Запустите focused tests и сохраните exact command, exit/result и evidence.
8. Выполните required combined/integration gate, если задача была частью
   параллельной работы.
9. Проведите self-review: scope, secrets, negative cases, docs, residual gaps.
10. Передайте результат на human code review и QA; не merge и не transition.

## Ожидаемый результат

- изменены только разрешённые файлы;
- implementation связана со stable scenario/task IDs;
- actual tests/review evidence сохранены;
- неисполненные проверки отмечены `not-run` с причиной;
- blockers и residual limitations видимы;
- approval/lifecycle/release/archive остаются false/pending.

## Доказательства

Сохраните task/read-pack identity, source IDs/path/hash, список изменённых
paths, commands и реальные outputs, tests и negative cases, review reference,
unresolved inputs, limitations и prohibited attempts. Фраза «тесты должны
пройти» не является evidence.

## Решения и границы

Developer принимает инженерные решения внутри одобренного design/write scope и
может предложить correction. Он не расширяет scope молча, не подтверждает DoR
за owner, не изменяет classification, не принимает QA/risk/release и не
переводит lifecycle.

Если implementation обнаружила новый material impact, остановитесь и верните
change Analyst/Tech Lead вместо скрытого расширения.

## Передача работы

QA получает exact revision, scenario mapping, environment, commands/results и
known gaps. Reviewer получает bounded diff и acceptance links. Analyst/Tech
Lead получают обнаруженные scope/design contradictions. Handoff не означает,
что DoD или release пройдены.

## Сбои, fallback и эскалация

- `sdd next` blocked — исправить/эскалировать missing context, не угадывать;
- DoR evidence неполно — вернуть ответственному owner;
- dependency/write scope пересекаются — остановить параллельную работу;
- test failed — сохранить failed-run, исправлять только в scope либо эскалировать;
- requirement/design конфликтуют — вернуть Analyst/Tech Lead;
- AI недоступен — продолжить по sources и commands вручную.

## Работа с AI

```text
Ты работаешь как bounded Developer assistant. Scope: <paths>. Sources:
<REQ/SCEN/TASK/design IDs>. Сначала перечисли gaps/dependencies. Изменяй только
scope, запускай только согласованные checks, приводи actual output. Не меняй
policy/lifecycle/approval и остановись для human review.
```

Для `sdd next` разрешайте AI только конкретный `--json` вызов. Следующую
operation подтверждайте отдельно после проверки результата.

## Чек-лист завершения

- [ ] Change/revision/class/DoR проверены.
- [ ] Dependencies и write scope ясны.
- [ ] Scenario mapping выполнен.
- [ ] Изменены только разрешённые paths.
- [ ] Focused/required checks реально запущены.
- [ ] Failed/not-run evidence не скрыто.
- [ ] Secrets/private data отсутствуют.
- [ ] QA/reviewer получили полный handoff.
- [ ] Merge/lifecycle/release/archive не присвоены самовольно.
