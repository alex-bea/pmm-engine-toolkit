#!/usr/bin/env python3
"""Read-only audit for opted-in governed Markdown documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError:  # The standalone skill keeps a bounded parser fallback.
    yaml = None


DOC_TYPES = {"STD", "RUN", "DOC", "REF", "BP"}
STATUSES = {"Draft", "Active", "Deprecated", "Superseded", "Archived"}
REQUIRED_FIELDS = {
    "doc_type",
    "normative",
    "requires",
    "status",
    "version",
    "owner",
    "consumers",
    "change_control",
}
EXCLUDED_PARTS = {".git", ".venv", "__pycache__"}
LOCAL_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    path: str
    message: str


class FrontmatterError(ValueError):
    """Raised when the dependency-free frontmatter parser cannot read the mapping."""


def relative_path(repo: Path, path: Path) -> str:
    return path.relative_to(repo).as_posix()


def within(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def simple_scalar(value: str) -> Any:
    value = value.strip()
    if value == "[]":
        return []
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"\"", "'"}:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        items = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        return [simple_scalar(item) for item in items]
    return value


def simple_yaml_mapping(raw: str) -> dict[str, Any]:
    """Parse the small YAML subset used by the governed-document metadata contract.

    This fallback lets an individually installed skill run without an extra package. Full
    YAML parsing is used whenever PyYAML is available.
    """
    result: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?", line)
        if not match:
            raise FrontmatterError(f"unsupported YAML syntax: {line}")
        key, value = match.groups()
        if value:
            result[key] = simple_scalar(value)
            continue
        items: list[Any] = []
        while index < len(lines):
            nested = lines[index]
            if not nested.strip() or nested.lstrip().startswith("#"):
                index += 1
                continue
            item_match = re.fullmatch(r"\s+-\s+(.*)", nested)
            if not item_match:
                break
            items.append(simple_scalar(item_match.group(1)))
            index += 1
        result[key] = items if items else ""
    return result


def parse_yaml_mapping(raw: str) -> dict[str, Any]:
    if yaml is None:
        return simple_yaml_mapping(raw)
    try:
        parsed = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise FrontmatterError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise FrontmatterError("frontmatter must be a mapping")
    return parsed


def frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None, str]:
    """Return parsed metadata, an error, and Markdown body.

    A file with no opening fence or no `doc_type` declaration is not governed.
    """
    if not text.startswith("---\n"):
        return None, None, text
    closing = text.find("\n---\n", 4)
    raw = text[4:] if closing < 0 else text[4:closing]
    body = "" if closing < 0 else text[closing + 5:]
    if not re.search(r"^doc_type\s*:", raw, re.MULTILINE):
        return None, None, body
    if closing < 0:
        return {}, "frontmatter is not terminated", body
    try:
        return parse_yaml_mapping(raw), None, body
    except FrontmatterError as exc:
        return {}, str(exc), body


def find_governed_documents(repo: Path) -> list[tuple[Path, dict[str, Any], str | None, str]]:
    documents: list[tuple[Path, dict[str, Any], str | None, str]] = []
    for path in sorted(repo.rglob("*.md")):
        if path.name == "SKILL.md" or path.is_symlink():
            continue
        if any(part in EXCLUDED_PARTS for part in path.relative_to(repo).parts):
            continue
        if not within(repo, path):
            continue
        try:
            metadata, error, body = frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if metadata is not None:
            documents.append((path, metadata, error, body))
    return documents


def validate_metadata(repo: Path, path: Path, metadata: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative_path(repo, path)
    missing = sorted(field for field in REQUIRED_FIELDS if field not in metadata)
    if missing:
        findings.append(Finding("DOC002", "error", rel, f"missing required metadata: {', '.join(missing)}"))
    if metadata.get("doc_type") not in DOC_TYPES:
        findings.append(Finding("DOC003", "error", rel, "doc_type must be one of " + ", ".join(sorted(DOC_TYPES))))
    if not isinstance(metadata.get("normative"), bool):
        findings.append(Finding("DOC004", "error", rel, "normative must be a boolean"))
    if metadata.get("status") not in STATUSES:
        findings.append(Finding("DOC005", "error", rel, "status must be one of " + ", ".join(sorted(STATUSES))))
    for field in ("version", "owner", "change_control"):
        if field in metadata and (not isinstance(metadata[field], str) or not metadata[field].strip()):
            findings.append(Finding("DOC006", "error", rel, f"{field} must be a non-empty string"))
    for field in ("requires", "consumers"):
        value = metadata.get(field)
        if field in metadata and (not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value)):
            findings.append(Finding("DOC007", "error", rel, f"{field} must be a list of non-empty strings"))
    return findings


def validate_required_paths(repo: Path, path: Path, metadata: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    requires = metadata.get("requires")
    if not isinstance(requires, list):
        return findings
    rel = relative_path(repo, path)
    for required in requires:
        if not isinstance(required, str) or not required.strip():
            continue
        target = path.parent / required
        if not within(repo, target):
            findings.append(Finding("DOC008", "error", rel, f"requires path escapes repository: {required}"))
        elif not target.is_file():
            findings.append(Finding("DOC009", "error", rel, f"requires path does not exist: {required}"))
    return findings


def local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip().split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return target


def validate_local_links(repo: Path, path: Path, body: str) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative_path(repo, path)
    for raw_target in LOCAL_LINK.findall(body):
        target_text = local_link_target(raw_target)
        if target_text is None:
            continue
        target = path.parent / target_text
        if not within(repo, target):
            findings.append(Finding("DOC010", "error", rel, f"local link escapes repository: {raw_target}"))
        elif not target.exists():
            findings.append(Finding("DOC011", "error", rel, f"broken local Markdown link: {raw_target}"))
    return findings


def audit(repo: Path) -> tuple[int, list[Finding]]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise ValueError(f"repository is not a directory: {repo}")
    findings: list[Finding] = []
    documents = find_governed_documents(repo)
    for path, metadata, parse_error, body in documents:
        rel = relative_path(repo, path)
        if parse_error:
            findings.append(Finding("DOC001", "error", rel, parse_error))
            continue
        findings.extend(validate_metadata(repo, path, metadata))
        findings.extend(validate_required_paths(repo, path, metadata))
        findings.extend(validate_local_links(repo, path, body))
    return len(documents), findings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit", help="audit opted-in governed Markdown")
    audit_parser.add_argument("--repo", required=True, type=Path, help="repository to audit")
    audit_parser.add_argument("--format", choices=("text", "json"), default="text")
    audit_parser.add_argument("--strict", action="store_true", help="fail when findings exist")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        count, findings = audit(args.repo)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps({"governed_documents": count, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print(f"Audited {count} governed Markdown document(s).")
        if findings:
            for item in findings:
                print(f"{item.id} {item.severity} {item.path}: {item.message}")
        else:
            print("No findings.")
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
