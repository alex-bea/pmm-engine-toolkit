import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/govern-skills"
RUN = PACKAGE / "references/RUN-govern-skills-setup-workflow-v1.0.md"
STANDARDS = (
    "STD-ai-skill-governance-prd-v1.0.md",
    "STD-approval-gates-v1.0.md",
    "STD-evidence-privacy-v1.0.md",
    "STD-governance-document-metadata-v1.0.md",
    "STD-runtime-enforcement-v1.0.md",
    "STD-skill-dependencies-v1.0.md",
    "STD-skill-primitives-v1.0.md",
    "STD-skill-structure-v1.0.md",
)


def file_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


class GovernSkillsStandaloneTest(unittest.TestCase):
    def test_package_is_direct_copy_ready(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        agent = (PACKAGE / "agents/openai.yaml").read_text(encoding="utf-8")

        self.assertEqual(
            [path.name for path in (PACKAGE / "references").glob("RUN-*.md")],
            ["RUN-govern-skills-setup-workflow-v1.0.md"],
        )
        self.assertIn("references/RUN-govern-skills-setup-workflow-v1.0.md", skill)
        self.assertIn("No plugin", readme)
        self.assertIn("read-only inventory", readme)
        self.assertIn("exact proposed file plan", " ".join(readme.split()))
        self.assertIn("$govern-skills", agent)
        for primitive in (
            "`SKILL.md`", "`RUN-*.md`", "`STD-*.md`", "`REF-*.md`",
            "Templates", "Examples", "Scripts", "Policy decision",
            "Harness adapter", "Capability boundary",
        ):
            self.assertIn(primitive, readme)

    def test_setup_contract_and_stale_receipt_are_explicit(self):
        run = RUN.read_text(encoding="utf-8")
        headings = [
            "## 1. Setup outcome",
            "## 2. Installation checks",
            "## 3. Source mapping",
            "## 4. Output destinations",
            "## 5. Configuration and state",
            "## 6. Permissions and secrets",
            "## 7. Test run",
            "## 8. Setup receipt",
            "## 9. Repair, rerun, and reconfiguration",
            "## 10. Normal execution",
        ]
        positions = [run.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn(
            "| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |",
            run,
        )
        self.assertIn(
            "| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |",
            run,
        )
        for phrase in (
            "ready-with-optional-limitations", "blocked", "publishing",
            "notifications", "scheduling", "production", "receipt is stale",
            "examples/fixtures/fictional-repository-map.yaml",
        ):
            self.assertIn(phrase, run)

    def test_package_links_and_standard_mirrors_close_locally(self):
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in PACKAGE.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("/" + "Users/", text)
            for target in link_re.findall(text):
                clean = target.split("#", 1)[0]
                if not clean or clean.startswith(("http://", "https://", "mailto:")):
                    continue
                self.assertTrue(
                    (path.parent / clean).resolve().is_file(),
                    f"broken package link {target!r} in {path.relative_to(PACKAGE)}",
                )
        for name in STANDARDS:
            self.assertEqual(
                (PACKAGE / "references" / name).read_bytes(),
                (ROOT / "docs" / name).read_bytes(),
                name,
            )

    def test_fictional_documents_only_setup_is_isolated(self):
        fixture_path = PACKAGE / "examples/fixtures/fictional-repository-map.yaml"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertTrue(fixture["fictional"])
        self.assertTrue(fixture["selected_layers"]["instruction_only"])
        self.assertFalse(any(
            enabled for layer, enabled in fixture["selected_layers"].items()
            if layer != "instruction_only"
        ))
        self.assertIn("publishing", fixture["disabled_actions"])

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            installed = workspace / "packages/govern-skills"
            shutil.copytree(PACKAGE, installed)
            before = file_digest(installed)
            output = workspace / "temporary/acorn-governance-test"
            agents_target = output / "docs/governance/AGENTS.md"
            skill_target = output / "agent-skills/sample-skill/SKILL.md"
            receipt_target = output / ".agents/governance/setup-receipt.md"
            agents_target.parent.mkdir(parents=True)
            skill_target.parent.mkdir(parents=True)
            receipt_target.parent.mkdir(parents=True)
            shutil.copyfile(installed / "assets/templates/AGENTS.md", agents_target)
            shutil.copyfile(installed / "assets/templates/SKILL.md", skill_target)
            shutil.copyfile(
                installed / "examples/fixtures/fictional-setup-receipt.md",
                receipt_target,
            )

            actual = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*") if path.is_file()
            }
            self.assertEqual(actual, set(fixture["expected_test_files"]))
            self.assertEqual(file_digest(installed), before)
            receipt = receipt_target.read_text(encoding="utf-8")
            self.assertIn("ready-with-optional-limitations", receipt)
            self.assertIn("not applicable", receipt)
            self.assertIn("becomes stale", receipt)


if __name__ == "__main__":
    unittest.main()
