import io
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
from pmm_instinct.adapters import resolve_adapter
import instinct_review as instinct_cli


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


def enabled_paths(root: Path, *, model="gpt-adopter-test"):
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


def write_candidate_audit(
    paths,
    *,
    session_id: str,
    day: str,
    candidate_type: str,
    rule: str,
    source_skill: str = "",
    cwd: str = "",
):
    paths.sessions.mkdir(parents=True, exist_ok=True)
    suggestions = paths.sessions / f"{session_id}-suggestions.md"
    runtime.atomic_write_text(
        suggestions,
        runtime.render_suggestions(
            session_id,
            [
                {
                    "type": candidate_type,
                    "rule": rule,
                    "evidence": "The user corrected the proposed structure.",
                    "context": "A recurring fictional report was under review.",
                    "why_it_matters": "The correction prevents the same structural error from recurring.",
                }
            ],
            source_skill or None,
        ),
    )
    audit = paths.sessions / f"{day}-1200-{session_id}-audit.md"
    runtime.atomic_write_text(
        audit,
        "\n".join(
            [
                "processed: false",
                f"**session_id:** {session_id}",
                f"**suggestions_path:** {suggestions}",
                f"**cwd:** {cwd}",
                f"**skill:** {source_skill}",
                "",
            ]
        ),
    )
    return audit


def invoke_cli(*arguments: object) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    argv = [str(SCRIPTS / "instinct_review.py"), *(str(argument) for argument in arguments)]
    with mock.patch.object(sys, "argv", argv), mock.patch.object(sys, "stdout", stdout), mock.patch.object(
        sys, "stderr", stderr
    ):
        code = instinct_cli.main()
    return code, stdout.getvalue(), stderr.getvalue()


def write_skill(paths, slug: str, references: dict[str, str]) -> Path:
    skill = paths.codex_home / "skills" / slug
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {slug}\ndescription: Fictional test skill.\n---\n",
        encoding="utf-8",
    )
    for relative, content in references.items():
        destination = skill / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    return skill


def accepted_instinct_id(
    paths,
    root: Path,
    *,
    source_skill: str,
    candidate_type: str = "workflow",
    rule: str = "Use the approved fictional workflow.",
) -> str:
    repository = root / "supporting-repository"
    (repository / ".git").mkdir(parents=True, exist_ok=True)
    for index in range(3):
        write_candidate_audit(
            paths,
            session_id=f"{source_skill}-{candidate_type}-{index}",
            day=f"2026-09-{index + 1:02d}",
            candidate_type=candidate_type,
            rule=rule,
            source_skill=source_skill,
            cwd=str(repository),
        )
    selected = runtime.clusters(paths)[0]
    receipt = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
    return Path(receipt["instinct_path"]).stem


class PluginContractTests(unittest.TestCase):
    def test_manifest_and_marketplace_registration(self):
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "pmm-instinct-review")
        self.assertEqual(manifest["version"], "0.3.1")
        entries = [entry for entry in marketplace["plugins"] if entry["name"] == "pmm-instinct-review"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["source"]["path"], "./plugins/pmm-instinct-review")
        catalog = (ROOT / "docs" / "SKILL-CATALOG.md").read_text(encoding="utf-8")
        self.assertIn("`pmm-instinct-review` (`0.3.1` draft)", catalog)
        self.assertIn("native Codex or Claude Code hooks", catalog)

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

    def test_templates_and_complete_fictional_lifecycle_are_bundled(self):
        assets = SKILL / "assets"
        example = SKILL / "examples" / "fictional-northstar-reports"
        expected_assets = {
            "config-template.json",
            "state-contracts.md",
            "instinct-template.md",
            "output-template.md",
        }
        expected_examples = {
            "README.md",
            "config.json",
            "normalized.jsonl",
            "audit.md",
            "queue.json",
            "suggestions.md",
            "status.json",
            "priority-snapshot.json",
            "bucket-summary.md",
            "candidate-card.md",
            "instinct.md",
            "promotion-preview.json",
            "installation-receipt.json",
            "AGENTS-before.md",
            "AGENTS-after.md",
        }
        self.assertTrue(expected_assets <= {path.name for path in assets.iterdir()})
        self.assertEqual(expected_examples, {path.name for path in example.iterdir() if path.is_file()})
        self.assertTrue((example / "claude").is_dir())
        for path in example.iterdir():
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
        before = (example / "AGENTS-before.md").read_text(encoding="utf-8")
        after = (example / "AGENTS-after.md").read_text(encoding="utf-8")
        expected = runtime._render_guidance_update(
            before,
            "- Lead recurring decision reports with the decision and supporting evidence before chronology.",
        )
        self.assertEqual(after, expected)

    def test_fictional_preview_signature_and_cluster_score_recompute(self):
        example = SKILL / "examples" / "fictional-northstar-reports"
        preview = json.loads((example / "promotion-preview.json").read_text(encoding="utf-8"))
        self.assertEqual(preview["signature"], runtime._preview_signature(preview))
        snapshot = json.loads((example / "priority-snapshot.json").read_text(encoding="utf-8"))
        cluster = snapshot["areas"][0]["clusters"][0]
        expected_score = runtime.TYPE_WEIGHTS[cluster["type"]] + cluster["support_count"] + 2
        self.assertEqual(cluster["impact_score"], expected_score)
        self.assertEqual(cluster["cluster_id"], runtime.cluster_id(cluster["type"], cluster["normalized_rule"]))


class AdapterTests(unittest.TestCase):
    def test_portable_adapter_requires_an_explicit_isolated_root(self):
        with self.assertRaisesRegex(ValueError, "explicit --state-root"):
            resolve_adapter("portable")
        with self.assertRaisesRegex(ValueError, "native agent store"):
            resolve_adapter("portable", state_root=Path.home() / ".codex" / "instinct-review")
        with tempfile.TemporaryDirectory() as tmp:
            adapter = resolve_adapter("portable", state_root=Path(tmp) / "review-state")
            self.assertFalse(adapter.capture_supported)
            self.assertEqual(adapter.paths.store, (Path(tmp) / "review-state").resolve())

    def test_portable_status_is_read_only_and_capture_commands_are_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            adapter = resolve_adapter("portable", state_root=Path(tmp) / "review-state")
            receipt = runtime.runtime_status(adapter.paths)
            self.assertFalse(adapter.paths.store.exists())
            self.assertEqual(receipt["active_instincts"], 0)
            for command in ("on", "hook", "backfill", "worker", "retry", "promote"):
                with self.assertRaisesRegex(PermissionError, "review-only"):
                    adapter.require_command(command)

    def test_portable_import_and_review_never_touch_codex_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex_marker = root / "codex-state" / "marker"
            codex_marker.parent.mkdir()
            codex_marker.write_text("unchanged\n", encoding="utf-8")
            adapter = resolve_adapter("portable", state_root=root / "portable-state")
            source = root / "candidates.json"
            source.write_text(
                json.dumps(
                    [
                        {
                            "id": "fictional-1",
                            "lesson": "Lead with the decision.",
                            "source": "fictional-review.md",
                            "observed_on": "2026-09-01",
                            "evidence": ["The user corrected the order."],
                            "type": "workflow",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            receipt = runtime.import_candidates(
                adapter.paths,
                source,
                source_runtime=adapter.name,
                confirm=True,
            )
            cluster = runtime.clusters(adapter.paths)[0]
            reviewed = runtime.review_cluster(
                adapter.paths,
                cluster.cluster_id,
                "accept",
                source_runtime=adapter.name,
                confirm=True,
            )
            instinct = runtime.load_instincts(adapter.paths)[0]
            self.assertEqual(receipt["errors"], [])
            self.assertTrue(Path(reviewed["instinct_path"]).is_file())
            self.assertEqual(instinct.source_runtime, "portable")
            self.assertEqual(codex_marker.read_text(encoding="utf-8"), "unchanged\n")


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
        self.assertEqual(config["run_routes"], {})
        self.assertEqual(config["voice_ref_routes"], {})

    def test_first_enablement_requires_and_persists_one_trimmed_model_before_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex_home = root / "codex"
            observed = {}

            def inspect_preflight(paths, **_kwargs):
                config = runtime.load_config(paths)
                observed.update(model=config["extractor_model"], enabled=config["enabled"])
                return {
                    "ok": True,
                    "checks": {"python": True, "codex": True, "extractor_schema": True, "model_policy": True},
                    "codex_binary": sys.executable,
                    "extractor_model": config["extractor_model"],
                }

            with mock.patch.object(instinct_cli, "preflight", side_effect=inspect_preflight):
                code, stdout, stderr = invoke_cli(
                    "--codex-home",
                    codex_home,
                    "on",
                    "--acknowledge-local-chat-storage",
                    "--model",
                    "  gpt-adopter-selected  ",
                    "--codex-binary",
                    sys.executable,
                )
            config = runtime.load_config(runtime.resolve_paths(codex_home))

        self.assertEqual((code, stderr), (0, ""))
        self.assertIn('"enabled": true', stdout)
        self.assertEqual(observed, {"model": "gpt-adopter-selected", "enabled": False})
        self.assertTrue(config["enabled"])
        self.assertEqual(config["extractor_model"], "gpt-adopter-selected")

    def test_first_enablement_without_model_and_explicit_whitespace_model_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "codex-bin"
            executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            executable.chmod(0o700)
            for suffix, model_arguments in (("missing", ()), ("blank", ("--model", "   "))):
                with self.subTest(case=suffix):
                    codex_home = root / suffix
                    code, _stdout, stderr = invoke_cli(
                        "--codex-home",
                        codex_home,
                        "on",
                        "--acknowledge-local-chat-storage",
                        "--codex-binary",
                        executable,
                        *model_arguments,
                    )
                    config = runtime.load_config(runtime.resolve_paths(codex_home))
                    self.assertEqual(code, 1)
                    self.assertIn("model", stderr.lower())
                    self.assertFalse(config["enabled"])
                    self.assertIsNone(config["extractor_model"])

    def test_existing_persisted_model_can_be_reused_on_later_enablement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            executable = root / "codex-bin"
            executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            executable.chmod(0o700)
            codex_home = root / "codex"
            paths = runtime.resolve_paths(codex_home)
            runtime.update_config(
                paths,
                enabled=False,
                privacy_acknowledged_at="2026-09-11T00:00:00+00:00",
                extractor_model="gpt-persisted",
                codex_binary=str(executable),
            )
            code, _stdout, stderr = invoke_cli("--codex-home", codex_home, "on")
            config = runtime.load_config(paths)

        self.assertEqual((code, stderr), (0, ""))
        self.assertTrue(config["enabled"])
        self.assertEqual(config["extractor_model"], "gpt-persisted")

    def test_legacy_enabled_null_model_repair_stays_disabled_when_preflight_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex"
            paths = runtime.resolve_paths(codex_home)
            runtime.ensure_store(paths)
            legacy = dict(runtime.DEFAULT_CONFIG)
            legacy.update(
                enabled=True,
                privacy_acknowledged_at="2026-09-11T00:00:00+00:00",
                extractor_model=None,
            )
            runtime.atomic_write_json(paths.config, legacy)

            def failed_preflight(observed_paths, **_kwargs):
                observed = runtime.load_config(observed_paths)
                self.assertFalse(observed["enabled"])
                self.assertEqual(observed["extractor_model"], "gpt-repaired")
                return {
                    "ok": False,
                    "checks": {
                        "python": True,
                        "codex": False,
                        "extractor_schema": True,
                        "model_policy": True,
                    },
                    "codex_binary": None,
                    "extractor_model": "gpt-repaired",
                }

            with mock.patch.object(instinct_cli, "preflight", side_effect=failed_preflight):
                code, _stdout, stderr = invoke_cli(
                    "--codex-home",
                    codex_home,
                    "on",
                    "--model",
                    "gpt-repaired",
                )
            config = runtime.load_config(paths)

        self.assertEqual(code, 1)
        self.assertIn("preflight failed", stderr)
        self.assertFalse(config["enabled"])
        self.assertEqual(config["extractor_model"], "gpt-repaired")

    def test_null_model_preflight_and_status_fail_without_rewriting_legacy_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = runtime.resolve_paths(Path(tmp) / "codex")
            runtime.ensure_store(paths)
            legacy = dict(runtime.DEFAULT_CONFIG)
            legacy.pop("run_routes")
            legacy.update(
                enabled=True,
                privacy_acknowledged_at="2026-09-11T00:00:00+00:00",
                extractor_model=None,
            )
            runtime.atomic_write_json(paths.config, legacy)
            before = paths.config.read_bytes()
            receipt = runtime.preflight(paths, codex_binary=sys.executable)
            status = runtime.runtime_status(paths)
            after = paths.config.read_bytes()

        self.assertFalse(receipt["ok"])
        self.assertFalse(receipt["checks"]["model_policy"])
        self.assertFalse(status["preflight"]["ok"])
        self.assertIn("on --model <model>", json.dumps(status))
        self.assertEqual(after, before)

    def test_preflight_supports_documented_python_310_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = enabled_paths(Path(tmp) / "codex", model="gpt-configured")
            with mock.patch.object(runtime.sys, "version_info", (3, 10, 0)):
                supported = runtime.preflight(paths, codex_binary=sys.executable)
            with mock.patch.object(runtime.sys, "version_info", (3, 9, 18)):
                unsupported = runtime.preflight(paths, codex_binary=sys.executable)

        self.assertTrue(supported["checks"]["python"])
        self.assertTrue(supported["ok"])
        self.assertFalse(unsupported["checks"]["python"])
        self.assertFalse(unsupported["ok"])

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

    def test_capture_is_idempotent_and_uses_persisted_model_not_transcript_model(self):
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
        self.assertEqual(queue["extractor_model"], "gpt-adopter-test")

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

    def test_hook_job_uses_configured_model_over_event_and_transcript_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex", model="gpt-configured")
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="gpt-transcript")
            payload = {
                "session_id": "session-1",
                "transcript_path": str(transcript),
                "cwd": str(root),
                "model": "gpt-event",
            }
            with mock.patch.object(instinct_cli, "_read_hook_payload", return_value=payload), mock.patch.object(
                instinct_cli, "start_detached_worker"
            ) as start_worker:
                self.assertEqual(instinct_cli._session_end(paths), 0)
            queue = runtime.read_queue(paths)[0][1]
        self.assertEqual(queue["extractor_model"], "gpt-configured")
        start_worker.assert_called_once()

    def test_legacy_enabled_null_model_skips_capture_without_writing_even_with_metadata_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = runtime.resolve_paths(root / "codex")
            runtime.ensure_store(paths)
            config = dict(runtime.DEFAULT_CONFIG)
            config.update(
                enabled=True,
                privacy_acknowledged_at="2026-09-11T00:00:00+00:00",
                extractor_model=None,
            )
            runtime.atomic_write_json(paths.config, config)
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="gpt-transcript")
            before_config = paths.config.read_bytes()
            before_transcript = transcript.read_bytes()
            result = runtime.capture_session(
                paths,
                session_id="session-1",
                transcript_path=transcript,
                model="gpt-event",
            )
            session_files = list(paths.sessions.iterdir())
            queue_files = list(paths.queue.iterdir())
            after_config = paths.config.read_bytes()
            after_transcript = transcript.read_bytes()

        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["reason"], "unconfigured_model")
        self.assertEqual(result["session_id"], "session-1")
        self.assertEqual(session_files, [])
        self.assertEqual(queue_files, [])
        self.assertEqual(after_config, before_config)
        self.assertEqual(after_transcript, before_transcript)

    def test_existing_explicit_model_queue_drains_after_config_becomes_legacy_null(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex", model="gpt-queued")
            transcript = root / "session.jsonl"
            write_transcript(transcript, model="gpt-transcript")
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            config = json.loads(paths.config.read_text(encoding="utf-8"))
            config["extractor_model"] = None
            runtime.atomic_write_json(paths.config, config)
            commands = []

            def runner(command, **_kwargs):
                commands.append(command)
                output = Path(command[command.index("--output-last-message") + 1])
                output.write_text('{"candidates": []}\n', encoding="utf-8")
                return type("Result", (), {"returncode": 0})()

            receipt = runtime.drain_queue(paths, codex_binary=sys.executable, runner=runner)
            record = json.loads(Path(captured["queue_path"]).read_text(encoding="utf-8"))

        self.assertEqual(receipt["succeeded"], 1)
        self.assertEqual(record["state"], "succeeded")
        self.assertEqual(commands[0][commands[0].index("--model") + 1], "gpt-queued")

    def test_malformed_queue_model_types_fail_closed_before_extractor_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = enabled_paths(Path(tmp) / "codex", model="gpt-configured")
            for malformed in (True, 42, ["gpt-not-a-string"], {"model": "gpt-not-a-string"}):
                with self.subTest(malformed=malformed), self.assertRaisesRegex(
                    RuntimeError, "model unavailable"
                ):
                    runtime.run_extractor_job(
                        paths,
                        {"extractor_model": malformed},
                        runner=mock.Mock(side_effect=AssertionError("extractor must not run")),
                    )

    def test_legacy_empty_model_queue_fails_and_retry_does_not_claim_model_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex", model="gpt-current")
            transcript = root / "session.jsonl"
            write_transcript(transcript)
            captured = runtime.capture_session(paths, session_id="session-1", transcript_path=transcript)
            queue_path = Path(captured["queue_path"])
            record = json.loads(queue_path.read_text(encoding="utf-8"))
            record["extractor_model"] = ""
            runtime.atomic_write_json(queue_path, record)
            receipt = runtime.drain_queue(paths, codex_binary=sys.executable)
            self.assertEqual(runtime.retry_failed(paths, "session-1"), 0)
            retried = json.loads(queue_path.read_text(encoding="utf-8"))

        self.assertEqual(receipt["failed"], 1)
        self.assertEqual(retried["state"], "failed")
        self.assertEqual(retried["extractor_model"], "")

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

    def test_exact_match_requires_type_and_normalized_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            first = root / "workflow.jsonl"
            write_transcript(first, session_id="workflow")
            capture_with_suggestion(paths, first, "workflow", "Use one summary.", candidate_type="workflow")
            cluster = runtime.clusters(paths)[0]
            runtime.review_cluster(paths, cluster.cluster_id, "accept", confirm=True)
            second = root / "correction.jsonl"
            write_transcript(second, session_id="correction")
            capture_with_suggestion(paths, second, "correction", "Use one summary.", candidate_type="correction")
            cluster = runtime.clusters(paths)[0]
            self.assertEqual(cluster.match_state, "new")
            runtime.review_cluster(paths, cluster.cluster_id, "accept", confirm=True)
            self.assertEqual({item.instinct_type for item in runtime.load_instincts(paths)}, {"workflow", "correction"})

    def test_priority_is_voice_first_then_breadth_newness_and_recency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = runtime.resolve_paths(root / "codex")
            repo_one = root / "one"
            repo_two = root / "two"
            (repo_one / ".git").mkdir(parents=True)
            (repo_two / ".git").mkdir(parents=True)
            for index, (skill, cwd, day) in enumerate(
                (("skill-a", repo_one, "2026-08-20"), ("skill-b", repo_two, "2026-08-21")),
                start=1,
            ):
                write_candidate_audit(
                    paths,
                    session_id=f"broad-{index}",
                    day=day,
                    candidate_type="workflow",
                    rule="Use one approved outline.",
                    source_skill=skill,
                    cwd=str(cwd),
                )
            write_candidate_audit(
                paths,
                session_id="voice-1",
                day="2026-08-01",
                candidate_type="voice",
                rule="Use plain language.",
                cwd=str(repo_one),
            )
            write_candidate_audit(
                paths,
                session_id="scope-old",
                day="2026-08-10",
                candidate_type="scope",
                rule="Keep the release narrow.",
            )
            write_candidate_audit(
                paths,
                session_id="scope-new",
                day="2026-08-30",
                candidate_type="scope",
                rule="Defer optional integrations.",
            )
            ranked = runtime.clusters(paths)
            self.assertEqual(ranked[0].candidate_type, "voice")
            workflow = next(item for item in ranked if item.rule == "Use one approved outline.")
            self.assertEqual(workflow.source_skills, ("skill-a", "skill-b"))
            self.assertEqual(len(workflow.session_cwds), 2)
            scopes = [item for item in ranked if item.candidate_type == "scope"]
            self.assertEqual([item.rule for item in scopes], ["Defer optional integrations.", "Keep the release narrow."])

    def test_priority_snapshot_and_status_include_stale_count_without_read_only_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = runtime.resolve_paths(Path(tmp) / "codex")
            paths.instincts.mkdir(parents=True)
            legacy = paths.instincts / "pmm-instinct-2026-07-01-001.md"
            runtime.atomic_write_text(
                legacy,
                runtime._serialize_frontmatter(
                    {
                        "id": legacy.stem,
                        "type": "workflow",
                        "confidence": 0.3,
                        "created": "2026-07-01",
                        "last_seen": "2026-07-01",
                        "seen_count": 1,
                        "status": "active",
                    },
                    "Use one summary.\n\n**Evidence:** Fictional evidence.",
                ),
            )
            before = legacy.read_bytes()
            self.assertEqual(runtime.runtime_status(paths)["stale_instincts"], 1)
            runtime.backlog(paths)
            self.assertEqual(legacy.read_bytes(), before)
            destination = runtime.write_priority_snapshot(paths)
            snapshot = json.loads(destination.read_text(encoding="utf-8"))
            self.assertEqual(snapshot["instincts"]["stale_candidates"], 1)
            self.assertEqual(runtime.load_instincts(paths)[0].suggested_destination, "")
            write_candidate_audit(
                paths,
                session_id="legacy-match",
                day="2026-09-01",
                candidate_type="workflow",
                rule="Use one summary.",
            )
            cluster = runtime.clusters(paths)[0]
            runtime.review_cluster(
                paths,
                cluster.cluster_id,
                "match",
                source_runtime="portable",
                confirm=True,
            )
            metadata, _ = runtime._parse_frontmatter(legacy.read_text(encoding="utf-8"))
            self.assertEqual(metadata["source_runtime"], "portable")
            self.assertTrue(metadata["suggested_destination"])
            self.assertIn("promotion_outcome", metadata)

    def test_strong_correction_and_contradiction_are_explicit_instinct_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            for index in range(3):
                transcript = root / f"correction-{index}.jsonl"
                write_transcript(transcript, session_id=f"correction-{index}")
                capture_with_suggestion(
                    paths,
                    transcript,
                    f"correction-{index}",
                    "Keep the evidence beside the claim.",
                    candidate_type="correction",
                )
            cluster = runtime.clusters(paths)[0]
            runtime.review_cluster(
                paths,
                cluster.cluster_id,
                "accept",
                strong_correction=True,
                contradicted=True,
                confirm=True,
            )
            instinct = runtime.load_instincts(paths)[0]
            metadata, _ = runtime._parse_frontmatter(instinct.path.read_text(encoding="utf-8"))
            self.assertTrue(metadata["strong_correction"])
            self.assertTrue(instinct.contradicted)
            self.assertEqual(instinct.confidence, 0.45)
            self.assertTrue(instinct.suggested_destination)

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
            self.assertTrue(applied["applied"])
            self.assertEqual(applied["terminal_status"], "promoted")
            promoted = runtime.load_instincts(paths)[0]
            self.assertEqual(promoted.status, "promoted")
            self.assertEqual(promoted.promotion_outcome, "promoted")
            self.assertEqual(runtime.runtime_status(paths)["promotion_candidates"], 0)
            with self.assertRaisesRegex(ValueError, "not eligible"):
                runtime.promotion_preview(paths, instinct_id, destination="project")
            self.assertIn(runtime.PROMOTED_GUIDANCE_HEADING, (repo / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual((repo / "AGENTS.md").stat().st_mode & 0o777, 0o644)

    def test_already_covered_promotion_becomes_terminal_without_duplicate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            (repo / ".git").mkdir(parents=True)
            rule = "Put the decision first."
            agents = repo / "AGENTS.md"
            agents.write_text(f"# Instructions\n\n{runtime.PROMOTED_GUIDANCE_HEADING}\n\n- {rule}\n", encoding="utf-8")
            before = agents.read_bytes()
            paths = enabled_paths(root / "codex")
            for index in range(3):
                transcript = root / f"covered-{index}.jsonl"
                write_transcript(transcript, session_id=f"covered-{index}", cwd=str(repo))
                capture_with_suggestion(paths, transcript, f"covered-{index}", rule)
            selected = runtime.clusters(paths)[0]
            receipt = runtime.review_cluster(paths, selected.cluster_id, "accept", confirm=True)
            instinct_id = Path(receipt["instinct_path"]).stem
            preview = runtime.promotion_preview(paths, instinct_id, destination="project")
            self.assertTrue(preview["targets"][0]["duplicate"])
            covered = runtime.apply_promotion(paths, instinct_id, destination="project", confirm=True)
            self.assertEqual(covered["terminal_status"], "covered")
            self.assertEqual(covered["changed"], [])
            self.assertEqual(agents.read_bytes(), before)
            self.assertEqual(runtime.load_instincts(paths)[0].status, "covered")

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
            unavailable = runtime.promotion_preview(paths, instinct_id, destination="ref")
        self.assertNotIn("ref", selection["available_destinations"])
        self.assertFalse(unavailable["applicable"])
        self.assertEqual(unavailable["reason"], "no-eligible-target")

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


class CodexParityRoutingTests(unittest.TestCase):
    def test_legacy_config_gets_empty_run_routes_in_memory_without_status_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = runtime.resolve_paths(Path(tmp) / "codex")
            runtime.ensure_store(paths)
            legacy = dict(runtime.DEFAULT_CONFIG)
            legacy.pop("run_routes")
            legacy["voice_ref_routes"] = {"voice-skill": "references/REF-voice.md"}
            runtime.atomic_write_json(paths.config, legacy)
            before = paths.config.read_bytes()
            loaded = runtime.load_config(paths)
            status = runtime.runtime_status(paths)
            after = paths.config.read_bytes()

        self.assertEqual(loaded["run_routes"], {})
        self.assertEqual(loaded["voice_ref_routes"]["voice-skill"], "references/REF-voice.md")
        self.assertEqual(status["extractor_model"], legacy["extractor_model"])
        self.assertEqual(after, before)

    def test_valid_route_shapes_deduplicate_voice_targets_preserving_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            voice_skill = write_skill(
                paths,
                "voice-skill",
                {
                    "references/REF-first.md": "# First voice reference\n",
                    "references/REF-second.md": "# Second voice reference\n",
                },
            )
            configured = runtime.update_config(
                paths,
                run_routes={"workflow-skill": "references/RUN-active.md"},
                voice_ref_routes={
                    "voice-skill": [
                        "references/REF-second.md",
                        "references/REF-first.md",
                        "references/REF-second.md",
                    ]
                },
            )
            reloaded = runtime.load_config(paths)
            instinct_id = accepted_instinct_id(
                paths,
                root,
                source_skill="voice-skill",
                candidate_type="voice",
                rule="Use the selected fictional voice reference.",
            )
            choice = runtime.promotion_preview(paths, instinct_id, destination="ref")

        self.assertEqual(configured, reloaded)
        self.assertEqual(
            reloaded["voice_ref_routes"]["voice-skill"],
            ["references/REF-second.md", "references/REF-first.md"],
        )
        self.assertFalse(choice["applicable"])
        self.assertEqual(choice["reason"], "multiple-eligible-targets")
        self.assertEqual(
            choice["eligible_targets"],
            [
                str((voice_skill / "references" / "REF-second.md").resolve()),
                str((voice_skill / "references" / "REF-first.md").resolve()),
            ],
        )

    def test_explicit_route_updates_reject_bad_shapes_without_rewriting_config(self):
        bad_updates = (
            {"run_routes": []},
            {"run_routes": {"workflow-skill": "/absolute/RUN-active.md"}},
            {"run_routes": {"workflow-skill": "../references/RUN-active.md"}},
            {"run_routes": {"workflow-skill": "references/nested/RUN-active.md"}},
            {"run_routes": {"workflow-skill": "references/REF-wrong.md"}},
            {"run_routes": {"workflow-skill": "references/RUN-\x00.md"}},
            {"voice_ref_routes": []},
            {"voice_ref_routes": {"voice-skill": []}},
            {"voice_ref_routes": {"voice-skill": [""]}},
            {"voice_ref_routes": {"voice-skill": "references/RUN-wrong.md"}},
        )
        with tempfile.TemporaryDirectory() as tmp:
            paths = enabled_paths(Path(tmp) / "codex")
            before = paths.config.read_bytes()
            for update in bad_updates:
                with self.subTest(update=update), self.assertRaisesRegex(ValueError, "route"):
                    runtime.update_config(paths, **update)
                self.assertEqual(paths.config.read_bytes(), before)

    def test_configured_run_route_selects_active_run_when_discovery_is_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "workflow-skill",
                {
                    "references/RUN-active.md": "# Active workflow\n",
                    "references/RUN-archived.md": "# Archived workflow\n",
                },
            )
            runtime.update_config(paths, run_routes={"workflow-skill": "references/RUN-active.md"})
            instinct_id = accepted_instinct_id(paths, root, source_skill="workflow-skill")
            preview = runtime.promotion_preview(paths, instinct_id, destination="run")

        self.assertEqual(preview["decision"], "run")
        self.assertEqual(preview["targets"], [{"path": str((skill / "references" / "RUN-active.md").resolve()), "duplicate": False}])

    def test_unconfigured_unique_run_fallback_remains_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(paths, "workflow-skill", {"references/RUN-only.md": "# Only workflow\n"})
            config = json.loads(paths.config.read_text(encoding="utf-8"))
            config.pop("run_routes")
            runtime.atomic_write_json(paths.config, config)
            before = paths.config.read_bytes()
            instinct_id = accepted_instinct_id(paths, root, source_skill="workflow-skill")
            preview = runtime.promotion_preview(paths, instinct_id, destination="run")
            after = paths.config.read_bytes()

        self.assertEqual(Path(preview["targets"][0]["path"]), (skill / "references" / "RUN-only.md").resolve())
        self.assertEqual(after, before)

    def test_ambiguous_run_requires_exact_emitted_canonical_target_and_rechecks_at_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "workflow-skill",
                {
                    "references/RUN-alpha.md": "# Alpha\n",
                    "references/RUN-beta.md": "# Beta\n",
                },
            )
            alpha = (skill / "references" / "RUN-alpha.md").resolve()
            beta = (skill / "references" / "RUN-beta.md").resolve()
            instinct_id = accepted_instinct_id(paths, root, source_skill="workflow-skill")
            choice = runtime.promotion_preview(paths, instinct_id, destination="run")
            preview_record = paths.state / f"promotion-preview-{runtime.safe_session_id(instinct_id)}.json"

            self.assertFalse(choice["applicable"])
            self.assertEqual(choice["reason"], "multiple-eligible-targets")
            self.assertEqual(choice["eligible_targets"], [str(alpha), str(beta)])
            self.assertEqual(choice["targets"], [])
            self.assertFalse(preview_record.exists())

            exact = runtime.promotion_preview(paths, instinct_id, destination="run", target=str(beta))
            self.assertEqual(exact["targets"][0]["path"], str(beta))
            self.assertTrue(preview_record.is_file())

            aliases = [
                "references/RUN-beta.md",
                str(beta.parent / ".." / "references" / beta.name),
            ]
            alias = root / "RUN-beta-alias.md"
            alias.symlink_to(beta)
            aliases.append(str(alias))
            for candidate in aliases:
                with self.subTest(candidate=candidate):
                    rejected = runtime.promotion_preview(paths, instinct_id, destination="run", target=candidate)
                    self.assertFalse(rejected["applicable"])
                    self.assertEqual(rejected["reason"], "invalid-target-selection")
                    self.assertEqual(rejected["eligible_targets"], [str(alpha), str(beta)])

            beta.unlink()
            with self.assertRaisesRegex(ValueError, "invalid-target-selection"):
                runtime.apply_promotion(
                    paths,
                    instinct_id,
                    destination="run",
                    target=str(beta),
                    confirm=True,
                )

    def test_ordered_voice_ref_choices_deduplicate_and_accept_one_exact_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "voice-skill",
                {
                    "references/REF-a.md": "# Voice A\n",
                    "references/REF-b.md": "# Voice B\n",
                },
            )
            ref_a = (skill / "references" / "REF-a.md").resolve()
            ref_b = (skill / "references" / "REF-b.md").resolve()
            runtime.update_config(
                paths,
                voice_ref_routes={
                    "voice-skill": [
                        "references/REF-b.md",
                        "references/REF-a.md",
                        "references/REF-b.md",
                    ]
                },
            )
            instinct_id = accepted_instinct_id(
                paths,
                root,
                source_skill="voice-skill",
                candidate_type="voice",
                rule="Use the selected fictional framing.",
            )
            choice = runtime.promotion_preview(paths, instinct_id, destination="ref")
            selected = runtime.promotion_preview(paths, instinct_id, destination="ref", target=str(ref_a))

        self.assertFalse(choice["applicable"])
        self.assertEqual(choice["reason"], "multiple-eligible-targets")
        self.assertEqual(choice["eligible_targets"], [str(ref_b), str(ref_a)])
        self.assertEqual(selected["targets"][0]["path"], str(ref_a))

    def test_ambiguous_run_apply_changes_only_the_exact_selected_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "workflow-skill",
                {
                    "references/RUN-alpha.md": "# Alpha\n",
                    "references/RUN-beta.md": "# Beta\n",
                },
            )
            alpha = (skill / "references" / "RUN-alpha.md").resolve()
            beta = (skill / "references" / "RUN-beta.md").resolve()
            instinct_id = accepted_instinct_id(
                paths,
                root,
                source_skill="workflow-skill",
                rule="Apply guidance only to the selected fictional workflow.",
            )
            runtime.promotion_preview(paths, instinct_id, destination="run", target=str(beta))
            applied = runtime.apply_promotion(
                paths,
                instinct_id,
                destination="run",
                target=str(beta),
                confirm=True,
            )
            alpha_text = alpha.read_text(encoding="utf-8")
            beta_text = beta.read_text(encoding="utf-8")

        self.assertEqual(applied["changed"], [str(beta)])
        self.assertNotIn(runtime.PROMOTED_GUIDANCE_HEADING, alpha_text)
        self.assertIn(runtime.PROMOTED_GUIDANCE_HEADING, beta_text)

    def test_configured_route_across_two_discovered_roots_requires_exact_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            user_skill = write_skill(
                paths,
                "shared-skill",
                {"references/RUN-active.md": "# User-owned active workflow\n"},
            )
            repository = root / "supporting-repository"
            repository_skill = repository / "skills" / "shared-skill"
            (repository_skill / "references").mkdir(parents=True)
            (repository_skill / "SKILL.md").write_text(
                "---\nname: shared-skill\ndescription: Repository-local fictional skill.\n---\n",
                encoding="utf-8",
            )
            (repository_skill / "references" / "RUN-active.md").write_text(
                "# Repository-owned active workflow\n",
                encoding="utf-8",
            )
            runtime.update_config(
                paths,
                run_routes={"shared-skill": "references/RUN-active.md"},
            )
            instinct_id = accepted_instinct_id(paths, root, source_skill="shared-skill")
            choice = runtime.promotion_preview(paths, instinct_id, destination="run")
            expected = {
                str((user_skill / "references" / "RUN-active.md").resolve()),
                str((repository_skill / "references" / "RUN-active.md").resolve()),
            }
            selected_target = str((repository_skill / "references" / "RUN-active.md").resolve())
            selected = runtime.promotion_preview(
                paths,
                instinct_id,
                destination="run",
                target=selected_target,
            )

        self.assertFalse(choice["applicable"])
        self.assertEqual(choice["reason"], "multiple-eligible-targets")
        self.assertEqual(set(choice["eligible_targets"]), expected)
        self.assertEqual(selected["targets"][0]["path"], selected_target)

    def test_malformed_route_shapes_remain_readable_but_fail_closed_at_resolution(self):
        cases = {
            "run-map-wrong-type": ("workflow", {"run_routes": []}),
            "run-value-wrong-type": ("workflow", {"run_routes": {"route-skill": 7}}),
            "run-control-character": (
                "workflow",
                {"run_routes": {"route-skill": "references/RUN-\x00.md"}},
            ),
            "voice-map-wrong-type": ("voice", {"voice_ref_routes": []}),
            "voice-empty-list": ("voice", {"voice_ref_routes": {"route-skill": []}}),
            "voice-empty-entry": ("voice", {"voice_ref_routes": {"route-skill": [""]}}),
        }
        for case, (candidate_type, updates) in cases.items():
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                paths = enabled_paths(root / "codex")
                write_skill(
                    paths,
                    "route-skill",
                    {
                        "references/RUN-fallback.md": "# Fallback\n",
                        "references/REF-fallback.md": "# Fallback voice\n",
                    },
                )
                config = json.loads(paths.config.read_text(encoding="utf-8"))
                config.update(updates)
                runtime.atomic_write_json(paths.config, config)
                before = paths.config.read_bytes()
                self.assertEqual(runtime.load_config(paths)[next(iter(updates))], next(iter(updates.values())))
                instinct_id = accepted_instinct_id(
                    paths,
                    root,
                    source_skill="route-skill",
                    candidate_type=candidate_type,
                    rule=f"Use the safe {case} behavior.",
                )
                result = runtime.promotion_preview(
                    paths,
                    instinct_id,
                    destination="ref" if candidate_type == "voice" else "run",
                )
                self.assertFalse(result["applicable"])
                self.assertEqual(result["reason"], "invalid-route-configuration")
                self.assertTrue(result["route_errors"])
                self.assertEqual(result["eligible_targets"], [])
                self.assertEqual(paths.config.read_bytes(), before)

    def test_run_route_path_family_and_confinement_matrix_fails_closed_without_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "route-skill",
                {
                    "references/RUN-fallback.md": "# Safe fallback that must not mask bad config\n",
                    "references/REF-wrong-family.md": "# Wrong family\n",
                    "references/nested/RUN-nested.md": "# Nested\n",
                    "references/RUN-read-only.md": "# Read only\n",
                },
            )
            (skill / "references" / "RUN-directory.md").mkdir()
            external = root / "external" / "RUN-external.md"
            external.parent.mkdir()
            external.write_text("# External\n", encoding="utf-8")
            (skill / "references" / "RUN-symlink.md").symlink_to(external)
            other = write_skill(paths, "other-skill", {"references/RUN-other.md": "# Other skill\n"})
            (skill / "references" / "RUN-cross-skill.md").symlink_to(other / "references" / "RUN-other.md")
            plugin_run = PLUGIN / "skills" / "pmm-instinct-review" / "references" / "RUN-workflow.md"
            (skill / "references" / "RUN-plugin.md").symlink_to(plugin_run)
            read_only = skill / "references" / "RUN-read-only.md"
            instinct_id = accepted_instinct_id(paths, root, source_skill="route-skill")

            cases = {
                "absolute": str((skill / "references" / "RUN-fallback.md").resolve()),
                "traversal": "../other-skill/references/RUN-other.md",
                "nested": "references/nested/RUN-nested.md",
                "wrong-family": "references/REF-wrong-family.md",
                "missing": "references/RUN-missing.md",
                "directory": "references/RUN-directory.md",
                "symlink-escape": "references/RUN-symlink.md",
                "cross-skill": "references/RUN-cross-skill.md",
                "plugin-owned": "references/RUN-plugin.md",
                "non-writable": "references/RUN-read-only.md",
            }
            real_access = runtime.os.access

            def access(candidate, mode):
                if Path(candidate).resolve() == read_only.resolve():
                    return False
                return real_access(candidate, mode)

            for case, route in cases.items():
                with self.subTest(case=case), mock.patch.object(runtime.os, "access", side_effect=access):
                    config = runtime.load_config(paths)
                    config["run_routes"] = {"route-skill": route}
                    runtime.atomic_write_json(paths.config, config)
                    result = runtime.promotion_preview(paths, instinct_id, destination="run")
                    self.assertFalse(result["applicable"])
                    self.assertEqual(result["reason"], "invalid-route-configuration")
                    self.assertTrue(result["route_errors"])
                    self.assertEqual(result["eligible_targets"], [])

    def test_legacy_string_voice_route_and_unaffected_destination_classes_remain_compatible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex")
            skill = write_skill(
                paths,
                "voice-skill",
                {
                    "references/RUN-only.md": "# Workflow\n",
                    "references/REF-legacy.md": "# Voice\n",
                },
            )
            runtime.update_config(
                paths,
                run_routes={"voice-skill": "references/RUN-only.md"},
                voice_ref_routes={"voice-skill": "references/REF-legacy.md"},
            )
            instinct_id = accepted_instinct_id(
                paths,
                root,
                source_skill="voice-skill",
                candidate_type="voice",
                rule="Use the compatible fictional voice route.",
            )
            ref_preview = runtime.promotion_preview(paths, instinct_id, destination="ref")
            skill_preview = runtime.promotion_preview(paths, instinct_id, destination="skill")
            global_preview = runtime.promotion_preview(paths, instinct_id, destination="global")
            project_preview = runtime.promotion_preview(paths, instinct_id, destination="project")
            both_preview = runtime.promotion_preview(paths, instinct_id, destination="both")
            no_preview = runtime.promotion_preview(paths, instinct_id, destination="no")
            edit_preview = runtime.promotion_preview(
                paths,
                instinct_id,
                destination="edit",
                edited_rule="Use the edited compatible fictional voice route.",
            )

        self.assertEqual(Path(ref_preview["targets"][0]["path"]), (skill / "references" / "REF-legacy.md").resolve())
        self.assertEqual(Path(skill_preview["targets"][0]["path"]), (skill / "references" / "RUN-only.md").resolve())
        self.assertEqual(global_preview["decision"], "global")
        self.assertEqual(project_preview["decision"], "project")
        self.assertEqual(both_preview["decision"], "both")
        self.assertEqual(len(both_preview["targets"]), 2)
        self.assertEqual(no_preview["decision"], "no")
        self.assertEqual(edit_preview["decision"], "select-destination")

    def test_cli_forwards_exact_target_to_preview_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex"
            target = str((Path(tmp) / "skills" / "demo" / "references" / "RUN-active.md").resolve())
            with mock.patch.object(
                instinct_cli,
                "promotion_preview",
                return_value={"decision": "run", "targets": [{"path": target, "duplicate": False}]},
            ) as preview:
                code, _stdout, stderr = invoke_cli(
                    "--codex-home",
                    codex_home,
                    "promote",
                    "--instinct",
                    "pmm-instinct-2026-09-11-001",
                    "--destination",
                    "run",
                    "--target",
                    target,
                )
            self.assertEqual((code, stderr), (0, ""))
            self.assertEqual(preview.call_args.kwargs["target"], target)

            with mock.patch.object(
                instinct_cli,
                "apply_promotion",
                return_value={"decision": "run", "targets": [{"path": target}], "applied": True},
            ) as apply:
                code, _stdout, stderr = invoke_cli(
                    "--codex-home",
                    codex_home,
                    "promote",
                    "--instinct",
                    "pmm-instinct-2026-09-11-001",
                    "--destination",
                    "run",
                    "--target",
                    target,
                    "--apply",
                    "--confirm",
                )
            self.assertEqual((code, stderr), (0, ""))
            self.assertEqual(apply.call_args.kwargs["target"], target)


class BackfillTests(unittest.TestCase):
    def test_legacy_null_model_backfill_skips_without_writing_or_using_inventory_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = runtime.resolve_paths(root / "codex")
            runtime.ensure_store(paths)
            config = dict(runtime.DEFAULT_CONFIG)
            config.update(
                enabled=True,
                privacy_acknowledged_at="2026-09-11T00:00:00+00:00",
                extractor_model=None,
            )
            runtime.atomic_write_json(paths.config, config)
            transcript = root / "legacy-backfill.jsonl"
            write_transcript(transcript, session_id="legacy-backfill", model="gpt-inventory-fallback")
            before_config = paths.config.read_bytes()
            results = runtime.apply_backfill(
                paths,
                [
                    {
                        "session_id": "legacy-backfill",
                        "transcript_path": str(transcript),
                        "cwd": str(root),
                        "model": "gpt-inventory-fallback",
                    }
                ],
            )
            session_files = list(paths.sessions.iterdir())
            queue_files = list(paths.queue.iterdir())
            after_config = paths.config.read_bytes()

        self.assertEqual(
            results,
            [{"status": "skipped", "reason": "unconfigured_model", "session_id": "legacy-backfill"}],
        )
        self.assertEqual(session_files, [])
        self.assertEqual(queue_files, [])
        self.assertEqual(after_config, before_config)

    def test_backfill_dry_inventory_and_apply_bind_persisted_model_not_transcript_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = enabled_paths(root / "codex", model="gpt-backfill-configured")
            transcript = paths.codex_home / "sessions" / "2026" / "session.jsonl"
            write_transcript(transcript, session_id="backfill-1", model="gpt-backfill-transcript")
            old = runtime.utc_now().timestamp() - 3600
            os.utime(transcript, (old, old))
            inventory = runtime.discover_backfill(paths, limit=5, older_than_minutes=30)
            self.assertEqual([item["session_id"] for item in inventory], ["backfill-1"])
            applied = runtime.apply_backfill(paths, inventory)
            queue = runtime.read_queue(paths)[0][1]
            self.assertEqual(applied[0]["status"], "queued")
            self.assertEqual(queue["extractor_model"], "gpt-backfill-configured")
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
