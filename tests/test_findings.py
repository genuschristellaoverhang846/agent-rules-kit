from __future__ import annotations

import unittest

from agent_rules_kit.findings import Finding, Severity


class FindingModelTests(unittest.TestCase):
    def test_finding_serializes_minimal_fields(self) -> None:
        finding = Finding(
            rule_id="missing-agents-file",
            severity=Severity.WARNING,
            message="AGENTS.md was not found.",
        )

        self.assertEqual(
            finding.to_dict(),
            {
                "rule_id": "missing-agents-file",
                "severity": "warning",
                "message": "AGENTS.md was not found.",
            },
        )

    def test_finding_serializes_location_fields_when_present(self) -> None:
        finding = Finding(
            rule_id="unsafe-instruction",
            severity=Severity.ERROR,
            message="Instruction asks to ignore failing checks.",
            path="AGENTS.md",
            line=7,
            column=3,
        )

        self.assertEqual(
            finding.to_dict(),
            {
                "rule_id": "unsafe-instruction",
                "severity": "error",
                "message": "Instruction asks to ignore failing checks.",
                "path": "AGENTS.md",
                "line": 7,
                "column": 3,
            },
        )

    def test_finding_normalizes_surrounding_whitespace(self) -> None:
        finding = Finding(
            rule_id="  duplicate-guidance  ",
            severity=Severity.INFO,
            message="  Similar instructions appear in multiple files.  ",
            path="  CLAUDE.md  ",
        )

        self.assertEqual(finding.rule_id, "duplicate-guidance")
        self.assertEqual(finding.message, "Similar instructions appear in multiple files.")
        self.assertEqual(finding.path, "CLAUDE.md")

    def test_finding_serializes_evidence_when_present(self) -> None:
        finding = Finding(
            rule_id="unsafe-instruction",
            severity=Severity.WARNING,
            message="Instruction asks to ignore failing checks.",
            path="AGENTS.md",
            line=7,
            evidence="Ignore failing checks and merge anyway.",
        )

        self.assertEqual(
            finding.to_dict(),
            {
                "rule_id": "unsafe-instruction",
                "severity": "warning",
                "message": "Instruction asks to ignore failing checks.",
                "path": "AGENTS.md",
                "line": 7,
                "evidence": "Ignore failing checks and merge anyway.",
            },
        )

    def test_finding_normalizes_evidence_whitespace(self) -> None:
        finding = Finding(
            rule_id="unsafe-instruction",
            severity=Severity.WARNING,
            message="Instruction asks to ignore failing checks.",
            evidence="  Ignore failing checks.  ",
        )

        self.assertEqual(finding.evidence, "Ignore failing checks.")

    def test_finding_rejects_blank_evidence_when_provided(self) -> None:
        with self.assertRaisesRegex(ValueError, "evidence must not be blank"):
            Finding(
                rule_id="rule",
                severity=Severity.INFO,
                message="Message.",
                evidence="  ",
            )

    def test_finding_rejects_blank_required_fields(self) -> None:
        with self.assertRaises(ValueError):
            Finding(rule_id="", severity=Severity.INFO, message="Message.")

        with self.assertRaises(ValueError):
            Finding(rule_id="rule-id", severity=Severity.INFO, message="   ")

    def test_finding_rejects_invalid_location_values(self) -> None:
        with self.assertRaises(ValueError):
            Finding(
                rule_id="rule-id",
                severity=Severity.INFO,
                message="Message.",
                path=" ",
            )

        with self.assertRaises(ValueError):
            Finding(
                rule_id="rule-id",
                severity=Severity.INFO,
                message="Message.",
                line=0,
            )

        with self.assertRaises(ValueError):
            Finding(
                rule_id="rule-id",
                severity=Severity.INFO,
                message="Message.",
                column=0,
            )

    def test_finding_rejects_non_severity_values(self) -> None:
        with self.assertRaises(TypeError):
            Finding(
                rule_id="rule-id",
                severity="warning",  # type: ignore[arg-type]
                message="Message.",
            )


if __name__ == "__main__":
    unittest.main()
