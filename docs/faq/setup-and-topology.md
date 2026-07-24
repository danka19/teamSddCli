# Setup, `team-specs` и подключение проекта

Канонический источник: [repo topology contract](../../openspec/specs/repo-topology-config/spec.md),
[process package setup](../runbooks/PROCESS_PACKAGE_SETUP.md) и
[self-service onboarding](../../openspec/changes/add-self-service-operator-onboarding/specs/self-service-operator-onboarding/spec.md).

<!-- faq-question: setup --><!-- faq-question: topology -->

## Что создаёт setup

`sdd setup` создаёт новое локальное central workspace:

```text
<workspace>/
├── process/
│   ├── package.yaml
│   ├── policies/
│   ├── schemas/
│   ├── templates/
│   └── validators/
└── team-specs/
    ├── sdd.config.yaml
    ├── owners.yaml
    ├── projects.yaml
    └── openspec/
        ├── changes/
        └── specs/
```

`process/` — versioned deterministic package. `team-specs/` — центральная
рабочая область команды для changes, Master Specs, configuration, evidence и
traceability. Это не папка для secrets.

## Что нужно до начала

- `sdd --version --json` возвращает ожидаемый package identity;
- выбран новый пустой destination;
- человек понимает, что `--confirm` разрешает локальное создание файлов;
- реальные owner/project values будут добавлены отдельным review;
- destination не является существующим code repository.

## Создать workspace

Сначала безопасно проверьте отсутствие подтверждения:

```text
sdd setup C:/work/sample-sdd-workspace --json
```

Ожидается `status: blocked`, blocker `confirmation-required`; destination не
создаётся.

После того как человек проверил путь:

```text
sdd setup C:/work/sample-sdd-workspace --confirm --json
```

Ожидается:

- `status: created`;
- точный путь в `workspace`;
- созданные `process/` и `team-specs/`;
- `next_command: sdd start new-requirement --role Analyst --json`;
- отсутствие network/external mutation.

AI может подготовить строку команды, но не должен добавлять `--confirm` от
своего имени. Путь и подтверждение выбирает человек.

## Настроить non-secret team values

Файл `team-specs/sdd.config.yaml` связывает package, OpenSpec version, policy
set, canonical paths и registries. `owners.yaml` и `projects.yaml` содержат
проверенные командой идентификаторы владельцев и проектов.

При заполнении:

1. сохраните package ID/version и OpenSpec pin;
2. замените только документированные synthetic placeholders;
3. используйте стабильные non-secret IDs, а не email/password/token;
4. проверьте пути относительно central workspace;
5. прогоните configuration validation из
   [process package setup runbook](../runbooks/PROCESS_PACKAGE_SETUP.md).

Публичный `sdd` пока не даёт отдельную self-service команду для полной
валидации team config. Точный compatibility entrypoint остаётся в specialist
setup runbook. Не заменяйте его визуальной проверкой YAML или выводом AI.

FAQ не воспроизводит schema rules: при расхождении каноничны package schemas и
OpenSpec contract.

## Подключить существующий code repository

Не запускайте `sdd setup` поверх code repository. Первый поддерживаемый
topology — один central `team-specs`, а project repo при необходимости получает
маленький `.sdd-project.yaml`, который указывает:

- stable project ID;
- путь к central `team-specs`;
- принятую package/config version;
- проверенные local path mappings.

Используйте шаблон `templates/project-adapter/.sdd-project.yaml`. Не копируйте
Master/Delta Specs в code repo и не создавайте второй independent config.
Настоящие corporate paths и интеграции добавляются только на этапе
контролируемой адаптации.

## Проверить первый маршрут

Из любого каталога, где доступен установленный `sdd`:

```text
sdd start new-requirement --role Analyst --fact classification=minor --json
```

Ожидается `status: guided`, отсутствие `missing_facts`, human owner `Tech Lead`
и следующий неавторитетный шаг `sdd request create-change --role Analyst
--json`. Команда не создаёт change и не меняет lifecycle.

<!-- faq-question: start-next --><!-- faq-question: json-output -->

Без `--json` `sdd` печатает краткое объяснение для человека. С `--json`
возвращается один structured result для evidence или разрешённого AI caller.
Оба режима используют один route и не заполняют неизвестные факты.

## Если setup заблокирован

| Blocker | Что делать |
| --- | --- |
| `confirmation-required` | Проверить destination и повторить человеку с `--confirm` |
| `destination-not-empty` | Не очищать папку автоматически; выбрать новый пустой путь или вручную решить судьбу содержимого |
| `input-invalid` | Проверить package root/template source и повторить без догадок |
| package/config incompatibility | Остановить setup, сохранить JSON и использовать update/rollback runbook |
| private/secret value обнаружен | Удалить значение из versioned config и перенести его в разрешённое local secret storage |

## Следующий шаг

Пройдите [первый synthetic change](first-change.md) либо откройте
[runbook владельца процесса](roles/process-owner.md).
