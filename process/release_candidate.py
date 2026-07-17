"""Deterministic construction and validation of immutable transfer candidates."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .errors import OperationError


_RELEASE_ID = re.compile(r"^[a-z][a-z0-9.-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DRIVE = re.compile(r"^[A-Za-z]:")
_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
_REPARSE_POINT = 0x400
_MUTABLE_EVIDENCE_PARTS = {("process", "release", "evidence"), (".superpowers",), ("tests",)}


@dataclass(frozen=True)
class ReleaseInputs:
    release_id: str
    known_limitations: tuple[str, ...]
    raw_artifact_root: Path


def validate_portable_path(value: str) -> str:
    """Return a canonical portable path or fail closed on Windows/POSIX threats."""
    if not isinstance(value, str) or not value or value in {".", ".."} or "\\" in value:
        raise OperationError("release.path-unsafe", "path is not portable")
    if value.startswith(("/", "//")) or _DRIVE.match(value) or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise OperationError("release.path-unsafe", "path is not portable")
    path = PurePosixPath(value)
    if str(path) != value or any(part in {"", ".", ".."} for part in path.parts):
        raise OperationError("release.path-unsafe", "path is not canonical")
    for part in path.parts:
        if ":" in part or part.endswith((".", " ")):
            raise OperationError("release.path-unsafe", "path is unsafe on Windows")
        if part.split(".", 1)[0].upper() in _RESERVED:
            raise OperationError("release.path-unsafe", "reserved Windows device name")
    return value


def _is_link_or_reparse(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & _REPARSE_POINT)


def _assert_no_mutable_evidence(parts: tuple[str, ...]) -> None:
    folded = tuple(part.casefold() for part in parts)
    for denied in _MUTABLE_EVIDENCE_PARTS:
        target = tuple(part.casefold() for part in denied)
        if folded[: len(target)] == target:
            raise OperationError("release.mutable-evidence-forbidden", "mutable development or release evidence is not payload content")


def payload_inventory(payload_root: Path) -> dict[str, Any]:
    """Inspect a payload and return its full sorted byte inventory and canonical digest."""
    root = payload_root.resolve()
    if not root.is_dir():
        raise OperationError("release.payload-missing", "payload root is missing", exit_code=3)
    inventory: list[dict[str, Any]] = []
    identities: dict[str, str] = {}
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        validate_portable_path(relative)
        _assert_no_mutable_evidence(tuple(PurePosixPath(relative).parts))
        identity = unicodedata.normalize("NFC", relative).casefold()
        previous = identities.setdefault(identity, relative)
        if previous != relative:
            raise OperationError("release.path-collision", "portable path identities collide")
        if _is_link_or_reparse(path):
            raise OperationError("release.link-forbidden", "links and reparse points are forbidden")
        if path.is_dir():
            continue
        if not path.is_file():
            raise OperationError("release.asset-unsafe", "payload contains a non-regular asset")
        data = path.read_bytes()
        inventory.append({"path": relative, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    encoded = json.dumps(inventory, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return {"inventory": inventory, "payload_sha256": hashlib.sha256(encoded).hexdigest()}


def _load_mapping(path: Path, code: str) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise OperationError(code, "required contract is missing or malformed", exit_code=3) from error
    if not isinstance(value, dict):
        raise OperationError(code, "required contract root must be a mapping", exit_code=3)
    return value


def _validate_schema(document: Mapping[str, Any], schema_path: Path, code: str) -> None:
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise OperationError(code, "schema is missing or malformed", exit_code=3) from error
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.absolute_path))
    if errors:
        raise OperationError(code, "document does not satisfy its schema")


def _assert_file(path: Path, relative: str) -> None:
    if not path.is_file() or _is_link_or_reparse(path):
        raise OperationError("release.asset-missing", f"declared asset is unavailable: {relative}", exit_code=3)


def _copy_file(source: Path, target: Path, relative: str) -> None:
    validate_portable_path(relative)
    _assert_file(source, relative)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def _copy_tree(source: Path, target: Path, relative: str) -> None:
    validate_portable_path(relative)
    if not source.is_dir() or _is_link_or_reparse(source):
        raise OperationError("release.asset-missing", f"declared asset root is unavailable: {relative}", exit_code=3)
    # Inspect source bytes and links before copying; destination receives regular files only.
    payload_inventory(source)
    shutil.copytree(source, target)


def _raw_artifacts(root: Path) -> list[dict[str, Any]]:
    resolved = root.resolve()
    if not resolved.is_dir() or _is_link_or_reparse(resolved):
        raise OperationError("release.raw-artifacts-invalid", "raw artifact root is missing or unsafe", exit_code=3)
    result: list[dict[str, Any]] = []
    identities: set[str] = set()
    for path in sorted(resolved.rglob("*"), key=lambda p: p.relative_to(resolved).as_posix()):
        relative = path.relative_to(resolved).as_posix()
        validate_portable_path(relative)
        identity = unicodedata.normalize("NFC", relative).casefold()
        if identity in identities:
            raise OperationError("release.path-collision", "raw artifact paths collide")
        identities.add(identity)
        if _is_link_or_reparse(path):
            raise OperationError("release.link-forbidden", "raw artifact links are forbidden")
        if path.is_dir():
            continue
        data = path.read_bytes()
        result.append({"reference": f"artifact:{relative}", "sha256": hashlib.sha256(data).hexdigest()})
    if not result:
        raise OperationError("release.raw-artifacts-invalid", "raw artifact root must contain evidence", exit_code=3)
    return result


def _certification_references(payload_root: Path) -> list[dict[str, str]]:
    evidence = payload_root / "process/certification/evidence"
    references: list[dict[str, str]] = []
    for path in sorted(evidence.glob("*.yaml")):
        name = path.name.casefold()
        family = "qwen" if "qwen" in name else "deepseek" if "deepseek" in name else None
        if family:
            references.append({
                "model_family": family,
                "path": path.relative_to(payload_root).as_posix(),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    if {item["model_family"] for item in references} != {"qwen", "deepseek"}:
        raise OperationError("release.certification-missing", "normalized Qwen and DeepSeek evidence is required")
    return references


def generate_release_manifest(payload_root: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Generate a byte-stable manifest exclusively from inputs and inspected contracts."""
    if not _RELEASE_ID.fullmatch(inputs.release_id) or any(not isinstance(v, str) or not v for v in inputs.known_limitations):
        raise OperationError("input-invalid", "release inputs are malformed", exit_code=3)
    root = payload_root.resolve()
    package = _load_mapping(root / "process/package.yaml", "release.package-invalid")
    config_schema = json.loads((root / "process/schemas/sdd-config.schema.json").read_text(encoding="utf-8"))
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_schema(allowlist, root / "process/schemas/release-allowlist.schema.json", "release.allowlist-invalid")
    inspected = payload_inventory(root)
    requirements = {}
    for line in (root / "requirements-test.txt").read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            name, version = line.split("==", 1)
            requirements[name] = version
    allowlist_bytes = (root / "process/release-allowlist.yaml").read_bytes()
    return {
        "schema_version": "2.0",
        "release_id": inputs.release_id,
        "payload_sha256": inspected["payload_sha256"],
        "inventory": inspected["inventory"],
        "allowlist_sha256": hashlib.sha256(allowlist_bytes).hexdigest(),
        "process_package": package["package"],
        "config_schema_version": config_schema["properties"]["config_schema_version"]["const"],
        "openspec": package["openspec"],
        "host_evidence": [
            {"platform_id": "windows", "evidence_level": "full-clean-rehearsal"},
            {"platform_id": "linux-wsl2", "evidence_level": "portability-smoke"},
            {"platform_id": "macos", "evidence_level": "not-certified"},
        ],
        "compatibility": {
            "python": "3.11+", "node": "20+", "git": "2.40+", "openspec": package["openspec"]["cli_version"],
            "mcp": "provisioned-or-explicitly-unavailable", "shells": ["powershell-7+", "bash-5+"],
            "packages": [{"name": name, "version": requirements[name]} for name in sorted(requirements)],
        },
        "verification": {
            "commands": [
                "python -m pytest tests/test_release_candidate.py tests/test_process_package.py -q",
                "python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py tests/test_packaged_flow_cli.py -q",
            ],
            "evidence_requirements": ["windows-full-clean-rehearsal", "linux-wsl2-portability-smoke", "negative-acceptance-cases"],
        },
        "raw_artifacts": _raw_artifacts(inputs.raw_artifact_root),
        "weak_model_certification": _certification_references(root),
        "known_limitations": list(inputs.known_limitations),
        "rollback_reference": "docs/runbooks/PROCESS_PACKAGE_SETUP.md",
    }


def _declared_top_level(payload_root: Path, allowlist: Mapping[str, Any], package: Mapping[str, Any]) -> set[str]:
    declared = set(allowlist["requirements"])
    declared.update(allowlist["template_roots"])
    declared.update(f"docs/runbooks/{name}" for name in allowlist["runbooks"])
    declared.update(f"scripts/{item['name']}" for item in allowlist["entry_points"])
    declared.update(f"process/{name}" for name in package["distribution"]["files"])
    declared.update(f"process/{name}" for name in package["distribution"]["roots"])
    return declared


def _validate_declared_assets(payload_root: Path, allowlist: Mapping[str, Any], package: Mapping[str, Any]) -> None:
    expected_scripts = {item["name"] for item in allowlist["entry_points"]}
    actual_scripts = {path.name for path in (payload_root / "scripts").iterdir() if path.is_file()}
    if actual_scripts != expected_scripts:
        raise OperationError("release.allowlist-mismatch", "public entry-point inventory differs from the allowlist")
    for relative in _declared_top_level(payload_root, allowlist, package):
        if not (payload_root / relative).exists():
            raise OperationError("release.asset-missing", "payload omits a declared release asset")


def validate_release_manifest(
    candidate_root: Path, manifest: Mapping[str, Any], *, now: datetime | None = None
) -> dict[str, Any]:
    """Validate manifest schema and semantic binding to the immutable candidate payload."""
    del now  # Reserved for Task 2 evidence freshness without making Task 1 time-dependent.
    candidate = candidate_root.resolve()
    payload = candidate / "payload" if (candidate / "payload").is_dir() else candidate
    schema_path = payload / "process/schemas/release-manifest.schema.json"
    _validate_schema(manifest, schema_path, "release.manifest-invalid")
    allowlist = _load_mapping(payload / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_schema(allowlist, payload / "process/schemas/release-allowlist.schema.json", "release.allowlist-invalid")
    package = _load_mapping(payload / "process/package.yaml", "release.package-invalid")
    _validate_declared_assets(payload, allowlist, package)
    actual = payload_inventory(payload)
    if list(manifest["inventory"]) != actual["inventory"] or manifest["payload_sha256"] != actual["payload_sha256"]:
        raise OperationError("release.inventory-mismatch", "manifest does not bind to exact payload bytes")
    allowlist_sha = hashlib.sha256((payload / "process/release-allowlist.yaml").read_bytes()).hexdigest()
    if manifest["allowlist_sha256"] != allowlist_sha:
        raise OperationError("release.allowlist-mismatch", "manifest allowlist checksum differs")
    return {"operation": "validate-release-manifest", "status": "valid", "release_id": manifest["release_id"], "payload_sha256": actual["payload_sha256"]}


def build_release_candidate(repository_root: Path, destination: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Atomically create one immutable allowlisted candidate in a new destination."""
    root = repository_root.resolve()
    target = destination.resolve()
    if not root.is_dir():
        raise OperationError("release.repository-missing", "repository root is missing", exit_code=3)
    if target == root or root in target.parents or target in root.parents:
        raise OperationError("release.path-overlap", "source and destination must not overlap")
    if target.exists():
        raise OperationError("release.destination-exists", "destination must not already exist")
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_schema(allowlist, root / "process/schemas/release-allowlist.schema.json", "release.allowlist-invalid")
    package = _load_mapping(root / "process/package.yaml", "release.package-invalid")
    staging = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=target.parent))
    try:
        payload = staging / "payload"
        payload.mkdir()
        for name in package["distribution"]["files"]:
            _copy_file(root / "process" / name, payload / "process" / name, f"process/{name}")
        for name in package["distribution"]["roots"]:
            _copy_tree(root / "process" / name, payload / "process" / name, f"process/{name}")
        for relative in allowlist["requirements"]:
            _copy_file(root / relative, payload / relative, relative)
        for relative in allowlist["template_roots"]:
            _copy_tree(root / relative, payload / relative, relative)
        for name in allowlist["runbooks"]:
            _copy_file(root / "docs/runbooks" / name, payload / "docs/runbooks" / name, f"docs/runbooks/{name}")
        for item in allowlist["entry_points"]:
            name = item["name"]
            _copy_file(root / "scripts" / name, payload / "scripts" / name, f"scripts/{name}")
        manifest = generate_release_manifest(payload, inputs)
        manifest_text = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, line_break="\n")
        (staging / "release-manifest.yaml").write_text(manifest_text, encoding="utf-8", newline="\n")
        validate_release_manifest(staging, manifest)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(staging), str(target))
        return manifest
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
