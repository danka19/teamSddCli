#!/usr/bin/env python3
"""Validate navigation and mandatory safety coverage in the product FAQ."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
REQUIRED_QUESTIONS = {"product-purpose", "benefits", "openspec-comparison", "nis-foundation", "installed-sdd", "setup", "start-next", "json-output", "topology", "lifecycle", "change-classes", "evidence-ci", "ai-permissions", "ai-prohibitions", "privacy", "failure-escalation", "release-boundary", "corporate-pilot", "updates-support"}
LINK = re.compile(r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)")
def validate_product_faq(root: Path) -> list[str]:
    faq = root / "docs" / "faq"; pages = sorted(faq.rglob("*.md")) if faq.is_dir() else []; errors: list[str] = []
    if not pages: return ["FAQ directory is missing"]
    content = "\n".join(page.read_text(encoding="utf-8") for page in pages); found = set(re.findall(r"<!-- faq-question: ([a-z0-9-]+) -->", content))
    errors += [f"required question is missing: {q}" for q in sorted(REQUIRED_QUESTIONS - found)]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if "Канонический источник:" not in text: errors.append(f"canonical reference is missing: {page.relative_to(root)}")
        for target in LINK.findall(text):
            if not (page.parent / target).resolve().is_file(): errors.append(f"broken link: {page.relative_to(root)} -> {target}")
    if re.search(r"AI can (approve|confirm) (a |)release", content, re.I): errors.append("unsafe AI authority wording")
    if "Status: completed." in content: errors.append("stale status claim")
    return errors
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1]); parser.add_argument("--json", action="store_true"); args = parser.parse_args(argv)
    errors = validate_product_faq(args.root); payload = {"operation": "validate-product-faq", "status": "valid" if not errors else "invalid", "errors": errors}; print(json.dumps(payload, ensure_ascii=False, sort_keys=True) if args.json else "Product FAQ: " + payload["status"]); return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
