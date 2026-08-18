#!/usr/bin/env python3
"""Validate the public PMM skill inventory and its local dependency closure."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = {
    "pm-prioritizer", "pmm-em-tracker", "pmm-plan-scaffolder", "pmm-plan-auditor",
    "pmm-launch-scaffolder", "daily-starter", "manage-up", "pmm-habits",
    "notes-weekly-team-comms", "status-update", "people-intelligence", "comp-intel",
    "pmm-weekly-impact", "guidance-review", "linkedin-ghostwriter", "marketing-brief",
    "pre-read-sharpener", "product-page-copywriter", "sales-one-pager",
    "strategic-narrative-coach", "meeting-notes-scaffolder", "slack-monitor-scaffolder",
    "weekly-summary-promoter", "git-sweep", "pmm-accepted-plan-importer",
    "pmm-instinct-review",
}
REQUIRED_SHARED = {
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "PRIVACY.md",
    "SECURITY.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "docs/legal/IP-INVENTORY.csv",
    "docs/legal/IP-RIGHTS-REVIEW-2026-08-18.md",
    "docs/legal/scancode-summary-2026-08-18.json",
    "docs/security/SECRET-AUDIT-2026-08-18.md",
    "docs/security/gitleaks-history-2026-08-18.json",
    "docs/security/gitleaks-tracked-tree-2026-08-18.json",
    "docs/STD-evidence-privacy-v1.0.md",
    "docs/STD-approval-gates-v1.0.md",
    "docs/STD-skill-dependencies-v1.0.md",
}
AUDIT_REPORTS = {
    "docs/security/gitleaks-history-2026-08-18.json",
    "docs/security/gitleaks-tracked-tree-2026-08-18.json",
}
IP_INVENTORY = "docs/legal/IP-INVENTORY.csv"
PATH_RE = re.compile(r"`((?:references|assets|scripts|examples|docs)/[^`\s]+)")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BLOCKED = re.compile(
    r"(/Users/|polygon|clickup|@polygon|channel[_ -]?id\s*[:=]\s*[A-Z0-9]|"
    r"api[_ -]?key\s*[:=]|secret\s*[:=]|token\s*[:=])",
    re.IGNORECASE,
)


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError("missing YAML frontmatter")
    raw = text.split("\n---\n", 1)[0][4:]
    keys = re.findall(r"^([a-z_]+):", raw, re.MULTILINE)
    name_match = re.search(r"^name:\s*([^\n]+)$", raw, re.MULTILINE)
    if not name_match:
        raise ValueError("frontmatter needs name")
    if "description" not in keys:
        raise ValueError("frontmatter needs description")
    return {"name": name_match.group(1).strip(), "description": "", "_keys": keys}


def main() -> int:
    errors: list[str] = []
    actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if actual != SKILLS:
        errors.append(f"skill inventory mismatch: missing={sorted(SKILLS-actual)} extra={sorted(actual-SKILLS)}")

    for rel in REQUIRED_SHARED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing shared dependency: {rel}")

    for rel in AUDIT_REPORTS:
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            findings = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid secrets-audit report {rel}: {exc}")
            continue
        if findings != []:
            errors.append(f"secrets-audit report contains findings: {rel}")

    inventory_path = ROOT / IP_INVENTORY
    if inventory_path.is_file():
        with inventory_path.open(encoding="utf-8", newline="") as handle:
            inventory_rows = list(csv.DictReader(handle))
        inventory_files = [row.get("path", "") for row in inventory_rows]
        duplicate_files = sorted({path for path in inventory_files if inventory_files.count(path) > 1})
        public_files = {
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*")
            if path.is_file()
            and not any(part in {".git", ".venv", "__pycache__"} for part in path.relative_to(ROOT).parts)
            and path.suffix != ".pyc"
        }
        if set(inventory_files) != public_files:
            errors.append(
                "IP inventory mismatch: "
                f"missing={sorted(public_files-set(inventory_files))} "
                f"extra={sorted(set(inventory_files)-public_files)}"
            )
        if duplicate_files:
            errors.append(f"IP inventory contains duplicate paths: {duplicate_files}")
        incomplete = [
            row.get("path", "<missing>")
            for row in inventory_rows
            if any(not row.get(field) for field in (
                "path", "artifact_class", "provenance_basis", "third_party_content",
                "redistribution_basis", "disposition",
            )) or row.get("disposition") != "include"
        ]
        if incomplete:
            errors.append(f"IP inventory contains incomplete or excluded rows: {sorted(incomplete)}")

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").is_file() else ""
    if "Apache License" not in license_text or "Version 2.0, January 2004" not in license_text:
        errors.append("LICENSE is not the Apache License 2.0 text")

    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8") if (ROOT / "CONTRIBUTING.md").is_file() else ""
    full_test_command = ".venv/bin/python -m unittest discover -s tests"
    stale_test_command = "python3 -m unittest tests/test_diffguard_lite.py"
    if full_test_command not in contributing:
        errors.append("CONTRIBUTING.md is missing the full test command")
    if stale_test_command in contributing:
        errors.append("CONTRIBUTING.md contains the stale partial test command")

    for name in sorted(SKILLS):
        skill = ROOT / "skills" / name
        skill_md = skill / "SKILL.md"
        try:
            meta = frontmatter(skill_md)
            if set(meta["_keys"]) != {"name", "description"}:
                errors.append(f"{name}: frontmatter keys must be name and description")
            if meta.get("name") != name:
                errors.append(f"{name}: frontmatter name mismatch")
        except (OSError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
            continue

        for rel in ("agents/openai.yaml", "assets/output-template.md", "examples/EX-synthetic.md"):
            if not (skill / rel).is_file():
                errors.append(f"{name}: missing {rel}")
        if not any((skill / "references").glob("RUN*.md")):
            errors.append(f"{name}: missing references/RUN*.md")

        agent_path = skill / "agents" / "openai.yaml"
        if agent_path.is_file():
            agent_text = agent_path.read_text(encoding="utf-8")
            for field in ("display_name", "short_description", "default_prompt"):
                if not re.search(rf"^\s*{field}:\s*\"[^\"]+\"\s*$", agent_text, re.MULTILINE):
                    errors.append(f"{name}: agents/openai.yaml missing quoted {field}")
            if f"${name}" not in agent_text:
                errors.append(f"{name}: default prompt must name ${name}")

        text = skill_md.read_text(encoding="utf-8")
        for target in PATH_RE.findall(text):
            resolved = (ROOT / target) if target.startswith("docs/") else (skill / target)
            if not resolved.exists():
                errors.append(f"{name}: broken dependency `{target}`")

    for path in ROOT.rglob("*"):
        if (not path.is_file() or ".git" in path.parts or ".venv" in path.parts
                or "__pycache__" in path.parts):
            continue
        if path.name in {"validate_skill_pack.py", "test_skill_pack.py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if "TODO:" in text or "example_asset.txt" in text or "api_reference.md" in text:
            errors.append(f"placeholder content: {path.relative_to(ROOT)}")
        match = BLOCKED.search(text)
        if match:
            errors.append(f"public-safety pattern {match.group(0)!r}: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".md":
            for target in MARKDOWN_LINK_RE.findall(text):
                clean_target = target.split("#", 1)[0]
                if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
                    continue
                if not (path.parent / clean_target).resolve().exists():
                    errors.append(
                        f"broken Markdown link {target!r}: {path.relative_to(ROOT)}"
                    )

    if errors:
        print("Skill pack validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(SKILLS)} public skills and their declared dependencies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
