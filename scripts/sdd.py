#!/usr/bin/env python3
"""Portable entry point for the local P3 dispatcher."""
from pathlib import Path
import sys
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from process.operation_dispatcher import main
if __name__ == "__main__":
    raise SystemExit(main())
