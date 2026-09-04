import re
import unittest
from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "marketing-brief"
EXAMPLE = PACKAGE / "examples" / "fictional-report-filters"

SECTION_HEADINGS = [
    "## 1. Brief Info",
    "## 2. Launch Summary",
    "## 3. Audience and Problem",
    "## 4. Launch Scope and Value",
    "## 5. Messaging",
    "## 6. Distribution",
    "## 7. Success",
]


def read(path):
    return path.read_text(encoding="utf-8")


def output_headings(text):
    return [line for line in text.splitlines() if re.fullmatch(r"## [1-7]\. .+", line)]


def words(value):
    return re.findall(r"\b[\w'-]+\b", value)


class MarketingBriefPublicTest(unittest.TestCase):
    def test_package_is_complete_and_directly_installable(self):
        required = {
            "README.md",
            "SKILL.md",
            "agents/openai.yaml",
            "references/RUN-marketing-brief-workflow.md",
            "references/REF-source-priority.md",
            "references/REF-launch-tiers.md",
            "references/REF-evidence-and-privacy.md",
            "assets/output-template.md",
            "examples/EX-synthetic.md",
            "examples/fictional-report-filters/source-packet.md",
            "examples/fictional-report-filters/marketing-brief.md",
        }
        missing = [relative for relative in sorted(required) if not (PACKAGE / relative).is_file()]
        self.assertEqual(missing, [])

        skill = read(PACKAGE / "SKILL.md")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertEqual(set(yaml.safe_load(frontmatter)), {"name", "description"})
        for target in re.findall(r"`((?:references|assets|examples)/[^`]+)`", skill):
            self.assertTrue((PACKAGE / target).is_file(), target)
        self.assertNotIn("docs/", skill)

    def test_readme_links_resolve(self):
        path = PACKAGE / "README.md"
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
            self.assertFalse(target.startswith(("http://", "https://")))
            self.assertTrue((path.parent / target).resolve().is_file(), target)

    def test_template_has_exact_golden_sections_fields_and_limits(self):
        template = read(PACKAGE / "assets" / "output-template.md")
        self.assertEqual(output_headings(template), SECTION_HEADINGS)
        fields = {
            "Owner",
            "Launch Name",
            "Product / Campaign",
            "Business Unit",
            "Tier / Priority",
            "Launch Date",
            "Primary Audience",
            "Secondary Audience",
            "Core Problem",
            "Why Now",
            "Scope",
            "Customer Value",
            "Proof Point 1",
            "Proof Point 2",
            "Proof Point 3",
            "Topline Message",
            "Support Point 1",
            "Support Point 2",
            "Support Point 3",
            "CTA",
            "Goal 1",
            "Goal 2",
            "Goal 3",
        }
        self.assertEqual(set(re.findall(r"^- \*\*([^*]+):\*\*", template, re.MULTILINE)), fields)
        for required in (
            "Launch Name is six words maximum",
            "Maximum 50 words",
            "18 words maximum",
            "20 words maximum",
            "15 words maximum",
            "10 words maximum",
            "Eight words maximum",
        ):
            self.assertIn(required, template)

    def test_completed_example_is_complete_and_within_limits(self):
        example = read(EXAMPLE / "marketing-brief.md")
        self.assertEqual(output_headings(example), SECTION_HEADINGS)
        self.assertNotRegex(example, r"\[(?:Missing|TODO|TBD)\]|\b(?:TODO|TBD)\b")

        values = dict(re.findall(r"^- \*\*([^*]+):\*\*\s*(.+)$", example, re.MULTILINE))
        limits = {
            "Owner": 8,
            "Launch Name": 6,
            "Product / Campaign": 8,
            "Business Unit": 8,
            "Tier / Priority": 8,
            "Launch Date": 8,
            "Primary Audience": 5,
            "Secondary Audience": 5,
            "Core Problem": 18,
            "Why Now": 18,
            "Scope": 20,
            "Customer Value": 18,
            "Proof Point 1": 10,
            "Proof Point 2": 10,
            "Proof Point 3": 10,
            "Topline Message": 15,
            "Support Point 1": 10,
            "Support Point 2": 10,
            "Support Point 3": 10,
            "CTA": 8,
            "Goal 1": 10,
            "Goal 2": 10,
            "Goal 3": 10,
        }
        self.assertEqual(set(values), set(limits))
        for field, limit in limits.items():
            self.assertLessEqual(len(words(values[field])), limit, f"{field}: {values[field]}")

        summary = example.split("## 2. Launch Summary\n", 1)[1].split("\n## 3.", 1)[0]
        self.assertLessEqual(len(words(summary)), 50)

    def test_fictional_sources_support_the_completed_brief(self):
        source = read(EXAMPLE / "source-packet.md")
        brief = read(EXAMPLE / "marketing-brief.md")
        for phrase in (
            "Maya Chen",
            "October 15, 2026",
            "Tier 2",
            "operations team leads",
            "analytics administrators",
            "Save recurring report views once, then reuse them every week.",
            "Create your first Saved View.",
            "Product blog",
            "Lifecycle email",
            "LinkedIn",
        ):
            self.assertIn(phrase.casefold(), source.casefold(), phrase)
            self.assertIn(phrase.casefold(), brief.casefold(), phrase)
        self.assertIn("14 minutes to 6 minutes", source)
        self.assertIn("fourteen minutes to six", brief)
        self.assertIn("120 Saved Views", source)
        self.assertIn("120 Saved Views", brief)

    def test_all_example_urls_use_reserved_domains(self):
        urls = []
        for path in EXAMPLE.glob("*.md"):
            urls.extend(re.findall(r"https?://[^\s>`]+", read(path)))
        self.assertGreater(len(urls), 0)
        for url in urls:
            host = urlparse(url).hostname or ""
            self.assertTrue(host.endswith(".invalid"), url)

    def test_source_priority_and_tier_rules_are_faithful(self):
        priority = read(PACKAGE / "references" / "REF-source-priority.md")
        order = re.findall(r"^\d\. (.+)$", priority.split("## Default source order", 1)[1].split("##", 1)[0], re.MULTILINE)
        self.assertEqual(len(order), 7)
        self.assertTrue(order[0].startswith("Final PRD"))
        self.assertTrue(order[-1].startswith("Meeting notes"))
        self.assertIn("Do not merge conflicting", priority)
        self.assertIn("equal-authority sources conflict", priority)

        tiers = read(PACKAGE / "references" / "REF-launch-tiers.md")
        for heading in (
            "## Tier 1 — Market-expanding or business-critical launch",
            "## Tier 2 — Meaningful feature, segment, or awareness launch",
            "## Tier 3 — Small update or visibility moment",
        ):
            self.assertIn(heading, tiers)
        self.assertIn("result remains ambiguous, use Tier 2", tiers)
        self.assertIn("explicitly approved tier", tiers)

    def test_workflow_covers_multi_launch_missing_data_edits_and_errors(self):
        workflow = read(PACKAGE / "references" / "RUN-marketing-brief-workflow.md")
        for required in (
            "If more than one is present",
            "Do not search for it",
            "default to Tier 2",
            "Do not merge conflicting claims",
            "return the full updated brief",
            "## Error handling",
            "publish, message, schedule, or mutate an external system",
        ):
            self.assertIn(required, workflow)

    def test_public_slice_has_no_obvious_private_or_credential_material(self):
        blocked_pattern = (
            r"/" + r"Users/|@" + "poly" + "gon"
            + r"|channel[_ -]?id\s*[:=]|api[_ -]?key\s*[:=]|"
            + r"secret\s*[:=]|\bsk-[A-Za-z0-9_-]{16,}\b"
        )
        blocked = re.compile(blocked_pattern, re.IGNORECASE)
        findings = []
        for path in PACKAGE.rglob("*"):
            if path.is_file():
                match = blocked.search(read(path))
                if match:
                    findings.append(f"{path.relative_to(PACKAGE)}: {match.group(0)}")
        self.assertEqual(findings, [])

    def test_governed_requirements_and_inventory_are_traceable(self):
        prd = read(ROOT / "docs" / "DOC-marketing-brief-product-requirements-v1.0.md")
        inventory = read(ROOT / "docs" / "DOC-marketing-brief-source-inventory-v1.0.md")
        requirements = set(re.findall(r"\bMB-REQ-\d{3}\b", prd))
        acceptance = set(re.findall(r"\bMB-AT-\d{3}\b", prd))
        self.assertEqual(requirements, {f"MB-REQ-{number:03d}" for number in range(1, 19)})
        self.assertEqual(acceptance, {f"MB-AT-{number:03d}" for number in range(1, 13)})
        inventory_requirements = set(re.findall(r"\bMB-REQ-\d{3}\b", inventory))
        self.assertTrue(inventory_requirements.issubset(requirements))
        for requirement in requirements:
            self.assertGreaterEqual(prd.count(requirement), 2, requirement)
        self.assertIn("status: Active", prd)
        self.assertIn("normative: true", prd)

    def test_catalog_links_to_package_and_governed_documents(self):
        catalog_path = ROOT / "docs" / "SKILL-CATALOG.md"
        catalog = read(catalog_path)
        section = catalog.split("- `marketing-brief`", 1)[1].split("\n- `pre-read-sharpener`", 1)[0]
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", section):
            self.assertTrue((catalog_path.parent / target).resolve().is_file(), target)


if __name__ == "__main__":
    unittest.main()
