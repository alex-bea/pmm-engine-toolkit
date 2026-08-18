#!/usr/bin/env python3
"""Transform simple headed Markdown notes into a reviewable weekly update."""

from __future__ import annotations

import argparse
from pathlib import Path


SECTIONS = {"shipped": [], "in progress": [], "risks": [], "asks": [], "next": []}


def parse(text: str) -> dict[str, list[str]]:
    result = {key: [] for key in SECTIONS}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#"):
            heading = line.lstrip("#").strip().lower()
            current = heading if heading in result else None
        elif current and line.startswith(("- ", "* ")):
            item = line[2:].strip()
            if item and item not in result[current]:
                result[current].append(item)
    return result


def render(items: dict[str, list[str]]) -> str:
    def bullets(key: str) -> str:
        return "\n".join(f"- {item}" for item in items[key]) or "- None supplied"
    return f"""# Weekly communications

## Manager wrap

### Shipped
{bullets('shipped')}

### In progress
{bullets('in progress')}

### Risks
{bullets('risks')}

### Asks
{bullets('asks')}

## Team update

### Outcomes
{bullets('shipped')}

### Next week
{bullets('next')}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = render(parse(args.input.read_text(encoding="utf-8")))
    if args.output:
        if args.output.exists():
            parser.error(f"refusing to overwrite {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
