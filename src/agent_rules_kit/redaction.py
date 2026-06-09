"""Redaction helpers for secret-like values."""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern

REDACTION_TEXT = "[REDACTED]"


@dataclass(frozen=True, slots=True)
class RedactionPattern:
    """A named pattern used to redact secret-like values."""

    name: str
    pattern: Pattern[str]


SECRET_LIKE_PATTERNS: tuple[RedactionPattern, ...] = (
    RedactionPattern(
        name="openai_api_key",
        pattern=re.compile(r"sk-[A-Za-z0-9_-]{12,}"),
    ),
    RedactionPattern(
        name="github_token",
        pattern=re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    ),
    RedactionPattern(
        name="aws_access_key",
        pattern=re.compile(r"AKIA[0-9A-Z]{16}"),
    ),
    RedactionPattern(
        name="private_key_block",
        pattern=re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
    ),
)


def redact_secret_like_values(text: str) -> str:
    """Redact supported secret-like values from text."""
    redacted = text

    for item in SECRET_LIKE_PATTERNS:
        redacted = item.pattern.sub(REDACTION_TEXT, redacted)

    return redacted


__all__ = [
    "REDACTION_TEXT",
    "RedactionPattern",
    "SECRET_LIKE_PATTERNS",
    "redact_secret_like_values",
]
