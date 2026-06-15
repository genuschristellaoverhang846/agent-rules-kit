"""Finding model for diagnostic results."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    """Diagnostic finding severity."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class Finding:
    """A single diagnostic finding.

    The model is intentionally small and dependency-free so it can support
    console, JSON, and Markdown output later without pulling in runtime tools.
    """

    rule_id: str
    severity: Severity
    message: str
    path: str | None = None
    line: int | None = None
    column: int | None = None
    evidence: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.severity, Severity):
            raise TypeError("severity must be a Severity value")

        normalized_rule_id = self.rule_id.strip()
        normalized_message = self.message.strip()

        if not normalized_rule_id:
            raise ValueError("rule_id must not be blank")
        if not normalized_message:
            raise ValueError("message must not be blank")

        object.__setattr__(self, "rule_id", normalized_rule_id)
        object.__setattr__(self, "message", normalized_message)

        if self.path is not None:
            normalized_path = self.path.strip()
            if not normalized_path:
                raise ValueError("path must not be blank when provided")
            object.__setattr__(self, "path", normalized_path)

        if self.evidence is not None:
            normalized_evidence = self.evidence.strip()
            if not normalized_evidence:
                raise ValueError("evidence must not be blank when provided")
            object.__setattr__(self, "evidence", normalized_evidence)

        if self.line is not None and self.line < 1:
            raise ValueError("line must be greater than or equal to 1")
        if self.column is not None and self.column < 1:
            raise ValueError("column must be greater than or equal to 1")

    def to_dict(self) -> dict[str, str | int]:
        """Return a stable dictionary representation for future reporters."""
        data: dict[str, str | int] = {
            "rule_id": self.rule_id,
            "severity": self.severity.value,
            "message": self.message,
        }

        if self.path is not None:
            data["path"] = self.path
        if self.line is not None:
            data["line"] = self.line
        if self.column is not None:
            data["column"] = self.column
        if self.evidence is not None:
            data["evidence"] = self.evidence

        return data


__all__ = ["Finding", "Severity"]
