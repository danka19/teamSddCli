## Why

Текущий typed analytics framework сохраняет только минимальный набор структурированных артефактов и не определяет, как самостоятельные ФП, их независимые жизненные циклы и составные релизы превращаются в понятную человеку документацию и корпоративные страницы Confluence. Без отдельного контракта команда снова столкнётся со смешением живой аналитики, релизных изменений, сырых OpenSpec-файлов и вручную поддерживаемых вложенных таблиц.

## What Changes

- Для каждой самостоятельной ФП вводится одна полная актуальная страница аналитики, которая показывает текущее принятое состояние ФП и является основной точкой входа для человека.
- Для каждого релиза/инкремента вводится отдельная зафиксированная страница, показывающая состав и изменения именно этого инкремента, включая функциональность из нескольких ФП.
- Git/OpenSpec/Markdown/YAML остаются каноническими источниками; страницы Confluence являются детерминированно генерируемыми read models.
- Вводятся явные FP, capability, change, release и publication manifests, правила владения, cross-FP-ссылок, актуализации живой страницы и фиксации релизных страниц.
- Корпоративный шаблон аналитики раскладывается на типизированные секции с правилами применимости, источниками, renderer contracts и режимами inline/child page.
- Вложенные таблицы хранятся как нормализованные типизированные данные и собираются renderer-ом; вручную поддерживаемые вложенные Markdown/HTML-таблицы не становятся источником.
- Локальный preview использует ту же промежуточную publication model, что и будущая Confluence-публикация, и проверяется golden snapshots.
- Согласованный AI Analyst Discovery Skill включается как upstream authoring flow: он превращает сырую идею в подтверждённую человеком сводку и draft change package, но publication принимает его результат только через reviewed canonical Markdown/YAML/OpenSpec sources.
- AI может помогать заполнять, проверять и объяснять документы, но не определяет владение, применимость, согласование, релизный состав или истинность опубликованного состояния.

## Capabilities

### New Capabilities

- `fp-analytics-publication`: контракт полной актуальной страницы ФП, страниц релизных инкрементов, publication manifests, секционной композиции, вложенных renderer-ов, навигации, актуализации и локального preview.

### Modified Capabilities

- `repo-topology-config`: центральный `team-specs` получает явное пространство ФП и общие каталоги изменений, релизов и публикации без предположения `1 repository = 1 project = 1 FP`.
- `confluence-feedback-loop`: семантический набор generated views фиксируется как актуальная страница ФП плюс страницы релизных инкрементов; корпоративная среда выбирает только технический mapping space/parent/macros и разрешённый способ публикации.
- `traceability-contract`: релизный инкремент связывает изменения нескольких ФП с requirement/scenario IDs, evidence и состоянием включения без копирования нормативного текста.

## Impact

Затрагиваются будущие schemas/templates/validators typed analytics, структура `team-specs`, publication model, локальный preview/renderer, Confluence adapter, каталоги ФП и релизов, cross-FP traceability, role runbooks и документация аналитиков. План зависит от согласованного дизайна `docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md`: discovery skill владеет интервью, truth-status evidence и созданием черновиков, а этот change владеет проверяемым допуском reviewed canonical artifacts в current/release publication. Реальные Confluence API/MCP-вызовы, credentials, корпоративные space IDs, массовая миграция старых страниц и автоматическая публикация не входят в этот proposal до проверки корпоративной среды и отдельного разрешения на реализацию.

## Roadmap

- Execution phase: P5
- Related phases: P3, P4
- Lifecycle status: planned

## Change Intake

```text
Idea: Для каждой ФП поддерживать одну полную актуальную страницу аналитики и отдельную страницу каждого релизного инкремента.
Source: Решение владельца от 2026-07-24 после повторного анализа 38 снимков корпоративного шаблона.
Type: scope_refinement, architecture_change, data_contract_change, documentation_change
Decision: create_openspec_change
Reason: Решение задаёт новые типы generated views, manifests, cross-FP связи, правила актуализации и renderer contracts, поэтому не может оставаться только planning note.
Affected specs: fp-analytics-publication (new), repo-topology-config, confluence-feedback-loop, traceability-contract.
Affected architecture: FP становится единицей владения и человекочитаемой навигации; release increment становится неизменяемым историческим представлением; Confluence остаётся generated read model.
Data contract impact: Нужны FP, capability, release и publication identities, section applicability, typed section sources и cross-FP inclusion records.
Verification impact: Нужны schema/semantic validation, link/traceability checks, current-page reconciliation, immutable increment checks, local rendering parity и golden snapshots сложных таблиц.
Status: Записано в отдельный change; реализация принадлежит P5 и не начата.
```

### Additional intake: AI Analyst Discovery Skill

```text
Idea: Учесть согласованный AI companion skill для аналитического интервью в модели хранения и публикации аналитики.
Source: Решение владельца от 2026-07-24 и docs/superpowers/specs/2026-07-24-ai-analyst-discovery-skill-design.md.
Type: scope_refinement, architecture_change, data_contract_change, verification_change, documentation_change
Decision: adopt_now
Reason: Change ещё находится на стадии proposal; без явного upstream interface discovery drafts могли бы стать параллельным источником или попасть в delivered/current publication без human review.
Affected specs: fp-analytics-publication; role-aware-guided-workflow остаётся внешней зависимостью и не переписывается этим change.
Affected architecture: analyst-discovery -> human-confirmed summary -> draft change package -> guided-change -> accepted/delivered canonical source -> current/release publication.
Data contract impact: Publication различает interaction discovery map и assertion truth evidence confirmed/proposed/unknown/conflict; в delivered body допускаются только reviewed canonical facts.
Verification impact: Нужны negative cases для draft/proposed/unknown/conflict leakage, cross-FP ownership proposals и остановок перед file creation/commands.
Status: Принято в proposal/design/spec/tasks; реализация discovery skill и publication остаётся не начатой.
```
