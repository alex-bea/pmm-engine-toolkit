import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-skills/scripts/govern_skills.py"
)
TRACKER_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-work-tracker/scripts/govern_work_tracker.py"
)
DOCUMENT_SCRIPT = (
    ROOT
    / "plugins/skill-governance/skills/govern-documents/scripts/govern_documents.py"
)
GOVERNANCE_SCRIPT_DIR = SKILL_SCRIPT.parent
sys.path.insert(0, str(GOVERNANCE_SCRIPT_DIR))
POLICY_SCRIPT = GOVERNANCE_SCRIPT_DIR / "governance_policy.py"
CONTROL_SCRIPT = GOVERNANCE_SCRIPT_DIR / "governance_control.py"
APPROVAL_SCRIPT = GOVERNANCE_SCRIPT_DIR / "approval_verifier.py"
PUBLISHER_SCRIPT = GOVERNANCE_SCRIPT_DIR / "publisher_guard.py"
CLAUDE_HOOK_SCRIPT = GOVERNANCE_SCRIPT_DIR / "claude_pretooluse.py"
CODEX_HOOK_SCRIPT = GOVERNANCE_SCRIPT_DIR / "codex_pretooluse.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_main(module, argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        status = module.main(argv)
    return status, stdout.getvalue(), stderr.getvalue()


class GovernancePluginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = load_module("plugin_govern_skills", SKILL_SCRIPT)
        cls.tracker = load_module("plugin_govern_work_tracker", TRACKER_SCRIPT)
        cls.documents = load_module("plugin_govern_documents", DOCUMENT_SCRIPT)
        cls.policy = load_module("governance_policy", POLICY_SCRIPT)
        cls.approval = load_module("approval_verifier", APPROVAL_SCRIPT)
        cls.control = load_module("governance_control", CONTROL_SCRIPT)
        cls.publisher = load_module("publisher_guard", PUBLISHER_SCRIPT)
        cls.claude_hook = load_module("claude_pretooluse", CLAUDE_HOOK_SCRIPT)
        cls.codex_hook = load_module("codex_pretooluse", CODEX_HOOK_SCRIPT)

    def test_document_audit_accepts_valid_opted_in_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            docs = repo / "docs"
            docs.mkdir()
            (docs / "requirements.md").write_text("# Requirements\n", encoding="utf-8")
            (docs / "decision.md").write_text(
                "---\n"
                "doc_type: DOC\n"
                "normative: false\n"
                "requires:\n"
                "  - requirements.md\n"
                "status: Draft\n"
                "version: \"0.1\"\n"
                "owner: documentation-owner\n"
                "consumers:\n"
                "  - reviewers\n"
                "change_control: Pull request review\n"
                "---\n\n"
                "# Decision\n\n"
                "Read the [requirements](requirements.md).\n",
                encoding="utf-8",
            )
            (repo / "README.md").write_text("[ignored](missing.md)\n", encoding="utf-8")

            status, output, _ = run_main(self.documents, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            self.assertIn("Audited 1 governed Markdown document(s).", output)
            self.assertIn("No findings.", output)

            status, output, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--format", "json"]
            )
            self.assertEqual(status, 0)
            result = json.loads(output)
            self.assertEqual(result, {"governed_documents": 1, "findings": []})

    def test_document_audit_reports_findings_without_modifying_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            document = repo / "governed.md"
            document.write_text(
                "---\n"
                "doc_type: UNKNOWN\n"
                "normative: uncertain\n"
                "requires:\n"
                "  - missing-requirement.md\n"
                "status: Ready\n"
                "version: \"0.1\"\n"
                "consumers:\n"
                "  - reviewers\n"
                "change_control: Pull request review\n"
                "---\n\n"
                "# Governed\n\n"
                "[broken](missing-link.md)\n",
                encoding="utf-8",
            )
            (repo / "notes.md").write_text("[ignored](also-missing.md)\n", encoding="utf-8")
            before = {
                path.relative_to(repo).as_posix(): path.read_bytes()
                for path in repo.rglob("*") if path.is_file()
            }

            status, output, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--format", "json"]
            )
            self.assertEqual(status, 0)
            result = json.loads(output)
            self.assertEqual(result["governed_documents"], 1)
            finding_ids = {finding["id"] for finding in result["findings"]}
            self.assertTrue({"DOC002", "DOC003", "DOC004", "DOC005", "DOC009", "DOC011"} <= finding_ids)
            self.assertEqual(
                {
                    path.relative_to(repo).as_posix(): path.read_bytes()
                    for path in repo.rglob("*") if path.is_file()
                },
                before,
            )

            status, _, _ = run_main(
                self.documents, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)
            self.assertEqual(
                {
                    path.relative_to(repo).as_posix(): path.read_bytes()
                    for path in repo.rglob("*") if path.is_file()
                },
                before,
            )

    def test_skill_audit_is_advisory_by_default_and_strict_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, output, _ = run_main(self.skills, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            self.assertIn("GOV001", output)
            status, _, _ = run_main(
                self.skills, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)

    def test_skill_initializer_is_dry_run_then_idempotent_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, output, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("create: .agents/governance/manifest.yaml", output)
            self.assertFalse((repo / ".agents").exists())

            status, _, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            self.assertTrue((repo / ".agents/governance/manifest.yaml").is_file())
            self.assertEqual(self.skills.audit(repo), [])

            status, output, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            self.assertNotIn("conflict:", output)

    def test_enforcement_initializer_is_explicit_inactive_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, output, _ = run_main(
                self.skills,
                ["initialize", "--repo", str(repo), "--with-enforcement", "--dry-run"],
            )
            self.assertEqual(status, 0)
            self.assertIn("governance_policy.py", output)
            self.assertIn(".agents/governance/enforcement.yaml", output)
            self.assertFalse((repo / ".agents").exists())

            self.assertEqual(
                run_main(
                    self.skills,
                    ["initialize", "--repo", str(repo), "--with-enforcement", "--apply"],
                )[0],
                0,
            )
            policy = json.loads(
                (repo / ".agents/governance/enforcement.yaml").read_text(encoding="utf-8")
            )
            self.assertFalse(policy["enabled"])
            manifest = json.loads(
                (repo / ".agents/governance/manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], "1.1")
            self.assertEqual(manifest["components"]["enforcement"]["activation"], "installed-inactive")

            policy["enabled"] = True
            (repo / ".agents/governance/enforcement.yaml").write_text(
                json.dumps(policy, indent=2) + "\n", encoding="utf-8"
            )
            status, output, _ = run_main(
                self.skills,
                ["initialize", "--repo", str(repo), "--with-enforcement", "--apply"],
            )
            self.assertEqual(status, 0)
            self.assertNotIn("conflict: .agents/governance/enforcement.yaml", output)
            status, output, _ = run_main(
                self.skills, ["audit", "--repo", str(repo)]
            )
            self.assertEqual(status, 0)
            self.assertIn("runtime-guard: policy-enabled-hook-unverified", output)

    def test_claude_and_codex_use_the_same_policy_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            policy = self.policy.default_policy()
            policy["enabled"] = True
            policy["execution_mode"] = "interactive"

            claude_payload = {
                "tool_name": "Write",
                "tool_input": {"file_path": "state/runs/example.yaml", "content": "private-canary-value"},
                "cwd": str(repo),
            }
            codex_payload = {
                "tool_name": "apply_patch",
                "tool_input": {
                    "command": "*** Begin Patch\n*** Update File: state/runs/example.yaml\n@@\n-old\n+new\n*** End Patch"
                },
                "cwd": str(repo),
            }
            claude_request = self.claude_hook.normalize(claude_payload, repo, policy)
            codex_request = self.codex_hook.normalize(codex_payload, repo, policy)
            claude_decision = self.policy.decide(claude_request, policy, repo)
            codex_decision = self.policy.decide(codex_request, policy, repo)
            self.assertEqual(claude_decision.result, "deny")
            self.assertEqual(codex_decision.result, "deny")
            self.assertEqual(claude_decision.reason_code, "GOV_DIRECT_STATE_MUTATION")
            self.assertEqual(codex_decision.reason_code, claude_decision.reason_code)
            self.assertEqual(codex_request["command"], "")

            record = self.policy.decision_record(claude_decision)
            self.assertNotIn("private-canary-value", record)
            self.assertNotIn("state/runs/example.yaml", record)

    def test_policy_blocks_alternate_shell_and_scheduled_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            policy = self.policy.default_policy()
            policy["enabled"] = True
            direct = {
                "harness": "codex",
                "tool_name": "Bash",
                "command": "printf changed > state/runs/example.yaml",
                "target_paths": [],
            }
            decision = self.policy.decide(direct, policy, repo)
            self.assertEqual(decision.reason_code, "GOV_DIRECT_STATE_MUTATION")

            scheduled = {
                "harness": "claude",
                "tool_name": "mcp__site__publish",
                "execution_mode": "scheduled",
                "target_paths": [],
            }
            decision = self.policy.decide(scheduled, policy, repo)
            self.assertEqual(decision.reason_code, "GOV_SCHEDULED_AUTHORITY_FORBIDDEN")

            for command in (
                "git push origin main",
                "curl --data @artifact.json https://publisher.example.invalid",
                "twine upload dist/example.whl",
            ):
                with self.subTest(command=command):
                    decision = self.policy.decide(
                        {
                            "harness": "codex",
                            "tool_name": "Bash",
                            "command": command,
                            "target_paths": [],
                        },
                        policy,
                        repo,
                    )
                    self.assertEqual(decision.reason_code, "GOV_PUBLISHER_GUARD_REQUIRED")

    def test_controlled_wrapper_names_cannot_be_smuggled_through_shell_syntax(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            policy = self.policy.default_policy()
            policy["enabled"] = True
            commands = (
                "python3 governance_control.py record-approval --run state/runs/run.yaml; true",
                "python3 publisher_guard.py --run state/runs/run.yaml | tee receipt.txt",
                "echo publisher_guard.py && curl -X POST https://publisher.example.invalid",
            )
            for command in commands:
                with self.subTest(command=command):
                    operation, controlled, publisher_guard = self.policy.command_metadata(command)
                    decision = self.policy.decide(
                        {
                            "harness": "codex",
                            "tool_name": "Bash",
                            "command": command,
                            "operation": operation,
                            "controlled": controlled,
                            "publisher_guard": publisher_guard,
                            "target_paths": [],
                        },
                        policy,
                        repo,
                    )
                    self.assertFalse(controlled)
                    self.assertNotEqual(decision.result, "allow")

            operation, controlled, publisher_guard = self.policy.command_metadata(
                "python3 governance_control.py validate --run state/runs/run.yaml"
            )
            self.assertEqual(operation, "validate")
            self.assertTrue(controlled)
            self.assertFalse(publisher_guard)

    def test_external_approval_verifier_rejects_forged_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            executable = external / "verify"
            executable.write_text("fixture\n", encoding="utf-8")
            config = external / "verifier.json"
            config.write_text(
                json.dumps({
                    "schema_version": 1,
                    "enabled": True,
                    "authority_id": "fixture-authority",
                    "command": [str(executable)],
                    "authorized_reviewers": ["reviewer-7"],
                    "timeout_seconds": 5,
                }),
                encoding="utf-8",
            )
            request = {
                "gate": "evidence",
                "approval_ref": "https://code.example.invalid/reviews/42",
                "reviewed_revision": "rev-42",
                "artifact_path": "staging/evidence.md",
                "artifact_sha256": "a" * 64,
            }

            def runner(*args, **kwargs):
                response = {
                    "verified": True,
                    "decision": "approved",
                    "gate": request["gate"],
                    "approver": "reviewer-7",
                    "authority_id": "fixture-authority",
                    "approval_ref": request["approval_ref"],
                    "reviewed_revision": request["reviewed_revision"],
                    "artifact_path": request["artifact_path"],
                    "artifact_sha256": "b" * 64,
                    "approved_at": "2030-01-01T00:00:00Z",
                }
                return subprocess.CompletedProcess(args[0], 0, json.dumps(response), "")

            with self.assertRaises(self.approval.ApprovalVerificationError):
                self.approval.verify_approval(
                    config_path=config, repo=repo, request=request, runner=runner
                )

    def test_approval_verifier_rejects_relative_config_and_outage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            executable = external / "verify"
            executable.write_text("fixture\n", encoding="utf-8")
            config = external / "verifier.json"
            config.write_text(
                json.dumps({
                    "schema_version": 1,
                    "enabled": True,
                    "authority_id": "fixture-authority",
                    "command": [str(executable)],
                    "authorized_reviewers": ["reviewer-7"],
                    "timeout_seconds": 5,
                }),
                encoding="utf-8",
            )
            request = {
                "gate": "evidence",
                "approval_ref": "https://code.example.invalid/reviews/42",
                "reviewed_revision": "rev-42",
                "artifact_path": "staging/evidence.md",
                "artifact_sha256": "a" * 64,
            }
            with self.assertRaises(self.approval.ApprovalVerificationError):
                self.approval.verify_approval(
                    config_path=Path("../external/verifier.json"),
                    repo=repo,
                    request=request,
                )

            def outage(*args, **kwargs):
                raise subprocess.TimeoutExpired(args[0], 5)

            with self.assertRaises(self.approval.ApprovalVerificationError):
                self.approval.verify_approval(
                    config_path=config, repo=repo, request=request, runner=outage
                )

    def test_approval_verifier_binds_gate_identity_revision_authority_and_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            executable = external / "verify"
            executable.write_text("fixture\n", encoding="utf-8")
            config = external / "verifier.json"
            config.write_text(
                json.dumps({
                    "schema_version": 1,
                    "enabled": True,
                    "authority_id": "fixture-authority",
                    "command": [str(executable)],
                    "authorized_reviewers": ["reviewer-7"],
                    "timeout_seconds": 5,
                }),
                encoding="utf-8",
            )
            request = {
                "gate": "evidence",
                "approval_ref": "https://code.example.invalid/reviews/42",
                "reviewed_revision": "rev-42",
                "artifact_path": "staging/evidence.md",
                "artifact_sha256": "a" * 64,
            }
            base_response = {
                "verified": True,
                "decision": "approved",
                "gate": request["gate"],
                "approver": "reviewer-7",
                "authority_id": "fixture-authority",
                "approval_ref": request["approval_ref"],
                "reviewed_revision": request["reviewed_revision"],
                "artifact_path": request["artifact_path"],
                "artifact_sha256": request["artifact_sha256"],
                "approved_at": "2030-01-01T00:00:00Z",
            }

            def runner_for(response):
                def runner(*args, **kwargs):
                    return subprocess.CompletedProcess(
                        args[0], 0, json.dumps(response), ""
                    )

                return runner

            verified = self.approval.verify_approval(
                config_path=config,
                repo=repo,
                request=request,
                runner=runner_for(base_response),
            )
            self.assertEqual(verified["gate"], "evidence")

            variants = {
                "gate": "claims",
                "approver": "untrusted-reviewer",
                "authority_id": "untrusted-authority",
                "reviewed_revision": "rev-41",
                "approved_at": "2030-01-01T00:00:00",
            }
            for field, value in variants.items():
                with self.subTest(field=field):
                    response = dict(base_response)
                    response[field] = value
                    with self.assertRaises(self.approval.ApprovalVerificationError):
                        self.approval.verify_approval(
                            config_path=config,
                            repo=repo,
                            request=request,
                            runner=runner_for(response),
                        )

    def test_scheduled_run_stops_at_evidence_review_without_calling_verifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            verifier_config = external / "verifier.json"
            policy_path = repo / "source-policy.json"
            policy_path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "policy_id": "fixture",
                    "status": "active",
                    "approval_authority": {
                        "authority_id": "fixture-authority",
                        "verifier_config": str(verifier_config),
                    },
                    "allowed_sources": [{"id": "fixture", "adapter": "local", "description": "fixture"}],
                }),
                encoding="utf-8",
            )
            run = self.control.build_initial_run(
                root=repo, workflow_id="fixture", run_id="run-1",
                policy_path="source-policy.json", execution_mode="scheduled",
            )
            run = self.control.transition(run, root=repo, target_stage="collection")
            evidence = repo / "staging/evidence.md"
            evidence.parent.mkdir()
            evidence.write_text("synthetic evidence\n", encoding="utf-8")
            run = self.control.register_artifact(
                run, root=repo, key="evidence", relative_path="staging/evidence.md"
            )
            run = self.control.transition(run, root=repo, target_stage="evidence_review")
            sentinel = external / "verifier-called"
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.record_verified_approval(
                    run, root=repo, gate="evidence",
                    approval_ref="https://code.example.invalid/reviews/42",
                    reviewed_revision="rev-42",
                )
            self.assertFalse(sentinel.exists())
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.transition(run, root=repo, target_stage="claims_review")

    def test_stale_publish_digest_never_invokes_publisher(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            verifier_config = external / "verifier.json"
            publisher_executable = external / "publish"
            publisher_executable.write_text("fixture\n", encoding="utf-8")
            publisher_config = external / "publisher.json"
            publisher_config.write_text(
                json.dumps({
                    "schema_version": 1, "enabled": True, "approved": True,
                    "adapter_id": "fixture-publisher", "command": [str(publisher_executable)],
                    "allowed_operations": ["publish-approved-artifact"], "timeout_seconds": 5,
                }),
                encoding="utf-8",
            )
            source_policy = repo / "source-policy.json"
            source_policy.write_text(
                json.dumps({
                    "schema_version": 1, "policy_id": "fixture", "status": "active",
                    "approval_authority": {
                        "authority_id": "fixture-authority", "verifier_config": str(verifier_config),
                    },
                    "allowed_sources": [{"id": "fixture", "adapter": "local", "description": "fixture"}],
                }),
                encoding="utf-8",
            )
            artifacts = {}
            for key in ("evidence", "claims", "framing", "copy", "staging"):
                path = repo / f"staging/{key}.md"
                path.parent.mkdir(exist_ok=True)
                path.write_text(f"{key} fixture\n", encoding="utf-8")
                artifacts[key] = {
                    "path": f"staging/{key}.md",
                    "sha256": self.control.sha256_file(path),
                    "disposition": "staging",
                }
            approvals = {}
            for gate, key in self.control.ARTIFACT_BY_GATE.items():
                approvals[gate] = {
                    "decision": "approved", "gate": gate, "approver": "reviewer-7",
                    "approval_ref": "https://code.example.invalid/reviews/42",
                    "reviewed_revision": "rev-42", "approved_at": "2030-01-01T00:00:00Z",
                    "authority_id": "fixture-authority", "verifier_config": str(verifier_config),
                    "artifact_path": artifacts[key]["path"],
                    "artifact_sha256": artifacts[key]["sha256"],
                }
            run = {
                "schema_version": 2, "workflow_id": "fixture", "run_id": "run-1",
                "stage": "publish_ready", "runtime": {"execution_mode": "interactive"},
                "source_policy": {
                    "path": "source-policy.json",
                    "sha256": self.control.sha256_file(source_policy),
                },
                "artifacts": artifacts,
                "approvals": approvals,
                "transition_history": [
                    {"from": self.control.STAGES[index], "to": self.control.STAGES[index + 1]}
                    for index in range(self.control.STAGES.index("publish_ready"))
                ],
            }
            self.control.write_run(repo, "state/runs/run.yaml", run)
            (repo / "staging/staging.md").write_text("changed after approval\n", encoding="utf-8")
            calls = []

            def runner(*args, **kwargs):
                calls.append(args)
                return subprocess.CompletedProcess(args[0], 0, "{}", "")

            with self.assertRaises(self.control.WorkflowControlError):
                self.publisher.publish_run(
                    root=repo, run_path="state/runs/run.yaml",
                    config_path=publisher_config,
                    operation="publish-approved-artifact", runner=runner,
                )
            self.assertEqual(calls, [])

    def test_control_plane_derives_verifier_and_enforces_stage_and_run_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            verifier_config = external / "verifier.json"
            source_policy = repo / ".agents/governance/source-policy.yaml"
            source_policy.parent.mkdir(parents=True)
            source_policy.write_text(
                json.dumps({
                    "schema_version": 1,
                    "policy_id": "fixture",
                    "status": "active",
                    "approval_authority": {
                        "authority_id": "fixture-authority",
                        "verifier_config": str(verifier_config),
                    },
                    "allowed_sources": [
                        {"id": "fixture", "adapter": "local", "description": "fixture"}
                    ],
                }),
                encoding="utf-8",
            )
            run = self.control.build_initial_run(
                root=repo,
                workflow_id="fixture",
                run_id="run-1",
                policy_path=".agents/governance/source-policy.yaml",
                execution_mode="interactive",
            )
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.write_run(repo, "run.yaml", run)
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.register_artifact(
                    run, root=repo, key="evidence", relative_path="staging/evidence.md"
                )

            run = self.control.transition(run, root=repo, target_stage="collection")
            evidence = repo / "staging/evidence.md"
            evidence.parent.mkdir()
            evidence.write_text("synthetic evidence\n", encoding="utf-8")
            run = self.control.register_artifact(
                run, root=repo, key="evidence", relative_path="staging/evidence.md"
            )
            run = self.control.transition(run, root=repo, target_stage="evidence_review")
            captured = {}

            def verified(**kwargs):
                captured.update(kwargs)
                request = kwargs["request"]
                return {
                    "decision": "approved",
                    "gate": request["gate"],
                    "approver": "reviewer-7",
                    "approval_ref": request["approval_ref"],
                    "reviewed_revision": request["reviewed_revision"],
                    "artifact_path": request["artifact_path"],
                    "artifact_sha256": request["artifact_sha256"],
                    "approved_at": "2030-01-01T00:00:00Z",
                    "authority_id": "fixture-authority",
                    "verifier_config": str(verifier_config),
                }

            def wrong_authority(**kwargs):
                response = verified(**kwargs)
                response["authority_id"] = "untrusted-authority"
                return response

            with mock.patch.object(
                self.control, "verify_approval", side_effect=wrong_authority
            ):
                with self.assertRaises(self.control.WorkflowControlError):
                    self.control.record_verified_approval(
                        run,
                        root=repo,
                        gate="evidence",
                        approval_ref="https://code.example.invalid/reviews/42",
                        reviewed_revision="rev-42",
                    )

            with mock.patch.object(self.control, "verify_approval", side_effect=verified):
                run = self.control.record_verified_approval(
                    run,
                    root=repo,
                    gate="evidence",
                    approval_ref="https://code.example.invalid/reviews/42",
                    reviewed_revision="rev-42",
                )
            self.assertEqual(captured["config_path"], verifier_config)
            claims = repo / "staging/claims.md"
            claims.write_text("synthetic claims\n", encoding="utf-8")
            run = self.control.register_artifact(
                run, root=repo, key="claims", relative_path="staging/claims.md"
            )
            run = self.control.transition(run, root=repo, target_stage="claims_review")
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.register_artifact(
                    run,
                    root=repo,
                    key="evidence",
                    relative_path="staging/evidence.md",
                )

            tampered = dict(run)
            tampered["transition_history"] = []
            with self.assertRaises(self.control.WorkflowControlError):
                self.control.validate_run(tampered, repo)

    def test_publisher_requires_a_response_bound_to_the_exact_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            verifier_config = external / "verifier.json"
            source_policy = repo / ".agents/governance/source-policy.yaml"
            source_policy.parent.mkdir(parents=True)
            source_policy.write_text(
                json.dumps({
                    "schema_version": 1,
                    "policy_id": "fixture",
                    "status": "active",
                    "approval_authority": {
                        "authority_id": "fixture-authority",
                        "verifier_config": str(verifier_config),
                    },
                    "allowed_sources": [
                        {"id": "fixture", "adapter": "local", "description": "fixture"}
                    ],
                }),
                encoding="utf-8",
            )
            artifacts = {}
            for key in ("evidence", "claims", "framing", "copy", "staging"):
                artifact = repo / f"staging/{key}.md"
                artifact.parent.mkdir(exist_ok=True)
                artifact.write_text(f"{key} fixture\n", encoding="utf-8")
                artifacts[key] = {
                    "path": f"staging/{key}.md",
                    "sha256": self.control.sha256_file(artifact),
                    "disposition": "staging",
                }
            approvals = {
                gate: {
                    "decision": "approved",
                    "gate": gate,
                    "approver": "reviewer-7",
                    "approval_ref": "https://code.example.invalid/reviews/42",
                    "reviewed_revision": "rev-42",
                    "approved_at": "2030-01-01T00:00:00Z",
                    "authority_id": "fixture-authority",
                    "verifier_config": str(verifier_config),
                    "artifact_path": artifacts[key]["path"],
                    "artifact_sha256": artifacts[key]["sha256"],
                }
                for gate, key in self.control.ARTIFACT_BY_GATE.items()
            }
            run = {
                "schema_version": 2,
                "workflow_id": "fixture",
                "run_id": "run-1",
                "stage": "publish_ready",
                "runtime": {"execution_mode": "interactive"},
                "source_policy": {
                    "path": ".agents/governance/source-policy.yaml",
                    "sha256": self.control.sha256_file(source_policy),
                },
                "artifacts": artifacts,
                "approvals": approvals,
                "transition_history": [
                    {"from": self.control.STAGES[index], "to": self.control.STAGES[index + 1]}
                    for index in range(self.control.STAGES.index("publish_ready"))
                ],
            }
            run_path = "state/runs/run.yaml"
            self.control.write_run(repo, run_path, run)
            publisher_executable = external / "publish"
            publisher_executable.write_text("fixture\n", encoding="utf-8")
            publisher_config = external / "publisher.json"
            publisher_config.write_text(
                json.dumps({
                    "schema_version": 1,
                    "adapter_id": "fixture-publisher",
                    "enabled": True,
                    "approved": True,
                    "command": [str(publisher_executable)],
                    "allowed_operations": ["publish-approved-artifact"],
                    "timeout_seconds": 5,
                }),
                encoding="utf-8",
            )
            verified = approvals["publish"]

            def response_for(request, *, digest):
                return {
                    "published": True,
                    "run_id": request["run_id"],
                    "operation": request["operation"],
                    "artifact_path": request["artifact_path"],
                    "artifact_sha256": digest,
                    "approval_ref": request["approval_ref"],
                    "receipt_id": "receipt-42",
                    "published_at": "2030-01-01T00:00:00Z",
                }

            def mismatched_runner(*args, **kwargs):
                request = json.loads(kwargs["input"])
                response = response_for(request, digest="f" * 64)
                return subprocess.CompletedProcess(args[0], 0, json.dumps(response), "")

            with mock.patch.object(
                self.publisher, "assert_publish_authorized", return_value=verified
            ):
                with self.assertRaises(self.publisher.PublisherError):
                    self.publisher.publish_run(
                        root=repo,
                        run_path=run_path,
                        config_path=publisher_config,
                        operation="publish-approved-artifact",
                        runner=mismatched_runner,
                    )
            self.assertEqual(self.control.load_run(repo, run_path)[1]["stage"], "publish_ready")

            def matched_runner(*args, **kwargs):
                request = json.loads(kwargs["input"])
                response = response_for(request, digest=request["artifact_sha256"])
                return subprocess.CompletedProcess(args[0], 0, json.dumps(response), "")

            with mock.patch.object(
                self.publisher, "assert_publish_authorized", return_value=verified
            ):
                receipt = self.publisher.publish_run(
                    root=repo,
                    run_path=run_path,
                    config_path=publisher_config,
                    operation="publish-approved-artifact",
                    runner=matched_runner,
                )
            self.assertEqual(receipt["receipt_id"], "receipt-42")
            self.assertEqual(self.control.load_run(repo, run_path)[1]["stage"], "published")

    def test_skill_initializer_never_overwrites_a_conflict(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.assertEqual(
                run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])[0],
                0,
            )
            target = repo / ".agents/governance/standards/STD-skill-structure-v1.0.md"
            target.write_text("local policy\n", encoding="utf-8")
            status, output, error = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 2)
            self.assertIn("conflict:", output)
            self.assertIn("not overwritten", error)
            self.assertEqual(target.read_text(encoding="utf-8"), "local policy\n")

    def test_initializers_refuse_paths_that_escape_through_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            external = root / "external"
            repo.mkdir()
            external.mkdir()
            (repo / ".agents").symlink_to(external, target_is_directory=True)
            skill_status, _, _ = run_main(
                self.skills, ["initialize", "--repo", str(repo), "--apply"]
            )
            tracker_status, _, _ = run_main(
                self.tracker, ["initialize", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(skill_status, 2)
            self.assertEqual(tracker_status, 2)
            self.assertEqual(list(external.iterdir()), [])
            self.assertFalse((repo / "state").exists())

    def test_skill_fix_adds_only_missing_interface_and_draft_registry_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])
            skill = repo / ".agents/skills/example-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: example-skill\ndescription: Example governed skill.\n---\n\n"
                "# Example Skill\n",
                encoding="utf-8",
            )
            status, output, _ = run_main(
                self.skills, ["fix", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("agents/openai.yaml", output)
            self.assertFalse((skill / "agents/openai.yaml").exists())

            status, _, _ = run_main(
                self.skills, ["fix", "--repo", str(repo), "--apply"]
            )
            self.assertEqual(status, 0)
            registry = json.loads(
                (repo / ".agents/governance/skill-registry.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(registry["skills"][0]["status"], "draft")
            self.assertEqual(registry["skills"][0]["owner"], "unassigned")
            self.assertEqual(self.skills.audit(repo), [])

    def test_ci_is_installed_only_when_explicitly_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            first.mkdir()
            second.mkdir()
            run_main(self.skills, ["initialize", "--repo", str(first), "--apply"])
            run_main(
                self.skills,
                ["initialize", "--repo", str(second), "--with-ci", "--apply"],
            )
            self.assertFalse((first / ".github/workflows/skill-governance.yml").exists())
            workflow = second / ".github/workflows/skill-governance.yml"
            self.assertTrue(workflow.is_file())
            self.assertEqual(
                run_main(self.skills, ["initialize", "--repo", str(second), "--apply"])[0],
                0,
            )
            self.assertTrue(workflow.is_file())
            workflow.unlink()
            self.assertEqual(
                run_main(self.skills, ["fix", "--repo", str(second), "--apply"])[0],
                0,
            )
            self.assertTrue(workflow.is_file())

    def test_tracker_initializer_merges_manifest_and_validates_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            run_main(self.skills, ["initialize", "--repo", str(repo), "--apply"])
            status, output, _ = run_main(
                self.tracker, ["initialize", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("state/work/roadmaps/.gitkeep", output)
            self.assertFalse((repo / "state/work").exists())

            self.assertEqual(
                run_main(self.tracker, ["initialize", "--repo", str(repo), "--apply"])[0],
                0,
            )
            manifest = json.loads(
                (repo / ".agents/governance/manifest.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(set(manifest["components"]), {"skills", "work-tracker"})
            self.assertEqual(self.tracker.audit(repo), [])

            templates = (
                ROOT / "plugins/skill-governance/skills/govern-work-tracker/assets/templates"
            )
            for kind, name in (
                ("roadmaps", "roadmap"),
                ("epics", "epic"),
                ("tasks", "task"),
            ):
                record = json.loads((templates / f"{name}.yaml").read_text(encoding="utf-8"))
                (repo / "state/work" / kind / f"{record['id']}.yaml").write_text(
                    json.dumps(record, indent=2) + "\n", encoding="utf-8"
                )
            self.assertEqual(self.tracker.audit(repo), [])

            task_path = repo / "state/work/tasks/synthesize-onboarding-interviews.yaml"
            task = json.loads(task_path.read_text(encoding="utf-8"))
            task["status"] = "done"
            task_path.write_text(json.dumps(task, indent=2) + "\n", encoding="utf-8")
            findings = self.tracker.audit(repo)
            self.assertTrue(any(item.id == "TRACKER017" for item in findings))

    def test_tracker_audit_is_advisory_and_fix_restores_missing_managed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            status, _, _ = run_main(self.tracker, ["audit", "--repo", str(repo)])
            self.assertEqual(status, 0)
            status, _, _ = run_main(
                self.tracker, ["audit", "--repo", str(repo), "--strict"]
            )
            self.assertEqual(status, 1)
            run_main(self.tracker, ["initialize", "--repo", str(repo), "--apply"])
            target = repo / ".agents/governance/schemas/task.schema.json"
            target.unlink()
            status, output, _ = run_main(
                self.tracker, ["fix", "--repo", str(repo), "--dry-run"]
            )
            self.assertEqual(status, 0)
            self.assertIn("task.schema.json", output)
            self.assertFalse(target.exists())
            self.assertEqual(
                run_main(self.tracker, ["fix", "--repo", str(repo), "--apply"])[0],
                0,
            )
            self.assertTrue(target.is_file())
            self.assertEqual(self.tracker.audit(repo), [])


if __name__ == "__main__":
    unittest.main()
