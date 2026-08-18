#!/usr/bin/env python3
"""Classify Git worktrees and remove only explicitly selected clean candidates."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, text=True, capture_output=True
    ).stdout


def worktrees(repo: Path) -> list[dict[str, str]]:
    blocks = git(repo, "worktree", "list", "--porcelain").strip().split("\n\n")
    result: list[dict[str, str]] = []
    current = Path(git(repo, "rev-parse", "--show-toplevel").strip()).resolve()
    for block in blocks:
        fields: dict[str, str] = {}
        for line in block.splitlines():
            key, _, value = line.partition(" ")
            fields[key] = value
        path = Path(fields.get("worktree", "")).resolve()
        branch = fields.get("branch", "").removeprefix("refs/heads/")
        dirty = bool(git(path, "status", "--porcelain"))
        merged = False
        if branch:
            merged = subprocess.run(
                ["git", "-C", str(repo), "merge-base", "--is-ancestor", branch, "HEAD"],
                capture_output=True,
            ).returncode == 0
        if path == current:
            classification = "protected-current"
        elif fields.get("locked") is not None:
            classification = "protected-locked"
        elif dirty:
            classification = "dirty"
        elif branch and merged:
            classification = "merged-and-clean"
        elif not branch:
            classification = "detached-and-clean"
        else:
            classification = "unmerged"
        result.append({"path": str(path), "branch": branch, "classification": classification})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--target", action="append", default=[])
    args = parser.parse_args()
    rows = worktrees(args.repo)
    if args.apply:
        approved = {str(Path(path).resolve()) for path in args.target}
        for row in rows:
            if row["path"] in approved:
                if row["classification"] not in {"merged-and-clean", "detached-and-clean"}:
                    parser.error(f"refusing unsafe target {row['path']}: {row['classification']}")
                subprocess.run(["git", "-C", str(args.repo), "worktree", "remove", row["path"]], check=True)
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
