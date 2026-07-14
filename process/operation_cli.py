"""Shared stable output boundary for deterministic workflow entry points."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from .workflow_operations import OperationError


def execute(operation: Callable[[], dict[str, Any]], json_output: bool) -> int:
    try:
        payload = operation()
    except OperationError as error:
        operational = error.exit_code == 3
        payload = {
            "schema_version": "1.0",
            "status": "operational-error" if operational else "error",
            "diagnostics": [{
                "code": error.code,
                "message": "A required local operation failed." if operational else "The operation could not be completed safely.",
            }],
        }
        rendered = "A required local operation failed." if operational else "The operation could not be completed safely."
        print(json.dumps(payload, sort_keys=True) if json_output else f"ERROR [{error.code}] {rendered}")
        return error.exit_code
    except Exception:
        payload = {
            "schema_version": "1.0",
            "status": "operational-error",
            "diagnostics": [{
                "code": "operation-failed",
                "message": "A required local operation failed.",
            }],
        }
        print(json.dumps(payload, sort_keys=True) if json_output else "ERROR [operation-failed] A required local operation failed.")
        return 3
    print(json.dumps(payload, sort_keys=True) if json_output else f"{payload['operation']}: {payload['status']}")
    return 0
