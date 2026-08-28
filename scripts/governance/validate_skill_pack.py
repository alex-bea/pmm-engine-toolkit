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
}
PLUGIN_NAME = "pmm-instinct-review"
PLUGIN = ROOT / "plugins" / PLUGIN_NAME
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
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/dependency-review.yml",
    "config/github-security-controls.json",
    "docs/CI.md",
    "docs/ci/CI-HARDENING-2026-08-18.md",
    "docs/legal/IP-INVENTORY.csv",
    "docs/legal/IP-RIGHTS-REVIEW-2026-08-18.md",
    "docs/legal/scancode-summary-2026-08-18.json",
    "docs/security/SECRET-AUDIT-2026-08-18.md",
    "docs/security/GITHUB-SECURITY-CONTROLS.md",
    "docs/security/gitleaks-history-2026-08-18.json",
    "docs/security/gitleaks-tracked-tree-2026-08-18.json",
    "docs/security/SECRET-AUDIT-2026-08-25.md",
    "docs/security/gitleaks-all-refs-2026-08-25.json",
    "docs/security/gitleaks-tracked-tree-2026-08-25.json",
    "docs/legal/IP-RIGHTS-REVIEW-2026-08-25.md",
    "docs/STD-evidence-privacy-v1.0.md",
    "docs/STD-approval-gates-v1.0.md",
    "docs/STD-skill-dependencies-v1.0.md",
    "docs/STD-governance-document-metadata-v1.0.md",
    "docs/CODEX-GOVERNANCE-PLUGIN.md",
    "docs/CODEX-DOCUMENT-GOVERNANCE.md",
    ".agents/plugins/marketplace.json",
    "plugins/skill-governance/.codex-plugin/plugin.json",
    "requirements-build.lock",
    "requirements-build.txt",
    "requirements.lock",
    "scripts/governance/configure_github_security.py",
}
AUDIT_REPORTS = {
    "docs/security/gitleaks-history-2026-08-18.json",
    "docs/security/gitleaks-tracked-tree-2026-08-18.json",
    "docs/security/gitleaks-all-refs-2026-08-25.json",
    "docs/security/gitleaks-tracked-tree-2026-08-25.json",
}
IP_INVENTORY = "docs/legal/IP-INVENTORY.csv"
PATH_RE = re.compile(r"`((?:references|assets|scripts|examples|docs)/[^`\s]+)")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BLOCKED = re.compile(
    r"(/Users/|polygon|clickup|@polygon|channel[_ -]?id\s*[:=]\s*[A-Z0-9]|"
    r"api[_ -]?key\s*[:=]|secret\s*[:=]|token\s*[:=])",
    re.IGNORECASE,
)

PLUGIN_ROOT = ROOT / "plugins" / "skill-governance"
PLUGIN_SKILLS = {"govern-documents", "govern-skills", "govern-work-tracker"}
STANDARD_MIRRORS = {
    "govern-skills": (
        "STD-ai-skill-governance-prd-v1.0.md",
        "STD-approval-gates-v1.0.md",
        "STD-evidence-privacy-v1.0.md",
        "STD-governance-document-metadata-v1.0.md",
        "STD-skill-dependencies-v1.0.md",
        "STD-skill-primitives-v1.0.md",
        "STD-skill-structure-v1.0.md",
    ),
    "govern-work-tracker": (
        "STD-approval-gates-v1.0.md",
        "STD-work-tracker-v1.0.md",
    ),
    "govern-documents": (
        "STD-approval-gates-v1.0.md",
        "STD-evidence-privacy-v1.0.md",
        "STD-governance-document-metadata-v1.0.md",
    ),
}


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


def validate_governance_plugin(errors: list[str]) -> None:
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid governance plugin manifest: {exc}")
        return
    if manifest.get("name") != "skill-governance":
        errors.append("governance plugin manifest name mismatch")
    if manifest.get("version") != "0.2.0":
        errors.append("governance plugin manifest version must be 0.2.0")
    if manifest.get("skills") != "./skills/":
        errors.append("governance plugin must declare ./skills/")
    if "apps" in manifest or "mcpServers" in manifest or "hooks" in manifest:
        errors.append("governance plugin declares an unsupported or unimplemented component")

    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid governance marketplace: {exc}")
        marketplace = {}
    if marketplace.get("name") != "pmm-engine-toolkit":
        errors.append("marketplace name must be pmm-engine-toolkit")
    entries = marketplace.get("plugins", [])
    plugin_entry = next(
        (entry for entry in entries if isinstance(entry, dict) and entry.get("name") == "skill-governance"),
        None,
    )
    if plugin_entry is None:
        errors.append("marketplace is missing skill-governance")
    else:
        if plugin_entry.get("source") != {"source": "local", "path": "./plugins/skill-governance"}:
            errors.append("marketplace skill-governance source mismatch")
        if plugin_entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
            errors.append("marketplace skill-governance policy mismatch")

    skill_root = PLUGIN_ROOT / "skills"
    actual = {path.name for path in skill_root.iterdir() if path.is_dir()}
    if actual != PLUGIN_SKILLS:
        errors.append(
            f"governance plugin skill inventory mismatch: "
            f"missing={sorted(PLUGIN_SKILLS-actual)} extra={sorted(actual-PLUGIN_SKILLS)}"
        )
    required_by_skill = {
        "govern-skills": (
            "agents/openai.yaml",
            "scripts/govern_skills.py",
            "assets/schemas/governance-manifest.schema.json",
            "assets/schemas/skill-registry.schema.json",
            "assets/templates/SKILL.md",
            "assets/templates/openai.yaml",
            "assets/templates/skill-registry.yaml",
            "assets/templates/skill-governance-ci.yml",
            "assets/examples/pmm-engine/EX-pmm-engine-skill-governance.md",
        ),
        "govern-work-tracker": (
            "agents/openai.yaml",
            "scripts/govern_work_tracker.py",
            "assets/schemas/roadmap.schema.json",
            "assets/schemas/epic.schema.json",
            "assets/schemas/task.schema.json",
            "assets/templates/roadmap.yaml",
            "assets/templates/epic.yaml",
            "assets/templates/task.yaml",
            "assets/examples/pmm-engine/EX-pmm-engine-work-tracker.md",
        ),
        "govern-documents": (
            "agents/openai.yaml",
            "scripts/govern_documents.py",
            "assets/templates/governed-document.md",
            "references/RUN-document-governance-audit-v1.0.md",
        ),
    }
    for name in sorted(PLUGIN_SKILLS):
        skill = skill_root / name
        skill_md = skill / "SKILL.md"
        try:
            meta = frontmatter(skill_md)
            if set(meta["_keys"]) != {"name", "description"}:
                errors.append(f"plugin {name}: frontmatter keys must be name and description")
            if meta.get("name") != name:
                errors.append(f"plugin {name}: frontmatter name mismatch")
        except (OSError, ValueError) as exc:
            errors.append(f"plugin {name}: {exc}")
            continue
        for rel in required_by_skill[name]:
            resource = skill / rel
            if not resource.is_file():
                errors.append(f"plugin {name}: missing {rel}")
            elif resource.suffix == ".json":
                try:
                    json.loads(resource.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    errors.append(f"plugin {name}: invalid JSON in {rel}: {exc}")
        agent_text = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
        for field in ("display_name", "short_description", "default_prompt"):
            if not re.search(rf"^\s*{field}:\s*\"[^\"]+\"\s*$", agent_text, re.MULTILINE):
                errors.append(f"plugin {name}: agents/openai.yaml missing quoted {field}")
        if f"${name}" not in agent_text:
            errors.append(f"plugin {name}: default prompt must name ${name}")
        text = skill_md.read_text(encoding="utf-8")
        for target in PATH_RE.findall(text):
            if not (skill / target).exists():
                errors.append(f"plugin {name}: broken dependency `{target}`")
        for standard in STANDARD_MIRRORS[name]:
            canonical = ROOT / "docs" / standard
            mirror = skill / "references" / standard
            if not mirror.is_file():
                errors.append(f"plugin {name}: missing standard mirror {standard}")
            elif canonical.read_bytes() != mirror.read_bytes():
                errors.append(f"plugin {name}: standard mirror drift {standard}")

    canonical_template = ROOT / "docs/templates/DOC-skill-md-template-v1.0.md"
    plugin_template = skill_root / "govern-skills/assets/templates/SKILL.md"
    if canonical_template.read_bytes() != plugin_template.read_bytes():
        errors.append("plugin govern-skills: SKILL.md template drift")


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

    validate_governance_plugin(errors)

    manifest_path = PLUGIN / ".codex-plugin" / "plugin.json"
    hooks_path = PLUGIN / "hooks" / "hooks.json"
    plugin_skill = PLUGIN / "skills" / PLUGIN_NAME
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("name") != PLUGIN_NAME or manifest.get("version") != "0.1.0":
            errors.append("instinct-review plugin manifest name/version mismatch")
        if manifest.get("skills") != "./skills/":
            errors.append("instinct-review plugin must declare bundled skills")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid instinct-review plugin manifest: {exc}")

    try:
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        entries = [item for item in marketplace.get("plugins", []) if item.get("name") == PLUGIN_NAME]
        if len(entries) != 1 or entries[0].get("category") != "Productivity":
            errors.append("marketplace must contain one Productivity instinct-review plugin")
        if entries and entries[0].get("source", {}).get("path") != f"./plugins/{PLUGIN_NAME}":
            errors.append("marketplace instinct-review source path mismatch")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid plugin marketplace: {exc}")

    try:
        hooks = json.loads(hooks_path.read_text(encoding="utf-8")).get("hooks", {})
        if set(hooks) != {"SessionStart", "SessionEnd"}:
            errors.append("instinct-review plugin must declare SessionStart and SessionEnd hooks")
        commands = [hook.get("command", "") for groups in hooks.values() for group in groups for hook in group.get("hooks", [])]
        if not commands or any("${PLUGIN_ROOT}" not in command for command in commands):
            errors.append("instinct-review hooks must resolve commands through ${PLUGIN_ROOT}")
        if any("hooks.json" in command for command in commands):
            errors.append("instinct-review hooks must not modify user hook configuration")
    except (OSError, json.JSONDecodeError, AttributeError) as exc:
        errors.append(f"invalid instinct-review plugin hooks: {exc}")

    try:
        meta = frontmatter(plugin_skill / "SKILL.md")
        if set(meta["_keys"]) != {"name", "description"} or meta.get("name") != PLUGIN_NAME:
            errors.append("bundled instinct-review skill frontmatter mismatch")
    except (OSError, ValueError) as exc:
        errors.append(f"bundled instinct-review skill: {exc}")
    for rel in (
        "agents/openai.yaml", "references/RUN-workflow.md", "assets/output-template.md",
        "assets/extractor-prompt.md", "assets/extractor-schema.json", "examples/EX-synthetic.md",
        "scripts/instinct_review.py", "scripts/pmm_instinct/runtime.py",
    ):
        if not (plugin_skill / rel).is_file():
            errors.append(f"bundled instinct-review skill missing {rel}")
    plugin_python = "\n".join(path.read_text(encoding="utf-8") for path in plugin_skill.rglob("*.py"))
    for forbidden in ("import yaml", "from yaml", "capability-registry", ".venv", ".claude", "/Users/"):
        if forbidden in plugin_python:
            errors.append(f"instinct-review runtime contains forbidden dependency/path: {forbidden}")

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
    print(f"Validated {len(SKILLS)} public standalone skills, two plugins, and their declared dependencies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
