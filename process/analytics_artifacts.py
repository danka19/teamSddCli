"""Local, deterministic validation and read-only previews for P3 analytics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


PACKAGE_FILES = {
    "analytics-manifest.yaml": "analytics_manifest",
    "status-model.yaml": "status_model",
    "channel-support.yaml": "channel_support",
    "data-model.yaml": "data_model",
    "platform-services.yaml": "platform_services",
    "journey.yaml": "journey",
    "screens.yaml": "screens",
    "integrations.yaml": "integrations",
}


def validate_analytics_package(package_root: Path, *, schema_root: Path | None = None) -> dict[str, Any]:
    root = package_root.resolve()
    schemas = schema_root or Path(__file__).resolve().parent / "schemas"
    diagnostics: list[dict[str, str]] = []
    documents: dict[str, Any] = {}
    for name, schema_id in PACKAGE_FILES.items():
        path = root / name
        try:
            documents[name] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            diagnostics.append({"code": "analytics.document-invalid", "path": name})
            continue
        schema_path = schemas / f"{schema_id.replace('_', '-')}.schema.json"
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            diagnostics.append({"code": "analytics.schema-unavailable", "path": schema_path.name})
            continue
        if list(Draft202012Validator(schema).iter_errors(documents[name])):
            diagnostics.append({"code": "analytics.schema-invalid", "path": name})
    manifest = documents.get("analytics-manifest.yaml")
    if isinstance(manifest, dict) and set(manifest.get("artifacts", [])) != set(PACKAGE_FILES) - {"analytics-manifest.yaml"}:
        diagnostics.append({"code": "analytics.manifest-incomplete", "path": "analytics-manifest.yaml"})
    for item in (documents.get("integrations.yaml") or {}).get("integrations", []):
        if item.get("mode") != "passive":
            diagnostics.append({"code": "analytics.integration-not-passive", "path": "integrations.yaml"})
    return {"operation": "validate-analytics-artifacts", "status": "valid" if not diagnostics else "invalid", "diagnostics": diagnostics, "external_state_mutated": False}


def preview_analytics(package_root: Path, report: dict[str, Any]) -> dict[str, Any]:
    root = package_root.resolve()
    screens = yaml.safe_load((root / "screens.yaml").read_text(encoding="utf-8")) or {}
    integrations = yaml.safe_load((root / "integrations.yaml").read_text(encoding="utf-8")) or {}
    journey = yaml.safe_load((root / "journey.yaml").read_text(encoding="utf-8")) or {}
    return {"operation": "preview-analytics-artifacts", "status": report["status"], "journey": journey.get("steps", []), "screens": screens.get("screens", []), "integrations": integrations.get("integrations", []), "integration_actions": [], "external_state_mutated": False}
