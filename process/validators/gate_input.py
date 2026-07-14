"""Versioned schema validation for gate and lifecycle CLI input."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_NAME = "gate-evaluation-input.schema.json"
LIFECYCLE_STATES = (
    "draft", "spec_review", "approved", "in_implementation",
    "ready_to_archive", "archived",
)
_LIFECYCLE_TRANSITIONS = {
    "draft": ("spec_review",),
    "spec_review": ("draft", "approved"),
    "approved": ("in_implementation",),
    "in_implementation": ("ready_to_archive",),
    "ready_to_archive": ("in_implementation", "archived"),
    "archived": (),
}


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
    diagnostics.extend(_lifecycle_history_diagnostics(document))
    return sorted(
        diagnostics, key=lambda item: (item["pointer"], item["code"])
    )


def _pointer(parts: Any) -> str:
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "/" + "/".join(encoded) if encoded else "/"


def lifecycle_state_was_reached(
    current_state: Any,
    history: Any,
    evaluation_date: Any,
    due_state: Any,
    lifecycle_states: tuple[str, ...],
) -> bool | None:
    """Return monotonic reached-state evidence, or None when it is unknowable."""
    if current_state not in lifecycle_states or due_state not in lifecycle_states:
        return None
    if lifecycle_states.index(current_state) >= lifecycle_states.index(due_state):
        return True
    records = _validated_history_records(
        current_state, history, evaluation_date, lifecycle_states
    )
    if records is None:
        return None
    return any(
        lifecycle_states.index(record["state"]) >= lifecycle_states.index(due_state)
        for record in records
    )


def _lifecycle_history_diagnostics(document: Any) -> list[dict[str, str]]:
    if not isinstance(document, dict) or "lifecycle_history" not in document:
        return []
    history = document.get("lifecycle_history")
    records = history.get("reached_states") if isinstance(history, dict) else None
    diagnostics: list[dict[str, str]] = []
    if isinstance(records, list):
        identifiers = [
            record.get("id") for record in records if isinstance(record, dict)
        ]
        if len(identifiers) != len(set(identifiers)):
            diagnostics.append({
                "code": "gate.lifecycle-history-id-duplicate",
                "pointer": "/lifecycle_history/reached_states",
                "message": "Lifecycle history record identifiers must be unique.",
            })
    if _validated_history_records(
        document.get("status"),
        history,
        document.get("evaluation_date"),
        LIFECYCLE_STATES,
    ) is None:
        diagnostics.append({
            "code": "gate.lifecycle-history-inconsistent",
            "pointer": "/lifecycle_history/reached_states",
            "message": (
                "Lifecycle history must be chronological, canonical, current-state "
                "consistent, source-linked, and human-recorded."
            ),
        })
    return diagnostics


def _validated_history_records(
    current_state: Any,
    history: Any,
    evaluation_date: Any,
    lifecycle_states: tuple[str, ...],
) -> list[dict[str, Any]] | None:
    if (
        not isinstance(history, dict)
        or set(history) != {"schema_version", "reached_states"}
        or history.get("schema_version") != "1.0"
        or not isinstance(history.get("reached_states"), list)
        or not history["reached_states"]
        or current_state not in lifecycle_states
    ):
        return None
    try:
        evaluated = date.fromisoformat(evaluation_date)
    except (TypeError, ValueError):
        return None
    records = history["reached_states"]
    identifiers: set[str] = set()
    previous_time: datetime | None = None
    previous_state: str | None = None
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "id", "state", "reached_at", "source_ref", "recorded_by"
        }:
            return None
        identifier = record.get("id")
        state = record.get("state")
        authority = record.get("recorded_by")
        if (
            not isinstance(identifier, str)
            or not identifier
            or identifier in identifiers
            or state not in lifecycle_states
            or not isinstance(record.get("source_ref"), str)
            or not record["source_ref"].strip()
            or not isinstance(authority, dict)
            or set(authority) != {"type", "id"}
            or authority.get("type") != "human"
            or not isinstance(authority.get("id"), str)
            or not authority["id"].strip()
        ):
            return None
        try:
            reached_at = datetime.fromisoformat(
                str(record.get("reached_at")).replace("Z", "+00:00")
            )
        except (TypeError, ValueError):
            return None
        if (
            reached_at.tzinfo is None
            or reached_at.date() > evaluated
            or (previous_time is not None and reached_at <= previous_time)
            or (
                previous_state is not None
                and state not in _LIFECYCLE_TRANSITIONS.get(previous_state, ())
            )
        ):
            return None
        identifiers.add(identifier)
        previous_time = reached_at
        previous_state = state
    return records if previous_state == current_state else None
