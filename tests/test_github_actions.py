import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "validate_github_actions.py"


class GitHubActionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("validate_github_actions", SCRIPT)
        cls.module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.module)

    def test_workflows_follow_public_security_policy(self):
        self.assertEqual(self.module.main(), 0)

    def test_unreviewed_action_and_write_permission_are_rejected(self):
        workflow = """name: Unsafe
on: [pull_request]
permissions:
  contents: write
concurrency:
  group: unsafe
  cancel-in-progress: true
jobs:
  unsafe:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    steps:
      - uses: example/unsafe-action@v1
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "unsafe.yml"
            path.write_text(workflow, encoding="utf-8")
            errors = self.module.validate_workflow(path)
        self.assertTrue(any("top-level permissions" in error for error in errors))
        self.assertTrue(any("full commit SHA" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
