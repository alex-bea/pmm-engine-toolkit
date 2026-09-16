import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "pre-read-sharpener"
EXAMPLE = PACKAGE / "examples" / "fictional-rollout-decision"


def read(path):
    return path.read_text(encoding="utf-8")


def words(value):
    return re.findall(r"\b[\w'-]+\b", value)


class PreReadSharpenerPublicTest(unittest.TestCase):
    def test_package_is_complete_and_directly_installable(self):
        required = {
            "README.md",
            "SKILL.md",
            "agents/openai.yaml",
            "assets/output-template.md",
            "examples/EX-synthetic.md",
            "examples/fictional-rollout-decision/source-draft.md",
            "examples/fictional-rollout-decision/review-and-rewrite.md",
            "examples/fixtures/behavior-cases.md",
            "references/RUN-pre-read-sharpener-workflow.md",
            "references/REF-decision-ready-criteria.md",
            "references/REF-evidence-and-privacy.md",
        }
        missing = [relative for relative in sorted(required) if not (PACKAGE / relative).is_file()]
        self.assertEqual(missing, [])

        skill = read(PACKAGE / "SKILL.md")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertEqual(set(yaml.safe_load(frontmatter)), {"name", "description"})
        for target in re.findall(r"`((?:references|assets|examples)/[^`]+)`", skill):
            self.assertTrue((PACKAGE / target).is_file(), target)
        self.assertNotIn("docs/", skill)

    def test_discovery_metadata_remains_valid(self):
        metadata = read(PACKAGE / "agents" / "openai.yaml")
        for field in ("display_name", "short_description", "default_prompt"):
            self.assertRegex(metadata, rf'(?m)^\s*{field}:\s*"[^"]+"\s*$', field)
        self.assertIn("$pre-read-sharpener", metadata)

    def test_readme_and_example_links_resolve(self):
        for relative in ("README.md", "examples/EX-synthetic.md"):
            path = PACKAGE / relative
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
                self.assertFalse(target.startswith(("http://", "https://")))
                self.assertTrue((path.parent / target).resolve().is_file(), target)

    def test_template_preserves_sections_fields_and_limits(self):
        template = read(PACKAGE / "assets" / "output-template.md")
        headings = re.findall(
            r"^## (TL;DR|The decision|Tradeoffs|What changes if we say yes|Open questions \(if any\))$",
            template,
            re.MULTILINE,
        )
        self.assertEqual(
            headings,
            ["TL;DR", "The decision", "Tradeoffs", "What changes if we say yes", "Open questions (if any)"],
        )
        fields = set(re.findall(r"^\*\*([^*]+):\*\*", template, re.MULTILINE))
        self.assertEqual(fields, {"Audience", "Decision needed", "Recommended"})
        for required in (
            "at most 600 words",
            "10 words maximum",
            "25 words maximum",
            "100 words maximum",
            "20 words maximum",
            "80 words maximum",
            "| Option | Pros | Cons | Cost to reverse |",
            "Use exactly three TL;DR bullets",
            "Use two or three option rows total",
            "Do not use em dashes in the final rewrite",
        ):
            self.assertIn(required, template)

    def test_criteria_preserve_four_anchors_and_ten_binary_rows(self):
        criteria = read(PACKAGE / "references" / "REF-decision-ready-criteria.md")
        for anchor in ("Clear audience", "Clear decision", "Clear tradeoff", "Clear outcome"):
            self.assertIn(anchor, criteria)
        rows = re.findall(r"^\| (\d+) \| ([^|]+) \|", criteria, re.MULTILINE)
        self.assertEqual([int(number) for number, _ in rows], list(range(1, 11)))
        for name in (
            "Single thesis upfront",
            "Specific over abstract",
            "Scannable in two minutes",
            "Strong opinion",
            "Plain English and active voice",
            "No consultant language",
            "Decision and tradeoffs visible",
            "No throat-clearing",
            "Cost to reverse stated",
            "One deciding question",
        ):
            self.assertIn(name, criteria)
        self.assertIn("Partial credit does not exist", criteria)
        self.assertIn("after three revision rounds", criteria)

    def test_workflow_covers_complete_review_repair_persistence_and_edits(self):
        workflow = read(PACKAGE / "references" / "RUN-pre-read-sharpener-workflow.md")
        for required in (
            "## Step 0 — Accept input",
            "### 3.1 Blunt PM review",
            "### 3.2 Biggest issues",
            "### 3.3 Specific cuts",
            "### 3.4 Tightened rewrite",
            "### 3.5 Suggested agenda",
            "no more than three revision rounds",
            "outputs/pre-reads/YYYY-MM-DD-<slug>-pre-read.md",
            "append `-2`, `-3`",
            "## Edit handling",
            "## Error handling",
            "Do not silently choose another destination",
        ):
            self.assertIn(required, workflow)

    def test_completed_example_has_full_ordered_delivery(self):
        example = read(EXAMPLE / "review-and-rewrite.md")
        order = [
            "## Blunt PM review",
            "## Biggest issues",
            "## Specific cuts",
            "## Tightened rewrite",
            "## Suggested agenda",
            "## Decision-ready criteria self-check",
        ]
        positions = [example.index(heading) for heading in order]
        self.assertEqual(positions, sorted(positions))
        self.assertNotRegex(example, r"\[(?:Missing|TODO|TBD)\]|\b(?:TODO|TBD)\b")

        rewrite = example.split("## Tightened rewrite\n", 1)[1].split("\n## Suggested agenda", 1)[0]
        self.assertLessEqual(len(words(rewrite)), 600)
        self.assertNotIn("—", rewrite)
        fields = dict(re.findall(r"^\*\*([^*]+):\*\*[ \t]*([^\n]+)", rewrite, re.MULTILINE))
        self.assertEqual(set(fields), {"Audience", "Decision needed", "Recommended"})
        self.assertLessEqual(len(words(fields["Decision needed"])), 25)
        self.assertLessEqual(len(words(fields["Recommended"])), 15)

        tldr = rewrite.split("## TL;DR\n", 1)[1].split("\n## The decision", 1)[0]
        bullets = re.findall(r"^- (.+)$", tldr, re.MULTILINE)
        self.assertEqual(len(bullets), 3)
        for bullet in bullets:
            self.assertLessEqual(len(words(bullet)), 25)

        decision = rewrite.split("## The decision\n", 1)[1].split("\n## Tradeoffs", 1)[0]
        outcome = rewrite.split("## What changes if we say yes\n", 1)[1].split("\n## Open questions", 1)[0]
        self.assertLessEqual(len(words(decision)), 100)
        self.assertLessEqual(len(words(outcome)), 80)
        self.assertIn("| Option | Pros | Cons | Cost to reverse |", rewrite)
        self.assertEqual(len(re.findall(r"^\| (?:✓|Keep)", rewrite, re.MULTILINE)), 2)

    def test_completed_example_agenda_and_self_check_are_complete(self):
        example = read(EXAMPLE / "review-and-rewrite.md")
        agenda = example.split("## Suggested agenda\n", 1)[1].split("\n**Deciding question", 1)[0]
        agenda_items = re.findall(r"^- (.+)$", agenda, re.MULTILINE)
        self.assertEqual(len(agenda_items), 4)
        for item in agenda_items:
            self.assertLessEqual(len(words(item)), 10)

        self_check = example.split("## Decision-ready criteria self-check\n", 1)[1]
        rows = re.findall(r"^\| ([^|]+) \| Pass \|", self_check, re.MULTILINE)
        self.assertEqual(len(rows), 10)
        self.assertEqual(len(set(rows)), 10)

    def test_fictional_source_supports_completed_rewrite(self):
        source = read(EXAMPLE / "source-draft.md").casefold()
        output = read(EXAMPLE / "review-and-rewrite.md").casefold()
        for phrase in (
            "guided import",
            "vp product",
            "vp customer success",
            "head of engineering",
            "october 5",
            "october 30",
            "24 beta workspaces",
            "16 invitations",
            "four hours",
            "one business day",
            "no more than six mapping-related tickets",
        ):
            self.assertIn(phrase, source, phrase)
            self.assertIn(phrase, output, phrase)
        self.assertIn("harborline software", source)
        self.assertIn("harborline software", output)
        self.assertIn("fictional source", source)
        self.assertIn("fictional output", output)

    def test_behavior_cases_cover_required_edges(self):
        cases = read(PACKAGE / "examples" / "fixtures" / "behavior-cases.md")
        expected = {
            "CASE-PRS-001": "No draft",
            "CASE-PRS-002": "Wrong document type",
            "CASE-PRS-003": "Missing decision facts",
            "CASE-PRS-004": "Decision call",
            "CASE-PRS-005": "Informational pre-read",
            "CASE-PRS-006": "Persistent quality failure",
            "CASE-PRS-007": "Save and collision",
            "CASE-PRS-008": "Scoped edit",
        }
        for case_id, title in expected.items():
            self.assertEqual(cases.count(case_id), 1, case_id)
            self.assertIn(title, cases)
        self.assertIn("Fictional test fixture", cases)

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

    def test_governed_documents_are_traceable(self):
        prd = read(ROOT / "docs" / "DOC-pre-read-sharpener-product-requirements-v1.0.md")
        inventory = read(ROOT / "docs" / "DOC-pre-read-sharpener-source-inventory-v1.0.md")
        requirements = set(re.findall(r"\bPRS-REQ-\d{3}\b", prd))
        acceptance = set(re.findall(r"\bPRS-AT-\d{3}\b", prd))
        self.assertEqual(requirements, {f"PRS-REQ-{number:03d}" for number in range(1, 13)})
        self.assertEqual(acceptance, {f"PRS-AT-{number:03d}" for number in range(1, 13)})
        inventory_requirements = set(re.findall(r"\bPRS-REQ-\d{3}\b", inventory))
        self.assertTrue(inventory_requirements.issubset(requirements))
        for requirement in requirements:
            self.assertGreaterEqual(prd.count(requirement), 2, requirement)
        self.assertIn("status: Draft", prd)
        self.assertIn("normative: false", prd)

    def test_catalog_links_to_package_and_governed_documents(self):
        catalog_path = ROOT / "docs" / "SKILL-CATALOG.md"
        catalog = read(catalog_path)
        section = catalog.split("- `pre-read-sharpener`", 1)[1].split("\n- `product-page-copywriter`", 1)[0]
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", section):
            self.assertTrue((catalog_path.parent / target).resolve().is_file(), target)


if __name__ == "__main__":
    unittest.main()
