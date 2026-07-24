# Установка и проверка `sdd`

Канонический источник: [self-service onboarding walkthrough](../audits/SELF_SERVICE_OPERATOR_ONBOARDING_WALKTHROUGH_2026-07-23.md),
[`pyproject.toml`](../../pyproject.toml) и
[process package](../../process/package.yaml).

Общий порядок от установки до первого рабочего шага:
[self-service маршрут](self-service-entrypoint.md).

<!-- faq-question: installed-sdd -->

## Что требуется

- Python 3.11 или новее.
- Доверенный checkout или утверждённый release/source package `sdd-process`.
- Возможность установить зависимости `PyYAML` и `jsonschema` из разрешённого
  package source или корпоративного mirror.
- Локальный путь без секретов и корпоративных выгрузок.

Текущий внешний пакет проверен на Windows и имеет отдельные Linux/WSL2
ограничения, перечисленные в [roadmap](roadmap.md). macOS не сертифицирован.

## 1. Создайте изолированное окружение

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

POSIX shell:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Не храните окружение в Git. Если корпоративная политика запрещает обновление
`pip` или доступ в сеть, используйте утверждённый mirror и зафиксированный
процесс установки команды.

## 2. Установите пакет

Из корня доверенного source package:

```text
python -m pip install .
```

Либо укажите утверждённый локальный путь:

```text
python -m pip install <path-to-approved-sdd-process>
```

Не устанавливайте package из случайного URL и не передавайте credentials
через аргументы команды.

## 3. Проверьте identity и entrypoint

Для человека:

```text
sdd --help
```

Для записываемой или AI-readable проверки:

```text
sdd --version --json
```

Успешный JSON содержит:

```json
{
  "operation": "sdd-version",
  "package": {
    "id": "sdd-process",
    "version": "<installed-version>"
  },
  "status": "ok"
}
```

Версия должна совпадать с версией, принятой вашей командой. Сам факт запуска
`sdd` не подтверждает совместимость конкретного workspace — это проверяется
при setup/update.

## 4. Проверьте доступные команды

```text
sdd --help
sdd op list --json
```

Ожидается, что help показывает `setup`, `start`, `next`, `op`, `check`,
`prepare`, `request` и `run`. Каталог операций сообщает mutation class,
разрешённые роли, evidence и human decision boundary.

## Если установка не сработала

| Симптом | Проверка | Действие |
| --- | --- | --- |
| `python` не найден | `python --version` или `python3 --version` | Установить/разрешить Python 3.11+ через корпоративный канал |
| `sdd` не найден после install | `python -m pip show sdd-process` | Активировать то же venv, куда установлен package; не копировать launcher вручную |
| Dependency download запрещён | Посмотреть ошибку `pip` без публикации secrets | Использовать утверждённый mirror/offline wheelhouse |
| Версия не та | `sdd --version --json` | Остановиться и использовать controlled update/rollback runbook |
| Help работает, setup блокируется | Сохранить JSON-вывод setup | Перейти к [setup troubleshooting](setup-and-topology.md#если-setup-заблокирован) |

## Следующий шаг

После успешной проверки владелец процесса создаёт
[центральное workspace](setup-and-topology.md). Если workspace уже существует,
откройте [runbook своей роли](roles/index.md).
