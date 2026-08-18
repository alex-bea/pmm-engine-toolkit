import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "governance" / "configure_github_security.py"
POLICY = ROOT / "config" / "github-security-controls.json"


def load_module():
    spec = importlib.util.spec_from_file_location("configure_github_security", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class GitHubSecurityTest(unittest.TestCase):
    def test_policy_matches_required_public_baseline(self):
        module = load_module()
        policy = module.load_policy(POLICY)
        self.assertEqual(policy["repository"]["required_visibility"], "public")
        self.assertEqual(policy["ruleset"]["bypass_actors"], [])
        self.assertTrue(policy["actions"]["permissions"]["sha_pinning_required"])

    def test_plan_covers_all_remote_control_families(self):
        module = load_module()
        policy = module.load_policy(POLICY)
        plan = module.build_plan(policy, "example/pmm-engine-toolkit")
        endpoints = {operation["endpoint"] for operation in plan}
        self.assertEqual(
            endpoints,
            {
                "repos/example/pmm-engine-toolkit",
                "repos/example/pmm-engine-toolkit/actions/permissions",
                "repos/example/pmm-engine-toolkit/actions/permissions/selected-actions",
                "repos/example/pmm-engine-toolkit/actions/permissions/workflow",
                "repos/example/pmm-engine-toolkit/vulnerability-alerts",
                "repos/example/pmm-engine-toolkit/automated-security-fixes",
                "repos/example/pmm-engine-toolkit/private-vulnerability-reporting",
                "repos/example/pmm-engine-toolkit/rulesets",
            },
        )

    def test_default_mode_is_offline_plan(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", "example/pmm-engine-toolkit"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["repository"], "example/pmm-engine-toolkit")
        self.assertEqual(output["operations"][-1]["method"], "UPSERT")

    def test_public_main_guard_refuses_wrong_target(self):
        module = load_module()
        policy = module.load_policy(POLICY)
        with self.assertRaises(module.SecurityControlsError):
            module.require_public_main(
                {"visibility": "private", "default_branch": "main"}, policy
            )
        with self.assertRaises(module.SecurityControlsError):
            module.require_public_main(
                {"visibility": "public", "default_branch": "master"}, policy
            )


if __name__ == "__main__":
    unittest.main()
