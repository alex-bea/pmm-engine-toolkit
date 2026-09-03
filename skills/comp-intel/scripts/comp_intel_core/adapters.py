"""Offline source adapters and their shared capability contract."""

from __future__ import annotations

import json
import mimetypes
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .contracts import validate_candidate
from .io_utils import digest_bytes, ensure_within, read_json, relative_safe


@dataclass
class Capability:
    source_id: str
    adapter_id: str
    state: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "adapter_id": self.adapter_id,
            "state": self.state,
            "message": self.message,
        }


@dataclass
class CollectionResult:
    candidates: list[dict[str, Any]] = field(default_factory=list)
    checkpoint: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    complete: bool = True


class SourceAdapter:
    adapter_id = "base"
    version = "1.0.0"

    def probe(self, source: dict[str, Any], data_root: Path) -> Capability:
        raise NotImplementedError

    def collect(self, source: dict[str, Any], data_root: Path) -> CollectionResult:
        raise NotImplementedError


class SyntheticAdapter(SourceAdapter):
    adapter_id = "synthetic"

    def _fixture(self, source: dict[str, Any], data_root: Path) -> Path:
        raw = source.get("config", {}).get("fixture_path")
        if not isinstance(raw, str) or not raw:
            raise ValueError("synthetic fixture_path is required")
        if Path(raw).is_absolute() or ".." in Path(raw).parts:
            raise ValueError("synthetic fixture_path must be relative to the data root")
        return ensure_within(data_root / raw, data_root, must_exist=True)

    def probe(self, source: dict[str, Any], data_root: Path) -> Capability:
        try:
            fixture = self._fixture(source, data_root)
            value = read_json(fixture)
            if not isinstance(value, dict) or not isinstance(value.get("pages"), list):
                raise ValueError("fixture must contain a pages array")
        except (OSError, ValueError) as exc:
            return Capability(source["source_id"], self.adapter_id, "missing", str(exc))
        return Capability(source["source_id"], self.adapter_id, "available", "fixture is readable")

    def collect(self, source: dict[str, Any], data_root: Path) -> CollectionResult:
        value = read_json(self._fixture(source, data_root))
        pages = value.get("pages")
        if not isinstance(pages, list):
            raise ValueError("synthetic fixture must contain a pages array")
        failure = value.get("failure") if isinstance(value.get("failure"), dict) else {}
        fail_after = failure.get("after_page")
        result = CollectionResult(checkpoint={"next_page": 0, "pages_total": len(pages)})
        for page_number, page in enumerate(pages, start=1):
            if fail_after is not None and page_number > fail_after:
                result.complete = False
                result.errors.append(str(failure.get("message") or "synthetic adapter failure"))
                break
            if not isinstance(page, list):
                result.complete = False
                result.errors.append(f"page {page_number} must be an array")
                break
            for index, candidate in enumerate(page):
                errors = validate_candidate(candidate, f"page[{page_number}][{index}]")
                if errors:
                    result.warnings.extend(errors)
                    continue
                copied = dict(candidate)
                copied["_adapter_id"] = self.adapter_id
                copied["_adapter_version"] = self.version
                copied["_source_id"] = source["source_id"]
                copied["_query_id"] = copied.get("query_id", source["source_id"])
                result.candidates.append(copied)
            result.checkpoint["next_page"] = page_number
        return result


class LocalFilesAdapter(SourceAdapter):
    adapter_id = "local_files"
    supported_extensions = {".json", ".md", ".txt"}

    def _resolve(self, source: dict[str, Any], data_root: Path) -> tuple[list[Path], list[Path]]:
        config = source.get("config", {})
        raw_roots = config.get("allowed_roots")
        raw_files = config.get("files")
        if not isinstance(raw_roots, list) or not raw_roots:
            raise ValueError("local_files allowed_roots must be a non-empty array")
        if not isinstance(raw_files, list):
            raise ValueError("local_files files must be an array")
        roots: list[Path] = []
        for raw in raw_roots:
            if not isinstance(raw, str) or Path(raw).is_absolute() or ".." in Path(raw).parts:
                raise ValueError("local_files allowed roots must be safe relative paths")
            root = ensure_within(data_root / raw, data_root, must_exist=True)
            if not root.is_dir():
                raise ValueError(f"allowed root is not a directory: {raw}")
            roots.append(root)
        files: list[Path] = []
        for raw in raw_files:
            if not isinstance(raw, str) or Path(raw).is_absolute() or ".." in Path(raw).parts:
                raise ValueError("local_files file entries must be safe relative paths")
            path = ensure_within(data_root / raw, data_root, must_exist=True)
            if not any(_is_within(path, root) for root in roots):
                raise ValueError(f"local file is outside allowed roots: {raw}")
            if not path.is_file():
                raise ValueError(f"local source is not a file: {raw}")
            if path.suffix.lower() not in self.supported_extensions:
                raise ValueError(f"unsupported local file format: {path.suffix}")
            files.append(path)
        return roots, files

    def probe(self, source: dict[str, Any], data_root: Path) -> Capability:
        try:
            _, files = self._resolve(source, data_root)
        except (OSError, ValueError) as exc:
            return Capability(source["source_id"], self.adapter_id, "missing", str(exc))
        return Capability(source["source_id"], self.adapter_id, "available", f"{len(files)} file(s) readable")

    def collect(self, source: dict[str, Any], data_root: Path) -> CollectionResult:
        _, files = self._resolve(source, data_root)
        config = source.get("config", {})
        maximum_files = int(config.get("max_files", 100))
        maximum_bytes = int(config.get("max_bytes_per_file", 1_000_000))
        if len(files) > maximum_files:
            return CollectionResult(errors=[f"local file count exceeds configured maximum {maximum_files}"], complete=False)
        result = CollectionResult(checkpoint={"files_total": len(files), "files_read": 0})
        for path in files:
            raw = path.read_bytes()
            if len(raw) > maximum_bytes:
                result.errors.append(f"file exceeds configured byte maximum: {relative_safe(path, data_root)}")
                result.complete = False
                continue
            try:
                candidates = self._parse_file(path, raw, source, data_root)
            except (UnicodeDecodeError, ValueError) as exc:
                result.warnings.append(str(exc))
                continue
            for index, candidate in enumerate(candidates):
                errors = validate_candidate(candidate, f"{relative_safe(path, data_root)}[{index}]")
                if errors:
                    result.warnings.extend(errors)
                    continue
                candidate["_adapter_id"] = self.adapter_id
                candidate["_adapter_version"] = self.version
                candidate["_source_id"] = source["source_id"]
                candidate["_query_id"] = candidate.get("query_id", source["source_id"])
                candidate.setdefault("metadata", {})
                candidate["metadata"].update({
                    "relative_path": relative_safe(path, data_root),
                    "content_digest": digest_bytes(raw),
                    "media_type": mimetypes.guess_type(path.name)[0] or "text/plain",
                    "parser_version": self.version,
                })
                result.candidates.append(candidate)
            result.checkpoint["files_read"] += 1
        return result

    def _parse_file(self, path: Path, raw: bytes, source: dict[str, Any], data_root: Path) -> list[dict[str, Any]]:
        if path.suffix.lower() == ".json":
            try:
                value = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON in local source {relative_safe(path, data_root)}: {exc}") from exc
            rows = value if isinstance(value, list) else value.get("candidates") if isinstance(value, dict) else None
            if not isinstance(rows, list):
                raise ValueError(f"local JSON source must be an array or candidates object: {relative_safe(path, data_root)}")
            return [dict(row) if isinstance(row, dict) else row for row in rows]
        text = raw.decode("utf-8")
        summary = " ".join(line.strip("# ") for line in text.splitlines() if line.strip())[:1000]
        defaults = source.get("config", {}).get("defaults", {})
        return [{
            "native_id": relative_safe(path, data_root),
            "source_version": digest_bytes(raw),
            "canonical_uri": f"local:{relative_safe(path, data_root)}",
            "title": path.stem.replace("-", " ").title(),
            "summary": summary,
            "source_type": defaults.get("source_type", "local_file"),
            "competitor_id": defaults.get("competitor_id", "unknown"),
            "category": defaults.get("category", "other"),
            "classification": defaults.get("classification", "reported"),
            "confidence": defaults.get("confidence", "low"),
            "sensitivity": defaults.get("sensitivity", "internal"),
            "public_safe": defaults.get("public_safe", False),
        }]


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


ADAPTERS: dict[str, SourceAdapter] = {
    "synthetic": SyntheticAdapter(),
    "local_files": LocalFilesAdapter(),
}


def adapter_for(adapter_id: str) -> SourceAdapter | None:
    return ADAPTERS.get(adapter_id)
