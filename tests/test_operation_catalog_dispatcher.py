"""Focused contracts for the catalog-backed P3 dispatcher."""

from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_catalog_covers_each_script_once_and_rejects_external_mutation() -> None:
    from process.operations_catalog import load_operations_catalog

    catalog = load_operations_catalog(ROOT / "process" / "catalogs" / "operations.yaml")
    assert {item["entrypoint"] for item in catalog["operations"]} == {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "scripts").glob("*.py")
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
    assert sdd_main(["check", "preview-analytics", "--json"]) == 3
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

    assert sdd_main(["check", "preview-analytics", "--json"]) == 3
    captured = capsys.readouterr()
    assert captured.err == ""
    assert [json.loads(line) for line in captured.out.splitlines()] == [
        {
            "diagnostics": [{"code": "operation-failed", "message": "A required local operation failed."}],
            "schema_version": "1.0",
            "status": "operational-error",
        }
    ]


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
    assert sdd_main(["check", "prepare-spec-pr", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-class-not-permitted"
    assert sdd_main(["prepare", "classify-change", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-class-not-permitted"
    assert sdd_main(["run", "create-change", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "confirmation-contract-pending"


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
    assert sdd_main(["check", "preview-analytics", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["evidence"] == {"operation": "preview-analytics"}
    assert sdd_main(["prepare", "prepare-spec-pr", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["evidence"] == {"operation": "prepare-spec-pr"}


def test_request_digest_binds_operation_and_ordered_forwarded_argv(capsys: pytest.CaptureFixture[str]) -> None:
    import json
    from scripts.sdd import main as sdd_main

    assert sdd_main(["request", "create-change", "--", "sample", "--json"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert sdd_main(["request", "create-change", "--", "--json", "sample"]) == 0
    second = json.loads(capsys.readouterr().out)
    assert first["status"] == "confirmation-requested"
    assert first["authority_granted"] is False
    assert first["input_digest"] != second["input_digest"]
    assert sdd_main(["request", "create-change", "--", "sample", "sample", "--json"]) == 0
    duplicate = json.loads(capsys.readouterr().out)
    assert duplicate["input_digest"] != first["input_digest"]


def test_request_blocks_non_mutating_operations_before_side_effect(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    import json
    from scripts.sdd import main as sdd_main

    monkeypatch.setattr("process.operation_dispatcher._run_entrypoint", pytest.fail)
    for operation_id in ("preview-analytics", "prepare-spec-pr"):
        assert sdd_main(["request", operation_id, "--json"]) == 1
        assert json.loads(capsys.readouterr().out)["blockers"][0]["code"] == "operation-not-requestable"
