# Analyst: начать разбор требования

Канонический источник: [guided workflow](../../runbooks/GUIDED_OWNER_WORKFLOW.md),
[bounded Analyst instruction](../../../process/roles/analyst.md) и
[role-aware workflow](../../../openspec/specs/role-aware-guided-workflow/spec.md).

## Когда использовать

Используйте этот runbook, когда появляется новое бизнес-требование, меняется
существующее поведение, нужно подготовить Delta Spec либо в change остаются
неразрешённые вопросы о scope, сценариях и ожидаемом результате.

Результат Analyst — один source-linked draft stage и явный список неизвестных.
Analyst не начинает реализацию и не подтверждает classification за Tech Lead.

## Что нужно до начала

- ваша роль подтверждена как `Analyst`;
- известна ситуация: новое требование или существующий change;
- есть безопасный source requirement и stable IDs, если они уже созданы;
- для нового требования есть предложенная, но ещё human-owned classification;
- для existing change известен точный путь и lifecycle state;
- private data и credentials исключены из input/AI context.

Если classification неизвестна, не подставляйте `minor` как default. Сначала
зафиксируйте неизвестность и передайте вопрос Tech Lead.

## Пошаговый маршрут

1. Отделите проверенные факты от предположений и предлагаемого текста.
2. Для нового требования запустите:

   ```text
   sdd start new-requirement --role Analyst --fact classification=<minor|major|hotfix> --json
   ```

3. Проверьте `missing_facts`, `expected_evidence`, `human_decision`,
   `authority_boundary` и `next_command`.
4. Если route guided, подготовьте только указанный intent/draft:

   ```text
   sdd request create-change --role Analyst --json
   ```

5. Пометьте request как неавторитетный: он не создаёт change и не принимает
   classification.
6. Для существующего change используйте:

   ```text
   sdd next --change <path-to-change> --role Analyst --json
   ```

   На real schema-v2 package `sdd next` читает канонический top-level `status`.
   Не добавляйте вручную второе persisted-поле `lifecycle_state`; missing или
   unsupported status остаётся blocker, который нужно сохранить и эскалировать
   по specialist lifecycle runbook.
7. Прочитайте proposal, Delta Spec, traceability и открытые decisions. Не
   переходите в design/implementation, если текущий этап — requirement/spec.
8. Запишите unresolved inputs и остановитесь для human review.

## Ожидаемый результат

- один понятный requirement/Delta draft или корректный blocked result;
- факты и assumptions разделены;
- scenarios описывают observable behavior и negative cases;
- classification остаётся `pending`, пока её не подтвердил Tech Lead;
- в результате нет claims об approval, DoR, implementation или tests;
- следующий human owner и последствие отсутствия решения названы явно.

## Доказательства

Сохраните safe command JSON, source requirement/reference, draft path и digest,
список прочитанных canonical IDs, unresolved inputs, proposed scenarios и
ссылку на classification evidence. Команду или проверку без реального output
записывайте как `not-run`, а не как passed.

## Решения и границы

Analyst может уточнять intent, scope и acceptance wording в пределах своей
ответственности и может подготовить decision draft. Он не должен:

- подтверждать `minor | major | hotfix` за Tech Lead;
- выдавать AI-authored YAML за human acceptance;
- утверждать DoR/DoD, release, archive или tracker Done;
- выбирать default молча при material uncertainty;
- поручать Developer реализацию до readiness.

## Передача работы

Tech Lead получает source requirement, proposed class, Delta draft,
classification evidence, risks и открытые решения. Developer получает content
только после applicable human acceptance и DoR. QA получает stable
requirement/scenario IDs и expected behavior, а не устное резюме без source.

## Сбои, fallback и эскалация

- `missing-context` — добавить только проверяемый факт либо вернуть вопрос его
  владельцу;
- conflicting sources — привести обе ссылки и остановиться;
- AI/model unavailable — продолжить вручную по canonical source и сохранить
  draft/evidence;
- change path отсутствует — запросить точный path у владельца процесса;
- route предлагает implementation CTA Analyst — остановиться и сообщить Tech
  Lead/владельцу процесса: это нарушение role boundary.

## Работа с AI

Без команд:

```text
Ты помогаешь в роли Analyst. Прочитай только перечисленные canonical sources.
Раздели факты, assumptions и open decisions. Подготовь один Delta draft,
не подтверждай classification/DoR и остановись для human review.
```

С разрешённой командой попросите AI выполнить конкретный `sdd ... --json`,
вернуть raw result, объяснить `missing_facts` и не запускать `next_command`
без нового разрешения.

## Чек-лист завершения

- [ ] Роль и change/situation определены.
- [ ] Факты отделены от assumptions.
- [ ] Requirement и scenarios source-linked.
- [ ] Classification не выдана за принятую.
- [ ] Unknowns и risks видимы.
- [ ] Evidence сохранено без secrets.
- [ ] Назван следующий human owner.
- [ ] Работа остановлена до решения/следующего разрешённого этапа.
