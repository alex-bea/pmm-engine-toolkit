"""Standard-library-only runtime for the PMM Instinct Review plugin."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable


DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": 1,
    "enabled": False,
    "privacy_acknowledged_at": None,
    "min_user_messages": 5,
    "max_turns": 200,
    "max_normalized_chars": 120000,
    "retention": "until_reviewed",
    "extractor_model": None,
    "extractor_reasoning_effort": "medium",
    "max_attempts": 3,
    "voice_ref_routes": {},
}
ALLOWED_TYPES = ("correction", "confirmation", "voice", "scope", "workflow")
TYPE_WEIGHTS = {"voice": 10, "workflow": 6, "scope": 5, "correction": 4, "confirmation": 3}
TYPE_AREAS = {
    "voice": ("voice-framing", "Voice and framing", 5),
    "workflow": ("execution-workflow", "Execution workflow", 4),
    "scope": ("scope-decision-rules", "Scope and decision rules", 3),
    "correction": ("execution-corrections", "Execution corrections", 2),
    "confirmation": ("preference-confirmation", "Preference and confirmation", 1),
}
LEGACY_RATIONALE = "Without this rule, the correction described in the evidence could recur."
PROMOTED_GUIDANCE_HEADING = "## PMM Instinct Review — Promoted Guidance"
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
FIELD_RE = re.compile(r"^\*\*([^*]+):\*\*[ \t]*(.*)$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


@dataclass(frozen=True)
class RuntimePaths:
    codex_home: Path
    store: Path
    sessions: Path
    queue: Path
    instincts: Path
    logs: Path
    state: Path
    config: Path
    global_agents: Path


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
    model: str
    source_format: str
    eligible_main_thread: bool
    turns: tuple[Turn, ...]
    user_messages: int
    normalized_chars: int


@dataclass(frozen=True)
class Audit:
    path: Path
    session_id: str
    processed: bool
    cwd: str
    normalized_path: Path | None
    suggestions_path: Path
    audit_date: date | None


@dataclass(frozen=True)
class Candidate:
    session_id: str
    audit_path: Path
    audit_date: date | None
    candidate_type: str
    rule: str
    evidence: str
    context: str
    why_it_matters: str
    source_skill: str
    cwd: str


@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    candidate_type: str
    normalized_rule: str
    rule: str
    evidence: str
    context: str
    why_it_matters: str
    support_count: int
    session_ids: tuple[str, ...]
    audit_paths: tuple[Path, ...]
    source_skills: tuple[str, ...]
    session_cwds: tuple[str, ...]
    earliest: date | None
    latest: date | None
    impact_score: int
    impact_tier: str
    area_key: str
    area_label: str
    match_state: str = "new"


@dataclass(frozen=True)
class Instinct:
    path: Path
    instinct_id: str
    instinct_type: str
    confidence: float
    created: date
    last_seen: date
    seen_count: int
    status: str
    rule: str
    source_skill: str
    source_skills: tuple[str, ...]
    source_runtime: str
    source_transcript_format: str
    source_cwds: tuple[str, ...]
    source_repositories: tuple[Path, ...]
    why_it_matters: str
    contradicted: bool
    suggested_destination: str
    promotion_outcome: str
    promoted_to: tuple[str, ...]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat(timespec="seconds")


def resolve_paths(codex_home: str | Path | None = None) -> RuntimePaths:
    root = Path(codex_home).expanduser() if codex_home else Path.home() / ".codex"
    store = root / "instinct-review"
    return RuntimePaths(
        codex_home=root,
        store=store,
        sessions=store / "sessions",
        queue=store / "queue",
        instincts=store / "instincts",
        logs=store / "logs",
        state=store / "state",
        config=store / "config.json",
        global_agents=root / "AGENTS.md",
    )


def atomic_write_text(path: str | Path, text: str) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.chmod(0o600)
    temporary.replace(destination)
    return destination


def atomic_write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    return atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def ensure_store(paths: RuntimePaths, *, create_config: bool = True) -> None:
    for directory in (paths.store, paths.sessions, paths.queue, paths.instincts, paths.logs, paths.state):
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
    if create_config and not paths.config.exists():
        atomic_write_json(paths.config, dict(DEFAULT_CONFIG))
    if paths.config.exists():
        paths.config.chmod(0o600)


def load_config(paths: RuntimePaths, *, create: bool = False) -> dict[str, Any]:
    if create:
        ensure_store(paths)
    config = dict(DEFAULT_CONFIG)
    if not paths.config.exists():
        return config
    try:
        payload = json.loads(paths.config.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid instinct-review config: {type(error).__name__}") from error
    if not isinstance(payload, dict):
        raise ValueError("invalid instinct-review config: expected object")
    config.update(payload)
    return config


def update_config(paths: RuntimePaths, **updates: Any) -> dict[str, Any]:
    config = load_config(paths, create=True)
    config.update(updates)
    atomic_write_json(paths.config, config)
    return config


def redact_text(text: str) -> str:
    value = PEM_RE.sub("[REDACTED PRIVATE KEY]", text)
    value = BEARER_RE.sub("Bearer [REDACTED TOKEN]", value)
    value = KNOWN_TOKEN_RE.sub("[REDACTED TOKEN]", value)
    return ENV_SECRET_RE.sub(r"\1[REDACTED]", value)


def _is_context_wrapper_turn(text: str) -> bool:
    """Return whether the entire turn is one or more known context wrappers."""

    lowered = text.lower()
    cursor = 0
    matched = False
    while True:
        while cursor < len(lowered) and lowered[cursor].isspace():
            cursor += 1
        if cursor == len(lowered):
            return matched

        markers = next(
            (pair for pair in CONTEXT_WRAPPER_MARKERS if lowered.startswith(pair[0], cursor)),
            None,
        )
        if markers is None:
            return False

        opening, closing = markers
        closing_at = lowered.find(closing, cursor + len(opening))
        if closing_at < 0:
            return False
        cursor = closing_at + len(closing)
        matched = True


def sanitize_turn_text(text: str) -> str:
    stripped = text.strip()
    if not stripped or _is_context_wrapper_turn(stripped):
        return ""
    return redact_text(stripped).strip()


def _content_text(content: Any, *, assistant: bool) -> str:
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    allowed = {"output_text", "text"} if assistant else {"input_text", "text"}
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict) or item.get("type") not in allowed:
            continue
        value = item.get("text")
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
    return "\n".join(parts)


def _metadata(payload: dict[str, Any], path: Path) -> tuple[str, str, str, str, bool]:
    session_id = str(payload.get("id") or payload.get("session_id") or "").strip()
    if not session_id:
        match = re.search(r"([0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})", path.name, re.I)
        session_id = match.group(1) if match else path.stem
    source = payload.get("source")
    thread_source = str(payload.get("thread_source") or "").lower()
    is_subagent = bool(payload.get("parent_thread_id")) or thread_source == "subagent" or isinstance(source, dict)
    return (
        session_id,
        str(payload.get("cwd") or "").strip(),
        str(payload.get("timestamp") or "").strip(),
        str(payload.get("model") or "").strip(),
        not is_subagent,
    )


def _limit_turns(turns: list[tuple[str, str]], *, max_turns: int, max_chars: int) -> list[tuple[str, str]]:
    if max_turns > 0:
        turns = turns[-max_turns:]
    if max_chars <= 0:
        return []
    kept: list[tuple[str, str]] = []
    used = 0
    for role, text in reversed(turns):
        remaining = max_chars - used
        if remaining <= 0:
            break
        if len(text) <= remaining:
            kept.append((role, text))
            used += len(text)
            continue
        if not kept:
            marker = "[TRUNCATED]\n"
            tail = max(0, remaining - len(marker))
            kept.append((role, marker + text[-tail:] if tail else marker[:remaining]))
        break
    return list(reversed(kept))


def normalize_transcript(
    path: str | Path,
    *,
    max_turns: int = 200,
    max_chars: int = 120000,
) -> NormalizationResult:
    transcript = Path(path)
    if not transcript.is_file():
        raise FileNotFoundError(f"Codex transcript not found: {transcript}")
    metadata: dict[str, Any] = {}
    event_turns: list[tuple[str, str]] = []
    fallback_turns: list[tuple[str, str]] = []
    saw_event = False
    with transcript.open(encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(record, dict) or not isinstance(record.get("payload"), dict):
                continue
            payload = record["payload"]
            if record.get("type") == "session_meta" and not metadata:
                metadata = payload
                continue
            if record.get("type") == "event_msg":
                subtype = payload.get("type")
                if subtype not in {"user_message", "agent_message"}:
                    continue
                saw_event = True
                raw_text = payload.get("message")
                text = sanitize_turn_text(raw_text if isinstance(raw_text, str) else "")
                if text:
                    event_turns.append(("user" if subtype == "user_message" else "assistant", text))
                continue
            if record.get("type") != "response_item" or payload.get("type") != "message":
                continue
            role = str(payload.get("role") or "")
            if role not in {"user", "assistant"}:
                continue
            text = sanitize_turn_text(_content_text(payload.get("content"), assistant=role == "assistant"))
            if text:
                fallback_turns.append((role, text))
    selected = event_turns if saw_event else fallback_turns
    deduplicated: list[tuple[str, str]] = []
    for turn in selected:
        if not deduplicated or deduplicated[-1] != turn:
            deduplicated.append(turn)
    user_messages = sum(role == "user" for role, _ in deduplicated)
    limited = _limit_turns(deduplicated, max_turns=max_turns, max_chars=max_chars)
    turns = tuple(Turn(index, role, text) for index, (role, text) in enumerate(limited, start=1))
    session_id, cwd, timestamp, model, eligible = _metadata(metadata, transcript)
    return NormalizationResult(
        session_id=session_id,
        cwd=cwd,
        timestamp=timestamp,
        model=model,
        source_format="codex-rollout-event-msg-v1" if saw_event else "codex-rollout-response-item-v1",
        eligible_main_thread=eligible,
        turns=turns,
        user_messages=user_messages,
        normalized_chars=sum(len(turn.text) for turn in turns),
    )


def serialize_turns(turns: Iterable[Turn]) -> str:
    return "".join(
        json.dumps({"schema_version": 1, "index": turn.index, "role": turn.role, "text": turn.text}, ensure_ascii=False) + "\n"
        for turn in turns
    )


def load_turns(path: str | Path) -> list[Turn]:
    turns: list[Turn] = []
    with Path(path).open(encoding="utf-8") as handle:
        for raw in handle:
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if not isinstance(payload, dict) or payload.get("schema_version") != 1:
                continue
            role = str(payload.get("role") or "")
            text = str(payload.get("text") or "").strip()
            if role in {"user", "assistant"} and text:
                turns.append(Turn(len(turns) + 1, role, text))
    return turns


def safe_session_id(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]", "-", value).strip("-.")
    return (safe or "unknown")[:100]


def _audit_stamp(result: NormalizationResult) -> str:
    parsed: datetime | None = None
    if result.timestamp:
        try:
            parsed = datetime.fromisoformat(result.timestamp.replace("Z", "+00:00"))
        except ValueError:
            pass
    return (parsed or utc_now()).astimezone().strftime("%Y-%m-%d-%H%M")


def _existing_audit(paths: RuntimePaths, session_id: str) -> Path | None:
    for path in paths.sessions.glob("*-audit.md") if paths.sessions.exists() else ():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if re.search(rf"^\*\*session_id:\*\*[ \t]*{re.escape(session_id)}[ \t]*$", text, re.MULTILINE):
            return path
    return None


def capture_session(
    paths: RuntimePaths,
    *,
    session_id: str,
    transcript_path: str | Path,
    cwd: str = "",
    model: str = "",
    force: bool = False,
) -> dict[str, Any]:
    if os.environ.get("PMM_INSTINCT_EXTRACTOR") == "1":
        return {"status": "skipped", "reason": "extractor-run", "session_id": session_id}
    config = load_config(paths, create=force)
    if not force and not config.get("enabled"):
        return {"status": "skipped", "reason": "disabled", "session_id": session_id}
    if not config.get("privacy_acknowledged_at"):
        return {"status": "skipped", "reason": "privacy-not-acknowledged", "session_id": session_id}
    native = Path(transcript_path).expanduser()
    normalized = normalize_transcript(
        native,
        max_turns=int(config["max_turns"]),
        max_chars=int(config["max_normalized_chars"]),
    )
    resolved_id = normalized.session_id or session_id.strip()
    if not normalized.eligible_main_thread:
        return {"status": "skipped", "reason": "not-main-thread", "session_id": resolved_id}
    if normalized.user_messages < int(config["min_user_messages"]):
        return {"status": "skipped", "reason": "below-minimum-user-messages", "session_id": resolved_id}
    ensure_store(paths)
    safe_id = safe_session_id(resolved_id)
    normalized_path = paths.sessions / f"{safe_id}-normalized.jsonl"
    suggestions_path = paths.sessions / f"{safe_id}-suggestions.md"
    audit_path = paths.sessions / f"{_audit_stamp(normalized)}-{safe_id}-audit.md"
    queue_path = paths.queue / f"{safe_id}.json"
    actual_cwd = cwd.strip() or normalized.cwd
    effective_model = str(config.get("extractor_model") or model or normalized.model or "").strip()
    existing = _existing_audit(paths, resolved_id)
    if existing:
        existing_audit = load_audit(existing)
        if existing_audit.processed or queue_path.is_file():
            return {"status": "exists", "reason": "idempotent", "session_id": resolved_id, "audit_path": str(existing)}
        normalized_path = existing_audit.normalized_path or normalized_path
        suggestions_path = existing_audit.suggestions_path
        if not normalized_path.is_file():
            atomic_write_text(normalized_path, serialize_turns(normalized.turns))
        now = iso_now()
        atomic_write_json(
            queue_path,
            {
                "schema_version": 1,
                "session_id": resolved_id,
                "state": "queued",
                "attempts": 0,
                "created_at": now,
                "updated_at": now,
                "started_at": None,
                "finished_at": None,
                "native_transcript_path": str(native),
                "normalized_transcript_path": str(normalized_path),
                "audit_path": str(existing),
                "suggestions_path": str(suggestions_path),
                "source_format": normalized.source_format,
                "extractor_model": effective_model,
                "error": None,
                "recovered": True,
            },
        )
        return {
            "status": "queued",
            "reason": "recovered-partial-capture",
            "session_id": resolved_id,
            "audit_path": str(existing),
            "normalized_path": str(normalized_path),
            "queue_path": str(queue_path),
        }
    atomic_write_text(normalized_path, serialize_turns(normalized.turns))
    audit = "\n".join(
        [
            f"# Session Audit — {_audit_stamp(normalized)}-{safe_id}",
            "processed: false",
            f"**session_id:** {resolved_id}",
            f"**user_messages:** {normalized.user_messages}",
            f"**transcript_path:** {native}",
            f"**normalized_transcript_path:** {normalized_path}",
            f"**suggestions_path:** {suggestions_path}",
            f"**source_transcript_format:** {normalized.source_format}",
            "**source_runtime:** codex",
            f"**extractor_model:** {effective_model}",
            f"**cwd:** {actual_cwd}",
            "**skill:**",
            "",
        ]
    )
    atomic_write_text(audit_path, audit)
    now = iso_now()
    atomic_write_json(
        queue_path,
        {
            "schema_version": 1,
            "session_id": resolved_id,
            "state": "queued",
            "attempts": 0,
            "created_at": now,
            "updated_at": now,
            "started_at": None,
            "finished_at": None,
            "native_transcript_path": str(native),
            "normalized_transcript_path": str(normalized_path),
            "audit_path": str(audit_path),
            "suggestions_path": str(suggestions_path),
            "source_format": normalized.source_format,
            "extractor_model": effective_model,
            "error": None,
        },
    )
    return {
        "status": "queued",
        "session_id": resolved_id,
        "audit_path": str(audit_path),
        "normalized_path": str(normalized_path),
        "queue_path": str(queue_path),
    }


def read_queue(paths: RuntimePaths) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    if not paths.queue.exists():
        return records
    for path in sorted(paths.queue.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            records.append((path, payload))
    return records


def queue_counts(paths: RuntimePaths) -> dict[str, int]:
    counts = {state: 0 for state in ("queued", "running", "succeeded", "failed")}
    for _, record in read_queue(paths):
        state = str(record.get("state") or "")
        if state in counts:
            counts[state] += 1
    return counts


def sanitize_error(error: BaseException | str) -> str:
    if isinstance(error, str):
        value = error
    elif isinstance(error, (RuntimeError, ValueError, FileNotFoundError)):
        value = f"{type(error).__name__}: {error}"
    else:
        value = type(error).__name__
    value = re.sub(r"[\r\n]+", " ", redact_text(value)).strip()
    return value[:300] or "unknown-error"


def write_log(paths: RuntimePaths, session_id: str, event: str) -> None:
    ensure_store(paths)
    safe_event = re.sub(r"[^A-Za-z0-9_.:= /-]", "?", event)[:300]
    log_path = paths.logs / f"{safe_session_id(session_id)}.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{iso_now()} {safe_event}\n")
    log_path.chmod(0o600)


def skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _skill_slug_from_file(path: Path) -> str | None:
    try:
        head = path.read_text(encoding="utf-8")[:8000]
    except OSError:
        return None
    match = re.search(r"(?m)^name:\s*['\"]?([a-z0-9][a-z0-9-]{0,63})['\"]?\s*$", head)
    return match.group(1) if match else None


def _skill_search_roots(paths: RuntimePaths, cwd: str | Path | None = None) -> list[Path]:
    roots = [paths.codex_home / "skills", plugin_root() / "skills"]
    current = Path(cwd).expanduser().resolve() if cwd else None
    if current:
        roots.extend(parent / ".codex" / "skills" for parent in (current, *current.parents))
        roots.extend(parent / "skills" for parent in (current, *current.parents))
    return roots


def discover_skills(paths: RuntimePaths, cwd: str | Path | None = None) -> dict[str, tuple[Path, ...]]:
    discovered: dict[str, set[Path]] = {}
    seen_roots: set[Path] = set()
    for root in _skill_search_roots(paths, cwd):
        resolved_root = root.resolve()
        if resolved_root in seen_roots or not root.is_dir():
            continue
        seen_roots.add(resolved_root)
        for descriptor in root.glob("*/SKILL.md"):
            slug = _skill_slug_from_file(descriptor)
            if slug:
                discovered.setdefault(slug, set()).add(descriptor.parent.resolve())
    return {slug: tuple(sorted(locations)) for slug, locations in sorted(discovered.items())}


def derive_source_skill(turns: Iterable[Turn], valid_slugs: Iterable[str]) -> str | None:
    slugs = tuple(sorted(set(valid_slugs), key=lambda item: (-len(item), item)))
    joined = "\n".join(turn.text for turn in turns)
    for slug in slugs:
        if re.search(rf"(?:\$|/){re.escape(slug)}\b", joined, re.IGNORECASE):
            return slug
    for slug in slugs:
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
    for candidate in candidates:
        if not isinstance(candidate, dict) or set(candidate) != {
            "type",
            "rule",
            "evidence",
            "context",
            "why_it_matters",
        }:
            raise ValueError("invalid extractor candidate fields")
        candidate_type = candidate.get("type")
        values = (
            candidate.get("rule"),
            candidate.get("evidence"),
            candidate.get("context"),
            candidate.get("why_it_matters"),
        )
        if candidate_type not in ALLOWED_TYPES or not all(isinstance(item, str) for item in values):
            raise ValueError("invalid extractor candidate")
        rule, evidence, context, why_it_matters = (" ".join(str(item).split()).strip() for item in values)
        if not rule or not why_it_matters or len(evidence) > 160 or len(context) > 300 or len(why_it_matters) > 300:
            raise ValueError("extractor candidate violates length constraints")
        validated.append(
            {
                "type": candidate_type,
                "rule": rule,
                "evidence": evidence,
                "context": context,
                "why_it_matters": why_it_matters,
            }
        )
    return validated


def render_suggestions(session_id: str, candidates: list[dict[str, str]], source_skill: str | None) -> str:
    lines = [
        "---",
        f"# Instinct Suggestions — {session_id}",
        f"**generated:** {iso_now()}",
        f"**candidates:** {len(candidates)}",
        f"**skill:** {source_skill or ''}",
        "**source_runtime:** codex",
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
                f"**why it matters:** {candidate.get('why_it_matters') or LEGACY_RATIONALE}",
            ]
        )
        if source_skill:
            lines.append(f"**skill:** {source_skill}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def resolve_codex_executable(config: dict[str, Any], explicit: str | None = None) -> str | None:
    configured = explicit or str(config.get("codex_binary") or "").strip()
    if configured:
        candidate = Path(configured).expanduser()
        return str(candidate) if candidate.is_file() and os.access(candidate, os.X_OK) else None
    on_path = shutil.which("codex")
    if on_path:
        return on_path
    for candidate in (
        Path("/Applications/ChatGPT.app/Contents/Resources/codex"),
        Path("/Applications/Codex.app/Contents/Resources/codex"),
    ):
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def extractor_command(
    *,
    codex_binary: str,
    model: str,
    reasoning_effort: str,
    schema_path: Path,
    output_path: Path,
    cwd: Path,
) -> list[str]:
    return [
        codex_binary,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(output_path),
        "--cd",
        str(cwd),
        "-",
    ]


def run_extractor_job(
    paths: RuntimePaths,
    record: dict[str, Any],
    *,
    codex_binary: str | None = None,
    runner: Any = subprocess.run,
) -> list[dict[str, str]]:
    config = load_config(paths)
    model = str(record.get("extractor_model") or "").strip()
    if not model:
        raise RuntimeError("extractor model unavailable in SessionEnd event and configuration")
    normalized_path = Path(str(record.get("normalized_transcript_path") or ""))
    turns = load_turns(normalized_path)
    audit_path = Path(str(record.get("audit_path") or ""))
    cwd = load_audit(audit_path).cwd if audit_path.is_file() else ""
    discovered = discover_skills(paths, cwd)
    source_skill = derive_source_skill(turns, discovered)
    prompt_path = skill_root() / "assets" / "extractor-prompt.md"
    schema_path = skill_root() / "assets" / "extractor-schema.json"
    if not prompt_path.is_file() or not schema_path.is_file():
        raise RuntimeError("extractor prompt or schema unavailable")
    instruction = prompt_path.read_text(encoding="utf-8").replace(
        "{{VALID_SKILL_SLUGS}}", ", ".join(discovered)
    )
    transcript_payload = serialize_turns(turns)
    stdin_payload = (
        instruction
        + "\n\n<untrusted_transcript_jsonl>\n"
        + transcript_payload
        + "</untrusted_transcript_jsonl>\n"
    )
    resolved_codex = resolve_codex_executable(config, codex_binary)
    if not resolved_codex:
        raise RuntimeError("codex executable unavailable")
    with tempfile.TemporaryDirectory(prefix="pmm-instinct-extractor-") as temporary:
        extractor_cwd = Path(temporary)
        output_path = extractor_cwd / "output.json"
        command = extractor_command(
            codex_binary=resolved_codex,
            model=model,
            reasoning_effort=str(config.get("extractor_reasoning_effort") or "medium"),
            schema_path=schema_path,
            output_path=output_path,
            cwd=extractor_cwd,
        )
        environment = os.environ.copy()
        environment["PMM_INSTINCT_EXTRACTOR"] = "1"
        completed = runner(
            command,
            input=stdin_payload,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=environment,
            timeout=900,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"codex exec exited with status {completed.returncode}")
        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError("extractor produced invalid JSON") from error
    candidates = validate_extractor_payload(payload)
    suggestions_path = Path(str(record["suggestions_path"]))
    atomic_write_text(suggestions_path, render_suggestions(str(record["session_id"]), candidates, source_skill))
    return candidates


def transition_queue(path: Path, record: dict[str, Any], **updates: Any) -> dict[str, Any]:
    changed = dict(record)
    changed.update(updates)
    changed["updated_at"] = iso_now()
    atomic_write_json(path, changed)
    return changed


def worker_lock(paths: RuntimePaths) -> Path | None:
    ensure_store(paths)
    lock = paths.state / "worker.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        try:
            payload = json.loads(lock.read_text(encoding="utf-8"))
            os.kill(int(payload.get("pid", 0)), 0)
            return None
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            lock.unlink(missing_ok=True)
            return worker_lock(paths)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump({"pid": os.getpid(), "created_at": iso_now()}, handle)
    return lock


def drain_queue(
    paths: RuntimePaths,
    *,
    session_id: str | None = None,
    codex_binary: str | None = None,
    runner: Any = subprocess.run,
) -> dict[str, int | str]:
    lock = worker_lock(paths)
    if lock is None:
        return {"status": "locked", "processed": 0, "succeeded": 0, "failed": 0}
    processed = succeeded = failed = 0
    try:
        max_attempts = int(load_config(paths).get("max_attempts", 3))
        for queue_path, record in read_queue(paths):
            if session_id and str(record.get("session_id")) != session_id:
                continue
            attempts = int(record.get("attempts", 0))
            if record.get("state") not in {"queued", "failed", "running"} or attempts >= max_attempts:
                continue
            processed += 1
            record = transition_queue(
                queue_path,
                record,
                state="running",
                attempts=attempts + 1,
                started_at=iso_now(),
                finished_at=None,
                error=None,
            )
            write_log(paths, str(record.get("session_id")), f"attempt={attempts + 1} state=running")
            try:
                candidates = run_extractor_job(paths, record, codex_binary=codex_binary, runner=runner)
            except Exception as error:  # Worker must preserve the retryable queue on every failure.
                failed += 1
                sanitized = sanitize_error(error)
                transition_queue(queue_path, record, state="failed", finished_at=iso_now(), error=sanitized)
                write_log(paths, str(record.get("session_id")), f"state=failed error={sanitized}")
                continue
            succeeded += 1
            transition_queue(
                queue_path,
                record,
                state="succeeded",
                finished_at=iso_now(),
                error=None,
                candidate_count=len(candidates),
            )
            write_log(paths, str(record.get("session_id")), f"state=succeeded candidates={len(candidates)}")
    finally:
        lock.unlink(missing_ok=True)
    return {"status": "complete", "processed": processed, "succeeded": succeeded, "failed": failed}


def retry_failed(paths: RuntimePaths, session_id: str | None = None) -> int:
    retried = 0
    for queue_path, record in read_queue(paths):
        if record.get("state") != "failed" or (session_id and str(record.get("session_id")) != session_id):
            continue
        transition_queue(
            queue_path,
            record,
            state="queued",
            attempts=0,
            started_at=None,
            finished_at=None,
            error=None,
            manual_retries=int(record.get("manual_retries", 0)) + 1,
        )
        retried += 1
    return retried


def start_detached_worker(paths: RuntimePaths, cli_path: str | Path) -> bool:
    config = load_config(paths)
    max_attempts = int(config.get("max_attempts", 3))
    if not any(
        record.get("state") in {"queued", "failed", "running"} and int(record.get("attempts", 0)) < max_attempts
        for _, record in read_queue(paths)
    ):
        return False
    environment = os.environ.copy()
    environment["PMM_INSTINCT_EXTRACTOR"] = "1"
    subprocess.Popen(
        [sys.executable, str(Path(cli_path).resolve()), "--codex-home", str(paths.codex_home), "worker", "--drain"],
        cwd=tempfile.gettempdir(),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
        env=environment,
    )
    return True


def _markdown_fields(text: str) -> dict[str, str]:
    return {match.group(1).strip().lower(): match.group(2).strip() for match in FIELD_RE.finditer(text)}


def load_audit(path: str | Path) -> Audit:
    audit_path = Path(path)
    text = audit_path.read_text(encoding="utf-8")
    fields = _markdown_fields(text)
    audit_date: date | None = None
    match = re.match(r"(\d{4}-\d{2}-\d{2})", audit_path.name)
    if match:
        try:
            audit_date = date.fromisoformat(match.group(1))
        except ValueError:
            pass
    normalized_raw = fields.get("normalized_transcript_path", "")
    suggestions_raw = fields.get("suggestions_path", "")
    session_id = fields.get("session_id", "")
    return Audit(
        path=audit_path,
        session_id=session_id,
        processed=bool(re.search(r"(?m)^processed:\s*true\s*$", text)),
        cwd=fields.get("cwd", ""),
        normalized_path=Path(normalized_raw) if normalized_raw else None,
        suggestions_path=(
            Path(suggestions_raw)
            if suggestions_raw
            else audit_path.parent / f"{safe_session_id(session_id)}-suggestions.md"
        ),
        audit_date=audit_date,
    )


def find_audits(paths: RuntimePaths, *, pending_only: bool = False) -> list[Audit]:
    audits = [load_audit(path) for path in sorted(paths.sessions.glob("*-audit.md"))] if paths.sessions.exists() else []
    return [audit for audit in audits if not audit.processed] if pending_only else audits


def suggestion_count(path: str | Path) -> int | None:
    suggestion_path = Path(path)
    if not suggestion_path.is_file():
        return None
    fields = _markdown_fields(suggestion_path.read_text(encoding="utf-8"))
    try:
        return int(fields.get("candidates", "0"))
    except ValueError:
        return 0


def load_candidates(audit: Audit) -> list[Candidate]:
    if not audit.suggestions_path.is_file():
        return []
    text = audit.suggestions_path.read_text(encoding="utf-8")
    file_fields = _markdown_fields(text.split("## Candidate", 1)[0])
    chunks = re.split(r"(?m)^## Candidate\s+\d+\s*$", text)[1:]
    candidates: list[Candidate] = []
    for chunk in chunks:
        fields = _markdown_fields(chunk)
        candidate_type = fields.get("type", "")
        rule = fields.get("rule", "")
        if candidate_type not in ALLOWED_TYPES or not rule:
            continue
        candidates.append(
            Candidate(
                session_id=audit.session_id,
                audit_path=audit.path,
                audit_date=audit.audit_date,
                candidate_type=candidate_type,
                rule=rule,
                evidence=fields.get("evidence", ""),
                context=fields.get("context", ""),
                why_it_matters=fields.get("why it matters", ""),
                source_skill=fields.get("skill", "") or file_fields.get("skill", ""),
                cwd=audit.cwd,
            )
        )
    return candidates


def normalize_rule(rule: str) -> str:
    value = " ".join(rule.lower().strip().split())
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def cluster_id(candidate_type: str, normalized_rule: str) -> str:
    digest = hashlib.sha256(f"{candidate_type}\0{normalized_rule}".encode()).hexdigest()[:12]
    return f"{candidate_type}-{digest}"


def _review_ledger(paths: RuntimePaths) -> dict[str, Any]:
    ledger_path = paths.state / "review-decisions.json"
    if not ledger_path.is_file():
        return {}
    try:
        payload = json.loads(ledger_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_review_ledger(paths: RuntimePaths, ledger: dict[str, Any]) -> None:
    atomic_write_json(paths.state / "review-decisions.json", ledger)


def _area_for_type(candidate_type: str) -> tuple[str, str, int]:
    return TYPE_AREAS.get(candidate_type, ("other", "Other", 0))


def _impact_tier(impact: int, support: int, skill_count: int, cwd_count: int) -> str:
    if impact >= 20 or (support >= 10 and skill_count >= 3):
        return "critical"
    if impact >= 12 or support >= 8 or skill_count >= 2 or cwd_count >= 3:
        return "high"
    if impact >= 6 or support >= 4:
        return "medium"
    return "low"


def _cluster_sort_key(item: Cluster) -> tuple[Any, ...]:
    area_priority = _area_for_type(item.candidate_type)[2]
    recency = item.latest.toordinal() if item.latest else 0
    return (-area_priority, -item.impact_score, -item.support_count, -recency, item.cluster_id)


def _all_clusters(paths: RuntimePaths, *, include_decided: bool) -> list[Cluster]:
    ledger = _review_ledger(paths)
    instincts = load_instincts(paths)
    instinct_keys = {
        (instinct.instinct_type, normalize_rule(instinct.rule))
        for instinct in instincts
        if instinct.status == "active"
    }
    grouped: dict[tuple[str, str], list[Candidate]] = {}
    for audit in find_audits(paths, pending_only=True):
        for candidate in load_candidates(audit):
            normalized = normalize_rule(candidate.rule)
            identifier = cluster_id(candidate.candidate_type, normalized)
            decided_sessions = set(ledger.get(identifier, {}).get("session_ids", []))
            if not include_decided and candidate.session_id in decided_sessions:
                continue
            grouped.setdefault((candidate.candidate_type, normalized), []).append(candidate)
    records: list[Cluster] = []
    for (candidate_type, normalized), items in grouped.items():
        items = sorted(items, key=lambda item: (item.audit_date or date.min, item.session_id))
        first = items[0]
        support = len({item.session_id for item in items})
        source_skills = tuple(sorted({item.source_skill for item in items if item.source_skill}))
        session_cwds = tuple(sorted({item.cwd for item in items if item.cwd}))
        match_state = "exact" if (candidate_type, normalized) in instinct_keys else "new"
        skill_breadth = max(0, len(source_skills) - 1) * 2
        cwd_breadth = max(0, len(session_cwds) - 1)
        impact = (
            TYPE_WEIGHTS.get(candidate_type, 2)
            + support
            + skill_breadth
            + cwd_breadth
            + (2 if match_state == "new" else 0)
        )
        tier = _impact_tier(impact, support, len(source_skills), len(session_cwds))
        area_key, area_label, _ = _area_for_type(candidate_type)
        dates = sorted(item.audit_date for item in items if item.audit_date)
        records.append(
            Cluster(
                cluster_id=cluster_id(candidate_type, normalized),
                candidate_type=candidate_type,
                normalized_rule=normalized,
                rule=first.rule,
                evidence=first.evidence,
                context=first.context,
                why_it_matters=first.why_it_matters,
                support_count=support,
                session_ids=tuple(sorted({item.session_id for item in items})),
                audit_paths=tuple(sorted({item.audit_path for item in items})),
                source_skills=source_skills,
                session_cwds=session_cwds,
                earliest=dates[0] if dates else None,
                latest=dates[-1] if dates else None,
                impact_score=impact,
                impact_tier=tier,
                area_key=area_key,
                area_label=area_label,
                match_state=match_state,
            )
        )
    return sorted(records, key=_cluster_sort_key)


def clusters(paths: RuntimePaths) -> list[Cluster]:
    return _all_clusters(paths, include_decided=False)


def confidence_for_support(
    support: int,
    *,
    strong_correction: bool = False,
    contradicted: bool = False,
) -> float:
    if support >= 11:
        confidence = 0.85
    elif support >= 6:
        confidence = 0.70
    elif support >= 3:
        confidence = 0.50
    else:
        confidence = 0.30
    if strong_correction:
        confidence += 0.05
    if contradicted:
        confidence -= 0.10
    return max(0.0, min(1.0, round(confidence, 2)))


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing instinct frontmatter")
    metadata: dict[str, Any] = {}
    for raw in match.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        scalar = value.strip()
        try:
            metadata[key.strip()] = json.loads(scalar)
        except json.JSONDecodeError:
            metadata[key.strip()] = scalar
    return metadata, match.group(2).strip()


def _serialize_frontmatter(metadata: dict[str, Any], body: str) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        if value is None:
            encoded = "null"
        elif isinstance(value, (str, list, dict, bool, int, float)):
            encoded = json.dumps(value, ensure_ascii=False)
        else:
            encoded = json.dumps(str(value), ensure_ascii=False)
        lines.append(f"{key}: {encoded}")
    lines.extend(["---", "", body.strip(), ""])
    return "\n".join(lines)


def _body_rule(body: str) -> str:
    return body.split("\n\n", 1)[0].strip()


def _body_labeled_value(body: str, label: str) -> str:
    prefix = f"**{label}:**"
    for chunk in body.split("\n\n"):
        candidate = chunk.strip()
        if candidate.startswith(prefix):
            return candidate.removeprefix(prefix).strip()
    return ""


def _metadata_strings(metadata: dict[str, Any], key: str) -> tuple[str, ...]:
    value = metadata.get(key) or []
    if isinstance(value, str):
        value = [value] if value else []
    return tuple(str(item).strip() for item in value if str(item).strip()) if isinstance(value, list) else ()


def load_instincts(paths: RuntimePaths) -> list[Instinct]:
    instincts: list[Instinct] = []
    if not paths.instincts.exists():
        return instincts
    for path in sorted(paths.instincts.glob("pmm-instinct-*.md")):
        try:
            metadata, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
            created = date.fromisoformat(str(metadata.get("created")))
            last_seen = date.fromisoformat(str(metadata.get("last_seen") or metadata.get("created")))
            promoted = metadata.get("promoted_to") or []
            if isinstance(promoted, str):
                promoted = [promoted] if promoted else []
            source_skill = str(metadata.get("source_skill") or "")
            source_skills = _metadata_strings(metadata, "source_skills") or ((source_skill,) if source_skill else ())
            instincts.append(
                Instinct(
                    path=path,
                    instinct_id=str(metadata.get("id") or path.stem),
                    instinct_type=str(metadata.get("type") or "workflow"),
                    confidence=float(metadata.get("confidence", 0)),
                    created=created,
                    last_seen=last_seen,
                    seen_count=int(metadata.get("seen_count", 1)),
                    status=str(metadata.get("status") or "active"),
                    rule=_body_rule(body),
                    source_skill=source_skill,
                    source_skills=source_skills,
                    source_runtime=str(metadata.get("source_runtime") or ""),
                    source_transcript_format=str(metadata.get("source_transcript_format") or ""),
                    source_cwds=_metadata_strings(metadata, "source_cwds"),
                    source_repositories=tuple(Path(item) for item in _metadata_strings(metadata, "source_repositories")),
                    why_it_matters=_body_labeled_value(body, "Why it matters") or LEGACY_RATIONALE,
                    contradicted=bool(metadata.get("contradicted", False)),
                    suggested_destination=str(metadata.get("suggested_destination") or ""),
                    promotion_outcome=str(metadata.get("promotion_outcome") or ""),
                    promoted_to=tuple(str(item) for item in promoted if str(item)),
                )
            )
        except (OSError, ValueError, TypeError):
            continue
    return instincts


def next_instinct_id(instincts: Iterable[Instinct], created: date | None = None) -> str:
    day = created or date.today()
    prefix = f"pmm-instinct-{day.isoformat()}-"
    numbers = []
    for instinct in instincts:
        if instinct.instinct_id.startswith(prefix):
            try:
                numbers.append(int(instinct.instinct_id.rsplit("-", 1)[1]))
            except ValueError:
                pass
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def _source_repositories(cwds: Iterable[str]) -> tuple[Path, ...]:
    repositories: list[Path] = []
    for cwd in cwds:
        candidate = _nearest_repository(cwd)
        if candidate is not None and candidate not in repositories:
            repositories.append(candidate)
    return tuple(repositories)


def suggested_destination_for_cluster(cluster: Cluster) -> str:
    """Return a conservative destination hint without resolving or writing a path."""

    if cluster.candidate_type == "voice":
        return "ref" if cluster.source_skills else "global"
    if len(cluster.source_skills) >= 3:
        return "standard"
    if cluster.source_skills and cluster.candidate_type in {"workflow", "scope", "correction"}:
        return "run"
    if len(_source_repositories(cluster.session_cwds)) == 1:
        return "project"
    return "both" if cluster.session_cwds else "global"


def stale_instincts(
    instincts: Iterable[Instinct],
    *,
    today: date | None = None,
    stale_days: int = 28,
) -> list[Instinct]:
    current = today or date.today()
    return sorted(
        (
            instinct
            for instinct in instincts
            if instinct.status == "active"
            and instinct.seen_count == 1
            and (current - instinct.created).days > stale_days
        ),
        key=lambda instinct: (instinct.created, instinct.instinct_id),
    )


def _write_new_instinct(
    paths: RuntimePaths,
    cluster: Cluster,
    rule: str | None = None,
    why_it_matters: str | None = None,
    *,
    source_runtime: str = "codex",
    strong_correction: bool = False,
    contradicted: bool = False,
) -> Path:
    ensure_store(paths)
    instincts = load_instincts(paths)
    created = date.today()
    identifier = next_instinct_id(instincts, created)
    chosen_rule = rule or cluster.rule
    chosen_why = why_it_matters or cluster.why_it_matters or LEGACY_RATIONALE
    if len(chosen_why) > 300:
        raise ValueError("instinct rationale must be at most 300 characters")
    metadata = {
        "id": identifier,
        "type": cluster.candidate_type,
        "confidence": confidence_for_support(
            cluster.support_count,
            strong_correction=strong_correction,
            contradicted=contradicted,
        ),
        "created": created.isoformat(),
        "last_seen": (cluster.latest or created).isoformat(),
        "seen_count": cluster.support_count,
        "status": "active",
        "source_skill": cluster.source_skills[0] if len(cluster.source_skills) == 1 else "",
        "source_skills": list(cluster.source_skills),
        "source_runtime": source_runtime,
        "source_transcript_format": (
            "normalized-jsonl-v1" if source_runtime == "codex" else "explicit-candidate-json-v1"
        ),
        "source_cwds": list(cluster.session_cwds),
        "source_repositories": [str(path) for path in _source_repositories(cluster.session_cwds)],
        "strong_correction": strong_correction,
        "contradicted": contradicted,
        "suggested_destination": suggested_destination_for_cluster(cluster),
        "promotion_outcome": "",
        "promoted_to": [],
    }
    body = "\n\n".join(
        [
            chosen_rule,
            f"**Evidence:** {cluster.evidence or 'Clustered from approved session suggestions.'}",
            f"**Why it matters:** {chosen_why}",
        ]
    )
    return atomic_write_text(paths.instincts / f"{identifier}.md", _serialize_frontmatter(metadata, body))


def _update_instinct(
    instinct: Instinct,
    cluster: Cluster,
    *,
    source_runtime: str = "codex",
    strong_correction: bool = False,
    contradicted: bool = False,
) -> Path:
    metadata, body = _parse_frontmatter(instinct.path.read_text(encoding="utf-8"))
    seen = instinct.seen_count + cluster.support_count
    metadata["seen_count"] = seen
    metadata["last_seen"] = (cluster.latest or date.today()).isoformat()
    metadata["strong_correction"] = bool(metadata.get("strong_correction", False)) or strong_correction
    metadata["contradicted"] = bool(metadata.get("contradicted", False)) or contradicted
    metadata["confidence"] = confidence_for_support(
        seen,
        strong_correction=bool(metadata["strong_correction"]),
        contradicted=bool(metadata["contradicted"]),
    )
    metadata["source_cwds"] = sorted(set(instinct.source_cwds) | set(cluster.session_cwds))
    metadata["source_skills"] = sorted(set(instinct.source_skills) | set(cluster.source_skills))
    metadata["source_repositories"] = sorted(
        {str(path) for path in instinct.source_repositories} | {str(path) for path in _source_repositories(cluster.session_cwds)}
    )
    metadata["source_runtime"] = str(metadata.get("source_runtime") or source_runtime)
    metadata["source_transcript_format"] = str(
        metadata.get("source_transcript_format")
        or ("normalized-jsonl-v1" if source_runtime == "codex" else "explicit-candidate-json-v1")
    )
    metadata["suggested_destination"] = str(
        metadata.get("suggested_destination") or suggested_destination_for_cluster(cluster)
    )
    metadata["promotion_outcome"] = str(metadata.get("promotion_outcome") or "")
    return atomic_write_text(instinct.path, _serialize_frontmatter(metadata, body))


def mark_audit_processed(audit: Audit) -> None:
    text = audit.path.read_text(encoding="utf-8")
    if re.search(r"(?m)^processed:\s*(?:true|false)\s*$", text):
        text = re.sub(r"(?m)^processed:\s*(?:true|false)\s*$", "processed: true", text, count=1)
    else:
        text = "processed: true\n" + text
    atomic_write_text(audit.path, text)


def resolve_audits(paths: RuntimePaths, audit_paths: Iterable[Path]) -> list[str]:
    warnings: list[str] = []
    for audit_path in audit_paths:
        audit = load_audit(audit_path)
        mark_audit_processed(audit)
        if audit.normalized_path and audit.normalized_path.exists():
            try:
                audit.normalized_path.unlink()
            except OSError as error:
                warning = f"{audit.session_id}: {sanitize_error(error)}"
                warnings.append(warning)
                write_log(paths, audit.session_id, f"cleanup-warning error={sanitize_error(error)}")
    return warnings


def cleanup_processed(paths: RuntimePaths) -> dict[str, Any]:
    removed = 0
    warnings: list[str] = []
    for audit in find_audits(paths):
        if not audit.processed or not audit.normalized_path or not audit.normalized_path.exists():
            continue
        try:
            audit.normalized_path.unlink()
            removed += 1
        except OSError as error:
            warnings.append(f"{audit.session_id}: {sanitize_error(error)}")
    return {"removed": removed, "warnings": warnings}


def review_cluster(
    paths: RuntimePaths,
    selected_id: str,
    decision: str,
    *,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
    source_runtime: str = "codex",
    strong_correction: bool = False,
    contradicted: bool = False,
    confirm: bool = False,
) -> dict[str, Any]:
    if decision not in {"accept", "reject", "edit", "match"}:
        raise ValueError("decision must be accept, reject, edit, or match")
    if not confirm:
        raise PermissionError("review requires --confirm")
    selected = next((item for item in clusters(paths) if item.cluster_id == selected_id), None)
    if not selected:
        raise ValueError(f"cluster not found: {selected_id}")
    if decision == "edit" and not (edited_rule or "").strip():
        raise ValueError("edit requires a non-empty edited rule")
    if decision != "edit" and edited_rationale is not None:
        raise ValueError("edited rationale is allowed only with an edit decision")
    if strong_correction and selected.candidate_type != "correction":
        raise ValueError("strong correction applies only to correction candidates")
    matching = next(
        (
            item
            for item in load_instincts(paths)
            if item.status == "active"
            and item.instinct_type == selected.candidate_type
            and normalize_rule(item.rule) == selected.normalized_rule
        ),
        None,
    )
    instinct_path: Path | None = None
    if decision == "match":
        if not matching:
            raise ValueError("match decision requires an exact active instinct")
        instinct_path = _update_instinct(
            matching,
            selected,
            source_runtime=source_runtime,
            strong_correction=strong_correction,
            contradicted=contradicted,
        )
    elif decision in {"accept", "edit"}:
        if matching:
            raise ValueError("an exact active instinct exists; use match")
        instinct_path = _write_new_instinct(
            paths,
            selected,
            (edited_rule or "").strip() or None,
            (edited_rationale or "").strip() or None,
            source_runtime=source_runtime,
            strong_correction=strong_correction,
            contradicted=contradicted,
        )
    ledger = _review_ledger(paths)
    previous_sessions = set(ledger.get(selected.cluster_id, {}).get("session_ids", []))
    ledger[selected.cluster_id] = {
        "decision": decision,
        "session_ids": sorted(previous_sessions | set(selected.session_ids)),
        "reviewed_at": iso_now(),
        "instinct_path": str(instinct_path) if instinct_path else None,
    }
    _write_review_ledger(paths, ledger)
    resolved_paths: list[Path] = []
    for audit_path in selected.audit_paths:
        audit = load_audit(audit_path)
        audit_candidates = load_candidates(audit)
        if audit_candidates and all(
            candidate.session_id
            in set(
                ledger.get(
                    cluster_id(candidate.candidate_type, normalize_rule(candidate.rule)), {}
                ).get("session_ids", [])
            )
            for candidate in audit_candidates
        ):
            resolved_paths.append(audit_path)
    warnings = resolve_audits(paths, resolved_paths)
    return {
        "cluster_id": selected.cluster_id,
        "decision": decision,
        "instinct_path": str(instinct_path) if instinct_path else None,
        "strong_correction": strong_correction,
        "contradicted": contradicted,
        "resolved_audits": [str(path) for path in resolved_paths],
        "cleanup_warnings": warnings,
    }


def resolve_zero_candidate_audits(paths: RuntimePaths, *, confirm: bool = False) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("zero-candidate resolution requires --confirm")
    audits = [
        audit
        for audit in find_audits(paths, pending_only=True)
        if suggestion_count(audit.suggestions_path) == 0
    ]
    warnings = resolve_audits(paths, [audit.path for audit in audits])
    return {"resolved": len(audits), "cleanup_warnings": warnings}


def backlog(paths: RuntimePaths) -> dict[str, Any]:
    pending = find_audits(paths, pending_only=True)
    items = clusters(paths)
    zero_audits = [audit for audit in pending if suggestion_count(audit.suggestions_path) == 0]
    missing_audits = [audit for audit in pending if suggestion_count(audit.suggestions_path) is None]
    unresolved = sum(bool(audit.normalized_path and audit.normalized_path.exists()) for audit in pending)
    serialized: list[dict[str, Any]] = []
    for item in items:
        source_repositories = [str(path) for path in _source_repositories(item.session_cwds)]
        serialized.append(
            {
                "cluster_id": item.cluster_id,
                "type": item.candidate_type,
                "area_key": item.area_key,
                "area_label": item.area_label,
                "rule": item.rule,
                "normalized_rule": item.normalized_rule,
                "evidence": item.evidence,
                "context": item.context,
                "why_it_matters": item.why_it_matters or LEGACY_RATIONALE,
                "candidate_card": {
                    "what_happened": item.context or "No additional context was captured.",
                    "your_feedback": item.evidence or "No redacted feedback was captured.",
                    "proposed_future_behavior": item.rule,
                    "why_it_matters": item.why_it_matters or LEGACY_RATIONALE,
                    "support_count": item.support_count,
                    "source_skills": list(item.source_skills),
                    "source_repositories": source_repositories,
                    "session_cwds": list(item.session_cwds),
                    "first_seen": item.earliest.isoformat() if item.earliest else None,
                    "last_seen": item.latest.isoformat() if item.latest else None,
                    "existing_match": item.match_state,
                },
                "support_count": item.support_count,
                "session_ids": list(item.session_ids),
                "audit_paths": [str(path) for path in item.audit_paths],
                "source_skills": list(item.source_skills),
                "source_repositories": source_repositories,
                "session_cwds": list(item.session_cwds),
                "first_seen": item.earliest.isoformat() if item.earliest else None,
                "last_seen": item.latest.isoformat() if item.latest else None,
                "impact_score": item.impact_score,
                "impact_tier": item.impact_tier,
                "match_state": item.match_state,
            }
        )
    areas = []
    for area_key, area_label, _ in sorted(TYPE_AREAS.values(), key=lambda value: -value[2]):
        area_clusters = [item for item in serialized if item["area_key"] == area_key]
        if area_clusters:
            areas.append(
                {
                    "area_key": area_key,
                    "area_label": area_label,
                    "cluster_count": len(area_clusters),
                    "clusters": area_clusters,
                }
            )
    tier_counts = {
        tier: sum(item["impact_tier"] == tier for item in serialized)
        for tier in ("critical", "high", "medium", "low")
    }
    match_counts = {
        state: sum(item["match_state"] == state for item in serialized)
        for state in ("new", "exact")
    }
    return {
        "pending_audits": len(pending),
        "positive_clusters": len(items),
        "positive_suggestions": sum((suggestion_count(audit.suggestions_path) or 0) for audit in pending),
        "zero_candidate_audits": len(zero_audits),
        "missing_suggestions": len(missing_audits),
        "unresolved_normalized_transcripts": unresolved,
        "priority_summary": {
            "impact_tiers": tier_counts,
            "areas": {area["area_key"]: area["cluster_count"] for area in areas},
            "match_states": match_counts,
        },
        "buckets": {
            "zero_candidate": {
                "count": len(zero_audits),
                "audit_ids": [audit.session_id for audit in zero_audits],
            },
            "positive_clusters": {"count": len(items)},
            "missing_suggestions": {
                "count": len(missing_audits),
                "audit_ids": [audit.session_id for audit in missing_audits],
            },
        },
        "areas": areas,
        "clusters": serialized,
    }


def priority_snapshot_path(paths: RuntimePaths) -> Path:
    return paths.sessions / "instinct-priority.json"


def build_priority_snapshot(
    paths: RuntimePaths,
    *,
    generated_at: datetime | None = None,
    today: date | None = None,
) -> dict[str, Any]:
    snapshot = backlog(paths)
    instincts = load_instincts(paths)
    return {
        "schema_version": 1,
        "generated_at": (generated_at or utc_now()).isoformat(timespec="seconds"),
        "store": str(paths.store),
        "priority_snapshot_path": str(priority_snapshot_path(paths)),
        "backlog": {key: value for key, value in snapshot.items() if key not in {"clusters", "areas"}},
        "instincts": {
            "active": sum(item.status == "active" for item in instincts),
            "promotion_candidates": sum(
                item.status == "active" and item.confidence >= 0.5 for item in instincts
            ),
            "stale_candidates": len(stale_instincts(instincts, today=today)),
        },
        "areas": snapshot["areas"],
    }


def write_priority_snapshot(paths: RuntimePaths) -> Path:
    return atomic_write_json(priority_snapshot_path(paths), build_priority_snapshot(paths))


def _nearest_repository(path: str | Path) -> Path | None:
    current = Path(path).expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _project_agents_path(instinct: Instinct, explicit_project: str | Path | None = None) -> Path | None:
    if explicit_project:
        root = _nearest_repository(explicit_project) or Path(explicit_project).expanduser().resolve()
    else:
        repositories = {_nearest_repository(item) for item in instinct.source_cwds if Path(item).expanduser().exists()}
        repositories.discard(None)
        if len(repositories) != 1:
            return None
        root = next(iter(repositories))
    assert root is not None
    cwd = Path(instinct.source_cwds[0]).expanduser().resolve() if instinct.source_cwds else root
    if root not in (cwd, *cwd.parents):
        cwd = root
    for candidate in (cwd, *cwd.parents):
        if root not in (candidate, *candidate.parents):
            break
        existing = candidate / "AGENTS.md"
        if existing.is_file():
            return existing
        if candidate == root:
            break
    return root / "AGENTS.md"


def _is_plugin_owned_path(paths: RuntimePaths, candidate: Path) -> bool:
    resolved = candidate.resolve()
    plugin_cache = (paths.codex_home / "plugins" / "cache").resolve()
    bundled = plugin_root().resolve()
    return plugin_cache in (resolved, *resolved.parents) or bundled in (resolved, *resolved.parents)


def _writable_user_file(paths: RuntimePaths, candidate: Path) -> bool:
    return candidate.is_file() and os.access(candidate, os.W_OK) and not _is_plugin_owned_path(paths, candidate)


def _source_skill_locations(paths: RuntimePaths, instinct: Instinct) -> tuple[Path, ...]:
    if len(instinct.source_skills) != 1:
        return ()
    discovered: set[Path] = set()
    for cwd in instinct.source_cwds or (None,):
        discovered.update(discover_skills(paths, cwd).get(instinct.source_skills[0], ()))
    return tuple(sorted(location for location in discovered if not _is_plugin_owned_path(paths, location)))


def _run_destination(paths: RuntimePaths, instinct: Instinct) -> Path | None:
    candidates: list[Path] = []
    for location in _source_skill_locations(paths, instinct):
        candidates.extend(path for path in (location / "references").glob("RUN-*.md") if _writable_user_file(paths, path))
    return candidates[0] if len(candidates) == 1 else None


def _voice_ref_destination(paths: RuntimePaths, instinct: Instinct) -> Path | None:
    if instinct.instinct_type != "voice" or len(instinct.source_skills) != 1:
        return None
    routes = load_config(paths).get("voice_ref_routes")
    route = routes.get(instinct.source_skills[0]) if isinstance(routes, dict) else None
    if not isinstance(route, str) or not route.strip():
        return None
    relative = Path(route)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    candidates: list[Path] = []
    for location in _source_skill_locations(paths, instinct):
        candidate = (location / relative).resolve()
        if location.resolve() not in (candidate, *candidate.parents):
            continue
        if candidate.name.startswith("REF-") and _writable_user_file(paths, candidate):
            candidates.append(candidate)
    return candidates[0] if len(candidates) == 1 else None


def _standard_destination(
    paths: RuntimePaths,
    instinct: Instinct,
    standard: str | Path | None,
) -> Path | None:
    if len(instinct.source_skills) < 3:
        raise ValueError("standard promotion requires evidence from at least three source skills")
    if not standard:
        raise ValueError("standard promotion requires --standard")
    candidate = Path(standard).expanduser().resolve()
    if not candidate.name.startswith("STD-") or candidate.suffix != ".md":
        raise ValueError("standard promotion requires an existing STD-*.md file")
    if not _writable_user_file(paths, candidate):
        raise ValueError("standard destination must be an existing writable non-plugin file")
    repositories = instinct.source_repositories or _source_repositories(instinct.source_cwds)
    if repositories and not any(root.resolve() in (candidate, *candidate.parents) for root in repositories):
        raise ValueError("standard destination must belong to a supporting source repository")
    return candidate


def instruction_contains_rule(path: str | Path, rule: str) -> bool:
    destination = Path(path)
    if not destination.is_file():
        return False
    return normalize_rule(rule) in normalize_rule(destination.read_text(encoding="utf-8"))


def _available_promotion_destinations(
    paths: RuntimePaths,
    instinct: Instinct,
    project: str | Path | None = None,
) -> list[str]:
    choices = ["global"]
    if _project_agents_path(instinct, project) is not None:
        choices.extend(["project", "both"])
    if _run_destination(paths, instinct) is not None:
        choices.append("run")
    if _voice_ref_destination(paths, instinct) is not None:
        choices.append("ref")
    if len(instinct.source_skills) >= 3:
        choices.append("standard")
    return choices


def _promotion_preview_path(paths: RuntimePaths, instinct_id: str) -> Path:
    return paths.state / f"promotion-preview-{safe_session_id(instinct_id)}.json"


def _preview_signature(preview: dict[str, Any]) -> str:
    signed = {
        "instinct_id": preview["instinct_id"],
        "decision": preview["decision"],
        "rule": preview["rule"],
        "why_it_matters": preview["why_it_matters"],
        "insertion": preview["insertion"],
        "targets": [target["path"] for target in preview["targets"]],
    }
    return hashlib.sha256(json.dumps(signed, sort_keys=True).encode("utf-8")).hexdigest()


def _build_promotion_preview(
    paths: RuntimePaths,
    instinct_id: str,
    *,
    destination: str | None = None,
    project: str | Path | None = None,
    standard: str | Path | None = None,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
) -> dict[str, Any]:
    instinct = next((item for item in load_instincts(paths) if item.instinct_id == instinct_id), None)
    if not instinct:
        raise ValueError(f"instinct not found: {instinct_id}")
    if instinct.status != "active" or instinct.confidence < 0.5:
        raise ValueError("instinct is not eligible for promotion (active and confidence >= 0.5 required)")
    rule = (edited_rule or instinct.rule).strip()
    why_it_matters = (edited_rationale or instinct.why_it_matters).strip()
    if not rule:
        raise ValueError("promotion rule cannot be blank")
    if not why_it_matters or len(why_it_matters) > 300:
        raise ValueError("promotion rationale must be between 1 and 300 characters")
    if destination == "no":
        return {"instinct_id": instinct_id, "decision": "no", "applied": False, "targets": []}
    if destination == "edit":
        if not edited_rule:
            raise ValueError("edit requires --edited-rule")
        destination = None
    if destination is None:
        return {
            "instinct_id": instinct_id,
            "decision": "select-destination",
            "rule": rule,
            "why_it_matters": why_it_matters,
            "available_destinations": _available_promotion_destinations(paths, instinct, project),
            "applied": False,
            "targets": [],
        }
    targets: list[Path] = []
    if destination in {"project", "both"}:
        project_path = _project_agents_path(instinct, project)
        if not project_path:
            raise ValueError("one repository could not be resolved; supply --project or choose global")
        targets.append(project_path)
    if destination in {"global", "both"}:
        targets.append(paths.global_agents)
    if destination in {"run", "skill"}:
        run_path = _run_destination(paths, instinct)
        if not run_path:
            raise ValueError("one exact writable registered skill RUN document could not be resolved")
        targets.append(run_path)
        destination = "run"
    if destination == "ref":
        ref_path = _voice_ref_destination(paths, instinct)
        if not ref_path:
            raise ValueError("one exact writable mapped voice REF document could not be resolved")
        targets.append(ref_path)
    if destination == "standard":
        targets.append(_standard_destination(paths, instinct, standard))
    if destination not in {"project", "global", "both", "run", "ref", "standard"}:
        raise ValueError("destination must be project, global, both, run, ref, standard, edit, or no")
    insertion = f"- {rule}"
    return {
        "instinct_id": instinct_id,
        "decision": destination,
        "rule": rule,
        "why_it_matters": why_it_matters,
        "insertion": insertion,
        "section": PROMOTED_GUIDANCE_HEADING,
        "targets": [
            {"path": str(target), "duplicate": instruction_contains_rule(target, rule)} for target in targets
        ],
        "applied": False,
    }


def promotion_preview(
    paths: RuntimePaths,
    instinct_id: str,
    *,
    destination: str | None = None,
    project: str | Path | None = None,
    standard: str | Path | None = None,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
) -> dict[str, Any]:
    preview = _build_promotion_preview(
        paths,
        instinct_id,
        destination=destination,
        project=project,
        standard=standard,
        edited_rule=edited_rule,
        edited_rationale=edited_rationale,
    )
    if preview["decision"] not in {"no", "select-destination"}:
        atomic_write_json(
            _promotion_preview_path(paths, instinct_id),
            {"signature": _preview_signature(preview), "previewed_at": iso_now()},
        )
        preview["confirmation_required"] = True
    return preview


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
    updated = lines[:section_end]
    if updated and updated[-1] != "":
        updated.append("")
    updated.extend([insertion, ""])
    updated.extend(lines[section_end:])
    return "\n".join(updated).rstrip() + "\n"


def _stage_text(path: Path, text: str, mode: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".pmm-instinct-review", dir=path.parent)
    temporary = Path(raw_path)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(text)
    temporary.chmod(mode)
    return temporary


def _write_guidance_updates(updates: list[tuple[Path, str]]) -> None:
    originals = [
        (path, path.read_text(encoding="utf-8") if path.exists() else "", path.exists(), path.stat().st_mode & 0o777 if path.exists() else 0o644)
        for path, _ in updates
    ]
    staged: list[tuple[Path, Path]] = []
    applied: list[tuple[Path, str, bool, int]] = []
    try:
        for (path, original, existed, mode), (_, updated) in zip(originals, updates, strict=True):
            staged.append((path, _stage_text(path, updated, mode)))
        for (path, original, existed, mode), (_, temporary) in zip(originals, staged, strict=True):
            os.replace(temporary, path)
            applied.append((path, original, existed, mode))
    except OSError:
        for path, original, existed, mode in reversed(applied):
            if existed:
                os.replace(_stage_text(path, original, mode), path)
            else:
                path.unlink(missing_ok=True)
        for _, temporary in staged:
            temporary.unlink(missing_ok=True)
        raise


def apply_promotion(
    paths: RuntimePaths,
    instinct_id: str,
    *,
    destination: str | None = None,
    project: str | Path | None = None,
    standard: str | Path | None = None,
    edited_rule: str | None = None,
    edited_rationale: str | None = None,
    confirm: bool = False,
) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("promotion requires --confirm after preview")
    preview = _build_promotion_preview(
        paths,
        instinct_id,
        destination=destination,
        project=project,
        standard=standard,
        edited_rule=edited_rule,
        edited_rationale=edited_rationale,
    )
    if preview.get("decision") == "no":
        return preview
    if preview.get("decision") == "select-destination":
        raise ValueError("select a promotion destination and preview it before applying")
    preview_record_path = _promotion_preview_path(paths, instinct_id)
    try:
        preview_record = json.loads(preview_record_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        preview_record = {}
    if preview_record.get("signature") != _preview_signature(preview):
        raise PermissionError("promotion requires a matching destination preview before --confirm")
    updates: list[tuple[Path, str]] = []
    for target in preview["targets"]:
        if target["duplicate"]:
            continue
        path = Path(target["path"])
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        updates.append((path, _render_guidance_update(existing, str(preview["insertion"]))))
    _write_guidance_updates(updates)
    instinct = next(item for item in load_instincts(paths) if item.instinct_id == instinct_id)
    metadata, body = _parse_frontmatter(instinct.path.read_text(encoding="utf-8"))
    metadata["promoted_to"] = sorted(
        set(instinct.promoted_to)
        | {f"{item['path']} § {PROMOTED_GUIDANCE_HEADING}" for item in preview["targets"]}
    )
    changed = [str(path) for path, _ in updates]
    covered = [item["path"] for item in preview["targets"] if item["duplicate"]]
    metadata["status"] = "promoted" if changed else "covered"
    metadata["promotion_outcome"] = metadata["status"]
    evidence = _body_labeled_value(body, "Evidence") or "Clustered from approved session suggestions."
    updated_body = "\n\n".join(
        [
            str(preview["rule"]),
            f"**Evidence:** {evidence}",
            f"**Why it matters:** {preview['why_it_matters']}",
        ]
    )
    atomic_write_text(instinct.path, _serialize_frontmatter(metadata, updated_body))
    preview_record_path.unlink(missing_ok=True)
    preview["applied"] = True
    preview["changed"] = changed
    preview["covered"] = covered
    preview["terminal_status"] = metadata["status"]
    return preview


def discover_backfill(
    paths: RuntimePaths,
    *,
    limit: int = 5,
    older_than_minutes: int = 30,
) -> list[dict[str, Any]]:
    sessions_root = paths.codex_home / "sessions"
    cutoff = utc_now().timestamp() - max(0, older_than_minutes) * 60
    candidates: list[dict[str, Any]] = []
    if not sessions_root.exists():
        return candidates
    config = load_config(paths)
    for transcript in sorted(sessions_root.glob("**/*.jsonl"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            if transcript.stat().st_mtime > cutoff:
                continue
            normalized = normalize_transcript(
                transcript,
                max_turns=int(config.get("max_turns", 200)),
                max_chars=int(config.get("max_normalized_chars", 120000)),
            )
        except (OSError, ValueError):
            continue
        if not normalized.eligible_main_thread or normalized.user_messages < int(config.get("min_user_messages", 5)):
            continue
        if _existing_audit(paths, normalized.session_id):
            continue
        candidates.append(
            {
                "session_id": normalized.session_id,
                "transcript_path": str(transcript),
                "cwd": normalized.cwd,
                "model": normalized.model,
                "user_messages": normalized.user_messages,
                "modified_at": datetime.fromtimestamp(transcript.stat().st_mtime, timezone.utc).isoformat(),
            }
        )
        if len(candidates) >= limit:
            break
    return candidates


def apply_backfill(paths: RuntimePaths, inventory: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    if not load_config(paths).get("privacy_acknowledged_at"):
        raise PermissionError("backfill requires prior local-chat-storage acknowledgment")
    results: list[dict[str, Any]] = []
    for candidate in inventory:
        results.append(
            capture_session(
                paths,
                session_id=str(candidate["session_id"]),
                transcript_path=str(candidate["transcript_path"]),
                cwd=str(candidate.get("cwd") or ""),
                model=str(candidate.get("model") or ""),
                force=True,
            )
        )
    return results


def import_candidates(
    paths: RuntimePaths,
    source: str | Path,
    *,
    cwd: str = "",
    source_runtime: str = "codex",
    confirm: bool = False,
) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("candidate import requires --confirm")
    candidate_path = Path(source)
    payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("candidate file must contain a JSON array")
    required = {"id", "lesson", "source", "observed_on", "evidence"}
    imported: list[str] = []
    errors: list[str] = []
    ensure_store(paths)
    valid_slugs = discover_skills(paths, cwd)
    for index, item in enumerate(payload):
        if not isinstance(item, dict) or required - set(item):
            errors.append(f"record {index}: missing required fields")
            continue
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{item.get('id')}: evidence must be a non-empty list")
            continue
        source_id = safe_session_id(f"import-{candidate_path.stem}-{item['id']}")
        if _existing_audit(paths, source_id):
            imported.append(source_id)
            continue
        observed = str(item.get("observed_on") or "")[:10]
        try:
            stamp = date.fromisoformat(observed).strftime("%Y-%m-%d-0000")
        except ValueError:
            errors.append(f"{item.get('id')}: invalid observed_on")
            continue
        suggestions_path = paths.sessions / f"{source_id}-suggestions.md"
        audit_path = paths.sessions / f"{stamp}-{source_id}-audit.md"
        source_skill = str(item.get("skill") or "")
        if source_skill not in valid_slugs:
            source_skill = ""
        raw_type = str(item.get("type") or "workflow")
        candidate_type = raw_type if raw_type in ALLOWED_TYPES else "workflow"
        candidate = {
            "type": candidate_type,
            "rule": " ".join(str(item["lesson"]).split()),
            "evidence": " ".join(str(evidence[0]).split())[:160],
            "context": f"Imported from {item['source']} observed {observed}"[:300],
            "why_it_matters": LEGACY_RATIONALE,
        }
        validate_extractor_payload({"candidates": [candidate]})
        atomic_write_text(suggestions_path, render_suggestions(source_id, [candidate], source_skill or None))
        atomic_write_text(
            audit_path,
            "\n".join(
                [
                    f"# Imported Audit — {source_id}",
                    "processed: false",
                    f"**session_id:** {source_id}",
                    f"**suggestions_path:** {suggestions_path}",
                    "**source_transcript_format:** explicit-candidate-json-v1",
                    f"**source_runtime:** {source_runtime}",
                    f"**cwd:** {cwd}",
                    f"**skill:** {source_skill}",
                    "",
                ]
            ),
        )
        imported.append(source_id)
    return {"imported": imported, "errors": errors}


def preflight(paths: RuntimePaths, *, codex_binary: str | None = None) -> dict[str, Any]:
    config = load_config(paths)
    schema_path = skill_root() / "assets" / "extractor-schema.json"
    schema_valid = False
    try:
        schema_valid = isinstance(json.loads(schema_path.read_text(encoding="utf-8")), dict)
    except (OSError, json.JSONDecodeError):
        pass
    resolved_codex = resolve_codex_executable(config, codex_binary)
    checks = {
        "python": sys.version_info >= (3, 11),
        "codex": bool(resolved_codex),
        "extractor_schema": schema_valid,
        "model_policy": bool(config.get("extractor_model")) or config.get("extractor_model") is None,
    }
    return {
        "ok": all(checks.values()),
        "checks": checks,
        "codex_binary": resolved_codex,
        "extractor_model": config.get("extractor_model") or "SessionEnd event (required)",
    }


def runtime_status(paths: RuntimePaths) -> dict[str, Any]:
    config = load_config(paths)
    instincts = load_instincts(paths)
    current_backlog = backlog(paths)
    return {
        "enabled": bool(config.get("enabled")),
        "privacy_acknowledged_at": config.get("privacy_acknowledged_at"),
        "extractor_model": config.get("extractor_model"),
        "queue": queue_counts(paths),
        "backlog": {
            key: value
            for key, value in current_backlog.items()
            if key not in {"clusters", "areas"}
        },
        "active_instincts": sum(item.status == "active" for item in instincts),
        "promotion_candidates": sum(item.status == "active" and item.confidence >= 0.5 for item in instincts),
        "stale_instincts": len(stale_instincts(instincts)),
        "priority_snapshot_path": str(priority_snapshot_path(paths)),
        "store": str(paths.store),
        "preflight": preflight(paths),
    }
