# FAQ: начать работу с teamSddCli

`teamSddCli` — локальный набор команд, шаблонов и проверок для командной
работы над изменениями через OpenSpec. Он помогает провести изменение от
первичного требования до проверяемых артефактов и следующего безопасного шага:
кто действует, что нужно подготовить, какая проверка обязательна и где решение
остаётся за человеком.

Продукт не принимает требования, риски, релиз или результат работы за команду.
В текущей версии он также не выполняет внешние операции: Jira, Confluence,
Bitbucket и Jenkins не изменяются командами `sdd`.

Канонический источник: [описание проекта](../README.md),
[контракт FAQ](../../openspec/specs/product-faq-and-role-runbook/spec.md)
и [контракт self-service CLI](../../openspec/changes/add-self-service-operator-onboarding/specs/self-service-operator-onboarding/spec.md).

<!-- faq-question: product-purpose --><!-- faq-question: benefits -->

## Выберите свой маршрут

### Я впервые вижу продукт

1. Откройте [self-service маршрут через public `sdd`](self-service-entrypoint.md).
2. Прочитайте [что это, кому подходит и чем отличается от OpenSpec](product-and-foundation.md).
3. Проверьте [требования и установите `sdd`](installation.md).
4. Если вы готовите команду, создайте [центральное рабочее пространство](setup-and-topology.md).
5. Пройдите [первый synthetic `minor` change](first-change.md):
   сначала [в паре с AI](first-change-with-ai.md), затем
   [тот же маршрут без AI](first-change-without-ai.md).

### Команда уже настроена, мне нужно начать работу

1. Откройте [runbook своей роли](roles/index.md).
2. Для нового требования начните с `sdd start <ситуация>`.
3. Для существующего change используйте
   `sdd next --change <путь-к-change> --role <роль>`.
4. Проверьте `status`, `missing_facts`, `next_command`,
   `expected_evidence` и `authority_boundary` в ответе.
5. Остановитесь, если требуется решение другой роли или отсутствует факт.

Schema-v2 change хранит lifecycle в top-level поле `status`, и `sdd next`
читает это каноническое поле. Не добавляйте вручную второе persisted-поле
`lifecycle_state`; если `status` отсутствует или не поддерживается, сохраните
blocker и используйте specialist runbook.

### Я хочу работать через AI

Для первого раза откройте [сквозной change вместе с AI](first-change-with-ai.md):
начните простой фразой, разрешите короткое аналитическое интервью, подтвердите
сводку и только затем переходите к командам. AI предложит candidate class по
фактам, покажет разрешённые команды и запросит отдельное подтверждение каждого
действия. Общие правила, permissions и готовые prompts находятся на странице
[«Работа с AI»](ai-collaboration.md).

## Быстрые ответы

### Что я получу после установки?

Публичную команду `sdd`. Она показывает версию package, создаёт подтверждённое
локальное workspace, выбирает маршрут по ситуации, продолжает существующий
change, показывает каталог операций и запускает разрешённые read-only или
preparation operations.

### Нужно ли знать имена Python-скриптов?

Для обычного старта — нет. Используйте `sdd setup`, `sdd start`, `sdd next`,
`sdd op`, `sdd check`, `sdd prepare` и `sdd request`. Прямые
`python scripts/*.py` остаются техническим compatibility-интерфейсом для
специализированных runbooks и не являются первым пользовательским маршрутом.

### Команда `sdd` сама создаст и завершит change?

Нет. `sdd start` и `sdd next` дают маршрут. `sdd request` формирует
неавторитетный локальный запрос. `sdd check` проверяет, а `sdd prepare`
подготавливает локальный результат. `sdd run` сейчас остаётся fail-closed и не
выполняет mutation. Подробно эта граница показана в
[первом change](first-change.md).

### Можно ли пользоваться без AI?

Да. Все обязательные проверки и человеческие решения имеют deterministic или
явный manual route. AI — помощник для объяснения, черновиков и разрешённых
локальных команд, а не обязательная часть процесса.

## Карта документации

- [Self-service: начать работу через public `sdd`](self-service-entrypoint.md)
- [Что это, польза, OpenSpec, OpenSpec DE и NIS](product-and-foundation.md)
- [НИС как основа корпоративного процесса](nis-foundation.md)
- [Установка и проверка `sdd`](installation.md)
- [Setup, `team-specs` и подключение проекта](setup-and-topology.md)
- [Первый change: порядок двух проходов](first-change.md)
  - [сначала в паре с AI](first-change-with-ai.md)
  - [затем тот же change без AI](first-change-without-ai.md)
- [Ежедневный lifecycle, классы и evidence](daily-workflow.md)
- [Начать по своей роли](roles/index.md)
- [Практическая работа с AI](ai-collaboration.md)
- [Сбои, приватность, релиз и поддержка](troubleshooting-and-boundaries.md)
- [Понятный roadmap: что работает, что запланировано и где открытые спеки](roadmap.md)
- [Словарь терминов](glossary.md)

## Главное правило безопасности

Успешный вывод команды означает только то, что написано в полях результата.
Он не означает автоматическое принятие классификации, прохождение DoR/DoD,
одобрение риска, release readiness, archive, merge, deployment или tracker
Done. Не дополняйте неизвестные факты догадками и не удаляйте failed-run после
успешного повтора.

## Поддержка FAQ

FAQ — поддерживаемое пользовательское представление, а не вторая политика.
OpenSpec владеет требованиями и acceptance, а подробные specialist runbooks —
операционными контрактами. Автор изменения обновляет затронутые FAQ-страницы и
запускает:

```text
python scripts/validate_product_faq.py --json
python -m pytest tests/test_product_faq_docs.py -q
```

Финальная проверка полноты — отдельный walkthrough человеком, который не
разрабатывал эти страницы. Автоматический или synthetic проход проверяет
команды, но не доказывает, что объяснение понятно новому пользователю.
