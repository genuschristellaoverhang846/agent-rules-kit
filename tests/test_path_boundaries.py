from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_rules_kit.discovery import (
    InstructionFile,
    InstructionFileKind,
    discover_instruction_files,
)
from agent_rules_kit.init_plan import InitPlanAction, build_init_plan
from agent_rules_kit.init_write import BASELINE_AGENTS_CONTENT, write_init_files


class PathBoundaryTests(unittest.TestCase):
    def test_discovery_reports_repository_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            cursor_rule = repository / ".cursor" / "rules" / "agent.mdc"
            cursor_rule.parent.mkdir(parents=True)
            cursor_rule.write_text("Cursor rule\n", encoding="utf-8")

            self.assertEqual(
                discover_instruction_files(repository),
                (
                    InstructionFile(
                        path=".cursor/rules/agent.mdc",
                        kind=InstructionFileKind.CURSOR_RULE,
                    ),
                ),
            )

    def test_discovery_ignores_backup_and_temporary_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            (repository / "AGENTS.md.agent-rules-kit.bak").write_text(
                "backup\n",
                encoding="utf-8",
            )
            (repository / ".AGENTS.md.agent-rules-kit.tmp").write_text(
                "temporary\n",
                encoding="utf-8",
            )

            self.assertEqual(discover_instruction_files(repository), ())

    def test_init_plan_only_targets_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            nested_agents = repository / "docs" / "AGENTS.md"
            nested_agents.parent.mkdir()
            nested_agents.write_text("nested instructions\n", encoding="utf-8")

            plan = build_init_plan(repository)

            self.assertEqual(plan.files[0].path, "AGENTS.md")
            self.assertEqual(plan.files[0].action, InitPlanAction.CREATE)
            self.assertEqual(
                nested_agents.read_text(encoding="utf-8"),
                "nested instructions\n",
            )

    def test_write_init_files_creates_only_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            with tempfile.TemporaryDirectory() as outside_directory_name:
                outside_agents = Path(outside_directory_name) / "AGENTS.md"
                outside_agents.write_text("outside instructions\n", encoding="utf-8")

                result = write_init_files(repository)

                self.assertEqual(result.files[0].path, "AGENTS.md")
                self.assertEqual(result.files[0].action, InitPlanAction.CREATE)
                self.assertEqual(
                    (repository / "AGENTS.md").read_text(encoding="utf-8"),
                    BASELINE_AGENTS_CONTENT,
                )
                self.assertEqual(
                    outside_agents.read_text(encoding="utf-8"),
                    "outside instructions\n",
                )

    def test_write_init_files_backs_up_only_root_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            root_agents = repository / "AGENTS.md"
            nested_agents = repository / "docs" / "AGENTS.md"
            nested_agents.parent.mkdir()

            root_agents.write_text("root instructions\n", encoding="utf-8")
            nested_agents.write_text("nested instructions\n", encoding="utf-8")

            result = write_init_files(repository)

            self.assertEqual(result.files[0].path, "AGENTS.md")
            self.assertEqual(result.files[0].action, InitPlanAction.BACKUP_AND_REPLACE)
            self.assertEqual(result.files[0].backup_path, "AGENTS.md.agent-rules-kit.bak")
            self.assertEqual(
                (repository / "AGENTS.md.agent-rules-kit.bak").read_text(
                    encoding="utf-8"
                ),
                "root instructions\n",
            )
            self.assertEqual(root_agents.read_text(encoding="utf-8"), BASELINE_AGENTS_CONTENT)
            self.assertEqual(
                nested_agents.read_text(encoding="utf-8"),
                "nested instructions\n",
            )

    def test_write_init_files_leaves_no_atomic_temporary_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)

            write_init_files(repository)

            self.assertFalse((repository / ".AGENTS.md.agent-rules-kit.tmp").exists())


if __name__ == "__main__":
    unittest.main()
