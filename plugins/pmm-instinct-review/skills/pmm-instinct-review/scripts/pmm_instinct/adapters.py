"""Explicit, isolated runtime adapters for instinct review."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .runtime import RuntimePaths, plugin_root, resolve_paths


PORTABLE_COMMANDS = frozenset(
    {
        "status",
        "list-priority",
        "snapshot-priority",
        "resolve-zero",
        "review",
        "cleanup",
        "import-candidates",
    }
)


@dataclass(frozen=True)
class RuntimeAdapter:
    """One explicitly selected data owner and its allowed behavior."""

    name: str
    paths: RuntimePaths
    capture_supported: bool

    def require_command(self, command: str) -> None:
        if self.name == "portable" and command not in PORTABLE_COMMANDS:
            raise PermissionError(
                f"{command} is unavailable in portable review-only mode; "
                "use explicit candidate import instead"
            )


def _portable_paths(state_root: str | Path) -> RuntimePaths:
    root = Path(state_root).expanduser().resolve()
    home = Path.home().resolve()
    reserved = (home / ".codex", home / ("." + "claude"))
    if any(root == item or item in root.parents for item in reserved):
        raise ValueError("portable state root must not be inside a native agent store")
    package = plugin_root().resolve()
    if root == package or package in root.parents:
        raise ValueError("portable state root must be outside the installed plugin")
    return RuntimePaths(
        codex_home=root,
        store=root,
        sessions=root / "sessions",
        queue=root / "queue",
        instincts=root / "instincts",
        logs=root / "logs",
        state=root / "state",
        config=root / "config.json",
        global_agents=root / "portable-instructions.md",
    )


def resolve_adapter(
    name: str,
    *,
    codex_home: str | Path | None = None,
    state_root: str | Path | None = None,
) -> RuntimeAdapter:
    """Resolve one adapter without falling back to another runtime's state."""

    normalized = name.strip().lower()
    if normalized == "codex":
        if state_root is not None:
            raise ValueError("--state-root is valid only with --adapter portable")
        return RuntimeAdapter("codex", resolve_paths(codex_home), True)
    if normalized == "portable":
        if codex_home is not None:
            raise ValueError("--codex-home cannot be combined with --adapter portable")
        if state_root is None or not str(state_root).strip():
            raise ValueError("portable review-only mode requires an explicit --state-root")
        return RuntimeAdapter("portable", _portable_paths(state_root), False)
    raise ValueError("adapter must be codex or portable")
