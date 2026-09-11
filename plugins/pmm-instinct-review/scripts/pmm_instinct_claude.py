"""Self-contained native Claude capture, extraction, and promotion runtime.

The module intentionally uses only the Python standard library. Session evidence is
untrusted input: it is minimized before persistence, supplied to a tool-less ephemeral
Claude invocation, and never executed by this runtime.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from collections import deque
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


ALLOWED_TYPES = ("correction", "confirmation", "voice", "scope", "workflow")
QUEUE_STATES = ("queued", "processing", "retryable", "completed", "failed")
QUEUE_SCHEMA_VERSION = 1
REVIEW_LEDGER_SCHEMA_VERSION = 2
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
AUDIT_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}-(?P<job_id>[A-Za-z0-9._-]+)-audit\.md$")
PROMOTED_GUIDANCE_HEADING = "## PMM Instinct Review — Promoted Guidance"
RUNTIME_SUMMARY_FIELDS = {
    "schema_version",
    "updated_at",
    "pending_extraction",
    "review_ready",
    "pending_promotion",
}
DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": 1,
    "enabled": False,
    "privacy_acknowledged_at": None,
    "min_user_messages": 5,
    "max_turns": 200,
    "max_normalized_chars": 120000,
    "max_attempts": 3,
    "processing_lease_seconds": 900,
    "extractor_model": "sonnet",
    "extractor_timeout_seconds": 900,
    "claude_binary": None,
}
STATE_ROOT_ENTRIES = {
    "config.json",
    "capture-inbox",
    "sessions",
    "queue",
    "instincts",
    "logs",
    "state",
    "promotion-receipts",
    "promotion-outcomes",
    "promotion-changesets",
}
CONTEXT_WRAPPER_MARKERS = tuple(
    (f"<{tag}>", f"</{tag}>")
    for tag in (
        "environment_context",
        "recommended_plugins",
        "app-context",
        "skills_instructions",
        "plugins_instructions",
        "permissions instructions",
        "model-switch",
        "model_switch",
        "system-reminder",
        "task-notification",
        "teammate-notification",
        "teammate-message",
    )
)
PEM_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----.*?"
    r"-----END (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    re.DOTALL,
)
BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")
KNOWN_TOKEN_RE = re.compile(
    r"\b(?:sk-(?:ant-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"xox[baprs]-[A-Za-z0-9-]{12,}|AKIA[0-9A-Z]{16})\b"
)
ENV_SECRET_RE = re.compile(
    r"(?im)^(\s*(?:export\s+)?[A-Za-z_][A-Za-z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)"
    r"[A-Za-z0-9_]*\s*=)\s*[^\n]*$"
)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


@dataclass(frozen=True)
class RuntimePaths:
    state_root: Path
    capture_inbox: Path
    sessions: Path
    queue: Path
    instincts: Path
    logs: Path
    state: Path
    previews: Path
    receipts: Path
    outcomes: Path
    changesets: Path
    config: Path


@dataclass(frozen=True)
class Turn:
    index: int
    role: str
    text: str


@dataclass(frozen=True)
class NormalizationResult:
    session_id: str
    cwd: str
    timestamp: str
    eligible_main_thread: bool
    turns: tuple[Turn, ...]
    user_messages: int
    normalized_chars: int
    redactions: int
    transcript_sha256: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now(value: datetime | None = None) -> str:
    return (value or utc_now()).astimezone(timezone.utc).isoformat(timespec="seconds")


def bundle_root() -> Path:
    return Path(__file__).resolve().parents[1]


def resolve_state_root(
    state_root: str | Path | None = None,
    *,
    plugin_data: str | Path | None = None,
) -> Path:
    if state_root:
        candidate = Path(state_root).expanduser()
    else:
        plugin = plugin_data or os.environ.get("CLAUDE_PLUGIN_DATA")
        if plugin:
            candidate = Path(plugin).expanduser() / "instinct-review"
        else:
            standalone = os.environ.get("PMM_INSTINCT_STATE_ROOT")
            if not standalone:
                raise ValueError("--state-root or CLAUDE_PLUGIN_DATA is required; no ambient store fallback is allowed")
            candidate = Path(standalone).expanduser()
    if candidate.is_symlink():
        raise ValueError("runtime state root must not be a symlink")
    root = candidate.resolve()
    package = bundle_root().resolve()
    if root == package or package in root.parents or root in package.parents:
        raise ValueError("runtime state root must be outside the installed bundle")
    if "plugins/cache" in root.as_posix():
        raise ValueError("runtime state root must be outside plugin caches")
    home = Path.home().resolve()
    claude_home = home / ".claude"
    codex_home = home / ".codex"
    if root in {Path(root.anchor), home, claude_home, codex_home} or codex_home in root.parents:
        raise ValueError("runtime state root must be a dedicated subdirectory")
    legacy_claude_store = claude_home / "instinct-review"
    if root == legacy_claude_store or legacy_claude_store in root.parents:
        raise ValueError("runtime state root must not reuse the legacy Claude review store")
    return root


def resolve_paths(
    state_root: str | Path | None = None,
    *,
    plugin_data: str | Path | None = None,
) -> RuntimePaths:
    root = resolve_state_root(state_root, plugin_data=plugin_data)
    return RuntimePaths(
        state_root=root,
        capture_inbox=root / "capture-inbox",
        sessions=root / "sessions",
        queue=root / "queue",
        instincts=root / "instincts",
        logs=root / "logs",
        state=root / "state",
        previews=root / "state" / "promotion-previews",
        receipts=root / "promotion-receipts",
        outcomes=root / "promotion-outcomes",
        changesets=root / "promotion-changesets",
        config=root / "config.json",
    )


def atomic_write_text(path: str | Path, text: str, *, mode: int = 0o600) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    created = os.fstat(descriptor)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        current = temporary.lstat()
        if (
            not stat.S_ISREG(current.st_mode)
            or current.st_dev != created.st_dev
            or current.st_ino != created.st_ino
        ):
            raise OSError("atomic write temporary file identity changed")
        os.replace(temporary, destination)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            current = temporary.lstat()
        except FileNotFoundError:
            pass
        else:
            if current.st_dev == created.st_dev and current.st_ino == created.st_ino:
                temporary.unlink()
    return destination


def atomic_write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    return atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _validate_store_layout(paths: RuntimePaths) -> None:
    root = paths.state_root
    if root.is_symlink() or (root.exists() and not root.is_dir()):
        raise ValueError("runtime state root must be a regular directory")
    if root.exists():
        unknown = sorted(item.name for item in root.iterdir() if item.name not in STATE_ROOT_ENTRIES)
        if unknown:
            raise ValueError("runtime state root is not a dedicated PMM Instinct Review store")
    for directory in (
        paths.state_root,
        paths.capture_inbox,
        paths.sessions,
        paths.queue,
        paths.instincts,
        paths.logs,
        paths.state,
        paths.previews,
        paths.receipts,
        paths.outcomes,
        paths.changesets,
    ):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise ValueError(f"runtime state directory must be a regular directory: {directory.name}")
    if paths.config.is_symlink() or (paths.config.exists() and not paths.config.is_file()):
        raise ValueError("runtime config must be a regular file")


def ensure_store(paths: RuntimePaths, *, create_config: bool = True) -> None:
    _validate_store_layout(paths)
    for directory in (
        paths.state_root,
        paths.capture_inbox,
        paths.sessions,
        paths.queue,
        paths.instincts,
        paths.logs,
        paths.state,
        paths.previews,
        paths.receipts,
        paths.outcomes,
        paths.changesets,
    ):
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
    if create_config and not paths.config.exists():
        atomic_write_json(paths.config, dict(DEFAULT_CONFIG))
    if paths.config.exists():
        paths.config.chmod(0o600)


def load_config(paths: RuntimePaths, *, create: bool = False) -> dict[str, Any]:
    _validate_store_layout(paths)
    if create:
        ensure_store(paths)
    if not paths.config.exists():
        return dict(DEFAULT_CONFIG)
    try:
        payload = json.loads(paths.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid Claude instinct config: {type(error).__name__}") from error
    if not isinstance(payload, dict):
        raise ValueError("invalid Claude instinct config: expected an object")
    return _validated_config_payload(payload)


def _validated_config_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if set(payload) != set(DEFAULT_CONFIG):
        raise ValueError("invalid Claude instinct config: fields do not match schema version 1")
    config = {**DEFAULT_CONFIG, **payload}
    if type(config.get("schema_version")) is not int or config["schema_version"] != 1:
        raise ValueError("invalid Claude instinct config: schema_version must be 1")
    if type(config.get("enabled")) is not bool:
        raise ValueError("invalid Claude instinct config: enabled must be true or false")
    acknowledgement = config.get("privacy_acknowledged_at")
    if acknowledgement is not None and _parse_timestamp(acknowledgement) is None:
        raise ValueError("invalid Claude instinct config: privacy acknowledgement must be an ISO timestamp or null")
    integer_limits = {
        "min_user_messages": 1000,
        "max_turns": 10000,
        "max_normalized_chars": 10_000_000,
        "max_attempts": 100,
        "processing_lease_seconds": 86_400,
        "extractor_timeout_seconds": 86_400,
    }
    for field, maximum in integer_limits.items():
        if type(config.get(field)) is not int or not 1 <= config[field] <= maximum:
            raise ValueError(f"invalid Claude instinct config: {field} must be a positive integer")
    model = config.get("extractor_model")
    if not isinstance(model, str) or not model.strip() or len(model) > 200:
        raise ValueError("invalid Claude instinct config: extractor_model must be a non-empty string")
    binary = config.get("claude_binary")
    if binary is not None:
        if not isinstance(binary, str) or not binary.strip() or len(binary) > 4096:
            raise ValueError("invalid Claude instinct config: claude_binary must be a canonical path or null")
        binary_path = Path(binary).expanduser()
        if not binary_path.is_absolute() or str(binary_path.resolve()) != binary:
            raise ValueError("invalid Claude instinct config: claude_binary must be a canonical path or null")
    return config


def update_config(paths: RuntimePaths, **updates: Any) -> dict[str, Any]:
    config = load_config(paths, create=True)
    config.update(updates)
    config = _validated_config_payload(config)
    atomic_write_json(paths.config, config)
    return config


def redact_text_with_count(text: str) -> tuple[str, int]:
    total = 0

    def replace(pattern: re.Pattern[str], value: str, source: str) -> str:
        nonlocal total
        updated, count = pattern.subn(value, source)
        total += count
        return updated

    result = replace(PEM_RE, "[REDACTED PRIVATE KEY]", text)
    result = replace(BEARER_RE, "Bearer [REDACTED TOKEN]", result)
    result = replace(KNOWN_TOKEN_RE, "[REDACTED TOKEN]", result)
    result = replace(ENV_SECRET_RE, r"\1[REDACTED]", result)
    return result, total


def _is_context_wrapper_turn(text: str) -> bool:
    stripped = text.strip()
    return bool(stripped) and not _strip_context_wrappers(stripped)


def _strip_context_wrappers(text: str) -> str:
    """Remove native context wrappers even when mixed into a conversation turn."""
    result = text
    for opening, _ in CONTEXT_WRAPPER_MARKERS:
        tag = re.escape(opening[1:-1])
        complete = re.compile(rf"<{tag}(?:\s[^>]*)?>.*?</{tag}\s*>", re.IGNORECASE | re.DOTALL)
        result = complete.sub("", result)
        unmatched = re.search(rf"<{tag}(?:\s[^>]*)?>", result, re.IGNORECASE)
        if unmatched:
            result = result[: unmatched.start()]
    return result.strip()


def _message_text(record: dict[str, Any]) -> tuple[str, str]:
    message = record.get("message")
    if isinstance(message, dict):
        role = str(message.get("role") or "").strip().lower()
        content = message.get("content")
    else:
        role = str(record.get("type") or "").strip().lower()
        content = record.get("content")
    if role not in {"user", "assistant"}:
        return "", ""
    if isinstance(content, str):
        return role, content
    if not isinstance(content, list):
        return "", ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict) or item.get("type") not in {"text", "input_text", "output_text"}:
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())
    return role, "\n".join(parts)


def _limit_turns(pairs: list[tuple[str, str]], *, max_turns: int, max_chars: int) -> list[tuple[str, str]]:
    if max_turns <= 0 or max_chars <= 0:
        return []
    selected: list[tuple[str, str]] = []
    used = 0
    for role, text in reversed(pairs[-max(0, max_turns) :]):
        remaining = max_chars - used
        if remaining <= 0:
            break
        kept = text if len(text) <= remaining else text[-remaining:]
        selected.append((role, kept))
        used += len(kept)
    return list(reversed(selected))


def normalize_transcript(
    transcript_path: str | Path,
    *,
    max_turns: int = 200,
    max_chars: int = 120000,
) -> NormalizationResult:
    path = Path(transcript_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Claude transcript not found: {path}")
    digest = hashlib.sha256()
    pairs: deque[tuple[str, str]] = deque(maxlen=max(0, max_turns))
    last_pair: tuple[str, str] | None = None
    metadata: dict[str, Any] = {}
    sidechain = False
    redactions = 0
    with path.open("rb") as handle:
        for raw in handle:
            digest.update(raw)
            try:
                record = json.loads(raw.decode("utf-8", errors="replace"))
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict):
                continue
            if record.get("isMeta") is True or record.get("is_meta") is True:
                continue
            role, raw_text = _message_text(record)
            if not role:
                continue
            sidechain = sidechain or bool(record.get("isSidechain") or record.get("is_sidechain"))
            if not metadata:
                metadata = record
            stripped = _strip_context_wrappers(raw_text.strip())
            if not stripped:
                continue
            text, count = redact_text_with_count(stripped)
            redactions += count
            pair = (role, text.strip())
            if pair[1] and pair != last_pair:
                pairs.append(pair)
                last_pair = pair
    limited = _limit_turns(list(pairs), max_turns=max_turns, max_chars=max_chars)
    user_messages = sum(role == "user" for role, _ in limited)
    turns = tuple(Turn(index, role, text) for index, (role, text) in enumerate(limited, start=1))
    return NormalizationResult(
        session_id=str(metadata.get("sessionId") or metadata.get("session_id") or "").strip(),
        cwd=str(metadata.get("cwd") or "").strip(),
        timestamp=str(metadata.get("timestamp") or "").strip(),
        eligible_main_thread=not sidechain,
        turns=turns,
        user_messages=user_messages,
        normalized_chars=sum(len(turn.text) for turn in turns),
        redactions=redactions,
        transcript_sha256=digest.hexdigest(),
    )


def _safe_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]", "-", value).strip("-.")
    return (safe or "unknown")[:100]


def _job_id(session_id: str, transcript_sha256: str) -> str:
    material = f"claude\0{session_id}\0{transcript_sha256}\0schema-1".encode()
    return f"{_safe_id(session_id)[:87]}-{hashlib.sha256(material).hexdigest()[:12]}"


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _queue_artifact_paths(paths: RuntimePaths, job_id: str, audit_name: str) -> dict[str, Path]:
    match = AUDIT_NAME_RE.fullmatch(audit_name)
    if match is None or match.group("job_id") != job_id:
        raise ValueError("queue audit filename does not match the job identity")
    return {
        "queue": paths.queue / f"{job_id}.json",
        "evidence": paths.sessions / f"{job_id}-evidence.json",
        "audit": paths.sessions / audit_name,
        "result": paths.sessions / f"{job_id}-suggestions.md",
    }


def _require_exact_int(value: Any, field: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"queue {field} has an invalid integer value")
    return value


def _require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"queue {field} is not a SHA-256 digest")
    return value


def validate_queue_record(
    paths: RuntimePaths,
    queue_path: str | Path,
    payload: Any,
) -> dict[str, Any]:
    """Validate queue identity and derive all authority-bearing artifact paths."""
    path = Path(queue_path)
    if not isinstance(payload, dict):
        raise ValueError("queue record must be an object")
    allowed_fields = {
        "schema_version", "runtime", "job_id", "session_id", "transcript_sha256",
        "state", "attempts", "created_at", "updated_at", "lease_started_at",
        "finished_at", "evidence_path", "evidence_sha256", "audit_path",
        "audit_sha256", "result_path", "source_format", "extractor_model",
        "last_error", "candidate_count", "result_sha256", "manual_retries",
    }
    if set(payload) != allowed_fields:
        raise ValueError("queue record fields do not match schema version 1")
    if type(payload.get("schema_version")) is not int or payload.get("schema_version") != QUEUE_SCHEMA_VERSION:
        raise ValueError("queue schema version mismatch")
    if payload.get("runtime") != "claude":
        raise ValueError("queue runtime must be claude")
    session_id = payload.get("session_id")
    transcript_sha256 = _require_sha256(payload.get("transcript_sha256"), "transcript_sha256")
    job_id = payload.get("job_id")
    if not isinstance(session_id, str) or not session_id or not isinstance(job_id, str):
        raise ValueError("queue session and job identities must be non-empty strings")
    if _job_id(session_id, transcript_sha256) != job_id or _safe_id(job_id) != job_id:
        raise ValueError("queue job identity mismatch")
    audit_value = payload.get("audit_path")
    if not isinstance(audit_value, str):
        raise ValueError("queue audit path must be a string")
    artifacts = _queue_artifact_paths(paths, job_id, Path(audit_value).name)
    expected_values = {
        "evidence_path": artifacts["evidence"],
        "audit_path": artifacts["audit"],
        "result_path": artifacts["result"],
    }
    if path != artifacts["queue"] or path.name != f"{job_id}.json" or path.is_symlink():
        raise ValueError("queue filename does not match the job identity")
    for field, expected in expected_values.items():
        value = payload.get(field)
        if not isinstance(value, str) or value != str(expected):
            raise ValueError(f"queue {field} is not the exact state-confined path")
        if expected.exists() and expected.is_symlink():
            raise ValueError(f"queue {field} must not reference a symlink")
    _require_sha256(payload.get("evidence_sha256"), "evidence_sha256")
    _require_sha256(payload.get("audit_sha256"), "audit_sha256")
    state = payload.get("state")
    if not isinstance(state, str) or state not in QUEUE_STATES:
        raise ValueError("queue state is invalid")
    attempts = _require_exact_int(payload.get("attempts"), "attempts")
    _require_exact_int(payload.get("manual_retries", 0), "manual_retries")
    if payload.get("source_format") != "claude-code-transcript-v1":
        raise ValueError("queue source format mismatch")
    if not isinstance(payload.get("extractor_model"), str):
        raise ValueError("queue extractor model must be a string")
    for field in ("created_at", "updated_at"):
        if _parse_timestamp(payload.get(field)) is None:
            raise ValueError(f"queue {field} must be an ISO timestamp")
    for field in ("lease_started_at", "finished_at"):
        value = payload.get(field)
        if value is not None and _parse_timestamp(value) is None:
            raise ValueError(f"queue {field} must be null or an ISO timestamp")
    if payload.get("last_error") is not None and not isinstance(payload.get("last_error"), str):
        raise ValueError("queue last_error must be null or a string")
    candidate_count = payload.get("candidate_count")
    result_sha256 = payload.get("result_sha256")
    if state == "completed":
        _require_exact_int(candidate_count, "candidate_count", maximum=5)
        _require_sha256(result_sha256, "result_sha256")
        if _parse_timestamp(payload.get("finished_at")) is None:
            raise ValueError("completed queue record requires finished_at")
    else:
        if candidate_count is not None or result_sha256 is not None:
            raise ValueError("non-completed queue records cannot claim a result")
    if state == "processing" and (attempts < 1 or _parse_timestamp(payload.get("lease_started_at")) is None):
        raise ValueError("processing queue record requires an active lease and attempt")
    return dict(payload)


def _audit_stamp(timestamp: str) -> str:
    parsed: datetime | None = None
    if timestamp:
        try:
            parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        except ValueError:
            pass
    return (parsed or utc_now()).astimezone().strftime("%Y-%m-%d-%H%M")


def read_queue(paths: RuntimePaths) -> list[tuple[Path, dict[str, Any]]]:
    _validate_store_layout(paths)
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(paths.queue.glob("*.json")) if paths.queue.exists() else ():
        if path.is_symlink():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            validated = validate_queue_record(paths, path, payload)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        records.append((path, validated))
    return records


def queue_counts(paths: RuntimePaths) -> dict[str, int]:
    counts = {state: 0 for state in QUEUE_STATES}
    for _, record in read_queue(paths):
        state = str(record.get("state") or "")
        if state in counts:
            counts[state] += 1
    return counts


def read_runtime_summary(paths: RuntimePaths) -> dict[str, Any]:
    """Read one bounded worker-produced snapshot without scanning retained artifacts."""
    _validate_store_layout(paths)
    summary_path = paths.state / "runtime-summary.json"
    empty = {
        "schema_version": 1,
        "updated_at": None,
        "pending_extraction": 0,
        "review_ready": 0,
        "pending_promotion": 0,
    }
    if not summary_path.exists():
        return empty
    if summary_path.is_symlink() or not summary_path.is_file() or summary_path.stat().st_size > 4096:
        raise ValueError("runtime summary must be one bounded regular state file")
    try:
        payload = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("runtime summary is unreadable or malformed") from error
    if not isinstance(payload, dict) or set(payload) != RUNTIME_SUMMARY_FIELDS:
        raise ValueError("runtime summary has an invalid contract")
    if payload.get("schema_version") != 1 or _parse_timestamp(payload.get("updated_at")) is None:
        raise ValueError("runtime summary version or timestamp is invalid")
    for field in ("pending_extraction", "review_ready", "pending_promotion"):
        if type(payload.get(field)) is not int or not 0 <= payload[field] <= 1_000_000_000:
            raise ValueError("runtime summary counts must be bounded non-negative integers")
    return payload


def _sanitize_audit_metadata(value: Any, *, limit: int = 1000) -> str:
    redacted, _ = redact_text_with_count(str(value or ""))
    flattened = re.sub(r"[\x00-\x1f\x7f]+", " ", redacted)
    return " ".join(flattened.split())[:limit]


def _validate_existing_capture_job(
    paths: RuntimePaths,
    record: dict[str, Any],
) -> dict[str, Any]:
    """Require every retained capture artifact before accepting a duplicate."""
    validated, artifacts = _validated_queue_artifacts(paths, record)
    try:
        audit_bytes = artifacts["audit"].read_bytes()
        audit_text = audit_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("existing capture audit is unreadable") from error
    if hashlib.sha256(audit_bytes).hexdigest() != validated["audit_sha256"]:
        raise ValueError("existing capture audit digest mismatch")
    fields = _markdown_fields(audit_text)
    if (
        fields.get("source_runtime") != "claude"
        or fields.get("session_id") != _sanitize_audit_metadata(validated["session_id"])
        or fields.get("transcript_sha256") != validated["transcript_sha256"]
    ):
        raise ValueError("existing capture audit identity mismatch")

    processed = bool(re.search(r"(?m)^processed:\s*true\s*$", audit_text))
    if artifacts["evidence"].exists():
        _load_validated_evidence(paths, validated)
    elif not (validated["state"] == "completed" and processed):
        raise ValueError("existing capture evidence is missing")

    if validated["state"] == "completed":
        try:
            result_bytes = artifacts["result"].read_bytes()
        except OSError as error:
            raise ValueError("existing capture suggestion result is unreadable") from error
        if hashlib.sha256(result_bytes).hexdigest() != validated["result_sha256"]:
            raise ValueError("existing capture suggestion result digest mismatch")
    return validated


def _capture_job_is_rebuildable(paths: RuntimePaths, record: dict[str, Any]) -> bool:
    """Avoid racing active work or recreating evidence deleted after human review."""
    if record.get("state") == "processing":
        return False
    if record.get("state") != "completed":
        return True
    try:
        artifacts = _queue_artifact_paths(
            paths,
            str(record["job_id"]),
            Path(str(record["audit_path"])).name,
        )
        audit_bytes = artifacts["audit"].read_bytes()
        if hashlib.sha256(audit_bytes).hexdigest() != record["audit_sha256"]:
            return False
        audit_text = audit_bytes.decode("utf-8")
    except (KeyError, OSError, UnicodeDecodeError, ValueError):
        return False
    return re.search(r"(?m)^processed:\s*true\s*$", audit_text) is None


def capture_session(
    paths: RuntimePaths,
    *,
    session_id: str,
    transcript_path: str | Path,
    cwd: str = "",
    agent_id: str = "",
    agent_type: str = "",
    allow_worker: bool = False,
) -> dict[str, Any]:
    if os.environ.get("PMM_INSTINCT_EXTRACTOR") == "1" or (
        os.environ.get("PMM_INSTINCT_WORKER") == "1" and not allow_worker
    ):
        return {"status": "skipped", "reason": "worker-run", "session_id": session_id}
    if agent_id.strip():
        return {"status": "skipped", "reason": "subagent", "session_id": session_id}
    config = load_config(paths)
    if not config.get("enabled"):
        return {"status": "skipped", "reason": "disabled", "session_id": session_id}
    if not config.get("privacy_acknowledged_at"):
        return {"status": "skipped", "reason": "privacy-not-acknowledged", "session_id": session_id}
    normalized = normalize_transcript(
        transcript_path,
        max_turns=int(config["max_turns"]),
        max_chars=int(config["max_normalized_chars"]),
    )
    resolved_id = session_id.strip() or normalized.session_id
    if normalized.session_id and resolved_id != normalized.session_id:
        return {"status": "skipped", "reason": "session-id-mismatch", "session_id": resolved_id}
    if not normalized.eligible_main_thread:
        return {"status": "skipped", "reason": "subagent", "session_id": resolved_id}
    if normalized.user_messages < int(config["min_user_messages"]):
        return {"status": "skipped", "reason": "below-minimum-user-messages", "session_id": resolved_id}
    ensure_store(paths)
    job_id = _job_id(resolved_id, normalized.transcript_sha256)
    queue_path = paths.queue / f"{job_id}.json"
    if queue_path.exists():
        existing_record: dict[str, Any] | None = None
        try:
            loaded_record = json.loads(queue_path.read_text(encoding="utf-8"))
            existing_record = validate_queue_record(paths, queue_path, loaded_record)
            _validate_existing_capture_job(paths, existing_record)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            if not allow_worker or existing_record is None or not _capture_job_is_rebuildable(paths, existing_record):
                raise ValueError("existing capture job is invalid; preserve it for operator recovery") from error
            write_log(paths, job_id, "capture=job-rebuilt-from-source-transcript")
        else:
            return {"status": "exists", "reason": "idempotent", "session_id": resolved_id, "queue_path": str(queue_path)}
    evidence_path = paths.sessions / f"{job_id}-evidence.json"
    suggestions_path = paths.sessions / f"{job_id}-suggestions.md"
    audit_path = paths.sessions / f"{_audit_stamp(normalized.timestamp)}-{job_id}-audit.md"
    captured_at = iso_now()
    actual_cwd = cwd.strip() or normalized.cwd
    atomic_write_json(
        evidence_path,
        {
            "schema_version": 1,
            "runtime": "claude",
            "session_id": resolved_id,
            "transcript_sha256": normalized.transcript_sha256,
            "captured_at": captured_at,
            "project_dir": actual_cwd,
            "messages": [{"role": turn.role, "text": turn.text} for turn in normalized.turns],
            "redactions": normalized.redactions,
        },
    )
    evidence_sha256 = _sha256_file(evidence_path)
    audit_values = {
        "session_id": _sanitize_audit_metadata(resolved_id),
        "evidence_path": _sanitize_audit_metadata(evidence_path),
        "suggestions_path": _sanitize_audit_metadata(suggestions_path),
        "transcript_sha256": _sanitize_audit_metadata(normalized.transcript_sha256),
        "cwd": _sanitize_audit_metadata(actual_cwd),
    }
    atomic_write_text(
        audit_path,
        "\n".join(
            [
                f"# Session Audit — {_audit_stamp(normalized.timestamp)}-{job_id}",
                "processed: false",
                f"**session_id:** {audit_values['session_id']}",
                f"**user_messages:** {normalized.user_messages}",
                f"**normalized_transcript_path:** {audit_values['evidence_path']}",
                f"**suggestions_path:** {audit_values['suggestions_path']}",
                "**source_transcript_format:** claude-code-transcript-v1",
                "**source_runtime:** claude",
                f"**transcript_sha256:** {audit_values['transcript_sha256']}",
                f"**redactions:** {normalized.redactions}",
                f"**cwd:** {audit_values['cwd']}",
                "**skill:**",
                "",
            ]
        ),
    )
    audit_sha256 = _sha256_file(audit_path)
    atomic_write_json(
        queue_path,
        {
            "schema_version": 1,
            "runtime": "claude",
            "job_id": job_id,
            "session_id": resolved_id,
            "transcript_sha256": normalized.transcript_sha256,
            "state": "queued",
            "attempts": 0,
            "created_at": captured_at,
            "updated_at": captured_at,
            "lease_started_at": None,
            "finished_at": None,
            "evidence_path": str(evidence_path),
            "evidence_sha256": evidence_sha256,
            "audit_path": str(audit_path),
            "audit_sha256": audit_sha256,
            "result_path": str(suggestions_path),
            "source_format": "claude-code-transcript-v1",
            "extractor_model": str(config.get("extractor_model") or "").strip(),
            "last_error": None,
            "candidate_count": None,
            "result_sha256": None,
            "manual_retries": 0,
        },
    )
    return {
        "status": "queued",
        "session_id": resolved_id,
        "audit_path": str(audit_path),
        "evidence_path": str(evidence_path),
        "queue_path": str(queue_path),
    }


CAPTURE_REQUEST_FIELDS = {
    "schema_version",
    "request_id",
    "session_id",
    "transcript_path",
    "cwd",
    "agent_id",
    "agent_type",
    "created_at",
    "attempts",
    "last_error",
}


def _capture_request_id(session_id: str, transcript_path: str) -> str:
    material = f"claude-capture\0{session_id}\0{transcript_path}\0schema-1".encode()
    return f"{_safe_id(session_id)[:87]}-{hashlib.sha256(material).hexdigest()[:12]}"


def queue_capture_request(paths: RuntimePaths, payload: dict[str, Any]) -> dict[str, Any]:
    """Spool only native hook metadata; transcript normalization happens detached."""
    session_id = str(payload.get("session_id") or "").strip()
    transcript_value = str(payload.get("transcript_path") or "").strip()
    agent_id = str(payload.get("agent_id") or "").strip()
    agent_type = str(payload.get("agent_type") or "").strip()
    if not session_id or not transcript_value:
        return {"status": "skipped", "reason": "missing-session-metadata"}
    if agent_id:
        return {"status": "skipped", "reason": "subagent", "session_id": session_id}
    if len(session_id) > 1000 or len(transcript_value) > 4096 or len(agent_type) > 200:
        return {"status": "skipped", "reason": "oversized-session-metadata", "session_id": session_id}
    config = load_config(paths)
    if not config.get("enabled"):
        return {"status": "skipped", "reason": "disabled", "session_id": session_id}
    if not config.get("privacy_acknowledged_at"):
        return {"status": "skipped", "reason": "privacy-not-acknowledged", "session_id": session_id}
    transcript = Path(transcript_value).expanduser().resolve()
    if not transcript.is_file():
        return {"status": "skipped", "reason": "transcript-unavailable", "session_id": session_id}
    if paths.capture_inbox.is_symlink():
        raise ValueError("capture inbox must not be a symlink")
    ensure_store(paths)
    request_id = _capture_request_id(session_id, str(transcript))
    request_path = paths.capture_inbox / f"{request_id}.json"
    request = {
        "schema_version": 1,
        "request_id": request_id,
        "session_id": session_id,
        "transcript_path": str(transcript),
        "cwd": str(payload.get("cwd") or "")[:4096],
        "agent_id": "",
        "agent_type": _sanitize_audit_metadata(agent_type, limit=200),
        "created_at": iso_now(),
        "attempts": 0,
        "last_error": None,
    }
    if request_path.is_symlink():
        raise ValueError("capture request must not be a symlink")
    if request_path.exists():
        try:
            existing = _validated_capture_request(
                paths,
                request_path,
                json.loads(request_path.read_text(encoding="utf-8")),
            )
        except (OSError, ValueError, json.JSONDecodeError):
            atomic_write_json(request_path, request)
            write_log(paths, request_id, "capture=request-repaired")
        else:
            if existing["session_id"] == session_id and existing["transcript_path"] == str(transcript):
                return {
                    "status": "exists",
                    "reason": "capture-request-idempotent",
                    "session_id": session_id,
                    "request_path": str(request_path),
                }
    atomic_write_json(request_path, request)
    return {"status": "queued", "session_id": session_id, "request_path": str(request_path)}


def _validated_capture_request(paths: RuntimePaths, path: Path, payload: Any) -> dict[str, Any]:
    if path.parent != paths.capture_inbox or path.is_symlink():
        raise ValueError("capture request path is not state-confined")
    if not isinstance(payload, dict) or set(payload) != CAPTURE_REQUEST_FIELDS:
        raise ValueError("capture request has an invalid contract")
    if payload.get("schema_version") != 1 or _parse_timestamp(payload.get("created_at")) is None:
        raise ValueError("capture request version or timestamp is invalid")
    session_id = payload.get("session_id")
    transcript_value = payload.get("transcript_path")
    if not isinstance(session_id, str) or not session_id or not isinstance(transcript_value, str):
        raise ValueError("capture request session metadata is invalid")
    if len(session_id) > 1000 or len(transcript_value) > 4096:
        raise ValueError("capture request session metadata is oversized")
    if str(Path(transcript_value).expanduser().resolve()) != transcript_value:
        raise ValueError("capture request transcript path is not canonical")
    request_id = _capture_request_id(session_id, transcript_value)
    if payload.get("request_id") != request_id or path.name != f"{request_id}.json":
        raise ValueError("capture request identity mismatch")
    for field in ("cwd", "agent_id", "agent_type"):
        if not isinstance(payload.get(field), str):
            raise ValueError("capture request metadata is invalid")
    if len(payload["cwd"]) > 4096 or payload["agent_id"] or len(payload["agent_type"]) > 200:
        raise ValueError("capture request metadata is not eligible")
    _require_exact_int(payload.get("attempts"), "capture request attempts")
    if payload.get("last_error") is not None and not isinstance(payload.get("last_error"), str):
        raise ValueError("capture request last_error must be null or a string")
    return dict(payload)


def drain_capture_requests(paths: RuntimePaths) -> dict[str, int | str]:
    ensure_store(paths)
    lock = _lock(paths.state, "capture-worker.lock")
    if lock is None:
        return {"status": "locked", "processed": 0, "queued": 0, "skipped": 0, "failed": 0}
    processed = queued = skipped = failed = 0
    try:
        ensure_store(paths)
        max_attempts = max(1, int(load_config(paths).get("max_attempts", 3)))
        for request_path in sorted(paths.capture_inbox.glob("*.json")):
            processed += 1
            validated: dict[str, Any] | None = None
            remove_request = True
            try:
                validated = _validated_capture_request(
                    paths,
                    request_path,
                    json.loads(request_path.read_text(encoding="utf-8")),
                )
                result = capture_session(
                    paths,
                    session_id=validated["session_id"],
                    transcript_path=validated["transcript_path"],
                    cwd=validated["cwd"],
                    agent_id=validated["agent_id"],
                    agent_type=validated["agent_type"],
                    allow_worker=True,
                )
                queued += int(result.get("status") in {"queued", "exists"})
                skipped += int(result.get("status") == "skipped")
            except Exception as error:
                failed += 1
                message = sanitize_error(error)
                write_log(paths, request_path.stem, f"capture=failed error={message}")
                if validated is not None and validated["attempts"] + 1 < max_attempts:
                    retry = dict(validated)
                    retry["attempts"] += 1
                    retry["last_error"] = message
                    atomic_write_json(request_path, retry)
                    remove_request = False
            finally:
                if remove_request and request_path.parent == paths.capture_inbox and not request_path.is_symlink():
                    request_path.unlink(missing_ok=True)
    finally:
        lock.unlink(missing_ok=True)
    return {"status": "complete", "processed": processed, "queued": queued, "skipped": skipped, "failed": failed}


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).astimezone(timezone.utc)


def recover_stale_jobs(paths: RuntimePaths, *, now: datetime | None = None) -> int:
    config = load_config(paths)
    cutoff = (now or utc_now()) - timedelta(seconds=max(1, int(config["processing_lease_seconds"])))
    max_attempts = max(1, int(config.get("max_attempts", 3)))
    recovered = 0
    for queue_path, record in read_queue(paths):
        if record.get("state") != "processing":
            continue
        started = _parse_timestamp(record.get("lease_started_at"))
        if started is not None and started > cutoff:
            continue
        terminal = int(record["attempts"]) >= max_attempts
        updated = dict(record)
        updated.update(
            state="failed" if terminal else "retryable",
            updated_at=iso_now(now),
            lease_started_at=None,
            finished_at=iso_now(now) if terminal else None,
            last_error="stale-processing-lease",
        )
        atomic_write_json(queue_path, updated)
        recovered += 1
    return recovered


def _lock(directory: Path, name: str) -> Path | None:
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("runtime lock directory must be a regular state directory")
    path = directory / name
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            owner_pid = int(payload.get("pid", 0))
            if owner_pid <= 1:
                raise ValueError("invalid lock owner")
            os.kill(owner_pid, 0)
            return None
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            path.unlink(missing_ok=True)
            return _lock(directory, name)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump({"pid": os.getpid(), "created_at": iso_now()}, handle)
    return path


def sanitize_error(error: BaseException | str) -> str:
    expose_message = isinstance(error, (RuntimeError, ValueError)) or (
        isinstance(error, PermissionError) and getattr(error, "filename", None) is None
    )
    value = str(error) if expose_message else type(error).__name__
    value, _ = redact_text_with_count(re.sub(r"[\r\n]+", " ", value))
    return value.strip()[:300] or "unknown-error"


def write_log(paths: RuntimePaths, identifier: str, event: str) -> None:
    ensure_store(paths)
    safe_event = re.sub(r"[^A-Za-z0-9_.:= /-]", "?", event)[:300]
    log_path = paths.logs / f"{_safe_id(identifier)}.log"
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(log_path, flags, 0o600)
    try:
        opened = os.fstat(descriptor)
        current = log_path.lstat()
        if (
            not stat.S_ISREG(opened.st_mode)
            or not stat.S_ISREG(current.st_mode)
            or opened.st_dev != current.st_dev
            or opened.st_ino != current.st_ino
        ):
            raise OSError("runtime log must be a regular state-confined file")
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(f"{iso_now()} {safe_event}\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _extractor_assets(root: Path | None = None) -> tuple[Path, Path]:
    assets = (root or bundle_root()) / "assets"
    return assets / "claude-extractor-prompt.md", assets / "claude-extractor-schema.json"


def resolve_claude_binary(config: dict[str, Any], explicit: str | None = None) -> str | None:
    configured = explicit or str(config.get("claude_binary") or "").strip()
    if configured:
        candidate = Path(configured).expanduser()
        return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
    return shutil.which("claude")


def discover_skill_slugs(cwd: str | Path | None = None, *, claude_home: str | Path | None = None) -> tuple[str, ...]:
    home = Path(claude_home).expanduser() if claude_home else Path.home() / ".claude"
    roots = [home / "skills"]
    if cwd:
        current = Path(cwd).expanduser().resolve()
        roots.extend(parent / ".claude" / "skills" for parent in (current, *current.parents))
    slugs: set[str] = {"pmm-instinct-review"}
    for root in roots:
        for descriptor in root.glob("*/SKILL.md") if root.is_dir() else ():
            try:
                match = re.search(r"(?m)^name:\s*['\"]?([a-z0-9][a-z0-9-]{0,63})", descriptor.read_text(encoding="utf-8")[:8000])
            except OSError:
                continue
            if match:
                slugs.add(match.group(1))
    return tuple(sorted(slugs))


def _derive_source_skill(messages: Iterable[dict[str, Any]], slugs: Iterable[str]) -> str | None:
    joined = "\n".join(str(item.get("text") or "") for item in messages)
    ordered = sorted(set(slugs), key=lambda slug: (-len(slug), slug))
    for slug in ordered:
        if re.search(rf"(?:\$|/){re.escape(slug)}\b", joined, re.IGNORECASE):
            return slug
    for slug in ordered:
        if re.search(rf"(?<![A-Za-z0-9-]){re.escape(slug)}(?![A-Za-z0-9-])", joined, re.IGNORECASE):
            return slug
    return None


def validate_extractor_payload(payload: Any) -> list[dict[str, str]]:
    if not isinstance(payload, dict) or set(payload) != {"candidates"}:
        raise ValueError("extractor output must contain only candidates")
    candidates = payload.get("candidates")
    if not isinstance(candidates, list) or len(candidates) > 5:
        raise ValueError("extractor candidates must be a list of at most five items")
    validated: list[dict[str, str]] = []
    required = {"type", "rule", "evidence", "context", "why_it_matters"}
    for candidate in candidates:
        if not isinstance(candidate, dict) or set(candidate) != required:
            raise ValueError("invalid extractor candidate fields")
        values = tuple(candidate.get(key) for key in ("rule", "evidence", "context", "why_it_matters"))
        if candidate.get("type") not in ALLOWED_TYPES or not all(isinstance(item, str) for item in values):
            raise ValueError("invalid extractor candidate")
        rule, evidence, context, rationale = (" ".join(str(item).split()).strip() for item in values)
        if (
            not rule
            or not rationale
            or len(rule) > 300
            or len(evidence) > 160
            or len(context) > 300
            or len(rationale) > 300
        ):
            raise ValueError("extractor candidate violates length constraints")
        validated.append(
            {
                "type": str(candidate["type"]),
                "rule": rule,
                "evidence": evidence,
                "context": context,
                "why_it_matters": rationale,
            }
        )
    return validated


def extractor_command(
    *,
    claude_binary: str,
    model: str,
    schema: dict[str, Any],
    prompt: str,
) -> list[str]:
    return [
        claude_binary,
        "--bare",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(schema, separators=(",", ":")),
        "--model",
        model,
        "--max-turns",
        "1",
        "--no-session-persistence",
        "--permission-mode",
        "dontAsk",
        "--tools",
        "",
        "--disallowedTools",
        "mcp__*",
    ]


def render_suggestions(session_id: str, candidates: list[dict[str, str]], source_skill: str | None) -> str:
    lines = [
        "---",
        f"# Instinct Suggestions — {_sanitize_audit_metadata(session_id)}",
        f"**generated:** {iso_now()}",
        f"**candidates:** {len(candidates)}",
        f"**skill:** {source_skill or ''}",
        "**source_runtime:** claude",
        "",
    ]
    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"## Candidate {index}",
                f"**type:** {candidate['type']}",
                f"**rule:** {candidate['rule']}",
                f"**evidence:** {candidate['evidence']}",
                f"**context:** {candidate['context']}",
                f"**why it matters:** {candidate['why_it_matters']}",
            ]
        )
        if source_skill:
            lines.append(f"**skill:** {source_skill}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _validated_queue_artifacts(
    paths: RuntimePaths,
    record: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Path]]:
    job_id = record.get("job_id")
    if not isinstance(job_id, str) or _safe_id(job_id) != job_id:
        raise ValueError("queue job identity is invalid")
    queue_path = paths.queue / f"{job_id}.json"
    try:
        stored = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("queue record is unreadable") from error
    if stored != record:
        raise ValueError("queue record changed after validation")
    validated = validate_queue_record(paths, queue_path, record)
    artifacts = _queue_artifact_paths(paths, job_id, Path(validated["audit_path"]).name)
    return validated, artifacts


def _load_validated_evidence(
    paths: RuntimePaths,
    record: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Path]]:
    validated, artifacts = _validated_queue_artifacts(paths, record)
    evidence_path = artifacts["evidence"]
    try:
        evidence_bytes = evidence_path.read_bytes()
        evidence = json.loads(evidence_bytes)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("captured Claude evidence is unreadable") from error
    if hashlib.sha256(evidence_bytes).hexdigest() != validated["evidence_sha256"]:
        raise ValueError("captured Claude evidence digest mismatch")
    expected_fields = {
        "schema_version", "runtime", "session_id", "transcript_sha256", "captured_at",
        "project_dir", "messages", "redactions",
    }
    if not isinstance(evidence, dict) or set(evidence) != expected_fields:
        raise ValueError("captured Claude evidence fields are invalid")
    if type(evidence.get("schema_version")) is not int or evidence.get("schema_version") != 1:
        raise ValueError("captured Claude evidence schema mismatch")
    if evidence.get("runtime") != "claude":
        raise ValueError("captured Claude evidence runtime mismatch")
    if evidence.get("session_id") != validated["session_id"]:
        raise ValueError("captured Claude evidence session mismatch")
    if evidence.get("transcript_sha256") != validated["transcript_sha256"]:
        raise ValueError("captured Claude evidence transcript digest mismatch")
    if _parse_timestamp(evidence.get("captured_at")) is None:
        raise ValueError("captured Claude evidence timestamp is invalid")
    if not isinstance(evidence.get("project_dir"), str):
        raise ValueError("captured Claude evidence project directory is invalid")
    if type(evidence.get("redactions")) is not int or evidence["redactions"] < 0:
        raise ValueError("captured Claude evidence redaction count is invalid")
    messages = evidence.get("messages")
    if not isinstance(messages, list) or any(
        not isinstance(message, dict)
        or set(message) != {"role", "text"}
        or message.get("role") not in {"user", "assistant"}
        or not isinstance(message.get("text"), str)
        for message in messages
    ):
        raise ValueError("captured Claude evidence messages are invalid")
    return evidence, artifacts


def run_extractor_job(
    paths: RuntimePaths,
    record: dict[str, Any],
    *,
    claude_binary: str | None = None,
    root: Path | None = None,
    runner: Any = subprocess.run,
) -> list[dict[str, str]]:
    record, artifacts = _validated_queue_artifacts(paths, record)
    config = load_config(paths)
    model = str(record.get("extractor_model") or config.get("extractor_model") or "").strip()
    if not model:
        raise RuntimeError("configured Claude extractor model is required")
    evidence, _ = _load_validated_evidence(paths, record)
    prompt_path, schema_path = _extractor_assets(root)
    try:
        prompt = prompt_path.read_text(encoding="utf-8")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError("Claude extractor prompt or schema is unavailable") from error
    slugs = discover_skill_slugs(evidence.get("project_dir"))
    resolved = resolve_claude_binary(config, claude_binary)
    if not resolved:
        raise RuntimeError("Claude Code executable is unavailable")
    command = extractor_command(claude_binary=resolved, model=model, schema=schema, prompt=prompt)
    stdin_payload = json.dumps(
        {"untrusted_session_evidence": evidence.get("messages", [])},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    environment = os.environ.copy()
    environment["PMM_INSTINCT_EXTRACTOR"] = "1"
    with tempfile.TemporaryDirectory(prefix="pmm-claude-instinct-") as temporary:
        completed = runner(
            command,
            input=stdin_payload,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=temporary,
            env=environment,
            timeout=int(config.get("extractor_timeout_seconds", 900)),
            check=False,
        )
    if completed.returncode != 0:
        error_text = str(getattr(completed, "stderr", "") or "").lower()
        auth_markers = (
            "authentication",
            "unauthenticated",
            "unauthorized",
            "api key",
            "apikeyhelper",
            "credential",
            "login required",
            "status 401",
        )
        if any(marker in error_text for marker in auth_markers):
            raise RuntimeError(
                "Claude extractor authentication failed in --bare mode; configure "
                "ANTHROPIC_API_KEY or supported Bedrock, Vertex, or Foundry credentials"
            )
        raise RuntimeError(f"Claude extractor exited with status {completed.returncode}")
    try:
        envelope = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError("Claude extractor produced invalid JSON") from error
    payload = envelope.get("structured_output") if isinstance(envelope, dict) else None
    candidates = validate_extractor_payload(payload)
    source_skill = _derive_source_skill(evidence["messages"], slugs)
    atomic_write_text(
        artifacts["result"],
        render_suggestions(str(record["session_id"]), candidates, source_skill),
    )
    return candidates


def _transition_queue(path: Path, record: dict[str, Any], **updates: Any) -> dict[str, Any]:
    changed = dict(record)
    changed.update(updates)
    changed["updated_at"] = iso_now()
    atomic_write_json(path, changed)
    return changed


def drain_extraction_queue(
    paths: RuntimePaths,
    *,
    job_id: str | None = None,
    claude_binary: str | None = None,
    root: Path | None = None,
    runner: Any = subprocess.run,
) -> dict[str, int | str]:
    ensure_store(paths)
    lock = _lock(paths.state, "extraction-worker.lock")
    if lock is None:
        return {"status": "locked", "processed": 0, "completed": 0, "retryable": 0, "failed": 0}
    processed = completed_count = retryable = failed = 0
    try:
        recover_stale_jobs(paths)
        max_attempts = max(1, int(load_config(paths).get("max_attempts", 3)))
        for queue_path, record in read_queue(paths):
            if job_id and str(record.get("job_id")) != job_id:
                continue
            attempts = record["attempts"]
            if record.get("state") not in {"queued", "retryable"}:
                continue
            if attempts >= max_attempts:
                processed += 1
                failed += 1
                exhausted = _transition_queue(
                    queue_path,
                    record,
                    state="failed",
                    lease_started_at=None,
                    finished_at=iso_now(),
                    last_error="maximum extraction attempts exhausted",
                    candidate_count=None,
                    result_sha256=None,
                )
                write_log(paths, str(exhausted["job_id"]), "state=failed error=maximum extraction attempts exhausted")
                continue
            processed += 1
            current = _transition_queue(
                queue_path,
                record,
                state="processing",
                attempts=attempts + 1,
                lease_started_at=iso_now(),
                finished_at=None,
                last_error=None,
                candidate_count=None,
                result_sha256=None,
            )
            try:
                candidates = run_extractor_job(
                    paths,
                    current,
                    claude_binary=claude_binary,
                    root=root,
                    runner=runner,
                )
            except Exception as error:
                message = sanitize_error(error)
                terminal = attempts + 1 >= max_attempts
                state = "failed" if terminal else "retryable"
                failed += int(terminal)
                retryable += int(not terminal)
                _transition_queue(
                    queue_path,
                    current,
                    state=state,
                    lease_started_at=None,
                    finished_at=iso_now() if terminal else None,
                    last_error=message,
                    candidate_count=None,
                    result_sha256=None,
                )
                write_log(paths, str(current.get("job_id")), f"state={state} error={message}")
                continue
            completed_count += 1
            _, artifacts = _validated_queue_artifacts(paths, current)
            _transition_queue(
                queue_path,
                current,
                state="completed",
                lease_started_at=None,
                finished_at=iso_now(),
                last_error=None,
                candidate_count=len(candidates),
                result_sha256=_sha256_file(artifacts["result"]),
            )
            write_log(paths, str(current.get("job_id")), f"state=completed candidates={len(candidates)}")
    finally:
        lock.unlink(missing_ok=True)
    return {
        "status": "complete",
        "processed": processed,
        "completed": completed_count,
        "retryable": retryable,
        "failed": failed,
    }


def retry_failed(paths: RuntimePaths, *, job_id: str | None = None) -> int:
    count = 0
    for queue_path, record in read_queue(paths):
        if record.get("state") != "failed" or (job_id and record.get("job_id") != job_id):
            continue
        _transition_queue(
            queue_path,
            record,
            state="retryable",
            attempts=0,
            lease_started_at=None,
            finished_at=None,
            last_error=None,
            manual_retries=int(record.get("manual_retries", 0)) + 1,
        )
        count += 1
    return count


def _markdown_fields(text: str) -> dict[str, str]:
    return {
        match.group(1).strip().lower(): match.group(2).strip()
        for match in re.finditer(r"^\*\*([^*]+):\*\*[ \t]*(.*)$", text, re.MULTILINE)
    }


def _completed_review_records(paths: RuntimePaths) -> tuple[list[dict[str, Any]], list[str]]:
    """Enumerate review input from completed validated queues, never Markdown paths."""
    records: list[dict[str, Any]] = []
    invalid: list[str] = []
    for queue_path, record in read_queue(paths):
        if record["state"] != "completed":
            continue
        try:
            record, artifacts = _validated_queue_artifacts(paths, record)
            audit_bytes = artifacts["audit"].read_bytes()
            if hashlib.sha256(audit_bytes).hexdigest() != record["audit_sha256"]:
                raise ValueError("audit digest mismatch")
            audit_text = audit_bytes.decode("utf-8")
            if re.search(r"(?m)^processed:\s*true\s*$", audit_text):
                continue
            fields = _markdown_fields(audit_text)
            if fields.get("source_runtime") != "claude":
                raise ValueError("audit runtime mismatch")
            if fields.get("session_id") != _sanitize_audit_metadata(record["session_id"]):
                raise ValueError("audit session mismatch")
            if fields.get("transcript_sha256") != record["transcript_sha256"]:
                raise ValueError("audit transcript digest mismatch")
            result_bytes = artifacts["result"].read_bytes()
            if hashlib.sha256(result_bytes).hexdigest() != record["result_sha256"]:
                raise ValueError("suggestion result digest mismatch")
            evidence, _ = _load_validated_evidence(paths, record)
        except (OSError, UnicodeDecodeError, ValueError):
            invalid.append(str(record.get("job_id") or queue_path.stem))
            continue
        records.append(
            {
                "path": artifacts["audit"],
                "text": audit_text,
                "queue_path": queue_path,
                "queue_record": record,
                "session_id": record["session_id"],
                "cwd": evidence["project_dir"],
                "suggestions_path": artifacts["result"],
                "evidence_path": artifacts["evidence"],
            }
        )
    return records, invalid


def _suggestion_candidates(audit: dict[str, Any]) -> list[dict[str, str]]:
    record = audit["queue_record"]
    path = audit["suggestions_path"]
    try:
        result_bytes = path.read_bytes()
        text = result_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("completed suggestion result is unreadable") from error
    if hashlib.sha256(result_bytes).hexdigest() != record["result_sha256"]:
        raise ValueError("completed suggestion result digest mismatch")
    chunks = re.split(r"(?m)^## Candidate\s+\d+\s*$", text)[1:]
    file_fields = _markdown_fields(text.split("## Candidate", 1)[0])
    if file_fields.get("source_runtime") != "claude":
        raise ValueError("completed suggestion runtime mismatch")
    try:
        declared_count = int(file_fields.get("candidates", ""))
    except ValueError as error:
        raise ValueError("completed suggestion candidate count is invalid") from error
    raw_candidates: list[dict[str, str]] = []
    source_skills: list[str] = []
    for chunk in chunks:
        fields = _markdown_fields(chunk)
        raw_candidates.append(
            {
                "type": fields.get("type", ""),
                "rule": fields.get("rule", ""),
                "evidence": fields.get("evidence", ""),
                "context": fields.get("context", ""),
                "why_it_matters": fields.get("why it matters", ""),
            }
        )
        source_skills.append(fields.get("skill", "") or file_fields.get("skill", ""))
    candidates = validate_extractor_payload({"candidates": raw_candidates})
    if declared_count != len(candidates) or record["candidate_count"] != len(candidates):
        raise ValueError("completed suggestion candidate count mismatch")
    for candidate, source_skill in zip(candidates, source_skills):
        candidate["source_skill"] = source_skill if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", source_skill) else ""
    return candidates


def normalize_rule(rule: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", " ".join(rule.lower().split())).strip()


def _cluster_id(candidate_type: str, rule: str) -> str:
    digest = hashlib.sha256(f"{candidate_type}\0{normalize_rule(rule)}".encode()).hexdigest()[:12]
    return f"{candidate_type}-{digest}"


def _empty_review_ledger() -> dict[str, Any]:
    return {
        "schema_version": REVIEW_LEDGER_SCHEMA_VERSION,
        "cluster_decisions": {},
        "zero_resolutions": [],
    }


def _validated_review_occurrence(payload: Any) -> dict[str, str]:
    expected_fields = {
        "job_id",
        "session_id",
        "transcript_sha256",
        "result_sha256",
        "audit_sha256",
    }
    if not isinstance(payload, dict) or set(payload) != expected_fields:
        raise ValueError("review decision ledger contains an invalid occurrence")
    session_id = payload.get("session_id")
    job_id = payload.get("job_id")
    if not isinstance(session_id, str) or not session_id:
        raise ValueError("review decision ledger contains an invalid session identifier")
    transcript_sha256 = _require_sha256(payload.get("transcript_sha256"), "transcript_sha256")
    if (
        not isinstance(job_id, str)
        or _safe_id(job_id) != job_id
        or _job_id(session_id, transcript_sha256) != job_id
    ):
        raise ValueError("review decision ledger contains an invalid job identifier")
    return {
        "job_id": job_id,
        "session_id": session_id,
        "transcript_sha256": transcript_sha256,
        "result_sha256": _require_sha256(payload.get("result_sha256"), "result_sha256"),
        "audit_sha256": _require_sha256(payload.get("audit_sha256"), "audit_sha256"),
    }


def _review_occurrence_key(occurrence: dict[str, str]) -> tuple[str, str, str, str, str]:
    return (
        occurrence["job_id"],
        occurrence["session_id"],
        occurrence["transcript_sha256"],
        occurrence["result_sha256"],
        occurrence["audit_sha256"],
    )


def _review_occurrence_from_audit(
    audit: dict[str, Any],
    *,
    audit_sha256: str | None = None,
) -> dict[str, str]:
    record = audit["queue_record"]
    return _validated_review_occurrence(
        {
            "job_id": record["job_id"],
            "session_id": record["session_id"],
            "transcript_sha256": record["transcript_sha256"],
            "result_sha256": record["result_sha256"],
            # This is always the pre-processing audit digest. Reconciliation
            # reconstructs that exact digest after `processed` becomes true.
            "audit_sha256": audit_sha256 or record["audit_sha256"],
        }
    )


def _review_ledger(paths: RuntimePaths) -> dict[str, Any]:
    _validate_store_layout(paths)
    path = paths.state / "review-decisions.json"
    if not path.exists():
        return _empty_review_ledger()
    if path.is_symlink():
        raise ValueError("review decision ledger must not be a symlink")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("review decision ledger is unreadable or malformed") from error
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version",
        "cluster_decisions",
        "zero_resolutions",
    }:
        raise ValueError("review decision ledger must use schema version 2")
    if type(payload.get("schema_version")) is not int or payload["schema_version"] != REVIEW_LEDGER_SCHEMA_VERSION:
        raise ValueError("review decision ledger schema version mismatch")
    decisions = payload.get("cluster_decisions")
    zero_resolutions = payload.get("zero_resolutions")
    if not isinstance(decisions, dict) or not isinstance(zero_resolutions, list):
        raise ValueError("review decision ledger contains invalid collections")

    for cluster_id, events in decisions.items():
        if not isinstance(cluster_id, str) or not re.fullmatch(
            rf"(?:{'|'.join(ALLOWED_TYPES)})-[0-9a-f]{{12}}", cluster_id
        ):
            raise ValueError("review decision ledger contains an invalid cluster identifier")
        if not isinstance(events, list) or not events:
            raise ValueError("review decision ledger contains invalid decision events")
        covered_occurrences: set[tuple[str, str, str, str, str]] = set()
        for event in events:
            if not isinstance(event, dict) or set(event) != {
                "decision",
                "decided_at",
                "occurrences",
                "instinct_path",
            }:
                raise ValueError("review decision ledger contains an invalid decision event")
            decision = event.get("decision")
            occurrences = event.get("occurrences")
            instinct_path = event.get("instinct_path")
            if decision not in {"accept", "reject", "edit", "match"}:
                raise ValueError("review decision ledger contains an invalid decision")
            if _parse_timestamp(event.get("decided_at")) is None:
                raise ValueError("review decision ledger contains an invalid timestamp")
            if not isinstance(occurrences, list) or not occurrences:
                raise ValueError("review decision ledger decision has no occurrences")
            for occurrence in occurrences:
                validated = _validated_review_occurrence(occurrence)
                key = _review_occurrence_key(validated)
                if key in covered_occurrences:
                    raise ValueError("review decision ledger covers an occurrence more than once")
                covered_occurrences.add(key)
            if decision == "reject":
                if instinct_path is not None:
                    raise ValueError("rejected review decision cannot claim an instinct")
                continue
            if not isinstance(instinct_path, str) or not instinct_path:
                raise ValueError("accepted review decision must identify its instinct")
            resolved_instinct = Path(instinct_path).expanduser().resolve()
            if (
                str(resolved_instinct) != instinct_path
                or resolved_instinct.parent != paths.instincts.resolve()
                or not re.fullmatch(r"pmm-instinct-\d{4}-\d{2}-\d{2}-\d{3}\.md", resolved_instinct.name)
            ):
                raise ValueError("review decision ledger contains an invalid instinct path")

    covered_zero: set[tuple[str, str, str, str, str]] = set()
    for event in zero_resolutions:
        if not isinstance(event, dict) or set(event) != {"decided_at", "occurrence"}:
            raise ValueError("review decision ledger contains an invalid zero-candidate resolution")
        if _parse_timestamp(event.get("decided_at")) is None:
            raise ValueError("review decision ledger contains an invalid timestamp")
        occurrence = _validated_review_occurrence(event.get("occurrence"))
        key = _review_occurrence_key(occurrence)
        if key in covered_zero:
            raise ValueError("review decision ledger resolves a zero-candidate occurrence more than once")
        covered_zero.add(key)
    return payload


def _cluster_occurrence_keys(
    ledger: dict[str, Any],
    cluster_id: str,
) -> set[tuple[str, str, str, str, str]]:
    return {
        _review_occurrence_key(occurrence)
        for event in ledger["cluster_decisions"].get(cluster_id, [])
        for occurrence in event["occurrences"]
    }


def _zero_occurrence_keys(ledger: dict[str, Any]) -> set[tuple[str, str, str, str, str]]:
    return {
        _review_occurrence_key(event["occurrence"])
        for event in ledger["zero_resolutions"]
    }


def review_backlog(paths: RuntimePaths) -> dict[str, Any]:
    _validate_store_layout(paths)
    ledger = _review_ledger(paths)
    grouped: dict[
        tuple[str, str],
        dict[tuple[str, str, str, str, str], dict[str, Any]],
    ] = {}
    zero: list[str] = []
    zero_occurrences = _zero_occurrence_keys(ledger)
    audits, invalid = _completed_review_records(paths)
    for audit in audits:
        try:
            candidates = _suggestion_candidates(audit)
        except ValueError:
            invalid.append(str(audit["queue_record"]["job_id"]))
            continue
        occurrence = _review_occurrence_from_audit(audit)
        occurrence_key = _review_occurrence_key(occurrence)
        if not candidates:
            if occurrence_key not in zero_occurrences:
                zero.append(str(audit["path"]))
            continue
        for candidate in candidates:
            identifier = _cluster_id(candidate["type"], candidate["rule"])
            if occurrence_key in _cluster_occurrence_keys(ledger, identifier):
                continue
            grouped.setdefault((candidate["type"], normalize_rule(candidate["rule"])), {})[
                occurrence_key
            ] = {
                **candidate,
                "audit_path": audit["path"],
                "session_id": audit["session_id"],
                "cwd": audit["cwd"],
                "occurrence": occurrence,
            }
    weights = {"voice": 5, "workflow": 4, "scope": 3, "correction": 2, "confirmation": 1}
    clusters: list[dict[str, Any]] = []
    for (candidate_type, _), occurrence_items in grouped.items():
        items = list(occurrence_items.values())
        first = items[0]
        sessions = sorted({item["session_id"] for item in items})
        skills = sorted({item["source_skill"] for item in items if item["source_skill"]})
        cwds = sorted({item["cwd"] for item in items if item["cwd"]})
        occurrences = sorted(
            (item["occurrence"] for item in items),
            key=_review_occurrence_key,
        )
        clusters.append(
            {
                "cluster_id": _cluster_id(candidate_type, first["rule"]),
                "type": candidate_type,
                "rule": first["rule"],
                "evidence": first["evidence"],
                "context": first["context"],
                "why_it_matters": first["why_it_matters"],
                "exact_match_state": "exact"
                if _active_matching_instinct(paths, candidate_type, first["rule"])
                else "new",
                "support_count": len(occurrences),
                "session_ids": sessions,
                "job_ids": [item["job_id"] for item in occurrences],
                "occurrences": occurrences,
                "source_skills": skills,
                "source_cwds": cwds,
                "audit_paths": sorted(str(item["audit_path"]) for item in items),
                "priority_score": weights.get(candidate_type, 0) * 100 + len(occurrences) * 10 + len(skills) * 2 + len(cwds),
            }
        )
    clusters.sort(key=lambda item: (-item["priority_score"], -item["support_count"], item["cluster_id"]))
    return {
        "zero_candidate_audits": zero,
        "missing_suggestion_audits": sorted(set(invalid)),
        "clusters": clusters,
        "positive_clusters": len(clusters),
    }


def review_ready_count(paths: RuntimePaths) -> int:
    """Count validated, unprocessed completed sessions ready for human review."""
    backlog = review_backlog(paths)
    positive_jobs = {
        occurrence["job_id"]
        for cluster in backlog["clusters"]
        for occurrence in cluster["occurrences"]
    }
    return len(backlog["zero_candidate_audits"]) + len(positive_jobs)


def _confidence(support: int, *, strong_correction: bool = False, contradicted: bool = False) -> float:
    value = 0.85 if support >= 11 else 0.70 if support >= 6 else 0.50 if support >= 3 else 0.30
    value += 0.05 if strong_correction else 0
    value -= 0.10 if contradicted else 0
    return max(0.0, min(1.0, round(value, 2)))


def _next_instinct_id(paths: RuntimePaths) -> str:
    prefix = f"pmm-instinct-{date.today().isoformat()}-"
    values: list[int] = []
    for path in paths.instincts.glob(f"{prefix}*.md") if paths.instincts.exists() else ():
        try:
            values.append(int(path.stem.rsplit("-", 1)[1]))
        except ValueError:
            continue
    return f"{prefix}{max(values, default=0) + 1:03d}"


def _write_instinct(
    paths: RuntimePaths,
    cluster: dict[str, Any],
    *,
    rule: str,
    rationale: str,
    strong_correction: bool,
    contradicted: bool,
) -> Path:
    identifier = _next_instinct_id(paths)
    skills = list(cluster["source_skills"])
    metadata = {
        "id": identifier,
        "type": cluster["type"],
        "confidence": _confidence(cluster["support_count"], strong_correction=strong_correction, contradicted=contradicted),
        "created": date.today().isoformat(),
        "last_seen": date.today().isoformat(),
        "seen_count": cluster["support_count"],
        "status": "active",
        "source_skill": skills[0] if len(skills) == 1 else "",
        "source_skills": skills,
        "source_runtime": "claude",
        "source_transcript_format": "claude-code-transcript-v1",
        "source_cwds": list(cluster["source_cwds"]),
        "strong_correction": strong_correction,
        "contradicted": contradicted,
        "suggested_destination": "skill" if skills else "global",
        "promotion_outcome": "",
        "promoted_to": [],
    }
    body = f"{rule}\n\n**Evidence:** {cluster['evidence']}\n\n**Why it matters:** {rationale}"
    ensure_store(paths)
    return atomic_write_text(paths.instincts / f"{identifier}.md", _serialize_frontmatter(metadata, body))


def _active_matching_instinct(paths: RuntimePaths, candidate_type: str, rule: str) -> tuple[Path, dict[str, Any], str] | None:
    for path in paths.instincts.glob("pmm-instinct-*.md") if paths.instincts.exists() else ():
        if path.is_symlink() or not path.is_file():
            continue
        try:
            metadata, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        existing_rule, _ = _rule_and_rationale(body)
        if metadata.get("status") == "active" and metadata.get("type") == candidate_type and normalize_rule(existing_rule) == normalize_rule(rule):
            return path, metadata, body
    return None


def _mark_audit_processed(paths: RuntimePaths, audit: dict[str, Any]) -> None:
    record, artifacts = _validated_queue_artifacts(paths, audit["queue_record"])
    text = audit["text"]
    if re.search(r"(?m)^processed:\s*(?:true|false)\s*$", text):
        text = re.sub(r"(?m)^processed:\s*(?:true|false)\s*$", "processed: true", text, count=1)
    else:
        text = "processed: true\n" + text
    atomic_write_text(artifacts["audit"], text)
    _transition_queue(
        artifacts["queue"],
        record,
        audit_sha256=_sha256_file(artifacts["audit"]),
    )
    artifacts["evidence"].unlink(missing_ok=True)


def _resolve_completed_audits(paths: RuntimePaths, ledger: dict[str, Any]) -> list[str]:
    completed: list[str] = []
    audits, _ = _completed_review_records(paths)
    for audit in audits:
        try:
            candidates = _suggestion_candidates(audit)
        except ValueError:
            continue
        if not candidates:
            continue
        occurrence_key = _review_occurrence_key(_review_occurrence_from_audit(audit))
        identifiers = {_cluster_id(item["type"], item["rule"]) for item in candidates}
        if all(occurrence_key in _cluster_occurrence_keys(ledger, identifier) for identifier in identifiers):
            try:
                _mark_audit_processed(paths, audit)
            except OSError as error:
                write_log(paths, str(audit["queue_record"]["job_id"]), f"review=cleanup-pending error={sanitize_error(error)}")
            else:
                completed.append(audit["session_id"])
    return completed


def _resolve_zero_candidate_audits(paths: RuntimePaths, ledger: dict[str, Any]) -> list[str]:
    completed: list[str] = []
    authorized = _zero_occurrence_keys(ledger)
    audits, _ = _completed_review_records(paths)
    for audit in audits:
        try:
            candidates = _suggestion_candidates(audit)
        except ValueError:
            continue
        occurrence_key = _review_occurrence_key(_review_occurrence_from_audit(audit))
        if candidates or occurrence_key not in authorized:
            continue
        try:
            _mark_audit_processed(paths, audit)
        except OSError as error:
            write_log(paths, str(audit["queue_record"]["job_id"]), f"review=cleanup-pending error={sanitize_error(error)}")
        else:
            completed.append(audit["session_id"])
    return completed


def reconcile_review_finalizations(paths: RuntimePaths) -> dict[str, int | str]:
    """Finish only cleanup already authorized by recorded human review decisions."""
    ensure_store(paths)
    transaction_lock = _lock(paths.state, "review-transaction.lock")
    if transaction_lock is None:
        return {"status": "locked", "recovered": 0, "finalized": 0, "cleaned": 0}
    recovered = cleaned = 0
    try:
        ledger = _review_ledger(paths)
        for queue_path, record in read_queue(paths):
            if record["state"] != "completed":
                continue
            try:
                record, artifacts = _validated_queue_artifacts(paths, record)
                audit_bytes = artifacts["audit"].read_bytes()
                audit_text = audit_bytes.decode("utf-8")
                fields = _markdown_fields(audit_text)
                if (
                    fields.get("source_runtime") != "claude"
                    or fields.get("session_id") != _sanitize_audit_metadata(record["session_id"])
                    or fields.get("transcript_sha256") != record["transcript_sha256"]
                ):
                    continue
                result_bytes = artifacts["result"].read_bytes()
                if hashlib.sha256(result_bytes).hexdigest() != record["result_sha256"]:
                    continue
                audit_sha256 = hashlib.sha256(audit_bytes).hexdigest()
                processed = bool(re.search(r"(?m)^processed:\s*true\s*$", audit_text))
                if not processed:
                    continue
                prior_text = re.sub(
                    r"(?m)^processed:\s*true\s*$",
                    "processed: false",
                    audit_text,
                    count=1,
                )
                if prior_text == audit_text:
                    continue
                review_audit_sha256 = sha256_text(prior_text)
                audit = {
                    "queue_record": record,
                    "suggestions_path": artifacts["result"],
                }
                candidates = _suggestion_candidates(audit)
                occurrence_key = _review_occurrence_key(
                    _review_occurrence_from_audit(
                        audit,
                        audit_sha256=review_audit_sha256,
                    )
                )
                if candidates:
                    identifiers = {_cluster_id(item["type"], item["rule"]) for item in candidates}
                    authorized = all(
                        occurrence_key in _cluster_occurrence_keys(ledger, identifier)
                        for identifier in identifiers
                    )
                else:
                    authorized = occurrence_key in _zero_occurrence_keys(ledger)
                if not authorized:
                    continue
                if audit_sha256 != record["audit_sha256"]:
                    if (
                        review_audit_sha256 != record["audit_sha256"]
                        or not artifacts["evidence"].exists()
                    ):
                        continue
                    _load_validated_evidence(paths, record)
                    record = _transition_queue(queue_path, record, audit_sha256=audit_sha256)
                    recovered += 1
                if artifacts["evidence"].exists():
                    _load_validated_evidence(paths, record)
                    artifacts["evidence"].unlink()
                    cleaned += 1
            except (OSError, UnicodeDecodeError, ValueError):
                continue
        finalized = len(_resolve_completed_audits(paths, ledger))
        finalized += len(_resolve_zero_candidate_audits(paths, ledger))
        return {
            "status": "complete",
            "recovered": recovered,
            "finalized": finalized,
            "cleaned": cleaned,
        }
    finally:
        transaction_lock.unlink(missing_ok=True)


def review_cluster(
    paths: RuntimePaths,
    cluster_id: str,
    decision: str,
    *,
    confirm: bool = False,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
    strong_correction: bool = False,
    contradicted: bool = False,
) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("review decisions require --confirm")
    if decision not in {"accept", "reject", "edit", "match"}:
        raise ValueError("decision must be accept, reject, edit, or match")
    ensure_store(paths)
    transaction_lock = _lock(paths.state, "review-transaction.lock")
    if transaction_lock is None:
        raise RuntimeError("another review transaction is already running")
    try:
        cluster = next((item for item in review_backlog(paths)["clusters"] if item["cluster_id"] == cluster_id), None)
        if cluster is None:
            raise ValueError(f"cluster not found: {cluster_id}")
        rule = (edited_rule or cluster["rule"]).strip()
        rationale = (edited_rationale or cluster["why_it_matters"]).strip()
        if decision == "edit" and not edited_rule:
            raise ValueError("edit requires --edited-rule")
        if not rule or not rationale or len(rationale) > 300:
            raise ValueError("approved rule and rationale are required")
        instinct_path: Path | None = None
        if decision in {"accept", "edit"}:
            if _active_matching_instinct(paths, cluster["type"], rule):
                raise ValueError("an exact active instinct already exists; use match")
            instinct_path = _write_instinct(
                paths,
                cluster,
                rule=rule,
                rationale=rationale,
                strong_correction=strong_correction,
                contradicted=contradicted,
            )
        elif decision == "match":
            match = _active_matching_instinct(paths, cluster["type"], rule)
            if match is None:
                raise ValueError("no exact active instinct exists for match")
            instinct_path, metadata, body = match
            seen = int(metadata.get("seen_count", 1)) + int(cluster["support_count"])
            metadata["seen_count"] = seen
            metadata["last_seen"] = date.today().isoformat()
            metadata["confidence"] = _confidence(
                seen,
                strong_correction=bool(metadata.get("strong_correction")) or strong_correction,
                contradicted=bool(metadata.get("contradicted")) or contradicted,
            )
            atomic_write_text(instinct_path, _serialize_frontmatter(metadata, body))
        ledger = _review_ledger(paths)
        ledger["cluster_decisions"].setdefault(cluster_id, []).append({
            "decision": decision,
            "decided_at": iso_now(),
            "occurrences": [dict(item) for item in cluster["occurrences"]],
            "instinct_path": str(instinct_path) if instinct_path else None,
        })
        atomic_write_json(paths.state / "review-decisions.json", ledger)
        completed = _resolve_completed_audits(paths, ledger)
        return {
            "cluster_id": cluster_id,
            "decision": decision,
            "instinct_path": str(instinct_path) if instinct_path else None,
            "processed_sessions": completed,
        }
    finally:
        transaction_lock.unlink(missing_ok=True)


def resolve_zero_candidates(paths: RuntimePaths, *, confirm: bool = False) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("zero-candidate resolution requires --confirm")
    ensure_store(paths)
    transaction_lock = _lock(paths.state, "review-transaction.lock")
    if transaction_lock is None:
        raise RuntimeError("another review transaction is already running")
    try:
        ledger = _review_ledger(paths)
        authorized = _zero_occurrence_keys(ledger)
        added = False
        audits, _ = _completed_review_records(paths)
        for audit in audits:
            try:
                candidates = _suggestion_candidates(audit)
            except ValueError:
                continue
            if candidates == []:
                occurrence = _review_occurrence_from_audit(audit)
                occurrence_key = _review_occurrence_key(occurrence)
                if occurrence_key not in authorized:
                    ledger["zero_resolutions"].append(
                        {"decided_at": iso_now(), "occurrence": occurrence}
                    )
                    authorized.add(occurrence_key)
                    added = True
        if added:
            atomic_write_json(paths.state / "review-decisions.json", ledger)
        resolved = _resolve_zero_candidate_audits(paths, ledger)
        return {"resolved": resolved, "count": len(resolved)}
    finally:
        transaction_lock.unlink(missing_ok=True)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("instinct file is missing frontmatter")
    metadata: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        try:
            metadata[key.strip()] = json.loads(value.strip())
        except json.JSONDecodeError:
            metadata[key.strip()] = value.strip()
    return metadata, match.group(2).strip()


def _serialize_frontmatter(metadata: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.extend(["---", "", body.strip(), ""])
    return "\n".join(lines)


def _load_instinct(
    paths: RuntimePaths,
    instinct_id: str,
    *,
    eligible_statuses: tuple[str, ...] = ("active",),
) -> tuple[Path, dict[str, Any], str]:
    _validate_store_layout(paths)
    path = paths.instincts / f"{_safe_id(instinct_id)}.md"
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"instinct not found: {instinct_id}")
    metadata, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
    if str(metadata.get("id") or path.stem) != instinct_id:
        raise ValueError("instinct identifier does not match its filename")
    confidence = metadata.get("confidence")
    if (
        type(confidence) not in (int, float)
        or not math.isfinite(float(confidence))
        or not 0.0 <= float(confidence) <= 1.0
    ):
        raise ValueError("instinct confidence must be a finite number from 0 to 1")
    if str(metadata.get("status") or "") not in eligible_statuses or float(confidence) < 0.5:
        raise ValueError("instinct status is not eligible or confidence is below 0.5")
    return path, metadata, body


def _rule_and_rationale(body: str) -> tuple[str, str]:
    rule = body.split("\n\n", 1)[0].strip()
    match = re.search(r"(?m)^\*\*Why it matters:\*\*\s*(.+)$", body)
    rationale = match.group(1).strip() if match else "Without this rule, the evidence-backed correction could recur."
    return rule, rationale


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return sha256_text(path.read_text(encoding="utf-8") if path.exists() else "")


def _render_guidance_update(existing: str, insertion: str) -> str:
    content = existing.rstrip() or "# Instructions"
    lines = content.splitlines()
    try:
        heading = lines.index(PROMOTED_GUIDANCE_HEADING)
    except ValueError:
        return f"{content}\n\n{PROMOTED_GUIDANCE_HEADING}\n\n{insertion}\n"
    section_end = next(
        (index for index in range(heading + 1, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    normalized = re.sub(r"[^a-z0-9]+", " ", insertion.removeprefix("- ").lower()).strip()
    existing_rules = {
        re.sub(r"[^a-z0-9]+", " ", match.group(1).lower()).strip()
        for line in lines[heading + 1 : section_end]
        if (match := re.match(r"^\s*[-*+]\s+(.+?)\s*$", line))
    }
    if normalized and normalized in existing_rules:
        return existing
    updated = lines[:section_end]
    if updated and updated[-1] != "":
        updated.append("")
    updated.extend([insertion, ""])
    updated.extend(lines[section_end:])
    return "\n".join(updated).rstrip() + "\n"


def _canonical_digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


PROMOTION_ACTION_FIELDS = {
    "schema_version",
    "instinct_id",
    "source_guidance_sha256",
    "destination_class",
    "delivery",
    "target_path",
    "target_sha256",
    "rule",
    "why_it_matters",
    "section",
    "insertion",
    "resulting_text",
    "resulting_sha256",
    "duplicate",
    "previewed_at",
}
PROMOTION_PREVIEW_FIELDS = PROMOTION_ACTION_FIELDS | {"preview_digest", "confirmation_required"}
PROMOTION_RECEIPT_FIELDS = {
    "schema_version",
    "preview_digest",
    "approved_at",
    "approved_action",
    "receipt_digest",
}


def _validated_saved_promotion_preview(
    paths: RuntimePaths,
    preview_digest: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if SHA256_RE.fullmatch(preview_digest) is None:
        raise ValueError("promotion preview digest must be a lowercase SHA-256 value")
    preview_path = paths.previews / f"{preview_digest}.json"
    if preview_path.is_symlink() or not preview_path.is_file():
        raise ValueError("saved promotion preview is missing or not a regular file")
    try:
        preview = json.loads(preview_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError("saved promotion preview is unreadable or malformed") from error
    if (
        not isinstance(preview, dict)
        or set(preview) != PROMOTION_PREVIEW_FIELDS
        or preview.get("preview_digest") != preview_digest
        or preview.get("confirmation_required") is not True
    ):
        raise ValueError("saved promotion preview has an invalid contract")
    action = {
        key: value
        for key, value in preview.items()
        if key not in {"preview_digest", "confirmation_required"}
    }
    if _canonical_digest(action) != preview_digest:
        raise ValueError("saved promotion preview digest is invalid")
    return preview, action


def _validate_promotion_destination(target: Path, destination_class: str, delivery: str) -> None:
    if destination_class == "global":
        if target != (Path.home() / ".claude" / "CLAUDE.md").resolve() or delivery != "local":
            raise ValueError("global Claude promotion requires local delivery to ~/.claude/CLAUDE.md")
        return
    if destination_class == "project":
        if target.name != "CLAUDE.md" or delivery != "local":
            raise ValueError("project Claude promotion requires local delivery to a CLAUDE.md file")
        return
    if destination_class == "skill":
        if delivery != "review" or not target.name.startswith(("RUN-", "REF-")) or target.suffix != ".md":
            raise ValueError("skill promotion requires review delivery to an exact governed RUN or REF document")
        return
    if delivery != "review" or not target.name.startswith("STD-") or target.suffix != ".md":
        raise ValueError("standard promotion requires review delivery to an exact governed STD document")


def _validate_promotion_action(
    paths: RuntimePaths,
    action: Any,
    preview_digest: str,
    *,
    allow_already_applied: bool = False,
) -> tuple[dict[str, Any], Path]:
    if not isinstance(action, dict) or set(action) != PROMOTION_ACTION_FIELDS:
        raise PermissionError("approved promotion action has an invalid contract")
    if not SHA256_RE.fullmatch(preview_digest) or _canonical_digest(action) != preview_digest:
        raise PermissionError("approved promotion action does not match its preview digest")
    try:
        _, saved_action = _validated_saved_promotion_preview(paths, preview_digest)
    except ValueError as error:
        raise PermissionError("approved promotion preview is missing or unreadable") from error
    if saved_action != action or _canonical_digest(saved_action) != preview_digest:
        raise PermissionError("approved promotion action does not match the saved preview")
    if action.get("schema_version") != 1 or action.get("section") != PROMOTED_GUIDANCE_HEADING:
        raise PermissionError("approved promotion action has invalid version or section metadata")
    target_value = action.get("target_path")
    if not isinstance(target_value, str) or not target_value:
        raise PermissionError("approved promotion target is invalid")
    target = Path(target_value).expanduser().resolve()
    if str(target) != target_value:
        raise PermissionError("approved promotion target is not canonical")
    root = bundle_root().resolve()
    if target == root or root in target.parents:
        raise PermissionError("approved promotion cannot modify the installed bundle")
    if target == paths.state_root or paths.state_root in target.parents:
        raise PermissionError("approved promotion target cannot be inside the runtime state store")
    if "plugins/cache" in target.as_posix():
        raise PermissionError("approved promotion cannot modify a plugin cache")
    destination_class = action.get("destination_class")
    delivery = action.get("delivery")
    if not isinstance(destination_class, str) or not isinstance(delivery, str):
        raise PermissionError("approved promotion destination metadata is invalid")
    try:
        _validate_promotion_destination(target, destination_class, delivery)
    except ValueError as error:
        raise PermissionError(str(error)) from error
    rule = action.get("rule")
    rationale = action.get("why_it_matters")
    insertion = action.get("insertion")
    resulting_text = action.get("resulting_text")
    if (
        not isinstance(rule, str)
        or not rule.strip()
        or not isinstance(rationale, str)
        or not rationale.strip()
        or len(rationale) > 300
        or insertion != f"- {rule}"
        or not isinstance(resulting_text, str)
    ):
        raise PermissionError("approved promotion content is invalid")
    existing = target.read_text(encoding="utf-8") if target.exists() else ""
    existing_sha256 = sha256_text(existing)
    already_applied = bool(
        allow_already_applied
        and delivery == "local"
        and action.get("duplicate") is False
        and existing_sha256 == action.get("resulting_sha256")
    )
    duplicate_already_covered = bool(
        allow_already_applied
        and delivery == "local"
        and action.get("duplicate") is True
        and existing_sha256 == action.get("target_sha256") == action.get("resulting_sha256")
    )
    if existing_sha256 != action.get("target_sha256") and not already_applied:
        raise PermissionError("target changed after approval")
    expected_result = resulting_text if already_applied else _render_guidance_update(existing, insertion)
    if expected_result != resulting_text or sha256_text(resulting_text) != action.get("resulting_sha256"):
        raise PermissionError("approved promotion result is inconsistent")
    expected_duplicate = False if already_applied else resulting_text == existing
    if action.get("duplicate") is not expected_duplicate:
        raise PermissionError("approved promotion duplicate state is inconsistent")
    eligible_statuses = (
        ("active", "promoted", "covered")
        if already_applied or duplicate_already_covered
        else ("active",)
    )
    _, _, instinct_body = _load_instinct(
        paths,
        str(action.get("instinct_id") or ""),
        eligible_statuses=eligible_statuses,
    )
    current_rule, current_rationale = _rule_and_rationale(instinct_body)
    current_source_digest = _canonical_digest(
        {"rule": current_rule, "why_it_matters": current_rationale}
    )
    if action.get("source_guidance_sha256") != current_source_digest:
        raise PermissionError("source instinct changed after preview")
    return action, target


def create_promotion_preview(
    paths: RuntimePaths,
    *,
    instinct_id: str,
    target: str | Path,
    destination_class: str,
    delivery: str,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
) -> dict[str, Any]:
    _validate_store_layout(paths)
    if destination_class not in {"global", "project", "skill", "standard"}:
        raise ValueError("destination class must be global, project, skill, or standard")
    if delivery not in {"local", "review"}:
        raise ValueError("delivery must be local or review")
    _, _, body = _load_instinct(paths, instinct_id)
    original_rule, original_rationale = _rule_and_rationale(body)
    rule = (edited_rule or original_rule).strip()
    rationale = (edited_rationale or original_rationale).strip()
    if not rule or not rationale or len(rationale) > 300:
        raise ValueError("promotion rule and a rationale of at most 300 characters are required")
    target_path = Path(target).expanduser().resolve()
    root = bundle_root().resolve()
    if target_path == root or root in target_path.parents:
        raise ValueError("promotion cannot modify the installed bundle")
    if paths.state_root == target_path or paths.state_root in target_path.parents:
        raise ValueError("promotion target cannot be inside the runtime state store")
    if "plugins/cache" in target_path.as_posix():
        raise ValueError("promotion cannot modify a plugin cache")
    _validate_promotion_destination(target_path, destination_class, delivery)
    existing = target_path.read_text(encoding="utf-8") if target_path.exists() else ""
    insertion = f"- {rule}"
    resulting = _render_guidance_update(existing, insertion)
    payload = {
        "schema_version": 1,
        "instinct_id": instinct_id,
        "source_guidance_sha256": _canonical_digest(
            {"rule": original_rule, "why_it_matters": original_rationale}
        ),
        "destination_class": destination_class,
        "delivery": delivery,
        "target_path": str(target_path),
        "target_sha256": sha256_text(existing),
        "rule": rule,
        "why_it_matters": rationale,
        "section": PROMOTED_GUIDANCE_HEADING,
        "insertion": insertion,
        "resulting_text": resulting,
        "resulting_sha256": sha256_text(resulting),
        "duplicate": resulting == existing,
        "previewed_at": iso_now(),
    }
    digest = _canonical_digest(payload)
    preview = {**payload, "preview_digest": digest, "confirmation_required": True}
    ensure_store(paths)
    atomic_write_json(paths.previews / f"{digest}.json", preview)
    return preview


def approve_promotion(paths: RuntimePaths, preview_digest: str, *, confirm: bool = False) -> dict[str, Any]:
    _validate_store_layout(paths)
    if not confirm:
        raise PermissionError("promotion approval requires --confirm after reviewing the exact preview")
    if not SHA256_RE.fullmatch(preview_digest):
        raise ValueError("promotion preview digest must be a lowercase SHA-256 value")
    try:
        _, unsigned = _validated_saved_promotion_preview(paths, preview_digest)
    except ValueError as error:
        raise ValueError("matching promotion preview was not found") from error
    ensure_store(paths)
    transaction_lock = _lock(paths.state, "promotion-approval.lock")
    if transaction_lock is None:
        raise RuntimeError("another promotion approval transaction is already running")
    try:
        for receipt_path in sorted(paths.receipts.glob("*.json")):
            try:
                existing = _validated_promotion_receipt(paths, receipt_path)
            except (OSError, PermissionError, ValueError, json.JSONDecodeError):
                continue
            if existing["preview_digest"] == preview_digest and existing["approved_action"] == unsigned:
                return {**existing, "receipt_path": str(receipt_path)}
        try:
            _validate_promotion_action(paths, unsigned, preview_digest)
        except PermissionError as error:
            if str(error) == "target changed after approval":
                raise PermissionError("promotion target changed after preview; create and approve a new preview") from error
            raise
        receipt_payload = {
            "schema_version": 1,
            "preview_digest": preview_digest,
            "approved_at": iso_now(),
            "approved_action": unsigned,
        }
        receipt_digest = _canonical_digest(receipt_payload)
        receipt = {**receipt_payload, "receipt_digest": receipt_digest}
        receipt_path = paths.receipts / f"{receipt_digest}.json"
        if not receipt_path.exists():
            atomic_write_json(receipt_path, receipt)
        return {**receipt, "receipt_path": str(receipt_path)}
    finally:
        transaction_lock.unlink(missing_ok=True)


def _validated_promotion_receipt(paths: RuntimePaths, receipt_path: Path) -> dict[str, Any]:
    if receipt_path.parent != paths.receipts or receipt_path.is_symlink():
        raise PermissionError("promotion receipt path is not state-confined")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(receipt, dict) or set(receipt) != PROMOTION_RECEIPT_FIELDS:
        raise PermissionError("promotion receipt has an invalid contract")
    receipt_digest = str(receipt.get("receipt_digest") or "")
    if not SHA256_RE.fullmatch(receipt_digest) or receipt_path.stem != receipt_digest:
        raise PermissionError("receipt filename does not match its digest")
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    action = receipt.get("approved_action")
    preview_digest = receipt.get("preview_digest")
    if (
        receipt.get("schema_version") != 1
        or _parse_timestamp(receipt.get("approved_at")) is None
        or _canonical_digest(unsigned) != receipt_digest
        or not isinstance(preview_digest, str)
        or SHA256_RE.fullmatch(preview_digest) is None
        or not isinstance(action, dict)
        or set(action) != PROMOTION_ACTION_FIELDS
        or _canonical_digest(action) != preview_digest
    ):
        raise PermissionError("receipt digest is invalid")
    return receipt


def _mark_instinct_promoted(paths: RuntimePaths, action: dict[str, Any], outcome: str) -> None:
    path, metadata, body = _load_instinct(
        paths,
        str(action["instinct_id"]),
        eligible_statuses=("active", outcome),
    )
    promoted = metadata.get("promoted_to") or []
    if isinstance(promoted, str):
        promoted = [promoted] if promoted else []
    promoted.append(f"{action['target_path']} § {action['section']}")
    metadata["promoted_to"] = sorted(set(str(item) for item in promoted))
    metadata["status"] = outcome
    metadata["promotion_outcome"] = outcome
    atomic_write_text(path, _serialize_frontmatter(metadata, body))


def _review_changeset(target: Path, current: str, resulting_text: str) -> str:
    return "".join(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            resulting_text.splitlines(keepends=True),
            fromfile=str(target),
            tofile=str(target),
            n=0,
        )
    )


def execute_promotion_receipts(paths: RuntimePaths) -> dict[str, int | str]:
    ensure_store(paths)
    lock = _lock(paths.state, "promotion-worker.lock")
    if lock is None:
        return {"status": "locked", "processed": 0, "applied": 0, "awaiting_review": 0, "failed": 0}
    processed = applied = awaiting_review = failed = 0
    try:
        ensure_store(paths)
        for receipt_path in sorted(paths.receipts.glob("*.json")):
            action: dict[str, Any] | None = None
            target: Path | None = None
            try:
                receipt = _validated_promotion_receipt(paths, receipt_path)
                receipt_digest = receipt["receipt_digest"]
                action = receipt["approved_action"]
                if _promotion_outcome_status(
                    paths.outcomes / f"{receipt_digest}.json",
                    receipt_digest,
                    action=action,
                    paths=paths,
                ) is not None:
                    continue
                action, target = _validate_promotion_action(
                    paths,
                    action,
                    str(receipt.get("preview_digest") or ""),
                    allow_already_applied=True,
                )
                processed += 1
                if action.get("delivery") == "review":
                    current = target.read_text(encoding="utf-8") if target.exists() else ""
                    patch = _review_changeset(target, current, str(action["resulting_text"]))
                    patch_path = paths.changesets / f"{receipt_digest}.patch"
                    atomic_write_text(patch_path, patch)
                    outcome = {
                        "schema_version": 1,
                        "receipt_digest": receipt_digest,
                        "status": "awaiting_review",
                        "created_at": iso_now(),
                        "changeset_path": str(patch_path),
                        "changeset_sha256": _sha256_file(patch_path),
                        "target_path": str(target),
                    }
                    awaiting_review += 1
                else:
                    terminal = "covered" if action.get("duplicate") else "promoted"
                    target_already_matches = file_digest(target) == action.get("resulting_sha256")
                    if not action.get("duplicate") and not target_already_matches:
                        target_mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o600
                        atomic_write_text(target, str(action["resulting_text"]), mode=target_mode)
                        if file_digest(target) != action.get("resulting_sha256"):
                            raise OSError("post-write digest verification failed")
                    outcome = {
                        "schema_version": 1,
                        "receipt_digest": receipt_digest,
                        "status": terminal,
                        "completed_at": iso_now(),
                        "target_path": str(target),
                        "resulting_sha256": action.get("resulting_sha256"),
                    }
                    try:
                        _mark_instinct_promoted(paths, action, terminal)
                    except Exception as bookkeeping_error:
                        outcome["bookkeeping_warning"] = sanitize_error(bookkeeping_error)
                    applied += 1
                atomic_write_json(paths.outcomes / f"{receipt_digest}.json", outcome)
            except Exception as error:
                failed += 1
                identifier = receipt_path.stem
                if (
                    isinstance(action, dict)
                    and target is not None
                    and action.get("delivery") == "local"
                    and file_digest(target) == action.get("resulting_sha256")
                ):
                    failed -= 1
                    write_log(paths, identifier, "promotion=outcome-pending-recovery")
                    continue
                atomic_write_json(
                    paths.outcomes / f"{identifier}.json",
                    {
                        "schema_version": 1,
                        "receipt_digest": identifier,
                        "status": "failed",
                        "failed_at": iso_now(),
                        "error": sanitize_error(error),
                    },
                )
    finally:
        lock.unlink(missing_ok=True)
    return {
        "status": "complete",
        "processed": processed,
        "applied": applied,
        "awaiting_review": awaiting_review,
        "failed": failed,
    }


def _promotion_outcome_status(
    path: Path,
    receipt_key: str,
    *,
    action: dict[str, Any],
    paths: RuntimePaths,
) -> str | None:
    if not SHA256_RE.fullmatch(receipt_key) or path.is_symlink() or path.stem != receipt_key:
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        return None
    if payload.get("receipt_digest") != receipt_key:
        return None
    state = payload.get("status")
    if state in {"promoted", "covered"}:
        required = {"completed_at", "target_path", "resulting_sha256"}
    elif state == "awaiting_review":
        required = {"created_at", "changeset_path", "changeset_sha256", "target_path"}
    elif state == "failed":
        required = {"failed_at", "error"}
    else:
        return None
    if not required.issubset(payload) or not all(
        isinstance(payload[key], str) and payload[key] for key in required
    ):
        return None
    if state in {"promoted", "covered"}:
        expected_state = "covered" if action.get("duplicate") else "promoted"
        if (
            action.get("delivery") != "local"
            or state != expected_state
            or payload["target_path"] != action.get("target_path")
            or payload["resulting_sha256"] != action.get("resulting_sha256")
            or SHA256_RE.fullmatch(payload["resulting_sha256"]) is None
            or _parse_timestamp(payload["completed_at"]) is None
        ):
            return None
    elif state == "awaiting_review":
        expected_changeset = paths.changesets / f"{receipt_key}.patch"
        target_value = action.get("target_path")
        if not isinstance(target_value, str):
            return None
        target = Path(target_value).expanduser().resolve()
        if str(target) != target_value or target.is_symlink():
            return None
        try:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            patch_text = expected_changeset.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None
        expected_patch = _review_changeset(target, current, str(action.get("resulting_text") or ""))
        if (
            action.get("delivery") != "review"
            or payload["target_path"] != action.get("target_path")
            or payload["changeset_path"] != str(expected_changeset)
            or SHA256_RE.fullmatch(payload["changeset_sha256"]) is None
            or not expected_changeset.is_file()
            or expected_changeset.is_symlink()
            or _sha256_file(expected_changeset) != payload["changeset_sha256"]
            or sha256_text(current) != action.get("target_sha256")
            or patch_text != expected_patch
            or _parse_timestamp(payload["created_at"]) is None
        ):
            return None
    elif _parse_timestamp(payload["failed_at"]) is None:
        return None
    return str(state)


def promotion_counts(paths: RuntimePaths) -> dict[str, int]:
    _validate_store_layout(paths)
    receipt_paths = (
        [
            path
            for path in sorted(paths.receipts.glob("*.json"))
            if path.is_file() and not path.is_symlink()
        ]
        if paths.receipts.exists() and not paths.receipts.is_symlink()
        else []
    )
    statuses: dict[str, int] = {
        "approved": 0,
        "pending_execution": 0,
        "promoted": 0,
        "covered": 0,
        "awaiting_review": 0,
        "failed": 0,
        "invalid": 0,
    }
    for receipt_path in receipt_paths:
        try:
            receipt = _validated_promotion_receipt(paths, receipt_path)
        except (OSError, PermissionError, ValueError, json.JSONDecodeError):
            statuses["invalid"] += 1
            continue
        statuses["approved"] += 1
        state = _promotion_outcome_status(
            paths.outcomes / f"{receipt_path.stem}.json",
            receipt_path.stem,
            action=receipt["approved_action"],
            paths=paths,
        )
        if state is None:
            statuses["pending_execution"] += 1
        else:
            statuses[state] += 1
    return statuses


def refresh_runtime_summary(paths: RuntimePaths) -> dict[str, Any]:
    """Compute retained-store status only in a detached worker or explicit operator call."""
    ensure_store(paths)
    counts = queue_counts(paths)
    promotions = promotion_counts(paths)
    summary = {
        "schema_version": 1,
        "updated_at": iso_now(),
        "pending_extraction": counts["queued"] + counts["retryable"],
        "review_ready": review_ready_count(paths),
        "pending_promotion": promotions["pending_execution"],
    }
    atomic_write_json(paths.state / "runtime-summary.json", summary)
    return summary


def runtime_status(paths: RuntimePaths) -> dict[str, Any]:
    config = load_config(paths)
    prompt_path, schema_path = _extractor_assets()
    return {
        "enabled": bool(config.get("enabled")),
        "privacy_acknowledged": bool(config.get("privacy_acknowledged_at")),
        "state_root": str(paths.state_root),
        "extractor_model": config.get("extractor_model"),
        "claude_binary": resolve_claude_binary(config),
        "queue": queue_counts(paths),
        "promotion": promotion_counts(paths),
        "extraction_available": prompt_path.is_file() and schema_path.is_file(),
        "promotion_automation_available": True,
        "human_approval_required": True,
    }


def start_detached_worker(
    paths: RuntimePaths,
    *,
    root: Path | None = None,
    launcher: Any = subprocess.Popen,
    force: bool = False,
) -> bool:
    config = load_config(paths)
    capture_pending = False
    if not force:
        capture_pending = any(
            path.is_file() and not path.is_symlink()
            for path in paths.capture_inbox.glob("*.json")
        ) if paths.capture_inbox.exists() and not paths.capture_inbox.is_symlink() else False
    if not force and not capture_pending:
        cutoff = utc_now() - timedelta(seconds=max(1, int(config.get("processing_lease_seconds", 900))))
        extraction_pending = any(
            record["state"] in {"queued", "retryable"}
            or (
                record["state"] == "processing"
                and (_parse_timestamp(record["lease_started_at"]) or datetime.min.replace(tzinfo=timezone.utc)) <= cutoff
            )
            for _, record in read_queue(paths)
        )
        promotion_pending = promotion_counts(paths)["pending_execution"] > 0
        if not extraction_pending and not promotion_pending:
            return False
    worker = (root or bundle_root()) / "scripts" / "claude_instinct_worker.py"
    environment = os.environ.copy()
    environment["PMM_INSTINCT_WORKER"] = "1"
    launcher(
        [sys.executable, str(worker), "--state-root", str(paths.state_root), "--drain"],
        cwd=tempfile.gettempdir(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
        env=environment,
    )
    return True
