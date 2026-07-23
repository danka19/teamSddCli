"""Deterministic P3 checks for trusted guided-package acceptance."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


ACCEPTANCE_PATH = Path("decisions/spec-acceptance.yaml")
REQUIRED_DOCUMENTS = ("proposal.md", "design.md", "tasks.md", "traceability.yaml", "status.md")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|placeholder)\b|<[^>]+>", re.IGNORECASE)
BLOCKER = re.compile(r"\b(?:blocker|unresolved|open question)\b", re.IGNORECASE)
LITERAL_ACCEPTANCE = "Спека принята, реализуй"
TRUSTED_ROLES = {"Analyst", "Tech Lead"}


def validate_guided_change_package(package_root: Path) -> dict[str, Any]:
    """Validate readiness and trusted human acceptance without side effects."""
    root = package_root.resolve()
    diagnostics: list[dict[str, str]] = []
    for name in REQUIRED_DOCUMENTS:
        _require_nonempty(root / name, diagnostics)
    spec_paths = sorted((root / "specs").glob("**/spec.md")) if (root / "specs").is_dir() else []
    if not spec_paths:
        _error(diagnostics, "guided-process.spec-missing", "at least one Delta Spec is required")
    for spec in spec_paths:
        text = _read(spec, diagnostics)
        if "#### Scenario:" not in text:
            _error(diagnostics, "guided-process.scenario-missing", f"{spec.relative_to(root)} has no testable scenario")
        _content_is_ready(text, spec.name, diagnostics)
    for name in REQUIRED_DOCUMENTS:
        text = _read(root / name, diagnostics)
        _content_is_ready(text, name, diagnostics)

    traceability = _load_yaml(root / "traceability.yaml", diagnostics)
    if not isinstance(traceability, dict) or not isinstance(traceability.get("requirements"), list) or not traceability["requirements"]:
        _error(diagnostics, "guided-process.traceability-missing", "traceability.yaml must contain requirement rows")
    status = _read(root / "status.md", diagnostics)
    if "DoR: passed" not in status:
        _error(diagnostics, "guided-process.dor-not-passed", "status.md must record DoR: passed before acceptance")

    acceptance = _load_yaml(root / ACCEPTANCE_PATH, diagnostics)
    revision = _validate_acceptance(root, acceptance, diagnostics)
    return {
        "operation": "validate-guided-process-integrity",
        "schema_version": "2.0",
        "status": "valid" if not diagnostics else "invalid",
        "package": str(root),
        "spec_revision": revision,
        "diagnostics": diagnostics,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }


def build_response_summary(
    package_root: Path | None,
    report: dict[str, Any],
    *,
    human_role: str | None = None,
    confirmation_event: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return one evidence-labelled, role-scoped next action."""
    action = "resolve-blocking-package-discrepancy"
    if report["status"] == "valid":
        action = "monitor-process-status" if human_role == "Tech Lead" else "prepare-role-pr-approval" if human_role == "Analyst" else "await-role-pr-approval"
    confirmation = _validated_confirmation_summary(confirmation_event)
    return {
        "operation": "guided-process-summary",
        "schema_version": "2.0",
        "role": human_role or "unknown",
        "spec_revision": report.get("spec_revision"),
        "checks": {"status": report["status"], "diagnostics": report["diagnostics"]},
        "decision_confirmation": confirmation,
        "next_permitted_action": action,
        "lifecycle_mutated": False,
        "external_state_mutated": False,
    }


def _validated_confirmation_summary(event: dict[str, Any] | None) -> dict[str, Any]:
    """Expose only a validated, human-originated decision record; never AI authority."""
    required = (
        "decision_card_code", "change_id", "decision_type", "revision_digest", "source_message",
        "confirmation_message", "source_chat_event_ref", "trusted_chat_event_ref", "confirmed_at", "expires_at",
    )
    if not isinstance(event, dict) or event.get("schema_version") != "1.0" or event.get("record_type") != "confirmation_event":
        return {"status": "unconfirmed"}
    if not all(isinstance(event.get(key), str) and event[key] for key in required):
        return {"status": "unconfirmed"}
    if not re.fullmatch(r"DEC-[0-9A-F]{12}", event["decision_card_code"]) or not re.fullmatch(r"[0-9a-f]{64}", event["revision_digest"]):
        return {"status": "unconfirmed"}
    exact = f"Подтверждаю {event['decision_card_code']}"
    normalized = " ".join(event["confirmation_message"].split())
    if event["confirmation_message"] != exact and normalized != "Подтверждаю":
        return {"status": "unconfirmed"}
    try:
        confirmed_at = datetime.fromisoformat(event["confirmed_at"].replace("Z", "+00:00"))
        expires_at = datetime.fromisoformat(event["expires_at"].replace("Z", "+00:00"))
    except ValueError:
        return {"status": "unconfirmed"}
    if confirmed_at > expires_at:
        return {"status": "unconfirmed"}
    return {
        "status": "confirmed",
        "card_code": event["decision_card_code"],
        "change_id": event["change_id"],
        "revision_digest": event["revision_digest"],
        "trusted_chat_event_ref": event["trusted_chat_event_ref"],
    }


def _validate_acceptance(root: Path, value: Any, diagnostics: list[dict[str, str]]) -> dict[str, str] | None:
    if not isinstance(value, dict):
        _error(diagnostics, "guided-process.acceptance-record-missing", "trusted acceptance record is required")
        return None
    event = value.get("event")
    revision = value.get("spec_revision")
    shown = value.get("shown_summary")
    if value.get("schema_version") != "2.0" or not isinstance(value.get("change_id"), str):
        _error(diagnostics, "guided-process.acceptance-record-invalid", "acceptance identity is invalid")
    if not isinstance(event, dict) or event.get("actor_type") != "human" or event.get("human_role") not in TRUSTED_ROLES or not all(isinstance(event.get(key), str) and event[key] for key in ("timestamp", "reference")):
        _error(diagnostics, "guided-process.acceptance-provenance-invalid", "acceptance must be a trusted human event")
    if not isinstance(event, dict) or event.get("literal_message") != LITERAL_ACCEPTANCE:
        _error(diagnostics, "guided-process.acceptance-message-invalid", "UI confirmation is not literal human acceptance")
    if not isinstance(revision, dict) or not isinstance(revision.get("path"), str) or not re.fullmatch(r"[0-9a-f]{64}", str(revision.get("sha256", ""))):
        _error(diagnostics, "guided-process.acceptance-revision-invalid", "acceptance must name a hashed spec revision")
        return None
    path = root / revision["path"]
    actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
    if actual != revision["sha256"]:
        _error(diagnostics, "guided-process.acceptance-revision-mismatch", "accepted revision does not match shown spec")
    if not isinstance(shown, dict) or shown.get("path") != "status.md" or shown.get("spec_sha256") != revision["sha256"]:
        _error(diagnostics, "guided-process.acceptance-summary-invalid", "shown summary must bind the same spec revision")
    return {"path": revision["path"], "sha256": revision["sha256"]}


def _require_nonempty(path: Path, diagnostics: list[dict[str, str]]) -> None:
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        _error(diagnostics, "guided-process.document-required", f"{path.name} is required and non-empty")


def _read(path: Path, diagnostics: list[dict[str, str]]) -> str:
    try:
        return path.read_text(encoding="utf-8") if path.is_file() else ""
    except (OSError, UnicodeError):
        _error(diagnostics, "guided-process.document-unreadable", f"cannot read {path.name}")
        return ""


def _load_yaml(path: Path, diagnostics: list[dict[str, str]]) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else None
    except (OSError, UnicodeError, yaml.YAMLError):
        _error(diagnostics, "guided-process.document-invalid", f"cannot parse {path.name}")
        return None


def _content_is_ready(text: str, name: str, diagnostics: list[dict[str, str]]) -> None:
    if PLACEHOLDER.search(text):
        _error(diagnostics, "guided-process.placeholder", f"{name} contains a placeholder")
    if BLOCKER.search(text):
        _error(diagnostics, "guided-process.blocker-present", f"{name} contains an unresolved blocker")


def _error(diagnostics: list[dict[str, str]], code: str, message: str) -> None:
    diagnostics.append({"code": code, "message": message})
