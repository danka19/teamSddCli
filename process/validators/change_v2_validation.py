"""Pure cross-record integrity checks for schema-v2 change metadata."""

from __future__ import annotations

from typing import Any

from .config_validation import Diagnostic


def change_v2_integrity_diagnostics(
    document: dict[str, Any], source: str = "change-v2"
) -> list[Diagnostic]:
    """Check integrity JSON Schema cannot express without computing a class."""
    evidence = document.get("classification_evidence", [])
    identifiers = [
        item.get("id") for item in evidence if isinstance(item, dict)
    ]
    seen: set[Any] = set()
    for index, identifier in enumerate(identifiers):
        if identifier in seen:
            return [Diagnostic(
                "change.evidence-id-duplicate",
                "integrity",
                "Classification evidence identifiers must be unique.",
                6,
                source=source,
                pointer=f"/classification_evidence/{index}/id",
                hint="Keep one source-linked record per evidence identifier.",
            )]
        seen.add(identifier)
    return []
