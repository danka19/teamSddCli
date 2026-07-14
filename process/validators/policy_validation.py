"""Pure static validation and immutable resolution for the policy set."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator

from .config_validation import Diagnostic, secret_diagnostics


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
class EffectiveRule:
    value: Any
    source: str
    policy_id: str
    policy_version: str
    pointer: str


@dataclass(frozen=True)
class PolicySnapshot:
    policy_set_id: str
    policy_set_version: str
    rules: Mapping[str, EffectiveRule]
    corporate_values: Mapping[str, Any]


@dataclass
class PolicyValidationResult:
    diagnostics: list[Diagnostic] = field(default_factory=list)
    snapshot: PolicySnapshot | None = None


def validate_policy_bundle(
    package_root: Path,
    manifest: dict[str, Any],
    config: dict[str, Any],
    adapter: dict[str, Any] | None,
) -> PolicyValidationResult:
    """Validate a pinned local policy set and resolve bounded overrides."""
    result = PolicyValidationResult()
    policy_set = config.get("policy_set", {})
    expected_set = manifest.get("policy_set", {})
    for key in ("id", "version"):
        if policy_set.get(key) != expected_set.get(key):
            result.diagnostics.append(_diag(
                "policy.version-mismatch",
                "Central config and bundled policy-set pins do not match.",
                "central-config",
                f"/policy_set/{key}",
            ))

    corporate = policy_set.get("corporate_values", {})
    if not isinstance(corporate, dict):
        corporate = {}
    for index, requirement in enumerate(manifest.get("required_corporate_values", [])):
        identifier = requirement.get("id")
        if identifier not in corporate or corporate.get(identifier) in (None, "", [], {}):
            result.diagnostics.append(_diag(
                "policy.corporate-value-missing",
                "A required corporate value is missing; no value was guessed.",
                "central-config",
                f"/policy_set/corporate_values/{identifier}",
            ))
        elif not _matches_corporate_type(
            corporate.get(identifier), requirement.get("type")
        ):
            result.diagnostics.append(_diag(
                "policy.corporate-value-invalid",
                "A required corporate value has the wrong declared type.",
                "central-config",
                f"/policy_set/corporate_values/{identifier}",
            ))

    entries = manifest.get("policies", [])
    entry_ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    for duplicate in _duplicates(entry_ids):
        result.diagnostics.append(_diag(
            "policy.policy-id-duplicate",
            "Policy identifiers must be unique.",
            "policy-manifest",
            "/policies",
        ))
    kinds = [entry.get("kind") for entry in entries if isinstance(entry, dict)]
    if len(set(kinds)) != len(kinds):
        result.diagnostics.append(_diag(
            "policy.kind-duplicate",
            "Each policy kind must be selected exactly once.",
            "policy-manifest",
            "/policies",
        ))
    result.diagnostics.extend(_graph_diagnostics(entries, entry_ids))

    rules: dict[str, tuple[dict[str, Any], EffectiveRule]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        document = _load_local_policy(package_root, entry, index, result)
        if document is None:
            continue
        result.diagnostics.extend(
            secret_diagnostics(document, f"policy:{entry.get('id')}", stage=6)
        )
        if (
            document.get("policy_id") != entry.get("id")
            or document.get("version") != entry.get("version")
            or document.get("kind") != entry.get("kind")
        ):
            result.diagnostics.append(_diag(
                "policy.version-mismatch",
                "Manifest and policy document identity or version do not match.",
                "policy-manifest",
                f"/policies/{index}",
            ))
        for rule_index, rule in enumerate(document.get("rules", [])):
            identifier = rule.get("id")
            if identifier in rules:
                result.diagnostics.append(_diag(
                    "policy.rule-id-duplicate",
                    "Rule identifiers must be unique across the policy set.",
                    f"policy:{entry.get('id')}",
                    f"/rules/{rule_index}/id",
                ))
                continue
            effective = EffectiveRule(
                value=_freeze(rule.get("value")),
                source="bundled-policy",
                policy_id=str(entry.get("id")),
                policy_version=str(entry.get("version")),
                pointer=f"/rules/{rule_index}/value",
            )
            rules[str(identifier)] = (rule, effective)

    known_rules = set(rules)
    for identifier, (rule, _) in rules.items():
        for ref in rule.get("refs", []):
            if ref not in known_rules:
                result.diagnostics.append(_diag(
                    "policy.reference-missing",
                    "A policy rule references an unknown rule.",
                    f"policy:{identifier.split('.', 1)[0]}",
                    f"/rules/{identifier}/refs",
                ))
    rule_entries = [
        {"id": identifier, "requires": rule.get("requires", [])}
        for identifier, (rule, _) in rules.items()
    ]
    if _has_cycle(rule_entries):
        result.diagnostics.append(_diag(
            "policy.requirement-cycle",
            "Policy rule requirements must be acyclic.",
            "policy-manifest",
            "/policies",
        ))

    effective = {identifier: item for identifier, (_, item) in rules.items()}
    _apply_overrides(
        policy_set.get("overrides", []),
        "central-config",
        "/policy_set/overrides",
        rules,
        effective,
        result,
    )
    if adapter is not None:
        if "policy_paths" in adapter or "policies" in adapter:
            result.diagnostics.append(_diag(
                "policy.adapter-path-forbidden",
                "A project adapter cannot supply policy paths.",
                "project-adapter",
                "/policy_set/policy_paths",
            ))
        adapter_policy = adapter.get("policy_set", {})
        if isinstance(adapter_policy, dict):
            _apply_overrides(
                adapter_policy.get("overrides", []),
                "project-adapter",
                "/policy_set/overrides",
                rules,
                effective,
                result,
            )

    if not result.diagnostics:
        result.snapshot = PolicySnapshot(
            policy_set_id=str(expected_set.get("id")),
            policy_set_version=str(expected_set.get("version")),
            rules=MappingProxyType(dict(effective)),
            corporate_values=MappingProxyType({
                key: _freeze(value) for key, value in corporate.items()
            }),
        )
    return result


def _load_local_policy(
    package_root: Path,
    entry: dict[str, Any],
    index: int,
    result: PolicyValidationResult,
) -> dict[str, Any] | None:
    relative = entry.get("path")
    schema_relative = entry.get("schema")
    if not isinstance(relative, str) or not isinstance(schema_relative, str):
        return None
    try:
        path = (package_root / relative).resolve()
        schema_path = (package_root / schema_relative).resolve()
        path.relative_to(package_root.resolve())
        schema_path.relative_to(package_root.resolve())
        if not path.is_file() or not schema_path.is_file():
            raise ValueError
        document = yaml.load(
            path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise ValueError
        errors = list(Draft202012Validator(schema).iter_errors(document))
        if errors:
            result.diagnostics.append(_diag(
                "policy.document-invalid",
                "A policy document does not satisfy its pinned local schema.",
                "policy-manifest",
                f"/policies/{index}/path",
            ))
            return None
        return document
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, yaml.YAMLError):
        result.diagnostics.append(_diag(
            "policy.path-invalid",
            "A policy path or schema path is missing, unsafe, or invalid.",
            "policy-manifest",
            f"/policies/{index}/path",
        ))
        return None


def _apply_overrides(
    overrides: Any,
    source: str,
    base_pointer: str,
    rules: dict[str, tuple[dict[str, Any], EffectiveRule]],
    effective: dict[str, EffectiveRule],
    result: PolicyValidationResult,
) -> None:
    if not isinstance(overrides, list):
        return
    for index, override in enumerate(overrides):
        if not isinstance(override, dict):
            continue
        identifier = override.get("rule_id")
        pointer = f"{base_pointer}/{index}"
        if identifier not in rules:
            result.diagnostics.append(_diag(
                "policy.override-unknown-rule",
                "An override references an unknown rule.", source, f"{pointer}/rule_id"
            ))
            continue
        rule, bundled = rules[identifier]
        current = effective[identifier]
        mode = rule.get("override_mode")
        operation = override.get("operation")
        value = override.get("value")
        if mode == "locked":
            result.diagnostics.append(_diag(
                "policy.override-locked",
                "A locked policy minimum cannot be overridden.", source, pointer
            ))
            continue
        if mode == "additive":
            if operation != "add":
                result.diagnostics.append(_diag(
                    "policy.override-additive-delete",
                    "An additive policy minimum can only be extended.", source, pointer
                ))
                continue
            base = list(current.value) if isinstance(current.value, tuple) else []
            additions = value if isinstance(value, list) else [value]
            value = [*base, *[item for item in additions if item not in base]]
        elif mode == "stricter_only":
            if operation != "set" or not _is_stricter(
                current.value, value, rule.get("strictness")
            ):
                result.diagnostics.append(_diag(
                    "policy.override-not-stricter",
                    "A stricter-only override is weaker or not safely comparable.",
                    source,
                    pointer,
                ))
                continue
        elif mode == "replaceable":
            if operation != "set":
                result.diagnostics.append(_diag(
                    "policy.override-operation",
                    "A replaceable slot requires the set operation.", source, pointer
                ))
                continue
        effective[identifier] = EffectiveRule(
            value=_freeze(value),
            source=source,
            policy_id=bundled.policy_id,
            policy_version=bundled.policy_version,
            pointer=f"{pointer}/value",
        )


def _is_stricter(current: Any, proposed: Any, direction: Any) -> bool:
    if isinstance(current, bool) and isinstance(proposed, bool):
        return proposed or not current
    if isinstance(current, (int, float)) and isinstance(proposed, (int, float)):
        if direction == "maximum":
            return proposed <= current
        if direction == "minimum":
            return proposed >= current
        return False
    if isinstance(current, tuple) and isinstance(proposed, list):
        return set(current) <= set(proposed)
    return proposed == current


def _graph_diagnostics(entries: list[Any], known: list[Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    known_set = set(known)
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        for dependency in entry.get("requires", []):
            if dependency not in known_set:
                diagnostics.append(_diag(
                    "policy.reference-missing",
                    "A policy manifest dependency is missing.",
                    "policy-manifest",
                    f"/policies/{index}/requires",
                ))
    if _has_cycle(entries):
        diagnostics.append(_diag(
            "policy.requirement-cycle",
            "Policy manifest dependencies must be acyclic.",
            "policy-manifest",
            "/policies",
        ))
    return diagnostics


def _has_cycle(entries: list[Any]) -> bool:
    graph = {
        entry.get("id"): list(entry.get("requires", []))
        for entry in entries if isinstance(entry, dict) and entry.get("id")
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in graph.get(node, []):
            if child in graph and visit(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def _duplicates(values: list[Any]) -> set[Any]:
    seen: set[Any] = set()
    return {value for value in values if value in seen or seen.add(value)}


def _matches_corporate_type(value: Any, declared: Any) -> bool:
    if declared == "string":
        return isinstance(value, str) and bool(value)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "mapping":
        return isinstance(value, dict)
    return False


def _freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _diag(code: str, message: str, source: str, pointer: str) -> Diagnostic:
    return Diagnostic(
        code,
        "policy",
        message,
        6,
        source=source,
        pointer=pointer,
        hint="Use the pinned manifest and only permitted stronger or additive values.",
    )
