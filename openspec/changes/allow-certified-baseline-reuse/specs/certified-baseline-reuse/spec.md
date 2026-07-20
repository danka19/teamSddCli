## ADDED Requirements

### Requirement: Проверяемое переиспользование сертифицированной model matrix
Процесс SHALL разрешать successor release candidate ссылаться на полную
сертифицированную model matrix предыдущего package version только при
детерминированно проверенном совпадении AI-контракта и свежем ограниченном
preflight.

#### Scenario: Совместимый successor использует baseline matrix
- **WHEN** successor package изменяет версию или не-AI workflow, а adapter,
  role instruction, model catalog, response schema и model-operation plan
  совпадают с baseline по зарегистрированным SHA-256; изменённый launcher/read-pack
  слой проходит свежий preflight на текущей версии
- **THEN** release evidence связывает candidate с baseline matrix и свежим
  preflight, указывает причину reuse и проходит только после проверки всех
  этих полей

#### Scenario: Изменение AI-контракта требует полной matrix
- **WHEN** хотя бы один обязательный AI-contract SHA-256 не совпадает с
  baseline либо свежий preflight отсутствует или не проходит
- **THEN** validator fail-closed отклоняет baseline reuse и требует новую
  полную matrix для каждого выбранного model family

#### Scenario: Историческое evidence остаётся неизменяемым
- **WHEN** baseline reuse проходит проверку
- **THEN** старые normalized evidence и raw artifacts не переписываются, а
  successor evidence содержит отдельную ссылку на них и собственные hashes
