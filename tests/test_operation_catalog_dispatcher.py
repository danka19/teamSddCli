"""Focused contracts for the catalog-backed P3 dispatcher."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_covers_each_script_once_and_rejects_external_mutation() -> None:
    from process.operations_catalog import load_operations_catalog

    catalog = load_operations_catalog(ROOT / "process" / "catalogs" / "operations.yaml")
    assert {item["entrypoint"] for item in catalog["operations"]} == {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*.py") if path.name != "__init__.py"
    }
    assert all(item["mutation_level"] != "mutate_external" for item in catalog["operations"])


def test_release_allowlist_covers_every_catalog_entrypoint() -> None:
    import yaml
    from process.operations_catalog import load_operations_catalog

    catalog = load_operations_catalog(ROOT / "process" / "catalogs" / "operations.yaml")
    allowlist = yaml.safe_load((ROOT / "process" / "release-allowlist.yaml").read_text(encoding="utf-8"))

    assert allowlist["entry_points"] == [
        {"name": Path(item["entrypoint"]).name, **{key: value for key, value in item.items() if key != "entrypoint"}}
        for item in catalog["release_entrypoints"]
    ]


def test_release_allowlist_schema_has_the_catalog_derived_exact_contract() -> None:
    import yaml
    from process.operations_catalog import load_operations_catalog

    catalog = load_operations_catalog(ROOT / "process" / "catalogs" / "operations.yaml")
    schema = json.loads((ROOT / "process" / "schemas" / "release-allowlist.schema.json").read_text(encoding="utf-8"))

    assert schema["properties"]["entry_points"]["const"] == [
        {"name": Path(item["entrypoint"]).name, **{key: value for key, value in item.items() if key != "entrypoint"}}
        for item in catalog["release_entrypoints"]
    ]


def test_dispatcher_blocks_mutation_before_entrypoint_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    from process.operation_dispatcher import main

    called = False

    def unexpected(*_args: object, **_kwargs: object) -> object:
        nonlocal called
        called = True
        raise AssertionError("entrypoint must not execute")

    monkeypatch.setattr("process.operation_dispatcher.subprocess.run", unexpected)
    assert main(["run", "create-change", "--role", "Developer", "--json"]) == 1
    assert not called


def test_dedicated_dispatcher_core_is_the_script_boundary() -> None:
    from process.operation_dispatcher import build_parser

    parser = build_parser()
    parsed = parser.parse_args(["op", "list", "--json"])

    assert parsed.command == "op"


def test_dispatcher_returns_stable_operational_json_for_catalog_and_spawn_failures(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json
    from process.errors import OperationError
    from scripts.sdd import main as sdd_main

    monkeypatch.setattr(
        "process.operation_dispatcher.load_operations_catalog",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OperationError("operations-catalog-invalid", "unavailable", exit_code=3)),
    )
    assert sdd_main(["op", "list", "--json"]) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "operational-error"

    monkeypatch.undo()
    monkeypatch.setattr(
        "process.operation_dispatcher.subprocess.run",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("spawn failed")),
    )
    assert sdd_main(["check", "preview-analytics", "--role", "Analyst", "--json"]) == 3
    assert json.loads(capsys.readouterr().out)["status"] == "operational-error"


def test_dispatcher_renders_operational_json_when_child_output_decode_fails(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json
    from scripts.sdd import main as sdd_main

    monkeypatch.setattr(
        "process.operation_dispatcher.subprocess.run",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")
        ),
    )

    assert sdd_main(["check", "preview-analytics", "--role", "Analyst", "--json"]) == 3
    captured = capsys.readouterr()
    assert captured.err == ""
    assert [json.loads(line) for line in captured.out.splitlines()] == [
        {
            "diagnostics": [{"code": "operation-failed", "message": "A required local operation failed."}],
            "schema_version": "1.0",
            "status": "operational-error",
        }
    ]


def test_dispatcher_does_not_swallow_sibling_unicode_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from process import operation_dispatcher

    monkeypatch.setattr(
        operation_dispatcher,
        "dispatch",
        lambda _args: (_ for _ in ()).throw(
            UnicodeEncodeError("utf-8", "a", 0, 1, "synthetic encode failure")
        ),
    )

    with pytest.raises(UnicodeEncodeError):
        operation_dispatcher.main(["op", "list", "--json"])


def test_dispatcher_discovery_and_safe_execution_boundaries(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    import json
    from process import operation_dispatcher
    from scripts.sdd import main as sdd_main

    assert sdd_main(["op", "list", "--json"]) == 0
    public = json.loads(capsys.readouterr().out)
    assert public["operation"] == "sdd-op-list"
    assert all(item["visibility"] == "public" for item in public["operations"])

    assert sdd_main(["guide", "new-requirement", "--fact", "human_role=Analyst", "--fact", "classification=minor", "--json"]) == 0
    guided = json.loads(capsys.readouterr().out)
    assert guided["commands"] == ["create-change", "classify-change"]
    assert guided["human_decision"]["id"] == "classification-confirmation"

    assert sdd_main(["guide", "new-requirement", "--fact", "human_role=Analyst", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "missing-context"

    monkeypatch.setattr(operation_dispatcher, "_run_entrypoint", pytest.fail)
    assert sdd_main(["check", "prepare-spec-pr", "--role", "Analyst", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-class-not-permitted"
    assert sdd_main(["prepare", "classify-change", "--role", "Analyst", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-class-not-permitted"
    assert sdd_main(["run", "create-change", "--role", "Analyst", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "confirmation-contract-pending"


@pytest.mark.parametrize(
    ("args", "expected_route"),
    [
        (["guide", "new-requirement", "--role", "Analyst", "--fact", "classification=minor", "--json"], "new-requirement"),
        (["guide", "existing-change", "--role", "Analyst", "--fact", "change_id=sample-minor-001", "--fact", "lifecycle_state=draft", "--json"], "existing-change"),
        (["guide", "urgent-incident", "--role", "Tech Lead", "--fact", "incident_ref=evidence/INC-001.md", "--json"], "urgent-incident"),
        (["guide", "blocked-operation", "--role", "Tech Lead", "--fact", "failed_run_ref=evidence/failed-run-001.json", "--json"], "blocked-operation"),
    ],
)
def test_guide_accepts_role_after_situation_for_each_documented_route(
    args: list[str], expected_route: str, capsys: pytest.CaptureFixture[str],
) -> None:
    from scripts.sdd import main as sdd_main

    assert sdd_main(args) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "guided"
    assert payload["route_id"] == expected_route


def test_guide_rejects_conflicting_explicit_and_fact_roles(capsys: pytest.CaptureFixture[str]) -> None:
    from scripts.sdd import main as sdd_main

    assert sdd_main([
        "guide", "new-requirement", "--role", "Analyst", "--fact", "human_role=Tech Lead", "--fact", "classification=minor", "--json",
    ]) == 1

    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "invalid-context"


def test_dispatcher_next_and_operation_show_use_role_and_return_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json
    from process import operation_dispatcher
    from scripts.sdd import main as sdd_main

    change = tmp_path / "change.yaml"
    change.write_text("lifecycle_state: approved\n", encoding="utf-8")
    assert sdd_main(["next", "--change", str(change), "--role", "Tech Lead", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["cta"] == "monitor-process-status"
    assert sdd_main(["next", "--change", str(change), "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "unknown-role"

    assert sdd_main(["op", "show", "preview-analytics", "--role", "Analyst", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["operation_id"] == "preview-analytics"
    assert sdd_main(["op", "show", "preview-analytics", "--role", "Unknown", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "role-not-permitted"

    monkeypatch.setattr(operation_dispatcher, "_run_entrypoint", lambda item, args: {"status": "ok", "evidence": {"operation": item["id"]}, "diagnostics": [], "child_exit_code": 0})
    assert sdd_main(["check", "preview-analytics", "--role", "Analyst", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["evidence"] == {"operation": "preview-analytics"}
    assert sdd_main(["prepare", "prepare-spec-pr", "--role", "Analyst", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["evidence"] == {"operation": "prepare-spec-pr"}


def test_request_digest_binds_operation_and_ordered_forwarded_argv(capsys: pytest.CaptureFixture[str]) -> None:
    import json
    from scripts.sdd import main as sdd_main

    assert sdd_main(["request", "create-change", "--role", "Analyst", "--", "sample", "--json"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert sdd_main(["request", "create-change", "--role", "Analyst", "--", "--json", "sample"]) == 0
    second = json.loads(capsys.readouterr().out)
    assert first["status"] == "confirmation-requested"
    assert first["authority_granted"] is False
    assert first["trusted_event_metadata_required"] is True
    assert "record_type" not in first
    assert "source_chat_event_ref" not in first
    assert first["input_digest"] != second["input_digest"]
    assert sdd_main(["request", "create-change", "--role", "Analyst", "--", "sample", "sample", "--json"]) == 0
    duplicate = json.loads(capsys.readouterr().out)
    assert duplicate["input_digest"] != first["input_digest"]


def test_request_never_fabricates_trusted_ingress_evidence(capsys: pytest.CaptureFixture[str]) -> None:
    from scripts.sdd import main as sdd_main

    assert sdd_main(["request", "create-change", "--role", "Analyst", "--json"]) == 0

    request = json.loads(capsys.readouterr().out)
    assert request["status"] == "confirmation-requested"
    assert request["authority_granted"] is False
    assert request["trusted_event_metadata_required"] is True
    assert {"source_chat_event_ref", "card_chat_event_ref", "trusted_chat_event_ref"}.isdisjoint(request)


def test_operation_confirmation_contract_binds_catalog_role_input_revision_chain_and_expiry() -> None:
    from process.guided_workflow import (
        build_operation_confirmation_request,
        confirm_operation_confirmation_request,
        validate_operation_confirmation_event,
    )

    source = {
        "event_ref": "chat://trusted/source", "actor_type": "human", "sequence": 20,
        "timestamp": "2026-07-23T10:00:00Z", "message": "Запросить создание изменения",
    }
    card = {
        "event_ref": "chat://trusted/card", "actor_type": "assistant", "sequence": 21,
        "previous_event_ref": "chat://trusted/source", "timestamp": "2026-07-23T10:01:00Z",
    }
    request = build_operation_confirmation_request(
        human_role="Analyst", operation_id="create-change", forwarded_argv=["sample", "--json"],
        source_event=source, card_event=card, expires_at="2026-07-23T11:00:00Z",
    )
    event = confirm_operation_confirmation_request(request, {
        "event_ref": "chat://trusted/confirmation", "actor_type": "human", "sequence": 22,
        "previous_event_ref": "chat://trusted/card", "timestamp": "2026-07-23T10:02:00Z",
        "message": f"Подтверждаю {request['card_code']}",
    })

    assert event is not None
    from jsonschema import Draft202012Validator, FormatChecker
    request_schema = json.loads((ROOT / "process" / "schemas" / "operation-confirmation-request.schema.json").read_text(encoding="utf-8"))
    event_schema = json.loads((ROOT / "process" / "schemas" / "operation-confirmation-event.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(request_schema, format_checker=FormatChecker()).iter_errors(request)) == []
    assert list(Draft202012Validator(event_schema, format_checker=FormatChecker()).iter_errors(event)) == []
    assert not validate_operation_confirmation_event(event, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert validate_operation_confirmation_event(event, forwarded_argv=["sample", "--json"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({key: value for key, value in event.items() if key != "human_role"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "human_role": "Unknown"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "operation_id": "preview-analytics"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "input_digest": "f" * 64}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "revision_digest": "f" * 64}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event(event, forwarded_argv=["changed"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event(event, forwarded_argv=["sample"], now="2026-07-23T11:00:00Z")
    assert not validate_operation_confirmation_event({**event, "source_event_timestamp": "2026-07-23T10:04:00Z"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "issued_at": "2026-07-23T10:04:00Z"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "confirmed_at": "2026-07-23T10:04:00Z"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")
    assert not validate_operation_confirmation_event({**event, "unexpected": "field"}, forwarded_argv=["sample"], now="2026-07-23T10:03:00Z")


def test_valid_operation_event_never_enables_run_or_external_mutation(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    import copy
    import yaml
    from process.errors import OperationError
    from process.guided_workflow import (
        build_operation_confirmation_request,
        confirm_operation_confirmation_request,
        validate_operation_confirmation_event,
    )
    from process.operations_catalog import load_operations_catalog
    from scripts.sdd import main as sdd_main

    request = build_operation_confirmation_request(
        human_role="Analyst",
        operation_id="create-change",
        forwarded_argv=[],
        source_event={"event_ref": "chat://trusted/source", "actor_type": "human", "sequence": 1, "timestamp": "2026-07-23T10:00:00Z", "message": "Request"},
        card_event={"event_ref": "chat://trusted/card", "actor_type": "assistant", "sequence": 2, "previous_event_ref": "chat://trusted/source", "timestamp": "2026-07-23T10:01:00Z"},
        expires_at="2026-07-23T11:00:00Z",
    )
    event = confirm_operation_confirmation_request(request, {"event_ref": "chat://trusted/confirmation", "actor_type": "human", "sequence": 3, "previous_event_ref": "chat://trusted/card", "timestamp": "2026-07-23T10:02:00Z", "message": f"\u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e {request['card_code']}"})
    assert event is not None
    assert validate_operation_confirmation_event(event, forwarded_argv=[], now="2026-07-23T10:03:00Z")
    event_path = tmp_path / "operation-confirmation-event.json"
    event_path.write_text(json.dumps(event), encoding="utf-8")
    monkeypatch.setattr("process.operation_dispatcher._run_entrypoint", pytest.fail)
    monkeypatch.setattr("process.operation_dispatcher._utc_now", lambda: "2026-07-23T10:03:00Z")
    assert sdd_main(["run", "create-change", "--role", "Analyst", "--confirmation-event", str(event_path), "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "confirmation-contract-pending"
    event["human_role"] = "Developer"
    event_path.write_text(json.dumps(event), encoding="utf-8")
    assert sdd_main(["run", "create-change", "--role", "Analyst", "--confirmation-event", str(event_path), "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-confirmation-invalid"

    catalog_path = ROOT / "process" / "catalogs" / "operations.yaml"
    external_catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    external_catalog = copy.deepcopy(external_catalog)
    external_catalog["operations"][0]["mutation_level"] = "mutate_external"
    candidate = tmp_path / "operations.yaml"
    candidate.write_text(yaml.safe_dump(external_catalog, allow_unicode=True, sort_keys=False), encoding="utf-8")
    with pytest.raises(OperationError, match="external mutation"):
        load_operations_catalog(candidate)


def test_request_blocks_non_mutating_operations_before_side_effect(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json
    from scripts.sdd import main as sdd_main

    monkeypatch.setattr("process.operation_dispatcher._run_entrypoint", pytest.fail)
    for operation_id in ("preview-analytics", "prepare-spec-pr"):
        assert sdd_main(["request", operation_id, "--role", "Analyst", "--json"]) == 1
        assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-not-requestable"


def test_catalog_validator_checks_derived_contracts_and_generated_readme(tmp_path: Path) -> None:
    """The release/readme views are derived from the catalog, never a second policy."""
    from process.operations_catalog import generate_operation_table, validate_operations_catalog

    errors = validate_operations_catalog(ROOT)
    assert errors == []
    assert "| Operation | Role | Situation | Boundary | Runbook |" in generate_operation_table(ROOT)


def test_execution_requires_an_explicit_permitted_role(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    from scripts.sdd import main as sdd_main

    assert sdd_main(["check", "preview-analytics", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "role-required"
    monkeypatch.setattr("process.operation_dispatcher._run_entrypoint", lambda *_: {"status": "ok", "evidence": {}, "diagnostics": [], "child_exit_code": 0})
    assert sdd_main(["prepare", "prepare-spec-pr", "--role", "Analyst", "--json"]) == 0


def test_dispatcher_parser_errors_are_structured_json(capsys: pytest.CaptureFixture[str]) -> None:
    from scripts.sdd import main as sdd_main

    assert sdd_main(["check", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["diagnostics"][0]["code"] == "invalid-command"
