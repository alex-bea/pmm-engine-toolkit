import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "pmm-instinct-review"
SKILL = PLUGIN / "skills" / "pmm-instinct-review"
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

from pmm_instinct import runtime


def write_transcript(
    path: Path,
    *,
    session_id: str = "session-1",
    cwd: str = "",
    model: str = "gpt-test",
    users: int = 5,
    source=None,
    fallback: bool = False,
) -> None:
    meta = {
        "type": "session_meta",
        "payload": {"id": session_id, "cwd": cwd, "model": model, "timestamp": "2026-08-20T12:00:00Z"},
    }
    if source is not None:
        meta["payload"]["source"] = source
    rows = [meta]
    for index in range(users):
        if fallback:
            rows.extend(
                [
                    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": f"user {index}"}]}},
                    {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": f"assistant {index}"}]}},
                ]
            )
        else:
            rows.extend(
                [
                    {"type": "event_msg", "payload": {"type": "user_message", "message": f"user {index}"}},
                    {"type": "event_msg", "payload": {"type": "agent_message", "message": f"assistant {index}"}},
                ]
            )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def enabled_paths(root: Path, *, model=None):
    paths = runtime.resolve_paths(root)
    runtime.update_config(
        paths,
        enabled=True,
        privacy_acknowledged_at="2026-08-20T00:00:00+00:00",
        extractor_model=model,
    )
    return paths


def capture_with_suggestion(paths, transcript: Path, session_id: str, rule: str, *, candidate_type="workflow", source_skill=None):
    result = runtime.capture_session(
        paths,
        session_id=session_id,
        transcript_path=transcript,
        model="gpt-test",
    )
    queue = json.loads(Path(result["queue_path"]).read_text(encoding="utf-8"))
    runtime.atomic_write_text(
        queue["suggestions_path"],
        runtime.render_suggestions(
            session_id,
            [
                {
                    "type": candidate_type,
                    "rule": rule,
                    "evidence": "User corrected the workflow.",
                    "context": "Repeated work preference.",
                    "why_it_matters": "It prevents the corrected behavior from recurring in later work.",
                }
            ],
            source_skill,
        ),
    )
    return result


class PluginContractTests(unittest.TestCase):
    def test_manifest_and_marketplace_registration(self):
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "pmm-instinct-review")
        self.assertEqual(manifest["version"], "0.1.0")
        self.assertEqual(marketplace["plugins"][0]["name"], "pmm-instinct-review")

    def test_hooks_use_plugin_root_and_both_events(self):
        hooks = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
        self.assertEqual(set(hooks), {"SessionStart", "SessionEnd"})
        commands = [entry["command"] for event in hooks.values() for group in event for entry in group["hooks"]]
        self.assertTrue(all("${PLUGIN_ROOT}" in command for command in commands))
        self.assertTrue(all("~/.codex/hooks.json" not in command for command in commands))

    def test_runtime_is_standard_library_and_public_path_only(self):
        text = "\n".join(path.read_text(encoding="utf-8") for path in SCRIPTS.rglob("*.py"))
        for forbidden in ("import yaml", "from yaml", ".venv", ".claude", "/Us" + "ers/"):
            self.assertNotIn(forbidden, text)

    def test_runtime_state_is_outside_plugin(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = runtime.resolve_paths(tmp)
        self.assertEqual(paths.store, Path(tmp) / "instinct-review")
        self.assertNotIn(str(PLUGIN), str(paths.store))


class NormalizerTests(unittest.TestCase):
    def test_event_messages_are_preferred(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            write_transcript(path, users=1)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": "fallback"}]}}) + "\n")
            result = runtime.normalize_transcript(path)
        self.assertEqual(result.source_format, "codex-rollout-event-msg-v1")
        self.assertNotIn("fallback", [turn.text for turn in result.turns])

    def test_response_item_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            write_transcript(path, users=2, fallback=True)
            result = runtime.normalize_transcript(path)
        self.assertEqual(result.source_format, "codex-rollout-response-item-v1")
        self.assertEqual(result.user_messages, 2)

    def test_non_chat_records_are_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            write_transcript(path, users=1)
            with path.open("a", encoding="utf-8") as handle:
                for kind in ("reasoning", "function_call", "function_call_output", "compaction"):
                    handle.write(json.dumps({"type": "response_item", "payload": {"type": kind, "text": "PRIVATE"}}) + "\n")
            result = runtime.normalize_transcript(path)
        self.assertNotIn("PRIVATE", runtime.serialize_turns(result.turns))

    def test_adjacent_duplicates_are_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            rows = [
                {"type": "session_meta", "payload": {"id": "s"}},
                {"type": "event_msg", "payload": {"type": "user_message", "message": "same"}},
                {"type": "event_msg", "payload": {"type": "user_message", "message": "same"}},
            ]
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            result = runtime.normalize_transcript(path)
        self.assertEqual(len(result.turns), 1)

    def test_context_wrapper_and_secret_redaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            rows = [
                {"type": "session_meta", "payload": {"id": "s"}},
                {"type": "event_msg", "payload": {"type": "user_message", "message": "<environment_context>hidden</environment_context>"}},
                {"type": "event_msg", "payload": {"type": "user_message", "message": "API_" + "TO" + "KEN=secret-value\nBearer abcdefghijklmnop"}},
            ]
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            result = runtime.normalize_transcript(path)
        self.assertEqual(len(result.turns), 1)
        self.assertIn("[REDACTED]", result.turns[0].text)
        self.assertIn("Bearer [REDACTED TOKEN]", result.turns[0].text)
        self.assertNotIn("secret-value", result.turns[0].text)

    def test_context_wrapper_parser_handles_long_adversarial_inputs(self):
        wrappers = " \n".join(
            "<environment_context>hidden</environment_context>" for _ in range(5_000)
        )
        self.assertTrue(runtime._is_context_wrapper_turn(wrappers))
        self.assertFalse(
            runtime._is_context_wrapper_turn(
                "<environment_context>" + (" " * 250_000)
            )
        )
        self.assertFalse(
            runtime._is_context_wrapper_turn(
                "<environment_context>hidden</environment_context> keep this"
            )
        )

    def test_turn_and_character_limits_keep_newest(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rollout.jsonl"
            write_transcript(path, users=5)
            result = runtime.normalize_transcript(path, max_turns=3, max_chars=25)
        self.assertLessEqual(len(result.turns), 3)
        self.assertLessEqual(result.normalized_chars, 25)
        self.assertIn("assistant 4", result.turns[-1].text)

    def test_missing_transcript_raises(self):
        with self.assertRaises(FileNotFoundError):
            runtime.normalize_transcript("/definitely/missing/rollout.jsonl")


class CaptureAndQueueTests(unittest.TestCase):
    def test_default_config_is_disabled(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = runtime.load_config(runtime.resolve_paths(tmp))
        self.assertFalse(config["enabled"])
        self.assertIsNone(config["extractor_model"])

    def test_disabled_capture_creates_no_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            paths = runtime.resolve_paths(root / "codex")
            result = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            self.assertEqual(result["reason"], "disabled")
            self.assertFalse(paths.store.exists())

    def test_below_five_turns_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript, users=4)
            result = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
        self.assertEqual(result["reason"], "below-minimum-user-messages")

    def test_subagent_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript, source={"subagent": "test"})
            result = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
        self.assertEqual(result["reason"], "not-main-thread")

    def test_capture_is_idempotent_and_persists_session_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="gpt-session")
            first = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            second = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            queue = json.loads(Path(first["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(first["status"], "queued")
        self.assertEqual(second["status"], "exists")
        self.assertEqual(queue["extractor_model"], "gpt-session")

    def test_duplicate_session_end_repairs_a_partial_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            first = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            Path(first["queue_path"]).unlink()
            repaired = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            record = json.loads(Path(repaired["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(repaired["reason"], "recovered-partial-capture")
        self.assertTrue(record["recovered"])

    def test_configured_model_overrides_session_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex", model="gpt-configured")
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="gpt-session")
            result = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            queue = json.loads(Path(result["queue_path"]).read_text(encoding="utf-8"))
        self.assertEqual(queue["extractor_model"], "gpt-configured")

    def test_missing_model_fails_without_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="")
            result = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            record = json.loads(Path(result["queue_path"]).read_text(encoding="utf-8"))
            with self.assertRaisesRegex(RuntimeError, "model unavailable"):
                runtime.run_extractor_job(paths, record)

    def test_explicit_codex_resolution_requires_executable(self):
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "codex"
            executable.write_text("#!/bin/sh\n", encoding="utf-8")
            executable.chmod(0o700)
            resolved = runtime.resolve_codex_executable({}, str(executable))
            missing = runtime.resolve_codex_executable({}, str(Path(tmp) / "missing"))
        self.assertEqual(resolved, str(executable))
        self.assertIsNone(missing)

    def test_extractor_schema_allows_zero_and_rejects_bad_output(self):
        self.assertEqual(runtime.validate_extractor_payload({"candidates": []}), [])
        valid = {
            "candidates": [
                {
                    "type": "workflow",
                    "rule": "Use the approved source.",
                    "evidence": "Use the approved source.",
                    "context": "The user corrected the workflow.",
                    "why_it_matters": "It prevents drafting against an unapproved source.",
                }
            ]
        }
        self.assertEqual(runtime.validate_extractor_payload(valid)[0]["why_it_matters"], "It prevents drafting against an unapproved source.")
        with self.assertRaises(ValueError):
            runtime.validate_extractor_payload({"candidates": [{"type": "other", "rule": "x", "evidence": "", "context": ""}]})
        with self.assertRaises(ValueError):
            runtime.validate_extractor_payload(
                {
                    "candidates": [
                        {
                            "type": "workflow",
                            "rule": "x",
                            "evidence": "x",
                            "context": "x",
                            "why_it_matters": "x" * 301,
                        }
                    ]
                }
            )

    def test_blank_skill_field_does_not_consume_the_next_metadata_line(self):
        text = "**skill:** \n**source_runtime:** codex\n"
        fields = runtime._markdown_fields(text)
        self.assertEqual(fields["skill"], "")
        self.assertEqual(fields["source_runtime"], "codex")

    def test_worker_succeeds_with_valid_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)

            def runner(command, **kwargs):
                output = Path(command[command.index("--output-last-message") + 1])
                output.write_text('{"candidates": []}\n', encoding="utf-8")
                return type("Result", (), {"returncode": 0})()

            result = runtime.drain_queue(paths, codex_binary=sys.executable, runner=runner)
            record = runtime.read_queue(paths)[0][1]
        self.assertEqual(result["succeeded"], 1)
        self.assertEqual(record["state"], "succeeded")

    def test_worker_stops_after_three_failures_and_manual_retry_resets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)

            def runner(command, **kwargs):
                return type("Result", (), {"returncode": 2})()

            for _ in range(4):
                runtime.drain_queue(paths, codex_binary=sys.executable, runner=runner)
            record = runtime.read_queue(paths)[0][1]
            self.assertEqual(record["attempts"], 3)
            self.assertEqual(runtime.retry_failed(paths), 1)
            reset = runtime.read_queue(paths)[0][1]
        self.assertEqual(reset["state"], "queued")
        self.assertEqual(reset["attempts"], 0)

    def test_live_and_stale_worker_locks(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = enabled_paths(Path(tmp))
            first = runtime.worker_lock(paths)
            self.assertIsNotNone(first)
            self.assertIsNone(runtime.worker_lock(paths))
            first.unlink()
            stale = paths.state / "worker.lock"
            stale.write_text('{"pid": 99999999}', encoding="utf-8")
            recovered = runtime.worker_lock(paths)
            self.assertIsNotNone(recovered)
            recovered.unlink()

    def test_running_job_is_recovered_after_worker_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            queue_path = Path(captured["queue_path"])
            record = json.loads(queue_path.read_text(encoding="utf-8"))
            runtime.transition_queue(queue_path, record, state="running", attempts=1)

            def runner(command, **kwargs):
                output = Path(command[command.index("--output-last-message") + 1])
                output.write_text('{"candidates": []}\n', encoding="utf-8")
                return type("Result", (), {"returncode": 0})()

            receipt = runtime.drain_queue(paths, codex_binary=sys.executable, runner=runner)
        self.assertEqual(receipt["succeeded"], 1)

    def test_dynamic_skill_discovery_and_explicit_derivation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "codex" / "skills" / "demo-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: demo-skill\ndescription: demo\n---\n", encoding="utf-8")
            paths = runtime.resolve_paths(root / "codex")
            found = runtime.discover_skills(paths)
            source = runtime.derive_source_skill([runtime.Turn(1, "user", "Use $demo-skill")], found)
        self.assertIn("demo-skill", found)
        self.assertEqual(source, "demo-skill")


class ReviewAndPromotionTests(unittest.TestCase):
    def test_accept_requires_confirmation_and_deletes_only_normalized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            captured = capture_with_suggestion(paths, transcript, "session-1", "Lead with the decision.")
            selected = runtime.clusters(paths)[0]
            with self.assertRaises(PermissionError):
                runtime.review_cluster(paths, selected.cluster_id, "accept")
            receipt = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            self.assertTrue(transcript.exists())
            self.assertFalse(Path(captured["normalized_path"]).exists())
            self.assertTrue(Path(receipt["instinct_path"]).exists())

    def test_reject_creates_no_instinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            capture_with_suggestion(paths, transcript, "session-1", "Use one summary.")
            selected = runtime.clusters(paths)[0]
            runtime.review_cluster(paths, selected.cluster_id, "reject", confirm=True)
        self.assertEqual(runtime.load_instincts(paths), [])

    def test_exact_duplicate_requires_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            first = root / "first.jsonl"
            write_transcript(first, session_id="one")
            capture_with_suggestion(paths, first, "one", "Use one summary.")
            selected = runtime.clusters(paths)[0]
            runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            second = root / "second.jsonl"
            write_transcript(second, session_id="two")
            capture_with_suggestion(paths, second, "two", "Use one summary.")
            selected = runtime.clusters(paths)[0]
            self.assertEqual(selected.match_state, "exact")
            with self.assertRaisesRegex(ValueError, "use match"):
                runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            runtime.review_cluster(paths, selected.cluster_id, "match", confirm=True)
            self.assertEqual(runtime.load_instincts(paths)[0].seen_count, 2)

    def test_confidence_reaches_promotion_threshold_at_three_supports(self):
        self.assertLess(runtime.confidence_for_support(2), 0.5)
        self.assertEqual(runtime.confidence_for_support(3), 0.5)

    def test_candidate_card_uses_rationale_without_routing_and_persists_source_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript, cwd=str(repo))
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript, model="gpt-test")
            record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
            runtime.atomic_write_text(
                record["suggestions_path"],
                runtime.render_suggestions(
                    "session-1",
                    [{"type": "workflow", "rule": "Use the approved source.", "evidence": "Use the approved source.", "context": "The owner corrected the workflow."}],
                    "demo-skill",
                ),
            )
            queue = runtime.backlog(paths)
            card = queue["clusters"][0]["candidate_card"]
            self.assertEqual(card["what_happened"], "The owner corrected the workflow.")
            self.assertEqual(card["your_feedback"], "Use the approved source.")
            self.assertEqual(card["proposed_future_behavior"], "Use the approved source.")
            self.assertEqual(card["why_it_matters"], runtime.LEGACY_RATIONALE)
            self.assertNotIn("destination", card)
            receipt = runtime.review_cluster(paths, queue["clusters"][0]["cluster_id"], "accept", confirm=True)
            instinct = runtime.load_instincts(paths)[0]
            instinct_path_exists = Path(receipt["instinct_path"]).exists()
        self.assertTrue(instinct_path_exists)
        self.assertEqual(instinct.why_it_matters, runtime.LEGACY_RATIONALE)
        self.assertEqual(instinct.source_skills, ("demo-skill",))
        self.assertEqual(tuple(path.resolve() for path in instinct.source_repositories), (repo.resolve(),))

    def test_edit_can_update_the_persisted_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            capture_with_suggestion(paths, transcript, "session-1", "Use one summary.")
            selected = runtime.clusters(paths)[0]
            runtime.review_cluster(
                paths,
                selected.cluster_id,
                "edit",
                edited_rule="Use one approved summary.",
                edited_rationale="It keeps the deliverable aligned with the approved scope.",
                confirm=True,
            )
            instinct = runtime.load_instincts(paths)[0]
        self.assertEqual(instinct.rule, "Use one approved summary.")
        self.assertEqual(instinct.why_it_matters, "It keeps the deliverable aligned with the approved scope.")

    def test_promotion_preview_and_second_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            paths = enabled_paths(root / "codex")
            for index in range(3):
                transcript = root / f"{index}.jsonl"
                write_transcript(transcript, session_id=f"session-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"session-{index}", "Put the decision first.")
            selected = runtime.clusters(paths)[0]
            receipt = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(receipt["instinct_path"]).stem
            selection = runtime.promotion_preview(paths, instinct_id)
            self.assertEqual(selection["decision"], "select-destination")
            with self.assertRaisesRegex(PermissionError, "matching destination preview"):
                runtime.apply_promotion(paths, instinct_id, destination="project", confirm=True)
            preview = runtime.promotion_preview(paths, instinct_id, destination="project")
            self.assertEqual(Path(preview["targets"][0]["path"]), (repo / "AGENTS.md").resolve())
            with self.assertRaises(PermissionError):
                runtime.apply_promotion(paths, instinct_id, destination="project")
            applied = runtime.apply_promotion(paths, instinct_id, destination="project", confirm=True)
            duplicate = runtime.promotion_preview(paths, instinct_id, destination="project")
            covered = runtime.apply_promotion(paths, instinct_id, destination="project", confirm=True)
            self.assertTrue(applied["applied"])
            self.assertTrue(duplicate["targets"][0]["duplicate"])
            self.assertEqual(covered["changed"], [])
            self.assertEqual(covered["covered"], [str((repo / "AGENTS.md").resolve())])
            self.assertIn(runtime.PROMOTED_GUIDANCE_HEADING, (repo / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual((repo / "AGENTS.md").stat().st_mode & 0o777, 0o644)

    def test_low_confidence_cannot_promote(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "one.jsonl"
            write_transcript(transcript)
            capture_with_suggestion(paths, transcript, "session-1", "Use one summary.")
            selected = runtime.clusters(paths)[0]
            receipt = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            with self.assertRaisesRegex(ValueError, "not eligible"):
                runtime.promotion_preview(paths, Path(receipt["instinct_path"]).stem)

    def test_legacy_candidate_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = runtime.resolve_paths(root / "codex")
            source = root / "candidates.json"
            source.write_text(json.dumps([{"id": "c1", "lesson": "Lead with the decision.", "source": "retro.md", "observed_on": "2026-08-18", "evidence": ["line 10"]}]), encoding="utf-8")
            with self.assertRaises(PermissionError):
                runtime.import_candidates(paths, source)
            receipt = runtime.import_candidates(paths, source, confirm=True)
            self.assertEqual(len(receipt["imported"]), 1)
            self.assertEqual(len(runtime.clusters(paths)), 1)

    def test_cleanup_retries_processed_transcript_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            captured = capture_with_suggestion(paths, transcript, "session-1", "Use one summary.")
            audit = runtime.find_audits(paths)[0]
            runtime.mark_audit_processed(audit)
            receipt = runtime.cleanup_processed(paths)
        self.assertEqual(receipt["removed"], 1)
        self.assertFalse(Path(captured["normalized_path"]).exists())

    def test_every_candidate_in_an_audit_needs_a_decision_before_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript, model="gpt-test")
            record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
            suggestions = [
                {"type": "workflow", "rule": "Lead with the decision.", "evidence": "a", "context": "a"},
                {"type": "scope", "rule": "Keep the first release narrow.", "evidence": "b", "context": "b"},
            ]
            runtime.atomic_write_text(record["suggestions_path"], runtime.render_suggestions("session-1", suggestions, None))
            first, second = runtime.clusters(paths)
            runtime.review_cluster(paths, first.cluster_id, "reject", confirm=True)
            self.assertTrue(Path(captured["normalized_path"]).exists())
            self.assertFalse(runtime.find_audits(paths)[0].processed)
            runtime.review_cluster(paths, second.cluster_id, "reject", confirm=True)
            self.assertFalse(Path(captured["normalized_path"]).exists())
            self.assertTrue(runtime.find_audits(paths)[0].processed)

    def test_zero_candidate_audits_have_explicit_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = root / "native.jsonl"
            write_transcript(transcript)
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript, model="gpt-test")
            record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))
            runtime.atomic_write_text(record["suggestions_path"], runtime.render_suggestions("session-1", [], None))
            with self.assertRaises(PermissionError):
                runtime.resolve_zero_candidate_audits(paths)
            receipt = runtime.resolve_zero_candidate_audits(paths, confirm=True)
        self.assertEqual(receipt["resolved"], 1)

    def test_cross_repository_default_is_global_and_both_is_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            repositories = [root / "one", root / "two"]
            for repository in repositories:
                (repository / ".git").mkdir(parents=True)
            for index in range(3):
                transcript = root / f"cross-{index}.jsonl"
                cwd = repositories[index % 2]
                write_transcript(transcript, session_id=f"cross-{index}", cwd=str(cwd))
                capture_with_suggestion(paths, transcript, f"cross-{index}", "Use the same review gate.")
            selected = runtime.clusters(paths)[0]
            accepted = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(accepted["instinct_path"]).stem
            preview = runtime.promotion_preview(paths, instinct_id, destination="global")
            self.assertEqual(preview["decision"], "global")
            both = runtime.promotion_preview(paths, instinct_id, destination="both", project=repositories[0])
            applied = runtime.apply_promotion(paths, instinct_id, destination="both", project=repositories[0], confirm=True)
            self.assertEqual(len(both["targets"]), 2)
            self.assertEqual(len(applied["changed"]), 2)
            self.assertTrue(all(runtime.PROMOTED_GUIDANCE_HEADING in Path(item["path"]).read_text(encoding="utf-8") for item in both["targets"]))

    def test_skill_promotion_uses_one_writable_user_skill_not_plugin_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            user_skill = paths.codex_home / "skills" / "demo-skill"
            (user_skill / "references").mkdir(parents=True)
            (user_skill / "SKILL.md").write_text("---\nname: demo-skill\ndescription: demo\n---\n", encoding="utf-8")
            (user_skill / "references" / "RUN-demo.md").write_text("# Demo workflow\n", encoding="utf-8")
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            for index in range(3):
                transcript = root / f"skill-{index}.jsonl"
                write_transcript(transcript, session_id=f"skill-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"skill-{index}", "Always use the demo template.", source_skill="demo-skill")
            selected = runtime.clusters(paths)[0]
            accepted = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            preview = runtime.promotion_preview(paths, Path(accepted["instinct_path"]).stem, destination="run")
        self.assertEqual(Path(preview["targets"][0]["path"]), (user_skill / "references" / "RUN-demo.md").resolve())

    def test_voice_ref_promotion_requires_an_explicit_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            user_skill = paths.codex_home / "skills" / "voice-skill"
            (user_skill / "references").mkdir(parents=True)
            (user_skill / "SKILL.md").write_text("---\nname: voice-skill\ndescription: demo\n---\n", encoding="utf-8")
            ref = user_skill / "references" / "REF-voice.md"
            ref.write_text("# Voice\n", encoding="utf-8")
            runtime.update_config(paths, voice_ref_routes={"voice-skill": "references/REF-voice.md"})
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            for index in range(3):
                transcript = root / f"voice-{index}.jsonl"
                write_transcript(transcript, session_id=f"voice-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"voice-{index}", "Use the established framing.", candidate_type="voice", source_skill="voice-skill")
            selected = runtime.clusters(paths)[0]
            accepted = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(accepted["instinct_path"]).stem
            preview = runtime.promotion_preview(paths, instinct_id, destination="ref")
            runtime.apply_promotion(paths, instinct_id, destination="ref", confirm=True)
            expected_ref = ref.resolve()
            ref_contains_guidance = runtime.PROMOTED_GUIDANCE_HEADING in ref.read_text(encoding="utf-8")
        self.assertEqual(Path(preview["targets"][0]["path"]), expected_ref)
        self.assertTrue(ref_contains_guidance)

    def test_unmapped_voice_ref_is_unavailable_and_never_guessed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            user_skill = paths.codex_home / "skills" / "voice-skill"
            (user_skill / "references").mkdir(parents=True)
            (user_skill / "SKILL.md").write_text("---\nname: voice-skill\ndescription: demo\n---\n", encoding="utf-8")
            (user_skill / "references" / "REF-voice.md").write_text("# Voice\n", encoding="utf-8")
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            for index in range(3):
                transcript = root / f"voice-unmapped-{index}.jsonl"
                write_transcript(transcript, session_id=f"voice-unmapped-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"voice-unmapped-{index}", "Use the established framing.", candidate_type="voice", source_skill="voice-skill")
            selected = runtime.clusters(paths)[0]
            accepted = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(accepted["instinct_path"]).stem
            selection = runtime.promotion_preview(paths, instinct_id)
            with self.assertRaisesRegex(ValueError, "mapped voice REF"):
                runtime.promotion_preview(paths, instinct_id, destination="ref")
        self.assertNotIn("ref", selection["available_destinations"])

    def test_standard_promotion_needs_three_source_skills_and_a_supporting_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            standard = repo / "docs" / "STD-review.md"
            standard.parent.mkdir()
            standard.write_text("# Review standard\n", encoding="utf-8")
            for index in range(3):
                source_skill = f"skill-{index}"
                skill = paths.codex_home / "skills" / source_skill
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: {source_skill}\ndescription: demo\n---\n", encoding="utf-8")
                transcript = root / f"standard-{index}.jsonl"
                write_transcript(transcript, session_id=f"standard-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"standard-{index}", "Keep promotion review explicit.", source_skill=source_skill)
            selected = runtime.clusters(paths)[0]
            accepted = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(accepted["instinct_path"]).stem
            preview = runtime.promotion_preview(paths, instinct_id, destination="standard", standard=standard)
            runtime.apply_promotion(paths, instinct_id, destination="standard", standard=standard, confirm=True)
            expected_standard = standard.resolve()
            standard_contains_guidance = runtime.PROMOTED_GUIDANCE_HEADING in standard.read_text(encoding="utf-8")
        self.assertEqual(Path(preview["targets"][0]["path"]), expected_standard)
        self.assertTrue(standard_contains_guidance)


class BackfillTests(unittest.TestCase):
    def test_backfill_dry_inventory_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            transcript = paths.codex_home / "sessions" / "2026" / "session.jsonl"
            write_transcript(transcript, session_id="backfill-1")
            old = runtime.utc_now().timestamp() - 3600
            os.utime(transcript, (old, old))
            inventory = runtime.discover_backfill(paths, limit=5, older_than_minutes=30)
            self.assertEqual([item["session_id"] for item in inventory], ["backfill-1"])
            applied = runtime.apply_backfill(paths, inventory)
            self.assertEqual(applied[0]["status"], "queued")
            self.assertEqual(runtime.discover_backfill(paths, limit=5, older_than_minutes=30), [])

    def test_imported_state_survives_independent_plugin_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = enabled_paths(Path(tmp) / "codex")
            marker = paths.state / "preserved"
            marker.write_text("state\n", encoding="utf-8")
            self.assertTrue(marker.is_file())
            self.assertNotIn(str(PLUGIN), str(marker))


if __name__ == "__main__":
    unittest.main()
