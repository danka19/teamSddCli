## Context

Guided workflow меняет ситуацию, onboarding и read-only guidance, а не
модельные adapter/prompt/schema contracts. Текущий selection schema привязан
к exact package version и поэтому не умеет выразить безопасную связь между
новой версией и неизменённой полной matrix.

## Goals / Non-Goals

**Goals:** выразить reuse как отдельное проверяемое evidence, не допустить
silent reuse и не ослабить authority/retention проверки.

**Non-Goals:** не переименовывать или редактировать rc6, не принимать
candidate автоматически и не разрешать reuse при изменении AI-контракта.

## Decisions

1. В selection вводится явный режим `baseline-reuse`, а не неявное игнорирование
   различия версий.
2. Validator сравнивает allowlisted hashes AI-contract sources и требует
   свежий preflight для каждого model family.
3. Несовпадение любого значения — отказ; fallback не является pass.

## Risks / Trade-offs

- [Слишком широкий reuse] → allowlist точных sources и отрицательные tests.
- [Устаревший preflight] → existing freshness and raw checksum rules remain.
- [Потеря истории] → baseline evidence remains immutable and referenced only.
