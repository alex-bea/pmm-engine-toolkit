#!/usr/bin/env python3
"""Initialize, audit, and mechanically repair a lightweight repository work tracker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


PACK_VERSION = "1.0.0"
PACK_SOURCE = "https://github.com/alex-bea/pmm-engine-toolkit"
SKILL_DIR = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(".agents/governance/manifest.yaml")
VALID_STATUSES = {"icebox", "todo", "active", "blocked", "done"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KINDS = ("roadmaps", "epics", "tasks")


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


def json_yaml(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=False) + "\n"


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


def source_entries() -> dict[Path, bytes]:
    sources = {
        Path(".agents/governance/standards/STD-approval-gates-v1.0.md"):
            SKILL_DIR / "references/STD-approval-gates-v1.0.md",
        Path(".agents/governance/standards/STD-work-tracker-v1.0.md"):
            SKILL_DIR / "references/STD-work-tracker-v1.0.md",
        Path(".agents/governance/schemas/roadmap.schema.json"):
            SKILL_DIR / "assets/schemas/roadmap.schema.json",
        Path(".agents/governance/schemas/epic.schema.json"):
            SKILL_DIR / "assets/schemas/epic.schema.json",
        Path(".agents/governance/schemas/task.schema.json"):
            SKILL_DIR / "assets/schemas/task.schema.json",
        Path(".agents/governance/templates/roadmap.yaml"):
            SKILL_DIR / "assets/templates/roadmap.yaml",
        Path(".agents/governance/templates/epic.yaml"):
            SKILL_DIR / "assets/templates/epic.yaml",
        Path(".agents/governance/templates/task.yaml"):
            SKILL_DIR / "assets/templates/task.yaml",
        Path(".agents/governance/bin/govern_work_tracker.py"):
            Path(__file__).resolve(),
    }
    entries: dict[Path, bytes] = {}
    for target, source in sources.items():
        if not source.is_file():
            raise FileNotFoundError(f"work-tracker pack source is missing: {source}")
        entries[target] = source.read_bytes()
    for kind in KINDS:
        entries[Path("state/work") / kind / ".gitkeep"] = b""
    return entries


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
    components["work-tracker"] = {
        "version": PACK_VERSION,
        "files": {path.as_posix(): sha256(data) for path, data in sorted(entries.items())},
    }
    manifest["schema_version"] = "1.0"
    manifest["source"] = PACK_SOURCE
    return json_yaml(manifest).encode()


def planned_writes(repo: Path) -> dict[Path, bytes]:
    entries = source_entries()
    entries[MANIFEST_PATH] = manifest_content(repo, entries)
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
    repo: Path, entries: dict[Path, bytes], *, generated_updates: set[Path] | None = None
) -> tuple[int, list[dict[str, str]]]:
    rows = classify_writes(repo, entries, generated_updates=generated_updates)
    if any(row["action"] == "conflict" for row in rows):
        return 2, rows
    for row in rows:
        if row["action"] not in {"create", "update"}:
            continue
        rel = Path(row["path"])
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(entries[rel])
    return 0, rows


def audit_manifest(repo: Path) -> list[Finding]:
    path = repo / MANIFEST_PATH
    if not is_confined(repo, path):
        return [Finding("TRACKER020", "error", MANIFEST_PATH.as_posix(), "governance path resolves outside the repository")]
    if not path.is_file():
        return [Finding("TRACKER001", "warning", MANIFEST_PATH.as_posix(), "governance pack is not initialized", True)]
    try:
        manifest = read_structured(path)
    except ValueError as exc:
        return [Finding("TRACKER001", "error", MANIFEST_PATH.as_posix(), str(exc))]
    component = manifest.get("components", {}).get("work-tracker", {}) if isinstance(manifest, dict) else {}
    files = component.get("files", {}) if isinstance(component, dict) else {}
    if not isinstance(files, dict):
        return [Finding("TRACKER001", "warning", MANIFEST_PATH.as_posix(), "work-tracker component is not installed", True)]
    findings: list[Finding] = []
    for rel, expected in sorted(files.items()):
        target = repo / rel
        if not target.is_file():
            findings.append(Finding("TRACKER002", "warning", rel, "managed tracker file is missing", True))
        elif sha256(target.read_bytes()) != expected:
            findings.append(Finding("TRACKER003", "warning", rel, "managed tracker file differs from the installed hash"))
    return findings


def load_records(repo: Path) -> tuple[dict[str, list[tuple[Path, dict[str, Any]]]], list[Finding]]:
    records: dict[str, list[tuple[Path, dict[str, Any]]]] = {kind: [] for kind in KINDS}
    findings: list[Finding] = []
    for kind in KINDS:
        root = repo / "state/work" / kind
        if not is_confined(repo, root) or root.is_symlink():
            findings.append(Finding("TRACKER020", "error", root.relative_to(repo).as_posix(), "tracker path resolves outside the repository"))
            continue
        if not root.exists():
            findings.append(Finding("TRACKER004", "warning", root.relative_to(repo).as_posix(), "tracker directory is missing", True))
            continue
        for path in sorted(root.glob("*.yaml")) + sorted(root.glob("*.yml")) + sorted(root.glob("*.json")):
            try:
                data = read_structured(path)
            except ValueError as exc:
                findings.append(Finding("TRACKER005", "error", path.relative_to(repo).as_posix(), str(exc)))
                continue
            if not isinstance(data, dict):
                findings.append(Finding("TRACKER005", "error", path.relative_to(repo).as_posix(), "record root must be a mapping"))
                continue
            records[kind].append((path, data))
    return records, findings


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_records(repo: Path, records: dict[str, list[tuple[Path, dict[str, Any]]]]) -> list[Finding]:
    findings: list[Finding] = []
    all_ids: dict[str, tuple[str, Path]] = {}
    indexed: dict[str, dict[str, dict[str, Any]]] = {kind: {} for kind in KINDS}

    for kind, items in records.items():
        for path, record in items:
            rel = path.relative_to(repo).as_posix()
            record_id = record.get("id")
            if not nonempty(record_id) or not ID_RE.fullmatch(record_id):
                findings.append(Finding("TRACKER006", "error", rel, "id must be lowercase kebab-case"))
                continue
            if path.stem != record_id:
                findings.append(Finding("TRACKER006", "error", rel, f"filename stem must equal id {record_id!r}"))
            if record_id in all_ids:
                findings.append(Finding("TRACKER007", "error", rel, f"duplicate id also used by {all_ids[record_id][1].relative_to(repo)}"))
            all_ids[record_id] = (kind, path)
            indexed[kind][record_id] = record

            for field in ("title", "status", "rank", "updated_at"):
                if field not in record:
                    findings.append(Finding("TRACKER008", "error", rel, f"missing required field {field}"))
            if not nonempty(record.get("title")):
                findings.append(Finding("TRACKER008", "error", rel, "title must be non-empty"))
            if record.get("status") not in VALID_STATUSES:
                findings.append(Finding("TRACKER009", "error", rel, f"invalid status {record.get('status')!r}"))
            if not isinstance(record.get("rank"), int) or record.get("rank", 0) < 1:
                findings.append(Finding("TRACKER010", "error", rel, "rank must be a positive integer"))
            updated = record.get("updated_at")
            if not nonempty(updated) or not DATE_RE.fullmatch(updated):
                findings.append(Finding("TRACKER011", "error", rel, "updated_at must use YYYY-MM-DD"))
            else:
                try:
                    date.fromisoformat(updated)
                except ValueError:
                    findings.append(Finding("TRACKER011", "error", rel, "updated_at is not a valid date"))

    roadmaps = indexed["roadmaps"]
    epics = indexed["epics"]
    tasks = indexed["tasks"]
    for path, epic in records["epics"]:
        rel = path.relative_to(repo).as_posix()
        if epic.get("roadmap_id") not in roadmaps:
            findings.append(Finding("TRACKER012", "error", rel, f"unknown roadmap_id {epic.get('roadmap_id')!r}"))
    for path, task in records["tasks"]:
        rel = path.relative_to(repo).as_posix()
        if task.get("epic_id") not in epics:
            findings.append(Finding("TRACKER013", "error", rel, f"unknown epic_id {task.get('epic_id')!r}"))
        criteria = task.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria or not all(nonempty(item) for item in criteria):
            findings.append(Finding("TRACKER014", "error", rel, "acceptance_criteria must be a non-empty string list"))
        if task.get("status") in {"active", "blocked"}:
            for field in ("current_task", "next_action", "resume_from"):
                if not nonempty(task.get(field)):
                    findings.append(Finding("TRACKER015", "error", rel, f"{task.get('status')} task needs {field}"))
        if task.get("status") == "blocked" and not nonempty(task.get("blocked_reason")):
            findings.append(Finding("TRACKER016", "error", rel, "blocked task needs blocked_reason"))
        evidence = task.get("evidence")
        if task.get("status") == "done" and (
            not isinstance(evidence, list) or not evidence or not all(nonempty(item) for item in evidence)
        ):
            findings.append(Finding("TRACKER017", "error", rel, "done task needs non-empty evidence"))

    lanes: dict[tuple[str, str], dict[int, str]] = {}
    for kind, items in records.items():
        for path, record in items:
            if record.get("status") == "done" or not isinstance(record.get("rank"), int):
                continue
            parent = "root"
            if kind == "epics":
                parent = str(record.get("roadmap_id"))
            elif kind == "tasks":
                parent = str(record.get("epic_id"))
            lane = lanes.setdefault((kind, parent), {})
            if record["rank"] in lane:
                findings.append(Finding(
                    "TRACKER018", "error", path.relative_to(repo).as_posix(),
                    f"rank {record['rank']} duplicates {lane[record['rank']]} in the same lane",
                ))
            else:
                lane[record["rank"]] = str(record.get("id"))

    for kind, items in records.items():
        for path, record in items:
            dependencies = record.get("depends_on", [])
            if dependencies is None:
                dependencies = []
            if not isinstance(dependencies, list):
                findings.append(Finding("TRACKER019", "error", path.relative_to(repo).as_posix(), "depends_on must be a list"))
                continue
            for dependency in dependencies:
                if dependency not in all_ids:
                    findings.append(Finding("TRACKER019", "error", path.relative_to(repo).as_posix(), f"unknown dependency {dependency!r}"))
    return findings


def audit(repo: Path) -> list[Finding]:
    findings = audit_manifest(repo)
    records, load_findings = load_records(repo)
    findings.extend(load_findings)
    findings.extend(validate_records(repo, records))
    return findings


def render_findings(findings: list[Finding], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps({"findings": [asdict(item) for item in findings]}, indent=2))
        return
    if not findings:
        print("Work tracker audit passed with no findings.")
        return
    for finding in findings:
        suffix = " [fixable]" if finding.fixable else ""
        print(f"{finding.severity.upper()} {finding.id} {finding.path}: {finding.message}{suffix}")
    print(f"\nAdvisory findings: {len(findings)}")


def fix_entries(repo: Path, selected: str | None) -> dict[Path, bytes]:
    findings = audit(repo)
    if selected:
        findings = [item for item in findings if item.id == selected]
    ids = {item.id for item in findings}
    entries: dict[Path, bytes] = {}
    restore_pack = bool(ids & {"TRACKER001", "TRACKER002", "TRACKER004"})
    if restore_pack:
        for rel, data in source_entries().items():
            if not (repo / rel).exists():
                entries[rel] = data
    if restore_pack:
        entries[MANIFEST_PATH] = manifest_content(repo, source_entries())
    return entries


def print_plan(rows: list[dict[str, str]], *, applying: bool) -> None:
    print("Apply result:" if applying else "Dry-run plan:")
    if not rows:
        print("- no mechanical changes available; semantic findings require review")
        return
    for row in rows:
        print(f"- {row['action']}: {row['path']}")


def add_repo_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    audit_parser = commands.add_parser("audit", help="Run a read-only tracker audit")
    add_repo_argument(audit_parser)
    audit_parser.add_argument("--format", choices=("text", "json"), default="text")
    audit_parser.add_argument("--strict", action="store_true", help="Return nonzero when findings exist")

    init_parser = commands.add_parser("initialize", help="Plan or install the tracker pack")
    add_repo_argument(init_parser)
    init_parser.add_argument("--apply", action="store_true", help="Write the displayed plan")
    init_parser.add_argument("--dry-run", action="store_true", help="Explicitly select the default no-write mode")

    fix_parser = commands.add_parser("fix", help="Plan or restore missing managed files")
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
            entries = planned_writes(repo)
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
    else:
        entries = fix_entries(repo, args.finding)
    generated = {MANIFEST_PATH}
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
