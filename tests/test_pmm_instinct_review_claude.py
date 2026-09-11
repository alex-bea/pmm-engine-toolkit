import difflib
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from contextlib import redirect_stderr, redirect_stdout


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "plugins" / "pmm-instinct-review"
SCRIPTS = BUNDLE / "scripts"
sys.path.insert(0, str(SCRIPTS))

import pmm_instinct_claude as runtime  # noqa: E402
import claude_instinct_hook as hook  # noqa: E402
import claude_instinct_review as review_cli  # noqa: E402
import claude_instinct_worker as worker  # noqa: E402
import install_claude_instinct_review as installer  # noqa: E402


class FakeRunner:
    def __init__(self, payload=None, returncode=0, stderr="private error text"):
        self.payload = payload or {"candidates": []}
        self.returncode = returncode
        self.stderr = stderr
        self.calls = []

    def __call__(self, command, **kwargs):
        self.calls.append((command, kwargs))
        stdout = json.dumps({"structured_output": self.payload})
        return SimpleNamespace(returncode=self.returncode, stdout=stdout, stderr=self.stderr)


class FakeLauncher:
    def __init__(self):
        self.calls = []

    def __call__(self, command, **kwargs):
        self.calls.append((command, kwargs))
        return object()


class PublicClaudeRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))
        self.paths = runtime.resolve_paths(self.tmp / "state")

    def _transcript(self, session_id="session-one", prefix="prompt"):
        path = self.tmp / f"{session_id}.jsonl"
        records = []
        for index in range(5):
            records.extend(
                [
                    {
                        "type": "user",
                        "sessionId": session_id,
                        "cwd": str(self.tmp / "repo"),
                        "timestamp": f"2026-09-10T12:00:{index * 2:02d}Z",
                        "message": {"role": "user", "content": f"{prefix} {index}"},
                    },
                    {
                        "type": "assistant",
                        "sessionId": session_id,
                        "cwd": str(self.tmp / "repo"),
                        "timestamp": f"2026-09-10T12:00:{index * 2 + 1:02d}Z",
                        "message": {
                            "role": "assistant",
                            "content": [
                                {"type": "text", "text": f"answer {index}"},
                                {"type": "tool_use", "name": "Read", "input": {"file": "secret"}},
                            ],
                        },
                    },
                ]
            )
        path.write_text("".join(json.dumps(item) + "\n" for item in records), encoding="utf-8")
        return path

    def _enable(self):
        runtime.update_config(
            self.paths,
            enabled=True,
            privacy_acknowledged_at="2026-09-10T12:00:00+00:00",
            extractor_model="sonnet",
        )

    def _capture(self, session_id="session-one", prefix="prompt"):
        self._enable()
        return runtime.capture_session(
            self.paths,
            session_id=session_id,
            transcript_path=self._transcript(session_id, prefix),
        )

    def test_bundle_has_no_private_repository_launcher_dependency(self):
        for path in SCRIPTS.glob("*.py"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("PMM_ENGINE_REPO_ROOT", text, path.name)
            self.assertNotIn("scripts/utilities", text, path.name)
            self.assertNotIn("/Us" + "ers/", text, path.name)
        template = json.loads((BUNDLE / "assets" / "claude-config-template.json").read_text(encoding="utf-8"))
        self.assertEqual(template, runtime.DEFAULT_CONFIG)

    def test_public_manifests_and_native_hook_contract(self):
        claude_manifest = json.loads((BUNDLE / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        codex_manifest = json.loads((BUNDLE / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(claude_manifest["version"], "0.3.0")
        self.assertEqual(codex_manifest["version"], "0.3.0")
        self.assertEqual(claude_manifest["skills"], ["./skills/pmm-instinct-review"])
        self.assertEqual(claude_manifest["hooks"], "./hooks/claude-hooks.json")
        hook_contract = json.loads((BUNDLE / "hooks" / "claude-hooks.json").read_text(encoding="utf-8"))
        serialized = json.dumps(hook_contract)
        self.assertIn("SessionStart", hook_contract["hooks"])
        self.assertIn("SessionEnd", hook_contract["hooks"])
        handlers = [
            handler
            for entries in hook_contract["hooks"].values()
            for entry in entries
            for handler in entry["hooks"]
        ]
        self.assertTrue(all(handler["command"] == "python3" for handler in handlers))
        self.assertTrue(all(isinstance(handler.get("args"), list) for handler in handlers))
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/claude_instinct_hook.py", serialized)
        self.assertNotIn("/Us" + "ers/", serialized)
        self.assertNotIn("async", hook_contract["hooks"]["SessionStart"][0]["hooks"][0])
        self.assertIs(hook_contract["hooks"]["SessionEnd"][0]["hooks"][0]["async"], True)

    def test_fictional_claude_lifecycle_digests_and_relationships_are_exact(self):
        example = (
            BUNDLE
            / "skills"
            / "pmm-instinct-review"
            / "examples"
            / "fictional-northstar-reports"
            / "claude"
        )

        def load(name):
            return json.loads((example / name).read_text(encoding="utf-8"))

        config = load("config.json")
        evidence = load("evidence.json")
        queue = load("queue.json")
        installation = load("installation-receipt.json")
        decisions = load("review-decisions.json")
        preview = load("promotion-preview.json")
        receipt = load("promotion-receipt.json")
        outcome = load("promotion-outcome.json")
        status = load("status.json")

        self.assertEqual(installation["schema_version"], 2)
        self.assertEqual(
            installation["receipt_digest"],
            installer._receipt_digest(installation),
        )
        self.assertEqual(
            installation["owned_hook_handlers"],
            installer._hook_identities(
                Path(installation["active_root"]),
                Path(installation["state_root"]),
            ),
        )
        installer._validate_receipt(
            installation,
            claude_home=Path(installation["claude_home"]),
            state_root=Path(installation["state_root"]),
        )

        self.assertEqual(set(config), set(runtime.DEFAULT_CONFIG))
        self.assertTrue(config["enabled"])
        self.assertIsNotNone(config["privacy_acknowledged_at"])
        for key in (
            "schema_version",
            "min_user_messages",
            "max_turns",
            "max_normalized_chars",
            "max_attempts",
            "processing_lease_seconds",
            "extractor_model",
            "extractor_timeout_seconds",
        ):
            self.assertEqual(config[key], runtime.DEFAULT_CONFIG[key], key)

        self.assertEqual(evidence["runtime"], "claude")
        self.assertEqual(queue["runtime"], "claude")
        self.assertEqual(queue["session_id"], evidence["session_id"])
        self.assertEqual(queue["transcript_sha256"], evidence["transcript_sha256"])
        expected_job = runtime._job_id(evidence["session_id"], evidence["transcript_sha256"])
        self.assertEqual(queue["job_id"], expected_job)
        self.assertEqual(queue["state"], "completed")
        self.assertEqual(queue["candidate_count"], 1)
        self.assertEqual(queue["evidence_path"], f"{installation['state_root']}/sessions/{expected_job}-evidence.json")
        self.assertEqual(queue["result_path"], f"{installation['state_root']}/sessions/{expected_job}-suggestions.md")
        self.assertTrue(queue["audit_path"].endswith(f"-{expected_job}-audit.md"))
        self.assertEqual(queue["evidence_sha256"], runtime._sha256_file(example / "evidence.json"))
        self.assertEqual(queue["audit_sha256"], runtime._sha256_file(example / "audit.md"))
        self.assertEqual(queue["result_sha256"], runtime._sha256_file(example / "suggestions.md"))
        self.assertEqual(queue["manual_retries"], 0)

        audit = (example / "audit.md").read_text(encoding="utf-8")
        self.assertIn(expected_job, audit)
        self.assertIn(f"**normalized_transcript_path:** {queue['evidence_path']}", audit)
        self.assertIn(f"**suggestions_path:** {queue['result_path']}", audit)
        self.assertIn(f"**transcript_sha256:** {queue['transcript_sha256']}", audit)
        candidates = runtime._suggestion_candidates(
            {"suggestions_path": example / "suggestions.md", "queue_record": queue}
        )
        self.assertIsNotNone(candidates)
        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        expected_cluster = runtime._cluster_id(candidate["type"], candidate["rule"])
        self.assertEqual(decisions["schema_version"], 2)
        self.assertEqual(set(decisions["cluster_decisions"]), {expected_cluster})
        self.assertEqual(decisions["zero_resolutions"], [])
        decision = decisions["cluster_decisions"][expected_cluster][0]
        self.assertEqual(decision["decision"], "accept")
        occurrences = decision["occurrences"]
        current_occurrence = next(
            item for item in occurrences if item["session_id"] == evidence["session_id"]
        )
        self.assertEqual(current_occurrence["job_id"], queue["job_id"])
        self.assertEqual(current_occurrence["transcript_sha256"], queue["transcript_sha256"])
        self.assertEqual(current_occurrence["result_sha256"], queue["result_sha256"])
        pre_review_audit = audit.replace("processed: true", "processed: false", 1)
        self.assertEqual(current_occurrence["audit_sha256"], runtime.sha256_text(pre_review_audit))
        for occurrence in occurrences:
            self.assertEqual(
                occurrence["job_id"],
                runtime._job_id(occurrence["session_id"], occurrence["transcript_sha256"]),
            )

        instinct_metadata, instinct_body = runtime._parse_frontmatter(
            (example / "instinct.md").read_text(encoding="utf-8")
        )
        instinct_rule, instinct_rationale = runtime._rule_and_rationale(instinct_body)
        self.assertEqual(instinct_metadata["id"], Path(decision["instinct_path"]).stem)
        self.assertEqual(instinct_metadata["type"], candidate["type"])
        self.assertEqual(instinct_rule, candidate["rule"])
        self.assertEqual(instinct_rationale, candidate["why_it_matters"])
        self.assertEqual(
            preview["source_guidance_sha256"],
            runtime._canonical_digest(
                {"rule": instinct_rule, "why_it_matters": instinct_rationale}
            ),
        )
        self.assertEqual(instinct_metadata["seen_count"], len(occurrences))
        self.assertEqual(
            instinct_metadata["confidence"],
            runtime._confidence(len(occurrences)),
        )

        before = (example / "CLAUDE-before.md").read_text(encoding="utf-8")
        after = (example / "CLAUDE-after.md").read_text(encoding="utf-8")
        self.assertEqual(preview["target_sha256"], runtime.sha256_text(before))
        self.assertEqual(preview["resulting_sha256"], runtime.sha256_text(after))
        self.assertEqual(preview["resulting_text"], after)
        self.assertEqual(runtime._render_guidance_update(before, preview["insertion"]), after)
        preview_action = {
            key: value
            for key, value in preview.items()
            if key not in {"preview_digest", "confirmation_required"}
        }
        self.assertEqual(runtime._canonical_digest(preview_action), preview["preview_digest"])
        self.assertEqual(receipt["preview_digest"], preview["preview_digest"])
        self.assertEqual(receipt["approved_action"], preview_action)
        receipt_payload = {key: value for key, value in receipt.items() if key != "receipt_digest"}
        self.assertEqual(runtime._canonical_digest(receipt_payload), receipt["receipt_digest"])
        self.assertEqual(outcome["receipt_digest"], receipt["receipt_digest"])
        self.assertEqual(outcome["target_path"], preview["target_path"])
        self.assertEqual(outcome["resulting_sha256"], preview["resulting_sha256"])
        self.assertEqual(status["state_root"], installation["state_root"])
        self.assertEqual(status["queue"]["completed"], 1)
        self.assertEqual(status["promotion"][outcome["status"]], 1)

        governed_before = "# Fictional release summary workflow\n\n- Use only approved launch evidence.\n"
        governed_after = runtime._render_guidance_update(governed_before, preview["insertion"])
        governed_target = "/fictional/northstar-reports/skills/release-summary/references/RUN-workflow.md"
        expected_patch = "".join(
            difflib.unified_diff(
                governed_before.splitlines(keepends=True),
                governed_after.splitlines(keepends=True),
                fromfile=governed_target,
                tofile=governed_target,
                n=0,
            )
        )
        self.assertEqual(
            (example / "governed-changeset.patch").read_text(encoding="utf-8"),
            expected_patch,
        )

    def test_state_root_is_explicit_and_capture_is_private_by_default(self):
        with self.assertRaises(ValueError):
            runtime.resolve_paths()
        runtime.ensure_store(self.paths)
        transcript = self._transcript()
        result = runtime.capture_session(self.paths, session_id="session-one", transcript_path=transcript)
        self.assertEqual(result["reason"], "disabled")
        self.assertFalse(runtime.load_config(self.paths)["enabled"])

    def test_legacy_claude_store_and_descendants_are_rejected(self):
        fake_home = self.tmp / "fake-home"
        fake_home.mkdir()
        legacy = fake_home / ".claude" / "instinct-review"
        with mock.patch.object(runtime.Path, "home", return_value=fake_home):
            for candidate in (legacy, legacy / "nested" / "runtime"):
                with self.subTest(candidate=candidate):
                    with self.assertRaisesRegex(ValueError, "legacy Claude review store"):
                        runtime.resolve_paths(candidate)
                    self.assertFalse(candidate.exists())

    def test_malformed_config_and_non_dedicated_state_root_fail_closed(self):
        runtime.ensure_store(self.paths)
        malformed = dict(runtime.DEFAULT_CONFIG)
        malformed.update(enabled="false", privacy_acknowledged_at="false")
        runtime.atomic_write_json(self.paths.config, malformed)
        with self.assertRaisesRegex(ValueError, "enabled must be true or false"):
            runtime.capture_session(
                self.paths,
                session_id="session-one",
                transcript_path=self._transcript(),
            )
        self.assertEqual(list(self.paths.queue.glob("*.json")), [])

        unrelated = self.tmp / "unrelated"
        unrelated.mkdir()
        marker = unrelated / "README.md"
        marker.write_text("keep\n", encoding="utf-8")
        original_mode = unrelated.stat().st_mode & 0o777
        with self.assertRaisesRegex(ValueError, "not a dedicated"):
            runtime.ensure_store(runtime.resolve_paths(unrelated))
        self.assertEqual(unrelated.stat().st_mode & 0o777, original_mode)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")
        with self.assertRaisesRegex(ValueError, "outside the installed bundle"):
            runtime.resolve_paths(BUNDLE / "runtime-state")

        external_config = self.tmp / "external-config.json"
        external_config.write_text(json.dumps(runtime.DEFAULT_CONFIG), encoding="utf-8")
        linked_root = self.tmp / "linked-config-state"
        linked_root.mkdir()
        (linked_root / "config.json").symlink_to(external_config)
        with self.assertRaisesRegex(ValueError, "config must be a regular file"):
            runtime.load_config(runtime.resolve_paths(linked_root))

        outside = self.tmp / "outside-previews"
        outside.mkdir()
        preview_root = self.tmp / "linked-preview-state"
        (preview_root / "state").mkdir(parents=True)
        (preview_root / "state" / "promotion-previews").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "state directory must be a regular directory"):
            runtime.ensure_store(runtime.resolve_paths(preview_root))
        self.assertEqual(list(outside.iterdir()), [])

    def test_atomic_write_ignores_a_preplanted_predictable_temp_symlink(self):
        destination = self.tmp / "shared" / "CLAUDE.md"
        destination.parent.mkdir()
        victim = self.tmp / "victim.md"
        victim.write_text("untouched\n", encoding="utf-8")
        predictable = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
        predictable.symlink_to(victim)
        runtime.atomic_write_text(destination, "approved\n")
        self.assertEqual(destination.read_text(encoding="utf-8"), "approved\n")
        self.assertEqual(victim.read_text(encoding="utf-8"), "untouched\n")
        self.assertTrue(predictable.is_symlink())

    def test_write_log_rejects_a_preplanted_log_symlink_without_touching_victim(self):
        runtime.ensure_store(self.paths)
        victim = self.tmp / "victim.log"
        victim.write_text("untouched\n", encoding="utf-8")
        victim.chmod(0o640)
        before = victim.read_bytes()
        before_mode = victim.stat().st_mode & 0o777
        log_path = self.paths.logs / "session-one.log"
        log_path.symlink_to(victim)

        with self.assertRaises(OSError):
            runtime.write_log(self.paths, "session-one", "state=queued")

        self.assertTrue(log_path.is_symlink())
        self.assertEqual(victim.read_bytes(), before)
        self.assertEqual(victim.stat().st_mode & 0o777, before_mode)

    def test_normalizer_strips_mixed_and_unclosed_native_context_wrappers(self):
        transcript = self.tmp / "mixed-context.jsonl"
        messages = (
            "keep prefix <system-reminder>SENSITIVE_SENTINEL</system-reminder> keep suffix",
            "keep assistant <task-notification>PRIVATE_STATUS</task-notification> text",
            "keep before <teammate-message>UNFINISHED_PRIVATE_CONTEXT",
        )
        records = [
            {
                "type": "user" if index != 1 else "assistant",
                "sessionId": "mixed-context",
                "cwd": str(self.tmp / "repo"),
                "timestamp": f"2026-09-10T12:00:0{index}Z",
                "message": {
                    "role": "user" if index != 1 else "assistant",
                    "content": value,
                },
            }
            for index, value in enumerate(messages)
        ]
        transcript.write_text(
            "".join(json.dumps(item) + "\n" for item in records),
            encoding="utf-8",
        )
        normalized = runtime.normalize_transcript(transcript)
        combined = "\n".join(turn.text for turn in normalized.turns)
        self.assertIn("keep prefix  keep suffix", combined)
        self.assertIn("keep assistant  text", combined)
        self.assertIn("keep before", combined)
        self.assertNotIn("SENSITIVE_SENTINEL", combined)
        self.assertNotIn("PRIVATE_STATUS", combined)
        self.assertNotIn("UNFINISHED_PRIVATE_CONTEXT", combined)

    def test_top_level_custom_agent_is_eligible_but_subagent_is_not(self):
        self._enable()
        transcript = self._transcript("custom-agent-session")
        queued = runtime.queue_capture_request(
            self.paths,
            {
                "session_id": "custom-agent-session",
                "transcript_path": str(transcript),
                "agent_type": "release-reviewer",
            },
        )
        self.assertEqual(queued["status"], "queued")
        self.assertEqual(runtime.drain_capture_requests(self.paths)["queued"], 1)
        skipped = runtime.queue_capture_request(
            self.paths,
            {
                "session_id": "subagent-session",
                "transcript_path": str(self._transcript("subagent-session")),
                "agent_id": "agent-123",
                "agent_type": "release-reviewer",
            },
        )
        self.assertEqual(skipped["reason"], "subagent")

    def test_plugin_data_precedes_standalone_environment_state(self):
        explicit = self.tmp / "explicit-state"
        plugin_data = self.tmp / "plugin-data"
        standalone = self.tmp / "standalone-state"
        with mock.patch.dict(
            runtime.os.environ,
            {
                "CLAUDE_PLUGIN_DATA": str(plugin_data),
                "PMM_INSTINCT_STATE_ROOT": str(standalone),
            },
        ):
            self.assertEqual(
                runtime.resolve_state_root(),
                (plugin_data / "instinct-review").resolve(),
            )
            self.assertEqual(runtime.resolve_state_root(explicit), explicit.resolve())

    def test_normalizer_excludes_native_meta_wrappers_and_digests_full_input(self):
        transcript = self.tmp / "native-context.jsonl"

        def record(text, *, role="user", **metadata):
            return {
                "type": role,
                "sessionId": "native-context",
                "cwd": str(self.tmp / "repo"),
                "timestamp": "2026-09-10T12:00:00Z",
                "message": {"role": role, "content": text},
                **metadata,
            }

        records = [
            record("kept 0"),
            record("kept 1", role="assistant"),
            record("<system-reminder>internal context</system-reminder>"),
            record("kept 2"),
            record("<task-notification>background status</task-notification>"),
            record("<teammate-notification>agent status</teammate-notification>"),
            record("kept 3", role="assistant"),
            record("kept 4"),
            record("hidden camel metadata", isMeta=True),
            record("hidden snake metadata", is_meta=True),
        ]
        transcript.write_text(
            "".join(json.dumps(item) + "\n" for item in records),
            encoding="utf-8",
        )

        normalized = runtime.normalize_transcript(
            transcript,
            max_turns=3,
            max_chars=1000,
        )

        self.assertEqual(
            [turn.text for turn in normalized.turns],
            ["kept 2", "kept 3", "kept 4"],
        )
        self.assertEqual(normalized.transcript_sha256, runtime._sha256_file(transcript))

    def test_capture_enforces_minimum_after_turn_and_character_limits(self):
        self._enable()
        runtime.update_config(self.paths, max_turns=4, min_user_messages=5)
        turn_limited = runtime.capture_session(
            self.paths,
            session_id="session-one",
            transcript_path=self._transcript(),
        )
        self.assertEqual(turn_limited["reason"], "below-minimum-user-messages")
        runtime.update_config(self.paths, max_turns=200, max_normalized_chars=12)
        character_limited = runtime.capture_session(
            self.paths,
            session_id="session-two",
            transcript_path=self._transcript("session-two"),
        )
        self.assertEqual(character_limited["reason"], "below-minimum-user-messages")
        self.assertEqual(runtime.queue_counts(self.paths)["queued"], 0)

    def test_capture_is_redacted_bounded_and_idempotent(self):
        self._enable()
        transcript = self._transcript(prefix="export SERVICE_API_" + "KEY=supersecret")
        first = runtime.capture_session(self.paths, session_id="session-one", transcript_path=transcript)
        second = runtime.capture_session(self.paths, session_id="session-one", transcript_path=transcript)
        self.assertEqual(first["status"], "queued")
        self.assertEqual(second["status"], "exists")
        evidence = json.loads(Path(first["evidence_path"]).read_text(encoding="utf-8"))
        serialized = json.dumps(evidence)
        self.assertIn("[REDACTED]", serialized)
        self.assertNotIn("supersecret", serialized)
        self.assertNotIn("tool_use", serialized)
        self.assertEqual(runtime.queue_counts(self.paths)["queued"], 1)

    def test_session_end_spools_only_metadata_before_detached_capture(self):
        self._enable()
        transcript = self._transcript(prefix="private conversation text")
        payload = {
            "session_id": "session-one",
            "transcript_path": str(transcript),
            "cwd": str(self.tmp / "repo"),
        }
        with (
            mock.patch.object(runtime, "normalize_transcript", side_effect=AssertionError("hook parsed transcript")),
            mock.patch.object(hook, "start_detached_worker", return_value=True),
        ):
            self.assertEqual(hook.session_end(payload, state_root=self.paths.state_root), 0)
        requests = list(self.paths.capture_inbox.glob("*.json"))
        self.assertEqual(len(requests), 1)
        serialized = requests[0].read_text(encoding="utf-8")
        self.assertNotIn("private conversation text", serialized)
        drained = runtime.drain_capture_requests(self.paths)
        self.assertEqual(drained, {"status": "complete", "processed": 1, "queued": 1, "skipped": 0, "failed": 0})
        self.assertEqual(list(self.paths.capture_inbox.glob("*.json")), [])
        self.assertEqual(runtime.queue_counts(self.paths)["queued"], 1)

    def test_capture_request_repairs_corruption_and_long_ids_remain_authoritative(self):
        self._enable()
        session_id = "session-" + "x" * 180
        transcript = self._transcript(session_id=session_id)
        payload = {"session_id": session_id, "transcript_path": str(transcript), "cwd": str(self.tmp)}
        first = runtime.queue_capture_request(self.paths, payload)
        Path(first["request_path"]).write_text("{}", encoding="utf-8")
        repaired = runtime.queue_capture_request(self.paths, payload)
        self.assertEqual(repaired["status"], "queued")
        self.assertEqual(runtime.drain_capture_requests(self.paths)["queued"], 1)
        records = runtime.read_queue(self.paths)
        self.assertEqual(len(records), 1)
        self.assertLessEqual(len(records[0][1]["job_id"]), 100)

    def test_corrupt_existing_queue_retains_capture_request_for_recovery(self):
        self._enable()
        transcript = self._transcript()
        normalized = runtime.normalize_transcript(transcript)
        runtime.ensure_store(self.paths)
        job_id = runtime._job_id("session-one", normalized.transcript_sha256)
        (self.paths.queue / f"{job_id}.json").write_text("{}", encoding="utf-8")
        runtime.queue_capture_request(
            self.paths,
            {"session_id": "session-one", "transcript_path": str(transcript), "cwd": str(self.tmp)},
        )
        result = runtime.drain_capture_requests(self.paths)
        self.assertEqual(result["failed"], 1)
        pending = list(self.paths.capture_inbox.glob("*.json"))
        self.assertEqual(len(pending), 1)
        self.assertEqual(json.loads(pending[0].read_text(encoding="utf-8"))["attempts"], 1)
        self.assertEqual(runtime.queue_counts(self.paths)["queued"], 0)

    def test_duplicate_capture_rebuilds_damaged_derived_artifacts_from_spool(self):
        for session_id, artifact_key in (
            ("missing-evidence-session", "evidence_path"),
            ("tampered-audit-session", "audit_path"),
        ):
            with self.subTest(artifact=artifact_key):
                captured = self._capture(session_id)
                artifact = Path(captured[artifact_key])
                if artifact_key == "evidence_path":
                    artifact.unlink()
                else:
                    artifact.write_text(artifact.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
                transcript = self._transcript(session_id)
                runtime.queue_capture_request(
                    self.paths,
                    {"session_id": session_id, "transcript_path": str(transcript), "cwd": str(self.tmp)},
                )
                result = runtime.drain_capture_requests(self.paths)
                self.assertEqual(result["queued"], 1)
                self.assertEqual(result["failed"], 0)
                queue_path = Path(captured["queue_path"])
                record = json.loads(queue_path.read_text(encoding="utf-8"))
                self.assertEqual(runtime._sha256_file(Path(record["evidence_path"])), record["evidence_sha256"])
                self.assertEqual(runtime._sha256_file(Path(record["audit_path"])), record["audit_sha256"])
                self.assertEqual(list(self.paths.capture_inbox.glob("*.json")), [])

    def test_background_extractor_is_toolless_ephemeral_and_schema_checked(self):
        captured = self._capture(prefix="Use $pmm-instinct-review and keep the summary short")
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep the summary short",
                    "context": "The user corrected the preferred response length.",
                    "why_it_matters": "Long summaries make the requested output harder to scan.",
                }
            ]
        }
        runner = FakeRunner(payload)
        result = runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=runner,
        )
        self.assertEqual(result["completed"], 1)
        command, kwargs = runner.calls[0]
        for flag in (
            "--bare",
            "--json-schema",
            "--no-session-persistence",
            "--tools",
            "--disallowedTools",
        ):
            self.assertIn(flag, command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertEqual(command[command.index("--disallowedTools") + 1], "mcp__*")
        self.assertNotIn("Valid installed skill slugs", " ".join(command))
        self.assertEqual(kwargs["env"]["PMM_INSTINCT_EXTRACTOR"], "1")
        self.assertNotIn("supersecret", kwargs["input"])
        queue = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(queue["state"], "completed")
        suggestions = Path(queue["result_path"]).read_text(encoding="utf-8")
        self.assertIn("**source_runtime:** claude", suggestions)
        self.assertIn("Keep summaries short.", suggestions)

    def test_failed_extraction_is_retryable_then_terminal(self):
        captured = self._capture()
        runner = FakeRunner(returncode=1)
        for expected in ("retryable", "retryable", "failed"):
            runtime.drain_extraction_queue(
                self.paths,
                claude_binary=sys.executable,
                root=BUNDLE,
                runner=runner,
            )
            record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
            self.assertEqual(record["state"], expected)
        self.assertEqual(runtime.retry_failed(self.paths), 1)
        record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(record["state"], "retryable")
        self.assertEqual(record["attempts"], 0)

    def test_retry_failed_rejects_an_externally_symlinked_queue_directory(self):
        runtime.ensure_store(self.paths)
        external_queue = self.tmp / "external-queue"
        external_queue.mkdir()
        marker = external_queue / "failed.json"
        marker.write_text('{"state":"failed"}\n', encoding="utf-8")
        before = marker.read_bytes()
        self.paths.queue.rmdir()
        self.paths.queue.symlink_to(external_queue, target_is_directory=True)

        with self.assertRaisesRegex(ValueError, "runtime state directory must be a regular directory"):
            runtime.retry_failed(self.paths)

        self.assertTrue(self.paths.queue.is_symlink())
        self.assertEqual(marker.read_bytes(), before)

    def test_authentication_failure_is_clear_without_persisting_provider_output(self):
        captured = self._capture()
        runner = FakeRunner(
            returncode=1,
            stderr="authentication failed: tok" + "en=supersecret",
        )
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=runner,
        )
        record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
        self.assertIn("authentication failed in --bare mode", record["last_error"])
        self.assertIn("ANTHROPIC_API_KEY", record["last_error"])
        self.assertIn("Bedrock, Vertex, or Foundry", record["last_error"])
        self.assertNotIn("apiKeyHelper", record["last_error"])
        self.assertNotIn("supersecret", record["last_error"])

    def test_review_creates_an_instinct_only_after_confirmation(self):
        self._capture(prefix="Use $pmm-instinct-review and keep summaries short")
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep summaries short",
                    "context": "The user corrected response length.",
                    "why_it_matters": "Long summaries are harder to scan.",
                }
            ]
        }
        runtime.drain_extraction_queue(self.paths, claude_binary=sys.executable, root=BUNDLE, runner=FakeRunner(payload))
        cluster = runtime.review_backlog(self.paths)["clusters"][0]
        self.assertEqual(cluster["exact_match_state"], "new")
        with self.assertRaises(PermissionError):
            runtime.review_cluster(self.paths, cluster["cluster_id"], "accept")
        result = runtime.review_cluster(self.paths, cluster["cluster_id"], "accept", confirm=True)
        self.assertTrue(Path(result["instinct_path"]).is_file())
        self.assertEqual(runtime.review_backlog(self.paths)["positive_clusters"], 0)
        self.assertEqual(runtime.review_ready_count(self.paths), 0)
        self.assertFalse(next(self.paths.sessions.glob("*-evidence.json"), None))

    def test_review_reconciliation_finishes_cleanup_after_ledger_write_crash(self):
        captured = self._capture(prefix="keep summaries short")
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep summaries short",
                    "context": "The user corrected response length.",
                    "why_it_matters": "Long summaries are harder to scan.",
                }
            ]
        }
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(payload),
        )
        cluster = runtime.review_backlog(self.paths)["clusters"][0]
        evidence_path = Path(captured["evidence_path"])
        audit_path = Path(captured["audit_path"])

        with (
            mock.patch.object(runtime, "_resolve_completed_audits", side_effect=OSError("simulated crash")),
            self.assertRaisesRegex(OSError, "simulated crash"),
        ):
            runtime.review_cluster(self.paths, cluster["cluster_id"], "reject", confirm=True)

        ledger = json.loads((self.paths.state / "review-decisions.json").read_text(encoding="utf-8"))
        decision = ledger["cluster_decisions"][cluster["cluster_id"]][0]
        self.assertEqual(ledger["schema_version"], 2)
        self.assertEqual(decision["decision"], "reject")
        self.assertEqual(decision["occurrences"], cluster["occurrences"])
        self.assertTrue(evidence_path.is_file())
        self.assertNotIn("processed: true", audit_path.read_text(encoding="utf-8"))

        result = runtime.reconcile_review_finalizations(self.paths)

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["finalized"], 1)
        self.assertFalse(evidence_path.exists())
        self.assertIn("processed: true", audit_path.read_text(encoding="utf-8"))
        queue = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(queue["audit_sha256"], runtime._sha256_file(audit_path))
        self.assertEqual(runtime.review_ready_count(self.paths), 0)

    def test_review_decision_is_bound_to_job_result_and_audit_not_reused_session_id(self):
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep summaries short",
                    "context": "The user corrected response length.",
                    "why_it_matters": "Long summaries are harder to scan.",
                }
            ]
        }
        first = self._capture("resumed-session", "first transcript keep summaries short")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(payload),
        )
        first_cluster = runtime.review_backlog(self.paths)["clusters"][0]
        runtime.review_cluster(self.paths, first_cluster["cluster_id"], "reject", confirm=True)
        self.assertFalse(Path(first["evidence_path"]).exists())

        second = self._capture("resumed-session", "changed transcript keep summaries short")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(payload),
        )
        first_job_id = Path(first["queue_path"]).stem
        second_job_id = Path(second["queue_path"]).stem
        self.assertNotEqual(first_job_id, second_job_id)
        backlog = runtime.review_backlog(self.paths)
        self.assertEqual(backlog["positive_clusters"], 1)
        second_cluster = backlog["clusters"][0]
        self.assertEqual(second_cluster["session_ids"], ["resumed-session"])
        self.assertEqual(second_cluster["job_ids"], [second_job_id])
        self.assertEqual(
            second_cluster["occurrences"][0]["result_sha256"],
            runtime._sha256_file(self.paths.sessions / f"{second_job_id}-suggestions.md"),
        )
        self.assertTrue(Path(second["evidence_path"]).is_file())

        reconciliation = runtime.reconcile_review_finalizations(self.paths)
        self.assertEqual(reconciliation["finalized"], 0)
        self.assertTrue(Path(second["evidence_path"]).is_file())
        self.assertNotIn("processed: true", Path(second["audit_path"]).read_text(encoding="utf-8"))

        runtime.review_cluster(self.paths, second_cluster["cluster_id"], "reject", confirm=True)
        ledger = runtime._review_ledger(self.paths)
        events = ledger["cluster_decisions"][second_cluster["cluster_id"]]
        self.assertEqual(len(events), 2)
        self.assertNotEqual(events[0]["occurrences"], events[1]["occurrences"])
        self.assertFalse(Path(second["evidence_path"]).exists())

    def test_legacy_or_malformed_review_ledger_fails_closed(self):
        captured = self._capture(prefix="keep summaries short")
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep summaries short",
                    "context": "The user corrected response length.",
                    "why_it_matters": "Long summaries are harder to scan.",
                }
            ]
        }
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(payload),
        )
        cluster = runtime.review_backlog(self.paths)["clusters"][0]
        ledger_path = self.paths.state / "review-decisions.json"
        runtime.atomic_write_json(
            ledger_path,
            {
                cluster["cluster_id"]: {
                    "decision": "reject",
                    "decided_at": "2026-09-10T12:30:00+00:00",
                    "session_ids": ["session-one"],
                    "instinct_path": None,
                }
            },
        )
        with self.assertRaisesRegex(ValueError, "schema version 2"):
            runtime.review_backlog(self.paths)
        with self.assertRaisesRegex(ValueError, "schema version 2"):
            runtime.reconcile_review_finalizations(self.paths)
        self.assertTrue(Path(captured["evidence_path"]).is_file())

        wrong_occurrence = dict(cluster["occurrences"][0])
        wrong_occurrence["result_sha256"] = "0" * 64
        runtime.atomic_write_json(
            ledger_path,
            {
                "schema_version": 2,
                "cluster_decisions": {
                    cluster["cluster_id"]: [
                        {
                            "decision": "reject",
                            "decided_at": "2026-09-10T12:30:00+00:00",
                            "occurrences": [wrong_occurrence],
                            "instinct_path": None,
                        }
                    ]
                },
                "zero_resolutions": [],
            },
        )
        self.assertEqual(runtime.review_backlog(self.paths)["positive_clusters"], 1)
        self.assertEqual(runtime.reconcile_review_finalizations(self.paths)["finalized"], 0)
        self.assertTrue(Path(captured["evidence_path"]).is_file())

        malformed = runtime._empty_review_ledger()
        malformed["cluster_decisions"][cluster["cluster_id"]] = [
            {
                "decision": "reject",
                "decided_at": "2026-09-10T12:30:00+00:00",
                "occurrences": [{"job_id": Path(captured["queue_path"]).stem}],
                "instinct_path": None,
            }
        ]
        runtime.atomic_write_json(ledger_path, malformed)
        with self.assertRaisesRegex(ValueError, "invalid occurrence"):
            runtime.review_backlog(self.paths)
        self.assertTrue(Path(captured["evidence_path"]).is_file())

    def test_positive_review_does_not_resolve_zero_candidate_audits(self):
        self._capture("zero-session", "routine update")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner({"candidates": []}),
        )
        self._capture("positive-session", "keep summaries short")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(
                {
                    "candidates": [
                        {
                            "type": "voice",
                            "rule": "Keep summaries short.",
                            "evidence": "keep summaries short",
                            "context": "The user corrected response length.",
                            "why_it_matters": "Long summaries are harder to scan.",
                        }
                    ]
                }
            ),
        )
        backlog = runtime.review_backlog(self.paths)
        runtime.review_cluster(self.paths, backlog["clusters"][0]["cluster_id"], "accept", confirm=True)
        remaining = runtime.review_backlog(self.paths)
        self.assertEqual(len(remaining["zero_candidate_audits"]), 1)
        self.assertEqual(runtime.resolve_zero_candidates(self.paths, confirm=True)["count"], 1)

    def test_zero_candidate_confirmation_is_durable_before_cleanup(self):
        captured = self._capture(prefix="routine update")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner({"candidates": []}),
        )
        with (
            mock.patch.object(runtime, "_resolve_zero_candidate_audits", side_effect=OSError("simulated crash")),
            self.assertRaisesRegex(OSError, "simulated crash"),
        ):
            runtime.resolve_zero_candidates(self.paths, confirm=True)

        ledger = runtime._review_ledger(self.paths)
        self.assertEqual(len(ledger["zero_resolutions"]), 1)
        self.assertEqual(runtime.review_backlog(self.paths)["zero_candidate_audits"], [])
        self.assertTrue(Path(captured["evidence_path"]).is_file())

        result = runtime.reconcile_review_finalizations(self.paths)
        self.assertEqual(result["finalized"], 1)
        self.assertFalse(Path(captured["evidence_path"]).exists())

    def test_processed_marker_without_bound_ledger_authority_cannot_delete_evidence(self):
        captured = self._capture(prefix="keep summaries short")
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(
                {
                    "candidates": [
                        {
                            "type": "voice",
                            "rule": "Keep summaries short.",
                            "evidence": "keep summaries short",
                            "context": "The user corrected response length.",
                            "why_it_matters": "Long summaries are harder to scan.",
                        }
                    ]
                }
            ),
        )
        audit_path = Path(captured["audit_path"])
        queue_path = Path(captured["queue_path"])
        queue_before = json.loads(queue_path.read_text(encoding="utf-8"))
        runtime.atomic_write_text(
            audit_path,
            audit_path.read_text(encoding="utf-8").replace("processed: false", "processed: true", 1),
        )

        result = runtime.reconcile_review_finalizations(self.paths)

        self.assertEqual(result, {"status": "complete", "recovered": 0, "finalized": 0, "cleaned": 0})
        self.assertTrue(Path(captured["evidence_path"]).is_file())
        queue_after = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(queue_after["audit_sha256"], queue_before["audit_sha256"])

    def test_review_backlog_reports_and_applies_an_exact_active_match(self):
        runtime.ensure_store(self.paths)
        existing = self.paths.instincts / "pmm-instinct-2026-09-10-001.md"
        existing.write_text(
            "---\n"
            'id: "pmm-instinct-2026-09-10-001"\n'
            'type: "voice"\n'
            "confidence: 0.3\n"
            'status: "active"\n'
            "seen_count: 1\n"
            "---\n\n"
            "Keep summaries short.\n\n"
            "**Why it matters:** Existing guidance.\n",
            encoding="utf-8",
        )
        self._capture(prefix="keep summaries short")
        payload = {
            "candidates": [
                {
                    "type": "voice",
                    "rule": "Keep summaries short.",
                    "evidence": "keep summaries short",
                    "context": "The user repeated an existing preference.",
                    "why_it_matters": "The response should stay easy to scan.",
                }
            ]
        }
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner(payload),
        )
        cluster = runtime.review_backlog(self.paths)["clusters"][0]
        self.assertEqual(cluster["exact_match_state"], "exact")
        result = runtime.review_cluster(
            self.paths,
            cluster["cluster_id"],
            "match",
            confirm=True,
        )
        self.assertEqual(result["instinct_path"], str(existing))
        metadata, _ = runtime._parse_frontmatter(existing.read_text(encoding="utf-8"))
        self.assertEqual(metadata["seen_count"], 2)
        self.assertEqual(len(list(self.paths.instincts.glob("pmm-instinct-*.md"))), 1)

    def test_promotion_rejects_non_finite_or_non_numeric_confidence(self):
        runtime.ensure_store(self.paths)
        invalid_values = ("NaN", "Infinity", '"0.5"', "true")
        for index, confidence in enumerate(invalid_values, start=1):
            with self.subTest(confidence=confidence):
                instinct_id = f"pmm-instinct-2026-09-10-{index:03d}"
                instinct = self.paths.instincts / f"{instinct_id}.md"
                instinct.write_text(
                    "---\n"
                    f'id: "{instinct_id}"\n'
                    'type: "workflow"\n'
                    f"confidence: {confidence}\n"
                    'status: "active"\n'
                    "---\n\n"
                    "Validate guidance before promotion.\n\n"
                    "**Why it matters:** Invalid confidence cannot authorize promotion.\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(
                    ValueError,
                    "instinct confidence must be a finite number from 0 to 1",
                ):
                    runtime.create_promotion_preview(
                        self.paths,
                        instinct_id=instinct_id,
                        target=self.tmp / f"invalid-confidence-{index}" / "CLAUDE.md",
                        destination_class="project",
                        delivery="local",
                    )
        self.assertEqual(list(self.paths.previews.glob("*.json")), [])

    def test_promotion_receipt_binds_exact_target_and_executes_after_approval(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-001"
        instinct = self.paths.instincts / f"{instinct_id}.md"
        instinct.write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "promoted_to: []\n"
            "---\n\n"
            "Verify the final artifact before sharing it.\n\n"
            "**Why it matters:** This prevents avoidable handoff defects.\n",
            encoding="utf-8",
        )
        target = self.tmp / "repo" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("# Project guidance\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        with self.assertRaises(PermissionError):
            runtime.approve_promotion(self.paths, preview["preview_digest"])
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        self.assertTrue(Path(receipt["receipt_path"]).is_file())
        result = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(result["applied"], 1)
        self.assertIn("Verify the final artifact before sharing it.", target.read_text(encoding="utf-8"))
        self.assertEqual(runtime.execute_promotion_receipts(self.paths)["processed"], 0)
        self.assertIn('status: "promoted"', instinct.read_text(encoding="utf-8"))

    def test_promotion_approval_rejects_symlink_and_non_regular_preview_leaves(self):
        runtime.ensure_store(self.paths)
        real_read_text = Path.read_text

        for index, leaf_kind in enumerate(("symlink", "directory"), start=31):
            with self.subTest(leaf_kind=leaf_kind):
                instinct_id = f"pmm-instinct-2026-09-10-{index:03d}"
                (self.paths.instincts / f"{instinct_id}.md").write_text(
                    "---\n"
                    f'id: "{instinct_id}"\n'
                    'type: "workflow"\n'
                    "confidence: 0.5\n"
                    'status: "active"\n'
                    "---\n\n"
                    "Keep preview authority inside the private state store.\n\n"
                    "**Why it matters:** Approval must not follow an outside-store leaf.\n",
                    encoding="utf-8",
                )
                target = self.tmp / f"preview-leaf-{leaf_kind}" / "CLAUDE.md"
                target.parent.mkdir()
                preview = runtime.create_promotion_preview(
                    self.paths,
                    instinct_id=instinct_id,
                    target=target,
                    destination_class="project",
                    delivery="local",
                )
                preview_path = self.paths.previews / f"{preview['preview_digest']}.json"
                preview_bytes = preview_path.read_bytes()
                preview_path.unlink()
                forbidden_reads = {preview_path}
                if leaf_kind == "symlink":
                    outside = self.tmp / f"outside-preview-{index}.json"
                    outside.write_bytes(preview_bytes)
                    preview_path.symlink_to(outside)
                else:
                    preview_path.mkdir()

                def guarded_read_text(path, *args, **kwargs):
                    if path in forbidden_reads:
                        raise AssertionError("preview authority leaf was read")
                    return real_read_text(path, *args, **kwargs)

                with mock.patch.object(Path, "read_text", new=guarded_read_text):
                    with self.assertRaisesRegex(ValueError, "matching promotion preview was not found"):
                        runtime.approve_promotion(
                            self.paths,
                            preview["preview_digest"],
                            confirm=True,
                        )
                self.assertEqual(list(self.paths.receipts.glob("*.json")), [])

    def test_promotion_rejects_and_matching_skips_outside_store_instinct_leaves(self):
        runtime.ensure_store(self.paths)
        real_read_text = Path.read_text
        outside = self.tmp / "outside-instinct.md"
        instinct_id = "pmm-instinct-2026-09-10-041"
        outside.write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.9\n"
            'status: "active"\n'
            "---\n\n"
            "Never source promotion guidance outside the state store.\n\n"
            "**Why it matters:** State confinement is part of approval authority.\n",
            encoding="utf-8",
        )
        instinct = self.paths.instincts / f"{instinct_id}.md"
        instinct.symlink_to(outside)

        def guarded_read_text(path, *args, **kwargs):
            if path == instinct:
                raise AssertionError("outside-store instinct leaf was read")
            return real_read_text(path, *args, **kwargs)

        with mock.patch.object(Path, "read_text", new=guarded_read_text):
            self.assertIsNone(
                runtime._active_matching_instinct(
                    self.paths,
                    "workflow",
                    "Never source promotion guidance outside the state store.",
                )
            )
            with self.assertRaisesRegex(ValueError, "instinct not found"):
                runtime.create_promotion_preview(
                    self.paths,
                    instinct_id=instinct_id,
                    target=self.tmp / "outside-instinct-target" / "CLAUDE.md",
                    destination_class="project",
                    delivery="local",
                )
        self.assertEqual(list(self.paths.previews.glob("*.json")), [])
        self.assertEqual(list(self.paths.receipts.glob("*.json")), [])

        instinct.unlink()
        instinct.mkdir()
        self.assertIsNone(
            runtime._active_matching_instinct(
                self.paths,
                "workflow",
                "Never source promotion guidance outside the state store.",
            )
        )
        with self.assertRaisesRegex(ValueError, "instinct not found"):
            runtime._load_instinct(self.paths, instinct_id)

    def test_promotion_supports_edited_preview_and_preserves_target_modes(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-011"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Check the artifact.\n\n"
            "**Why it matters:** It prevents mistakes.\n",
            encoding="utf-8",
        )
        existing = self.tmp / "existing" / "CLAUDE.md"
        existing.parent.mkdir()
        existing.write_text("# Existing\n", encoding="utf-8")
        existing.chmod(0o640)
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=existing,
            destination_class="project",
            delivery="local",
            edited_rule="Verify the exact artifact before sharing it.",
            edited_rationale="The approved wording is more precise.",
        )
        self.assertEqual(preview["rule"], "Verify the exact artifact before sharing it.")
        runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        new_target = self.tmp / "new" / "CLAUDE.md"
        new_target.parent.mkdir()
        new_instinct_id = "pmm-instinct-2026-09-10-014"
        (self.paths.instincts / f"{new_instinct_id}.md").write_text(
            "---\n"
            f'id: "{new_instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Check the artifact.\n\n"
            "**Why it matters:** It prevents mistakes.\n",
            encoding="utf-8",
        )
        new_preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=new_instinct_id,
            target=new_target,
            destination_class="project",
            delivery="local",
        )
        runtime.approve_promotion(self.paths, new_preview["preview_digest"], confirm=True)
        self.assertEqual(runtime.execute_promotion_receipts(self.paths)["applied"], 2)
        self.assertEqual(existing.stat().st_mode & 0o777, 0o640)
        self.assertEqual(new_target.stat().st_mode & 0o777, 0o600)

    def test_guidance_duplicate_detection_requires_an_exact_normalized_bullet(self):
        insertion = "- Review public claims before shipping."
        non_duplicates = (
            (
                "shorter-existing",
                f"# Guidance\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n- Review public claims.\n",
            ),
            (
                "longer-existing",
                f"# Guidance\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n"
                "- Always review public claims before shipping carefully.\n",
            ),
            (
                "split-existing",
                f"# Guidance\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n"
                "- Review public claims\n  before shipping.\n",
            ),
        )
        for label, existing in non_duplicates:
            with self.subTest(label=label):
                updated = runtime._render_guidance_update(existing, insertion)
                self.assertNotEqual(updated, existing)
                self.assertIn(f"\n{insertion}\n", updated)

        equivalent = (
            f"# Guidance\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n"
            "* REVIEW PUBLIC CLAIMS BEFORE SHIPPING!!!\n"
        )
        self.assertEqual(runtime._render_guidance_update(equivalent, insertion), equivalent)

        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-011"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Review public claims before shipping.\n\n"
            "**Why it matters:** Exact duplicate detection preserves distinct guidance.\n",
            encoding="utf-8",
        )
        target = self.tmp / "substring" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text(non_duplicates[1][1], encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        self.assertFalse(preview["duplicate"])
        runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        self.assertEqual(runtime.execute_promotion_receipts(self.paths)["applied"], 1)
        self.assertIn(f"\n{insertion}\n", target.read_text(encoding="utf-8"))

    def test_duplicate_promotion_does_not_rewrite_target(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-012"
        rule = "Keep the approved wording exact."
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "scope"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            f"{rule}\n\n"
            "**Why it matters:** Exact wording preserves the decision.\n",
            encoding="utf-8",
        )
        target = self.tmp / "duplicate" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text(
            f"# Guidance\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n- {rule}\n",
            encoding="utf-8",
        )
        inode = target.stat().st_ino
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        self.assertTrue(preview["duplicate"])
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        original_write_json = runtime.atomic_write_json
        failed_once = False

        def fail_first_outcome(path, payload):
            nonlocal failed_once
            if Path(path).parent == self.paths.outcomes and not failed_once:
                failed_once = True
                raise OSError("simulated covered outcome interruption")
            return original_write_json(path, payload)

        with mock.patch.object(runtime, "atomic_write_json", side_effect=fail_first_outcome):
            self.assertEqual(runtime.execute_promotion_receipts(self.paths)["applied"], 1)
        outcome = self.paths.outcomes / f"{receipt['receipt_digest']}.json"
        self.assertFalse(outcome.exists())
        recovered = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(recovered["applied"], 1)
        self.assertEqual(recovered["failed"], 0)
        self.assertEqual(json.loads(outcome.read_text(encoding="utf-8"))["status"], "covered")
        self.assertEqual(target.stat().st_ino, inode)

    def test_source_drift_and_forged_outcome_fail_closed(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-013"
        instinct = self.paths.instincts / f"{instinct_id}.md"
        instinct.write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Use the approved checklist.\n\n"
            "**Why it matters:** It preserves review intent.\n",
            encoding="utf-8",
        )
        target = self.tmp / "drift" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("# Original\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        receipt_digest = receipt["receipt_digest"]
        runtime.atomic_write_json(
            self.paths.outcomes / f"{receipt_digest}.json",
            {
                "schema_version": 1,
                "receipt_digest": "0" * 64,
                "status": "promoted",
                "completed_at": runtime.iso_now(),
                "target_path": str(target),
                "resulting_sha256": preview["resulting_sha256"],
            },
        )
        self.assertEqual(runtime.promotion_counts(self.paths)["pending_execution"], 1)
        instinct.write_text(instinct.read_text(encoding="utf-8").replace("approved checklist", "changed checklist"), encoding="utf-8")
        result = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(target.read_text(encoding="utf-8"), "# Original\n")

    def test_repeated_approval_reuses_one_receipt(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-015"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Reuse the exact approval.\n\n"
            "**Why it matters:** Duplicate receipts create conflicting execution state.\n",
            encoding="utf-8",
        )
        target = self.tmp / "idempotent" / "CLAUDE.md"
        target.parent.mkdir()
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        with mock.patch.object(runtime, "iso_now", return_value="2026-09-10T12:00:01+00:00"):
            first = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        with mock.patch.object(runtime, "iso_now", return_value="2026-09-10T12:05:01+00:00"):
            second = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        self.assertEqual(first["receipt_digest"], second["receipt_digest"])
        self.assertEqual(len(list(self.paths.receipts.glob("*.json"))), 1)

    def test_invalid_receipts_and_unbound_outcomes_cannot_claim_execution(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-016"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "scope"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Bind outcomes to the approved target.\n\n"
            "**Why it matters:** An unrelated file cannot prove execution.\n",
            encoding="utf-8",
        )
        target = self.tmp / "bound" / "CLAUDE.md"
        target.parent.mkdir()
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        (self.paths.receipts / "junk.json").write_text("{}", encoding="utf-8")
        runtime.atomic_write_json(
            self.paths.outcomes / f"{receipt['receipt_digest']}.json",
            {
                "schema_version": 1,
                "receipt_digest": receipt["receipt_digest"],
                "status": "promoted",
                "completed_at": runtime.iso_now(),
                "target_path": str(self.tmp / "wrong" / "CLAUDE.md"),
                "resulting_sha256": "0" * 64,
            },
        )
        counts = runtime.promotion_counts(self.paths)
        self.assertEqual(counts["approved"], 1)
        self.assertEqual(counts["invalid"], 1)
        self.assertEqual(counts["pending_execution"], 1)
        result = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(result["applied"], 1)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(runtime.promotion_counts(self.paths)["promoted"], 1)

    def test_promotion_recovers_after_target_write_before_outcome(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-017"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Recover an exact completed write.\n\n"
            "**Why it matters:** A process crash must not convert success into drift.\n",
            encoding="utf-8",
        )
        target = self.tmp / "recovery" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("# Before\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        original_write_json = runtime.atomic_write_json
        failed_once = False

        def fail_first_outcome(path, payload):
            nonlocal failed_once
            if Path(path).parent == self.paths.outcomes and not failed_once:
                failed_once = True
                raise OSError("simulated outcome interruption")
            return original_write_json(path, payload)

        with mock.patch.object(runtime, "atomic_write_json", side_effect=fail_first_outcome):
            first = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(first["applied"], 1)
        outcome = self.paths.outcomes / f"{receipt['receipt_digest']}.json"
        self.assertFalse(outcome.exists())
        inode = target.stat().st_ino
        second = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(second["applied"], 1)
        self.assertEqual(second["failed"], 0)
        self.assertEqual(target.stat().st_ino, inode)
        self.assertEqual(json.loads(outcome.read_text(encoding="utf-8"))["status"], "promoted")

    def test_promotion_executor_rejects_tampered_approval_receipt(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-018"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Reject altered approval evidence.\n\n"
            "**Why it matters:** Execution must remain bound to the exact approved action.\n",
            encoding="utf-8",
        )
        target = self.tmp / "receipt-tamper" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("# Before\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        receipt_path = Path(receipt["receipt_path"])
        tampered = json.loads(receipt_path.read_text(encoding="utf-8"))
        tampered["approved_action"]["rule"] = "Tampered rule."
        runtime.atomic_write_json(receipt_path, tampered)

        result = runtime.execute_promotion_receipts(self.paths)

        self.assertEqual(result["applied"], 0)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(target.read_text(encoding="utf-8"), "# Before\n")
        self.assertEqual(runtime.promotion_counts(self.paths)["invalid"], 1)

    def test_promotion_executor_rejects_target_drift_after_approval(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-019"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "scope"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Reject execution-time target drift.\n\n"
            "**Why it matters:** Approval applies only to the reviewed target bytes.\n",
            encoding="utf-8",
        )
        target = self.tmp / "execution-drift" / "CLAUDE.md"
        target.parent.mkdir()
        target.write_text("# Before\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        receipt = runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        target.write_text("# External change\n", encoding="utf-8")

        result = runtime.execute_promotion_receipts(self.paths)

        self.assertEqual(result["applied"], 0)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(target.read_text(encoding="utf-8"), "# External change\n")
        outcome_path = self.paths.outcomes / f"{receipt['receipt_digest']}.json"
        outcome = json.loads(outcome_path.read_text(encoding="utf-8"))
        self.assertEqual(outcome["status"], "failed")
        self.assertIn("target changed after approval", outcome["error"])

    def test_target_drift_invalidates_approval(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-002"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "scope"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Keep changes inside the approved scope.\n\n"
            "**Why it matters:** Scope drift changes the approved outcome.\n",
            encoding="utf-8",
        )
        target = self.tmp / "CLAUDE.md"
        target.write_text("# Original\n", encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="project",
            delivery="local",
        )
        target.write_text("# Changed\n", encoding="utf-8")
        with self.assertRaises(PermissionError):
            runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)

    def test_promotion_rejects_destination_class_mismatches(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-004"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Keep human approval before promotion.\n\n"
            "**Why it matters:** Background work must not manufacture approval.\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            runtime.create_promotion_preview(
                self.paths,
                instinct_id=instinct_id,
                target=self.tmp / "notes.md",
                destination_class="project",
                delivery="local",
            )
        with self.assertRaises(ValueError):
            runtime.create_promotion_preview(
                self.paths,
                instinct_id=instinct_id,
                target=self.tmp / "RUN-workflow.md",
                destination_class="skill",
                delivery="local",
            )

    def test_promotion_preview_rejects_protected_targets_and_low_confidence(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-020"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "scope"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Keep promotions outside protected runtime paths.\n\n"
            "**Why it matters:** Runtime packages and evidence stores are not guidance targets.\n",
            encoding="utf-8",
        )
        protected_targets = (
            runtime.bundle_root() / "CLAUDE.md",
            self.paths.state_root / "CLAUDE.md",
            self.tmp / "plugins" / "cache" / "example" / "CLAUDE.md",
        )
        for target in protected_targets:
            with self.subTest(target=target), self.assertRaises(ValueError):
                runtime.create_promotion_preview(
                    self.paths,
                    instinct_id=instinct_id,
                    target=target,
                    destination_class="project",
                    delivery="local",
                )

        low_confidence_id = "pmm-instinct-2026-09-10-021"
        (self.paths.instincts / f"{low_confidence_id}.md").write_text(
            "---\n"
            f'id: "{low_confidence_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.3\n"
            'status: "active"\n'
            "---\n\n"
            "Do not promote an unconfirmed suggestion.\n\n"
            "**Why it matters:** Low-confidence guidance has not crossed the promotion threshold.\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "confidence is below 0.5"):
            runtime.create_promotion_preview(
                self.paths,
                instinct_id=low_confidence_id,
                target=self.tmp / "low-confidence" / "CLAUDE.md",
                destination_class="project",
                delivery="local",
            )

    def test_governed_delivery_creates_review_patch_without_mutating_target(self):
        runtime.ensure_store(self.paths)
        instinct_id = "pmm-instinct-2026-09-10-003"
        (self.paths.instincts / f"{instinct_id}.md").write_text(
            "---\n"
            f'id: "{instinct_id}"\n'
            'type: "workflow"\n'
            "confidence: 0.5\n"
            'status: "active"\n'
            "---\n\n"
            "Record review evidence before publication.\n\n"
            "**Why it matters:** Review needs a traceable basis.\n",
            encoding="utf-8",
        )
        target = self.tmp / "repo" / "RUN-workflow.md"
        target.parent.mkdir()
        original = "# Workflow\n"
        target.write_text(original, encoding="utf-8")
        preview = runtime.create_promotion_preview(
            self.paths,
            instinct_id=instinct_id,
            target=target,
            destination_class="skill",
            delivery="review",
        )
        runtime.approve_promotion(self.paths, preview["preview_digest"], confirm=True)
        result = runtime.execute_promotion_receipts(self.paths)
        self.assertEqual(result["awaiting_review"], 1)
        self.assertEqual(target.read_text(encoding="utf-8"), original)
        patch_path = next(self.paths.changesets.glob("*.patch"))
        outcome_path = next(self.paths.outcomes.glob("*.json"))
        outcome = json.loads(outcome_path.read_text(encoding="utf-8"))
        self.assertEqual(outcome["changeset_sha256"], runtime._sha256_file(patch_path))
        patch_path.write_text("tampered\n", encoding="utf-8")
        outcome["changeset_sha256"] = runtime._sha256_file(patch_path)
        runtime.atomic_write_json(outcome_path, outcome)
        self.assertEqual(runtime.execute_promotion_receipts(self.paths)["awaiting_review"], 1)
        repaired = json.loads(outcome_path.read_text(encoding="utf-8"))
        self.assertEqual(repaired["changeset_sha256"], runtime._sha256_file(patch_path))
        self.assertNotEqual(patch_path.read_text(encoding="utf-8"), "tampered\n")

    def test_detached_worker_launches_only_for_pending_work(self):
        self._capture()
        launcher = FakeLauncher()
        self.assertTrue(runtime.start_detached_worker(self.paths, root=BUNDLE, launcher=launcher))
        command, kwargs = launcher.calls[0]
        self.assertTrue(command[1].endswith("claude_instinct_worker.py"))
        self.assertIn("--drain", command)
        self.assertTrue(kwargs["start_new_session"])
        self.assertEqual(kwargs["env"]["PMM_INSTINCT_WORKER"], "1")

    def test_plugin_data_state_root_survives_detached_worker_round_trip(self):
        plugin_data = self.tmp / ".claude" / "plugins" / "data" / "pmm-instinct-review"
        with mock.patch.dict(
            runtime.os.environ,
            {"CLAUDE_PLUGIN_DATA": str(plugin_data)},
            clear=False,
        ):
            plugin_paths = runtime.resolve_paths()
        runtime.ensure_store(plugin_paths)
        runtime.atomic_write_json(plugin_paths.capture_inbox / "pending.json", {"pending": True})
        launcher = FakeLauncher()

        self.assertTrue(runtime.start_detached_worker(plugin_paths, root=BUNDLE, launcher=launcher))

        command, _ = launcher.calls[0]
        state_argument = command[command.index("--state-root") + 1]
        resolved_round_trip = runtime.resolve_paths(state_argument)
        self.assertEqual(resolved_round_trip.state_root, plugin_paths.state_root)
        self.assertEqual(
            resolved_round_trip.state_root,
            (plugin_data / "instinct-review").resolve(),
        )

    def test_capture_pending_launch_short_circuits_retained_store_scans(self):
        runtime.ensure_store(self.paths)
        runtime.atomic_write_json(self.paths.capture_inbox / "pending.json", {"pending": True})
        launcher = FakeLauncher()
        with (
            mock.patch.object(runtime, "read_queue", side_effect=AssertionError("queue scanned in SessionEnd path")),
            mock.patch.object(runtime, "promotion_counts", side_effect=AssertionError("receipts scanned in SessionEnd path")),
        ):
            self.assertTrue(runtime.start_detached_worker(self.paths, root=BUNDLE, launcher=launcher))
        self.assertEqual(len(launcher.calls), 1)

    def test_session_start_briefs_from_one_summary_without_retained_artifact_scans(self):
        runtime.ensure_store(self.paths)
        snapshot = {
            "schema_version": 1,
            "updated_at": "2026-09-10T12:34:56+00:00",
            "pending_extraction": 2,
            "review_ready": 3,
            "pending_promotion": 4,
        }
        summary_path = self.paths.state / "runtime-summary.json"
        runtime.atomic_write_json(summary_path, snapshot)
        self.assertLessEqual(summary_path.stat().st_size, 4096)
        output = io.StringIO()
        forbidden = AssertionError("SessionStart scanned retained runtime artifacts")
        with (
            mock.patch.object(hook, "ensure_store", wraps=hook.ensure_store) as ensure,
            mock.patch.object(hook, "start_detached_worker", return_value=True) as start,
            mock.patch.object(
                hook,
                "read_runtime_summary",
                wraps=runtime.read_runtime_summary,
            ) as read_summary,
            mock.patch.object(hook, "read_queue", create=True, side_effect=forbidden),
            mock.patch.object(hook, "review_ready_count", create=True, side_effect=forbidden),
            mock.patch.object(hook, "promotion_counts", create=True, side_effect=forbidden),
            mock.patch.object(
                hook,
                "reconcile_review_finalizations",
                create=True,
                side_effect=forbidden,
            ),
            redirect_stdout(output),
        ):
            self.assertEqual(
                hook.session_start({"session_id": "summary-session"}, state_root=self.paths.state_root),
                0,
            )

        ensure.assert_called_once_with(self.paths, create_config=False)
        start.assert_called_once_with(self.paths, root=hook.ROOT, force=True)
        read_summary.assert_called_once_with(self.paths)
        response = json.loads(output.getvalue())
        context = response["hookSpecificOutput"]["additionalContext"]
        self.assertIn(snapshot["updated_at"], context)
        self.assertIn("2 extraction job(s) pending", context)
        self.assertIn("3 extracted session(s)", context)
        self.assertIn("4 approved promotion receipt(s)", context)

    def test_worker_drains_reconciles_promotes_and_refreshes_summary_in_order(self):
        calls = []

        def stage(name):
            def invoke(paths, **kwargs):
                calls.append(name)
                return {"status": "complete"}

            return invoke

        with (
            mock.patch.object(worker, "resolve_paths", return_value=self.paths),
            mock.patch.object(worker, "drain_capture_requests", side_effect=stage("capture")),
            mock.patch.object(
                worker,
                "reconcile_review_finalizations",
                side_effect=stage("reconciliation"),
            ),
            mock.patch.object(worker, "drain_extraction_queue", side_effect=stage("extraction")),
            mock.patch.object(worker, "execute_promotion_receipts", side_effect=stage("promotion")),
            mock.patch.object(worker, "refresh_runtime_summary", side_effect=stage("summary")),
            mock.patch.object(sys, "argv", ["claude_instinct_worker.py", "--state-root", str(self.paths.state_root), "--drain"]),
            redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(worker.main(), 0)
        self.assertEqual(
            calls,
            ["capture", "reconciliation", "extraction", "promotion", "summary"],
        )

    def test_review_cli_reports_lock_contention_without_traceback(self):
        runtime.ensure_store(self.paths)
        (self.paths.state / "review-transaction.lock").write_text(
            json.dumps({"pid": os.getpid(), "created_at": runtime.iso_now()}),
            encoding="utf-8",
        )
        stderr = io.StringIO()
        with (
            mock.patch.object(
                sys,
                "argv",
                [
                    "claude_instinct_review.py",
                    "--state-root",
                    str(self.paths.state_root),
                    "resolve-zero",
                    "--confirm",
                ],
            ),
            redirect_stderr(stderr),
        ):
            self.assertEqual(review_cli.main(), 2)
        self.assertIn("another review transaction is already running", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_standalone_installer_preserves_unrelated_hooks_and_state(self):
        claude_home = self.tmp / ".claude"
        claude_home.mkdir()
        settings = {
            "hooks": {
                "SessionStart": [
                    {"hooks": [{"type": "command", "command": "other-tool", "args": ["start"]}]},
                ]
            }
        }
        (claude_home / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        self.assertEqual(receipt["schema_version"], 2)
        self.assertEqual(receipt["receipt_digest"], installer._receipt_digest(receipt))
        self.assertEqual(
            receipt["owned_hook_handlers"],
            installer._hook_identities(BUNDLE, state_root),
        )
        session_end_handler = next(
            item["handler"] for item in receipt["owned_hook_handlers"] if item["event"] == "SessionEnd"
        )
        self.assertNotIn("async", session_end_handler)
        self.assertTrue(Path(receipt["skill_path"]).is_symlink())
        serialized = (claude_home / "settings.json").read_text(encoding="utf-8")
        self.assertIn("other-tool", serialized)
        self.assertIn("claude_instinct_hook.py", serialized)
        installed_settings = json.loads(serialized)
        owned_handlers = [
            handler
            for event in ("SessionStart", "SessionEnd")
            for entry in installed_settings["hooks"][event]
            for handler in entry["hooks"]
            if any("claude_instinct_hook.py" in str(arg) for arg in handler.get("args", []))
        ]
        self.assertEqual(len(owned_handlers), 2)
        self.assertTrue(all(handler["command"] == "python3" for handler in owned_handlers))
        self.assertTrue(all(len(handler["args"]) == 4 for handler in owned_handlers))
        self.assertTrue(all(handler["args"][1] == "--state-root" for handler in owned_handlers))
        self.assertFalse(runtime.load_config(runtime.resolve_paths(state_root))["enabled"])
        status = installer.check(claude_home=claude_home, state_root=state_root)
        self.assertTrue(status["receipt_valid"])
        self.assertTrue(status["skill_target_valid"])
        self.assertTrue(status["bundle_valid"])
        self.assertTrue(status["installation_valid"])
        self.assertEqual(status["owned_hook_handlers"], 2)
        removed = installer.uninstall(claude_home=claude_home, state_root=state_root, confirm=True)
        self.assertEqual(removed["removed_hook_handlers"], 2)
        self.assertTrue(state_root.is_dir())
        self.assertIn("other-tool", (claude_home / "settings.json").read_text(encoding="utf-8"))

    def test_installer_check_rejects_a_retargeted_skill_symlink(self):
        claude_home = self.tmp / "retargeted-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        skill_path = Path(receipt["skill_path"])
        unrelated_skill = self.tmp / "unrelated-skill-target"
        unrelated_skill.mkdir()
        (unrelated_skill / "SKILL.md").write_text(
            "---\nname: unrelated-skill\n---\n",
            encoding="utf-8",
        )
        skill_path.unlink()
        skill_path.symlink_to(unrelated_skill, target_is_directory=True)

        status = installer.check(claude_home=claude_home, state_root=state_root)

        self.assertTrue(status["receipt_valid"])
        self.assertTrue(status["skill_symlink"])
        self.assertFalse(status["skill_target_valid"])
        self.assertFalse(status["installation_valid"])

    def test_symlinked_installed_state_directory_invalidates_check_and_uninstall(self):
        claude_home = self.tmp / "symlinked-state-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        settings_path = claude_home / "settings.json"
        skill_path = Path(receipt["skill_path"])
        settings_before = settings_path.read_bytes()
        skill_target_before = os.readlink(skill_path)
        backups_before = list(claude_home.glob("settings.json.*.bak"))
        installed_state = state_root / "state"
        external_state = self.tmp / "external-installed-state"
        installed_state.rename(external_state)
        receipt_before = (external_state / "installation.json").read_bytes()
        installed_state.symlink_to(external_state, target_is_directory=True)

        status = installer.check(claude_home=claude_home, state_root=state_root)
        self.assertFalse(status["receipt_valid"])
        self.assertFalse(status["installation_valid"])
        self.assertTrue(installed_state.is_symlink())
        self.assertEqual((external_state / "installation.json").read_bytes(), receipt_before)

        with self.assertRaisesRegex(
            PermissionError,
            "uninstall requires a valid, untampered installation receipt",
        ):
            installer.uninstall(
                claude_home=claude_home,
                state_root=state_root,
                confirm=True,
            )

        self.assertEqual(settings_path.read_bytes(), settings_before)
        self.assertEqual(os.readlink(skill_path), skill_target_before)
        self.assertEqual(list(claude_home.glob("settings.json.*.bak")), backups_before)
        self.assertEqual((external_state / "installation.json").read_bytes(), receipt_before)
        self.assertTrue(installed_state.is_symlink())

    def test_installer_refuses_an_incomplete_public_bundle_with_nested_skill(self):
        bundle = self.tmp / "plugins" / "pmm-instinct-review"
        (bundle / "scripts").mkdir(parents=True)
        (bundle / "scripts" / "claude_instinct_hook.py").write_text("# hook\n", encoding="utf-8")
        skill = bundle / "skills" / "pmm-instinct-review"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: pmm-instinct-review\n---\n", encoding="utf-8")
        claude_home = self.tmp / "public-claude"
        claude_home.mkdir()
        state_root = claude_home / "pmm-instinct-review-data"
        with self.assertRaisesRegex(ValueError, "bundle is incomplete"):
            installer.install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=bundle,
                mode="symlink",
            )
        self.assertFalse(state_root.exists())
        self.assertFalse((claude_home / "skills").exists())
        self.assertFalse((claude_home / "settings.json").exists())

    def test_installer_check_detects_missing_or_symlinked_bundle_assets(self):
        for mutation in ("missing", "symlink"):
            with self.subTest(mutation=mutation):
                claude_home = self.tmp / f"bundle-check-{mutation}"
                state_root = claude_home / "pmm-instinct-review-data"
                receipt = installer.install(
                    claude_home=claude_home,
                    state_root=state_root,
                    source_root=BUNDLE,
                    mode="copy",
                )
                intact = installer.check(claude_home=claude_home, state_root=state_root)
                self.assertTrue(intact["bundle_valid"])
                self.assertTrue(intact["installation_valid"])

                asset = Path(receipt["active_root"]) / "assets" / "claude-extractor-schema.json"
                asset.unlink()
                if mutation == "symlink":
                    replacement = self.tmp / f"replacement-{mutation}.json"
                    replacement.write_text("{}\n", encoding="utf-8")
                    asset.symlink_to(replacement)

                invalid = installer.check(claude_home=claude_home, state_root=state_root)
                self.assertTrue(invalid["receipt_valid"])
                self.assertTrue(invalid["skill_target_valid"])
                self.assertFalse(invalid["bundle_valid"])
                self.assertFalse(invalid["installation_valid"])

    def test_repeat_copy_install_refuses_a_damaged_receipt_owned_snapshot_without_mutation(self):
        claude_home = self.tmp / "damaged-copy-upgrade"
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="copy",
        )
        active_root = Path(receipt["active_root"])
        damaged_asset = active_root / "assets" / "claude-extractor-schema.json"
        damaged_asset.unlink()
        settings_path = claude_home / "settings.json"
        receipt_path = state_root / "state" / "installation.json"
        skill_path = Path(receipt["skill_path"])
        settings_before = settings_path.read_bytes()
        receipt_before = receipt_path.read_bytes()
        skill_before = os.readlink(skill_path)
        backups_before = list(claude_home.glob("settings.json.*.bak"))

        with self.assertRaisesRegex(ValueError, "bundle is incomplete"):
            installer.install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=BUNDLE,
                mode="copy",
            )

        self.assertEqual(settings_path.read_bytes(), settings_before)
        self.assertEqual(receipt_path.read_bytes(), receipt_before)
        self.assertEqual(os.readlink(skill_path), skill_before)
        self.assertEqual(list(claude_home.glob("settings.json.*.bak")), backups_before)
        self.assertFalse(damaged_asset.exists())

    def test_public_bundle_check_covers_mandatory_nested_skill_dependencies(self):
        cases = (
            (
                "missing-run",
                Path("skills/pmm-instinct-review/references/RUN-workflow.md"),
                "missing",
            ),
            (
                "symlinked-runtime",
                Path("skills/pmm-instinct-review/scripts/instinct_review.py"),
                "symlink",
            ),
        )
        for label, relative, mutation in cases:
            with self.subTest(label=label):
                claude_home = self.tmp / f"nested-bundle-check-{label}"
                state_root = claude_home / "pmm-instinct-review-data"
                receipt = installer.install(
                    claude_home=claude_home,
                    state_root=state_root,
                    source_root=BUNDLE,
                    mode="copy",
                )
                dependency = Path(receipt["active_root"]) / relative
                dependency.unlink()
                if mutation == "symlink":
                    replacement = self.tmp / "external-instinct-review.py"
                    replacement.write_text("# external replacement\n", encoding="utf-8")
                    dependency.symlink_to(replacement)

                status = installer.check(claude_home=claude_home, state_root=state_root)
                self.assertTrue(status["receipt_valid"])
                self.assertFalse(status["bundle_valid"])
                self.assertFalse(status["installation_valid"])

    def test_public_bundle_check_covers_each_nested_runtime_module(self):
        modules = (
            Path("skills/pmm-instinct-review/scripts/pmm_instinct/__init__.py"),
            Path("skills/pmm-instinct-review/scripts/pmm_instinct/adapters.py"),
            Path("skills/pmm-instinct-review/scripts/pmm_instinct/runtime.py"),
        )
        for module in modules:
            for mutation in ("missing", "symlink"):
                label = f"{module.stem}-{mutation}"
                with self.subTest(module=str(module), mutation=mutation):
                    claude_home = self.tmp / f"nested-runtime-check-{label}"
                    state_root = claude_home / "pmm-instinct-review-data"
                    receipt = installer.install(
                        claude_home=claude_home,
                        state_root=state_root,
                        source_root=BUNDLE,
                        mode="copy",
                    )
                    dependency = Path(receipt["active_root"]) / module
                    dependency.unlink()
                    if mutation == "symlink":
                        replacement = self.tmp / f"external-{module.name}"
                        replacement.write_text("# external replacement\n", encoding="utf-8")
                        dependency.symlink_to(replacement)

                    status = installer.check(claude_home=claude_home, state_root=state_root)
                    self.assertTrue(status["receipt_valid"])
                    self.assertFalse(status["bundle_valid"])
                    self.assertFalse(status["installation_valid"])

    def test_uninstall_preserves_an_unowned_skill_symlink(self):
        claude_home = self.tmp / "unowned-claude"
        skill_parent = claude_home / "skills"
        skill_parent.mkdir(parents=True)
        unrelated = self.tmp / "unrelated-skill"
        unrelated.mkdir()
        (skill_parent / "pmm-instinct-review").symlink_to(unrelated, target_is_directory=True)
        state_root = claude_home / "pmm-instinct-review-data"
        runtime.ensure_store(runtime.resolve_paths(state_root))
        before = sorted(str(path.relative_to(claude_home)) for path in claude_home.rglob("*"))
        with self.assertRaises(PermissionError):
            installer.uninstall(claude_home=claude_home, state_root=state_root, confirm=True)
        after = sorted(str(path.relative_to(claude_home)) for path in claude_home.rglob("*"))
        self.assertEqual(after, before)
        self.assertTrue((skill_parent / "pmm-instinct-review").is_symlink())

    def test_tampered_receipt_blocks_uninstall_without_mutation(self):
        claude_home = self.tmp / "tampered-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        receipt_path = state_root / "state" / "installation.json"
        tampered = json.loads(receipt_path.read_text(encoding="utf-8"))
        tampered["active_root"] = str(self.tmp / "other-bundle")
        receipt_path.write_text(json.dumps(tampered), encoding="utf-8")
        settings_path = claude_home / "settings.json"
        settings_before = settings_path.read_bytes()
        backups_before = list(claude_home.glob("settings.json.*.bak"))

        with self.assertRaises(PermissionError):
            installer.uninstall(claude_home=claude_home, state_root=state_root, confirm=True)

        self.assertEqual(settings_path.read_bytes(), settings_before)
        self.assertEqual(list(claude_home.glob("settings.json.*.bak")), backups_before)
        self.assertTrue(Path(receipt["skill_path"]).is_symlink())

    def test_uninstall_preserves_modified_and_same_basename_handlers(self):
        claude_home = self.tmp / "modified-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        settings_path = claude_home / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        modified = settings["hooks"]["SessionStart"][0]["hooks"][0]
        modified["timeout"] = 17
        collision = {
            "type": "command",
            "command": "python3",
            "args": [
                "/tmp/coincidental/claude_instinct_hook.py",
                "--state-root",
                "/tmp/unrelated-state",
                "session-end",
            ],
            "timeout": 5,
        }
        settings["hooks"]["SessionEnd"].append({"hooks": [collision]})
        settings_path.write_text(json.dumps(settings), encoding="utf-8")

        before = settings_path.read_bytes()
        skill_path = claude_home / "skills" / "pmm-instinct-review"
        status = installer.check(claude_home=claude_home, state_root=state_root)
        self.assertTrue(status["receipt_valid"])
        self.assertEqual(status["owned_hook_handlers"], 1)
        self.assertEqual(status["ambiguous_hook_handlers"], 2)
        with self.assertRaises(PermissionError):
            installer.uninstall(
                claude_home=claude_home,
                state_root=state_root,
                confirm=True,
            )

        self.assertEqual(settings_path.read_bytes(), before)
        self.assertTrue(skill_path.is_symlink())

    def test_upgrade_refuses_modified_or_same_basename_handlers_without_mutation(self):
        claude_home = self.tmp / "upgrade-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        settings_path = claude_home / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        modified = settings["hooks"]["SessionStart"][0]["hooks"][0]
        modified["timeout"] = 19
        collision = {
            "type": "command",
            "command": "python3",
            "args": [
                "/tmp/coincidental/claude_instinct_hook.py",
                "--state-root",
                "/tmp/unrelated-state",
                "session-start",
            ],
            "timeout": 5,
        }
        settings["hooks"]["SessionStart"].append({"hooks": [collision]})
        settings_path.write_text(json.dumps(settings), encoding="utf-8")

        before = settings_path.read_bytes()
        receipt_path = state_root / "state" / "installation.json"
        receipt_before = receipt_path.read_bytes()
        backups_before = list(claude_home.glob("settings.json.*.bak"))
        with self.assertRaises(PermissionError):
            installer.install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=BUNDLE,
                mode="symlink",
            )

        self.assertEqual(settings_path.read_bytes(), before)
        self.assertEqual(receipt_path.read_bytes(), receipt_before)
        self.assertEqual(list(claude_home.glob("settings.json.*.bak")), backups_before)
        self.assertTrue((claude_home / "skills" / "pmm-instinct-review").is_symlink())

    def test_clean_upgrade_replaces_exact_receipt_owned_handlers(self):
        claude_home = self.tmp / "clean-upgrade-claude"
        state_root = claude_home / "pmm-instinct-review-data"
        installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )
        settings_path = claude_home / "settings.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        unrelated = {"type": "command", "command": "other-tool", "args": ["start"]}
        settings["hooks"]["SessionStart"].append({"hooks": [unrelated]})
        settings_path.write_text(json.dumps(settings), encoding="utf-8")
        runtime.update_config(
            runtime.resolve_paths(state_root),
            enabled=True,
            privacy_acknowledged_at="2026-09-10T12:00:00+00:00",
        )

        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="symlink",
        )

        upgraded = json.loads(settings_path.read_text(encoding="utf-8"))
        handlers = [
            handler
            for entries in upgraded["hooks"].values()
            for entry in entries
            for handler in entry["hooks"]
        ]
        self.assertIn(unrelated, handlers)
        for identity in receipt["owned_hook_handlers"]:
            self.assertEqual(handlers.count(identity["handler"]), 1)
        self.assertTrue(receipt["capture_enabled"])
        self.assertTrue(receipt["privacy_acknowledged"])
        self.assertEqual(receipt["receipt_digest"], installer._receipt_digest(receipt))
        self.assertTrue(installer.check(claude_home=claude_home, state_root=state_root)["receipt_valid"])

    def test_install_stops_on_unreceipted_pmm_looking_hook(self):
        claude_home = self.tmp / "ambiguous-claude"
        claude_home.mkdir()
        settings_path = claude_home / "settings.json"
        settings_path.write_text(
            json.dumps(
                {
                    "hooks": {
                        "SessionEnd": [
                            {
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "python3",
                                        "args": [
                                            "/tmp/coincidental/claude_instinct_hook.py",
                                            "--state-root",
                                            "/tmp/unrelated-state",
                                            "session-end",
                                        ],
                                        "timeout": 5,
                                    }
                                ]
                            }
                        ]
                    }
                }
            ),
            encoding="utf-8",
        )
        settings_before = settings_path.read_bytes()
        state_root = claude_home / "pmm-instinct-review-data"

        status = installer.check(claude_home=claude_home, state_root=state_root)
        self.assertFalse(status["receipt_valid"])
        self.assertEqual(status["owned_hook_handlers"], 0)
        self.assertEqual(status["ambiguous_hook_handlers"], 1)
        with self.assertRaises(PermissionError):
            installer.install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertEqual(settings_path.read_bytes(), settings_before)
        self.assertFalse(state_root.exists())
        self.assertFalse((claude_home / "skills").exists())

    def test_install_rejects_protected_state_roots_without_mutation(self):
        def snapshot(root):
            paths = [root, *sorted(root.rglob("*"), key=str)]
            result = {}
            for path in paths:
                key = "." if path == root else str(path.relative_to(root))
                mode = path.lstat().st_mode
                if path.is_symlink():
                    value = ("symlink", mode, os.readlink(path))
                elif path.is_file():
                    value = ("file", mode, path.read_bytes())
                else:
                    value = ("directory", mode, None)
                result[key] = value
            return result

        for case in (
            "claude-home",
            "settings",
            "settings-descendant",
            "skills-directory",
            "skill-target",
            "skill-target-descendant",
            "source-ancestor",
            "active-bundle-ancestor",
        ):
            with self.subTest(case=case):
                case_root = self.tmp / f"protected-state-{case}"
                claude_home = case_root / "custom-claude"
                skills = claude_home / "skills"
                skills.mkdir(parents=True)
                settings = claude_home / "settings.json"
                settings.write_text('{"custom":"preserve"}\n', encoding="utf-8")
                (skills / "keep.txt").write_text("preserve\n", encoding="utf-8")
                source = BUNDLE
                mode = "symlink"
                if case == "claude-home":
                    state_root = claude_home
                elif case == "settings":
                    state_root = settings
                elif case == "settings-descendant":
                    state_root = settings / "nested-state"
                elif case == "skills-directory":
                    state_root = skills
                elif case == "skill-target":
                    state_root = skills / "pmm-instinct-review"
                elif case == "skill-target-descendant":
                    state_root = skills / "pmm-instinct-review" / "nested-state"
                elif case == "source-ancestor":
                    state_root = case_root / "source-container"
                    source = state_root / "bundle"
                    shutil.copytree(BUNDLE, source)
                else:
                    state_root = case_root
                    mode = "copy"
                before = snapshot(case_root)

                with self.assertRaisesRegex(ValueError, "state root"):
                    installer.install(
                        claude_home=claude_home,
                        state_root=state_root,
                        source_root=source,
                        mode=mode,
                    )

                self.assertEqual(snapshot(case_root), before)

    def test_install_rejects_unknown_state_entry_without_creating_config_or_mutating(self):
        claude_home = self.tmp / "unknown-state-claude"
        claude_home.mkdir()
        settings = claude_home / "settings.json"
        settings.write_text('{"custom":"preserve"}\n', encoding="utf-8")
        state_root = claude_home / "pmm-instinct-review-data"
        state_root.mkdir()
        unknown = state_root / "foreign-entry.txt"
        unknown.write_text("preserve\n", encoding="utf-8")
        unknown.chmod(0o640)
        settings_before = settings.read_bytes()
        unknown_before = unknown.read_bytes()
        unknown_mode = unknown.stat().st_mode & 0o777
        entries_before = sorted(path.name for path in state_root.iterdir())
        backups_before = list(claude_home.glob("settings.json.*.bak"))

        with self.assertRaisesRegex(ValueError, "not a dedicated PMM Instinct Review store"):
            installer.install(
                claude_home=claude_home,
                state_root=state_root,
                source_root=BUNDLE,
                mode="symlink",
            )

        self.assertEqual(settings.read_bytes(), settings_before)
        self.assertEqual(unknown.read_bytes(), unknown_before)
        self.assertEqual(unknown.stat().st_mode & 0o777, unknown_mode)
        self.assertEqual(sorted(path.name for path in state_root.iterdir()), entries_before)
        self.assertEqual(list(claude_home.glob("settings.json.*.bak")), backups_before)
        self.assertFalse((state_root / "config.json").exists())
        self.assertFalse((claude_home / "skills").exists())

    def test_install_preflights_settings_and_destinations_before_mutation(self):
        invalid_home = self.tmp / "invalid-settings-claude"
        invalid_home.mkdir()
        invalid_settings = invalid_home / "settings.json"
        invalid_settings.write_text('{"hooks":{"SessionStart":{}}}', encoding="utf-8")
        invalid_before = invalid_settings.read_bytes()
        invalid_state = invalid_home / "pmm-instinct-review-data"
        with self.assertRaises(ValueError):
            installer.install(
                claude_home=invalid_home,
                state_root=invalid_state,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertEqual(invalid_settings.read_bytes(), invalid_before)
        self.assertFalse(invalid_state.exists())
        self.assertFalse((invalid_home / "skills").exists())

        occupied_home = self.tmp / "occupied-claude"
        occupied_skill = occupied_home / "skills" / "pmm-instinct-review"
        occupied_skill.mkdir(parents=True)
        occupied_settings = occupied_home / "settings.json"
        occupied_settings.write_text("{}", encoding="utf-8")
        occupied_before = occupied_settings.read_bytes()
        occupied_state = occupied_home / "pmm-instinct-review-data"
        with self.assertRaises(FileExistsError):
            installer.install(
                claude_home=occupied_home,
                state_root=occupied_state,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertEqual(occupied_settings.read_bytes(), occupied_before)
        self.assertFalse(occupied_state.exists())

        inbox_home = self.tmp / "occupied-inbox-claude"
        inbox_home.mkdir()
        inbox_settings = inbox_home / "settings.json"
        inbox_settings.write_text("{}", encoding="utf-8")
        inbox_state = inbox_home / "pmm-instinct-review-data"
        inbox_state.mkdir()
        occupied_inbox = inbox_state / "capture-inbox"
        occupied_inbox.write_text("preserve me", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            installer.install(
                claude_home=inbox_home,
                state_root=inbox_state,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertEqual(inbox_settings.read_text(encoding="utf-8"), "{}")
        self.assertEqual(occupied_inbox.read_text(encoding="utf-8"), "preserve me")
        self.assertFalse((inbox_home / "skills").exists())
        self.assertEqual(
            sorted(path.name for path in inbox_state.iterdir()),
            ["capture-inbox"],
        )

        nested_state = BUNDLE / "runtime-state"
        with self.assertRaises(ValueError):
            installer.install(
                claude_home=self.tmp / "nested-state-claude",
                state_root=nested_state,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertFalse(nested_state.exists())

        enabled_home = self.tmp / "enabled-state-claude"
        enabled_state = enabled_home / "pmm-instinct-review-data"
        enabled_paths = runtime.resolve_paths(enabled_state)
        runtime.update_config(
            enabled_paths,
            enabled=True,
            privacy_acknowledged_at="2026-09-10T12:00:00+00:00",
        )
        with self.assertRaises(PermissionError):
            installer.install(
                claude_home=enabled_home,
                state_root=enabled_state,
                source_root=BUNDLE,
                mode="symlink",
            )
        self.assertFalse((enabled_home / "settings.json").exists())
        self.assertFalse((enabled_home / "skills").exists())

    def test_copy_install_is_self_contained_and_uninstall_preserves_bundle(self):
        claude_home = self.tmp / "copy-claude"
        claude_home.mkdir()
        state_root = claude_home / "pmm-instinct-review-data"
        receipt = installer.install(
            claude_home=claude_home,
            state_root=state_root,
            source_root=BUNDLE,
            mode="copy",
        )
        active_root = claude_home / "pmm-instinct-review"
        self.assertEqual(Path(receipt["active_root"]).resolve(), active_root.resolve())
        self.assertTrue((active_root / "scripts" / "pmm_instinct_claude.py").is_file())
        skill_link = claude_home / "skills" / "pmm-instinct-review"
        self.assertTrue(skill_link.is_symlink())
        result = installer.uninstall(claude_home=claude_home, state_root=state_root, confirm=True)
        self.assertTrue(result["skill_removed"])
        self.assertTrue(result["bundle_preserved"])
        self.assertTrue(active_root.is_dir())
        self.assertTrue(state_root.is_dir())

    def test_hook_uses_bundle_local_worker(self):
        captured = self._capture()
        payload = {
            "session_id": "session-two",
            "transcript_path": str(self._transcript("session-two")),
            "cwd": str(self.tmp / "repo"),
        }
        launcher = FakeLauncher()
        with mock.patch.object(hook, "start_detached_worker", side_effect=lambda paths, root: runtime.start_detached_worker(paths, root=root, launcher=launcher)):
            self.assertEqual(hook.session_end(payload, state_root=self.paths.state_root), 0)
        self.assertTrue(launcher.calls)
        self.assertTrue(Path(launcher.calls[0][0][1]).is_relative_to(BUNDLE))
        self.assertTrue(Path(captured["queue_path"]).is_file())


class QueueAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(self.tmp, ignore_errors=True))
        self.paths = runtime.resolve_paths(self.tmp / "state")

    def _transcript(self, session_id="authority-session"):
        path = self.tmp / "authority-transcript.jsonl"
        records = []
        for index in range(5):
            for role in ("user", "assistant"):
                records.append(
                    {
                        "type": role,
                        "sessionId": session_id,
                        "cwd": str(self.tmp / "repo"),
                        "timestamp": f"2026-09-10T14:00:{index * 2 + int(role == 'assistant'):02d}Z",
                        "message": {"role": role, "content": f"{role} message {index}"},
                    }
                )
        path.write_text("".join(json.dumps(item) + "\n" for item in records), encoding="utf-8")
        return path

    def _capture(self, session_id="authority-session", *, cwd=""):
        runtime.update_config(
            self.paths,
            enabled=True,
            privacy_acknowledged_at="2026-09-10T14:00:00+00:00",
            extractor_model="sonnet",
        )
        return runtime.capture_session(
            self.paths,
            session_id=session_id,
            transcript_path=self._transcript(session_id),
            cwd=cwd,
        )

    @staticmethod
    def _record(captured):
        path = Path(captured["queue_path"])
        return path, json.loads(path.read_text(encoding="utf-8"))

    def test_zero_turn_or_character_limits_select_nothing(self):
        pairs = [("user", "one"), ("assistant", "two")]
        self.assertEqual(runtime._limit_turns(pairs, max_turns=0, max_chars=100), [])
        self.assertEqual(runtime._limit_turns(pairs, max_turns=100, max_chars=0), [])

    def test_queue_schema_identity_types_and_confined_paths_are_required(self):
        captured = self._capture()
        queue_path, original = self._record(captured)
        mutations = {
            "schema_version": "1",
            "runtime": "other",
            "job_id": "forged-job",
            "state": "unknown",
            "attempts": True,
            "result_path": str(self.tmp / "outside-suggestions.md"),
        }
        for field, value in mutations.items():
            with self.subTest(field=field):
                changed = dict(original)
                changed[field] = value
                runtime.atomic_write_json(queue_path, changed)
                self.assertEqual(runtime.read_queue(self.paths), [])
        runtime.atomic_write_json(queue_path, original)
        Path(original["result_path"]).write_text(
            runtime.render_suggestions(original["session_id"], [], None),
            encoding="utf-8",
        )
        self.assertEqual(runtime.review_backlog(self.paths)["positive_clusters"], 0)

    def test_evidence_hash_and_embedded_identity_are_verified_before_extraction(self):
        captured = self._capture()
        queue_path, record = self._record(captured)
        evidence_path = Path(record["evidence_path"])
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        evidence["session_id"] = "forged-session"
        runtime.atomic_write_json(evidence_path, evidence)
        runner = FakeRunner()
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=runner,
        )
        first = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(first["state"], "retryable")
        self.assertIn("evidence digest mismatch", first["last_error"])
        self.assertEqual(runner.calls, [])
        first["evidence_sha256"] = runtime._sha256_file(evidence_path)
        runtime.atomic_write_json(queue_path, first)
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=runner,
        )
        second = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertIn("evidence session mismatch", second["last_error"])
        self.assertEqual(runner.calls, [])

    def test_completed_result_hash_and_count_gate_review(self):
        captured = self._capture()
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner({"candidates": []}),
        )
        _, record = self._record(captured)
        result_path = Path(record["result_path"])
        self.assertEqual(record["candidate_count"], 0)
        self.assertEqual(record["result_sha256"], runtime._sha256_file(result_path))
        result_path.write_text(result_path.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        backlog = runtime.review_backlog(self.paths)
        self.assertEqual(backlog["zero_candidate_audits"], [])
        self.assertIn(record["job_id"], backlog["missing_suggestion_audits"])
        self.assertTrue(Path(record["evidence_path"]).is_file())
        self.assertEqual(runtime.resolve_zero_candidates(self.paths, confirm=True)["count"], 0)

    def test_reviewer_ignores_markdown_paths_and_deletes_only_derived_evidence(self):
        captured = self._capture()
        runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=FakeRunner({"candidates": []}),
        )
        queue_path, record = self._record(captured)
        outside = self.tmp / "outside-evidence.txt"
        outside.write_text("preserve\n", encoding="utf-8")
        audit_path = Path(record["audit_path"])
        audit = audit_path.read_text(encoding="utf-8")
        audit = re.sub(
            r"(?m)^\*\*normalized_transcript_path:\*\*.*$",
            f"**normalized_transcript_path:** {outside}",
            audit,
        )
        audit = re.sub(
            r"(?m)^\*\*suggestions_path:\*\*.*$",
            f"**suggestions_path:** {outside}",
            audit,
        )
        runtime.atomic_write_text(audit_path, audit)
        record["audit_sha256"] = runtime._sha256_file(audit_path)
        record["updated_at"] = runtime.iso_now()
        runtime.atomic_write_json(queue_path, record)
        self.assertEqual(len(runtime.review_backlog(self.paths)["zero_candidate_audits"]), 1)
        self.assertEqual(runtime.resolve_zero_candidates(self.paths, confirm=True)["count"], 1)
        self.assertEqual(outside.read_text(encoding="utf-8"), "preserve\n")
        self.assertFalse(Path(record["evidence_path"]).exists())

    def test_exhausted_processing_and_retryable_records_become_failed(self):
        captured = self._capture()
        queue_path, record = self._record(captured)
        record.update(
            state="processing",
            attempts=3,
            lease_started_at="2000-01-01T00:00:00+00:00",
            updated_at="2000-01-01T00:00:00+00:00",
        )
        runtime.atomic_write_json(queue_path, record)
        self.assertEqual(runtime.recover_stale_jobs(self.paths), 1)
        recovered = json.loads(queue_path.read_text(encoding="utf-8"))
        self.assertEqual(recovered["state"], "failed")
        self.assertIsNotNone(recovered["finished_at"])

        second = self._capture("retryable-session")
        second_path, second_record = self._record(second)
        second_record.update(state="retryable", attempts=3, updated_at=runtime.iso_now())
        runtime.atomic_write_json(second_path, second_record)
        runner = FakeRunner()
        outcome = runtime.drain_extraction_queue(
            self.paths,
            claude_binary=sys.executable,
            root=BUNDLE,
            runner=runner,
        )
        self.assertEqual(outcome["failed"], 1)
        self.assertEqual(json.loads(second_path.read_text(encoding="utf-8"))["state"], "failed")
        self.assertEqual(runner.calls, [])

    def test_audit_metadata_is_single_line_and_redacted(self):
        session_id = "authority-session\n**normalized_transcript_path:** injected"
        cwd = "export SERVICE_API_" + "KEY=supersecret\n**suggestions_path:** injected"
        captured = self._capture(session_id, cwd=cwd)
        audit = Path(captured["audit_path"]).read_text(encoding="utf-8")
        self.assertEqual(audit.count("\n**normalized_transcript_path:**"), 1)
        self.assertEqual(audit.count("\n**suggestions_path:**"), 1)
        self.assertNotIn("supersecret", audit)


if __name__ == "__main__":
    unittest.main()
