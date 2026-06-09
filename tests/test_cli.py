from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from agent_rules_kit.cli import main

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "repositories"


class CliTests(unittest.TestCase):
    def test_version_flag_prints_version(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["--version"])

        self.assertEqual(exit_code, 0)
        self.assertIn("agent-rules-kit 0.1.0", output.getvalue())

    def test_help_is_default(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main([])

        self.assertEqual(exit_code, 0)
        self.assertIn("usage:", output.getvalue())
        self.assertIn("check", output.getvalue())

    def test_check_reports_discovered_instruction_files(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "multi-agent-overlap")])

        text = output.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("Found 6 supported instruction file(s):", text)
        self.assertIn("- AGENTS.md [agents]", text)
        self.assertIn("- CLAUDE.md [claude]", text)
        self.assertIn("- GEMINI.md [gemini]", text)
        self.assertIn("- .cursor/rules/agent-rules.mdc [cursor-rule]", text)
        self.assertIn("- .github/copilot-instructions.md [copilot]", text)
        self.assertIn(
            "- .github/instructions/agents.instructions.md [github-instruction]",
            text,
        )

    def test_check_returns_one_when_no_instruction_files_are_found(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "empty-repo")])

        self.assertEqual(exit_code, 1)
        self.assertIn("No supported agent instruction files found.", output.getvalue())

    def test_check_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stderr(output):
            exit_code = main(["check", str(FIXTURE_ROOT / "missing-repo")])

        self.assertEqual(exit_code, 2)
        self.assertIn("ERROR: repository root does not exist:", output.getvalue())

    def test_check_reports_discovered_instruction_files_as_json(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "multi-agent-overlap"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["command"], "check")
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["error"], None)
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 6)
        self.assertEqual(
            payload["instruction_files"],
            [
                {"path": "AGENTS.md", "kind": "agents"},
                {"path": "CLAUDE.md", "kind": "claude"},
                {"path": "GEMINI.md", "kind": "gemini"},
                {
                    "path": ".github/copilot-instructions.md",
                    "kind": "copilot",
                },
                {
                    "path": ".cursor/rules/agent-rules.mdc",
                    "kind": "cursor-rule",
                },
                {
                    "path": ".github/instructions/agents.instructions.md",
                    "kind": "github-instruction",
                },
            ],
        )

    def test_check_json_returns_one_when_no_instruction_files_are_found(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "empty-repo"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 1)
        self.assertEqual(payload["status"], "no_instruction_files")
        self.assertEqual(payload["instruction_files"], [])
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 0)
        self.assertEqual(payload["error"], None)

    def test_check_json_returns_two_for_invalid_repository_root(self) -> None:
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(FIXTURE_ROOT / "missing-repo"),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["instruction_files"], [])
        self.assertEqual(payload["summary"]["supported_instruction_file_count"], 0)
        self.assertIn(
            "repository root does not exist:",
            payload["error"]["message"],
        )

    def test_check_json_redacts_secret_like_repository_values(self) -> None:
        output = io.StringIO()
        secret_like_path = FIXTURE_ROOT / ("sk-" + ("A" * 24))

        with redirect_stdout(output):
            exit_code = main(
                [
                    "check",
                    str(secret_like_path),
                    "--format",
                    "json",
                ]
            )

        payload = json.loads(output.getvalue())
        text = output.getvalue()

        self.assertEqual(exit_code, 2)
        self.assertIn("[REDACTED]", text)
        self.assertNotIn(secret_like_path.name, text)
        self.assertEqual(payload["status"], "error")


if __name__ == "__main__":
    unittest.main()
