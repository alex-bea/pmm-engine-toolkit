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
            "references/RUN-onboarding.md",
            "references/RUN-workflow.md",
            "references/REF-analyst-contract.md",
            "references/DOC-setup-and-mapping.md",
            "references/DOC-evidence-and-claims.md",
            "references/DOC-review-and-apply.md",
            "references/DOC-troubleshooting.md",
            "assets/source-map-template.md",
            "assets/onboarding-state-template.md",
            "assets/adopter-positioning-template.md",
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
            "onboarding-state.md",
            "source-map.md",
            "adopter-positioning.md",
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

    def test_onboarding_requires_verification_before_canonical_or_content_access(self):
        onboarding = (PACKAGE / "references/RUN-onboarding.md").read_text(encoding="utf-8")
        normalized = " ".join(onboarding.lower().split())
        self.assertIn(
            "only after the pmm verifies a candidate may it be written to `source-map.md`",
            normalized,
        )
        self.assertIn("do not read messages or document bodies yet", normalized)
        self.assertIn("ask the pmm which sources may be read", normalized)

        source_map = (
            PACKAGE / "examples/fictional-devtools/source-map.md"
        ).read_text(encoding="utf-8").lower()
        onboarding_state = (
            PACKAGE / "examples/fictional-devtools/onboarding-state.md"
        ).read_text(encoding="utf-8").lower()
        self.assertNotIn("| pending", source_map)
        self.assertIn("pending enrichment verification", onboarding_state)

    def test_fictional_example_is_a_scoped_first_baseline(self):
        market_pack = (
            PACKAGE / "examples/fictional-devtools/market-pack.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("market_id: fictional-devtools-us", market_pack)
        self.assertIn("scope_type: product-geography", market_pack)
        self.assertIn("product: LaunchPad Analytics", market_pack)
        self.assertIn("geography: United States", market_pack)
        self.assertEqual(market_pack.count("homepage: https://"), 4)

        positioning = (
            PACKAGE / "examples/fictional-devtools/adopter-positioning.md"
        ).read_text(encoding="utf-8")
        run_record = (
            PACKAGE / "examples/fictional-devtools/run-record.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Status: Approved", positioning)
        self.assertIn("| Mode | baseline |", run_record)
        self.assertIn("Approved adopter positioning", run_record)
        self.assertIn("| Coverage status | limited |", run_record)

    def test_limited_baseline_names_the_next_verification_step(self):
        briefing = (
            PACKAGE / "examples/fictional-devtools/draft-briefing.md"
        ).read_text(encoding="utf-8")
        self.assertIn("LIMITED COVERAGE", briefing)
        self.assertIn("Highest-value source to add next", briefing)
        self.assertIn("BluePeak customer-stories page", briefing)
        self.assertIn("only an approved link is copied into `source-map.md`", briefing)


if __name__ == "__main__":
    unittest.main()
