"""Contract tests for the navigable product FAQ and role runbooks."""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

ROLE_SECTIONS = (
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
)


def test_readme_keeps_a_human_readable_utf8_faq_entrypoint() -> None:
    readme = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    assert "## Начать с FAQ" in readme
    assert "`r`n" not in readme
    assert "РўРµ" not in readme


def test_product_faq_contract_is_valid() -> None:
    from scripts.validate_product_faq import validate_product_faq
    assert validate_product_faq(ROOT) == []


def test_nis_foundation_page_explains_positive_adoption_route() -> None:
    faq = ROOT / "docs" / "faq"
    page = (faq / "nis-foundation.md").read_text(encoding="utf-8")
    assert "## Что уже взято из НИС" in page
    assert "## Как это адаптировано в teamSddCli" in page
    assert "## Что планируется перенести дальше" in page
    assert "## Что не взято" not in page
    assert (
        "Переносимые process controls и роли не привязывают целевую архитектуру "
        "к PPRB или другой организационной модели НИС."
    ) in page
    assert "nis-foundation.md" in (faq / "index.md").read_text(encoding="utf-8")


def test_getting_started_pages_are_executable_and_linked() -> None:
    faq = ROOT / "docs" / "faq"
    index = (faq / "index.md").read_text(encoding="utf-8")
    for name in (
        "installation.md",
        "setup-and-topology.md",
        "first-change.md",
        "first-change-with-ai.md",
        "first-change-without-ai.md",
        "glossary.md",
    ):
        assert f"]({name})" in index

    installation = (faq / "installation.md").read_text(encoding="utf-8")
    for token in (
        "Python 3.11",
        "python -m pip install",
        "sdd --version --json",
        "## Если установка не сработала",
    ):
        assert token in installation

    first_change = (faq / "first-change.md").read_text(encoding="utf-8")
    with_ai = (faq / "first-change-with-ai.md").read_text(encoding="utf-8")
    without_ai = (faq / "first-change-without-ai.md").read_text(encoding="utf-8")
    assert "## Проход 1 — вместе с AI" in first_change
    assert "## Проход 2 — без AI" in first_change
    assert first_change.index("first-change-with-ai.md") < first_change.index(
        "first-change-without-ai.md"
    )
    assert index.index("first-change-with-ai.md") < index.index(
        "first-change-without-ai.md"
    )

    paired_tokens = (
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
        "python -m pytest tests/test_self_service_onboarding.py::test_start_human_renderer_uses_the_same_next_command -q",
        "evidence/baseline-test.txt",
        "decisions/impact-review.md",
        "spec_change.required: false",
        "decisions/classification.md",
        "Классификатор не доказывает",
    )
    for token in paired_tokens:
        assert token in with_ai
        assert token in without_ai

    for token in (
        "C:/work/teamSddCli-ai",
        "C:/work/faq-walkthrough-ai",
        "sample-minor-ai-001",
    ):
        assert token in with_ai
        assert token not in without_ai
    for token in (
        "C:/work/teamSddCli-manual",
        "C:/work/faq-walkthrough-manual",
        "sample-minor-manual-001",
    ):
        assert token in without_ai
        assert token not in with_ai

    for token in (
        "## Стартовый prompt",
        "## Шаг 1. AI собирает evidence из repository",
        "Сопоставь все 17 minor-condition IDs",
        "Выполняй только эту команду",
        "classification.human-confirmation-required",
        "Разрешаю только показанный rename внутри _render_human",
        "## Что именно подтверждает человек",
        "Ответ `Выполняй` относится только к показанной команде",
        "[тому же маршруту без AI](first-change-without-ai.md)",
    ):
        assert token in with_ai

    assert "## Где текущая автоматизация останавливается" in without_ai
    assert "--json?" not in with_ai
    assert "--json?" not in without_ai
    assert "behavior_change" not in with_ai
    assert "behavior_change" not in without_ai
    assert "--type refactor" in with_ai
    assert "--type refactor" in without_ai


def test_every_role_page_is_a_complete_start_runbook() -> None:
    roles = ROOT / "docs" / "faq" / "roles"
    for name in (
        "analyst.md",
        "tech-lead.md",
        "developer.md",
        "qa.md",
        "process-owner.md",
    ):
        text = (roles / name).read_text(encoding="utf-8")
        for section in ROLE_SECTIONS:
            assert section in text, f"{name}: missing {section}"


def test_product_ai_roadmap_and_troubleshooting_are_practical() -> None:
    faq = ROOT / "docs" / "faq"
    product = (faq / "product-and-foundation.md").read_text(encoding="utf-8")
    assert "| Вопрос | OpenSpec | OpenSpec DE | teamSddCli |" in product
    assert "## Кому подходит" in product
    assert "## Когда продукт не нужен" in product

    ai = (faq / "ai-collaboration.md").read_text(encoding="utf-8")
    for token in (
        "## Режим `analyst-discovery`: от сырой идеи к черновику",
        "Помоги разобраться и оформить новую идею",
        "сначала покажет темы интервью",
        "по одному вопросу",
        "`confirmed`",
        "`proposed`",
        "`unknown`",
        "`conflict`",
        "## Режим 1: AI только объясняет",
        "## Режим 2: AI запускает разрешённую команду",
        "```text",
        "--json",
        "## Продолжение без AI",
    ):
        assert token in ai

    roadmap = (faq / "roadmap.md").read_text(encoding="utf-8")
    for section in (
        "## Что уже можно сделать",
        "## Что появится следующим",
        "## Что планируется позже",
        "## Что намеренно не автоматизировано",
    ):
        assert section in roadmap

    troubleshooting = (faq / "troubleshooting-and-boundaries.md").read_text(encoding="utf-8")
    assert "| Симптом | Что это обычно означает | Что делать |" in troubleshooting


def test_ai_walkthrough_starts_with_plain_language_discovery() -> None:
    page = (ROOT / "docs" / "faq" / "first-change-with-ai.md").read_text(
        encoding="utf-8"
    )
    plain = "Помоги оформить небольшое изменение. Сначала помоги разобраться"
    assert plain in page
    assert page.index(plain) < page.index("## Стартовый prompt")
    for token in (
        "план тем",
        "Можно пройти по этим темам?",
        "по одному вопросу",
        "итоговая сводка",
        "показать первую команду",
    ):
        assert token in page


def test_validator_reports_broken_link(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "index.md").write_text(
        "# FAQ\n[broken](missing.md)\n",
        encoding="utf-8",
    )
    assert any("broken link" in error for error in validate_product_faq(tmp_path))


def test_validator_reports_missing_required_question(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "index.md").write_text("# FAQ\n", encoding="utf-8")
    assert any("required question" in error for error in validate_product_faq(tmp_path))


def test_validator_reports_missing_required_page_and_role_section(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    roles = faq / "roles"
    roles.mkdir(parents=True)
    (faq / "index.md").write_text("# FAQ\nКанонический источник: x\n", encoding="utf-8")
    (roles / "developer.md").write_text(
        "# Developer\nКанонический источник: x\n",
        encoding="utf-8",
    )

    errors = validate_product_faq(tmp_path)
    assert any("required page is missing" in error for error in errors)
    assert any("role runbook section is missing" in error for error in errors)


def test_validator_reports_required_page_not_linked_from_hub(tmp_path: Path) -> None:
    from scripts.validate_product_faq import REQUIRED_PAGES, validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    for name in REQUIRED_PAGES:
        (faq / name).write_text(
            "# Page\nКанонический источник: x\n",
            encoding="utf-8",
        )

    errors = validate_product_faq(tmp_path)
    assert any("hub link is missing: installation.md" in error for error in errors)


def test_validator_requires_complete_paired_first_change_sections(
    tmp_path: Path,
) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "first-change-with-ai.md").write_text(
        "# AI route\nКанонический источник: x\n",
        encoding="utf-8",
    )
    (faq / "first-change-without-ai.md").write_text(
        "# Manual route\nКанонический источник: x\n",
        encoding="utf-8",
    )

    errors = validate_product_faq(tmp_path)
    assert any("first-change section is missing" in error for error in errors)
    assert any("paired first-change token is missing" in error for error in errors)


def test_validator_rejects_stale_or_unsafe_ai_claims(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "index.md").write_text(
        "# FAQ\n<!-- faq-question: product-purpose -->\n"
        "AI can approve releases.\nStatus: completed.\n",
        encoding="utf-8",
    )
    errors = validate_product_faq(tmp_path)
    assert any("unsafe AI authority" in error for error in errors)
    assert any("stale status" in error for error in errors)


@pytest.mark.parametrize(
    "unsafe_claim",
    (
        "AI может подтвердить классификацию.",
        "AI вправе одобрить DoR.",
        "AI может принять риск.",
        "AI может выполнить archive.",
        "AI can approve release.",
    ),
)
def test_validator_rejects_governed_ai_authority_claims(
    tmp_path: Path,
    unsafe_claim: str,
) -> None:
    from scripts.validate_product_faq import validate_product_faq

    faq = tmp_path / "docs" / "faq"
    faq.mkdir(parents=True)
    (faq / "index.md").write_text(
        f"# FAQ\nКанонический источник: x\n{unsafe_claim}\n",
        encoding="utf-8",
    )
    errors = validate_product_faq(tmp_path)
    assert any("unsafe AI authority" in error for error in errors)
