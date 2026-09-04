import re
import unittest
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/comp-intel"
EXAMPLE = PACKAGE / "examples/fictional-embedded-wallets"

TEMPLATE_EXAMPLES = {
    "market-pack-template.yaml": "market-pack.yaml",
    "onboarding-state-template.md": "onboarding-state.md",
    "source-map-template.md": "source-map.md",
    "adopter-positioning-template.md": "adopter-positioning.md",
    "competitor-registry-template.md": "competitor-registry.md",
    "positioning-context-template.md": "positioning-context.md",
    "stakeholder-lens-template.yaml": "stakeholder-lens.yaml",
    "tracker-templates.md": "trackers.md",
    "run-record-template.md": "run-record.md",
    "evidence-log-template.md": "evidence-log.md",
    "output-template.md": "draft-briefing.md",
}

COMPETITORS = {
    "AP": "AsterPort",
    "BA": "BrindleAuth",
    "CK": "CinderKey",
    "DW": "Dovetail Wallets",
    "EP": "EmberPass",
    "FA": "FableAccount",
}

SOURCE_FAMILIES = {
    "homepage",
    "product",
    "pricing",
    "blog",
    "changelog",
    "releases",
    "docs",
    "repository",
    "social",
}


def read(path):
    return path.read_text(encoding="utf-8")


def h2_headings(path):
    return {line for line in read(path).splitlines() if line.startswith("## ")}


def markdown_table_headers(path):
    lines = read(path).splitlines()
    headers = set()
    for index, line in enumerate(lines[:-1]):
        if not (line.startswith("|") and line.endswith("|")):
            continue
        separator = lines[index + 1]
        if not (separator.startswith("|") and separator.endswith("|")):
            continue
        stripped = separator.replace("|", "").replace("-", "").replace(":", "")
        if not stripped.strip():
            headers.add(line)
    return headers


def parse_iso(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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

    def test_every_human_template_has_exactly_one_completed_counterpart(self):
        self.assertEqual(
            {path.name for path in EXAMPLE.iterdir() if path.is_file()},
            set(TEMPLATE_EXAMPLES.values()),
        )

        for template_name, example_name in TEMPLATE_EXAMPLES.items():
            template = PACKAGE / "assets" / template_name
            example = EXAMPLE / example_name
            self.assertTrue(template.is_file(), template_name)
            self.assertTrue(example.is_file(), example_name)
            self.assertGreater(len(read(example)), len(read(template)), example_name)

            if template.suffix == ".yaml":
                template_data = yaml.safe_load(read(template))
                example_data = yaml.safe_load(read(example))
                self.assertTrue(
                    set(template_data).issubset(example_data),
                    f"{example_name} omits template fields",
                )
                continue

            template_headings = h2_headings(template)
            example_headings = h2_headings(example)
            variable_prefixes = ("## Extended profile:", "## Versus")
            fixed_headings = {
                heading
                for heading in template_headings
                if not heading.startswith(variable_prefixes)
            }
            self.assertTrue(
                fixed_headings.issubset(example_headings),
                f"{example_name} omits template headings",
            )
            for prefix in variable_prefixes:
                if any(heading.startswith(prefix) for heading in template_headings):
                    self.assertTrue(
                        any(heading.startswith(prefix) for heading in example_headings),
                        f"{example_name} omits {prefix}",
                    )
            self.assertTrue(
                markdown_table_headers(template).issubset(markdown_table_headers(example)),
                f"{example_name} omits template table fields",
            )

    def test_completed_examples_have_no_scaffold_placeholders(self):
        forbidden = [
            r"\breplace-[a-z0-9-]+",
            r"\[market-id\]",
            r"\[source-id\]",
            r"\[YYYY-MM-DD\]",
            r"\[competitor\]",
            r"\[run ID\]",
            r"\[claim ID\]",
            r"\[source candidate\]",
            r"\bTBD\b",
            r"\bTODO\b",
        ]
        findings = []
        for path in EXAMPLE.iterdir():
            text = read(path)
            for pattern in forbidden:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    findings.append(f"{path.name}: {pattern}")
        self.assertEqual(findings, [])

    def test_example_roster_source_families_and_input_counts_are_complete(self):
        market_pack = yaml.safe_load(read(EXAMPLE / "market-pack.yaml"))
        self.assertEqual(market_pack["market_id"], "harborkey-embedded-wallets")
        self.assertEqual(market_pack["scope"]["scope_type"], "product")
        self.assertEqual(market_pack["scope"]["product"], "HarborKey Wallet Platform")
        self.assertEqual(market_pack["scope"]["geography"], "not-applicable")
        self.assertEqual(len(market_pack["competitors"]), 6)
        self.assertEqual(
            {item["status"] for item in market_pack["competitors"]},
            {"active", "monitor", "watchlist"},
        )

        source_map = read(EXAMPLE / "source-map.md")
        rows = {}
        for line in source_map.splitlines():
            match = re.match(
                r"\| ([A-Z]{2})-WEB-\d{2} \| ([^|]+) \| ([^|]+) \|", line
            )
            if match:
                rows.setdefault(match.group(1), []).append(
                    (match.group(2).strip(), match.group(3).strip())
                )
        self.assertEqual(set(rows), set(COMPETITORS))
        for prefix, competitor in COMPETITORS.items():
            self.assertEqual(len(rows[prefix]), 9, competitor)
            self.assertEqual({row[0] for row in rows[prefix]}, {competitor})
            self.assertEqual({row[1] for row in rows[prefix]}, SOURCE_FAMILIES)

        self.assertEqual(len(re.findall(r"^\| INT-0[1-3] \| Slack \|", source_map, re.M)), 3)
        self.assertEqual(len(re.findall(r"^\| HK-SRC-0[3-5] \| Drive \|", source_map, re.M)), 3)
        self.assertEqual(len(re.findall(r"^\| INT-04 \| local files \|", source_map, re.M)), 1)
        self.assertEqual(len(re.findall(r"^\| COM-01 \|", source_map, re.M)), 1)

        onboarding = read(EXAMPLE / "onboarding-state.md")
        pending_url = "https://asterport.example.invalid/migrate/"
        self.assertIn(pending_url, onboarding)
        self.assertNotIn(pending_url, source_map)

    def test_cross_file_ids_resolve(self):
        all_text = "\n".join(read(path) for path in EXAMPLE.iterdir() if path.is_file())
        evidence_log = read(EXAMPLE / "evidence-log.md")
        source_map = read(EXAMPLE / "source-map.md")
        briefing = read(EXAMPLE / "draft-briefing.md")
        positioning = read(EXAMPLE / "adopter-positioning.md")
        trackers = read(EXAMPLE / "trackers.md")

        evidence_defined = set(re.findall(r"^\| (E-\d{3}) \|", evidence_log, re.M))
        evidence_referenced = set(re.findall(r"\bE-\d{3}\b", all_text))
        self.assertTrue(evidence_referenced.issubset(evidence_defined))

        source_defined = set(
            re.findall(
                r"^\| ((?:[A-Z]{2}-WEB-\d{2}|HK-SRC-\d{2}|INT-\d{2}|COM-\d{2})) \|",
                source_map,
                re.M,
            )
        )
        source_referenced = set(
            re.findall(
                r"\b(?:[A-Z]{2}-WEB-\d{2}|HK-SRC-\d{2}|INT-\d{2}|COM-\d{2})\b",
                all_text,
            )
        )
        self.assertTrue(source_referenced.issubset(source_defined))
        self.assertEqual(re.findall(r"\b[A-Z]{2}-WEB\b(?!-)", all_text), [])

        adopter_claims = set(re.findall(r"^\| (HK-CL-\d{2}) \|", positioning, re.M))
        self.assertTrue(set(re.findall(r"\bHK-CL-\d{2}\b", all_text)).issubset(adopter_claims))

        briefing_claims = set(re.findall(r"^\| (C-\d{3}) \|", briefing, re.M))
        self.assertTrue(set(re.findall(r"\bC-\d{3}\b", all_text)).issubset(briefing_claims))

        tracker_ids = set(re.findall(r"^\| ((?:GAP|NAR|SIG|WATCH)-\d{3}) \|", trackers, re.M))
        tracker_refs = set(re.findall(r"\b(?:GAP|NAR|SIG|WATCH)-\d{3}\b", all_text))
        self.assertTrue(tracker_refs.issubset(tracker_ids))

        for name in TEMPLATE_EXAMPLES.values():
            if name == "stakeholder-lens.yaml":
                continue
            self.assertIn("harborkey-embedded-wallets", read(EXAMPLE / name), name)
        for name in ("evidence-log.md", "run-record.md", "draft-briefing.md", "trackers.md"):
            self.assertIn("harborkey-wallets-2026-09-01", read(EXAMPLE / name), name)

    def test_example_chronology_honors_review_gates(self):
        source_map = read(EXAMPLE / "source-map.md")
        positioning = read(EXAMPLE / "adopter-positioning.md")
        run_record = read(EXAMPLE / "run-record.md")

        source_verified = parse_iso(
            re.search(r"Version/verified date: ([^\n]+)", source_map).group(1)
        )
        positioning_approved = parse_iso(
            re.search(r"Last reviewed: ([^\n]+)", positioning).group(1)
        )
        collection_started = parse_iso(
            re.search(r"\| collect \| ([^ |]+) \|", run_record).group(1)
        )
        evidence_review_completed = parse_iso(
            re.search(r"\| evidence-review \| [^|]+ \| ([^ |]+) \|", run_record).group(1)
        )
        synthesis_started = parse_iso(
            re.search(r"\| synthesize \| ([^ |]+) \|", run_record).group(1)
        )
        self.assertLess(source_verified, positioning_approved)
        self.assertLess(positioning_approved, collection_started)
        self.assertLessEqual(evidence_review_completed, synthesis_started)
        self.assertIn(
            "No proposed registry, positioning, or tracker change has been applied", run_record
        )

    def test_example_tables_are_well_formed(self):
        failures = []
        for path in EXAMPLE.glob("*.md"):
            expected_columns = None
            for number, line in enumerate(read(path).splitlines(), 1):
                if line.startswith("|") and line.endswith("|"):
                    columns = line.count("|") - 1
                    if expected_columns is None:
                        expected_columns = columns
                    if columns != expected_columns:
                        failures.append(
                            f"{path.name}:{number}: expected {expected_columns}, got {columns}"
                        )
                else:
                    expected_columns = None
        self.assertEqual(failures, [])

    def test_example_uses_only_reserved_web_domains_and_safe_local_references(self):
        url_pattern = re.compile(r"https://[^\s`)>]+")
        findings = []
        for path in EXAMPLE.iterdir():
            text = read(path)
            for url in url_pattern.findall(text):
                host = urlparse(url.rstrip(".,")).hostname or ""
                if not host.endswith(".invalid"):
                    findings.append(f"{path.name}: {url}")
            for pattern in (
                r"/" + r"Users/",
                r"/home/",
                r"[A-Za-z]:\\Users\\",
                r"AKIA[0-9A-Z]{16}",
                r"gh[pousr]_[A-Za-z0-9]{20,}",
                r"(?:api[_-]?key|token|password)\s*[:=]\s*[^\s]+",
            ):
                if re.search(pattern, text, flags=re.IGNORECASE):
                    findings.append(f"{path.name}: {pattern}")
        self.assertEqual(findings, [])

    def test_skill_package_does_not_contain_private_golden_example_terms(self):
        forbidden = [
            r"#wg-",
            r"\bPolygon\b",
            r"\bAggLayer\b",
            r"\bSequence\b",
            r"\bPrivy\b",
            r"\bCrossmint\b",
            r"\bZeroDev\b",
            r"\bWeb3Auth\b",
            r"\bDynamic\b",
            r"\bMagic\b",
            r"\bCapsule\b",
            r"\bTurnkey\b",
            r"\bthirdweb\b",
        ]
        findings = []
        for path in PACKAGE.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = read(path)
            except UnicodeDecodeError:
                continue
            for pattern in forbidden:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    findings.append(f"{path.relative_to(PACKAGE)}: {pattern}")
        self.assertEqual(findings, [])

    def test_evidence_classes_safety_states_and_traceability_are_exercised(self):
        evidence_log = read(EXAMPLE / "evidence-log.md")
        briefing = read(EXAMPLE / "draft-briefing.md")
        combined = evidence_log + "\n" + briefing
        for value in (
            "observed",
            "attributed report",
            "inference",
            "recommendation",
            "unknown",
            "accepted",
            "rejected",
            "conflict",
            "public",
            "internal",
            "LIMITED COVERAGE",
        ):
            self.assertIn(value.lower(), combined.lower(), value)

        evidence_rows = {}
        accepted = set()
        for line in evidence_log.splitlines():
            if not re.match(r"^\| E-\d{3} \|", line):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            evidence_rows[cells[0]] = {"sensitivity": cells[7], "disposition": cells[8]}
            if "accepted" in cells[8]:
                accepted.add(cells[0])

        for name in (
            "competitor-registry.md",
            "positioning-context.md",
            "draft-briefing.md",
            "trackers.md",
        ):
            referenced = set(re.findall(r"\bE-\d{3}\b", read(EXAMPLE / name)))
            self.assertTrue(referenced.issubset(accepted), name)

        for line in briefing.splitlines():
            if not re.match(r"^\| C-\d{3} \|", line):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if cells[2] != "observed":
                continue
            ids = re.findall(r"E-\d{3}", cells[4])
            self.assertTrue(ids, cells[0])
            self.assertTrue(
                any(evidence_rows[item]["sensitivity"] == "public" for item in ids),
                f"{cells[0]} has no public support",
            )

        self.assertIn(
            "Internal evidence cannot support an external claim without corroborating public evidence.",
            briefing,
        )

    def test_skill_is_agent_neutral_and_method_first(self):
        skill = read(PACKAGE / "SKILL.md")
        normalized = " ".join(skill.split())
        self.assertIn("Claude Code, Codex", skill)
        self.assertIn("The method is the product", skill)
        self.assertIn("optional advanced mode", normalized)
        self.assertNotIn("Codex Desktop is the supported", skill)

    def test_onboarding_requires_verification_before_canonical_or_content_access(self):
        onboarding = read(PACKAGE / "references/RUN-onboarding.md")
        normalized = " ".join(onboarding.lower().split())
        self.assertIn(
            "only after the pmm verifies a candidate may it be written to `source-map.md`",
            normalized,
        )
        self.assertIn("do not read messages or document bodies yet", normalized)
        self.assertIn("ask the pmm which sources may be read", normalized)

        source_map = read(EXAMPLE / "source-map.md").lower()
        onboarding_state = read(EXAMPLE / "onboarding-state.md").lower()
        self.assertNotIn("| pending", source_map)
        self.assertIn("pending competitor-source candidates", onboarding_state)

    def test_example_is_a_scoped_limited_first_baseline(self):
        positioning = read(EXAMPLE / "adopter-positioning.md")
        run_record = read(EXAMPLE / "run-record.md")
        briefing = read(EXAMPLE / "draft-briefing.md")
        self.assertIn("Status: Approved", positioning)
        self.assertIn("| Mode | baseline |", run_record)
        self.assertIn("Approved adopter positioning", run_record)
        self.assertIn("| Coverage status | limited |", run_record)
        self.assertIn("LIMITED COVERAGE", briefing)
        self.assertIn("Highest-value source to add next", briefing)
        self.assertIn("AsterPort migration guide", briefing)
        self.assertIn("only an approved link may enter `source-map.md`", briefing)


if __name__ == "__main__":
    unittest.main()
