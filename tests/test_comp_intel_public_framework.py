import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/comp-intel"


class CompIntelPublicFrameworkTest(unittest.TestCase):
    def test_practical_framework_documents_are_packaged(self):
        required = [
            "README.md",
            "SKILL.md",
            "references/RUN-workflow.md",
            "references/REF-analyst-contract.md",
            "references/DOC-setup-and-mapping.md",
            "references/DOC-evidence-and-claims.md",
            "references/DOC-review-and-apply.md",
            "references/DOC-troubleshooting.md",
            "assets/source-map-template.md",
            "assets/competitor-registry-template.md",
            "assets/positioning-context-template.md",
            "assets/stakeholder-lens-template.yaml",
            "assets/tracker-templates.md",
            "assets/run-record-template.md",
            "assets/evidence-log-template.md",
            "assets/output-template.md",
        ]
        missing = [path for path in required if not (PACKAGE / path).is_file()]
        self.assertEqual(missing, [])

    def test_fictional_example_covers_inputs_evidence_output_and_updates(self):
        example_root = PACKAGE / "examples/fictional-devtools"
        required = {
            "market-pack.yaml",
            "source-map.md",
            "competitor-registry.md",
            "positioning-context.md",
            "stakeholder-lens.yaml",
            "run-record.md",
            "evidence-log.md",
            "draft-briefing.md",
            "trackers.md",
        }
        self.assertEqual({path.name for path in example_root.iterdir()}, required)
        for path in example_root.iterdir():
            text = path.read_text(encoding="utf-8").lower()
            self.assertTrue("fictional" in text or "example" in text, path.name)

    def test_skill_is_agent_neutral_and_method_first(self):
        skill = (PACKAGE / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        self.assertIn("Claude Code, Codex", skill)
        self.assertIn("The method is the product", skill)
        self.assertIn("optional advanced mode", normalized)
        self.assertNotIn("Codex Desktop is the supported", skill)

    def test_skill_package_does_not_contain_private_golden_example_terms(self):
        forbidden = [
            r"#wg-",
            r"\bPolygon\b",
            r"\bSequence\b",
            r"\bAggLayer\b",
            r"\bPrivy\b",
            r"\bCrossmint\b",
            r"\bZeroDev\b",
        ]
        findings = []
        for path in PACKAGE.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in forbidden:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    findings.append(f"{path.relative_to(PACKAGE)}: {pattern}")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
