# Начать по роли

Канонический источник: [guided workflow](../../runbooks/GUIDED_OWNER_WORKFLOW.md),
[role-aware contract](../../../openspec/specs/role-aware-guided-workflow/spec.md)
и [package role instructions](../../../process/roles/).

Выберите роль, под которой вы реально действуете. Роль нельзя выбирать ради
доступа к следующей команде. Если роли или owner нет в validated registry,
маршрут должен остановиться.

| Роль | Когда открывать | Основной результат | Кому обычно передаёт |
| --- | --- | --- | --- |
| [Analyst](analyst.md) | Новое/изменённое требование, неизвестные факты, scope | Source-linked requirement/Delta draft и открытые решения | Tech Lead и другие owners |
| [Tech Lead](tech-lead.md) | Classification, technical risk, hold/resume, engineering readiness | Decision-support findings и human control decision | Analyst, Developer, QA, release owners |
| [Developer](developer.md) | Change имеет одобренный bounded scope и DoR evidence | Реализация и фактические test/review evidence | QA и reviewers |
| [QA](qa.md) | Требуются scenario, regression и quality evidence | Выполненные проверки, defects и residual gaps | Developer, Tech Lead, applicable owners |
| [Владелец процесса](process-owner.md) | Установка, setup, package/config ownership, onboarding | Проверенное central workspace и рабочий onboarding route | Вся команда |

Для общего synthetic-примера сначала прочитайте
[«Первый minor change»](../first-change.md). Каждая роль выполняет только свой
этап и останавливается на human decision/handoff.
