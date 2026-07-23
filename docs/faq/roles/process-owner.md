# Владелец процесса: подготовить команду

Канонический источник: [walkthrough onboarding](../../audits/SELF_SERVICE_OPERATOR_ONBOARDING_WALKTHROUGH_2026-07-23.md).

Цель — создать локальную структуру команды без секретов и внешних вызовов. Человек запускает `sdd setup <папка> --confirm`. Результат — только `process/` и `team-specs/`, после чего возможен first minor-change walkthrough через `sdd start new-requirement --role Analyst`. Если папка не пуста, конфигурация невалидна или подтверждение не дано, ничего не обходите: исправьте ввод либо запросите поддержку.
