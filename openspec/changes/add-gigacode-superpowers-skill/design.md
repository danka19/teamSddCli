## Context

GigaCode bootstrap уже переносит declared файлы из `process/gigacode/`.
Существующий `sdd-process-companion.md` специально отвечает за SDD-роли,
операции и подтверждения. Он не должен разрастаться в общий coding workflow:
такой workflow нужен и до определения SDD-маршрута, и для обычных repository
задач.

Pressure-аудит старого набора показал устойчивые пробелы: нет обязательной
проверки ветки/status/scoped diff, разделения фактов и предположений,
предварительного плана, пропорциональной проверки до и после edit и
evidence-before-completion.

## Goals / Non-Goals

**Goals:**

- Дать GigaCode короткий обязательный общий workflow.
- Применять SDD companion поверх него, не дублируя role/authority policy.
- Устанавливать skill детерминированно при fresh bootstrap.
- Блокировать update при локальном изменении любого managed GigaCode-файла.
- Проверить поведение тестами и adversarial pressure-сценариями.

**Non-Goals:**

- Переносить глобальные Codex skills в репозиторий.
- Давать AI право на human decisions, merge, release или external mutation.
- Менять SDD lifecycle, classification policy или operation catalog.
- Автоматически разрешать команды по молчанию, срочности или общему
  «продолжай».

## Decisions

### 1. Отдельный flat Markdown skill

Файл поставляется как `.gigacode/skills/superpowers.md`, потому что GigaCode
активирует flat Markdown skills через `.gigacode/AGENTS.md`. Это project
package asset, а не копия глобального Codex `SKILL.md`.

Добавление правил в SDD companion отклонено: общий workflow должен работать и
для задач, которые ещё не классифицированы как SDD, а companion должен
оставаться специализированным.

### 2. Явный порядок композиции

`.gigacode/AGENTS.md` требует сначала применить Superpowers, затем добавить
SDD companion для SDD-задачи. При конфликте действуют более строгие safety и
human-authority ограничения.

### 3. Manifest-driven bootstrap

Новый файл объявляется рядом с двумя существующими GigaCode managed files в
`process/package.yaml` и schema fixture. Bootstrap остаётся data-driven, а
update использует существующий conflict check.

### 4. Patch-версия package

Состав распространяемого process package изменён, поэтому working source
повышается с `0.3.6` до `0.3.7`. Исторические release/certification evidence не
переписываются и не становятся свидетельством принятия `0.3.7`.

## Risks / Trade-offs

- [Skill становится слишком общим] → оставить только обязательные safety,
  scope, verification и reporting шаги; SDD policy держать в companion.
- [Два skill-файла противоречат друг другу] → задать порядок и правило более
  строгой границы.
- [Bootstrap забудет новый файл] → проверять exact inventory из manifest.
- [Локальная настройка будет перезаписана] → сохранять fail-closed managed-file
  conflict без перезаписи.

## Migration Plan

1. Добавить failing tests точного inventory, порядка активации и нового файла.
2. Добавить skill и manifest declaration.
3. Провести pressure-test, уточнить двусмысленные разрешения.
4. Повысить package version до `0.3.7` и обновить setup docs.
5. Проверить bootstrap, update conflict, package regressions и OpenSpec.

Rollback выполняется revert'ом package change; уже локально изменённые managed
файлы не удаляются и не перезаписываются автоматически.

## Open Questions

None.
