## ADDED Requirements

### Requirement: Navigable product FAQ
The product SHALL publish one concise Russian-language FAQ hub that links to focused pages for product purpose, comparison with OpenSpec/OpenSpec DE, NIS foundation, accepted `sdd` usage, setup, topology, daily workflow, role guides, AI usage, troubleshooting and plain-language roadmap. The hub SHALL NOT require a first-time user to read source code or OpenSpec artifacts to understand where to begin.

#### Scenario: First-time user finds a starting route
- **WHEN** a person opens the FAQ hub without prior framework knowledge
- **THEN** the page explains what the product is, who it is for, what it does not automate and links to a role-appropriate first action

#### Scenario: Specialized answer is reachable
- **WHEN** a person asks about setup, a change class, AI, a failed command or a corporate pilot
- **THEN** the FAQ hub links to a focused page that answers the question and points to its canonical detailed source

### Requirement: FAQ explains the accepted self-service CLI
The FAQ SHALL describe `sdd` as the supported operator entrypoint and SHALL explain `sdd setup`, `sdd start`, `sdd next`, `--json`, human-readable output and the `sdd run` fail-closed boundary. It SHALL identify `add-self-service-operator-onboarding` as the canonical source for this command contract and SHALL NOT direct ordinary users to discover `scripts/*.py` paths.

#### Scenario: First-time operator starts without knowing scripts
- **WHEN** a new operator follows the setup and first-workflow page
- **THEN** the page gives an explicit `sdd setup <destination> --confirm` or `sdd start` command appropriate to the situation and explains its expected non-external result

#### Scenario: User reaches a blocked operation
- **WHEN** the FAQ explains a release or external-operation step
- **THEN** it states that `sdd run` remains fail-closed and routes the user to the required human-owned evidence or future accepted automation change

### Requirement: Исполнимый маршрут первого запуска

FAQ SHALL содержать отдельные связанные страницы для prerequisites и
installation, workspace setup/topology и первого synthetic `minor` route.
Installation page SHALL указывать поддерживаемую версию Python, установку из
approved package source, `sdd --version --json` и маршрут при сбое. Setup page
SHALL показывать полученную topology `process/` и `team-specs/`, объяснять
пустой destination и отличать central workspace от optional project adapter.
First-change page SHALL для каждого шага называть actor, command, expected
result, evidence, handoff и текущий stop point.

#### Scenario: Новый владелец процесса готовит рабочее пространство

- **WHEN** человек начинает с доверенного локального package source
- **THEN** документация позволяет установить `sdd`, проверить package identity, безопасно выполнить confirmation-gated setup и увидеть точный следующий маршрут без чтения исходного кода

#### Scenario: Публичный CLI достигает границы мутации

- **WHEN** first-change tutorial доходит до создания change, lifecycle transition, release или external action
- **THEN** tutorial явно останавливается на human-owned/specialist route, не утверждает несуществующую автоматизацию и сохраняет `sdd run` fail-closed

### Requirement: Plain-language product and roadmap explanation
The FAQ SHALL explain the framework's value and its difference from OpenSpec and OpenSpec DE in practical terms. It SHALL include a short status view using `available now`, `planned`, and `intentionally blocked` language instead of internal phase or artifact terminology.

#### Scenario: User distinguishes framework layers
- **WHEN** a user reads the comparison page
- **THEN** it explains that OpenSpec records specification changes, while this framework adds governed role workflow, deterministic checks, evidence, topology and safe AI assistance without claiming to replace OpenSpec

### Requirement: NIS foundation is explained without importing an organization model
The FAQ SHALL explain that the target process takes NIS-aligned engineering controls as its foundation: flat `minor`/`major`/`hotfix` classification, class-aware DoR/DoD, explicit Tech Lead governance, regression/scope/stop/escalation/release controls, role-understanding evidence and failed-run retention. It SHALL also state that the framework does not copy PPRB or other NIS organizational structure as a target architecture.

#### Scenario: User understands what was adopted from NIS
- **WHEN** a user opens the NIS foundation page
- **THEN** it distinguishes adopted process controls from excluded organizational models and links to the canonical corporate-process decision/source

#### Scenario: User sees an honest status
- **WHEN** a user reads the roadmap page
- **THEN** completed, planned and unavailable capabilities are distinguishable and each unavailable automation boundary is explicit

### Requirement: Role-oriented start runbooks
The documentation SHALL provide separate start pages for Analyst, Tech Lead, Developer, QA and process owner. Each page SHALL state the role's purpose, inputs, first `sdd` command, expected result, human decisions, evidence responsibilities, fallback and escalation route. The process-owner page SHALL use confirmation-gated `sdd setup`; work-role pages SHALL use `sdd start` or `sdd next` before lower-level operations.

#### Scenario: Developer starts implementation safely
- **WHEN** a Developer opens the role runbook for an approved change
- **THEN** it identifies the bounded read context, the next command, required implementation evidence and the point where the Developer must stop for another role

#### Scenario: Process owner sets up a team
- **WHEN** a process owner follows the setup runbook
- **THEN** it explains central `team-specs`, project adapters, non-secret configuration, required confirmation and how to perform a first minor-change walkthrough

#### Scenario: Ролевая страница пригодна как рабочая инструкция

- **WHEN** человек открывает runbook своей роли без чтения OpenSpec contract
- **THEN** он видит prerequisites/inputs, numbered route, expected result, evidence, decisions and authority limits, handoff, failures/fallback/escalation, AI mode and a completion checklist

### Requirement: AI collaboration rules
The FAQ SHALL answer whether AI can operate `sdd`, whether AI can guide the process without invoking a command, and which rules constrain both cases. It SHALL state that AI can invoke permitted local commands with `--json` or explain deterministic output when acting under a human's authorized role, but SHALL NOT create authority, supply `--confirm` as a substitute for human confirmation, confirm decisions, invent missing facts, bypass a gate, perform forbidden external mutations or claim an unrun validation passed.

#### Scenario: AI uses a permitted command
- **WHEN** a human asks an AI assistant to continue an authorized local route
- **THEN** the documentation directs the assistant to invoke or report the relevant `sdd` result, preserve its authority boundary and request human confirmation where required

#### Scenario: AI guides without a command
- **WHEN** an AI explains the next process step without invoking `sdd`
- **THEN** the documentation requires it to label the explanation as guidance, link or refer to the canonical route, and not represent the lifecycle or evidence as changed

#### Scenario: AI encounters uncertainty or unavailable tooling
- **WHEN** facts, an AI tool or an integration are unavailable
- **THEN** the documentation directs the user to the deterministic manual fallback and prohibits fabricated completion or silent defaults

#### Scenario: Человек начинает безопасную AI-сессию

- **WHEN** человек хочет получить guidance или разрешает локальный `sdd` вызов
- **THEN** документация даёт готовый prompt pattern с ролью, задачей, bounded context, allowed command class, `--json`, privacy boundary, expected report and human stop point

### Requirement: FAQ coverage and navigation validation
The documentation set SHALL maintain a checked index of required questions and links. Required questions include product purpose, benefits, OpenSpec/OpenSpec DE comparison, NIS foundation and exclusions, installed `sdd`, `setup`, `start`, `next`, JSON/human output, direct-script compatibility, lifecycle, change classes, AI permissions, AI prohibitions, evidence, CI, privacy, failures, release boundary, corporate pilot, updates and support/escalation.

#### Scenario: A required answer is missing
- **WHEN** documentation validation finds an absent required question, broken internal link or missing canonical reference
- **THEN** it fails with the affected FAQ page and question identifier

#### Scenario: Маркер существует без рабочей инструкции

- **WHEN** обязательная getting-started, role or AI page не содержит требуемых task-oriented sections
- **THEN** deterministic documentation validation fails even if all HTML question markers and Markdown links exist
