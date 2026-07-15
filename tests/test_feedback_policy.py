from __future__ import annotations

import copy

from process.feedback_policy import evaluate_feedback_policy


def base() -> dict:
    return {
        "schema_version": "1.0", "namespace": "synthetic", "enabled": True,
        "sla": {"blocker_days": None, "non_blocker_days": None}, "comments": [],
        "core_route": {"change_class": "minor", "publication_implemented": False, "evidence_claimed": False},
        "source": {"mode": "git-openspec", "legacy_corpus_read_only": True},
        "generated_views": {"selection_owner": "corporate-environment", "selected": False},
    }


def test_feedback_sla_is_configurable() -> None:
    payload = base(); payload["enabled"] = False
    result = evaluate_feedback_policy(payload)
    assert result["sla"] == {"enabled": False, "blocker_days": None, "non_blocker_days": None}
    payload = base(); payload["sla"] = {"blocker_days": 2, "non_blocker_days": 4}
    assert evaluate_feedback_policy(payload)["sla"]["blocker_days"] == 2


def test_default_triage_sla_is_used_when_enabled() -> None:
    assert evaluate_feedback_policy(base())["sla"] == {"enabled": True, "blocker_days": 1, "non_blocker_days": 3}


def test_blocker_comment_prevents_final_publication() -> None:
    payload = base(); payload["comments"] = [{"id": "synthetic-comment", "severity": "blocker", "disposition": "unresolved", "follow_up": None}]
    result = evaluate_feedback_policy(payload)
    assert result["publication_allowed"] is False
    assert "feedback.blocker-unresolved" in result["codes"]
    for disposition in ("accepted", "rejected", "deferred", "duplicate", "approved-waiver"):
        candidate = copy.deepcopy(payload); candidate["comments"][0]["disposition"] = disposition
        if disposition in {"accepted", "deferred"}: candidate["comments"][0]["follow_up"] = "synthetic-follow-up"
        assert "feedback.blocker-unresolved" not in evaluate_feedback_policy(candidate)["codes"]


def test_non_blocking_comment_still_needs_disposition() -> None:
    payload = base(); payload["comments"] = [{"id": "synthetic-comment", "severity": "non-blocker", "disposition": "deferred", "follow_up": None}]
    assert "feedback.follow-up-missing" in evaluate_feedback_policy(payload)["codes"]
    payload["comments"][0]["follow_up"] = "synthetic-follow-up"
    assert evaluate_feedback_policy(payload)["may_continue"] is True


def test_core_class_routes_do_not_require_fabricated_confluence_evidence() -> None:
    for change_class in ("minor", "major", "hotfix"):
        payload = base(); payload["core_route"]["change_class"] = change_class
        result = evaluate_feedback_policy(payload)
        assert result["may_continue"] is True and result["publication_evidence"] == "not-applicable"
        payload["core_route"]["evidence_claimed"] = True
        assert "feedback.fabricated-evidence" in evaluate_feedback_policy(payload)["codes"]


def test_applicable_publication_becomes_class_aware_later() -> None:
    payload = base(); payload["core_route"]["publication_implemented"] = True
    result = evaluate_feedback_policy(payload)
    assert result["may_continue"] is False
    assert "feedback.future-class-aware-selection-required" in result["codes"]


def test_existing_confluence_corpus_is_read_only_archive() -> None:
    payload = base(); payload["source"] = {"mode": "legacy-reference", "legacy_corpus_read_only": False}
    assert "feedback.legacy-corpus-mutation" in evaluate_feedback_policy(payload)["codes"]
    payload["source"]["legacy_corpus_read_only"] = True
    assert evaluate_feedback_policy(payload)["source_action"] == "rewrite-or-link-through-git-openspec"


def test_generated_views_are_selected_in_corporate_environment() -> None:
    payload = base(); payload["generated_views"] = {"selection_owner": "external-package", "selected": True}
    assert "feedback.generated-view-owner" in evaluate_feedback_policy(payload)["codes"]
    assert evaluate_feedback_policy(base())["generated_view_status"] == "deferred-to-corporate-environment"
