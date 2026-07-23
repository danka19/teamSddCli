# Установка, `sdd` и рабочая структура

Канонический источник: [walkthrough onboarding](../audits/SELF_SERVICE_OPERATOR_ONBOARDING_WALKTHROUGH_2026-07-23.md) и [guided workflow](../runbooks/GUIDED_OWNER_WORKFLOW.md).

<!-- faq-question: installed-sdd --><!-- faq-question: setup -->

`sdd` — поддерживаемая точка входа оператора. Для новой команды владелец процесса запускает `sdd setup <папка> --confirm`: без `--confirm` ничего не создаётся. Подтверждение остаётся человеческим решением, а не формальностью для AI.

<!-- faq-question: topology -->

После setup появляются локальные `process/` и `team-specs/`. В `team-specs` хранятся change packages и несекретная конфигурация; проектные адаптеры добавляют только проверенные ссылки. Обычному пользователю не нужно искать Python-скрипты; прямые `scripts/*.py` сохранены лишь как совместимый технический интерфейс.

<!-- faq-question: start-next --><!-- faq-question: json-output -->

`sdd start <ситуация>` начинает маршрут, а `sdd next --change <путь>` подсказывает продолжение. Без `--json` ответ рассчитан на человека; `--json` даёт один структурированный результат для разрешённого вызова помощником AI. Оба режима не выдают недостающий факт за известный.
