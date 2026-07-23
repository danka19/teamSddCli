"""Contract tests for the navigable product FAQ and role runbooks."""
from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_product_faq_contract_is_valid() -> None:
    from scripts.validate_product_faq import validate_product_faq
    assert validate_product_faq(ROOT) == []
def test_validator_reports_broken_link(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq
    faq = tmp_path / "docs" / "faq"; faq.mkdir(parents=True); (faq / "index.md").write_text("# FAQ\n[broken](missing.md)\n", encoding="utf-8")
    assert any("broken link" in error for error in validate_product_faq(tmp_path))
def test_validator_reports_missing_required_question(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq
    faq = tmp_path / "docs" / "faq"; faq.mkdir(parents=True); (faq / "index.md").write_text("# FAQ\n", encoding="utf-8")
    assert any("required question" in error for error in validate_product_faq(tmp_path))
def test_validator_rejects_stale_or_unsafe_ai_claims(tmp_path: Path) -> None:
    from scripts.validate_product_faq import validate_product_faq
    faq = tmp_path / "docs" / "faq"; faq.mkdir(parents=True); (faq / "index.md").write_text("# FAQ\n<!-- faq-question: product-purpose -->\nAI can approve releases.\nStatus: completed.\n", encoding="utf-8")
    errors = validate_product_faq(tmp_path); assert any("unsafe AI authority" in e for e in errors); assert any("stale status" in e for e in errors)
