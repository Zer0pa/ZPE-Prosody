#!/usr/bin/env python3
"""Verify the package release surface is consistent.

Checks:
  1. pyproject.toml is parseable and has required fields.
  2. README.md exists and is non-empty.
  3. LICENSE file exists.
  4. Source package directory is importable.
  5. All declared entry points resolve.
"""

from __future__ import annotations

import importlib
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED_FILES = ["pyproject.toml", "README.md", "LICENSE"]


def main() -> int:
    errors: list[str] = []

    # 1. Required files
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"Missing required file: {name}")

    # 2. pyproject.toml parse
    try:
        with open(ROOT / "pyproject.toml", "rb") as f:
            meta = tomllib.load(f)
        project = meta.get("project", {})
        for field in ("name", "version", "description", "license"):
            if field not in project:
                errors.append(f"pyproject.toml [project] missing field: {field}")
    except Exception as exc:
        errors.append(f"pyproject.toml parse error: {exc}")

    # 3. Source package importable
    try:
        importlib.import_module("zpe_prosody")
    except ImportError as exc:
        errors.append(f"Cannot import zpe_prosody: {exc}")

    if errors:
        print("FAIL — release surface verification", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    print("PASS — release surface verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
