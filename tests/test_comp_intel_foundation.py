import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = ROOT / "skills/comp-intel/scripts"
sys.path.insert(0, str(SCRIPT_ROOT))

from comp_intel_core import CompIntelController, WorkflowError  # noqa: E402
from comp_intel_core.io_utils import atomic_write_json, digest_value, parse_jsonl, read_json  # noqa: E402


class CompIntelFoundationTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.data_root = Path(self.temporary.name) / "data"
        self.controller = CompIntelController(self.data_root)
        self.controller.init()

    def tearDown(self):
        self.temporary.cleanup()

    def collect(self, run_id="run_test", runtime_mode="interactive"):
        return self.controller.collect(
            "synthetic-devtools",
            "2026-08-18",
            "2026-08-26",
            observed_at="2026-08-26T12:00:00Z",
            run_id=run_id,
            runtime_mode=runtime_mode,
        )

    def approve_evidence(self, run_id="run_test"):
        template = read_json(self.data_root / f"runs/{run_id}/reviews/evidence-approval-template.json")
        template.update({
            "approval_id": "apr-evidence-reviewed",
            "decided_at": "2026-08-26T13:00:00Z",
            "comment": "Fictional fixture coverage reviewed.",
        })
        template["approver"]["id"] = "fictional-evidence-reviewer"
        path = Path(self.temporary.name) / f"{run_id}-evidence-approval.json"
        atomic_write_json(path, template)
        return self.controller.install_evidence_approval(run_id, path)

    def synthesis_package(self, run_id="run_test"):
        run_dir = self.data_root / f"runs/{run_id}"
        evidence = parse_jsonl(run_dir / "collection/evidence.jsonl")
        by_native = {record["source"]["native_id"]: record for record in evidence}
        support = [
            by_native["bluepeak-release-17"]["evidence_id"],
            by_native["bluepeak-docs-dashboard"]["evidence_id"],
        ]
        manifest = read_json(run_dir / "collection/evidence-manifest.json")
        registry = read_json(self.data_root / "state/markets/synthetic-devtools.json")
        return {
            "schema_version": 1,
            "run_id": run_id,
            "market_id": "synthetic-devtools",
            "evidence_digest": manifest["evidence_digest"],
            "claims": [
                {
                    "schema_version": 1,
                    "claim_id": "cl-dashboard-documented",
                    "market_id": "synthetic-devtools",
                    "competitor_id": "bluepeak",
                    "claim_type": "observation",
                    "text": "BluePeak documents a fictional team usage dashboard.",
                    "evidence_ids": support,
                    "confidence": "high",
                    "sensitivity": "public",
                    "limitations": ["Documentation does not establish customer adoption."],
                },
                {
                    "schema_version": 1,
                    "claim_id": "cl-comparison-gap",
                    "market_id": "synthetic-devtools",
                    "competitor_id": "bluepeak",
                    "claim_type": "recommendation",
                    "text": "Review whether dashboard comparison guidance needs an update.",
                    "evidence_ids": support,
                    "confidence": "medium",
                    "sensitivity": "public",
                    "limitations": ["This is analysis, not an observed market fact."],
                },
            ],
            "report": {
                "executive_signals": [{
                    "text": "A documented fictional dashboard may change capability comparisons.",
                    "claim_ids": ["cl-dashboard-documented", "cl-comparison-gap"],
                }],
                "coverage": ["Required synthetic feed and optional local fixture were collected."],
                "limitations": ["A local note is private and excluded from this public-safe selection."],
                "material_changes": [{
                    "text": "The fictional dashboard is documented by two first-party sources.",
                    "claim_ids": ["cl-dashboard-documented"],
                }],
                "implications": [{
                    "text": "Reporting may deserve a comparison-criteria review.",
                    "claim_ids": ["cl-comparison-gap"],
                }],
                "open_questions": ["No adoption evidence is available."],
                "next_actions": [{
                    "text": "Review the comparison criterion with its owner.",
                    "claim_ids": ["cl-comparison-gap"],
                }],
                "selected_claim_ids": ["cl-dashboard-documented", "cl-comparison-gap"],
                "public_safe": True,
            },
            "proposed_change_set": {
                "schema_version": 1,
                "change_set_id": "cs-dashboard-review",
                "run_id": run_id,
                "market_id": "synthetic-devtools",
                "base_registry_digest": digest_value(registry),
                "evidence_digest": manifest["evidence_digest"],
                "changes": [
                    {
                        "operation": "set_field",
                        "path": ["competitors", "bluepeak", "capabilities", "usage_dashboard"],
                        "value": {"status": "documented"},
                        "claim_ids": ["cl-dashboard-documented"],
                    },
                    {
                        "operation": "append_tracker_event",
                        "tracker": "battlecard_gaps",
                        "event": {"competitor_id": "bluepeak", "gap": "Review dashboard comparison guidance", "status": "open"},
                        "claim_ids": ["cl-comparison-gap"],
                    },
                ],
                "status": "proposed",
            },
        }

    def submit_synthesis(self, run_id="run_test"):
        package_path = Path(self.temporary.name) / f"{run_id}-synthesis.json"
        atomic_write_json(package_path, self.synthesis_package(run_id))
        return self.controller.submit_synthesis(run_id, package_path)

    def approve_apply(self, run_id="run_test"):
        template = read_json(self.data_root / f"runs/{run_id}/reviews/apply-approval-template.json")
        template.update({
            "approval_id": "apr-apply-reviewed",
            "decided_at": "2026-08-26T14:00:00Z",
            "comment": "Fictional changes reviewed.",
        })
        template["approver"]["id"] = "fictional-apply-approver"
        path = Path(self.temporary.name) / f"{run_id}-apply-approval.json"
        atomic_write_json(path, template)
        return self.controller.install_apply_approval(run_id, path)

    def test_initialization_is_non_destructive_and_exposes_mapping_checklist(self):
        mapping = read_json(self.data_root / "mapping.json")
        self.assertEqual(mapping["status"], "unmapped")
        self.assertIn("channels_and_users", mapping)
        with self.assertRaises(WorkflowError) as raised:
            self.controller.init()
        self.assertEqual(raised.exception.category, "usage/config")

    def test_collection_is_deterministic_and_preserves_quality_signals(self):
        first = self.collect("run_first")
        second_root = Path(self.temporary.name) / "second"
        second = CompIntelController(second_root)
        second.init()
        second.collect(
            "synthetic-devtools", "2026-08-18", "2026-08-26",
            observed_at="2026-08-26T12:00:00Z", run_id="run_second",
        )
        first_manifest = read_json(self.data_root / "runs/run_first/collection/evidence-manifest.json")
        second_manifest = read_json(second_root / "runs/run_second/collection/evidence-manifest.json")
        self.assertEqual(first_manifest["evidence_digest"], second_manifest["evidence_digest"])
        self.assertEqual(first["stage"], "evidence_review")

        evidence = parse_jsonl(self.data_root / "runs/run_first/collection/evidence.jsonl")
        by_native = {record["source"]["native_id"]: record for record in evidence}
        self.assertEqual(by_native["bluepeak-release-17"]["collection"]["observations"], 2)
        self.assertEqual(by_native["search-result-42"]["classification"], "reported")
        self.assertEqual(by_native["search-result-42"]["confidence"], "low")
        self.assertTrue(by_native["bluepeak-release-17"]["relationships"]["corroborates"])
        self.assertTrue(by_native["cedarworks-limit"]["relationships"]["conflicts_with"])
        self.assertNotIn("old-cedarworks-release", by_native)
        self.assertIn("not an instruction", by_native["hostile-source"]["content"]["summary"])
        revisions = [record for record in evidence if record["source"]["native_id"] == "northstar-homepage"]
        self.assertEqual(len(revisions), 2)
        self.assertEqual(sum(bool(record["relationships"]["supersedes"]) for record in revisions), 1)
        coverage = read_json(self.data_root / "runs/run_first/collection/coverage.json")
        self.assertEqual(
            {item["competitor_id"] for item in coverage["competitors"]},
            {"bluepeak", "cedarworks", "northstar-labs"},
        )
        near_duplicates = coverage["normalization"]["near_duplicates"]
        self.assertTrue(any(item["decision"] == "candidate_near_duplicate" for item in near_duplicates))

    def test_missing_required_capability_blocks_before_run_creation(self):
        market_path = self.data_root / "markets/synthetic-devtools.json"
        market = read_json(market_path)
        market["sources"][0]["config"]["fixture_path"] = "fixtures/missing.json"
        atomic_write_json(market_path, market)
        with self.assertRaises(WorkflowError) as raised:
            self.collect()
        self.assertEqual(raised.exception.category, "capability")
        self.assertEqual(list((self.data_root / "runs").iterdir()), [])

    def test_required_collection_failure_retains_partial_state_and_does_not_review(self):
        fixture_path = self.data_root / "fixtures/synthetic-source.json"
        fixture = read_json(fixture_path)
        fixture["failure"] = {"after_page": 1, "message": "fictional timeout"}
        atomic_write_json(fixture_path, fixture)
        with self.assertRaises(WorkflowError) as raised:
            self.collect()
        self.assertEqual(raised.exception.category, "collection")
        run = read_json(self.data_root / "runs/run_test/run.json")
        self.assertEqual(run["stage"], "failed")
        self.assertTrue((self.data_root / "runs/run_test/collection/raw/candidates.jsonl").is_file())

    def test_conversation_cannot_substitute_for_evidence_approval(self):
        self.collect()
        package_path = Path(self.temporary.name) / "package.json"
        atomic_write_json(package_path, self.synthesis_package())
        with self.assertRaises(WorkflowError) as raised:
            self.controller.submit_synthesis("run_test", package_path)
        self.assertEqual(raised.exception.category, "approval")
        self.assertEqual(self.controller.status("run_test")["stage"], "evidence_review")

    def test_stale_manifest_invalidates_approval(self):
        self.collect()
        self.approve_evidence()
        manifest_path = self.data_root / "runs/run_test/collection/evidence-manifest.json"
        manifest = read_json(manifest_path)
        manifest["record_count"] += 1
        atomic_write_json(manifest_path, manifest)
        package_path = Path(self.temporary.name) / "package.json"
        atomic_write_json(package_path, self.synthesis_package())
        with self.assertRaises(WorkflowError) as raised:
            self.controller.submit_synthesis("run_test", package_path)
        self.assertEqual(raised.exception.category, "validation")

    def test_unauthorized_approver_is_rejected(self):
        self.collect()
        template = read_json(self.data_root / "runs/run_test/reviews/evidence-approval-template.json")
        template.update({"approval_id": "apr-wrong", "decided_at": "2026-08-26T13:00:00Z", "comment": "Not authorized."})
        template["approver"]["id"] = "fictional-unapproved-reviewer"
        path = Path(self.temporary.name) / "unauthorized.json"
        atomic_write_json(path, template)
        with self.assertRaises(WorkflowError) as raised:
            self.controller.install_evidence_approval("run_test", path)
        self.assertEqual(raised.exception.category, "approval")

    def test_report_statements_require_claim_provenance(self):
        self.collect()
        self.approve_evidence()
        package = self.synthesis_package()
        package["report"]["material_changes"][0]["claim_ids"] = []
        path = Path(self.temporary.name) / "unsupported-report.json"
        atomic_write_json(path, package)
        with self.assertRaises(WorkflowError) as raised:
            self.controller.submit_synthesis("run_test", path)
        self.assertEqual(raised.exception.category, "synthesis")
        self.assertIn("must contain known claims", str(raised.exception))

    def test_public_safe_report_rejects_private_support(self):
        self.collect()
        self.approve_evidence()
        package = self.synthesis_package()
        evidence = parse_jsonl(self.data_root / "runs/run_test/collection/evidence.jsonl")
        private_evidence = next(record for record in evidence if not record["public_safe"])
        package["claims"].append({
            "schema_version": 1,
            "claim_id": "cl-private-note",
            "market_id": "synthetic-devtools",
            "competitor_id": "bluepeak",
            "claim_type": "attributed_report",
            "text": "A fictional private note asks a comparison question.",
            "evidence_ids": [private_evidence["evidence_id"]],
            "confidence": "low",
            "sensitivity": "internal",
            "limitations": ["Private local evidence."],
        })
        package["report"]["selected_claim_ids"].append("cl-private-note")
        path = Path(self.temporary.name) / "private-report.json"
        atomic_write_json(path, package)
        with self.assertRaises(WorkflowError) as raised:
            self.controller.submit_synthesis("run_test", path)
        self.assertEqual(raised.exception.category, "synthesis")
        self.assertIn("non-public support", str(raised.exception))

    def test_full_offline_workflow_applies_provenance_and_tracker_event(self):
        self.collect()
        self.approve_evidence()
        result = self.submit_synthesis()
        self.assertEqual(result["stage"], "draft_review")
        self.approve_apply()
        applied = self.controller.apply("run_test")
        self.assertEqual(applied["stage"], "complete")
        registry = read_json(self.data_root / "state/markets/synthetic-devtools.json")
        self.assertEqual(registry["competitors"]["bluepeak"]["capabilities"]["usage_dashboard"]["status"], "documented")
        self.assertEqual(len(registry["trackers"]["battlecard_gaps"]), 1)
        self.assertIn("run_test", registry["applied_runs"])
        self.assertEqual(self.controller.status("run_test")["integrity"], "valid")
        report = (self.data_root / "outputs/reports/run_test.md").read_text(encoding="utf-8")
        self.assertIn("Status: Draft", report)
        self.assertIn("cl-dashboard-documented", report)

    def test_base_digest_conflict_blocks_without_overwriting_state(self):
        self.collect()
        self.approve_evidence()
        self.submit_synthesis()
        self.approve_apply()
        registry_path = self.data_root / "state/markets/synthetic-devtools.json"
        registry = read_json(registry_path)
        registry["external_revision"] = "concurrent-change"
        atomic_write_json(registry_path, registry)
        expected = registry_path.read_bytes()
        with self.assertRaises(WorkflowError) as raised:
            self.controller.apply("run_test")
        self.assertEqual(raised.exception.category, "conflict")
        self.assertEqual(registry_path.read_bytes(), expected)
        self.assertEqual(read_json(self.data_root / "runs/run_test/run.json")["stage"], "blocked")

    def test_local_path_escape_is_reported_and_blocks_when_required(self):
        market_path = self.data_root / "markets/synthetic-devtools.json"
        market = read_json(market_path)
        local_source = market["sources"][1]
        local_source["required"] = True
        local_source["config"]["files"] = ["../outside.json"]
        atomic_write_json(market_path, market)
        doctor = self.controller.doctor("synthetic-devtools")
        self.assertTrue(doctor["blocking"])
        with self.assertRaises(WorkflowError) as raised:
            self.collect()
        self.assertEqual(raised.exception.category, "capability")

    def test_scheduled_runtime_has_a_mechanical_evidence_review_ceiling(self):
        result = self.collect(runtime_mode="scheduled")
        self.assertEqual(result["stage"], "evidence_review")
        run_dir = self.data_root / "runs/run_test"
        self.assertFalse((run_dir / "synthesis/synthesis-package.json").exists())
        self.assertEqual(read_json(run_dir / "run.json")["runtime"]["mode"], "scheduled")
        template = read_json(run_dir / "reviews/evidence-approval-template.json")
        template.update({"approval_id": "apr-scheduled", "decided_at": "2026-08-26T13:00:00Z", "comment": "Should not install unattended."})
        template["approver"]["id"] = "fictional-evidence-reviewer"
        path = Path(self.temporary.name) / "scheduled-approval.json"
        atomic_write_json(path, template)
        with self.assertRaises(WorkflowError) as raised:
            self.controller.install_evidence_approval("run_test", path, invocation_mode="scheduled")
        self.assertEqual(raised.exception.category, "approval")
        self.assertFalse((run_dir / "approvals/evidence.json").exists())

    def test_cli_returns_machine_readable_status(self):
        self.collect()
        process = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_ROOT / "comp_intel.py"),
                "status",
                "--data-root",
                str(self.data_root),
                "--run-id",
                "run_test",
                "--json",
            ],
            check=True,
            text=True,
            capture_output=True,
        )
        result = json.loads(process.stdout)
        self.assertEqual(result["code"], 0)
        self.assertEqual(result["stage"], "evidence_review")


if __name__ == "__main__":
    unittest.main()
