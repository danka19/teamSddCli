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
