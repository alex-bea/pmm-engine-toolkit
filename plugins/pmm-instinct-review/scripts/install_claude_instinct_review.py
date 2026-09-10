#!/usr/bin/env python3
"""Install or remove the standalone Claude skill and its owned lifecycle hooks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pmm_instinct_claude import atomic_write_json, ensure_store, load_config, resolve_paths  # noqa: E402


SOURCE_ROOT = Path(__file__).resolve().parents[1]
OWNED_SCRIPT = "claude_instinct_hook.py"
HOOK_EVENTS = ("SessionStart", "SessionEnd")
RECEIPT_SCHEMA_VERSION = 2
REQUIRED_BUNDLE_SURFACES = (
    "README.md",
    ".claude-plugin/plugin.json",
    "hooks/claude-hooks.json",
    "scripts/pmm_instinct_claude.py",
    "scripts/claude_instinct_capture.py",
    "scripts/claude_instinct_hook.py",
    "scripts/claude_instinct_worker.py",
    "scripts/claude_instinct_review.py",
    "scripts/claude_instinct_promote.py",
    "scripts/install_claude_instinct_review.py",
    "assets/claude-config-template.json",
    "assets/claude-extractor-prompt.md",
    "assets/claude-extractor-schema.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}") from error
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return payload


def _hook_entry(event: str, active_root: Path, state_root: Path) -> dict[str, Any]:
    if event not in HOOK_EVENTS:
        raise ValueError(f"unsupported Claude hook event: {event}")
    event_arg = "session-start" if event == "SessionStart" else "session-end"
    active_script = (active_root / "scripts" / OWNED_SCRIPT).expanduser().resolve()
    canonical_state = state_root.expanduser().resolve()
    handler: dict[str, Any] = {
        "type": "command",
        "command": "python3",
        "args": [
            str(active_script),
            "--state-root",
            str(canonical_state),
            event_arg,
        ],
        "timeout": 5,
    }
    if event == "SessionStart":
        handler["statusMessage"] = "Checking the private instinct queue"
        return {"matcher": "startup|resume|clear|compact", "hooks": [handler]}
    return {"hooks": [handler]}


def _hook_identity(event: str, active_root: Path, state_root: Path) -> dict[str, Any]:
    entry = _hook_entry(event, active_root, state_root)
    handler = entry["hooks"][0]
    return {
        "event": event,
        "matcher_present": "matcher" in entry,
        "matcher": entry.get("matcher"),
        "active_script": handler["args"][0],
        "state_root": handler["args"][2],
        "handler": handler,
    }


def _hook_identities(active_root: Path, state_root: Path) -> list[dict[str, Any]]:
    return [_hook_identity(event, active_root, state_root) for event in HOOK_EVENTS]


def _validate_settings(settings: dict[str, Any]) -> None:
    hooks = settings.get("hooks")
    if hooks is None:
        return
    if not isinstance(hooks, dict):
        raise ValueError("Claude settings hooks must be an object")
    for event, entries in hooks.items():
        if not isinstance(entries, list):
            raise ValueError(f"Claude settings hooks.{event} must be an array")
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("hooks"), list):
                raise ValueError(f"Claude settings hooks.{event} contains an invalid entry")
            if any(not isinstance(handler, dict) for handler in entry["hooks"]):
                raise ValueError(f"Claude settings hooks.{event} contains an invalid handler")


def _entry_matches_identity(entry: Any, identity: dict[str, Any]) -> bool:
    return (
        isinstance(entry, dict)
        and ("matcher" in entry) == identity["matcher_present"]
        and entry.get("matcher") == identity["matcher"]
        and isinstance(entry.get("hooks"), list)
    )


def _remove_one_identity(settings: dict[str, Any], identity: dict[str, Any]) -> bool:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return False
    event = identity["event"]
    entries = hooks.get(event)
    if not isinstance(entries, list):
        return False
    expected_handler = identity["handler"]
    for entry_index, entry in enumerate(entries):
        if not _entry_matches_identity(entry, identity):
            continue
        for handler_index, handler in enumerate(entry["hooks"]):
            if handler != expected_handler:
                continue
            changed_entry = dict(entry)
            changed_handlers = list(entry["hooks"])
            changed_handlers.pop(handler_index)
            if changed_handlers:
                changed_entry["hooks"] = changed_handlers
                entries[entry_index] = changed_entry
            else:
                entries.pop(entry_index)
            if not entries:
                hooks.pop(event, None)
            if not hooks:
                settings.pop("hooks", None)
            return True
    return False


def _remove_receipt_owned_entries(settings: dict[str, Any], identities: list[dict[str, Any]]) -> int:
    return sum(_remove_one_identity(settings, identity) for identity in identities)


def _pmm_looking_handlers(settings: dict[str, Any]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return matches
    for entries in hooks.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("hooks"), list):
                continue
            for handler in entry["hooks"]:
                if not isinstance(handler, dict):
                    continue
                command = handler.get("command")
                args = handler.get("args")
                fragments = [command] if isinstance(command, str) else []
                if isinstance(args, list):
                    fragments.extend(item for item in args if isinstance(item, str))
                if any(OWNED_SCRIPT in fragment for fragment in fragments):
                    matches.append(handler)
    return matches


def _install_hooks(settings: dict[str, Any], identities: list[dict[str, Any]]) -> None:
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError("Claude settings hooks must be an object")
    for identity in identities:
        event = identity["event"]
        entries = hooks.setdefault(event, [])
        if not isinstance(entries, list):
            raise ValueError(f"Claude settings hooks.{event} must be an array")
        entry: dict[str, Any] = {"hooks": [identity["handler"]]}
        if identity["matcher_present"]:
            entry["matcher"] = identity["matcher"]
        entries.append(entry)


RECEIPT_FIELDS = {
    "schema_version",
    "receipt_digest",
    "installed_at",
    "mode",
    "claude_home",
    "source_root",
    "active_root",
    "active_skill",
    "skill_path",
    "settings_path",
    "settings_backup",
    "state_root",
    "capture_enabled",
    "privacy_acknowledged",
    "state_preserved_on_uninstall",
    "bundle_preserved",
    "owned_hook_handlers",
}


def _clone_json(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload))


def _canonical(path: Path) -> Path:
    return path.expanduser().resolve()


def _receipt_digest(receipt: dict[str, Any]) -> str:
    unsigned = {key: value for key, value in receipt.items() if key != "receipt_digest"}
    canonical = json.dumps(unsigned, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_canonical_path(receipt: dict[str, Any], field: str) -> Path:
    value = receipt.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"installation receipt {field} must be a non-empty path")
    path = Path(value)
    if not path.is_absolute() or str(_canonical(path)) != value:
        raise ValueError(f"installation receipt {field} is not canonical")
    return path


def _build_receipt(
    *,
    installed_at: datetime,
    mode: str,
    claude_home: Path,
    source_root: Path,
    active_root: Path,
    active_skill: Path,
    skill_path: Path,
    settings_path: Path,
    settings_backup: Path | None,
    state_root: Path,
    identities: list[dict[str, Any]],
    capture_enabled: bool,
    privacy_acknowledged: bool,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "installed_at": installed_at.isoformat(timespec="seconds"),
        "mode": mode,
        "claude_home": str(claude_home),
        "source_root": str(source_root),
        "active_root": str(active_root),
        "active_skill": str(active_skill),
        "skill_path": str(skill_path),
        "settings_path": str(settings_path),
        "settings_backup": str(settings_backup) if settings_backup else None,
        "state_root": str(state_root),
        "capture_enabled": capture_enabled,
        "privacy_acknowledged": privacy_acknowledged,
        "state_preserved_on_uninstall": True,
        "bundle_preserved": True,
        "owned_hook_handlers": identities,
    }
    receipt["receipt_digest"] = _receipt_digest(receipt)
    return receipt


def _validate_receipt(
    receipt: dict[str, Any],
    *,
    claude_home: Path,
    state_root: Path,
) -> list[dict[str, Any]]:
    if set(receipt) != RECEIPT_FIELDS:
        raise ValueError("installation receipt has an unexpected schema")
    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        raise ValueError("installation receipt schema is unsupported")
    digest = receipt.get("receipt_digest")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(character not in "0123456789abcdef" for character in digest)
        or digest != _receipt_digest(receipt)
    ):
        raise ValueError("installation receipt digest does not match its contents")
    installed_at = receipt.get("installed_at")
    if not isinstance(installed_at, str):
        raise ValueError("installation receipt installed_at must be a timestamp")
    try:
        parsed_at = datetime.fromisoformat(installed_at)
    except ValueError as error:
        raise ValueError("installation receipt installed_at must be a timestamp") from error
    if parsed_at.tzinfo is None:
        raise ValueError("installation receipt installed_at must include a timezone")
    if receipt.get("mode") not in {"symlink", "copy"}:
        raise ValueError("installation receipt mode is invalid")
    if type(receipt.get("capture_enabled")) is not bool or type(receipt.get("privacy_acknowledged")) is not bool:
        raise ValueError("installation receipt capture observations are invalid")
    expected_flags = {"state_preserved_on_uninstall": True, "bundle_preserved": True}
    if any(receipt.get(key) is not value for key, value in expected_flags.items()):
        raise ValueError("installation receipt safety flags are invalid")

    recorded_home = _validate_canonical_path(receipt, "claude_home")
    recorded_source = _validate_canonical_path(receipt, "source_root")
    recorded_active = _validate_canonical_path(receipt, "active_root")
    recorded_skill = _validate_canonical_path(receipt, "active_skill")
    skill_path_value = receipt.get("skill_path")
    if not isinstance(skill_path_value, str) or not Path(skill_path_value).is_absolute():
        raise ValueError("installation receipt skill_path must be an absolute path")
    recorded_skill_path = Path(skill_path_value)
    recorded_settings = _validate_canonical_path(receipt, "settings_path")
    recorded_state = _validate_canonical_path(receipt, "state_root")
    if recorded_home != claude_home or recorded_state != state_root:
        raise ValueError("installation receipt belongs to a different Claude installation")
    if recorded_settings != claude_home / "settings.json":
        raise ValueError("installation receipt settings path is invalid")
    if recorded_skill_path != claude_home / "skills" / "pmm-instinct-review":
        raise ValueError("installation receipt skill path is invalid")
    if receipt["mode"] == "symlink" and recorded_active != recorded_source:
        raise ValueError("installation receipt symlink root is invalid")
    if receipt["mode"] == "copy" and recorded_active != claude_home / "pmm-instinct-review":
        raise ValueError("installation receipt copy root is invalid")
    allowed_skills = {
        recorded_active,
        recorded_active / "skills" / "pmm-instinct-review",
    }
    if recorded_skill not in allowed_skills:
        raise ValueError("installation receipt active skill is invalid")
    backup_value = receipt.get("settings_backup")
    if backup_value is not None:
        backup = _validate_canonical_path(receipt, "settings_backup")
        expected_prefix = f"{recorded_settings.name}.pmm-instinct-review."
        if backup.parent != recorded_settings.parent or not (
            backup.name.startswith(expected_prefix) and backup.name.endswith(".bak")
        ):
            raise ValueError("installation receipt settings backup is invalid")

    identities = receipt.get("owned_hook_handlers")
    expected_identities = _hook_identities(recorded_active, recorded_state)
    if identities != expected_identities:
        raise ValueError("installation receipt hook identities are invalid")
    return identities


def _required_receipt(*, claude_home: Path, state_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        paths = resolve_paths(state_root)
        _validate_installed_store(paths)
        receipt_path = paths.state / "installation.json"
        if receipt_path.is_symlink() or not receipt_path.is_file():
            raise ValueError("installation receipt is missing or not a regular file")
        receipt = _load_json(receipt_path)
        identities = _validate_receipt(receipt, claude_home=claude_home, state_root=state_root)
    except (OSError, ValueError) as error:
        raise PermissionError("uninstall requires a valid, untampered installation receipt") from error
    return receipt, identities


def _preflight_directory(path: Path, label: str) -> None:
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise FileExistsError(f"{label} is not a directory: {path}")


def _preflight_file(path: Path, label: str) -> None:
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise FileExistsError(f"{label} is not a regular file: {path}")


def _preflight_store(paths: Any) -> None:
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
        _preflight_directory(directory, "state destination")
    _preflight_file(paths.config, "state config")
    load_config(paths)
    _preflight_file(paths.state / "installation.json", "installation receipt")


def _validate_installed_store(paths: Any) -> None:
    """Validate receipt authority without creating or repairing state."""
    _preflight_store(paths)
    required_directories = (
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
    )
    if any(not path.is_dir() for path in required_directories):
        raise ValueError("installed runtime state is incomplete")
    if not paths.config.is_file() or paths.config.is_symlink():
        raise ValueError("installed runtime config is missing or invalid")
    load_config(paths)


def _planned_backup(path: Path, now: datetime) -> Path | None:
    if not path.exists():
        return None
    stamp = now.strftime("%Y%m%dT%H%M%S.%fZ")
    return path.with_name(f"{path.name}.pmm-instinct-review.{stamp}.bak")


def _backup(path: Path, destination: Path | None) -> Path | None:
    if destination is None:
        return None
    shutil.copy2(path, destination)
    return destination


def _copy_bundle(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"copy destination already exists: {destination}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def _skill_source(bundle_root: Path) -> Path:
    """Return the discoverable skill folder for private and public bundle layouts."""
    direct = bundle_root / "SKILL.md"
    nested = bundle_root / "skills" / "pmm-instinct-review" / "SKILL.md"
    if direct.is_file():
        return bundle_root
    if nested.is_file():
        return nested.parent
    raise ValueError("bundle has no discoverable PMM Instinct Review SKILL.md")


def _validate_complete_bundle(bundle_root: Path, skill_root: Path) -> None:
    """Require every standalone runtime surface before hooks can point at a bundle."""
    if bundle_root.is_symlink() or not bundle_root.is_dir() or bundle_root.resolve() != bundle_root:
        raise ValueError("bundle root must be a canonical regular directory")
    if (
        skill_root.is_symlink()
        or not skill_root.is_dir()
        or skill_root.resolve() != skill_root
        or (skill_root != bundle_root and bundle_root not in skill_root.parents)
    ):
        raise ValueError("bundle skill root must be a regular directory inside the bundle")
    required = [bundle_root / relative for relative in REQUIRED_BUNDLE_SURFACES]
    if skill_root == bundle_root:
        required.extend(
            skill_root / relative
            for relative in (
                "SKILL.md",
                "references/RUN-pmm-instinct-review-setup-workflow-prd-v2.6.0.md",
                "references/DOC-pmm-instinct-review-product-prd-v1.1.md",
                "references/BP-pmm-instinct-review-implementation-impl-v1.1.md",
                "references/REF-pmm-instinct-review-changelog.md",
            )
        )
    else:
        required.extend(bundle_root / relative for relative in (".codex-plugin/plugin.json", "hooks/hooks.json"))
        required.extend(
            skill_root / relative
            for relative in (
                "SKILL.md",
                "references/RUN-claude-setup.md",
                "references/RUN-workflow.md",
                "references/DOC-product-requirements.md",
                "references/DOC-implementation-blueprint.md",
                "references/DOC-submission-test-cases.md",
                "assets/config-template.json",
                "assets/extractor-prompt.md",
                "assets/extractor-schema.json",
                "assets/instinct-template.md",
                "assets/output-template.md",
                "assets/state-contracts.md",
                "scripts/instinct_review.py",
                "scripts/pmm_instinct/__init__.py",
                "scripts/pmm_instinct/adapters.py",
                "scripts/pmm_instinct/runtime.py",
            )
        )
    for path in required:
        try:
            resolved = path.resolve(strict=True)
        except OSError as error:
            raise ValueError(f"bundle is incomplete: missing {path.relative_to(bundle_root)}") from error
        if path.is_symlink() or not path.is_file() or resolved != path:
            raise ValueError(f"bundle surface must be a regular file: {path.relative_to(bundle_root)}")


def install(
    *,
    claude_home: Path,
    state_root: Path,
    source_root: Path,
    mode: str,
) -> dict[str, Any]:
    if mode not in {"symlink", "copy"}:
        raise ValueError("mode must be symlink or copy")
    home = _canonical(claude_home)
    state = _canonical(state_root)
    source = _canonical(source_root)
    source_skill = _skill_source(source)
    _validate_complete_bundle(source, source_skill)
    skill_relative = source_skill.relative_to(source)
    active_root = source if mode == "symlink" else home / "pmm-instinct-review"
    active_skill = active_root / skill_relative
    if source == home or source in home.parents or home in source.parents:
        raise ValueError("Claude home and source bundle must not overlap")
    if state == source or state.is_relative_to(source):
        raise ValueError("state root must be outside the source bundle")
    if state == active_root or state.is_relative_to(active_root):
        raise ValueError("state root must be outside the active bundle")
    skill_target = home / "skills" / "pmm-instinct-review"
    settings_path = home / "settings.json"
    if state == home or state in home.parents:
        raise ValueError("state root must not contain the Claude home")
    protected_destinations = (
        source,
        active_root,
        skill_target.parent,
        skill_target,
        settings_path,
    )
    if any(
        state == destination or state in destination.parents or destination in state.parents
        for destination in protected_destinations
    ):
        raise ValueError("state root must not overlap an installer-owned destination or bundle")
    paths = resolve_paths(state)
    receipt_path = paths.state / "installation.json"

    # Everything that can be validated is checked before any directory, backup,
    # symlink, settings, or receipt is created.
    _preflight_directory(home, "Claude home")
    _preflight_directory(skill_target.parent, "Claude skills directory")
    _preflight_file(settings_path, "Claude settings")
    _preflight_store(paths)
    settings = _load_json(settings_path)
    _validate_settings(settings)

    previous_receipt: dict[str, Any] | None = None
    previous_identities: list[dict[str, Any]] = []
    if receipt_path.exists():
        previous_receipt = _load_json(receipt_path)
        previous_identities = _validate_receipt(
            previous_receipt,
            claude_home=home,
            state_root=state,
        )
        expected_upgrade = {
            "mode": mode,
            "source_root": str(source),
            "active_root": str(active_root),
            "active_skill": str(active_skill),
            "skill_path": str(skill_target),
            "settings_path": str(settings_path),
        }
        if any(previous_receipt.get(key) != value for key, value in expected_upgrade.items()):
            raise ValueError("existing installation receipt does not match this upgrade")
    elif _pmm_looking_handlers(settings):
        raise PermissionError(
            "Claude settings contain PMM Instinct Review-looking hooks without a valid receipt; "
            "they were preserved and installation stopped"
        )
    existing_config = load_config(paths) if paths.config.exists() else {}
    capture_enabled = existing_config.get("enabled") is True
    privacy_acknowledged = bool(existing_config.get("privacy_acknowledged_at"))
    if previous_receipt is None and (capture_enabled or privacy_acknowledged):
        raise PermissionError(
            "unowned state root contains prior capture consent or enablement; installation stopped"
        )

    copy_needed = False
    if mode == "copy":
        if active_root.is_symlink():
            raise FileExistsError(f"copy install root may not be a symlink: {active_root}")
        if active_root.exists():
            if previous_receipt is None:
                raise FileExistsError(f"occupied install root is not receipt-owned: {active_root}")
            if not active_root.is_dir() or _skill_source(active_root) != active_skill:
                raise FileExistsError(f"receipt-owned install root is incomplete: {active_root}")
            _validate_complete_bundle(active_root, active_skill)
            _validate_complete_bundle(active_root, active_skill)
        else:
            copy_needed = True
    elif not active_skill.is_file() and not (active_skill / "SKILL.md").is_file():
        raise ValueError("active skill is missing")

    create_skill_link = False
    if skill_target.is_symlink():
        if previous_receipt is None:
            raise FileExistsError(f"skill target is not receipt-owned: {skill_target}")
        try:
            matches_active_skill = skill_target.resolve() == active_skill
        except OSError:
            matches_active_skill = False
        if not matches_active_skill:
            raise FileExistsError(f"receipt-owned skill target was changed: {skill_target}")
    elif skill_target.exists():
        raise FileExistsError(f"skill target already exists and is not an owned symlink: {skill_target}")
    else:
        create_skill_link = True

    identities = _hook_identities(active_root, state)
    updated_settings = _clone_json(settings)
    if previous_identities:
        _remove_receipt_owned_entries(updated_settings, previous_identities)
        remaining_handlers = _pmm_looking_handlers(updated_settings)
        if remaining_handlers:
            raise PermissionError(
                "Claude settings contain modified or ambiguous PMM Instinct Review hooks; "
                "they were preserved and upgrade stopped"
            )
    _install_hooks(updated_settings, identities)
    settings_changed = updated_settings != settings
    now = datetime.now(timezone.utc)
    backup = _planned_backup(settings_path, now) if settings_changed else None
    if backup is not None and (backup.exists() or backup.is_symlink()):
        raise FileExistsError(f"settings backup destination already exists: {backup}")
    receipt = _build_receipt(
        installed_at=now,
        mode=mode,
        claude_home=home,
        source_root=source,
        active_root=active_root,
        active_skill=active_skill,
        skill_path=skill_target,
        settings_path=settings_path,
        settings_backup=backup,
        state_root=state,
        identities=identities,
        capture_enabled=capture_enabled,
        privacy_acknowledged=privacy_acknowledged,
    )

    home.mkdir(parents=True, exist_ok=True)
    ensure_store(paths)
    if copy_needed:
        _copy_bundle(source, active_root)
    skill_target.parent.mkdir(parents=True, exist_ok=True)
    if create_skill_link:
        skill_target.symlink_to(active_skill, target_is_directory=True)
    if settings_changed:
        _backup(settings_path, backup)
        atomic_write_json(settings_path, updated_settings)
        settings_path.chmod(0o600)
    atomic_write_json(receipt_path, receipt)
    return receipt


def check(*, claude_home: Path, state_root: Path) -> dict[str, Any]:
    home = _canonical(claude_home)
    state = _canonical(state_root)
    skill_target = home / "skills" / "pmm-instinct-review"
    settings_path = home / "settings.json"
    settings = _load_json(settings_path)
    _validate_settings(settings)
    owned = 0
    expected_owned = 0
    receipt_valid = False
    skill_target_valid = False
    bundle_valid = False
    receipt_error: str | None = None
    bundle_error: str | None = None
    ambiguous = len(_pmm_looking_handlers(settings))
    paths = resolve_paths(state)
    receipt_path = paths.state / "installation.json"
    try:
        _validate_installed_store(paths)
        if receipt_path.is_file() and not receipt_path.is_symlink():
            receipt = _load_json(receipt_path)
            identities = _validate_receipt(receipt, claude_home=home, state_root=state)
            expected_owned = len(identities)
            probe = _clone_json(settings)
            owned = _remove_receipt_owned_entries(probe, identities)
            ambiguous = len(_pmm_looking_handlers(probe))
            recorded_skill = Path(receipt["active_skill"])
            try:
                skill_target_valid = (
                    skill_target.is_symlink()
                    and skill_target.resolve(strict=True) == recorded_skill.resolve(strict=True)
                    and recorded_skill.is_dir()
                    and (recorded_skill / "SKILL.md").is_file()
                )
            except (OSError, RuntimeError):
                skill_target_valid = False
            try:
                _validate_complete_bundle(
                    Path(receipt["active_root"]),
                    Path(receipt["active_skill"]),
                )
                bundle_valid = True
            except (OSError, ValueError) as error:
                bundle_error = str(error)
            receipt_valid = True
        else:
            receipt_error = "installation receipt is missing"
    except (OSError, ValueError) as error:
        receipt_error = str(error)
    if not receipt_valid and ambiguous:
        receipt_error = (
            f"{receipt_error}; {ambiguous} PMM-looking hook handler(s) have ambiguous ownership"
        )
    return {
        "skill_path": str(skill_target),
        "skill_installed": skill_target.exists() or skill_target.is_symlink(),
        "skill_symlink": skill_target.is_symlink(),
        "owned_hook_handlers": owned,
        "ambiguous_hook_handlers": ambiguous,
        "settings_path": str(settings_path),
        "state_root": str(state),
        "state_present": state.exists(),
        "receipt_valid": receipt_valid,
        "skill_target_valid": skill_target_valid,
        "bundle_valid": bundle_valid,
        "installation_valid": (
            receipt_valid
            and skill_target_valid
            and bundle_valid
            and owned == expected_owned
            and expected_owned > 0
            and ambiguous == 0
        ),
        "receipt_error": receipt_error,
        "bundle_error": bundle_error,
    }


def uninstall(*, claude_home: Path, state_root: Path, confirm: bool) -> dict[str, Any]:
    if not confirm:
        raise PermissionError("uninstall requires --confirm")
    home = _canonical(claude_home)
    state = _canonical(state_root)
    receipt, identities = _required_receipt(claude_home=home, state_root=state)
    settings_path = home / "settings.json"
    skill_target = home / "skills" / "pmm-instinct-review"

    _preflight_directory(home, "Claude home")
    _preflight_directory(skill_target.parent, "Claude skills directory")
    _preflight_file(settings_path, "Claude settings")
    settings = _load_json(settings_path)
    _validate_settings(settings)
    updated_settings = _clone_json(settings)
    removed_hooks = _remove_receipt_owned_entries(updated_settings, identities)
    remaining_handlers = _pmm_looking_handlers(updated_settings)
    if remaining_handlers:
        raise PermissionError(
            "Claude settings contain modified or ambiguous PMM Instinct Review hooks; "
            "they and the skill link were preserved and uninstall stopped"
        )
    now = datetime.now(timezone.utc)
    backup = _planned_backup(settings_path, now) if removed_hooks else None
    if backup is not None and (backup.exists() or backup.is_symlink()):
        raise FileExistsError(f"settings backup destination already exists: {backup}")

    skill_removed = False
    remove_skill_link = False
    if skill_target.is_symlink():
        try:
            remove_skill_link = skill_target.resolve() == Path(receipt["active_skill"])
        except OSError:
            remove_skill_link = False

    if removed_hooks:
        _backup(settings_path, backup)
        atomic_write_json(settings_path, updated_settings)
        settings_path.chmod(0o600)
    if remove_skill_link:
        skill_target.unlink()
        skill_removed = True
    return {
        "removed_hook_handlers": removed_hooks,
        "skill_removed": skill_removed,
        "settings_backup": str(backup) if backup else None,
        "state_root": str(state),
        "state_preserved": True,
        "bundle_preserved": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--install", action="store_true")
    action.add_argument("--uninstall", action="store_true")
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument("--source-root", default=str(SOURCE_ROOT))
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--state-root")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    claude_home = Path(args.claude_home).expanduser().resolve()
    state_root = Path(args.state_root).expanduser().resolve() if args.state_root else claude_home / "pmm-instinct-review-data"
    try:
        if args.check:
            result = check(claude_home=claude_home, state_root=state_root)
        elif args.install:
            result = install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=Path(args.source_root),
                mode=args.mode,
            )
        else:
            result = uninstall(claude_home=claude_home, state_root=state_root, confirm=args.confirm)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (FileExistsError, OSError, PermissionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
