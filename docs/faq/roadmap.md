# Что уже работает и что будет дальше

Канонический источник: [project roadmap](../ROADMAP.md),
[Phase 3 plan](../phases/PHASE_3_GUIDED_ROLE_AND_ANALYTICS_VERTICAL_SLICE.md)
и [implementation strategy](../IMPLEMENTATION_STRATEGY.md).

Roadmap здесь описан пользовательскими возможностями, без внутренних номеров
задач и обещаний календарных дат. Канонический roadmap остаётся gate-based.

## Что уже можно сделать

- установить локальный versioned `sdd-process` и проверить identity;
- безопасно создать central `process/` + `team-specs/` workspace только с
  human `--confirm`;
- начать маршрут по новому требованию, existing change, incident или failure;
- получить role-aware route для новых ситуаций; continuation real schema-v2
  change через `sdd next` имеет известный `status`/`lifecycle_state` blocker;
- посмотреть canonical operation catalog;
- запускать разрешённые read-only checks и preparation operations;
- работать в human-readable или structured `--json` режиме;
- продолжать обязательные gates без AI;
- хранить class-aware changes, evidence, traceability и failed-run history;
- использовать typed analytics artifacts и локальные read-only previews.

## Что появится следующим

Следующий практический gate — завершить human onboarding: новый участник должен
по этим страницам установить package, пройти synthetic route и правильно
назвать authority boundaries. До walkthrough необходимо согласовать
`sdd next` с каноническим schema-v2 полем `status` и доказать continuation на
реально созданном change. После этого принимается successor reusable
package, пригодный для controlled corporate adaptation.

Также остаётся обязательная portability-проверка принятого successor package в
Linux/WSL2 до начала корпоративного этапа.

## Что планируется позже

- заполнение реальных non-secret project/owner/config values в corporate
  environment;
- approved wiring доступных standard tools и thin AI adapter;
- один monitored real governed-change pilot;
- pilot-driven usability/reliability corrections;
- controlled publication views, Jira task planning, QA/AT proposal layers и
  role inbox после отдельных принятых contracts;
- дальнейшая bounded AI automation evidence assembly, routing и preparation
  при сохранении deterministic control plane.

## Что намеренно не автоматизировано

- `sdd run` mutations в текущей версии;
- AI approval, risk acceptance, waiver, merge, release или archive;
- автоматическое изменение Jira, Confluence, Bitbucket и Jenkins;
- deploy и customer acceptance;
- Jira tasks, Confluence publication, QA/AT generation и role inbox в первом
  MVP;
- silent defaults при неизвестном факте;
- удаление failed-run после успешного retry.

## Как понять статус конкретной функции

1. Посмотрите эту страницу для пользовательского уровня.
2. Проверьте `sdd --help` и `sdd op list --json` для установленной версии.
3. Для точного behavior/acceptance откройте linked OpenSpec requirement.
4. Не считайте planned capability доступной только потому, что о ней есть
   template, design или draft.
