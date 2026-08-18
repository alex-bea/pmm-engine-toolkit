import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "validate_github_actions.py"


class GitHubActionsTest(unittest.TestCase):
    def test_workflows_follow_public_security_policy(self):
        spec = importlib.util.spec_from_file_location("validate_github_actions", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()

