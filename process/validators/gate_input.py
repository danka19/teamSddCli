"""Versioned schema validation for gate and lifecycle CLI input."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_NAME = "gate-evaluation-input.schema.json"


def validate_gate_input(document: Any, process_root: Path) -> list[dict[str, str]]:
    """Return stable, path-redacted diagnostics for the packaged input contract."""
    try:
        root = process_root.resolve(strict=True)
        schema_path = (root / "schemas" / SCHEMA_NAME).resolve(strict=True)
        schema_path.relative_to(root)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return [{
            "code": "gate.input-schema-unavailable",
            "pointer": "/",
            "message": "The pinned local gate-input schema is unavailable or invalid.",
        }]

    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(document),
        key=lambda error: (list(error.absolute_path), error.validator, error.message),
    )
    diagnostics = [{
        "code": "gate.input-schema-invalid",
        "pointer": _pointer(error.absolute_path),
        "message": "Gate input does not satisfy the pinned schema.",
    } for error in errors]
    if isinstance(document, dict) and isinstance(document.get("evidence"), list):
        identifiers = [
            row.get("id") for row in document["evidence"] if isinstance(row, dict)
        ]
        if len(identifiers) != len(set(identifiers)):
            diagnostics.append({
                "code": "gate.evidence-id-duplicate",
                "pointer": "/evidence",
                "message": "Evidence identifiers must be unique.",
            })
    return sorted(
        diagnostics, key=lambda item: (item["pointer"], item["code"])
    )


def _pointer(parts: Any) -> str:
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded) if encoded else "/"
