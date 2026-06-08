from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from agent_rules_kit.cli import main


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


if __name__ == "__main__":
    unittest.main()
