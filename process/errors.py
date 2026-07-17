"""Stable public errors shared by deterministic process operations."""

from __future__ import annotations


class OperationError(ValueError):
    """Stable operator-safe error with a public code and CLI exit status."""

    def __init__(self, code: str, message: str, *, exit_code: int = 1) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.exit_code = exit_code
