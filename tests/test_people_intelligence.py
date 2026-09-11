import re
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "people-intelligence"
EXAMPLE = PACKAGE / "examples" / "fictional-team-coordination"

OUTPUT_HEADINGS = [
    "## 1. Summary",
    "## 2. Current work and decisions",
    "## 3. Key professional relationships",
    "## 4. Observed collaboration preferences",
    "## 5. Capacity and escalation signals",
    "## 6. Practical working guidance",
    "## 7. From optional long-form notes",
    "## 8. Changes since the prior brief",
    "## 9. Relational framing",
    "## 10. Uncertainties and corrections",
]


def read(path):
    return path.read_text(encoding="utf-8")


class PeopleIntelligencePublicTest(unittest.TestCase):
    def test_package_is_complete_and_directly_installable(self):
        required = {
            "README.md",
            "SKILL.md",
            "agents/openai.yaml",
            "references/RUN-workflow.md",
            "references/REF-evidence-privacy.md",
            "assets/output-template.md",
            "assets/writing-prompt-template.md",
            "assets/evidence-corpus-template.md",
            "assets/source-map-template.yaml",
            "examples/EX-synthetic.md",
            "examples/fictional-team-coordination/README.md",
            "examples/fictional-team-coordination/evidence-corpus.md",
            "examples/fictional-team-coordination/source-map.yaml",
            "examples/fictional-team-coordination/prior-brief.md",
            "examples/fictional-team-coordination/reference-brief.md",
            "examples/fictional-team-coordination/stakeholder-brief.md",
        }
        missing = [relative for relative in sorted(required) if not (PACKAGE / relative).is_file()]
        self.assertEqual(missing, [])

        skill = read(PACKAGE / "SKILL.md")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertEqual(set(re.findall(r"^([a-z_]+):", frontmatter, re.MULTILINE)), {"name", "description"})
        self.assertNotIn("docs/", skill)
        for target in re.findall(r"`((?:references|assets|examples)/[^`]+)`", skill):
            self.assertTrue((PACKAGE / target).is_file(), target)

    def test_readme_links_resolve(self):
        path = PACKAGE / "README.md"
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
            self.assertFalse(target.startswith(("http://", "https://")))
            self.assertTrue((path.parent / target).resolve().is_file(), target)

    def test_workflow_preserves_bounded_collection_and_safe_branches(self):
        workflow = read(PACKAGE / "references" / "RUN-workflow.md")
        for required in (
            "14-day lookback",
            "subject-originated",
            "subject-directed",
            "up to 10 high-value observations",
            "up to five additional",
            "fewer than 10",
            "Optional long-form notes",
            "Delta mode",
            "Relational mode",
            "at least two independent observations",
            "Never publish, send, schedule, or otherwise mutate",
        ):
            self.assertIn(required, workflow)

    def test_templates_keep_the_full_public_contract(self):
        output = read(PACKAGE / "assets" / "output-template.md")
        self.assertEqual(
            [line for line in output.splitlines() if re.fullmatch(r"## (?:10|[1-9])\. .+", line)],
            OUTPUT_HEADINGS,
        )
        self.assertIn("Correction or deletion path", output)
        self.assertIn("[Missing]", output)

        prompt = read(PACKAGE / "assets" / "writing-prompt-template.md")
        for section in (
            "## Observed communication approach",
            "## Current professional priorities",
            "## Helpful framing",
            "## Friction to avoid",
            "## Format defaults",
            "## Relational framing",
        ):
            self.assertIn(section, prompt)

    def test_complete_fictional_scenario_exercises_every_branch(self):
        brief = read(EXAMPLE / "stakeholder-brief.md")
        self.assertEqual(
            [line for line in brief.splitlines() if re.fullmatch(r"## (?:10|[1-9])\. .+", line)],
            OUTPUT_HEADINGS,
        )
        for phrase in (
            "11 dated observations",
            "fictional notes source",
            "fictional prior brief",
            "fictional reference brief",
            "## 7. From optional long-form notes",
            "## 8. Changes since the prior brief",
            "## 9. Relational framing",
            "## Writing-preparation prompt",
        ):
            self.assertIn(phrase, brief)

        corpus = read(EXAMPLE / "evidence-corpus.md")
        for identifier in ("E-001", "E-002", "E-003", "E-004", "E-005", "E-006", "E-007", "E-008", "E-009", "E-010", "E-011"):
            self.assertIn(identifier, corpus)
        for path in EXAMPLE.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml"}:
                self.assertNotRegex(read(path), r"\[(?:Missing|TODO|TBD)\]|\b(?:TODO|TBD)\b")

    def test_fictional_urls_use_reserved_domains(self):
        urls = []
        for path in EXAMPLE.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml"}:
                urls.extend(re.findall(r"https?://[^\s>`]+", read(path)))
        self.assertGreater(len(urls), 0)
        for url in urls:
            host = urlparse(url).hostname or ""
            self.assertTrue(host.endswith(".invalid"), url)

    def test_public_package_has_no_obvious_private_or_external_action_material(self):
        blocked = re.compile(
            r"/" + r"Users/|channel[_ -]?id\s*[:=]|api[_ -]?key\s*[:=]|"
            r"secret\s*[:=]|\bsk-[A-Za-z0-9_-]{16,}\b",
            re.IGNORECASE,
        )
        findings = []
        for path in PACKAGE.rglob("*"):
            if path.is_file():
                match = blocked.search(read(path))
                if match:
                    findings.append(f"{path.relative_to(PACKAGE)}: {match.group(0)}")
        self.assertEqual(findings, [])

    def test_catalog_and_governed_documents_describe_the_same_public_surface(self):
        catalog_path = ROOT / "docs" / "SKILL-CATALOG.md"
        catalog = read(catalog_path)
        section = catalog.split("- `people-intelligence`", 1)[1].split("\n- `comp-intel`", 1)[0]
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", section):
            self.assertTrue((catalog_path.parent / target).resolve().is_file(), target)

        requirements = read(ROOT / "docs" / "DOC-people-intelligence-product-requirements-v1.0.md")
        inventory = read(ROOT / "docs" / "DOC-people-intelligence-source-inventory-v1.0.md")
        acceptance = read(ROOT / "docs" / "DOC-people-intelligence-public-acceptance-tests-v1.0.md")
        expected_requirements = {f"PI-REQ-{number:03d}" for number in range(1, 13)}
        self.assertTrue(expected_requirements.issubset(set(re.findall(r"\bPI-REQ-\d{3}\b", requirements))))
        self.assertTrue(set(re.findall(r"\bPI-REQ-\d{3}\b", inventory)).issubset(expected_requirements))
        self.assertTrue({f"PI-AT-{number:03d}" for number in range(1, 13)}.issubset(set(re.findall(r"\bPI-AT-\d{3}\b", acceptance))))


if __name__ == "__main__":
    unittest.main()
