#!/usr/bin/env python3
"""Validate navigation and mandatory safety coverage in the product FAQ."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_QUESTIONS = {
    "product-purpose",
    "benefits",
    "openspec-comparison",
    "nis-foundation",
    "installed-sdd",
    "setup",
    "start-next",
    "json-output",
    "topology",
    "lifecycle",
    "change-classes",
    "evidence-ci",
    "ai-permissions",
    "ai-analyst-discovery",
    "ai-prohibitions",
    "privacy",
    "failure-escalation",
    "release-boundary",
    "corporate-pilot",
    "updates-support",
    "analytics-publication-roadmap",
}
REQUIRED_PAGES = {
    "ai-collaboration.md",
    "daily-workflow.md",
    "first-change.md",
    "first-change-with-ai.md",
    "first-change-without-ai.md",
    "glossary.md",
    "index.md",
    "installation.md",
    "nis-foundation.md",
    "product-and-foundation.md",
    "roadmap.md",
    "setup-and-topology.md",
    "troubleshooting-and-boundaries.md",
}
REQUIRED_INDEX_TARGETS = (REQUIRED_PAGES - {"index.md"}) | {"roles/index.md"}
ROLE_SECTIONS = {
    "## Когда использовать",
    "## Что нужно до начала",
    "## Пошаговый маршрут",
    "## Ожидаемый результат",
    "## Доказательства",
    "## Решения и границы",
    "## Передача работы",
    "## Сбои, fallback и эскалация",
    "## Работа с AI",
    "## Чек-лист завершения",
}
WALKTHROUGH_SECTIONS = {
    "first-change-with-ai.md": {
        "## Сначала простая фраза: аналитическое интервью",
        "## Учебная задача и точный scope",
        "## Перед началом: staged permissions",
        "## Стартовый prompt",
        "## Шаг 1. AI собирает evidence из repository",
        "## Шаг 2. AI предлагает `minor`, не подтверждая его",
        "## Шаг 3. AI запускает guided start",
        "## Шаг 4. AI создаёт только неавторитетный request",
        "## Шаг 5. Человек создаёт change package",
        "## Шаг 6. AI готовит classification evidence",
        "## Шаг 7. Tech Lead подтверждает class",
        "## Шаг 8. Developer выполняет один exact edit",
        "## Шаг 9. AI продолжает change и передаёт QA",
        "## Шаг 10. AI подготавливает review, но не публикует",
        "## Что именно подтверждает человек",
        "## Если AI или инструмент недоступен",
    },
    "first-change-without-ai.md": {
        "## Учебная задача и точный scope",
        "## Шаг 1. Проверить source и baseline",
        "## Шаг 2. Собрать признаки candidate `minor`",
        "## Шаг 3. Подготовить workspace",
        "## Шаг 4. Analyst запускает guided route",
        "## Шаг 5. Analyst создаёт неавторитетный request",
        "## Шаг 6. Человек создаёт change package",
        "## Шаг 7. Заполнить и проверить classification evidence",
        "## Шаг 8. Developer выполняет один exact edit",
        "## Шаг 9. Developer и QA получают continuation",
        "## Шаг 10. Подготовить review без публикации",
        "## Где текущая автоматизация останавливается",
        "## Что считать успешным walkthrough",
    },
}
DISCOVERY_TOKENS = {
    "Помоги разобраться и оформить новую идею",
    "по одному вопросу",
    "`confirmed`",
    "`proposed`",
    "`unknown`",
    "`conflict`",
    "показать первую команду",
}
PAIRED_WALKTHROUGH_TOKENS = {
    "process/operation_dispatcher.py",
    "_render_human",
    "lines",
    "output_lines",
    "test_start_human_renderer_uses_the_same_next_command",
    '--title "Rename internal renderer list variable"',
    "sdd start new-requirement --role Analyst --fact classification=minor --json",
    "sdd request create-change --role Analyst --json",
    'sdd check classify-change --role "Tech Lead"',
    "--role Developer --json",
    "--role QA --json",
    "sdd prepare prepare-spec-pr --role Developer",
    "evidence/baseline-test.txt",
    "decisions/impact-review.md",
    "spec_change.required: false",
    "decisions/classification.md",
    "Классификатор не доказывает",
}
WALKTHROUGH_INSTANCE_TOKENS = {
    "first-change-with-ai.md": {
        "C:/work/teamSddCli-ai",
        "C:/work/faq-walkthrough-ai",
        "sample-minor-ai-001",
    },
    "first-change-without-ai.md": {
        "C:/work/teamSddCli-manual",
        "C:/work/faq-walkthrough-manual",
        "sample-minor-manual-001",
    },
}
REQUIRED_ROADMAP_TOKENS = frozenset(
    {
        "## Как читать roadmap",
        "## Работает сейчас",
        "## Следующее",
        "## Запланировано",
        "## Намеренно недоступно",
        "### Полная аналитика ФП и страницы релизных инкрементов",
        "define-fp-analytics-publication-model",
        "0/70",
        "одна полная актуальная страница",
        "отдельная страница каждого релизного инкремента",
        "AI Analyst Discovery",
        "proposal.md",
        "design.md",
        "spec.md",
        "tasks.md",
    }
)
LINK = re.compile(r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)")
UNSAFE_AI_AUTHORITY_PATTERNS = (
    re.compile(
        r"\b(?:AI|ИИ)\s+(?:может|вправе|должен|разрешено)\b"
        r"(?=[^.\n]{0,120}\b"
        r"(?:подтверд\w*|одобр\w*|приня\w*|выполн\w*|измен\w*)\b)"
        r"(?=[^.\n]{0,120}\b"
        r"(?:классификац\w*|DoR|DoD|waiver\w*|риск\w*|release\w*|"
        r"релиз\w*|archive\w*|архив\w*|merge\w*|lifecycle\w*|"
        r"external\s+mutation)\b)"
        r"[^.\n]*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bAI\s+(?:can|may)\b[^.\n]{0,120}\b"
        r"(?:approve|confirm|accept|grant)\b",
        re.IGNORECASE,
    ),
)


def validate_product_faq(root: Path) -> list[str]:
    faq = root / "docs" / "faq"
    pages = sorted(faq.rglob("*.md")) if faq.is_dir() else []
    errors: list[str] = []
    if not pages:
        return ["FAQ directory is missing"]

    found_pages = {page.name for page in pages if page.parent == faq}
    errors += [
        f"required page is missing: {name}"
        for name in sorted(REQUIRED_PAGES - found_pages)
    ]

    index = faq / "index.md"
    if index.is_file():
        index_targets = set(LINK.findall(index.read_text(encoding="utf-8")))
        errors += [
            f"hub link is missing: {target}"
            for target in sorted(REQUIRED_INDEX_TARGETS - index_targets)
        ]

    content = "\n".join(page.read_text(encoding="utf-8") for page in pages)
    found = set(re.findall(r"<!-- faq-question: ([a-z0-9-]+) -->", content))
    errors += [f"required question is missing: {q}" for q in sorted(REQUIRED_QUESTIONS - found)]

    for page in pages:
        text = page.read_text(encoding="utf-8")
        if "Канонический источник:" not in text:
            errors.append(f"canonical reference is missing: {page.relative_to(root)}")
        for target in LINK.findall(text):
            if not (page.parent / target).resolve().is_file():
                errors.append(f"broken link: {page.relative_to(root)} -> {target}")

        if page.parent == faq / "roles" and page.name != "index.md":
            for section in sorted(ROLE_SECTIONS):
                if section not in text:
                    errors.append(
                        "role runbook section is missing: "
                        f"{page.relative_to(root)} -> {section}"
                    )
        if page.name in WALKTHROUGH_SECTIONS:
            for section in sorted(WALKTHROUGH_SECTIONS[page.name]):
                if section not in text:
                    errors.append(
                        "first-change section is missing: "
                        f"{page.relative_to(root)} -> {section}"
                    )
            for token in sorted(PAIRED_WALKTHROUGH_TOKENS):
                if token not in text:
                    errors.append(
                        "paired first-change token is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
            for token in sorted(WALKTHROUGH_INSTANCE_TOKENS[page.name]):
                if token not in text:
                    errors.append(
                        "first-change practice instance is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
            if "--json?" in text:
                errors.append(
                    f"copy-paste command contains punctuation: {page.relative_to(root)}"
                )
        if page.name in {"ai-collaboration.md", "first-change-with-ai.md"}:
            for token in sorted(DISCOVERY_TOKENS):
                if token not in text:
                    errors.append(
                        "AI discovery token is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )
        if page.name == "roadmap.md":
            for token in sorted(REQUIRED_ROADMAP_TOKENS):
                if token not in text:
                    errors.append(
                        "roadmap capability detail is missing: "
                        f"{page.relative_to(root)} -> {token}"
                    )

    if any(pattern.search(content) for pattern in UNSAFE_AI_AUTHORITY_PATTERNS):
        errors.append("unsafe AI authority wording")
    if "Status: completed." in content:
        errors.append("stale status claim")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors = validate_product_faq(args.root)
    payload = {
        "operation": "validate-product-faq",
        "status": "valid" if not errors else "invalid",
        "errors": errors,
    }
    print(
        json.dumps(payload, ensure_ascii=False, sort_keys=True)
        if args.json
        else "Product FAQ: " + payload["status"]
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
