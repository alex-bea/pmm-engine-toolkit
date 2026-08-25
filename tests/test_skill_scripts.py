import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SkillScriptTest(unittest.TestCase):
    def test_tracker_validation(self):
        module = load_module("tracker", "skills/pmm-em-tracker/scripts/tracker.py")
        good = {
            "roadmaps": [{"id": "r1", "title": "Roadmap"}],
            "epics": [{"id": "e1", "title": "Epic", "roadmap": "r1"}],
            "tasks": [{"id": "t1", "title": "Task", "epic": "e1", "status": "todo",
                       "acceptance_criteria": ["Verified"]}],
        }
        self.assertEqual(module.validate(good), [])
        good["tasks"][0]["status"] = "blocked"
        self.assertIn("t1: blocked task needs blocked_reason", module.validate(good))

    def test_plan_scaffold_and_audit(self):
        scaffold = load_module("scaffold", "skills/pmm-plan-scaffolder/scripts/scaffold_plan.py")
        audit = load_module("audit", "skills/pmm-plan-auditor/scripts/audit_plans.py")
        text = scaffold.render("Onboarding", "Improve setup clarity.", "epic")
        self.assertIn("tracker_id: \"[Missing]\"", text)
        with tempfile.TemporaryDirectory() as tmp:
            plans = Path(tmp)
            (plans / "PLAN-onboarding.md").write_text(text, encoding="utf-8")
            findings = audit.audit(plans, {"roadmaps": [], "epics": [], "tasks": []})
        self.assertEqual(findings[0]["finding"], "missing tracker_id")

    def test_weekly_notes_transform(self):
        module = load_module(
            "weekly", "skills/notes-weekly-team-comms/scripts/weekly_update_transform.py"
        )
        items = module.parse("# Shipped\n- Brief approved\n# Risks\n- Owner missing\n")
        output = module.render(items)
        self.assertIn("Brief approved", output)
        self.assertIn("Owner missing", output)

    def test_accepted_plan_proposal_is_content_addressed(self):
        module = load_module(
            "import_plan", "skills/pmm-accepted-plan-importer/scripts/import_plan.py"
        )
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "PLAN-demo.md"
            plan.write_text("# Plan\n", encoding="utf-8")
            first = module.proposal(plan, "Approver", "2026-08-18", "epic")
            second = module.proposal(plan, "Approver", "2026-08-18", "epic")
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertFalse(first["tracker_write_approved"])

    def test_git_sweep_protects_current_worktree(self):
        script = ROOT / "skills/git-sweep/scripts/worktree_hygiene.py"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            result = subprocess.run(
                [sys.executable, str(script), "--repo", str(repo)],
                text=True, capture_output=True, check=True,
            )
        rows = json.loads(result.stdout)
        self.assertEqual(rows[0]["classification"], "protected-current")


if __name__ == "__main__":
    unittest.main()
