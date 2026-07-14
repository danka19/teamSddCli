"""Bounded discovery and loading for process configuration validation."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import MappingProxyType
from typing import Any, Callable
from urllib.parse import urljoin, urlsplit
from urllib.request import url2pathname

import yaml
from jsonschema import Draft202012Validator

from .config_validation import (
    OPENSPEC_VERSION,
    Diagnostic,
    ValidationResult,
    adapter_compatibility,
    config_compatibility,
    integrity_diagnostics,
    package_compatibility,
    schema_diagnostics,
    secret_diagnostics,
)
from .policy_validation import validate_policy_bundle


MAX_FILE_BYTES = 1_048_576
BUNDLED_SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas"
REFERENCE_PATTERN = re.compile(r"^(sibling|registry|path):(.+)$")
REFERENCE_ID = re.compile(r"^[a-z][a-z0-9-]*$")
PORTABLE_PATH = re.compile(r"^[A-Za-z0-9 _.-]+(?:/[A-Za-z0-9 _.-]+)*$")
RESERVED_SEGMENT = re.compile(r"^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?$", re.I)


class DuplicateKeyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    value: dict[Any, Any] = {}
    for key_node, item_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in value:
            raise DuplicateKeyError("duplicate mapping key")
        value[key] = loader.construct_object(item_node, deep=deep)
    return value


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def detect_repository_root(start: Path) -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return start.resolve()
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else start.resolve()


def default_runtime_probe() -> str:
    executable = shutil.which("openspec")
    if executable is None:
        raise FileNotFoundError("openspec")
    result = subprocess.run(
        [executable, "--version"], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def load_yaml(path: Path, source: str, result: ValidationResult, stage: int = 2) -> Any | None:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("file exceeds the 1 MiB validation limit")
        text = path.read_text(encoding="utf-8")
        value = yaml.load(text, Loader=UniqueKeyLoader)
    except DuplicateKeyError:
        result.add(Diagnostic(
            "yaml.duplicate-key", "yaml", "Duplicate YAML mapping key is not allowed.",
            stage, source=source, hint="Remove the duplicate key and keep one explicit value.",
        ))
        return None
    except (OSError, UnicodeError, yaml.YAMLError, ValueError):
        result.add(Diagnostic(
            "yaml.invalid", "yaml", "The declared YAML document is unreadable or malformed.",
            stage, source=source, hint="Provide bounded UTF-8 YAML with unique mapping keys.",
        ))
        return None
    if not isinstance(value, dict):
        result.add(Diagnostic(
            "yaml.invalid", "yaml", "The YAML document root must be a mapping.",
            stage, source=source,
        ))
        return None
    return value


def load_schema_resources(schema_root: Path) -> Mapping[str, Any]:
    """Load a deeply immutable snapshot of local JSON Schema resources."""
    resources: dict[str, Any] = {}
    for path in sorted(schema_root.glob("*.json")):
        if path.stat().st_size > MAX_FILE_BYTES:
            raise ValueError("schema resource exceeds validation limit")
        resources[path.name] = _freeze_json(
            json.loads(path.read_text(encoding="utf-8"))
        )
    return MappingProxyType(resources)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType(
            {key: _freeze_json(child) for key, child in value.items()}
        )
    if isinstance(value, list):
        return tuple(_freeze_json(child) for child in value)
    return value


def validate_configuration(
    start: Path,
    registry: dict[str, Path],
    runtime_probe: Callable[[], str] | None = None,
) -> ValidationResult:
    result = ValidationResult()
    root = detect_repository_root(start)
    central_path = root / "sdd.config.yaml"
    adapter_path = root / ".sdd-project.yaml"
    present = [path for path in (central_path, adapter_path) if path.is_file()]
    if not present:
        result.add(Diagnostic(
            "discovery.config-missing", "discovery",
            "Neither approved configuration file exists at the detected repository root.", 1,
            hint="Add exactly one sdd.config.yaml or .sdd-project.yaml at the repository root.",
        ))
        return result
    if len(present) == 2:
        result.add(Diagnostic(
            "discovery.config-ambiguous", "discovery",
            "Both approved configuration files exist at the detected repository root.", 1,
            hint="Keep exactly one central config or project adapter at this root.",
        ))
        return result

    schema_resources = load_schema_resources(BUNDLED_SCHEMA_ROOT)

    adapter: dict[str, Any] | None = None
    if adapter_path.is_file():
        result.mode = "adapter"
        adapter = load_yaml(adapter_path, "project-adapter", result)
        if adapter is None:
            return result
        result.add(*secret_diagnostics(adapter, "project-adapter"))
        if "policy_paths" in adapter or "policies" in adapter:
            result.add(Diagnostic(
                "policy.adapter-path-forbidden",
                "policy",
                "A project adapter cannot supply policy paths.",
                4,
                source="project-adapter",
                pointer="/policy_paths",
                hint="Use only the policy set pinned by the central config.",
            ))
        if result.diagnostics:
            return result
        result.add(*schema_diagnostics(
            "project-adapter.schema.json", adapter, "project-adapter", stage=4,
            schema_resources=schema_resources,
        ))
        result.add(*adapter_compatibility(adapter))
        if result.diagnostics:
            reference = adapter.get("team_specs", {}).get("reference")
            if isinstance(reference, str) and not valid_reference_shape(reference):
                _invalid_reference(result, "project-adapter", "/team_specs/reference")
            return result
        central_root = resolve_reference(
            adapter["team_specs"]["reference"], root, registry, result,
            source="project-adapter", pointer="/team_specs/reference",
        )
        if central_root is None:
            return result
        central_path = central_root / adapter["team_specs"]["config_path"]
        if central_path.is_file() and (central_root / ".sdd-project.yaml").is_file():
            result.add(Diagnostic(
                "discovery.config-ambiguous", "discovery",
                "The resolved central repository contains both approved config files.", 1,
                hint="Keep only sdd.config.yaml in the referenced central repository.",
            ))
            return result
        if not central_path.is_file():
            result.add(Diagnostic(
                "reference.unresolved", "reference",
                "The resolved central repository does not contain its declared config.", 1,
                source="project-adapter", pointer="/team_specs/config_path",
            ))
            return result
    else:
        result.mode = "central"
        central_root = root

    config = load_yaml(central_path, "central-config", result)
    if config is None:
        return result
    result.add(*secret_diagnostics(config, "central-config"))
    if result.diagnostics:
        return result
    result.add(*schema_diagnostics(
        "sdd-config.schema.json", config, "central-config", stage=4,
        schema_resources=schema_resources,
    ))
    result.add(*config_compatibility(config))
    if result.diagnostics:
        return result

    package_root = resolve_package_location(config["process_package"]["location"], central_root, registry, result)
    if package_root is None:
        return result
    package = load_yaml(package_root / "package.yaml", "process-package", result, stage=5)
    if package is None:
        return result
    result.add(*secret_diagnostics(package, "process-package"))
    if result.diagnostics:
        return result
    result.add(*schema_diagnostics(
        "process-package.schema.json", package, "process-package", stage=5,
        schema_resources=schema_resources,
    ))
    if result.diagnostics:
        return result

    workflow_path = safe_package_path(package_root, package.get("workflow"), result, "process-package", "/workflow")
    if workflow_path is None:
        return result
    workflow = load_yaml(workflow_path, "process-workflow", result, stage=5)
    if workflow is None:
        return result
    result.add(*secret_diagnostics(workflow, "process-workflow"))
    result.add(*schema_diagnostics(
        "workflow.schema.json", workflow, "process-workflow", stage=5,
        schema_resources=schema_resources,
    ))
    validate_package_schemas(package_root, package.get("schemas"), result)
    version = load_version(package_root / "VERSION", result)
    if result.diagnostics:
        return result

    policy_manifest_path = safe_package_path(
        package_root,
        package.get("policies"),
        result,
        "process-package",
        "/policies",
    )
    if policy_manifest_path is None:
        return result
    policy_manifest = load_yaml(
        policy_manifest_path, "policy-manifest", result, stage=6
    )
    if policy_manifest is None:
        return result
    result.add(*secret_diagnostics(policy_manifest, "policy-manifest", stage=6))
    result.add(*schema_diagnostics(
        "policy-manifest.schema.json",
        policy_manifest,
        "policy-manifest",
        stage=6,
        schema_resources=schema_resources,
    ))
    if result.diagnostics:
        return result
    policy_result = validate_policy_bundle(
        package_root, policy_manifest, config, adapter
    )
    result.add(*policy_result.diagnostics)
    if result.diagnostics:
        return result

    projects_path = safe_registry_path(central_root, config["registries"]["projects"], result, "/registries/projects")
    owners_path = safe_registry_path(central_root, config["registries"]["owners"], result, "/registries/owners")
    if projects_path is None or owners_path is None:
        return result
    projects = load_yaml(projects_path, "projects-registry", result, stage=8)
    owners = load_yaml(owners_path, "owners-registry", result, stage=8)
    if projects is None or owners is None:
        return result
    result.add(*secret_diagnostics(projects, "projects-registry"))
    result.add(*secret_diagnostics(owners, "owners-registry"))
    if result.diagnostics:
        return result
    result.add(*schema_diagnostics(
        "projects.schema.json", projects, "projects-registry", stage=8,
        schema_resources=schema_resources,
    ))
    result.add(*schema_diagnostics(
        "owners.schema.json", owners, "owners-registry", stage=8,
        schema_resources=schema_resources,
    ))
    if result.diagnostics:
        return result

    result.add(*package_compatibility(config, package, workflow, version, adapter))
    for index, project in enumerate(projects["projects"]):
        resolve_reference(
            project["repository"]["reference"], central_root, registry, result,
            source="projects-registry", pointer=f"/projects/{index}/repository/reference",
        )
    result.add(*integrity_diagnostics(projects, owners, adapter))
    if result.diagnostics:
        return result

    probe = runtime_probe or default_runtime_probe
    try:
        result.runtime_version = probe()
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        result.add(Diagnostic(
            "runtime.openspec-unavailable", "operational",
            "The OpenSpec runtime could not be executed.", 9,
            hint="Install the pinned OpenSpec CLI and make it available to this process.",
        ))
        return result
    result.runtime_version = result.runtime_version.strip()
    if result.runtime_version != OPENSPEC_VERSION:
        result.add(Diagnostic(
            "compat.openspec-runtime", "compatibility",
            f"OpenSpec runtime is incompatible; required version is {OPENSPEC_VERSION}.", 9,
            source="openspec-runtime", hint="Install and run the exact pinned OpenSpec version.",
        ))
    return result


def resolve_reference(
    reference: str, declaring_root: Path, registry: dict[str, Path], result: ValidationResult,
    *, source: str, pointer: str,
) -> Path | None:
    match = REFERENCE_PATTERN.fullmatch(reference) if isinstance(reference, str) else None
    if match is None:
        result.add(Diagnostic(
            "reference.invalid", "reference", "Repository reference uses an unsupported form.", 1,
            source=source, pointer=pointer,
        ))
        return None
    scheme, value = match.groups()
    if scheme in {"sibling", "registry"} and not REFERENCE_ID.fullmatch(value):
        return _invalid_reference(result, source, pointer)
    if scheme == "sibling":
        candidate = declaring_root.parent / value
    elif scheme == "registry":
        if value not in registry:
            result.add(Diagnostic(
                "reference.registry-missing", "reference",
                "No explicit CLI registry mapping exists for this identifier.", 1,
                source=source, pointer=pointer,
                hint="Pass --registry ID=PATH; environment and network guessing are disabled.",
            ))
            return None
        candidate = registry[value]
    else:
        if not portable_relative_path(value):
            return _invalid_reference(result, source, pointer)
        candidate = (declaring_root / Path(*value.split("/"))).resolve()
        try:
            candidate.relative_to(declaring_root.resolve())
        except ValueError:
            return _invalid_reference(result, source, pointer)
    candidate = candidate.resolve()
    if not candidate.is_dir():
        result.add(Diagnostic(
            "reference.unresolved", "reference", "The declared repository reference does not resolve.", 1,
            source=source, pointer=pointer,
        ))
        return None
    return candidate


def portable_relative_path(value: str) -> bool:
    if not PORTABLE_PATH.fullmatch(value):
        return False
    return all(
        segment not in {".", ".."}
        and not segment.endswith((".", " "))
        and not RESERVED_SEGMENT.fullmatch(segment)
        for segment in value.split("/")
    )


def valid_reference_shape(reference: str) -> bool:
    match = REFERENCE_PATTERN.fullmatch(reference)
    if match is None:
        return False
    scheme, value = match.groups()
    return (
        bool(REFERENCE_ID.fullmatch(value))
        if scheme in {"sibling", "registry"}
        else portable_relative_path(value)
    )


def _invalid_reference(result: ValidationResult, source: str, pointer: str) -> None:
    result.add(Diagnostic(
        "reference.invalid", "reference", "Repository reference violates the portable reference contract.", 1,
        source=source, pointer=pointer,
    ))
    return None


def resolve_package_location(value: Any, central_root: Path, registry: dict[str, Path], result: ValidationResult) -> Path | None:
    if isinstance(value, str) and REFERENCE_PATTERN.fullmatch(value):
        return resolve_reference(
            value, central_root, registry, result,
            source="central-config", pointer="/process_package/location",
        )
    if (
        not isinstance(value, str)
        or not value
        or PurePosixPath(value).is_absolute()
        or bool(PureWindowsPath(value).anchor)
        or "\x00" in value
    ):
        result.add(Diagnostic(
            "package.location-invalid", "reference", "Process package location is not a safe declared path.", 5,
            source="central-config", pointer="/process_package/location",
        ))
        return None
    candidate = (central_root / value).resolve()
    if not candidate.is_dir():
        result.add(Diagnostic(
            "package.missing", "package", "The declared process package directory does not exist.", 5,
            source="central-config", pointer="/process_package/location",
        ))
        return None
    return candidate


def safe_package_path(root: Path, value: Any, result: ValidationResult, source: str, pointer: str) -> Path | None:
    if not isinstance(value, str) or Path(value).is_absolute():
        return _unsafe_asset(result, source, pointer)
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return _unsafe_asset(result, source, pointer)
    if not candidate.is_file():
        result.add(Diagnostic(
            "package.asset-missing", "package", "A declared process-package asset is missing.", 5,
            source=source, pointer=pointer,
        ))
        return None
    return candidate


def _unsafe_asset(result: ValidationResult, source: str, pointer: str) -> None:
    result.add(Diagnostic(
        "package.asset-unsafe", "security", "A package asset path escapes the declared package.", 5,
        source=source, pointer=pointer,
    ))
    return None


def validate_package_schemas(root: Path, schemas: Any, result: ValidationResult) -> None:
    if not isinstance(schemas, dict):
        return
    schema_root = (root / "schemas").resolve()
    visited: set[Path] = set()
    for name, relative in sorted(schemas.items()):
        path = safe_package_path(root, relative, result, "process-package", f"/schemas/{name}")
        if path is None:
            continue
        try:
            _validate_schema_resource(path, schema_root, visited)
        except Exception:
            # jsonschema exposes several validation exception types; none are safe to render verbatim.
            result.add(Diagnostic(
                "package.schema-invalid", "schema",
                "A declared package schema is invalid or has a non-local reference.", 5,
                source="process-package", pointer=f"/schemas/{name}",
            ))


def _validate_schema_resource(
    path: Path, schema_root: Path, visited: set[Path]
) -> None:
    path = path.resolve()
    path.relative_to(schema_root)
    if path in visited:
        return
    visited.add(path)
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("schema resource exceeds validation limit")
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    _validate_schema_references(schema, path.as_uri(), schema_root, visited)


def _validate_schema_references(
    value: Any, base_uri: str, schema_root: Path, visited: set[Path]
) -> None:
    if isinstance(value, dict):
        effective_base = base_uri
        if isinstance(value.get("$id"), str):
            effective_base = urljoin(base_uri, value["$id"])
        for keyword in ("$ref", "$dynamicRef"):
            reference = value.get(keyword)
            if isinstance(reference, str):
                _validate_schema_reference(
                    reference, effective_base, schema_root, visited
                )
        for child in value.values():
            _validate_schema_references(child, effective_base, schema_root, visited)
    elif isinstance(value, list):
        for child in value:
            _validate_schema_references(child, base_uri, schema_root, visited)


def _validate_schema_reference(
    reference: str, base_uri: str, schema_root: Path, visited: set[Path]
) -> None:
    authored = urlsplit(reference)
    if not authored.path and not authored.query:
        return
    if (
        authored.scheme
        or authored.netloc
        or PurePosixPath(authored.path).is_absolute()
        or bool(PureWindowsPath(authored.path).anchor)
    ):
        raise ValueError("non-local schema reference")
    resolved = urlsplit(urljoin(base_uri, reference))
    if resolved.scheme != "file" or resolved.netloc:
        raise ValueError("non-local schema reference")
    target = Path(url2pathname(resolved.path)).resolve()
    target.relative_to(schema_root)
    if not target.is_file():
        raise ValueError("missing local schema reference")
    _validate_schema_resource(target, schema_root, visited)


def safe_registry_path(root: Path, value: Any, result: ValidationResult, pointer: str) -> Path | None:
    if not isinstance(value, str) or not portable_relative_path(value):
        result.add(Diagnostic(
            "registry.path-unsafe", "security", "Registry path must stay within the central repository.", 8,
            source="central-config", pointer=pointer,
        ))
        return None
    candidate = (root / Path(*value.split("/"))).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        result.add(Diagnostic(
            "registry.path-unsafe", "security", "Registry path must stay within the central repository.", 8,
            source="central-config", pointer=pointer,
        ))
        return None
    if not candidate.is_file():
        result.add(Diagnostic(
            "registry.missing", "reference", "A declared registry file is missing.", 8,
            source="central-config", pointer=pointer,
        ))
        return None
    return candidate


def load_version(path: Path, result: ValidationResult) -> str:
    try:
        if path.stat().st_size > 128:
            raise ValueError
        return path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError, ValueError):
        result.add(Diagnostic(
            "package.version-missing", "package", "Package VERSION is missing or invalid.", 5,
            source="package-version",
        ))
        return ""
