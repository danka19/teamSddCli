## 1. Канонический skill package

- [x] 1.1 Добавить короткий `process/agent-skills/README.md` с canonical/projection и offline-правилами
- [x] 1.2 Добавить 24 самодостаточных `teamssd-*` skill каталога без глобальных зависимостей
- [x] 1.3 Зарегистрировать `agent-skills` в `process/package.yaml`

## 2. Runtime projection

- [x] 2.1 Добавить точную Codex-проекцию в `.agents/skills/`
- [x] 2.2 Документировать создание отдельных будущих runtime-проекций, включая `.gigacode/skills/`

## 3. Project guidance

- [x] 3.1 Обновить `AGENTS.md`, README, file structure и audit под repo-local package
- [x] 3.2 Удалить противоречащее правило об исключительно глобальных workflow-skills

## 4. Ручная проверка

- [x] 4.1 Проверить frontmatter, namespace, repo-local cross-references и совпадение проекции
- [x] 4.2 Просмотреть внешние URL/операции и подтвердить явную остановку перед внешним состоянием
- [x] 4.3 Выполнить OpenSpec, roadmap и diff consistency checks
- [x] 4.4 Зафиксировать отсутствие тестов по решению владельца и перевести change в `pending_acceptance`
