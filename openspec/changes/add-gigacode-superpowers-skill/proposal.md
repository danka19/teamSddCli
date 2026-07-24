## Why

Поставляемый GigaCode companion описывает SDD-роли и границы полномочий, но не
задаёт общий рабочий цикл до и после SDD-команд. Под давлением срочности модель
может пропустить проверку ветки и diff, смешать факты с предположениями,
расширить scope или объявить работу завершённой без свежей проверки.

## What Changes

- Добавить отдельный обязательный `.gigacode/skills/superpowers.md` с общим
  безопасным workflow для любой работы в репозитории.
- Активировать Superpowers первым, а `sdd-process-companion.md` — вторым для
  SDD-задач.
- Включить оба skill-файла и `.gigacode/AGENTS.md` в declared managed inventory
  process package.
- При rollback удалять файл, которого нет в target manifest, только если его
  bytes всё ещё совпадают с текущей package-версией; локальное изменение
  блокирует rollback.
- Сохранить human authority: skill не подтверждает classification, DoR/DoD,
  risk, release, archive, merge и внешние mutations.
- Проверять точный bootstrap inventory, порядок активации и конфликт локально
  изменённого managed-файла.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `role-aware-guided-workflow`: GigaCode получает обязательный общий workflow
  перед role-aware SDD companion.
- `repo-topology-config`: bootstrap process package устанавливает и защищает
  точный набор управляемых GigaCode-файлов.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress

## Impact

Изменение затрагивает `process/gigacode/`, package manifest/schema, bootstrap,
update/rollback regression tests, setup-документацию и patch-версию process package.
Оно не включает внешние интеграции, credentials, автономные решения,
автоматический merge/release или новую mutation authority.
