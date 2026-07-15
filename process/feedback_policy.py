"""Pure deterministic feedback/publication-boundary evaluation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


DISPOSITIONS = {"accepted", "rejected", "deferred", "duplicate", "approved-waiver"}


def evaluate_feedback_policy(payload: dict[str, Any], process_root: Path | None = None) -> dict[str, Any]:
    root = process_root or Path(__file__).resolve().parent
    schema = json.loads((root / "schemas/feedback-policy.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda item: list(item.path))
    if errors:
        return {"status": "blocked", "codes": ["feedback.schema"], "may_continue": False,
                "publication_allowed": False, "schema_paths": ["/".join(map(str, error.path)) for error in errors]}
    enabled = payload["enabled"]
    sla = payload["sla"]
    effective_sla = {"enabled": enabled, "blocker_days": (sla["blocker_days"] or 1) if enabled else None,
                     "non_blocker_days": (sla["non_blocker_days"] or 3) if enabled else None}
    codes: list[str] = []
    for comment in payload["comments"]:
        disposition = comment["disposition"]
        if comment["severity"] == "blocker" and disposition not in DISPOSITIONS:
            codes.append("feedback.blocker-unresolved")
        if comment["severity"] == "non-blocker" and disposition not in DISPOSITIONS:
            codes.append("feedback.non-blocker-undisposed")
        if disposition in {"accepted", "deferred"} and not comment["follow_up"]:
            codes.append("feedback.follow-up-missing")
    route = payload["core_route"]
    publication_evidence = "required" if route["publication_implemented"] else "not-applicable"
    if not route["publication_implemented"] and route["evidence_claimed"]:
        codes.append("feedback.fabricated-evidence")
    if route["publication_implemented"]:
        codes.append("feedback.future-class-aware-selection-required")
    source = payload["source"]
    source_action = "use-git-openspec-canonical"
    if source["mode"] == "legacy-reference":
        source_action = "rewrite-or-link-through-git-openspec"
        if not source["legacy_corpus_read_only"]:
            codes.append("feedback.legacy-corpus-mutation")
    views = payload["generated_views"]
    if views["selection_owner"] != "corporate-environment" or views["selected"]:
        codes.append("feedback.generated-view-owner")
    result = {
        "status": "passed" if not codes else "blocked", "codes": sorted(set(codes)),
        "may_continue": not codes, "publication_allowed": not codes,
        "sla": effective_sla, "publication_evidence": publication_evidence,
        "source_action": source_action,
        "generated_view_status": "deferred-to-corporate-environment" if not views["selected"] else "invalid-external-selection",
        "canonical_mutated": False, "integration_executed": False,
    }
    return result
