# Analyst: начать разбор

Канонический источник: [guided workflow](../../runbooks/GUIDED_OWNER_WORKFLOW.md).

Цель — собрать факты изменения и выбрать применимый gate. Начните с `sdd start new-requirement --role Analyst --fact classification=<minor|major|hotfix>`. Результат — локальный маршрут и список доказательств; классификацию подтверждает Tech Lead. Не начинайте реализацию: при неизвестном факте остановитесь и эскалируйте владельцу решения.
