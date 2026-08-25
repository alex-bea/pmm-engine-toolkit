import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-skills/scripts/govern_skills.py"
)
TRACKER_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-work-tracker/scripts/govern_work_tracker.py"
)
DOCUMENT_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-documents/scripts/govern_documents.py"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_main(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        status = module.main(argv)
    return status, stdout.getvalue(), stderr.getvalue()


class GovernancePluginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_module("plugin_govern_skills", SKILL_SCRIPT)
        cls.tracker = load_module("plugin_govern_work_tracker", TRACKER_SCRIPT)
        cls.documents = load_module("plugin_govern_documents", DOCUMENT_SCRIPT)

    def test_document_audit_accepts_valid_opted_in_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            docs = repo / "docs"
            docs.mkdir()
            (docs / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            (docs / "decision.md").write_text(
                "---\n"
                "doc_type: DOC\n"
                "normative: false\n"
                "requires:\n"
                "  - requirements.md\n"
                "status: Draft\n"
                "version: \"0.1\"\n"
                "owner: documentation-owner\n"
                "consumers:\n"
                "  - reviewers\n"
                "change_control: Pull request review\n"
                "---\n\n"
                "# Decision\n\n"
                "Read the [requirements](requirements.md).\n",
                encoding="utf-8",
            )
            (repo / "README.md").write_text("[ignored](missing.md)\n", encoding="utf-8")

            status, output, _ = run_main(self.documents, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            self.assertIn("Audited 1 governed Markdown document(s).", output)
            self.assertIn("No findings.", output)

            status, output, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--format", "json"]
            )
            self.assertEqual(status, 0)
            result = json.loads(output)
            self.assertEqual(result, {"governed_documents": 1, "findings": []})

    def test_document_audit_reports_findings_without_modifying_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            document = repo / "governed.md"
            document.write_text(
                "---\n"
                "doc_type: UNKNOWN\n"
                "normative: uncertain\n"
                "requires:\n"
                "  - missing-requirement.md\n"
                "status: Ready\n"
                "version: \"0.1\"\n"
                "consumers:\n"
                "  - reviewers\n"
                "change_control: Pull request review\n"
                "---\n\n"
                "# Governed\n\n"
                "[broken](missing-link.md)\n",
                encoding="utf-8",
            )
            (repo / "notes.md").write_text("[ignored](also-missing.md)\n", encoding="utf-8")
            before = {
                path.relative_to(repo).as_posix(): path.read_bytes()
                for path in repo.rglob("*") if path.is_file()
            }

            status, output, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--format", "json"]
            )
            self.assertEqual(status, 0)
            result = json.loads(output)
            self.assertEqual(result["governed_documents"], 1)
            finding_ids = {finding["id"] for finding in result["findings"]}
            self.assertTrue({"DOC002", "DOC003", "DOC004", "DOC005", "DOC009", "DOC011"} <= finding_ids)
            self.assertEqual(
                {
                    path.relative_to(repo).as_posix(): path.read_bytes()
                    for path in repo.rglob("*") if path.is_file()
                },
                before,
            )

            status, _, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)
            self.assertEqual(
                {
                    path.relative_to(repo).as_posix(): path.read_bytes()
                    for path in repo.rglob("*") if path.is_file()
                },
                before,
            )

    def test_skill_audit_is_advisory_by_default_and_strict_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, output, _ = run_main(self.skills, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            self.assertIn("GOV001", output)
            status, _, _ = run_main(
                self.skills, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)

    def test_skill_initializer_is_dry_run_then_idempotent_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, output, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("create: .agents/governance/manifest.yaml", output)
            self.assertFalse((repo / ".agents").exists())

            status, _, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            self.assertTrue((repo / ".agents/governance/manifest.yaml").is_file())
            self.assertEqual(self.skills.audit(repo), [])

            status, output, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            self.assertNotIn("conflict:", output)

    def test_skill_initializer_never_overwrites_a_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.assertEqual(
                run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])[0],
                0,
            )
            target = repo / ".agents/governance/standards/STD-skill-structure-v1.0.md"
            target.write_text("local policy\n", encoding="utf-8")
            status, output, error = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 2)
            self.assertIn("conflict:", output)
            self.assertIn("not overwritten", error)
            self.assertEqual(target.read_text(encoding="utf-8"), "local policy\n")

    def test_initializers_refuse_paths_that_escape_through_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            (repo / ".agents").symlink_to(external, target_is_directory=True)
            skill_status, _, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            tracker_status, _, _ = run_main(
                self.tracker, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(skill_status, 2)
            self.assertEqual(tracker_status, 2)
            self.assertEqual(list(external.iterdir()), [])
            self.assertFalse((repo / "state").exists())

    def test_skill_fix_adds_only_missing_interface_and_draft_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])
            skill = repo / ".agents/skills/example-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Example governed skill.\n---\n\n"
                "# Example Skill\n",
                encoding="utf-8",
            )
            status, output, _ = run_main(
                self.skills, ["fix", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("agents/openai.yaml", output)
            self.assertFalse((skill / "agents/openai.yaml").exists())

            status, _, _ = run_main(
                self.skills, ["fix", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            registry = json.loads(
                (repo / ".agents/governance/skill-registry.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(registry["skills"][0]["status"], "draft")
            self.assertEqual(registry["skills"][0]["owner"], "unassigned")
            self.assertEqual(self.skills.audit(repo), [])

    def test_ci_is_installed_only_when_explicitly_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            first.mkdir()
            second.mkdir()
            run_main(self.skills, ["initialize", "--repo", str(first), "--apply"])
            run_main(
                self.skills,
                ["initialize", "--repo", str(second), "--with-ci", "--apply"],
            )
            self.assertFalse((first / ".github/workflows/skill-governance.yml").exists())
            workflow = second / ".github/workflows/skill-governance.yml"
            self.assertTrue(workflow.is_file())
            self.assertEqual(
                run_main(self.skills, ["initialize", "--repo", str(second), "--apply"])[0],
                0,
            )
            self.assertTrue(workflow.is_file())
            workflow.unlink()
            self.assertEqual(
                run_main(self.skills, ["fix", "--repo", str(second), "--apply"])[0],
                0,
            )
            self.assertTrue(workflow.is_file())

    def test_tracker_initializer_merges_manifest_and_validates_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])
            status, output, _ = run_main(
                self.tracker, ["initialize", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("state/work/roadmaps/.gitkeep", output)
            self.assertFalse((repo / "state/work").exists())

            self.assertEqual(
                run_main(self.tracker, ["initialize", "--repo", str(repo), "--apply"])[0],
                0,
            )
            manifest = json.loads(
                (repo / ".agents/governance/manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(set(manifest["components"]), {"skills", "work-tracker"})
            self.assertEqual(self.tracker.audit(repo), [])

            templates = (
                ROOT / "plugins/skill-governance/skills/govern-work-tracker/assets/templates"
            )
            for kind, name in (
                ("roadmaps", "roadmap"),
                ("epics", "epic"),
                ("tasks", "task"),
            ):
                record = json.loads((templates / f"{name}.yaml").read_text(encoding="utf-8"))
                (repo / "state/work" / kind / f"{record['id']}.yaml").write_text(
                    json.dumps(record, indent=2) + "\n", encoding="utf-8"
                )
            self.assertEqual(self.tracker.audit(repo), [])

            task_path = repo / "state/work/tasks/synthesize-onboarding-interviews.yaml"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task["status"] = "done"
            task_path.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")
            findings = self.tracker.audit(repo)
            self.assertTrue(any(item.id == "TRACKER017" for item in findings))

    def test_tracker_audit_is_advisory_and_fix_restores_missing_managed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, _, _ = run_main(self.tracker, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            status, _, _ = run_main(
                self.tracker, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)
            run_main(self.tracker, ["initialize", "--repo", str(repo), "--apply"])
            target = repo / ".agents/governance/schemas/task.schema.json"
            target.unlink()
            status, output, _ = run_main(
                self.tracker, ["fix", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("task.schema.json", output)
            self.assertFalse(target.exists())
            self.assertEqual(
                run_main(self.tracker, ["fix", "--repo", str(repo), "--apply"])[0],
                0,
            )
            self.assertTrue(target.is_file())
            self.assertEqual(self.tracker.audit(repo), [])


if __name__ == "__main__":
    unittest.main()
