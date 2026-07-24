# Словарь пользователя

Канонический источник: [полный проектный glossary](../CONTEXT.md) и
[accepted OpenSpec specs](../../openspec/specs/).

| Термин | Простое объяснение |
| --- | --- |
| SDD | Работа, где требования, design, tasks и проверки начинаются со спецификации и остаются с ней связаны |
| OpenSpec | Формат и CLI для proposal, Delta Specs, design, tasks, validation и archive |
| OpenSpec DE | Внутренняя developer-oriented настройка OpenSpec, исследованная проектом; не официальный upstream-продукт |
| `teamSddCli` | Командный слой вокруг OpenSpec: роли, классы, gates, evidence, package и безопасная AI-помощь |
| Change package | Папка одного изменения с metadata, proposal, design, tasks, Delta Specs и evidence |
| Delta Spec | Предлагаемое изменение требования внутри change package |
| Master Spec | Принятая текущая спецификация capability после human-approved archive |
| `team-specs` | Центральное Git-пространство команды для changes, specs, config, evidence и traceability |
| Process package | Версионируемые policies, schemas, templates, validators, role instructions и catalogs |
| `minor` | Ограниченное изменение, для которого доказаны все low-impact условия |
| `major` | Изменение с material impact/risk либо неизвестной существенной областью |
| `hotfix` | Срочное изменение, где задержка увеличивает конкретный вред; обязательная безопасность и reconciliation сохраняются |
| Gate | Проверяемая точка, где нужны определённые факты/evidence и часто отдельное человеческое решение |
| DoR | Definition of Ready: человек решает, достаточно ли evidence для начала реализации |
| Implementation complete | Код/конфигурация и требуемые implementation checks существуют; это ещё не DoD/release/archive |
| DoD | Definition of Done: class-aware completion gate с acceptance, tests, review, docs и traceability |
| Evidence | Ссылка или сохранённый фактический результат проверки, решения или действия |
| Failed-run | Сохранённая неуспешная попытка; она не удаляется после успешного повтора |
| Traceability | Связи requirement → scenario → task → test → evidence |
| Hold | Явная остановка работы до выполнения условия или человеческого решения |
| Fallback | Разрешённый deterministic/manual путь, если AI или integration недоступны |
| Fail-closed | При неизвестном факте или неподтверждённом праве операция блокируется, а не угадывает продолжение |
| `--json` | Машиночитаемый один-result режим для evidence и разрешённого AI caller |
| `sdd start` | Выбрать маршрут по новой ситуации |
| `sdd next` | Получить применимое продолжение по existing change state; lifecycle schema-v2 читается только из top-level `status`, без второго persisted-поля `lifecycle_state` |
| `sdd request` | Подготовить неавторитетный intent/request; не предоставить authority |
| `sdd prepare` | Подготовить локальный артефакт/результат без external mutation и без принятия решения |
| `sdd run` | Mutation boundary; в текущей версии намеренно остаётся заблокированной |

Если термин влияет на policy или acceptance, канонично его определяет OpenSpec,
а эта страница только помогает ориентироваться.
