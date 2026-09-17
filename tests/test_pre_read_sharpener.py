import hashlib
import re
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills" / "pre-read-sharpener"
EXAMPLE = PACKAGE / "examples" / "fictional-rollout-decision"
SETUP_FIXTURE = PACKAGE / "examples" / "fixtures" / "setup-smoke-test.md"
NORMAL_RUN = PACKAGE / "references" / "RUN-pre-read-sharpener-workflow.md"
SETUP_CONTRACT = PACKAGE / "references" / "REF-pre-read-sharpener-setup-contract.md"


def read(path):
    return path.read_text(encoding="utf-8")


def words(value):
    return re.findall(r"\b[\w'-]+\b", value)


def tree_digest(root):
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def persistence_status(receipt, package_digest, configuration_digest):
    if receipt is None:
        return "missing"
    if receipt.get("status") == "blocked":
        return "blocked"
    if receipt.get("package_digest") != package_digest:
        return "stale"
    if receipt.get("configuration_digest") != configuration_digest:
        return "stale"
    required_checks = (
        "package_closure",
        "source_mapping",
        "destination_mapping",
        "local_permissions",
        "fictional_fixture",
        "package_unchanged",
    )
    if any(receipt.get("checks", {}).get(check) != "passed" for check in required_checks):
        return "blocked"
    return "ready"


class PreReadSharpenerPublicTest(unittest.TestCase):
    def test_package_is_complete_and_directly_installable(self):
        required = {
            "README.md",
            "SKILL.md",
            "agents/openai.yaml",
            "assets/output-template.md",
            "assets/setup-config.yaml",
            "assets/setup-receipt.yaml",
            "examples/EX-synthetic.md",
            "examples/fictional-rollout-decision/source-draft.md",
            "examples/fictional-rollout-decision/review-and-rewrite.md",
            "examples/fixtures/behavior-cases.md",
            "examples/fixtures/setup-smoke-test.md",
            "references/RUN-pre-read-sharpener-workflow.md",
            "references/REF-pre-read-sharpener-setup-contract.md",
            "references/REF-decision-ready-criteria.md",
            "references/REF-evidence-and-privacy.md",
        }
        missing = [relative for relative in sorted(required) if not (PACKAGE / relative).is_file()]
        self.assertEqual(missing, [])
        self.assertFalse((PACKAGE / "assets" / "setup-mapping.md").exists())
        self.assertFalse((PACKAGE / "assets" / "setup-receipt.md").exists())
        self.assertFalse(
            (PACKAGE / "references" / "RUN-pre-read-sharpener-setup-workflow.md").exists()
        )

        skill = read(PACKAGE / "SKILL.md")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertEqual(set(yaml.safe_load(frontmatter)), {"name", "description"})
        for target in re.findall(r"`((?:references|assets|examples)/[^`]+)`", skill):
            self.assertTrue((PACKAGE / target).is_file(), target)
        self.assertNotIn("docs/", skill)

    def test_sole_run_is_normal_execution_without_setup_detail(self):
        run_files = sorted((PACKAGE / "references").glob("RUN-*.md"))
        self.assertEqual([path.name for path in run_files], [NORMAL_RUN.name])
        workflow = read(NORMAL_RUN)
        self.assertIn("# Pre-Read Sharpener Workflow", workflow)
        self.assertIn("## Output-route preflight", workflow)
        self.assertIn("## Step 0 — Accept input", workflow)
        self.assertIn("## Step 6 — Return", workflow)
        self.assertNotIn("| Source ID | Purpose | Kind | Locator |", workflow)
        self.assertNotIn("| Destination ID | Artifact | Location |", workflow)
        self.assertNotIn("## 1. Setup profile", workflow)
        self.assertNotIn("## 8. Safe test run", workflow)

    def test_setup_contract_is_separate_and_complete(self):
        contract = read(SETUP_CONTRACT)
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
        positions = [contract.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("**Setup profile:** `local-persistence`", contract)
        self.assertIn(
            "| Source ID | Purpose | Kind | Locator | Authorization method | Data class | Required | Read check |",
            contract,
        )
        self.assertIn(
            "| Destination ID | Artifact | Location | Write mode | Visibility | Retention | External approval | Required | Write check |",
            contract,
        )
        for state in ("ready", "missing", "stale", "blocked"):
            self.assertIn(state, contract)
        for term in ("publishing", "notifications", "scheduling", "production"):
            self.assertIn(term, contract.lower())

    def test_router_bypasses_setup_when_not_applicable(self):
        skill = read(PACKAGE / "SKILL.md")
        for required in (
            "For `inline`",
            "do not load the setup contract",
            "explicit setup",
            "`missing`, `stale`, or `blocked`",
            "local-persistence",
        ):
            self.assertIn(required, skill)
        self.assertIn("Inline work bypasses setup", skill)
        self.assertIn("Setup completion must not rewrite or delete installed package files", skill)

    def test_yaml_setup_assets_are_blank_and_machine_readable(self):
        config = yaml.safe_load(read(PACKAGE / "assets" / "setup-config.yaml"))
        receipt = yaml.safe_load(read(PACKAGE / "assets" / "setup-receipt.yaml"))
        self.assertEqual(config["skill_slug"], "pre-read-sharpener")
        self.assertEqual(config["setup_profile"], "local-persistence")
        self.assertEqual({source["id"] for source in config["sources"]}, {
            "PRS-SRC-DRAFT",
            "PRS-SRC-FIXTURE",
        })
        self.assertEqual(
            {destination["id"] for destination in config["destinations"]},
            {"PRS-DST-OUTPUT", "PRS-DST-CONFIG", "PRS-DST-RECEIPT", "PRS-DST-TEST"},
        )
        self.assertIn("{authorized-workspace}", config["receipt_path"])
        self.assertEqual(receipt["skill_slug"], "pre-read-sharpener")
        self.assertEqual(receipt["normal_entrypoint"], "references/RUN-pre-read-sharpener-workflow.md")
        self.assertEqual(receipt["limitations"], [])
        self.assertNotRegex(
            read(PACKAGE / "assets" / "setup-config.yaml")
            + read(PACKAGE / "assets" / "setup-receipt.yaml"),
            r"/" + r"Users/|https?://|\bsk-[A-Za-z0-9_-]{16,}\b",
        )

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
        self.assertIn("Partial credit does not exist", criteria)
        self.assertIn("after three revision rounds", criteria)

    def test_workflow_covers_review_repair_routes_persistence_and_edits(self):
        workflow = read(NORMAL_RUN)
        for required in (
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
            "For an `inline` route, skip this step",
            "Do not silently choose another destination",
        ):
            self.assertIn(required, workflow)

    def test_setup_fixture_is_complete_and_internally_consistent(self):
        fixture = read(SETUP_FIXTURE)
        for required in (
            "Fictional setup fixture",
            "local-persistence",
            "PRS-SRC-DRAFT",
            "PRS-SRC-FIXTURE",
            "PRS-DST-OUTPUT",
            "PRS-DST-CONFIG",
            "PRS-DST-RECEIPT",
            "PRS-DST-TEST",
            "examples/fictional-rollout-decision/source-draft.md",
            "approve-the-four-week-guided-import-expansion",
            "ten passing criteria",
            'status: "ready"',
            "RUN-pre-read-sharpener-workflow.md",
            "package is unchanged",
            "missing",
            "stale",
            "blocked",
        ):
            self.assertIn(required, fixture)
        self.assertNotRegex(fixture, r"/" + r"Users/|https?://|\b(?:TODO|TBD)\b")

    def test_isolated_fixture_writes_only_workspace_and_preserves_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / "test-install" / "pre-read-sharpener"
            workspace = root / "test-workspace"
            shutil.copytree(PACKAGE, installed)
            before = tree_digest(installed)

            state = workspace / ".pmm-skills" / "pre-read-sharpener"
            output = workspace / "outputs" / "pre-reads"
            state.mkdir(parents=True)
            output.mkdir(parents=True)
            config = yaml.safe_load(read(installed / "assets" / "setup-config.yaml"))
            config["package"]["path"] = str(installed)
            config["destinations"][0]["location"] = str(output)
            config_path = state / "setup-config.yaml"
            config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

            content = read(installed / "examples" / "fictional-rollout-decision" / "review-and-rewrite.md")
            first = output / "2026-10-02-approve-the-four-week-guided-import-expansion-pre-read.md"
            second = output / "2026-10-02-approve-the-four-week-guided-import-expansion-pre-read-2.md"
            first.write_text(content, encoding="utf-8")
            second.write_text(content, encoding="utf-8")

            receipt = yaml.safe_load(read(installed / "assets" / "setup-receipt.yaml"))
            receipt.update(
                {
                    "status": "ready",
                    "package_digest": before,
                    "configuration_path": str(config_path),
                    "configuration_digest": hashlib.sha256(config_path.read_bytes()).hexdigest(),
                }
            )
            receipt["checks"] = {key: "passed" for key in receipt["checks"]}
            receipt_path = state / "setup-receipt.yaml"
            receipt_path.write_text(yaml.safe_dump(receipt, sort_keys=False), encoding="utf-8")

            self.assertEqual(persistence_status(receipt, before, receipt["configuration_digest"]), "ready")
            self.assertEqual(tree_digest(installed), before)
            self.assertEqual(first.read_text(encoding="utf-8"), second.read_text(encoding="utf-8"))
            self.assertEqual({path.name for path in output.iterdir()}, {first.name, second.name})

    def test_receipt_status_routes_ready_missing_stale_and_blocked(self):
        receipt = yaml.safe_load(read(PACKAGE / "assets" / "setup-receipt.yaml"))
        receipt.update(
            {
                "status": "ready",
                "package_digest": "package-a",
                "configuration_digest": "config-a",
                "installed_at": "2026-01-01T00:00:00Z",
                "verified_at": "2026-01-01T00:00:00Z",
            }
        )
        receipt["checks"] = {key: "passed" for key in receipt["checks"]}
        self.assertEqual(persistence_status(receipt, "package-a", "config-a"), "ready")
        self.assertEqual(persistence_status(None, "package-a", "config-a"), "missing")
        self.assertEqual(persistence_status(receipt, "package-b", "config-a"), "stale")
        self.assertEqual(persistence_status(receipt, "package-a", "config-b"), "stale")
        receipt["verified_at"] = "2036-01-01T00:00:00Z"
        self.assertEqual(persistence_status(receipt, "package-a", "config-a"), "ready")
        receipt["checks"]["local_permissions"] = "failed"
        self.assertEqual(persistence_status(receipt, "package-a", "config-a"), "blocked")

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

    def test_completed_example_agenda_and_self_check_are_complete(self):
        example = read(EXAMPLE / "review-and-rewrite.md")
        agenda = example.split("## Suggested agenda\n", 1)[1].split("\n**Deciding question", 1)[0]
        agenda_items = re.findall(r"^- (.+)$", agenda, re.MULTILINE)
        self.assertEqual(len(agenda_items), 4)
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

    def test_behavior_cases_cover_editorial_and_routing_edges(self):
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
            "CASE-PRS-009": "Inline bypass",
            "CASE-PRS-010": "Ready persistence route",
            "CASE-PRS-011": "Missing receipt",
            "CASE-PRS-012": "Stale receipt",
            "CASE-PRS-013": "Blocked persistence",
            "CASE-PRS-014": "Explicit setup request",
        }
        for case_id, title in expected.items():
            self.assertEqual(cases.count(case_id), 1, case_id)
            self.assertIn(title, cases)
        self.assertIn("Fictional test fixture", cases)

    def test_public_slice_has_no_obvious_private_or_credential_material(self):
        blocked = re.compile(
            r"/" + r"Users/|@" + "poly" + "gon" + r"|channel[_ -]?id\s*[:=]|api[_ -]?key\s*[:=]|"
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

    def test_governed_documents_are_traceable_and_history_is_superseded(self):
        prd = read(ROOT / "docs" / "DOC-pre-read-sharpener-product-requirements-v1.2.md")
        inventory = read(ROOT / "docs" / "DOC-pre-read-sharpener-source-inventory-v1.2.md")
        requirements = set(re.findall(r"\bPRSR-REQ-\d{3}\b", prd))
        acceptance = set(re.findall(r"\bPRSR-AT-\d{3}\b", prd))
        self.assertEqual(requirements, {f"PRSR-REQ-{number:03d}" for number in range(1, 13)})
        self.assertEqual(acceptance, {f"PRSR-AT-{number:03d}" for number in range(1, 13)})
        self.assertTrue(set(re.findall(r"\bPRSR-REQ-\d{3}\b", inventory)).issubset(requirements))
        for requirement in requirements:
            self.assertGreaterEqual(prd.count(requirement), 2, requirement)
        self.assertIn("status: Draft", prd)
        self.assertIn("normative: false", prd)
        for historical in (
            "DOC-pre-read-sharpener-product-requirements-v1.1.md",
            "DOC-pre-read-sharpener-source-inventory-v1.1.md",
        ):
            content = read(ROOT / "docs" / historical)
            self.assertIn("status: Superseded", content)
            self.assertIn("v1.2", content)

    def test_catalog_links_to_current_package_and_governed_documents(self):
        catalog_path = ROOT / "docs" / "SKILL-CATALOG.md"
        catalog = read(catalog_path)
        section = catalog.split("- `pre-read-sharpener`", 1)[1].split("\n- `product-page-copywriter`", 1)[0]
        self.assertIn("inline", section.lower())
        self.assertIn("local persistence", section.lower())
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", section):
            self.assertTrue((catalog_path.parent / target).resolve().is_file(), target)


if __name__ == "__main__":
    unittest.main()
