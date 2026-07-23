"""Read-only, catalog-backed guidance for a process-package owner."""

from __future__ import annotations

import copy
import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .errors import OperationError
from .operations_catalog import DEFAULT_CATALOG as DEFAULT_OPERATIONS_CATALOG, load_operations_catalog


PACKAGE_ROOT = Path(__file__).resolve().parent
DEFAULT_CATALOG = PACKAGE_ROOT / "catalogs" / "guided-owner-workflow.yaml"
INTERACTIVE_ROLES = {"Analyst", "Tech Lead", "Developer", "QA"}
DECISION_OWNERS = {"Analyst", "Tech Lead", "Change Owner"}  # legacy catalog record only
KNOWN_ROLES = INTERACTIVE_ROLES
SHA256 = re.compile(r"[0-9a-f]{64}")
DISCOVERY_CHOICES = ("углубиться", "принять defaults", "подготовить draft с открытыми решениями")


def load_catalog(path: Path = DEFAULT_CATALOG, *, operations_path: Path = DEFAULT_OPERATIONS_CATALOG) -> dict[str, Any]:
    """Load a small, explicit catalog and reject authority or command drift."""
    operations = {item["id"] for item in load_operations_catalog(operations_path)["operations"]}
    try:
        catalog = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError("catalog-invalid", "guided workflow catalog is unavailable") from error
    if not isinstance(catalog, dict) or catalog.get("schema_version") not in {"1.0", "1.1"}:
        raise OperationError("catalog-invalid", "guided workflow catalog has an unsupported shape")
    routes = catalog.get("routes")
    if not isinstance(routes, list) or not routes:
        raise OperationError("catalog-invalid", "guided workflow catalog has no routes")
    ids: set[str] = set()
    for route in routes:
        if not isinstance(route, dict):
            raise OperationError("catalog-invalid", "guided workflow route is malformed")
        identifier = route.get("id")
        required = route.get("required_facts")
        allowed_values = route.get("allowed_values", {})
        commands = route.get("commands")
        decision = route.get("human_decision")
        fallbacks = route.get("fallbacks")
        if (
            not isinstance(identifier, str) or not identifier or identifier in ids
            or route.get("situation") != identifier
            or not isinstance(required, list) or not all(isinstance(item, str) and item for item in required)
            or not isinstance(allowed_values, dict)
            or any(
                key not in required or not isinstance(values, list) or not values
                or not all(isinstance(value, str) and value for value in values)
                for key, values in allowed_values.items()
            )
            or not isinstance(commands, list) or not commands or not all(isinstance(command, str) and command in operations for command in commands)
            or not isinstance(decision, dict) or not isinstance(decision.get("id"), str)
            or decision.get("owner") not in DECISION_OWNERS
            or not isinstance(decision.get("consequence"), str)
            or not isinstance(fallbacks, list)
        ):
            raise OperationError("catalog-invalid", "guided workflow catalog violates the safe route contract")
        for fallback in fallbacks:
            if not isinstance(fallback, dict) or not isinstance(fallback.get("surface"), str) or not isinstance(fallback.get("command"), str):
                raise OperationError("catalog-invalid", "guided workflow fallback is malformed")
        ids.add(identifier)
    return catalog


def guide(
    situation: str,
    facts: dict[str, str],
    unavailable: set[str],
    *,
    catalog_path: Path = DEFAULT_CATALOG,
    interaction: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return guidance only; callers must invoke each command and gate explicitly."""
    catalog = load_catalog(catalog_path)
    route = next((item for item in catalog["routes"] if item["id"] == situation), None)
    if route is None:
        return _blocked("situation-unknown", [])
    role = facts.get("human_role")
    if not role:
        return _blocked("unknown-role", ["human_role"])
    if role not in KNOWN_ROLES:
        return _blocked("invalid-role", ["human_role"])
    missing = [key for key in route["required_facts"] if not facts.get(key)]
    if missing:
        return _blocked("missing-context", missing)
    invalid = sorted(
        key for key, values in route.get("allowed_values", {}).items()
        if facts[key] not in values
    )
    if invalid:
        return _blocked("invalid-context", invalid)
    fallbacks = [
        {"surface": item["surface"], "command": item["command"]}
        for item in route["fallbacks"] if item["surface"] in unavailable
    ]
    payload = {
        "operation": "guided-owner-workflow",
        "status": "guided",
        "schema_version": "1.0",
        "route_id": route["id"],
        "known_facts": {**{key: facts[key] for key in route["required_facts"]}, "human_role": role},
        "commands": route["commands"],
        "expected_evidence": route["evidence"],
        "human_decision": route["human_decision"],
        "unavailable": sorted(unavailable),
        "cta": _cta(route, role, facts),
        "fallbacks": fallbacks,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }
    if interaction is not None:
        try:
            payload["guided_interaction"] = _guided_interaction(interaction)
        except (TypeError, ValueError):
            return _blocked("invalid-guided-interaction", [])
    return payload


def _cta(route: dict[str, Any], role: str, facts: dict[str, str]) -> str:
    if facts.get("lifecycle_state") == "approved":
        return "monitor-process-status" if role == "Tech Lead" else "validate-readiness-and-prepare-role-pr"
    if role == "Analyst":
        return "prepare-one-draft-and-stop"
    return "follow-catalog-route"


def _blocked(code: str, required_facts: list[str]) -> dict[str, Any]:
    return {
        "operation": "guided-owner-workflow",
        "status": "blocked",
        "schema_version": "1.0",
        "blockers": [{"code": code, "required_facts": required_facts}],
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }


def _guided_interaction(interaction: dict[str, Any]) -> dict[str, Any]:
    """Derive read-only decision and discovery records for an already guided route."""
    if not isinstance(interaction, dict):
        raise ValueError("guided interaction is invalid")
    result: dict[str, Any] = {}
    decision = interaction.get("decision")
    if decision is not None:
        if not isinstance(decision, dict):
            raise ValueError("decision interaction is invalid")
        draft = create_decision_draft(**decision)
        result["decision_draft"] = draft
        confirmation = interaction.get("confirmation_event")
        if confirmation is not None:
            event = confirm_decision_draft(draft, confirmation)
            if event is not None:
                result["confirmation_event"] = event
    elif interaction.get("confirmation_event") is not None:
        raise ValueError("confirmation requires a decision draft")
    discovery = interaction.get("discovery")
    if discovery is not None:
        if not isinstance(discovery, dict):
            raise ValueError("discovery interaction is invalid")
        discovery_map = build_discovery_map(discovery.get("mode"), discovery.get("areas"))
        if "area_id" in discovery or "choice" in discovery:
            discovery_map = record_discovery_choice(discovery_map, discovery.get("area_id"), discovery.get("choice"))
        result["discovery_map"] = discovery_map
    return result


def create_decision_draft(
    *,
    change_id: str,
    decision_type: str,
    revision_digest: str,
    natural_message: str,
    consequence: str,
    source_event: dict[str, Any],
    card_event: dict[str, Any],
    expires_at: str,
) -> dict[str, Any]:
    """Prepare a non-authoritative card from one verbatim human decision message."""
    if not all(isinstance(value, str) and value for value in (change_id, decision_type, natural_message, consequence)):
        raise ValueError("decision draft identity is incomplete")
    if not SHA256.fullmatch(revision_digest) or not _valid_source_event(source_event, natural_message) or not _valid_card_event(card_event, source_event):
        raise ValueError("decision draft binding is invalid")
    issued_at = card_event["timestamp"]
    if not _is_after(expires_at, issued_at):
        raise ValueError("decision draft expiry is invalid")
    source_chat_event_ref = source_event["event_ref"]
    code_seed = "\x1f".join((change_id, decision_type, revision_digest, natural_message, consequence, source_chat_event_ref, issued_at))
    card_code = f"DEC-{hashlib.sha256(code_seed.encode('utf-8')).hexdigest()[:12].upper()}"
    return {
        "schema_version": "1.0",
        "record_type": "decision_draft",
        "card_code": card_code,
        "change_id": change_id,
        "decision_type": decision_type,
        "revision_digest": revision_digest,
        "source_message": natural_message,
        "source_chat_event_ref": source_chat_event_ref,
        "source_event_actor_type": source_event["actor_type"],
        "source_event_sequence": source_event["sequence"],
        "source_event_timestamp": source_event["timestamp"],
        "consequence": consequence,
        "card_chat_event_ref": card_event["event_ref"],
        "card_event_actor_type": card_event["actor_type"],
        "card_event_sequence": card_event["sequence"],
        "card_previous_event_ref": card_event["previous_event_ref"],
        "issued_at": issued_at,
        "expires_at": expires_at,
        "authority_recorded": False,
    }


def confirm_decision_draft(
    draft: dict[str, Any],
    confirmation_event: dict[str, Any],
) -> dict[str, Any] | None:
    """Return an immutable-by-contract event only for the active, bound confirmation."""
    if not _valid_draft(draft) or not _valid_next_confirmation(confirmation_event, draft):
        return None
    return {
        "schema_version": "1.0",
        "record_type": "confirmation_event",
        "decision_card_code": draft["card_code"],
        "change_id": draft["change_id"],
        "decision_type": draft["decision_type"],
        "revision_digest": draft["revision_digest"],
        "source_message": draft["source_message"],
        "consequence": draft["consequence"],
        "confirmation_message": confirmation_event["message"],
        "source_chat_event_ref": draft["source_chat_event_ref"],
        "source_event_actor_type": draft["source_event_actor_type"],
        "source_event_sequence": draft["source_event_sequence"],
        "source_event_timestamp": draft["source_event_timestamp"],
        "card_chat_event_ref": draft["card_chat_event_ref"],
        "card_event_actor_type": draft["card_event_actor_type"],
        "card_event_sequence": draft["card_event_sequence"],
        "card_previous_event_ref": draft["card_previous_event_ref"],
        "issued_at": draft["issued_at"],
        "trusted_chat_event_ref": confirmation_event["event_ref"],
        "confirmation_event_actor_type": confirmation_event["actor_type"],
        "confirmation_event_sequence": confirmation_event["sequence"],
        "confirmed_at": confirmation_event["timestamp"],
        "expires_at": draft["expires_at"],
    }


def build_discovery_map(mode: str, areas: list[dict[str, Any]]) -> dict[str, Any]:
    """Surface material unknowns without deciding defaults or readiness on behalf of a human."""
    if mode != "обычно" or not isinstance(areas, list):
        raise ValueError("discovery mode or areas are invalid")
    mapped: list[dict[str, Any]] = []
    for area in areas:
        if not isinstance(area, dict) or not all(isinstance(area.get(key), str) and area[key] for key in ("id", "impact")):
            raise ValueError("discovery area is invalid")
        material = area.get("material") is True
        mapped.append({
            "id": area["id"],
            "impact": area["impact"],
            "material": material,
            "status": "blocking" if material else "confirmed",
            "selection": "unresolved" if material else "not-required",
        })
    has_material_unknowns = any(area["material"] for area in mapped)
    return {
        "schema_version": "1.0",
        "record_type": "discovery_map",
        "mode": mode,
        "areas": mapped,
        "depth_recommendation": {
            "required": has_material_unknowns,
            "choices": list(DISCOVERY_CHOICES) if has_material_unknowns else [],
        },
        "intake_sufficient": not has_material_unknowns,
    }


def record_discovery_choice(discovery_map: dict[str, Any], area_id: str, choice: str | None) -> dict[str, Any]:
    """Record an explicit human choice; silence deliberately leaves an area unresolved."""
    if not isinstance(discovery_map, dict) or discovery_map.get("record_type") != "discovery_map":
        raise ValueError("discovery map is invalid")
    updated = copy.deepcopy(discovery_map)
    area = next((item for item in updated.get("areas", []) if item.get("id") == area_id), None)
    if area is None:
        raise ValueError("discovery area is unknown")
    if choice is None:
        return updated
    if choice not in DISCOVERY_CHOICES:
        raise ValueError("discovery choice is invalid")
    area["selection"] = choice
    area["status"] = {
        "углубиться": "blocking",
        "принять defaults": "proposed_default",
        "подготовить draft с открытыми решениями": "deferred",
    }[choice]
    updated["intake_sufficient"] = not any(item.get("status") == "blocking" for item in updated["areas"])
    return updated


def _valid_draft(value: Any) -> bool:
    if not isinstance(value, dict) or value.get("schema_version") != "1.0" or value.get("record_type") != "decision_draft":
        return False
    required = ("card_code", "change_id", "decision_type", "revision_digest", "source_message", "source_chat_event_ref", "source_event_actor_type", "source_event_timestamp", "consequence", "card_chat_event_ref", "card_event_actor_type", "card_previous_event_ref", "issued_at", "expires_at")
    return (
        all(isinstance(value.get(key), str) and value[key] for key in required)
        and isinstance(value.get("authority_recorded"), bool) and value["authority_recorded"] is False
        and bool(SHA256.fullmatch(value["revision_digest"]))
        and _is_sequence(value.get("source_event_sequence"))
        and _is_sequence(value.get("card_event_sequence"))
        and value["card_event_sequence"] == value["source_event_sequence"] + 1
        and value["source_event_actor_type"] == "human" and value["card_event_actor_type"] == "assistant"
        and value["card_previous_event_ref"] == value["source_chat_event_ref"]
        and _is_not_after(value["source_event_timestamp"], value["issued_at"])
        and value["card_code"] == _decision_card_code(value)
        and _is_after(value["expires_at"], value["issued_at"])
    )


def validate_confirmation_event(value: Any) -> bool:
    """Validate a persisted confirmation record without trusting caller assertions."""
    if not isinstance(value, dict) or value.get("schema_version") != "1.0" or value.get("record_type") != "confirmation_event":
        return False
    draft = {
        "schema_version": "1.0", "record_type": "decision_draft", "authority_recorded": False,
        **{key: value.get(key) for key in ("change_id", "decision_type", "revision_digest", "source_message", "source_chat_event_ref", "source_event_actor_type", "source_event_sequence", "source_event_timestamp", "consequence", "card_chat_event_ref", "card_event_actor_type", "card_event_sequence", "card_previous_event_ref", "issued_at", "expires_at")},
        "card_code": value.get("decision_card_code"),
    }
    confirmation = {
        "event_ref": value.get("trusted_chat_event_ref"), "actor_type": value.get("confirmation_event_actor_type"),
        "sequence": value.get("confirmation_event_sequence"), "previous_event_ref": value.get("card_chat_event_ref"),
        "timestamp": value.get("confirmed_at"), "message": value.get("confirmation_message"),
    }
    return _valid_draft(draft) and _valid_next_confirmation(confirmation, draft)


def _valid_source_event(event: Any, message: str) -> bool:
    return isinstance(event, dict) and event.get("actor_type") == "human" and event.get("message") == message and _valid_event_identity(event)


def _valid_card_event(event: Any, source: dict[str, Any]) -> bool:
    return (
        isinstance(event, dict) and event.get("actor_type") == "assistant" and _valid_event_identity(event)
        and event["sequence"] == source["sequence"] + 1 and event.get("previous_event_ref") == source["event_ref"]
        and _is_not_after(source["timestamp"], event["timestamp"])
    )


def _valid_next_confirmation(event: Any, draft: dict[str, Any]) -> bool:
    if not isinstance(event, dict) or event.get("actor_type") != "human" or not _valid_event_identity(event):
        return False
    if event["sequence"] != draft["card_event_sequence"] + 1 or event.get("previous_event_ref") != draft["card_chat_event_ref"]:
        return False
    if not (_is_not_after(draft["issued_at"], event["timestamp"]) and _is_not_after(event["timestamp"], draft["expires_at"])):
        return False
    exact = f"Подтверждаю {draft['card_code']}"
    normalized = " ".join(event.get("message", "").split()) if isinstance(event.get("message"), str) else ""
    return event.get("message") == exact or normalized == "Подтверждаю"


def _valid_event_identity(event: dict[str, Any]) -> bool:
    return isinstance(event.get("event_ref"), str) and bool(event["event_ref"]) and _is_sequence(event.get("sequence")) and _parse_aware(event.get("timestamp")) is not None


def _is_sequence(value: Any) -> bool:
    return type(value) is int and value >= 0


def _decision_card_code(value: dict[str, Any]) -> str:
    seed = "\x1f".join((value["change_id"], value["decision_type"], value["revision_digest"], value["source_message"], value["consequence"], value["source_chat_event_ref"], value["issued_at"]))
    return f"DEC-{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12].upper()}"


def _is_after(later: str, earlier: str) -> bool:
    later_value, earlier_value = _parse_aware(later), _parse_aware(earlier)
    return later_value is not None and earlier_value is not None and later_value > earlier_value


def _is_not_after(value: str, limit: str) -> bool:
    value_time, limit_time = _parse_aware(value), _parse_aware(limit)
    return value_time is not None and limit_time is not None and value_time <= limit_time


def _parse_aware(value: Any) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None
    return parsed if parsed.tzinfo is not None else None
