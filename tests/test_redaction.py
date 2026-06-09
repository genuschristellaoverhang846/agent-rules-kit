from __future__ import annotations

import unittest

from agent_rules_kit.redaction import REDACTION_TEXT, redact_secret_like_values


class RedactionTests(unittest.TestCase):
    def test_safe_text_is_unchanged(self) -> None:
        text = "Use local checks before opening a pull request."

        self.assertEqual(redact_secret_like_values(text), text)

    def test_redacts_openai_like_key(self) -> None:
        secret = "sk-" + ("A" * 24)

        redacted = redact_secret_like_values(f"token={secret}")

        self.assertEqual(redacted, f"token={REDACTION_TEXT}")
        self.assertNotIn(secret, redacted)

    def test_redacts_github_like_token(self) -> None:
        secret = "ghp_" + ("B" * 36)

        redacted = redact_secret_like_values(f"github={secret}")

        self.assertEqual(redacted, f"github={REDACTION_TEXT}")
        self.assertNotIn(secret, redacted)

    def test_redacts_aws_like_access_key(self) -> None:
        secret = "AKIA" + ("C" * 16)

        redacted = redact_secret_like_values(f"aws={secret}")

        self.assertEqual(redacted, f"aws={REDACTION_TEXT}")
        self.assertNotIn(secret, redacted)

    def test_redacts_private_key_block(self) -> None:
        header = "-----BEGIN " + "PRIVATE KEY" + "-----"
        footer = "-----END " + "PRIVATE KEY" + "-----"
        secret = f"{header}\nabc123\n{footer}"

        redacted = redact_secret_like_values(f"key:\n{secret}")

        self.assertEqual(redacted, f"key:\n{REDACTION_TEXT}")
        self.assertNotIn("abc123", redacted)

    def test_redacts_multiple_secret_like_values(self) -> None:
        openai_like = "sk-" + ("D" * 24)
        github_like = "gho_" + ("E" * 36)
        text = f"first={openai_like}\nsecond={github_like}"

        redacted = redact_secret_like_values(text)

        self.assertEqual(redacted.count(REDACTION_TEXT), 2)
        self.assertNotIn(openai_like, redacted)
        self.assertNotIn(github_like, redacted)


if __name__ == "__main__":
    unittest.main()
