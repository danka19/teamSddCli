#!/usr/bin/env python3
"""Bounded compatibility wrapper for the packaged Phase 1 validator.

New change creation uses schema-v2 under ``process/templates/change``. This
entry point remains available only for explicit legacy thin/full validation
and migration compatibility.
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from process.validators.legacy_change import *  # noqa: F401,F403
from process.validators.legacy_change import main


if __name__ == "__main__":
    raise SystemExit(main())
