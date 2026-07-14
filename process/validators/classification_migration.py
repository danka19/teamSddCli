"""Bounded check/apply migration from legacy mode to schema-v2 classification."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


MAPPINGS = {"thin": "minor", "full": "major"}
BACKUP_SUFFIX = ".pre-classification-v2.bak"
CHANGE_V2_SCHEMA = (
    Path(__file__).resolve().parents[1] / "schemas" / "change-v2.schema.json"
)


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    value: dict[Any, Any] = {}
    for key_node, item_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in value:
            raise ValueError("duplicate mapping key")
        value[key] = loader.construct_object(item_node, deep=deep)
    return value


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


@dataclass(frozen=True)
class MigrationResult:
    payload: dict[str, Any]

    @property
    def exit_code(self) -> int:
        return 1 if self.payload["status"] == "blocked" else 0

    def as_dict(self) -> dict[str, Any]:
        return self.payload

    def render_human(self) -> str:
        lines = [
            f"Migration: {self.payload['status']}",
            f"Plan digest: {self.payload['plan_digest']}",
            f"Schema: {self.payload['source_schema']} -> {self.payload['target_schema']}",
            f"Validation: {self.payload['validation_result']}",
            "Preserved fields: " + ", ".join(self.payload["preserved_fields"]),
            "Affected files: " + ", ".join(self.payload["affected_files"]),
            f"Rollback: {self.payload['rollback_evidence']['strategy']} "
            f"({self.payload['rollback_evidence']['backup_path']})",
            f"Hold required: {str(self.payload['hold_evidence']['required']).lower()}",
        ]
        mapping = self.payload.get("mapping")
        if mapping:
            lines.append(
                f"Mapping: {mapping['mode']} -> {mapping['classification']}"
            )
        for ambiguity in self.payload.get("ambiguities", []):
            lines.append(f"BLOCKER: {ambiguity}")
        return "\n".join(lines)


def plan_migration(path: str | Path) -> MigrationResult:
    """Return a stable non-mutating plan for one change metadata file."""
    target = _target(path)
    source = target.read_bytes()
    source_sha = hashlib.sha256(source).hexdigest()
    ambiguities: list[str] = []
    try:
        document = yaml.load(source.decode("utf-8"), Loader=_UniqueKeyLoader)
    except (UnicodeError, yaml.YAMLError, ValueError):
        document = None
        ambiguities.append("invalid-or-duplicate-yaml")
    if not isinstance(document, dict):
        document = {}
        if not ambiguities:
            ambiguities.append("metadata-must-be-mapping")

    mode = document.get("mode")
    classification = document.get("classification")
    excluded = _historical_path(target) or document.get("status") == "archived"
    validation_errors: list[str] = []
    if mode is not None and classification is not None:
        ambiguities.append(
            "legacy-target-conflict"
            if MAPPINGS.get(mode) != classification
            else "mixed-legacy-target-metadata"
        )
    elif mode is not None and mode not in MAPPINGS:
        ambiguities.append("unsupported-legacy-mode")

    if not excluded and not ambiguities and mode in MAPPINGS:
        try:
            proposed_text = _surgical_migration(
                source.decode("utf-8"), mode, MAPPINGS[mode], source_sha
            )
            proposed_document = yaml.load(proposed_text, Loader=_UniqueKeyLoader)
            validation_errors = _schema_errors(proposed_document)
        except (UnicodeError, yaml.YAMLError, ValueError):
            validation_errors = ["/: proposed metadata could not be constructed"]
        if validation_errors:
            ambiguities.append("target-schema-validation-failed")
    elif (
        not excluded
        and not ambiguities
        and document.get("schema_version") == 2
        and classification in {"minor", "major", "hotfix"}
    ):
        validation_errors = _schema_errors(document)
        if validation_errors:
            ambiguities.append("target-schema-validation-failed")

    if excluded:
        status = "excluded-history"
    elif ambiguities:
        status = "blocked"
    elif mode in MAPPINGS:
        status = "ready"
    elif (
        document.get("schema_version") == 2
        and classification in {"minor", "major", "hotfix"}
    ):
        status = "already-current"
    else:
        status = "blocked"
        ambiguities.append("no-supported-classification-metadata")

    mapping = (
        {"mode": mode, "classification": MAPPINGS[mode]}
        if mode in MAPPINGS and not (classification is not None)
        else None
    )
    base: dict[str, Any] = {
        "schema_version": "1.0",
        "status": status,
        "source_schema": "legacy-mode" if mode is not None else "schema-v2",
        "target_schema": 2,
        "mapping": mapping,
        "preserved_fields": sorted(
            str(key) for key in document if key not in {"mode", "classification"}
        ),
        "ambiguities": sorted(set(ambiguities)),
        "validation_errors": validation_errors,
        "diagnostics": ([{
            "code": "migration.legacy-mode-deprecated",
            "source_field": "mode",
            "message": "Legacy mode is read only for deterministic migration.",
        }] if mode is not None else []),
        "validation_result": "valid" if status in {
            "ready", "already-current", "excluded-history"
        } else "invalid",
        "affected_files": [target.name],
        "source_sha256": source_sha,
        "policy": {"id": "sdd-core", "version": "1.0.0"},
        "rollback_evidence": {
            "strategy": "backup-before-write",
            "backup_path": target.name + BACKUP_SUFFIX,
            "source_sha256": source_sha,
        },
        "hold_evidence": {
            "required": status == "blocked",
            "reasons": sorted(set(ambiguities)),
        },
    }
    base["plan_digest"] = _plan_digest(base)
    return MigrationResult(base)


def apply_migration(
    path: str | Path, *, expected_plan_digest: str
) -> MigrationResult:
    """Apply exactly a previously observed valid plan, or make no change."""
    target = _target(path)
    plan = plan_migration(target)
    payload = dict(plan.as_dict())
    if payload["status"] in {"already-current", "excluded-history"}:
        return plan
    if payload["status"] != "ready" or expected_plan_digest != payload["plan_digest"]:
        reasons = list(payload["hold_evidence"]["reasons"])
        if expected_plan_digest != payload["plan_digest"]:
            reasons.append("plan-digest-mismatch")
        payload.update({
            "status": "blocked",
            "validation_result": "invalid",
            "hold_evidence": {"required": True, "reasons": sorted(set(reasons))},
        })
        return MigrationResult(payload)

    source = target.read_bytes()
    backup = target.with_name(target.name + BACKUP_SUFFIX)
    if backup.exists():
        payload.update({
            "status": "blocked",
            "validation_result": "invalid",
            "hold_evidence": {
                "required": True,
                "reasons": ["rollback-backup-already-exists"],
            },
        })
        return MigrationResult(payload)

    mapping = payload["mapping"]
    assert isinstance(mapping, dict)
    migrated = _surgical_migration(
        source.decode("utf-8"),
        str(mapping["mode"]),
        str(mapping["classification"]),
        payload["source_sha256"],
    )
    parsed = yaml.load(migrated, Loader=_UniqueKeyLoader)
    if (
        not isinstance(parsed, dict)
        or parsed.get("classification") != mapping["classification"]
        or _schema_errors(parsed)
    ):
        payload.update({
            "status": "blocked",
            "validation_result": "invalid",
            "hold_evidence": {"required": True, "reasons": ["post-migration-validation-failed"]},
        })
        return MigrationResult(payload)

    _write_fsynced(backup, source, exclusive=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=target.parent,
            prefix=f".{target.name}.classification-v2-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(migrated.encode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        temporary = None
        _fsync_directory(target.parent)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    payload.update({
        "status": "applied",
        "validation_result": "valid",
        "rollback_evidence": {
            "strategy": "restore-backup",
            "backup_path": str(backup),
            "source_sha256": payload["source_sha256"],
        },
        "hold_evidence": {"required": False, "reasons": []},
    })
    return MigrationResult(payload)


def _target(path: str | Path) -> Path:
    target = Path(path)
    if target.is_dir():
        target = target / "change.yaml"
    if not target.is_file():
        raise FileNotFoundError("change metadata file does not exist")
    return target.resolve()


def _historical_path(path: Path) -> bool:
    parts = [item.lower() for item in path.parts]
    if any(item in {"archive", "archives", "archived", "accepted"} for item in parts):
        return True
    return any(
        parts[index:index + 2] == ["openspec", "specs"]
        for index in range(len(parts) - 1)
    )


def _plan_digest(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _schema_errors(document: Any) -> list[str]:
    schema = json.loads(CHANGE_V2_SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda item: list(item.path))
    return [
        f"/{'/'.join(str(item) for item in error.path)}: {error.validator}"
        for error in errors
    ]


def _write_fsynced(path: Path, content: bytes, *, exclusive: bool) -> None:
    mode = "xb" if exclusive else "wb"
    with path.open(mode) as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())


def _fsync_directory(path: Path) -> None:
    flags = getattr(os, "O_RDONLY", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def _surgical_migration(
    text: str, mode: str, classification: str, source_sha: str
) -> str:
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    replaced_mode = False
    replaced_schema = False
    for index, line in enumerate(lines):
        ending = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
        body = line[:-len(ending)] if ending else line
        if re.fullmatch(r"schema_version:\s*[^#]+(?:\s*#.*)?", body):
            lines[index] = f"schema_version: 2{ending or newline}"
            replaced_schema = True
        elif re.fullmatch(rf"mode:\s*{re.escape(mode)}\s*(?:#.*)?", body):
            lines[index] = f"classification: {classification}{ending or newline}"
            replaced_mode = True
    if not replaced_mode:
        raise ValueError("legacy mode line is not safely replaceable")
    if not replaced_schema:
        insertion = 0
        while insertion < len(lines) and lines[insertion].lstrip().startswith("#"):
            insertion += 1
        lines.insert(insertion, f"schema_version: 2{newline}")
    result = "".join(lines)
    if result and not result.endswith(("\n", "\r")):
        result += newline
    result += (
        f"compatibility:{newline}"
        f"  source: migrated{newline}"
        f"  legacy_mode: {mode}{newline}"
        f"  legacy_ref: change.yaml@sha256:{source_sha}{newline}"
    )
    return result
