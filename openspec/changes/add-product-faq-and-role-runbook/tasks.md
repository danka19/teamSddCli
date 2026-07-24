## 1. Information architecture and canonical sources
- [x] 1.1 Inventory existing user-facing docs, canonical OpenSpec contracts and specialist runbooks; define the FAQ navigation map and source ownership.
- [x] 1.2 Define the required-question index, stable page identifiers and deterministic link/reference validation.
- [x] 1.3 Add the FAQ hub and concise product, value, OpenSpec/OpenSpec DE comparison and NIS foundation pages.
  Evidence (2026-07-24): `nis-foundation.md` page contract, full FAQ pytest suite and JSON validator passed; the page is a required hub target.

## 2. Setup and daily workflow guides

- [x] 2.1 Add focused pages for installed `sdd`, confirmation-gated `sdd setup`, central `team-specs` topology, project adapters and first-time setup.
- [x] 2.2 Add a plain-language lifecycle, minor/major/hotfix, evidence, CI, failure and escalation guide.
- [x] 2.3 Add an honest plain-language roadmap with available, planned and intentionally blocked capability states.

## 3. Role and AI runbooks

- [x] 3.1 Add role pages for Analyst, Tech Lead, Developer, QA and process owner with `sdd start`/`sdd next` first commands, expected outcome, evidence, boundaries and fallback.
- [x] 3.2 Add the AI collaboration page and permission matrix: permitted `--json` command use, guidance-only mode, human confirmations including `sdd setup --confirm`, prohibited actions and uncertainty fallback.
- [x] 3.3 Add FAQ entries for privacy, release boundary, corporate pilot, process/package update and support/escalation.

## 4. Verification and maintenance

- [x] 4.1 Implement documentation navigation, required-question and canonical-reference validation.
- [x] 4.2 Add positive and negative tests for broken links, missing FAQ coverage, stale status claims and AI-authority wording.
- [x] 4.3 Run documentation checks, relevant regression tests, `openspec validate --all --strict`, roadmap/OpenSpec validation and `git diff --check`.
- [ ] 4.4 Record the user walkthrough of a first-time operator and update the FAQ maintenance ownership/process.

## 5. Content acceptance remediation

- [x] 5.1 Заменить summary-only onboarding связанными страницами installation, setup/topology, first-change и glossary с командами, ожидаемыми результатами, handoff и честными stop points.
- [x] 5.2 Расширить страницы Analyst, Tech Lead, Developer, QA и process owner через единый полный runbook: prerequisites, inputs, нумерованный маршрут, evidence, authority limits, handoff, failure handling, AI и completion checklist.
- [x] 5.3 Расширить product comparison, практическую пользу, AI cookbook, troubleshooting и plain-language roadmap без дублирования нормативной OpenSpec policy.
- [x] 5.4 Усилить deterministic FAQ validation и tests, чтобы наличие markers/links не заменяло обязательные task-oriented sections и smoke documented commands; real-package `sdd next` smoke подтвердил canonical `status` continuation без lifecycle/external mutation.
- [x] 5.5 Добавить парный walkthrough одного synthetic `minor`: сначала AI-first маршрут с candidate classification, exact разрешёнными командами, raw JSON и human confirmations, затем тот же маршрут без AI в отдельной clean practice-копии того же revision; заменить generated placeholders фактическими proposal/design/task/test/decision evidence, сохранить fail-closed mutation boundary и regression coverage структуры/навигации/порядка.
- [ ] 5.6 Перестроить FAQ-roadmap вокруг status legend и человекочитаемых capability-карточек; подробно описать `define-fp-analytics-publication-model`, связь с AI Analyst Discovery и отличия planned design от работающей функции; закрепить карточку validator/tests.
