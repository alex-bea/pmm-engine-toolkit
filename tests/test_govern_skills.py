import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/govern-skills"
RUN = PACKAGE / "references/RUN-govern-skills-workflow-v1.1.md"
SETUP = PACKAGE / "references/REF-govern-skills-setup-contract.md"
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


def top_level_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", text)
    return match.group(1).strip().strip('"\'') if match else None


class GovernSkillsStandaloneTest(unittest.TestCase):
    def test_package_is_direct_copy_ready(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        agent = (PACKAGE / "agents/openai.yaml").read_text(encoding="utf-8")

        self.assertEqual(
            [path.name for path in (PACKAGE / "references").glob("RUN-*.md")],
            ["RUN-govern-skills-workflow-v1.1.md"],
        )
        self.assertIn("references/RUN-govern-skills-workflow-v1.1.md", skill)
        self.assertIn("references/REF-govern-skills-setup-contract.md", skill)
        self.assertIn("Do not load the setup contract", skill)
        self.assertIn("explicit setup", skill)
        self.assertIn("## Setup", readme)
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
        setup = SETUP.read_text(encoding="utf-8")
        headings = [
            "## 1. Setup profile",
            "## 2. Readiness and routing",
            "## 3. Installation checks",
            "## 4. Source mapping",
            "## 5. Output destinations",
            "## 6. Configuration and state",
            "## 7. Permissions and secrets",
            "## 8. Safe test run",
            "## 9. Setup receipt",
            "## 10. Repair and reconfiguration",
        ]
        positions = [setup.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("**Setup profile:** `local-persistence`", setup)
        self.assertIn(
            "| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |",
            setup,
        )
        self.assertIn(
            "| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |",
            setup,
        )
        for phrase in (
            "ready", "missing", "stale", "blocked", "Publishing",
            "notifications", "scheduling", "production", "There is no TTL",
            "examples/fixtures/setup-smoke-test.md",
        ):
            self.assertIn(phrase, setup)

        config = (PACKAGE / "assets/setup-config.yaml").read_text()
        receipt = (PACKAGE / "assets/setup-receipt.yaml").read_text()
        for key in (
            "schema_version", "skill_slug", "setup_profile", "package", "sources",
            "destinations", "receipt_path",
        ):
            self.assertRegex(config, rf"(?m)^{re.escape(key)}:")
        for key in (
            "schema_version", "skill_slug", "status", "installed_at", "verified_at",
            "package_revision", "package_digest", "setup_contract_version",
            "configuration_path", "configuration_digest", "checks", "limitations",
            "normal_entrypoint",
        ):
            self.assertRegex(receipt, rf"(?m)^{re.escape(key)}:")

    def test_ready_and_setup_routes_are_separate(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        run = RUN.read_text(encoding="utf-8")
        adoption = (
            PACKAGE / "references/REF-governance-adoption-guide-v1.0.md"
        ).read_text(encoding="utf-8")
        setup_relative = "references/REF-govern-skills-setup-contract.md"
        normal_relative = "references/RUN-govern-skills-workflow-v1.1.md"

        ready_route = re.search(
            rf"For an audit.*?{re.escape(normal_relative)}.*?Do not load the setup contract",
            skill,
            re.DOTALL,
        )
        self.assertIsNotNone(ready_route)
        setup_route = re.search(
            rf"For explicit setup.*?missing, stale, or blocked.*?{re.escape(setup_relative)}",
            skill,
            re.DOTALL,
        )
        self.assertIsNotNone(setup_route)
        self.assertNotIn("REF-govern-skills-setup-contract.md", run.split("---", 2)[1])
        self.assertNotIn("REF-governance-adoption-guide-v1.0.md", run.split("---", 2)[1])
        self.assertNotIn("REF-govern-skills-setup-contract.md", adoption.split("---", 2)[1])

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
            state_root = output / ".agents/govern-skills"
            config_target = state_root / "setup-config.yaml"
            yaml_receipt_target = state_root / "setup-receipt.yaml"
            agents_target.parent.mkdir(parents=True)
            skill_target.parent.mkdir(parents=True)
            receipt_target.parent.mkdir(parents=True)
            state_root.mkdir(parents=True)
            shutil.copyfile(installed / "assets/templates/AGENTS.md", agents_target)
            shutil.copyfile(installed / "assets/templates/SKILL.md", skill_target)
            shutil.copyfile(
                installed / "examples/fixtures/fictional-setup-receipt.md",
                receipt_target,
            )
            shutil.copyfile(installed / "examples/fixtures/setup-config.yaml", config_target)
            shutil.copyfile(
                installed / "examples/fixtures/setup-receipt.yaml", yaml_receipt_target,
            )

            actual = {
                path.relative_to(output).as_posix()
                for path in output.rglob("*") if path.is_file()
            }
            self.assertEqual(
                actual,
                set(fixture["expected_test_files"]) | {
                    ".agents/govern-skills/setup-config.yaml",
                    ".agents/govern-skills/setup-receipt.yaml",
                },
            )
            self.assertEqual(file_digest(installed), before)
            receipt = receipt_target.read_text(encoding="utf-8")
            self.assertIn("ready-with-optional-limitations", receipt)
            self.assertIn("not applicable", receipt)
            self.assertIn("becomes stale", receipt)
            yaml_receipt = yaml_receipt_target.read_text()
            self.assertEqual(top_level_yaml_value(yaml_receipt, "status"), "ready")
            self.assertEqual(
                top_level_yaml_value(yaml_receipt, "normal_entrypoint"),
                "references/RUN-govern-skills-workflow-v1.1.md",
            )
            self.assertIn("  optional_layers: not-applicable", yaml_receipt)


if __name__ == "__main__":
    unittest.main()
