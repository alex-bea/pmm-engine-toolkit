import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "diffguard_lite.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "diffguard_lite"


def load_module():
    spec = importlib.util.spec_from_file_location("diffguard_lite", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class DiffguardLiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = load_module()

    # --- doc-only detection ---

    def test_is_doc_only_true_when_all_match(self):
        self.assertTrue(self.m.is_doc_only(
            ["docs/foo.md", "README.md", "outputs/report.md"],
            ["docs/**", "**/*.md", "outputs/**"],
        ))

    def test_is_doc_only_false_when_any_unmatched(self):
        self.assertFalse(self.m.is_doc_only(
            ["docs/foo.md", "scripts/bar.py"],
            ["docs/**", "**/*.md", "outputs/**"],
        ))

    def test_is_doc_only_false_for_empty(self):
        self.assertFalse(self.m.is_doc_only([], ["docs/**"]))

    # --- config ---

    def test_load_config_defaults_when_missing(self):
        cfg = self.m.load_config(Path("/nonexistent/path/diffguard-lite.yaml"))
        self.assertEqual(cfg["python"]["max_function_lines"], 60)
        self.assertIn("docs/**", cfg["doc_paths"])

    def test_load_config_merges_loaded_over_defaults(self):
        import tempfile
        import yaml
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            yaml.safe_dump({"python": {"max_function_lines": 10}}, f)
            path = Path(f.name)
        try:
            cfg = self.m.load_config(path)
            self.assertEqual(cfg["python"]["max_function_lines"], 10)
            # Unspecified defaults still present
            self.assertEqual(cfg["python"]["max_file_lines"], 400)
        finally:
            path.unlink()

    # --- python metrics ---

    def test_python_findings_detects_long_function(self):
        # Use a tight threshold so the fixture deterministically triggers the finding
        cfg = {"max_function_lines": 20, "max_file_lines": 1000,
               "max_cyclomatic": 15, "max_cognitive_complexity": 15,
               "max_nesting_depth": 4}
        findings = self.m.python_findings(
            FIXTURES / "sample_long_function.py",
            "tests/fixtures/diffguard_lite/sample_long_function.py",
            cfg,
        )
        metrics = {f.metric for f in findings}
        self.assertIn("python.function_lines", metrics)

    def test_python_findings_detects_complexity_and_nesting(self):
        # Tight thresholds so the fixture deterministically triggers both findings
        cfg = {"max_function_lines": 200, "max_file_lines": 1000,
               "max_cyclomatic": 5, "max_cognitive_complexity": 100,
               "max_nesting_depth": 3}
        findings = self.m.python_findings(
            FIXTURES / "sample_complex.py",
            "tests/fixtures/diffguard_lite/sample_complex.py",
            cfg,
        )
        metrics = {f.metric for f in findings}
        self.assertIn("python.cyclomatic", metrics)
        self.assertIn("python.nesting_depth", metrics)

    def test_python_findings_detects_cognitive_complexity(self):
        # sample_complex.py has nested branches → high cognitive complexity
        cfg = {"max_function_lines": 200, "max_file_lines": 1000,
               "max_cyclomatic": 100, "max_cognitive_complexity": 5,
               "max_nesting_depth": 100}
        findings = self.m.python_findings(
            FIXTURES / "sample_complex.py",
            "tests/fixtures/diffguard_lite/sample_complex.py",
            cfg,
        )
        metrics = {f.metric for f in findings}
        self.assertIn("python.cognitive_complexity", metrics)
        # Cognitive > cyclomatic for this fixture (nesting penalty)
        cognitive = next(f for f in findings if f.metric == "python.cognitive_complexity")
        self.assertGreater(cognitive.value, 5)

    def test_python_findings_clean_file_produces_none(self):
        cfg = self.m.DEFAULT_CONFIG["python"]
        findings = self.m.python_findings(
            FIXTURES / "sample_ok.py",
            "tests/fixtures/diffguard_lite/sample_ok.py",
            cfg,
        )
        self.assertEqual(findings, [])

    def test_python_findings_handles_syntax_error(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
            f.write("def broken(:\n    pass\n")
            path = Path(f.name)
        try:
            cfg = self.m.DEFAULT_CONFIG["python"]
            # Should return without raising
            findings = self.m.python_findings(path, "broken.py", cfg)
            # File-size may still produce a finding; just confirm no crash
            self.assertIsInstance(findings, list)
        finally:
            path.unlink()

    # --- javascript metrics ---

    def test_js_function_ranges_detects_forms(self):
        source = (FIXTURES / "sample.js").read_text()
        ranges = self.m.js_function_ranges(source)
        names = {r[0] for r in ranges}
        # Covers named function, arrow (named binding), property-method function
        self.assertIn("small", names)
        self.assertIn("arrowLong", names)

    def test_js_findings_flags_long_function(self):
        cfg = {"max_function_lines": 8, "max_file_lines": 500}
        findings = self.m.js_findings(
            FIXTURES / "sample.js",
            "tests/fixtures/diffguard_lite/sample.js",
            cfg,
        )
        metrics = {f.metric for f in findings}
        self.assertIn("javascript.function_lines", metrics)

    # --- reporter ---

    def test_build_report_counts_severities(self):
        findings = [
            self.m.Finding("a.py", 1, 2, "python.file_lines", 500, 400,
                           "advisory", "x"),
            self.m.Finding("b.py", 1, 2, "python.cyclomatic", 20, 15,
                           "blocking", "y"),
        ]
        cfg = self.m.DEFAULT_CONFIG
        report = self.m.build_report("origin/main", "HEAD", ["a.py", "b.py"], cfg,
                                     findings, {"status": "pass", "suite": "unittest", "count": 1})
        self.assertEqual(report["summary"]["advisory"], 1)
        self.assertEqual(report["summary"]["blocking"], 1)

    def test_build_report_sets_doc_only(self):
        cfg = self.m.DEFAULT_CONFIG
        report = self.m.build_report(
            "origin/main", "HEAD", ["docs/foo.md"], cfg, [],
            {"status": "skipped", "suite": "unittest", "count": 0},
        )
        self.assertTrue(report["doc_only"])

    # --- churn ---

    def test_churn_findings_flags_high_churn_file(self):
        with mock.patch.object(self.m, "churn_score_for", side_effect=lambda p, window_days, repo_root=None: 15 if p == "hot.py" else 2):
            scores, findings = self.m.churn_findings(
                ["hot.py", "cold.py"],
                {"window_days": 90, "high_threshold": 10},
                repo_root=Path("/"),
            )
        self.assertEqual(scores, {"hot.py": 15, "cold.py": 2})
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].metric, "churn.high_churn")
        self.assertEqual(findings[0].value, 15)

    def test_churn_findings_empty_file_list(self):
        scores, findings = self.m.churn_findings(
            [],
            {"window_days": 90, "high_threshold": 10},
            repo_root=Path("/"),
        )
        self.assertEqual(scores, {})
        self.assertEqual(findings, [])

    def test_render_markdown_marks_high_churn_findings(self):
        report = {
            "base": "origin/main", "head": "HEAD",
            "changed_files": ["hot.py"],
            "doc_only": False,
            "findings": [
                {"file": "hot.py", "line_start": 1, "line_end": 1,
                 "metric": "churn.high_churn", "value": 15, "threshold": 10,
                 "severity": "advisory", "message": "high churn"},
                {"file": "hot.py", "line_start": 42, "line_end": 150,
                 "metric": "python.function_lines", "value": 108, "threshold": 60,
                 "severity": "advisory", "message": "long fn"},
            ],
            "test_health": {"status": "pass", "suite": "unittest", "count": 1},
            "summary": {"advisory": 2, "blocking": 0},
            "churn_scores": {"hot.py": 15},
        }
        md = self.m.render_markdown(report)
        # Non-churn findings in a high-churn file get the ⚠️ prefix
        self.assertIn("⚠️ high-churn", md)
        # The churn.high_churn finding itself does not get the prefix
        self.assertIn("`python.function_lines=108`", md)

    def test_render_markdown_includes_key_fields(self):
        report = {
            "base": "origin/main",
            "head": "HEAD",
            "changed_files": ["scripts/foo.py", "scripts/bar.py"],
            "doc_only": False,
            "findings": [
                {"file": "scripts/foo.py", "line_start": 42, "line_end": 170,
                 "metric": "python.function_lines", "value": 128, "threshold": 60,
                 "severity": "advisory", "message": "Function `process` is 128 lines."},
            ],
            "test_health": {"status": "pass", "suite": "unittest", "count": 42},
            "summary": {"advisory": 1, "blocking": 0},
        }
        md = self.m.render_markdown(report)
        self.assertIn("## Diffguard-Lite Report", md)
        self.assertIn("**Test-health:** pass (42 tests", md)
        self.assertIn("advisory=1", md)
        self.assertIn("`scripts/foo.py:42-170`", md)

    def test_render_markdown_truncates_to_first_ten_findings(self):
        findings = [
            {"file": f"scripts/f{i}.py", "line_start": 1, "line_end": 10,
             "metric": "python.file_lines", "value": 500, "threshold": 400,
             "severity": "advisory", "message": f"msg {i}"}
            for i in range(15)
        ]
        report = {
            "base": "origin/main", "head": "HEAD",
            "changed_files": [f["file"] for f in findings],
            "doc_only": False, "findings": findings,
            "test_health": {"status": "pass", "suite": "unittest", "count": 1},
            "summary": {"advisory": 15, "blocking": 0},
        }
        md = self.m.render_markdown(report)
        self.assertIn("showing first 10 of 15", md)
        self.assertIn("scripts/f0.py", md)
        self.assertIn("scripts/f9.py", md)
        self.assertNotIn("scripts/f10.py", md)

    def test_render_text_includes_key_fields(self):
        report = {
            "base": "origin/main",
            "head": "HEAD",
            "changed_files": ["scripts/foo.py"],
            "doc_only": False,
            "findings": [],
            "test_health": {"status": "pass", "suite": "unittest", "count": 42},
            "summary": {"advisory": 0, "blocking": 0},
        }
        text = self.m.render_text(report)
        self.assertIn("base: origin/main", text)
        self.assertIn("42 tests", text)
        self.assertIn("advisory=0", text)

    # --- run_diffguard (integration with mocks) ---

    def test_run_diffguard_skips_tests_when_doc_only(self):
        with mock.patch.object(self.m, "changed_files", return_value=["docs/foo.md"]):
            report, exit_code = self.m.run_diffguard(
                "origin/main", Path("/nonexistent/cfg.yaml"),
            )
        self.assertEqual(report["test_health"]["status"], "skipped")
        self.assertEqual(exit_code, 0)

    def test_run_diffguard_fails_on_test_health_fail(self):
        with mock.patch.object(self.m, "changed_files", return_value=["scripts/x.py"]), \
             mock.patch.object(self.m, "run_test_health",
                               return_value={"status": "fail", "suite": "unittest", "count": 5}), \
             mock.patch.object(Path, "exists", return_value=False):
            report, exit_code = self.m.run_diffguard(
                "origin/main", Path("/nonexistent/cfg.yaml"),
            )
        self.assertEqual(report["test_health"]["status"], "fail")
        self.assertEqual(exit_code, 1)

    def test_run_diffguard_clean_returns_zero(self):
        with mock.patch.object(self.m, "changed_files", return_value=["scripts/x.py"]), \
             mock.patch.object(self.m, "run_test_health",
                               return_value={"status": "pass", "suite": "unittest", "count": 42}), \
             mock.patch.object(Path, "exists", return_value=False):
            report, exit_code = self.m.run_diffguard(
                "origin/main", Path("/nonexistent/cfg.yaml"),
            )
        self.assertEqual(report["summary"]["blocking"], 0)
        self.assertEqual(exit_code, 0)

    def test_run_diffguard_output_is_valid_json(self):
        with mock.patch.object(self.m, "changed_files", return_value=["docs/foo.md"]):
            report, _ = self.m.run_diffguard(
                "origin/main", Path("/nonexistent/cfg.yaml"),
            )
        dumped = json.dumps(report)
        self.assertEqual(json.loads(dumped)["doc_only"], True)


if __name__ == "__main__":
    unittest.main()
