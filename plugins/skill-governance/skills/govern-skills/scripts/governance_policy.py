#!/usr/bin/env python3
"""Shared fail-closed policy decisions for governed agent actions."""

from __future__ import annotations

import fnmatch
import json
import re
import shlex
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


POLICY_PATH = Path(".agents/governance/enforcement.yaml")
RESULTS = {"allow", "deny", "require-human"}
SENSITIVE_ACTIONS = {
    "approval",
    "human-transition",
    "policy-mutation",
    "publication",
    "run-state-mutation",
}
SCHEDULED_FORBIDDEN = {"approval", "human-transition", "publication"}
PUBLISH_RE = re.compile(
    r"(?:\bpublish(?:er|ing)?\b|\brelease\b|\bgit\s+push\b|\bgh\s+pr\s+merge\b|"
    r"\b(?:npm|pnpm|yarn)\s+publish\b|\btwine\s+upload\b|\bdocker\s+push\b|"
    r"curl\s+[^\n]*(?:(?:-X|--request)\s*(?:POST|PUT|PATCH|DELETE)|"
    r"(?:-d|--data(?:-binary|-raw|-urlencode)?|-F|--form|-T|--upload-file)(?:\s|=))|"
    r"gh\s+api\s+[^\n]*(?:-X|--method)\s*(?:POST|PUT|PATCH|DELETE))",
    re.IGNORECASE,
)
CONTROL_RE = re.compile(r"(?:^|[ /\"'])governance_control\.py(?:[\s\"']|$)")
PUBLISHER_GUARD_RE = re.compile(r"(?:^|[ /\"'])publisher_guard\.py(?:[\s\"']|$)")
SHELL_CONTROL_RE = re.compile(r"[\n\r;&|<>`]|\$\(")
CONTROL_OPERATIONS = (
    "record-approval",
    "transition",
    "add-artifact",
    "can-publish",
    "validate-all",
    "validate",
    "init",
)


class PolicyError(ValueError):
    """Raised when a governance policy or request is invalid."""


@dataclass(frozen=True)
class Decision:
    result: str
    reason_code: str
    explanation: str
    enforcement_class: str
    harness: str
    action_class: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def read_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError as exc:
            raise PolicyError(
                f"{path}: use JSON-compatible YAML or install PyYAML"
            ) from exc
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # type: ignore[attr-defined]
            raise PolicyError(f"{path}: invalid YAML: {exc}") from exc


def json_yaml(value: Any) -> str:
    """Return JSON, which is valid YAML 1.2 and dependency-free to parse."""
    return json.dumps(value, indent=2, sort_keys=False) + "\n"


def default_policy() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "enabled": False,
        "mode": "enforce",
        "execution_mode": "interactive",
        "run_state_globs": ["state/runs/*.yaml", "state/runs/**/*.yaml"],
        "protected_path_globs": [
            ".agents/governance/**",
            ".claude/settings*.json",
            ".codex/**",
        ],
        "publisher_tool_globs": ["mcp__*publish*", "*publisher*", "*send_message*"],
    }


def load_policy(repo: Path) -> tuple[Path, dict[str, Any]]:
    path = repo.resolve() / POLICY_PATH
    if not path.is_file():
        return path, default_policy()
    data = read_structured(path)
    if not isinstance(data, dict):
        raise PolicyError("enforcement policy must be a mapping")
    if data.get("schema_version") != 1:
        raise PolicyError("enforcement policy schema_version must be 1")
    if not isinstance(data.get("enabled"), bool):
        raise PolicyError("enforcement policy enabled must be boolean")
    if data.get("mode") not in {"audit", "enforce"}:
        raise PolicyError("enforcement policy mode must be audit or enforce")
    if data.get("execution_mode") not in {"interactive", "scheduled"}:
        raise PolicyError("execution_mode must be interactive or scheduled")
    for key in ("run_state_globs", "protected_path_globs", "publisher_tool_globs"):
        values = data.get(key, [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise PolicyError(f"{key} must be a list of strings")
    return path, data


def find_repo(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / POLICY_PATH).is_file() or (candidate / ".git").exists():
            return candidate
    return None


def _relative_path(repo: Path, raw: str) -> str | None:
    if not raw:
        return None
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = repo / candidate
    try:
        return candidate.resolve(strict=False).relative_to(repo.resolve()).as_posix()
    except ValueError:
        return None


def _matches_any(value: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(value, pattern) for pattern in patterns)


def classify_request(request: dict[str, Any], policy: dict[str, Any], repo: Path) -> str:
    explicit = request.get("action_class")
    if explicit in SENSITIVE_ACTIONS or explicit == "read-only":
        return str(explicit)

    tool_name = str(request.get("tool_name", ""))
    command = str(request.get("command", ""))
    operation = str(request.get("operation", ""))
    controlled = bool(request.get("controlled"))

    if operation in {"approve", "record-approval"}:
        return "approval"
    if operation in {"transition", "advance-review", "publish-ready"}:
        return "human-transition"
    if operation in {"publish", "external-write"}:
        return "publication"

    paths = request.get("target_paths", [])
    if not isinstance(paths, list):
        paths = []
    for raw in paths:
        if not isinstance(raw, str):
            continue
        relative = _relative_path(repo, raw)
        if relative is None:
            continue
        if _matches_any(relative, list(policy.get("protected_path_globs", []))):
            return "policy-mutation"
        if _matches_any(relative, list(policy.get("run_state_globs", []))):
            return "run-state-mutation"

    normalized_command = command.replace("\\", "/")
    if not controlled and any(
        marker in normalized_command
        for marker in (".agents/governance/", ".claude/settings", ".codex/")
    ):
        return "policy-mutation"
    if not controlled and "state/runs/" in normalized_command:
        return "run-state-mutation"

    if _matches_any(tool_name, list(policy.get("publisher_tool_globs", []))):
        return "publication"
    if command and PUBLISH_RE.search(command):
        if controlled and PUBLISHER_GUARD_RE.search(command):
            return "publication"
        return "publication"
    return "read-only"


def decide(request: dict[str, Any], policy: dict[str, Any], repo: Path) -> Decision:
    harness = str(request.get("harness", "unknown"))
    if harness not in {"claude", "codex", "internal"}:
        return Decision(
            "deny",
            "GOV_INVALID_HARNESS",
            "The request names an unsupported harness.",
            "runtime-guard",
            harness,
            "unknown",
        )

    action = classify_request(request, policy, repo)
    if not policy.get("enabled"):
        return Decision(
            "allow",
            "GOV_RUNTIME_GUARD_INACTIVE",
            "Repository runtime enforcement is not enabled; only documented and static controls apply.",
            "instruction-only",
            harness,
            action,
        )

    execution_mode = str(request.get("execution_mode") or policy.get("execution_mode"))
    controlled = bool(request.get("controlled"))
    if execution_mode == "scheduled" and action in SCHEDULED_FORBIDDEN:
        decision = Decision(
            "deny",
            "GOV_SCHEDULED_AUTHORITY_FORBIDDEN",
            "Scheduled execution cannot approve, advance a human gate, or publish.",
            "runtime-guard",
            harness,
            action,
        )
    elif action == "policy-mutation":
        decision = Decision(
            "deny",
            "GOV_POLICY_PATH_PROTECTED",
            "Agent tools cannot modify protected governance configuration.",
            "capability-boundary",
            harness,
            action,
        )
    elif action == "run-state-mutation" and not controlled:
        decision = Decision(
            "deny",
            "GOV_DIRECT_STATE_MUTATION",
            "Run state must be changed through the governed control command.",
            "runtime-guard",
            harness,
            action,
        )
    elif action == "approval" and not controlled:
        decision = Decision(
            "require-human",
            "GOV_EXTERNAL_APPROVAL_REQUIRED",
            "Approval requires an independently verified external authority event.",
            "external-authority",
            harness,
            action,
        )
    elif action == "human-transition" and not controlled:
        decision = Decision(
            "deny",
            "GOV_CONTROLLED_TRANSITION_REQUIRED",
            "Human-gate transitions must use the governed control command.",
            "runtime-guard",
            harness,
            action,
        )
    elif action == "publication" and not (
        controlled and bool(request.get("publisher_guard"))
    ):
        decision = Decision(
            "deny",
            "GOV_PUBLISHER_GUARD_REQUIRED",
            "Publication is available only through the approved publisher guard.",
            "capability-boundary",
            harness,
            action,
        )
    else:
        decision = Decision(
            "allow",
            "GOV_POLICY_ALLOW",
            "The request is allowed by the active governance policy.",
            "runtime-guard",
            harness,
            action,
        )

    if policy.get("mode") == "audit" and decision.result != "allow":
        return Decision(
            "allow",
            f"GOV_AUDIT_{decision.reason_code}",
            f"Audit mode would have blocked this request: {decision.explanation}",
            "static-validator",
            harness,
            action,
        )
    return decision


def decision_record(decision: Decision) -> str:
    """Serialize only non-sensitive decision metadata."""
    return json.dumps(decision.to_dict(), sort_keys=True)


def command_metadata(command: str) -> tuple[str | None, bool, bool]:
    """Extract only the control operation and trusted-wrapper flags from a shell command."""
    operation: str | None = None
    has_control = bool(CONTROL_RE.search(command))
    has_publisher_guard = bool(PUBLISHER_GUARD_RE.search(command))
    if CONTROL_RE.search(command):
        for candidate in CONTROL_OPERATIONS:
            if re.search(rf"(?:^|\s){re.escape(candidate)}(?:\s|$)", command):
                operation = candidate
                break
    elif has_publisher_guard:
        operation = "publish"

    # A wrapper name is not a trust signal when it appears beside shell control syntax.
    # The hook blocks the complete tool call, so fail closed before token inspection.
    if SHELL_CONTROL_RE.search(command):
        return operation, False, False
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return operation, False, False
    if not tokens:
        return operation, False, False

    script_index = 0
    executable = Path(tokens[0]).name
    if re.fullmatch(r"python(?:3(?:\.\d+)?)?", executable):
        script_index = 1
    elif executable == "env" and len(tokens) >= 3 and re.fullmatch(
        r"python(?:3(?:\.\d+)?)?", Path(tokens[1]).name
    ):
        script_index = 2
    if script_index >= len(tokens):
        return operation, False, False

    script_name = Path(tokens[script_index]).name
    if script_name == "governance_control.py" and has_control:
        return operation, True, False
    if script_name == "publisher_guard.py" and has_publisher_guard:
        return "publish", True, True
    return operation, False, False
