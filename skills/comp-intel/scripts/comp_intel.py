#!/usr/bin/env python3
"""Command-line entry point for the governed comp-intel controller."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from comp_intel_core import CompIntelController, WorkflowError


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="comp-intel", description="Governed competitive-intelligence workflow")
    subparsers = root.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="initialize an adopter-owned data root")
    _common(init)

    doctor = subparsers.add_parser("doctor", help="probe configured source capabilities")
    _common(doctor)
    doctor.add_argument("--market", required=True)

    collect = subparsers.add_parser("collect", help="collect evidence and stop at evidence review")
    _common(collect)
    collect.add_argument("--market", required=True)
    collect.add_argument("--from", dest="window_from", required=True)
    collect.add_argument("--to", dest="window_to", required=True)
    collect.add_argument("--observed-at")
    collect.add_argument("--run-id")
    collect.add_argument("--runtime-mode", choices=("interactive", "scheduled"), default="interactive")

    status = subparsers.add_parser("status", help="inspect one explicit run")
    _common(status)
    status.add_argument("--run-id", required=True)

    evidence = subparsers.add_parser("approve-evidence", help="install a digest-bound evidence approval")
    _common(evidence)
    evidence.add_argument("--run-id", required=True)
    evidence.add_argument("--approval-file", required=True, type=Path)
    evidence.add_argument("--invocation-mode", choices=("interactive", "scheduled"), default="interactive")

    synthesis = subparsers.add_parser("submit-synthesis", help="validate and stage a bounded synthesis package")
    _common(synthesis)
    synthesis.add_argument("--run-id", required=True)
    synthesis.add_argument("--package-file", required=True, type=Path)
    synthesis.add_argument("--invocation-mode", choices=("interactive", "scheduled"), default="interactive")

    approval = subparsers.add_parser("approve-apply", help="install a digest-bound change-set approval")
    _common(approval)
    approval.add_argument("--run-id", required=True)
    approval.add_argument("--approval-file", required=True, type=Path)
    approval.add_argument("--invocation-mode", choices=("interactive", "scheduled"), default="interactive")

    apply_parser = subparsers.add_parser("apply", help="transactionally apply an approved change set")
    _common(apply_parser)
    apply_parser.add_argument("--run-id", required=True)
    apply_parser.add_argument("--invocation-mode", choices=("interactive", "scheduled"), default="interactive")

    validate = subparsers.add_parser("validate", help="validate configuration and optional run state")
    _common(validate)
    validate.add_argument("--run-id")
    validate.add_argument("--market")
    return root


def _common(command: argparse.ArgumentParser) -> None:
    command.add_argument("--data-root", required=True, type=Path)
    command.add_argument("--json", action="store_true", dest="as_json")


def execute(arguments: argparse.Namespace) -> dict[str, Any]:
    controller = CompIntelController(arguments.data_root)
    if arguments.command == "init":
        return controller.init()
    if arguments.command == "doctor":
        return controller.doctor(arguments.market)
    if arguments.command == "collect":
        return controller.collect(
            arguments.market,
            arguments.window_from,
            arguments.window_to,
            observed_at=arguments.observed_at,
            run_id=arguments.run_id,
            runtime_mode=arguments.runtime_mode,
        )
    if arguments.command == "status":
        return controller.status(arguments.run_id)
    if arguments.command == "approve-evidence":
        return controller.install_evidence_approval(
            arguments.run_id, arguments.approval_file, invocation_mode=arguments.invocation_mode
        )
    if arguments.command == "submit-synthesis":
        return controller.submit_synthesis(
            arguments.run_id, arguments.package_file, invocation_mode=arguments.invocation_mode
        )
    if arguments.command == "approve-apply":
        return controller.install_apply_approval(
            arguments.run_id, arguments.approval_file, invocation_mode=arguments.invocation_mode
        )
    if arguments.command == "apply":
        return controller.apply(arguments.run_id, invocation_mode=arguments.invocation_mode)
    if arguments.command == "validate":
        return controller.validate(arguments.run_id, arguments.market)
    raise WorkflowError("usage/config", f"unsupported command: {arguments.command}")


def print_human(result: dict[str, Any]) -> None:
    print(result["message"])
    if result.get("run_id"):
        print(f"Run: {result['run_id']}")
    if result.get("stage"):
        print(f"Stage: {result['stage']}")
    for warning in result.get("warnings", []):
        print(f"Warning: {warning}")
    for action in result.get("next_actions", []):
        print(f"Next: {action}")


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        result = execute(arguments)
    except WorkflowError as exc:
        result = exc.result()
    except (OSError, ValueError) as exc:
        result = WorkflowError("validation", str(exc)).result()
    if arguments.as_json:
        print(json.dumps(result, sort_keys=True))
    else:
        print_human(result)
    return int(result["code"])


if __name__ == "__main__":
    raise SystemExit(main())
