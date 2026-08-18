#!/usr/bin/env python3
"""Build the complete public-artifact IP disposition inventory."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs" / "legal" / "IP-INVENTORY.csv"
EXCLUDED_PARTS = {".git", ".venv", "__pycache__"}
BRAND_RE = re.compile(
    r"\b(?:Git|GitHub|OpenAI|LinkedIn|Slack|PyYAML|Radon|cognitive[-_]complexity)\b",
    re.IGNORECASE,
)
URL_RE = re.compile(r"https?://")
FIELDS = (
    "path",
    "artifact_class",
    "provenance_basis",
    "third_party_content",
    "redistribution_basis",
    "disposition",
)


def public_paths() -> list[Path]:
    paths = {
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
        and path.suffix != ".pyc"
    }
    paths.add(INVENTORY)
    return sorted(paths, key=lambda path: path.relative_to(ROOT).as_posix())


def readable_text(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def classify(path: Path) -> dict[str, str]:
    rel = path.relative_to(ROOT).as_posix()
    text = readable_text(path)

    if rel == "LICENSE":
        return {
            "path": rel,
            "artifact_class": "external-standard-license-text",
            "provenance_basis": "Official Apache Software Foundation Apache License 2.0 text.",
            "third_party_content": "Apache License 2.0 standard text.",
            "redistribution_basis": "Included verbatim as the project's licensing instrument.",
            "disposition": "include",
        }

    if rel == "requirements.txt":
        return {
            "path": rel,
            "artifact_class": "dependency-manifest",
            "provenance_basis": "Project-authored dependency declaration.",
            "third_party_content": "Nominative package names and version constraints; no vendored code.",
            "redistribution_basis": "Manifest is project-authored; packages retain upstream license terms.",
            "disposition": "include",
        }

    if rel == INVENTORY.relative_to(ROOT).as_posix():
        artifact_class = "generated-legal-inventory"
        provenance = "Generated locally by scripts/governance/build_ip_inventory.py."
    elif rel.startswith("docs/security/") and path.suffix == ".json":
        artifact_class = "generated-security-evidence"
        provenance = "Generated locally by Gitleaks; zero-finding factual report."
    elif path.suffix in {".py", ".js"}:
        artifact_class = "project-authored-source-or-test"
        provenance = "Project-authored source or test committed in the fresh public history."
    elif path.suffix in {".yaml", ".yml"} or path.name == ".gitignore":
        artifact_class = "project-authored-configuration"
        provenance = "Project-authored configuration committed in the fresh public history."
    else:
        artifact_class = "project-authored-documentation-or-template"
        provenance = "Project-authored documentation or template committed in the fresh public history."

    references: list[str] = []
    if BRAND_RE.search(text):
        references.append("nominative product, service, or package references")
    if URL_RE.search(text):
        references.append("external hyperlinks only")

    return {
        "path": rel,
        "artifact_class": artifact_class,
        "provenance_basis": provenance,
        "third_party_content": "; ".join(references) if references else "none detected",
        "redistribution_basis": "Repository copyright holder's original contribution under Apache-2.0.",
        "disposition": "include",
    }


def main() -> int:
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    rows = [classify(path) for path in public_paths()]
    with INVENTORY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {INVENTORY.relative_to(ROOT)} with {len(rows)} artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
