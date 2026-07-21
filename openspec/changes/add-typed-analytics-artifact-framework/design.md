## Контекст

`D-025` требует typed analytics persistence до framework-readiness. `D-026` ограничивает P3 локальными read-only действиями и passive integration descriptors.

## Цели / Не-цели

**Цели:** семь whole-file YAML contracts, templates, schema/semantic validator, stable cross-references и локальный preview sanitized example.

**Не-цели:** product payment screens, live Jira/Confluence/Bitbucket/Jenkins, MCP, generated corporate views или legacy bulk migration.

## Решения

- `analytics-manifest.yaml` задаёт набор whole-file artifacts; отдельные fixed-name YAML files исключают merge ambiguity.
- Status, channel, data, platform services, journey, screens/assets и integrations имеют JSON Schema; semantic validator проверяет manifest completeness и passive-only integrations.
- Preview возвращает только parsed journey/screens/integrations и пустой список action; он не читает credentials, не делает сеть и не меняет файлы.
- Screens хранят stable ID и asset path; fixture использует synthetic path без продукта/платёжного UI.
- P3 preview является local read model. Генерируемые бизнес/corporate views остаются P5.

## Риски / Компромиссы

- Базовые schemas умышленно компактны → следующие capability changes могут расширять records без копирования UI или integration policy.
- Preview не подтверждает, что asset существует → это отдельный будущий asset-rendering gate; текущая граница сохраняет read-only P3 scope.
