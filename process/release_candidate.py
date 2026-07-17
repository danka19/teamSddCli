"""Deterministic construction and validation of immutable transfer candidates."""

from __future__ import annotations

import hashlib
import json
import os
import errno
import re
import shutil
import stat
import sys
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
_RUNBOOKS = (
    "ARTIFACT_AND_LIFECYCLE_GATES.md", "CERTIFICATION_EVIDENCE.md",
    "CLASSIFICATION_AND_MIGRATION.md", "CORPORATE_FLOW_CONTROLS.md",
    "PACKAGED_GOVERNED_FLOW.md", "PROCESS_PACKAGE_SETUP.md",
    "TECH_LEAD_GOVERNANCE.md", "TRANSFER_RELEASE_CANDIDATE.md",
    "WEAK_MODEL_OPERATING_KIT.md",
)
_ENTRY_POINTS = (
    ("bootstrap_team_specs.py", ("scripts/bootstrap_team_specs.py", "--help"), (0,)),
    ("check_corporate_flow.py", ("scripts/check_corporate_flow.py", "--help"), (2,)),
    ("check_lifecycle_transition.py", ("scripts/check_lifecycle_transition.py", "--help"), (0,)),
    ("check_tech_lead_control.py", ("scripts/check_tech_lead_control.py", "--help"), (2,)),
    ("classify_change.py", ("scripts/classify_change.py", "--help"), (0,)),
    ("create_change.py", ("scripts/create_change.py", "--help"), (0,)),
    ("evaluate_change_gates.py", ("scripts/evaluate_change_gates.py", "--help"), (0,)),
    ("manage_release_candidate.py", ("scripts/manage_release_candidate.py", "validate", "--help"), (0,)),
    ("manual_fallback.py", ("scripts/manual_fallback.py", "--help"), (0,)),
    ("migrate_change_classification.py", ("scripts/migrate_change_classification.py", "--help"), (0,)),
    ("prepare_archive.py", ("scripts/prepare_archive.py", "--help"), (0,)),
    ("prepare_spec_pr.py", ("scripts/prepare_spec_pr.py", "--help"), (0,)),
    ("review_tech_lead.py", ("scripts/review_tech_lead.py", "--help"), (2,)),
    ("update_process_package.py", ("scripts/update_process_package.py", "--help"), (0,)),
    ("validate_change.py", ("scripts/validate_change.py", "--help"), (0,)),
    ("validate_external_mapping.py", ("scripts/validate_external_mapping.py", "--help"), (0,)),
    ("validate_process_config.py", ("scripts/validate_process_config.py", "--help"), (0,)),
    ("validate_traceability.py", ("scripts/validate_traceability.py", "--help"), (0,)),
)
_HOST_EVIDENCE = [
    {"platform_id": "windows", "evidence_level": "full-clean-rehearsal"},
    {"platform_id": "linux-wsl2", "evidence_level": "portability-smoke"},
    {"platform_id": "macos", "evidence_level": "not-certified"},
]
_VERIFICATION_COMMANDS = [
    "python -m pytest tests/test_release_candidate.py tests/test_process_package.py -q",
    "python -m pytest tests/test_packaged_flow.py tests/test_packaged_flow_hardening.py tests/test_packaged_flow_cli.py -q",
]
_EVIDENCE_REQUIREMENTS = [
    "windows-full-clean-rehearsal", "linux-wsl2-portability-smoke", "negative-acceptance-cases"
]
_ROLLBACK_REFERENCE = "docs/runbooks/PROCESS_PACKAGE_SETUP.md"


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


def _safe_directory_root(path: Path, missing_code: str) -> Path:
    raw = Path(path)
    try:
        if _is_link_or_reparse(raw):
            raise OperationError("release.link-forbidden", "root links and reparse points are forbidden")
    except FileNotFoundError as error:
        raise OperationError(missing_code, "required directory is missing", exit_code=3) from error
    if not raw.is_dir():
        raise OperationError(missing_code, "required directory is missing", exit_code=3)
    return raw.resolve()


def _assert_no_mutable_evidence(parts: tuple[str, ...]) -> None:
    folded = tuple(part.casefold() for part in parts)
    for denied in _MUTABLE_EVIDENCE_PARTS:
        target = tuple(part.casefold() for part in denied)
        if folded[: len(target)] == target:
            raise OperationError("release.mutable-evidence-forbidden", "mutable development or release evidence is not payload content")


def payload_inventory(payload_root: Path) -> dict[str, Any]:
    """Inspect a payload and return its full sorted byte inventory and canonical digest."""
    root = _safe_directory_root(payload_root, "release.payload-missing")
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


def _expected_allowlist() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "requirements": ["requirements-test.txt"],
        "template_roots": ["templates/team-specs"],
        "runbooks": list(_RUNBOOKS),
        "entry_points": [
            {"name": name, "smoke": list(smoke), "expected_exit_codes": list(exits)}
            for name, smoke, exits in _ENTRY_POINTS
        ],
    }


def _validate_allowlist(allowlist: Mapping[str, Any], schema_path: Path) -> None:
    _validate_schema(allowlist, schema_path, "release.allowlist-invalid")
    if dict(allowlist) != _expected_allowlist():
        raise OperationError("release.allowlist-invalid", "allowlist differs from the public release contract")


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
    resolved = _safe_directory_root(root, "release.raw-artifacts-invalid")
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


def _validate_inputs(inputs: ReleaseInputs) -> None:
    if (
        not isinstance(inputs.release_id, str)
        or not _RELEASE_ID.fullmatch(inputs.release_id)
        or not isinstance(inputs.known_limitations, tuple)
        or any(not isinstance(value, str) or not value for value in inputs.known_limitations)
        or not isinstance(inputs.raw_artifact_root, Path)
    ):
        raise OperationError("input-invalid", "release inputs are malformed", exit_code=3)


def _package_contract(root: Path) -> dict[str, Any]:
    package = _load_mapping(root / "process/package.yaml", "release.package-invalid")
    _validate_schema(package, root / "process/schemas/process-package.schema.json", "release.package-invalid")
    return package


def _dependency_contract(root: Path, package: Mapping[str, Any]) -> dict[str, Any]:
    requirements: dict[str, str] = {}
    try:
        lines = (root / "requirements-test.txt").read_text(encoding="utf-8").splitlines()
        for line in lines:
            if line and not line.startswith("#"):
                name, version = line.split("==", 1)
                requirements[name] = version
    except (OSError, UnicodeError, ValueError) as error:
        raise OperationError("release.dependencies-invalid", "dependency pins are missing or malformed", exit_code=3) from error
    return {
        "python": "3.11+", "node": "20+", "git": "2.40+",
        "openspec": package["openspec"]["cli_version"],
        "mcp": "provisioned-or-explicitly-unavailable",
        "shells": ["powershell-7+", "bash-5+"],
        "packages": [{"name": name, "version": requirements[name]} for name in sorted(requirements)],
    }


def _derived_manifest_fields(root: Path) -> dict[str, Any]:
    package = _package_contract(root)
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_allowlist(allowlist, root / "process/schemas/release-allowlist.schema.json")
    inspected = payload_inventory(root)
    _validate_declared_assets(root, allowlist, package, inspected["inventory"])
    try:
        config_schema = json.loads((root / "process/schemas/sdd-config.schema.json").read_text(encoding="utf-8"))
        config_version = config_schema["properties"]["config_schema_version"]["const"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise OperationError("release.config-contract-invalid", "config identity cannot be derived", exit_code=3) from error
    return {
        "payload_sha256": inspected["payload_sha256"],
        "inventory": inspected["inventory"],
        "allowlist_sha256": hashlib.sha256((root / "process/release-allowlist.yaml").read_bytes()).hexdigest(),
        "process_package": package["package"],
        "config_schema_version": config_version,
        "openspec": package["openspec"],
        "host_evidence": [dict(row) for row in _HOST_EVIDENCE],
        "compatibility": _dependency_contract(root, package),
        "verification": {
            "commands": list(_VERIFICATION_COMMANDS),
            "evidence_requirements": list(_EVIDENCE_REQUIREMENTS),
        },
        "weak_model_certification": _certification_references(root),
        "rollback_reference": _ROLLBACK_REFERENCE,
    }


def generate_release_manifest(payload_root: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Generate a byte-stable manifest exclusively from inputs and inspected contracts."""
    _validate_inputs(inputs)
    root = _safe_directory_root(payload_root, "release.payload-missing")
    derived = _derived_manifest_fields(root)
    return {
        "schema_version": "2.0",
        "release_id": inputs.release_id,
        **derived,
        "raw_artifacts": _raw_artifacts(inputs.raw_artifact_root),
        "known_limitations": list(inputs.known_limitations),
    }


def _declared_top_level(payload_root: Path, allowlist: Mapping[str, Any], package: Mapping[str, Any]) -> set[str]:
    declared = set(allowlist["requirements"])
    declared.update(allowlist["template_roots"])
    declared.update(f"docs/runbooks/{name}" for name in allowlist["runbooks"])
    declared.update(f"scripts/{item['name']}" for item in allowlist["entry_points"])
    declared.update(f"process/{name}" for name in package["distribution"]["files"])
    declared.update(f"process/{name}" for name in package["distribution"]["roots"])
    return declared


def _validate_declared_assets(
    payload_root: Path,
    allowlist: Mapping[str, Any],
    package: Mapping[str, Any],
    inventory: list[dict[str, Any]],
) -> None:
    expected_scripts = {item["name"] for item in allowlist["entry_points"]}
    actual_scripts = {path.name for path in (payload_root / "scripts").iterdir() if path.is_file()}
    if actual_scripts != expected_scripts:
        raise OperationError("release.allowlist-mismatch", "public entry-point inventory differs from the allowlist")
    for relative in _declared_top_level(payload_root, allowlist, package):
        if not (payload_root / relative).exists():
            raise OperationError("release.asset-missing", "payload omits a declared release asset")
    exact = set(allowlist["requirements"])
    exact.update(f"docs/runbooks/{name}" for name in allowlist["runbooks"])
    exact.update(f"scripts/{item['name']}" for item in allowlist["entry_points"])
    exact.update(f"process/{name}" for name in package["distribution"]["files"])
    roots = [*allowlist["template_roots"], *(f"process/{name}" for name in package["distribution"]["roots"])]
    for item in inventory:
        path = item["path"]
        if path not in exact and not any(path.startswith(f"{root}/") for root in roots):
            raise OperationError("release.allowlist-closure", "payload contains an undeclared asset")


def validate_release_manifest(
    candidate_root: Path, manifest: Mapping[str, Any], *, now: datetime | None = None
) -> dict[str, Any]:
    """Validate manifest schema and semantic binding to the immutable candidate payload."""
    del now  # Reserved for Task 2 evidence freshness without making Task 1 time-dependent.
    candidate = _safe_directory_root(candidate_root, "release.candidate-missing")
    payload_path = candidate / "payload"
    if os.path.lexists(payload_path):
        payload = _safe_directory_root(payload_path, "release.payload-missing")
        entries = {path.name for path in candidate.iterdir()}
        if entries != {"payload", "release-manifest.yaml"}:
            raise OperationError("release.candidate-closure", "candidate root contains undeclared content")
    else:
        payload = candidate
    schema_path = payload / "process/schemas/release-manifest.schema.json"
    derived = _derived_manifest_fields(payload)
    for field, expected in derived.items():
        if manifest.get(field) != expected:
            raise OperationError("release.manifest-derived-mismatch", f"manifest field is not derived from payload: {field}")
    _validate_schema(manifest, schema_path, "release.manifest-invalid")
    return {
        "operation": "validate-release-manifest", "status": "valid",
        "release_id": manifest["release_id"], "payload_sha256": derived["payload_sha256"],
    }


def _publish_no_replace(staging: Path, target: Path) -> None:
    """Atomically publish a directory and fail if the destination already exists."""
    if os.name == "nt":
        try:
            os.rename(staging, target)
        except OSError as error:
            if os.path.lexists(target):
                raise OperationError("release.destination-exists", "destination appeared during candidate construction") from error
            raise
        return
    if sys.platform.startswith("linux"):
        import ctypes

        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = getattr(libc, "renameat2", None)
        if renameat2 is None:
            raise OperationError("release.atomic-publish-unsupported", "atomic no-replace publication is unavailable", exit_code=3)
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(
            -100, os.fsencode(staging), -100, os.fsencode(target), 1
        )
        if result == 0:
            return
        error_number = ctypes.get_errno()
        if error_number == errno.EEXIST:
            raise OperationError("release.destination-exists", "destination appeared during candidate construction")
        raise OSError(error_number, os.strerror(error_number), str(target))
    raise OperationError("release.atomic-publish-unsupported", "host is not certified for atomic publication", exit_code=3)


def build_release_candidate(repository_root: Path, destination: Path, inputs: ReleaseInputs) -> dict[str, Any]:
    """Atomically create one immutable allowlisted candidate in a new destination."""
    _validate_inputs(inputs)
    root = _safe_directory_root(repository_root, "release.repository-missing")
    requested = Path(destination)
    requested.parent.mkdir(parents=True, exist_ok=True)
    parent = _safe_directory_root(requested.parent, "release.destination-parent-invalid")
    validate_portable_path(requested.name)
    target = parent / requested.name
    if target == root or root in target.parents or target in root.parents:
        raise OperationError("release.path-overlap", "source and destination must not overlap")
    if os.path.lexists(target):
        raise OperationError("release.destination-exists", "destination must not already exist")
    allowlist = _load_mapping(root / "process/release-allowlist.yaml", "release.allowlist-invalid")
    _validate_allowlist(allowlist, root / "process/schemas/release-allowlist.schema.json")
    package = _package_contract(root)
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
        _publish_no_replace(staging, target)
        return manifest
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise
