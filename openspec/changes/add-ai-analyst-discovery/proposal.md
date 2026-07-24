# Change: добавить аналитическое интервью в AI companion

## Why

Текущий учебный маршрут начинается с уже точной постановки и предлагает
пользователю копировать длинный технический prompt. Аналитику нужен простой
вход, который помогает уточнить сырую идею и подготовить source-aware черновик,
не передавая AI человеческие полномочия.

## What Changes

- Существующий packaged `sdd-process-companion` получает режимы
  `analyst-discovery` и `guided-change`.
- Перед интервью AI показывает короткий план тем и получает разрешение.
- После разрешения AI задаёт по одному вопросу и сверяет понимание после
  смысловых блоков.
- Черновики создаются только после подтверждения итоговой сводки.
- Переход к файлам и командам требует отдельного согласия.
- FAQ получает человекочитаемый маршрут от простой фразы до управляемого change.

## What Does Not Change

- Детерминированные CLI contracts и human authority boundaries.
- Ручной и AI-disabled маршруты.
- Lifecycle, classification и gate semantics.
- Запрет P3 на автономное выполнение и external mutation.

## Capabilities

### Modified Capabilities

- `role-aware-guided-workflow`: добавляет permission-bound аналитическое
  интервью, evidence-сводку и явную передачу в guided change.

## Roadmap

- Execution phase: P3
- Related phases: P4
- Lifecycle status: in_progress

## Impact

Изменяются поставляемый `process/gigacode/skills/sdd-process-companion.md`,
контрактные тесты пакета, AI-разделы FAQ, FAQ validator и версия process
package. Новый runtime, schema, persistence или внешний integration layer не
добавляются.
