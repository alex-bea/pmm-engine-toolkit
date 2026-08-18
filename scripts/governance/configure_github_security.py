#!/usr/bin/env python3
"""Plan, apply, or verify the public repository's GitHub security controls."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "config" / "github-security-controls.json"
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class SecurityControlsError(RuntimeError):
    """Raised when policy application or verification cannot continue safely."""


def load_policy(path: Path) -> dict[str, Any]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SecurityControlsError(f"cannot load policy {path}: {exc}") from exc
    validate_policy(policy)
    return policy


def validate_policy(policy: dict[str, Any]) -> None:
    errors: list[str] = []
    repository = policy.get("repository", {})
    actions = policy.get("actions", {})
    ruleset = policy.get("ruleset", {})

    if policy.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(policy.get("api_version", ""))):
        errors.append("api_version must be an ISO date")
    if repository.get("required_visibility") != "public":
        errors.append("repository visibility must be public")
    if repository.get("required_default_branch") != "main":
        errors.append("default branch must be main")

    security = repository.get("security_and_analysis", {})
    for feature in ("secret_scanning", "secret_scanning_push_protection"):
        if security.get(feature, {}).get("status") != "enabled":
            errors.append(f"{feature} must be enabled")

    permissions = actions.get("permissions", {})
    if permissions != {
        "enabled": True,
        "allowed_actions": "selected",
        "sha_pinning_required": True,
    }:
        errors.append("Actions must require selected, full-SHA-pinned actions")
    if actions.get("selected_actions") != {
        "github_owned_allowed": True,
        "verified_allowed": False,
        "patterns_allowed": [],
    }:
        errors.append("only GitHub-owned actions may run")
    if actions.get("workflow_permissions") != {
        "default_workflow_permissions": "read",
        "can_approve_pull_request_reviews": False,
    }:
        errors.append("default workflow permissions must be read-only without PR approval")

    if policy.get("dependency_security") != {
        "vulnerability_alerts": True,
        "dependabot_security_updates": True,
    }:
        errors.append("dependency alerts and security updates must be enabled")
    if policy.get("private_vulnerability_reporting") is not True:
        errors.append("private vulnerability reporting must be enabled")

    if ruleset.get("enforcement") != "active" or ruleset.get("bypass_actors") != []:
        errors.append("ruleset must be active with no bypass actors")
    include = ruleset.get("conditions", {}).get("ref_name", {}).get("include")
    if include != ["~DEFAULT_BRANCH"]:
        errors.append("ruleset must target the default branch")
    rule_types = [rule.get("type") for rule in ruleset.get("rules", [])]
    required_types = {
        "deletion",
        "non_fast_forward",
        "required_linear_history",
        "pull_request",
        "required_status_checks",
    }
    if set(rule_types) != required_types or len(rule_types) != len(required_types):
        errors.append("ruleset rule inventory does not match the public baseline")

    rules = {rule.get("type"): rule for rule in ruleset.get("rules", [])}
    pull_request = rules.get("pull_request", {}).get("parameters", {})
    expected_pull_request = {
        "allowed_merge_methods": ["squash"],
        "dismiss_stale_reviews_on_push": True,
        "require_code_owner_review": False,
        "require_last_push_approval": True,
        "required_approving_review_count": 1,
        "required_review_thread_resolution": True,
    }
    if pull_request != expected_pull_request:
        errors.append("pull-request review policy differs from the public baseline")

    checks = rules.get("required_status_checks", {}).get("parameters", {})
    expected_contexts = {
        *(f"Tests (Python 3.{minor})" for minor in range(10, 15)),
        "Governance",
        "CodeQL",
    }
    actual_contexts = {
        check.get("context") for check in checks.get("required_status_checks", [])
    }
    if actual_contexts != expected_contexts:
        errors.append("required status-check inventory differs from the workflow contract")
    if checks.get("strict_required_status_checks_policy") is not True:
        errors.append("required status checks must use the latest default-branch code")

    if errors:
        raise SecurityControlsError("invalid security policy: " + "; ".join(errors))


def parse_repo(value: str) -> str:
    value = value.strip()
    if not REPO_RE.fullmatch(value):
        raise argparse.ArgumentTypeError("repository must use OWNER/REPOSITORY format")
    return value


def endpoint(repo: str, suffix: str = "") -> str:
    return f"repos/{repo}{suffix}"


def build_plan(policy: dict[str, Any], repo: str) -> list[dict[str, Any]]:
    repository = policy["repository"]
    actions = policy["actions"]
    return [
        {
            "method": "PATCH",
            "endpoint": endpoint(repo),
            "payload": {
                **repository["settings"],
                "security_and_analysis": repository["security_and_analysis"],
            },
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/actions/permissions"),
            "payload": actions["permissions"],
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/actions/permissions/selected-actions"),
            "payload": actions["selected_actions"],
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/actions/permissions/workflow"),
            "payload": actions["workflow_permissions"],
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/vulnerability-alerts"),
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/automated-security-fixes"),
        },
        {
            "method": "PUT",
            "endpoint": endpoint(repo, "/private-vulnerability-reporting"),
        },
        {
            "method": "UPSERT",
            "endpoint": endpoint(repo, "/rulesets"),
            "payload": policy["ruleset"],
        },
    ]


def gh_api(
    method: str,
    api_endpoint: str,
    api_version: str,
    payload: dict[str, Any] | None = None,
) -> Any:
    command = [
        "gh",
        "api",
        "--method",
        method,
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        f"X-GitHub-Api-Version: {api_version}",
        api_endpoint,
    ]
    stdin = None
    if payload is not None:
        command.extend(["--input", "-"])
        stdin = json.dumps(payload)
    try:
        result = subprocess.run(
            command,
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise SecurityControlsError("GitHub CLI is required for apply and verify modes") from exc
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown GitHub API error"
        raise SecurityControlsError(f"GitHub API {method} {api_endpoint} failed: {detail}")
    output = result.stdout.strip()
    if not output:
        return None
    try:
        return json.loads(output)
    except json.JSONDecodeError as exc:
        raise SecurityControlsError(
            f"GitHub API {method} {api_endpoint} returned invalid JSON"
        ) from exc


def require_public_main(metadata: dict[str, Any], policy: dict[str, Any]) -> None:
    repository = policy["repository"]
    actual_visibility = metadata.get("visibility")
    actual_default = metadata.get("default_branch")
    if actual_visibility != repository["required_visibility"]:
        raise SecurityControlsError(
            f"refusing to mutate repository with visibility {actual_visibility!r}"
        )
    if actual_default != repository["required_default_branch"]:
        raise SecurityControlsError(
            f"refusing to mutate repository with default branch {actual_default!r}"
        )


def upsert_ruleset(policy: dict[str, Any], repo: str) -> None:
    api_version = policy["api_version"]
    desired = policy["ruleset"]
    rulesets = gh_api("GET", endpoint(repo, "/rulesets"), api_version)
    if not isinstance(rulesets, list):
        raise SecurityControlsError("GitHub ruleset listing returned an unexpected response")
    matches = [item for item in rulesets if item.get("name") == desired["name"]]
    if len(matches) > 1:
        raise SecurityControlsError(f"multiple rulesets are named {desired['name']!r}")
    if matches:
        ruleset_id = matches[0].get("id")
        gh_api("PUT", endpoint(repo, f"/rulesets/{ruleset_id}"), api_version, desired)
    else:
        gh_api("POST", endpoint(repo, "/rulesets"), api_version, desired)


def apply_policy(policy: dict[str, Any], repo: str) -> None:
    api_version = policy["api_version"]
    metadata = gh_api("GET", endpoint(repo), api_version)
    if not isinstance(metadata, dict):
        raise SecurityControlsError("repository metadata returned an unexpected response")
    require_public_main(metadata, policy)

    for operation in build_plan(policy, repo):
        if operation["method"] == "UPSERT":
            upsert_ruleset(policy, repo)
            continue
        gh_api(
            operation["method"],
            operation["endpoint"],
            api_version,
            operation.get("payload"),
        )


def assert_subset(expected: Any, actual: Any, label: str) -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise SecurityControlsError(f"{label} is not an object")
        for key, expected_value in expected.items():
            if key not in actual:
                raise SecurityControlsError(f"{label}.{key} is missing")
            assert_subset(expected_value, actual[key], f"{label}.{key}")
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise SecurityControlsError(f"{label} differs from desired state")
        for index, (expected_value, actual_value) in enumerate(zip(expected, actual)):
            assert_subset(expected_value, actual_value, f"{label}[{index}]")
        return
    if expected != actual:
        raise SecurityControlsError(
            f"{label} is {actual!r}; expected {expected!r}"
        )


def verify_ruleset(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    for field in ("name", "target", "enforcement", "bypass_actors", "conditions"):
        assert_subset(expected[field], actual.get(field), f"ruleset.{field}")
    expected_rules = {rule["type"]: rule for rule in expected["rules"]}
    actual_rules = {rule.get("type"): rule for rule in actual.get("rules", [])}
    if set(actual_rules) != set(expected_rules):
        raise SecurityControlsError("ruleset rule inventory differs from desired state")
    for rule_type, expected_rule in expected_rules.items():
        assert_subset(expected_rule, actual_rules[rule_type], f"ruleset.rules.{rule_type}")


def verify_policy(policy: dict[str, Any], repo: str) -> None:
    api_version = policy["api_version"]
    metadata = gh_api("GET", endpoint(repo), api_version)
    if not isinstance(metadata, dict):
        raise SecurityControlsError("repository metadata returned an unexpected response")
    require_public_main(metadata, policy)
    assert_subset(policy["repository"]["settings"], metadata, "repository")
    assert_subset(
        policy["repository"]["security_and_analysis"],
        metadata.get("security_and_analysis"),
        "repository.security_and_analysis",
    )

    checks = (
        ("/actions/permissions", policy["actions"]["permissions"]),
        ("/actions/permissions/selected-actions", policy["actions"]["selected_actions"]),
        ("/actions/permissions/workflow", policy["actions"]["workflow_permissions"]),
    )
    for suffix, expected in checks:
        actual = gh_api("GET", endpoint(repo, suffix), api_version)
        assert_subset(expected, actual, suffix)

    gh_api("GET", endpoint(repo, "/vulnerability-alerts"), api_version)
    automated = gh_api("GET", endpoint(repo, "/automated-security-fixes"), api_version)
    assert_subset({"enabled": True}, automated, "dependabot_security_updates")
    reporting = gh_api("GET", endpoint(repo, "/private-vulnerability-reporting"), api_version)
    assert_subset({"enabled": True}, reporting, "private_vulnerability_reporting")

    rulesets = gh_api("GET", endpoint(repo, "/rulesets"), api_version)
    if not isinstance(rulesets, list):
        raise SecurityControlsError("GitHub ruleset listing returned an unexpected response")
    matches = [item for item in rulesets if item.get("name") == policy["ruleset"]["name"]]
    if len(matches) != 1:
        raise SecurityControlsError("expected exactly one managed default-branch ruleset")
    ruleset_id = matches[0].get("id")
    full_ruleset = gh_api("GET", endpoint(repo, f"/rulesets/{ruleset_id}"), api_version)
    if not isinstance(full_ruleset, dict):
        raise SecurityControlsError("GitHub ruleset detail returned an unexpected response")
    verify_ruleset(policy["ruleset"], full_ruleset)

    analyses = gh_api("GET", endpoint(repo, "/code-scanning/analyses?per_page=1"), api_version)
    if not isinstance(analyses, list) or not analyses:
        raise SecurityControlsError("CodeQL has not uploaded a code-scanning analysis")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--repo", required=True, type=parse_repo, help="OWNER/REPOSITORY")
    result.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    modes = result.add_mutually_exclusive_group()
    modes.add_argument("--plan", action="store_const", const="plan", dest="mode")
    modes.add_argument("--apply", action="store_const", const="apply", dest="mode")
    modes.add_argument("--verify", action="store_const", const="verify", dest="mode")
    result.set_defaults(mode="plan")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        policy = load_policy(args.policy)
        if args.mode == "plan":
            print(json.dumps({"repository": args.repo, "operations": build_plan(policy, args.repo)}, indent=2))
        elif args.mode == "apply":
            apply_policy(policy, args.repo)
            print(f"Applied GitHub security controls to {args.repo}.")
            print("Run --verify after the first CodeQL workflow completes on main.")
        else:
            verify_policy(policy, args.repo)
            print(f"Verified GitHub security controls for {args.repo}.")
    except SecurityControlsError as exc:
        print(f"Security controls failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
