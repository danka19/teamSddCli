"""Scenario-first tests for Phase 2 work item 2.6 owner governance."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from process.validators.owners import (
    AffectedPath,
    owner_registry_diagnostics,
    resolve_tech_lead_ownership,
)
from process.validators.policy_validation import EffectiveRule, PolicySnapshot
from tests.test_validate_process_config import (
    build_central_layout,
    diagnostic_codes,
    read_yaml,
    run_cli,
    write_yaml,
)


TECHNICAL_AUTHORITY = [
    "classification-confirmation",
    "technical-readiness",
    "architecture-decision",
    "owner-dependency-review",
    "stop-hold",
    "resume",
    "completion-recommendation",
    "release-readiness-recommendation",
]


def policy_snapshot() -> PolicySnapshot:
    return PolicySnapshot(
        policy_set_id="sdd-core",
        policy_set_version="1.0.0",
        rules={
            "flow.production-stop-triggers": EffectiveRule(
                value=("owner-authority-conflict",),
                source="bundled-policy",
                policy_id="flow-controls",
                policy_version="1.0.0",
                pointer="/rules/0/value",
            )
        },
        corporate_values={
            "tech_lead_owner": "sample-tech-leads",
            "qa_owner": "sample-qa-owners",
            "escalation_route": "sample-process-owners",
            "evidence_retention_days": 30,
        },
    )


def governed_owners() -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "owner_groups": [
            {
                "id": "sample-tech-leads",
                "roles": ["tech_lead"],
                "members": ["sample-primary", "sample-delegate"],
            },
            {
                "id": "sample-process-owners",
                "roles": ["process_owner"],
                "members": ["sample-escalation-owner"],
            },
            {
                "id": "sample-qa-owners",
                "roles": ["qa"],
                "members": ["sample-qa-owner"],
            },
        ],
        "zones": [
            {
                "id": "sample-app",
                "paths": ["src/**", "tests/**"],
                "owner_groups": ["sample-tech-leads", "sample-qa-owners"],
                "tech_lead": {
                    "primary": "sample-primary",
                    "authority": list(TECHNICAL_AUTHORITY),
                    "delegates": [
                        {
                            "owner": "sample-delegate",
                            "authority": [
                                "technical-readiness",
                                "owner-dependency-review",
                                "stop-hold",
                            ],
                        }
                    ],
                    "escalation_route": "sample-process-owners",
                },
            }
        ],
        "default_owner_groups": ["sample-tech-leads"],
    }


def projects() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "projects": [
            {
                "id": "sample-app",
                "repository": {"reference": "sibling:sample-app"},
                "adapter_allowed": True,
                "owner_zones": ["sample-app"],
                "local_paths": {"code": "src", "tests": "tests"},
            }
        ],
    }


def codes(diagnostics: object) -> list[str]:
    return [item.code for item in diagnostics]


def test_valid_owner_governance_resolves_bounded_immutable_coverage() -> None:
    owners = governed_owners()

    diagnostics = owner_registry_diagnostics(owners, projects(), policy_snapshot())
    resolution = resolve_tech_lead_ownership(
        owners,
        projects(),
        [AffectedPath(repository="sample-app", path="src/domain/service.py")],
        policy_snapshot(),
    )

    assert diagnostics == []
    assert resolution.diagnostics == ()
    assert resolution.primary == "sample-primary"
    assert resolution.zones == ("sample-app",)
    assert resolution.authority == frozenset(TECHNICAL_AUTHORITY)
    assert resolution.delegates[0].owner == "sample-delegate"
    assert resolution.delegates[0].authority == frozenset(
        {"technical-readiness", "owner-dependency-review", "stop-hold"}
    )
    assert resolution.policy_set == ("sdd-core", "1.0.0")


def test_legacy_owner_registry_is_explicitly_compatible_but_not_governance_ready() -> None:
    owners = governed_owners()
    owners["schema_version"] = "1.0"
    for zone in owners["zones"]:
        del zone["tech_lead"]

    assert owner_registry_diagnostics(owners, projects(), policy_snapshot()) == []
    resolution = resolve_tech_lead_ownership(
        owners,
        projects(),
        [AffectedPath(repository="sample-app", path="src/domain/service.py")],
        policy_snapshot(),
    )

    assert codes(resolution.diagnostics) == ["owners.governance-version-required"]


def test_missing_and_conflicting_primary_fail_closed() -> None:
    owners = governed_owners()
    del owners["zones"][0]["tech_lead"]["primary"]
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.primary-missing"
    ]

    owners = governed_owners()
    owners["owner_groups"][0]["members"].append("sample-other-primary")
    owners["zones"].append(
        {
            "id": "sample-app-nested",
            "paths": ["src/domain/**"],
            "owner_groups": ["sample-tech-leads"],
            "tech_lead": {
                "primary": "sample-other-primary",
                "authority": list(TECHNICAL_AUTHORITY),
                "delegates": [],
                "escalation_route": "sample-process-owners",
            },
        }
    )
    projects()["projects"][0]["owner_zones"].append("sample-app-nested")
    conflicting_projects = projects()
    conflicting_projects["projects"][0]["owner_zones"].append("sample-app-nested")
    resolution = resolve_tech_lead_ownership(
        owners,
        conflicting_projects,
        [AffectedPath(repository="sample-app", path="src/domain/service.py")],
        policy_snapshot(),
    )

    assert codes(resolution.diagnostics) == ["owners.primary-conflict"]


def test_unresolved_and_wrong_role_owner_references_fail_closed() -> None:
    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["primary"] = "missing-owner"
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.primary-unresolved"
    ]

    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["delegates"][0]["owner"] = "sample-qa-owner"
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.delegate-wrong-role"
    ]

    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["escalation_route"] = "sample-qa-owners"
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.escalation-wrong-role"
    ]


def test_delegate_authority_cannot_exceed_primary_or_cross_role_boundary() -> None:
    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["authority"].remove("resume")
    owners["zones"][0]["tech_lead"]["delegates"][0]["authority"].append("resume")
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.delegate-authority-broader"
    ]

    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["authority"].append("qa-approval")
    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.authority-forbidden"
    ]


@pytest.mark.parametrize(
    "authority",
    [
        "qa-approval", "product-approval", "security-approval",
        "release-approval", "merge-approval", "archive-approval",
        "tracker-approval",
    ],
)
def test_tech_lead_cannot_claim_independent_role_authority(authority: str) -> None:
    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["authority"].append(authority)

    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.authority-forbidden"
    ]


def test_zone_primary_cannot_escape_immutable_configured_owner_slot() -> None:
    owners = governed_owners()
    owners["owner_groups"].append(
        {
            "id": "alternate-tech-leads",
            "roles": ["tech_lead"],
            "members": ["alternate-primary"],
        }
    )
    owners["zones"][0]["tech_lead"]["primary"] = "alternate-primary"

    assert codes(owner_registry_diagnostics(owners, projects(), policy_snapshot())) == [
        "owners.primary-policy-conflict"
    ]


def test_uncovered_affected_repository_or_path_fails_closed() -> None:
    resolution = resolve_tech_lead_ownership(
        governed_owners(),
        projects(),
        [
            AffectedPath(repository="sample-app", path="docs/guide.md"),
            AffectedPath(repository="unknown-repository", path="src/app.py"),
        ],
        policy_snapshot(),
    )

    assert codes(resolution.diagnostics) == [
        "owners.affected-path-uncovered",
        "owners.affected-repository-unresolved",
    ]


def test_config_discovery_uses_v2_owner_validation_and_policy_snapshot(
    tmp_path: Path,
) -> None:
    root = build_central_layout(tmp_path / "central")
    owners = governed_owners()
    owners["zones"][0]["tech_lead"]["authority"].append("archive-approval")
    write_yaml(root / "owners.yaml", owners)
    registered_projects = read_yaml(root / "projects.yaml")
    registered_projects["projects"][0]["owner_zones"] = ["sample-app"]
    write_yaml(root / "projects.yaml", registered_projects)
    config = read_yaml(root / "sdd.config.yaml")
    config["policy_set"]["corporate_values"]["tech_lead_owner"] = "sample-tech-leads"
    config["policy_set"]["corporate_values"]["qa_owner"] = "sample-qa-owners"
    config["policy_set"]["corporate_values"]["escalation_route"] = (
        "sample-process-owners"
    )
    write_yaml(root / "sdd.config.yaml", config)

    code, stdout, stderr = run_cli([str(root), "--json"], lambda: "1.4.1")

    assert (code, stderr) == (1, "")
    assert diagnostic_codes(stdout) == ["owners.authority-forbidden"]
    diagnostic = json.loads(stdout)["diagnostics"][0]
    assert diagnostic["source"] == "owners-registry"
    assert diagnostic["pointer"].endswith("/authority")


SCENARIO_COVERAGE = {
    "test_valid_owner_governance_resolves_bounded_immutable_coverage": [
        {
            "capability": "repo-topology-config",
            "requirement": "Tech lead ownership registry",
            "scenario": "Tech lead mapping is resolvable",
            "source_kind": "delta"
        },
        {
            "source_kind": "accepted",
            "capability": "repo-topology-config",
            "requirement": "Owner registry and reviewer assignment",
            "scenario": "owners.yaml is the owner source"
        },
        {
            "source_kind": "accepted",
            "capability": "repo-topology-config",
            "requirement": "Owner registry and reviewer assignment",
            "scenario": "Multi-zone changes require all affected owners"
        }
    ],
    "test_uncovered_affected_repository_or_path_fails_closed": [
        {
            "source_kind": "accepted",
            "capability": "repo-topology-config",
            "requirement": "Owner registry and reviewer assignment",
            "scenario": "Unowned paths are visible"
        }
    ],
    "test_missing_and_conflicting_primary_fail_closed": [
        {
            "capability": "repo-topology-config",
            "requirement": "Tech lead ownership registry",
            "scenario": "Conflicting authority is visible",
            "source_kind": "delta"
        }
    ],
    "test_tech_lead_cannot_claim_independent_role_authority": [
        {
            "capability": "repo-topology-config",
            "requirement": "Tech lead ownership registry",
            "scenario": "Other role authority is preserved",
            "source_kind": "delta"
        }
    ]
}
