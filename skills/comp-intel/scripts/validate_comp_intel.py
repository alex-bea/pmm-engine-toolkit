#!/usr/bin/env python3
"""Validate bundled contracts and an optional initialized data root."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from comp_intel_core import CompIntelController, WorkflowError


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def validate_schemas() -> list[str]:
    errors: list[str] = []
    schema_root = PACKAGE_ROOT / "assets/schemas"
    for path in sorted(schema_root.glob("*.schema.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if value.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.name}: must declare JSON Schema draft 2020-12")
        if not isinstance(value.get("$id"), str) or not value["$id"].startswith("https://example.invalid/"):
            errors.append(f"{path.name}: must use a reserved public schema identifier")
    if not list(schema_root.glob("*.schema.json")):
        errors.append("no schemas found")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--market")
    parser.add_argument("--run-id")
    arguments = parser.parse_args(argv)
    errors = validate_schemas()
    if arguments.data_root:
        try:
            CompIntelController(arguments.data_root).validate(arguments.run_id, arguments.market)
        except WorkflowError as exc:
            errors.append(str(exc))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Competitive-intelligence contracts are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
