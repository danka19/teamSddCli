"""Pure Tech Lead ownership validation and non-mutating coverage resolution."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
from typing import Any, Mapping, Sequence

from .config_validation import Diagnostic
from .policy_validation import PolicySnapshot


OWNER_SCHEMA_LEGACY = "1.0"
OWNER_SCHEMA_GOVERNANCE = "2.0"

TECH_LEAD_AUTHORITIES = frozenset(
    {
        "classification-confirmation",
        "technical-readiness",
        "architecture-decision",
        "owner-dependency-review",
        "stop-hold",
        "resume",
        "completion-recommendation",
        "release-readiness-recommendation",
    }
)


@dataclass(frozen=True)
class AffectedPath:
    repository: str
    path: str


@dataclass(frozen=True)
class DelegateGrant:
    owner: str
    authority: frozenset[str]


@dataclass(frozen=True)
class TechLeadResolution:
    primary: str | None = None
    zones: tuple[str, ...] = ()
    authority: frozenset[str] = frozenset()
    delegates: tuple[DelegateGrant, ...] = ()
    escalation_route: str | None = None
    policy_set: tuple[str, str] | None = None
    diagnostics: tuple[Diagnostic, ...] = ()


def owner_registry_diagnostics(
    owners: Mapping[str, Any],
    projects: Mapping[str, Any],
    policy: PolicySnapshot,
) -> list[Diagnostic]:
    """Validate v2 governance without changing explicit v1 compatibility."""
    version = owners.get("schema_version")
    if version == OWNER_SCHEMA_LEGACY:
        return []
    if version != OWNER_SCHEMA_GOVERNANCE:
        return [_diag(
            "owners.version-unsupported",
            "The owner registry version is not supported.",
            "/schema_version",
        )]

    diagnostics: list[Diagnostic] = []
    groups, member_roles, group_members = _owner_index(owners)
    known_zones = {
        zone.get("id")
        for zone in owners.get("zones", [])
        if isinstance(zone, Mapping) and isinstance(zone.get("id"), str)
    }
    for project_index, project in enumerate(projects.get("projects", [])):
        if not isinstance(project, Mapping):
            continue
        for zone in project.get("owner_zones", []):
            if zone not in known_zones:
                diagnostics.append(_diag(
                    "owners.project-zone-unresolved",
                    "A project owner zone is absent from the owner registry.",
                    f"/projects/{project_index}/owner_zones",
                    source="projects-registry",
                ))

    expected_primary = policy.corporate_values.get("tech_lead_owner")
    expected_escalation = policy.corporate_values.get("escalation_route")
    for zone_index, zone in enumerate(owners.get("zones", [])):
        if not isinstance(zone, Mapping):
            continue
        base = f"/zones/{zone_index}/tech_lead"
        governance = zone.get("tech_lead")
        if not isinstance(governance, Mapping):
            diagnostics.append(_diag(
                "owners.primary-missing",
                "A governance owner zone must declare one primary Tech Lead.",
                f"{base}/primary",
            ))
            continue

        primary = governance.get("primary")
        if not isinstance(primary, str) or not primary:
            diagnostics.append(_diag(
                "owners.primary-missing",
                "A governance owner zone must declare one primary Tech Lead.",
                f"{base}/primary",
            ))
        else:
            primary_state = _reference_state(primary, "tech_lead", groups, member_roles)
            if primary_state != "valid":
                diagnostics.append(_diag(
                    f"owners.primary-{primary_state}",
                    "The primary Tech Lead reference is absent or has the wrong role.",
                    f"{base}/primary",
                ))
            elif isinstance(expected_primary, str) and not _within_reference(
                primary, expected_primary, group_members
            ):
                diagnostics.append(_diag(
                    "owners.primary-policy-conflict",
                    "The primary Tech Lead is outside the immutable configured owner slot.",
                    f"{base}/primary",
                ))

        authority = _authority_set(governance.get("authority"))
        if not authority <= TECH_LEAD_AUTHORITIES:
            diagnostics.append(_diag(
                "owners.authority-forbidden",
                "Tech Lead authority includes a decision reserved for another human role.",
                f"{base}/authority",
            ))

        for delegate_index, delegate in enumerate(governance.get("delegates", [])):
            if not isinstance(delegate, Mapping):
                continue
            delegate_base = f"{base}/delegates/{delegate_index}"
            owner = delegate.get("owner")
            if isinstance(owner, str):
                state = _reference_state(owner, "tech_lead", groups, member_roles)
                if state != "valid":
                    diagnostics.append(_diag(
                        f"owners.delegate-{state}",
                        "A delegate reference is absent or has the wrong role.",
                        f"{delegate_base}/owner",
                    ))
            delegated = _authority_set(delegate.get("authority"))
            if not delegated <= TECH_LEAD_AUTHORITIES:
                diagnostics.append(_diag(
                    "owners.authority-forbidden",
                    "Delegate authority includes a decision reserved for another role.",
                    f"{delegate_base}/authority",
                ))
            elif not delegated <= authority:
                diagnostics.append(_diag(
                    "owners.delegate-authority-broader",
                    "A delegate cannot receive broader authority than the primary Tech Lead.",
                    f"{delegate_base}/authority",
                ))

        escalation = governance.get("escalation_route")
        if isinstance(escalation, str):
            state = _reference_state(
                escalation, ("process_owner", "tech_lead"), groups, member_roles
            )
            if state != "valid":
                diagnostics.append(_diag(
                    f"owners.escalation-{state}",
                    "The escalation route is absent or has the wrong role.",
                    f"{base}/escalation_route",
                ))
            elif isinstance(expected_escalation, str) and not _within_reference(
                escalation, expected_escalation, group_members
            ):
                diagnostics.append(_diag(
                    "owners.escalation-policy-conflict",
                    "The escalation route conflicts with the immutable configured route.",
                    f"{base}/escalation_route",
                ))
    return diagnostics


def resolve_tech_lead_ownership(
    owners: Mapping[str, Any],
    projects: Mapping[str, Any],
    affected: Sequence[AffectedPath],
    policy: PolicySnapshot,
) -> TechLeadResolution:
    """Resolve read-only Tech Lead coverage for repository-relative affected paths."""
    policy_set = (policy.policy_set_id, policy.policy_set_version)
    if owners.get("schema_version") != OWNER_SCHEMA_GOVERNANCE:
        return TechLeadResolution(
            policy_set=policy_set,
            diagnostics=(_diag(
                "owners.governance-version-required",
                "Tech Lead decision support requires the explicit owner registry v2 contract.",
                "/schema_version",
            ),),
        )

    diagnostics = owner_registry_diagnostics(owners, projects, policy)
    if diagnostics:
        return TechLeadResolution(policy_set=policy_set, diagnostics=tuple(diagnostics))

    project_index = {
        project.get("id"): project
        for project in projects.get("projects", [])
        if isinstance(project, Mapping)
    }
    zone_index = {
        zone.get("id"): zone
        for zone in owners.get("zones", [])
        if isinstance(zone, Mapping)
    }
    matched: list[Mapping[str, Any]] = []
    matched_ids: list[str] = []
    for item in affected:
        project = project_index.get(item.repository)
        if project is None:
            diagnostics.append(_diag(
                "owners.affected-repository-unresolved",
                "An affected repository is absent from the project registry.",
                "/affected/repository",
                source="affected-scope",
            ))
            continue
        candidates = [
            zone_index[zone_id]
            for zone_id in project.get("owner_zones", [])
            if zone_id in zone_index
        ]
        path_matches = [
            zone for zone in candidates if _zone_matches(zone, item.repository, item.path)
        ]
        if not path_matches:
            diagnostics.append(_diag(
                "owners.affected-path-uncovered",
                "An affected path has no explicit Tech Lead owner-zone coverage.",
                "/affected/path",
                source="affected-scope",
            ))
            continue
        for zone in path_matches:
            zone_id = str(zone.get("id"))
            if zone_id not in matched_ids:
                matched_ids.append(zone_id)
                matched.append(zone)

    if diagnostics:
        return TechLeadResolution(policy_set=policy_set, diagnostics=tuple(diagnostics))

    primaries = {
        zone["tech_lead"]["primary"] for zone in matched
    }
    if len(primaries) != 1:
        return TechLeadResolution(
            zones=tuple(matched_ids),
            policy_set=policy_set,
            diagnostics=(_diag(
                "owners.primary-conflict",
                "Affected owner zones resolve to conflicting primary Tech Leads.",
                "/affected",
                source="affected-scope",
            ),),
        )

    authorities = {
        frozenset(zone["tech_lead"]["authority"]) for zone in matched
    }
    if len(authorities) != 1:
        return TechLeadResolution(
            primary=next(iter(primaries)),
            zones=tuple(matched_ids),
            policy_set=policy_set,
            diagnostics=(_diag(
                "owners.authority-conflict",
                "Overlapping affected zones declare incompatible Tech Lead authority.",
                "/affected",
                source="affected-scope",
            ),),
        )

    governance = matched[0]["tech_lead"]
    delegates = tuple(
        DelegateGrant(
            owner=delegate["owner"],
            authority=frozenset(delegate["authority"]),
        )
        for delegate in governance.get("delegates", [])
    )
    return TechLeadResolution(
        primary=next(iter(primaries)),
        zones=tuple(matched_ids),
        authority=next(iter(authorities)),
        delegates=delegates,
        escalation_route=governance["escalation_route"],
        policy_set=policy_set,
    )


def _owner_index(
    owners: Mapping[str, Any],
) -> tuple[
    dict[str, frozenset[str]],
    dict[str, frozenset[str]],
    dict[str, frozenset[str]],
]:
    groups: dict[str, frozenset[str]] = {}
    group_members: dict[str, frozenset[str]] = {}
    member_roles: dict[str, set[str]] = {}
    for group in owners.get("owner_groups", []):
        if not isinstance(group, Mapping) or not isinstance(group.get("id"), str):
            continue
        roles = frozenset(role for role in group.get("roles", []) if isinstance(role, str))
        groups[group["id"]] = roles
        group_members[group["id"]] = frozenset(
            member for member in group.get("members", []) if isinstance(member, str)
        )
        for member in group.get("members", []):
            if isinstance(member, str):
                member_roles.setdefault(member, set()).update(roles)
    return (
        groups,
        {member: frozenset(roles) for member, roles in member_roles.items()},
        group_members,
    )


def _reference_state(
    reference: str,
    required: str | tuple[str, ...],
    groups: Mapping[str, frozenset[str]],
    member_roles: Mapping[str, frozenset[str]],
) -> str:
    roles = groups.get(reference) or member_roles.get(reference)
    if roles is None:
        return "unresolved"
    required_roles = (required,) if isinstance(required, str) else required
    return "valid" if any(role in roles for role in required_roles) else "wrong-role"


def _within_reference(
    candidate: str, expected: str, group_members: Mapping[str, frozenset[str]]
) -> bool:
    if candidate == expected:
        return True
    return candidate in group_members.get(expected, frozenset())


def _authority_set(value: Any) -> frozenset[str]:
    if not isinstance(value, list):
        return frozenset()
    return frozenset(item for item in value if isinstance(item, str))


def _zone_matches(zone: Mapping[str, Any], repository: str, path: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("/")
    repository_path = f"{repository}/{normalized}"
    return any(
        isinstance(pattern, str)
        and (fnmatchcase(normalized, pattern) or fnmatchcase(repository_path, pattern))
        for pattern in zone.get("paths", [])
    )


def _diag(
    code: str,
    message: str,
    pointer: str,
    *,
    source: str = "owners-registry",
) -> Diagnostic:
    return Diagnostic(
        code=code,
        category="ownership",
        message=message,
        stage=8,
        source=source,
        pointer=pointer,
        hint="Resolve the human owner mapping without assigning authority to AI or another role.",
    )
