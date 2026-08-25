#!/usr/bin/env python3
"""Initialize, audit, and mechanically repair portable Codex skill governance."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PACK_VERSION = "1.0.0"
PACK_SOURCE = "https://github.com/alex-bea/pmm-engine-toolkit"
SKILL_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(".agents/governance/manifest.yaml")
REGISTRY_PATH = Path(".agents/governance/skill-registry.yaml")
VALID_STATUSES = {"draft", "active", "deprecated", "archived"}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

STANDARD_NAMES = (
    "STD-ai-skill-governance-prd-v1.0.md",
    "STD-approval-gates-v1.0.md",
    "STD-evidence-privacy-v1.0.md",
    "STD-governance-document-metadata-v1.0.md",
    "STD-skill-dependencies-v1.0.md",
    "STD-skill-primitives-v1.0.md",
    "STD-skill-structure-v1.0.md",
)


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    path: str
    message: str
    fixable: bool = False


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_confined(repo: Path, target: Path) -> bool:
    try:
        target.resolve(strict=False).relative_to(repo.resolve())
    except ValueError:
        return False
    return True


def read_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise ValueError(
                f"{path}: use JSON-compatible YAML or install PyYAML to read conventional YAML"
            ) from exc
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # type: ignore[attr-defined]
            raise ValueError(f"{path}: invalid YAML: {exc}") from exc


def json_yaml(data: Any) -> str:
    """Return JSON, which is valid YAML 1.2 and needs no runtime dependency."""
    return json.dumps(data, indent=2, sort_keys=False) + "\n"


def source_entries(*, with_ci: bool) -> dict[Path, bytes]:
    entries: dict[Path, bytes] = {}
    for name in STANDARD_NAMES:
        source = SKILL_DIR / "references" / name
        if not source.is_file():
            raise FileNotFoundError(f"governance pack source is missing: {source}")
        entries[Path(".agents/governance/standards") / name] = source.read_bytes()

    copies = {
        Path(".agents/governance/schemas/governance-manifest.schema.json"):
            SKILL_DIR / "assets/schemas/governance-manifest.schema.json",
        Path(".agents/governance/schemas/skill-registry.schema.json"):
            SKILL_DIR / "assets/schemas/skill-registry.schema.json",
        Path(".agents/governance/templates/SKILL.md"):
            SKILL_DIR / "assets/templates/SKILL.md",
        Path(".agents/governance/templates/openai.yaml"):
            SKILL_DIR / "assets/templates/openai.yaml",
        Path(".agents/governance/bin/govern_skills.py"):
            Path(__file__).resolve(),
    }
    if with_ci:
        copies[Path(".github/workflows/skill-governance.yml")] = (
            SKILL_DIR / "assets/templates/skill-governance-ci.yml"
        )
    for target, source in copies.items():
        if not source.is_file():
            raise FileNotFoundError(f"governance pack source is missing: {source}")
        entries[target] = source.read_bytes()
    return entries


def registry_seed() -> bytes:
    return json_yaml({"version": "1.0", "skills": []}).encode()


def manifest_content(repo: Path, entries: dict[Path, bytes]) -> bytes:
    path = repo / MANIFEST_PATH
    if path.exists():
        try:
            manifest = read_structured(path)
        except ValueError:
            manifest = None
    else:
        manifest = None
    if not isinstance(manifest, dict):
        manifest = {
            "schema_version": "1.0",
            "source": PACK_SOURCE,
            "components": {},
        }
    components = manifest.setdefault("components", {})
    if not isinstance(components, dict):
        components = {}
        manifest["components"] = components
    components["skills"] = {
        "version": PACK_VERSION,
        "files": {path.as_posix(): sha256(data) for path, data in sorted(entries.items())},
    }
    manifest["schema_version"] = "1.0"
    manifest["source"] = PACK_SOURCE
    return json_yaml(manifest).encode()


def ci_is_managed(repo: Path) -> bool:
    path = repo / MANIFEST_PATH
    if not path.is_file():
        return False
    try:
        manifest = read_structured(path)
    except ValueError:
        return False
    if not isinstance(manifest, dict):
        return False
    files = manifest.get("components", {}).get("skills", {}).get("files", {})
    return isinstance(files, dict) and ".github/workflows/skill-governance.yml" in files


def planned_writes(repo: Path, *, with_ci: bool) -> dict[Path, bytes]:
    managed = source_entries(with_ci=with_ci or ci_is_managed(repo))
    entries = dict(managed)
    if not (repo / REGISTRY_PATH).exists():
        entries[REGISTRY_PATH] = registry_seed()
    entries[MANIFEST_PATH] = manifest_content(repo, managed)
    return entries


def classify_writes(
    repo: Path, entries: dict[Path, bytes], *, generated_updates: set[Path] | None = None
) -> list[dict[str, str]]:
    generated_updates = generated_updates or set()
    rows: list[dict[str, str]] = []
    for rel, data in sorted(entries.items()):
        target = repo / rel
        if not is_confined(repo, target):
            action = "conflict"
        elif not target.exists():
            action = "create"
        elif target.read_bytes() == data:
            action = "unchanged"
        elif rel in generated_updates:
            action = "update"
        else:
            action = "conflict"
        rows.append({"path": rel.as_posix(), "action": action, "sha256": sha256(data)})
    return rows


def write_entries(
    repo: Path,
    entries: dict[Path, bytes],
    *,
    generated_updates: set[Path] | None = None,
) -> tuple[int, list[dict[str, str]]]:
    rows = classify_writes(repo, entries, generated_updates=generated_updates)
    conflicts = [row for row in rows if row["action"] == "conflict"]
    if conflicts:
        return 2, rows
    for row in rows:
        if row["action"] not in {"create", "update"}:
            continue
        rel = Path(row["path"])
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entries[rel])
    return 0, rows


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["missing YAML frontmatter"]
    marker = text.find("\n---\n", 4)
    if marker < 0:
        return {}, ["unterminated YAML frontmatter"]
    raw = text[4:marker]
    keys = re.findall(r"^([a-zA-Z0-9_-]+):", raw, re.MULTILINE)
    data: dict[str, str] = {"_keys": ",".join(keys)}
    for key in ("name", "description"):
        match = re.search(rf"^{key}:\s*(.*)$", raw, re.MULTILINE)
        if not match:
            errors.append(f"frontmatter needs {key}")
            continue
        value = match.group(1).strip().strip('"\'')
        if value not in {">", "|"} and not value:
            errors.append(f"frontmatter {key} is empty")
        data[key] = value
    return data, errors


def find_skills(repo: Path) -> list[Path]:
    results: list[Path] = []
    for root in (repo / ".agents/skills", repo / "skills"):
        if not root.is_dir() or root.is_symlink() or not is_confined(repo, root):
            continue
        for folder in sorted(root.iterdir()):
            if (
                folder.is_dir()
                and not folder.is_symlink()
                and not folder.name.startswith("_")
                and (folder / "SKILL.md").is_file()
            ):
                results.append(folder)
    return results


def load_registry(repo: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = repo / REGISTRY_PATH
    if not is_confined(repo, path):
        return None, f"{path}: target resolves outside the repository"
    if not path.exists():
        return None, None
    try:
        data = read_structured(path)
    except ValueError as exc:
        return None, str(exc)
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        return None, f"{path}: root must contain a skills list"
    return data, None


def audit(repo: Path) -> list[Finding]:
    findings: list[Finding] = []
    manifest_path = repo / MANIFEST_PATH
    if not is_confined(repo, manifest_path):
        findings.append(Finding(
            "GOV007", "error", MANIFEST_PATH.as_posix(),
            "governance path resolves outside the repository",
        ))
    elif not manifest_path.is_file():
        findings.append(Finding(
            "GOV001", "warning", MANIFEST_PATH.as_posix(),
            "governance pack is not initialized", True,
        ))
    else:
        try:
            manifest = read_structured(manifest_path)
        except ValueError as exc:
            findings.append(Finding("GOV001", "error", MANIFEST_PATH.as_posix(), str(exc)))
            manifest = None
        if isinstance(manifest, dict):
            component = manifest.get("components", {}).get("skills", {})
            files = component.get("files", {}) if isinstance(component, dict) else {}
            if not isinstance(files, dict):
                findings.append(Finding(
                    "GOV001", "error", MANIFEST_PATH.as_posix(),
                    "skills component file map is missing or invalid",
                ))
            else:
                for rel, expected in sorted(files.items()):
                    target = repo / rel
                    if not target.is_file():
                        findings.append(Finding("GOV002", "warning", rel, "managed file is missing", True))
                    elif sha256(target.read_bytes()) != expected:
                        findings.append(Finding(
                            "GOV003", "warning", rel,
                            "managed file differs from the installed governance-pack hash",
                        ))

    registry, registry_error = load_registry(repo)
    if registry_error:
        findings.append(Finding("REG001", "error", REGISTRY_PATH.as_posix(), registry_error))
    elif registry is None:
        findings.append(Finding("REG001", "warning", REGISTRY_PATH.as_posix(), "skill registry is missing", True))
    entries = registry.get("skills", []) if registry else []
    by_name: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str):
            findings.append(Finding("REG002", "error", REGISTRY_PATH.as_posix(), "registry entry needs a string name"))
            continue
        name = entry["name"]
        if name in by_name:
            findings.append(Finding("REG003", "error", REGISTRY_PATH.as_posix(), f"duplicate registry entry: {name}"))
        by_name[name] = entry
        status = entry.get("status")
        if status not in VALID_STATUSES:
            findings.append(Finding("REG004", "error", REGISTRY_PATH.as_posix(), f"{name}: invalid lifecycle status {status!r}"))
        if status == "deprecated" and not entry.get("replacement"):
            findings.append(Finding("REG005", "warning", REGISTRY_PATH.as_posix(), f"{name}: deprecated skill needs a replacement"))
        folder = entry.get("folder")
        if status != "archived" and (not isinstance(folder, str) or not (repo / folder).is_dir()):
            findings.append(Finding("REG006", "warning", REGISTRY_PATH.as_posix(), f"{name}: registered folder is missing"))

    for folder in find_skills(repo):
        rel_folder = folder.relative_to(repo).as_posix()
        name = folder.name
        if len(name) > 64 or not NAME_RE.fullmatch(name):
            findings.append(Finding("SKILL001", "error", rel_folder, "folder name must be lowercase kebab-case and at most 64 characters"))
        meta, errors = parse_frontmatter(folder / "SKILL.md")
        for error in errors:
            findings.append(Finding("SKILL002", "error", f"{rel_folder}/SKILL.md", error))
        keys = set(meta.get("_keys", "").split(",")) - {""}
        if keys and keys != {"name", "description"}:
            findings.append(Finding(
                "SKILL002", "error", f"{rel_folder}/SKILL.md",
                f"frontmatter keys must be name and description; found {sorted(keys)}",
            ))
        if meta.get("name") and meta["name"] != name:
            findings.append(Finding("SKILL001", "error", f"{rel_folder}/SKILL.md", f"frontmatter name must equal folder name {name!r}"))

        agent = folder / "agents/openai.yaml"
        if not agent.is_file():
            findings.append(Finding("SKILL003", "warning", f"{rel_folder}/agents/openai.yaml", "Codex interface metadata is missing", True))
        else:
            agent_text = agent.read_text(encoding="utf-8")
            for field in ("display_name", "short_description", "default_prompt"):
                if not re.search(rf"^\s*{field}:\s*\"[^\"]+\"\s*$", agent_text, re.MULTILINE):
                    findings.append(Finding("SKILL004", "warning", f"{rel_folder}/agents/openai.yaml", f"missing quoted interface.{field}"))
            if f"${name}" not in agent_text:
                findings.append(Finding("SKILL004", "warning", f"{rel_folder}/agents/openai.yaml", f"default prompt must name ${name}"))

        if name not in by_name:
            findings.append(Finding("SKILL005", "warning", rel_folder, "skill is not registered", True))
        elif by_name[name].get("folder") != rel_folder:
            findings.append(Finding("SKILL006", "warning", REGISTRY_PATH.as_posix(), f"{name}: registry folder does not match {rel_folder}"))
    return findings


def render_findings(findings: list[Finding], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"findings": [asdict(item) for item in findings]}, indent=2))
        return
    if not findings:
        print("Skill governance audit passed with no findings.")
        return
    for finding in findings:
        suffix = " [fixable]" if finding.fixable else ""
        print(f"{finding.severity.upper()} {finding.id} {finding.path}: {finding.message}{suffix}")
    print(f"\nAdvisory findings: {len(findings)}")


def generated_openai(name: str) -> bytes:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = f"Run the governed {display} workflow"
    if len(short) < 25:
        short += " safely"
    if len(short) > 64:
        short = short[:64].rstrip()
    return (
        "interface:\n"
        f"  display_name: {json.dumps(display)}\n"
        f"  short_description: {json.dumps(short)}\n"
        f"  default_prompt: {json.dumps(f'Use ${name} to run this governed workflow.')}\n"
    ).encode()


def fix_entries(repo: Path, selected: str | None) -> tuple[dict[Path, bytes], set[Path]]:
    findings = audit(repo)
    if selected:
        findings = [item for item in findings if item.id == selected]
    ids = {item.id for item in findings}
    entries: dict[Path, bytes] = {}
    generated_updates: set[Path] = set()

    restore_pack = bool(ids & {"GOV001", "GOV002"})
    managed_sources = source_entries(with_ci=ci_is_managed(repo)) if restore_pack else {}
    if restore_pack:
        for rel, data in managed_sources.items():
            if not (repo / rel).exists():
                entries[rel] = data

    for finding in findings:
        if finding.id == "SKILL003":
            skill_folder = Path(finding.path).parents[1]
            entries[Path(finding.path)] = generated_openai(skill_folder.name)

    if "REG001" in ids or "SKILL005" in ids:
        registry, error = load_registry(repo)
        if error:
            return entries, generated_updates
        if registry is None:
            registry = {"version": "1.0", "skills": []}
        existing = {item.get("name") for item in registry["skills"] if isinstance(item, dict)}
        for folder in find_skills(repo):
            if folder.name in existing:
                continue
            registry["skills"].append({
                "name": folder.name,
                "folder": folder.relative_to(repo).as_posix(),
                "version": "0.1.0",
                "owner": "unassigned",
                "status": "draft",
                "replacement": None,
            })
        entries[REGISTRY_PATH] = json_yaml(registry).encode()
        generated_updates.add(REGISTRY_PATH)

    if restore_pack:
        entries[MANIFEST_PATH] = manifest_content(repo, managed_sources)
        generated_updates.add(MANIFEST_PATH)
    return entries, generated_updates


def print_plan(rows: list[dict[str, str]], *, applying: bool) -> None:
    mode = "Apply result" if applying else "Dry-run plan"
    print(f"{mode}:")
    if not rows:
        print("- no mechanical changes available")
        return
    for row in rows:
        print(f"- {row['action']}: {row['path']}")


def add_repo_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    audit_parser = commands.add_parser("audit", help="Run a read-only governance audit")
    add_repo_argument(audit_parser)
    audit_parser.add_argument("--format", choices=("text", "json"), default="text")
    audit_parser.add_argument("--strict", action="store_true", help="Return nonzero when findings exist")

    init_parser = commands.add_parser("initialize", help="Plan or install the governance pack")
    add_repo_argument(init_parser)
    init_parser.add_argument("--apply", action="store_true", help="Write the displayed plan")
    init_parser.add_argument("--dry-run", action="store_true", help="Explicitly select the default no-write mode")
    init_parser.add_argument("--with-ci", action="store_true", help="Install blocking CI as an explicit opt-in")

    fix_parser = commands.add_parser("fix", help="Plan or apply safe mechanical fixes")
    add_repo_argument(fix_parser)
    fix_parser.add_argument("--apply", action="store_true", help="Write the displayed plan")
    fix_parser.add_argument("--dry-run", action="store_true", help="Explicitly select the default no-write mode")
    fix_parser.add_argument("--finding", help="Limit fixes to one finding ID")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo.resolve()
    if not repo.is_dir():
        print(f"ERROR: repository root does not exist: {repo}", file=sys.stderr)
        return 2

    if args.command == "audit":
        findings = audit(repo)
        render_findings(findings, args.format)
        return 1 if args.strict and findings else 0

    if args.command == "initialize":
        try:
            entries = planned_writes(repo, with_ci=args.with_ci)
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        generated = {MANIFEST_PATH}
    else:
        entries, generated = fix_entries(repo, args.finding)

    if args.apply:
        status, rows = write_entries(repo, entries, generated_updates=generated)
    else:
        rows = classify_writes(repo, entries, generated_updates=generated)
        status = 0
    print_plan(rows, applying=args.apply)
    if any(row["action"] == "conflict" for row in rows):
        print("Conflicts were not overwritten. Review the differing files manually.", file=sys.stderr)
        return 2 if args.apply else 0
    return status


if __name__ == "__main__":
    raise SystemExit(main())
