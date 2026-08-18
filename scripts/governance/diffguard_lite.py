#!/usr/bin/env python3
"""Diff-scoped code-quality checker for pmm-engine.

Analyzes changed files against a base ref and reports size, Python complexity,
and test-health in text or JSON. In v1, only test-health failure is blocking;
size and complexity findings are advisory.
"""

import argparse
import ast
import fnmatch
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "diffguard-lite.yaml"
DEFAULT_TEST_COMMAND = ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]

DEFAULT_CONFIG = {
    "python": {
        "max_function_lines": 60,
        "max_file_lines": 400,
        "max_cyclomatic": 15,
        "max_cognitive_complexity": 15,
        "max_nesting_depth": 4,
    },
    "javascript": {
        "max_function_lines": 80,
        "max_file_lines": 500,
    },
    "doc_paths": ["docs/**", "**/*.md", "outputs/**"],
    "churn": {
        "window_days": 90,
        "high_threshold": 10,
    },
}


@dataclass
class Finding:
    file: str
    line_start: int
    line_end: int
    metric: str
    value: int
    threshold: int
    severity: str
    message: str


def changed_files(base: str, cwd: Path = REPO_ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:
    if not path.exists():
        return _clone(DEFAULT_CONFIG)
    with path.open() as f:
        loaded = yaml.safe_load(f) or {}
    merged = _clone(DEFAULT_CONFIG)
    for key in ("python", "javascript", "churn"):
        merged[key] = {**DEFAULT_CONFIG[key], **(loaded.get(key) or {})}
    if "doc_paths" in loaded:
        merged["doc_paths"] = list(loaded["doc_paths"])
    return merged


def _clone(cfg: dict) -> dict:
    return {
        "python": dict(cfg["python"]),
        "javascript": dict(cfg["javascript"]),
        "doc_paths": list(cfg["doc_paths"]),
        "churn": dict(cfg["churn"]),
    }


def _matches_pattern(path: str, pattern: str) -> bool:
    """gitignore-style match supporting `prefix/**` and `**/suffix`."""
    if pattern.endswith("/**"):
        prefix = pattern[:-3]
        return path == prefix or path.startswith(prefix + "/")
    if pattern.startswith("**/"):
        suffix = pattern[3:]
        return fnmatch.fnmatch(path, suffix) or fnmatch.fnmatch(Path(path).name, suffix)
    return fnmatch.fnmatch(path, pattern)


def is_doc_only(files: list[str], doc_patterns: list[str]) -> bool:
    if not files:
        return False
    return all(any(_matches_pattern(f, pat) for pat in doc_patterns) for f in files)


def _max_nesting(node: ast.AST, depth: int = 0) -> int:
    nesting_types = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.AsyncFor, ast.AsyncWith)
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, nesting_types):
            child_depth = _max_nesting(child, depth + 1)
        else:
            child_depth = _max_nesting(child, depth)
        if child_depth > max_depth:
            max_depth = child_depth
    return max_depth


def python_findings(file_path: Path, rel_path: str, cfg: dict) -> list[Finding]:
    from radon.complexity import cc_visit
    from cognitive_complexity.api import get_cognitive_complexity

    findings: list[Finding] = []
    try:
        source = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    lines = source.splitlines()
    if len(lines) > cfg["max_file_lines"]:
        findings.append(Finding(
            file=rel_path,
            line_start=1,
            line_end=len(lines),
            metric="python.file_lines",
            value=len(lines),
            threshold=cfg["max_file_lines"],
            severity="advisory",
            message=f"File is {len(lines)} lines (threshold {cfg['max_file_lines']}).",
        ))

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return findings

    try:
        complexities = {c.name: c for c in cc_visit(source)}
    except SyntaxError:
        complexities = {}

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        start = node.lineno
        end = getattr(node, "end_lineno", None) or start
        size = end - start + 1

        if size > cfg["max_function_lines"]:
            findings.append(Finding(
                file=rel_path,
                line_start=start,
                line_end=end,
                metric="python.function_lines",
                value=size,
                threshold=cfg["max_function_lines"],
                severity="advisory",
                message=f"Function `{node.name}` is {size} lines (threshold {cfg['max_function_lines']}).",
            ))

        nesting = _max_nesting(node)
        if nesting > cfg["max_nesting_depth"]:
            findings.append(Finding(
                file=rel_path,
                line_start=start,
                line_end=end,
                metric="python.nesting_depth",
                value=nesting,
                threshold=cfg["max_nesting_depth"],
                severity="advisory",
                message=f"Function `{node.name}` nesting depth {nesting} (threshold {cfg['max_nesting_depth']}).",
            ))

        try:
            cognitive = get_cognitive_complexity(node)
        except Exception:
            cognitive = 0
        if cognitive > cfg.get("max_cognitive_complexity", 15):
            findings.append(Finding(
                file=rel_path,
                line_start=start,
                line_end=end,
                metric="python.cognitive_complexity",
                value=cognitive,
                threshold=cfg["max_cognitive_complexity"],
                severity="advisory",
                message=f"Function `{node.name}` cognitive complexity {cognitive} (threshold {cfg['max_cognitive_complexity']}).",
            ))

        comp = complexities.get(node.name)
        if comp and comp.complexity > cfg["max_cyclomatic"]:
            findings.append(Finding(
                file=rel_path,
                line_start=start,
                line_end=end,
                metric="python.cyclomatic",
                value=comp.complexity,
                threshold=cfg["max_cyclomatic"],
                severity="advisory",
                message=f"Function `{node.name}` cyclomatic complexity {comp.complexity} (threshold {cfg['max_cyclomatic']}).",
            ))

    return findings


_JS_FUNC_PATTERN = re.compile(
    r"(?:^|\s|=|,)"
    r"(?:"
    r"function\s+(?P<named>\w+)\s*\("
    r"|function\s*\("
    r"|(?P<prop>\w+)\s*:\s*function"
    r"|(?P<arrow>\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>"
    r"|(?P<expr>\w+)\s*=\s*function"
    r"|(?P<method>\w+)\s*\([^)]*\)\s*\{"
    r")"
)


def js_function_ranges(source: str) -> list[tuple[str, int, int]]:
    """Return (name, line_start, line_end) for functions found in JS source.

    Uses regex signature detection + brace counting. Not parser-accurate but
    adequate for advisory size metrics on human-written source.
    """
    ranges: list[tuple[str, int, int]] = []
    for match in _JS_FUNC_PATTERN.finditer(source):
        name = next((g for g in (match.group("named"), match.group("prop"),
                                 match.group("arrow"), match.group("expr"),
                                 match.group("method")) if g), "<anonymous>")
        open_idx = source.find("{", match.end() - 1)
        if open_idx == -1:
            continue
        depth = 1
        j = open_idx + 1
        while j < len(source) and depth > 0:
            ch = source[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        if depth != 0:
            continue
        start_line = source.count("\n", 0, match.start()) + 1
        end_line = source.count("\n", 0, j) + 1
        ranges.append((name, start_line, end_line))
    return ranges


def js_findings(file_path: Path, rel_path: str, cfg: dict) -> list[Finding]:
    findings: list[Finding] = []
    try:
        source = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    lines = source.splitlines()
    if len(lines) > cfg["max_file_lines"]:
        findings.append(Finding(
            file=rel_path,
            line_start=1,
            line_end=len(lines),
            metric="javascript.file_lines",
            value=len(lines),
            threshold=cfg["max_file_lines"],
            severity="advisory",
            message=f"File is {len(lines)} lines (threshold {cfg['max_file_lines']}).",
        ))

    for name, start, end in js_function_ranges(source):
        size = end - start + 1
        if size > cfg["max_function_lines"]:
            findings.append(Finding(
                file=rel_path,
                line_start=start,
                line_end=end,
                metric="javascript.function_lines",
                value=size,
                threshold=cfg["max_function_lines"],
                severity="advisory",
                message=f"Function `{name}` is {size} lines (threshold {cfg['max_function_lines']}).",
            ))

    return findings


_TEST_OUTPUT_TAIL_LINES = 40


def churn_score_for(path: str, window_days: int, repo_root: Path = REPO_ROOT) -> int:
    """Number of commits touching `path` in the last `window_days`.

    Uses `git log --follow` so renames count toward the same file. Returns 0 on
    any error (missing git, deleted file, invalid date spec).
    """
    try:
        result = subprocess.run(
            ["git", "log", "--follow", f"--since={window_days} days ago",
             "--pretty=format:%H", "--", path],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except (FileNotFoundError, OSError):
        return 0
    if result.returncode != 0:
        return 0
    return sum(1 for line in result.stdout.splitlines() if line.strip())


def churn_findings(files: list[str], cfg: dict, repo_root: Path = REPO_ROOT) -> tuple[dict, list[Finding]]:
    """Compute churn score per file + emit high-churn findings.

    Returns (churn_scores, findings).
    """
    window = cfg.get("window_days", 90)
    threshold = cfg.get("high_threshold", 10)
    scores: dict = {}
    findings: list[Finding] = []
    for rel in files:
        score = churn_score_for(rel, window_days=window, repo_root=repo_root)
        scores[rel] = score
        if score > threshold:
            findings.append(Finding(
                file=rel,
                line_start=1,
                line_end=1,
                metric="churn.high_churn",
                value=score,
                threshold=threshold,
                severity="advisory",
                message=f"`{rel}` changed {score} times in the last {window} days (threshold {threshold}).",
            ))
    return scores, findings


def run_test_health(cwd: Path = REPO_ROOT, command: Optional[list[str]] = None) -> dict:
    cmd = command or DEFAULT_TEST_COMMAND
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    output = (result.stderr or "") + (result.stdout or "")
    count_match = re.search(r"Ran (\d+) tests?", output)
    count = int(count_match.group(1)) if count_match else 0
    status = "pass" if result.returncode == 0 else "fail"
    payload = {"status": status, "suite": "unittest", "count": count}
    if status == "fail":
        tail = "\n".join((result.stderr or "").splitlines()[-_TEST_OUTPUT_TAIL_LINES:])
        payload["failure_tail"] = tail
    return payload


def build_report(base: str, head: str, files: list[str], cfg: dict,
                 findings: list[Finding], test_health: dict,
                 churn_scores: Optional[dict] = None) -> dict:
    advisory = sum(1 for f in findings if f.severity == "advisory")
    blocking = sum(1 for f in findings if f.severity == "blocking")
    report = {
        "base": base,
        "head": head,
        "changed_files": files,
        "doc_only": is_doc_only(files, cfg["doc_paths"]),
        "findings": [asdict(f) for f in findings],
        "test_health": test_health,
        "summary": {"advisory": advisory, "blocking": blocking},
    }
    if churn_scores is not None:
        report["churn_scores"] = churn_scores
    return report


_MARKDOWN_MAX_FINDINGS = 10


def render_markdown(report: dict) -> str:
    """GitHub Actions-friendly summary. Counts + first 10 findings per Design section."""
    th = report["test_health"]
    out = [
        "## Diffguard-Lite Report",
        "",
        f"- **Base:** `{report['base']}`",
        f"- **Head:** `{report['head']}`",
        f"- **Changed files:** {len(report['changed_files'])}",
        f"- **Doc-only:** {'yes' if report['doc_only'] else 'no'}",
        f"- **Test-health:** {th['status']} ({th['count']} tests, {th['suite']})",
        f"- **Findings:** advisory={report['summary']['advisory']}, "
        f"blocking={report['summary']['blocking']}",
    ]
    findings = report["findings"]
    churn_scores = report.get("churn_scores") or {}
    # Identify high-churn files for the prefix marker.
    high_churn_files = {f["file"] for f in findings if f["metric"] == "churn.high_churn"}

    if findings:
        total = len(findings)
        shown = findings[:_MARKDOWN_MAX_FINDINGS]
        header = f"### Findings ({total})" if total <= _MARKDOWN_MAX_FINDINGS \
            else f"### Findings (showing first {_MARKDOWN_MAX_FINDINGS} of {total})"
        out += ["", header, ""]
        for f in shown:
            prefix = "⚠️ high-churn " if f["file"] in high_churn_files and f["metric"] != "churn.high_churn" else ""
            out.append(
                f"- {prefix}**[{f['severity']}]** `{f['file']}:{f['line_start']}-{f['line_end']}` "
                f"— `{f['metric']}={f['value']}` (threshold {f['threshold']}) — {f['message']}"
            )
    if th.get("failure_tail"):
        out += ["", "### Test failure tail", "", "```", th["failure_tail"], "```"]
    return "\n".join(out) + "\n"


def render_text(report: dict) -> str:
    out = [
        "diffguard-lite report",
        f"  base: {report['base']}",
        f"  head: {report['head']}",
        f"  changed files: {len(report['changed_files'])}",
        f"  doc-only: {report['doc_only']}",
        f"  test-health: {report['test_health']['status']} "
        f"({report['test_health']['count']} tests, {report['test_health']['suite']})",
        f"  findings: advisory={report['summary']['advisory']} blocking={report['summary']['blocking']}",
    ]
    for f in report["findings"]:
        out.append(
            f"    [{f['severity']}] {f['file']}:{f['line_start']}-{f['line_end']} "
            f"{f['metric']}={f['value']} threshold={f['threshold']} — {f['message']}"
        )
    return "\n".join(out)


def run_diffguard(base: str, config_path: Path, *, skip_test_health: bool = False,
                  repo_root: Path = REPO_ROOT) -> tuple[dict, int]:
    cfg = load_config(config_path)
    files = changed_files(base, cwd=repo_root)
    doc_only = is_doc_only(files, cfg["doc_paths"])

    findings: list[Finding] = []
    churn_scores: Optional[dict] = None
    if not doc_only:
        for rel in files:
            abs_path = repo_root / rel
            if not abs_path.exists():
                continue  # deleted or renamed
            if rel.endswith(".py"):
                findings.extend(python_findings(abs_path, rel, cfg["python"]))
            elif rel.endswith((".js", ".mjs", ".cjs", ".ts", ".tsx")):
                findings.extend(js_findings(abs_path, rel, cfg["javascript"]))

        churn_scores, churn_list = churn_findings(files, cfg.get("churn", {}), repo_root=repo_root)
        findings.extend(churn_list)

    if skip_test_health or doc_only:
        test_health = {"status": "skipped", "suite": "unittest", "count": 0}
    else:
        test_health = run_test_health(cwd=repo_root)

    report = build_report(base, "HEAD", files, cfg, findings, test_health, churn_scores)

    if test_health["status"] == "fail" or report["summary"]["blocking"] > 0:
        exit_code = 1
    else:
        exit_code = 0
    return report, exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Diff-scoped code-quality checker for pmm-engine.")
    parser.add_argument("--base", default=None,
                        help="Base ref (default: $DIFFGUARD_BASE or origin/main)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--config", default=None,
                        help=f"Config path (default: {DEFAULT_CONFIG_PATH})")
    parser.add_argument("--skip-tests", action="store_true",
                        help="Skip test-health run (useful for local iteration)")
    parser.add_argument("--render-from", default=None,
                        help="Render a previously-saved JSON report without re-running the checker")
    args = parser.parse_args()

    # Rendering-only mode: load JSON, emit in the requested format, no diff/test run.
    if args.render_from:
        try:
            report = json.loads(Path(args.render_from).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: could not read {args.render_from}: {exc}", file=sys.stderr)
            return 2
        if args.format == "json":
            print(json.dumps(report, indent=2))
        elif args.format == "markdown":
            print(render_markdown(report))
        else:
            print(render_text(report))
        return 0

    base = args.base or os.environ.get("DIFFGUARD_BASE", "origin/main")
    config_path = Path(args.config) if args.config else DEFAULT_CONFIG_PATH

    try:
        report, exit_code = run_diffguard(base, config_path, skip_test_health=args.skip_tests)
    except Exception as exc:  # pragma: no cover — catch-all for internal errors
        print(f"ERROR: diffguard-lite internal error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2))
    elif args.format == "markdown":
        print(render_markdown(report))
    else:
        print(render_text(report))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
