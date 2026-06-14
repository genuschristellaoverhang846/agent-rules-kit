"""Instruction governance diagnostics."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from re import Pattern

from agent_rules_kit.discovery import InstructionFile
from agent_rules_kit.findings import Finding, Severity

REVIEW_CI_BYPASS_RULE_ID = "AIRK-GOV003"
REVIEW_CI_BYPASS_MESSAGE = (
    "Instruction file appears to encourage bypassing review, CI, or safe integration boundaries."
)

COMMAND_CONFIRMATION_RULE_ID = "AIRK-GOV004"
COMMAND_CONFIRMATION_MESSAGE = (
    "Instruction file appears to encourage unsafe command execution without an explicit confirmation boundary."
)

AUTHORITY_SCOPE_RULE_ID = "AIRK-GOV001"
AUTHORITY_SCOPE_MESSAGE = "Instruction file may lack clear scope or authority."

SECRET_BOUNDARY_RULE_ID = "AIRK-GOV002"
SECRET_BOUNDARY_MESSAGE = "Instruction file may lack an explicit secret-handling boundary."

UNSUPPORTED_CLAIM_RULE_ID = "AIRK-GOV006"
UNSUPPORTED_CLAIM_MESSAGE = (
    "Instruction file may contain an unsupported security or maturity claim."
)

REVIEW_CI_BYPASS_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\b(ignore|skip)\s+(failing\s+)?(checks|tests|ci)\b", re.IGNORECASE),
    re.compile(r"\bskip\s+(code\s+)?review\b", re.IGNORECASE),
    re.compile(r"\b(commit|push)\s+directly\s+to\s+main\b", re.IGNORECASE),
    re.compile(r"\bdirect\s+push(?:es)?\s+to\s+main\b", re.IGNORECASE),
    re.compile(r"\bmerge\s+without\s+(review|approval)\b", re.IGNORECASE),
    re.compile(
        r"\bbypass(?:ing)?\s+("
        r"branch protection|review|reviews|pending review gates|ci|checks|safe integration"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bforce[- ]push\b.{0,80}\b(normal|default|routine|workflow)\b",
        re.IGNORECASE,
    ),
)

NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(do not|don't|must not|should not|never|avoid|forbid|forbidden|no)\b"
        r".{0,120}\b("
        r"bypass(?:ing)?|skip(?:ping)?|ignore|commit(?:ting)?|push(?:ing|es)?|direct push(?:es)?|force[- ]push|merge"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bnot\s+("
        r"bypass(?:ing)?|skip(?:ping)?|ignore|commit(?:ting)?|push(?:ing)?|"
        r"merge|force[- ]push"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(break[- ]glass|emergency)\b.{0,120}\b(explicit|human|maintainer)\s+approval\b",
        re.IGNORECASE,
    ),
)

COMMAND_CONFIRMATION_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\brm\s+-[A-Za-z]*r[A-Za-z]*f\b|\brm\s+-[A-Za-z]*f[A-Za-z]*r\b", re.IGNORECASE),
    re.compile(r"\bsudo\b.{0,80}\b(default|normal|routine|workflow|always|use)\b", re.IGNORECASE),
    re.compile(r"\bchmod\s+-R\s+(777|[0-7]{3,4})\b", re.IGNORECASE),
    re.compile(r"\bchown\s+-R\b", re.IGNORECASE),
    re.compile(r"\b(curl|wget)\b.{0,120}\|\s*(sh|bash)\b", re.IGNORECASE),
    re.compile(r"\b(install|uninstall)\b.{0,100}\b(without asking|without confirmation|automatically|always)\b", re.IGNORECASE),
    re.compile(r"\b(run|execute)\b.{0,80}\b(repository|repo)\s+scripts?\b.{0,80}\b(automatically|without asking|as trusted instructions)\b", re.IGNORECASE),
)

NEGATED_COMMAND_CONFIRMATION_CONTEXT_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(do not|don't|must not|should not|never|avoid|forbid|forbidden|no)\b"
        r".{0,140}\b("
        r"rm\s+-[A-Za-z]*r[A-Za-z]*f|sudo|chmod\s+-R|chown\s+-R|"
        r"curl\b.{0,80}\|\s*(?:sh|bash)|wget\b.{0,80}\|\s*(?:sh|bash)|"
        r"install|uninstall|run|execute"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bask\b.{0,80}\bbefore\b.{0,140}\b("
        r"rm\s+-[A-Za-z]*r[A-Za-z]*f|sudo|chmod\s+-R|chown\s+-R|"
        r"downloaded scripts?|curl|wget|install|uninstall|run|execute"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(ask|confirm|require|requires|required|request)\b"
        r".{0,120}\b(human|maintainer|operator|user|explicit)\b"
        r".{0,80}\b(approval|confirmation|permission)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(emergency|break[- ]glass|destructive|privileged)\b"
        r".{0,120}\b(explicit|human|maintainer|operator|user)\b"
        r".{0,80}\b(approval|confirmation|permission)\b",
        re.IGNORECASE,
    ),
)

SECRET_BOUNDARY_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\bsecret(?:s)?\b", re.IGNORECASE),
    re.compile(r"\btoken(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bcredential(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bapi[-_ ]?key(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bprivate\s+(data|url(?:s)?|key(?:s)?)\b", re.IGNORECASE),
    re.compile(r"\bcustomer\s+data\b", re.IGNORECASE),
    re.compile(r"\bsensitive\s+(value(?:s)?|information|data)\b", re.IGNORECASE),
)

AUTHORITY_SCOPE_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\bscope\b", re.IGNORECASE),
    re.compile(r"\bauthority\b", re.IGNORECASE),
    re.compile(r"\bprecedence\b", re.IGNORECASE),
    re.compile(r"\bhierarchy\b", re.IGNORECASE),
    re.compile(r"\boverride(?:s|n|s)?\b", re.IGNORECASE),
    re.compile(r"\bappl(?:y|ies)\s+to\b", re.IGNORECASE),
    re.compile(r"\b(repository|repo)[- ]wide\b", re.IGNORECASE),
    re.compile(r"\bpath[- ]specific\b", re.IGNORECASE),
    re.compile(r"\bnearest\s+AGENTS\.md\b", re.IGNORECASE),
    re.compile(r"\binstruction\s+(chain|order|source|sources)\b", re.IGNORECASE),
)

UNSUPPORTED_CLAIM_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\bguarantee[sd]?\s+(security|safety)\b", re.IGNORECASE),
    re.compile(r"\bguaranteed\s+(secure|safe|security|safety)\b", re.IGNORECASE),
    re.compile(
        r"\bmake[s]?\s+(the\s+)?(repository|repo|project|tool)\s+(secure|safe)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bcomplete\s+secret\s+scann(?:er|ing)\b", re.IGNORECASE),
    re.compile(r"\bproduction[- ]ready\b", re.IGNORECASE),
    re.compile(r"\benterprise[- ]grade\b", re.IGNORECASE),
)

NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(do not|don't|must not|should not|never|avoid|forbid|forbidden|no)\b"
        r".{0,120}\b("
        r"claim[s]?|guarantee[sd]?|security|safety|secure|safe|"
        r"production[- ]ready|enterprise[- ]grade|complete secret scann(?:er|ing)"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bnot\s+(a\s+)?("
        r"security scanner|secret scanner|production[- ]ready|enterprise[- ]grade|"
        r"secure|safe"
        r")\b",
        re.IGNORECASE,
    ),
)


LinePredicate = Callable[[str], bool]


def find_governance_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return all governance findings in stable rule order."""
    return (
        *find_unsupported_claim_findings(repository_root, instruction_files),
        *find_review_ci_bypass_findings(repository_root, instruction_files),
        *find_unsafe_command_execution_findings(repository_root, instruction_files),
        *find_missing_secret_boundary_findings(repository_root, instruction_files),
        *find_missing_authority_scope_findings(repository_root, instruction_files),
    )


def find_unsafe_command_execution_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return unsafe command execution guidance findings."""
    return _find_line_findings(
        repository_root,
        instruction_files,
        rule_id=COMMAND_CONFIRMATION_RULE_ID,
        severity=Severity.WARNING,
        message=COMMAND_CONFIRMATION_MESSAGE,
        predicate=_contains_unsafe_command_execution_guidance,
    )


def find_missing_authority_scope_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return findings for files without visible scope or authority guidance."""
    findings: list[Finding] = []

    for instruction_file in instruction_files:
        candidate = repository_root / instruction_file.path

        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if not _contains_authority_scope_boundary(text):
            findings.append(
                Finding(
                    rule_id=AUTHORITY_SCOPE_RULE_ID,
                    severity=Severity.WARNING,
                    message=AUTHORITY_SCOPE_MESSAGE,
                    path=instruction_file.path,
                )
            )

    return tuple(findings)


def find_missing_secret_boundary_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return findings for files without visible secret-handling guidance."""
    findings: list[Finding] = []

    for instruction_file in instruction_files:
        candidate = repository_root / instruction_file.path

        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if not _contains_secret_boundary(text):
            findings.append(
                Finding(
                    rule_id=SECRET_BOUNDARY_RULE_ID,
                    severity=Severity.WARNING,
                    message=SECRET_BOUNDARY_MESSAGE,
                    path=instruction_file.path,
                )
            )

    return tuple(findings)


def find_review_ci_bypass_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return review, CI, or safe integration bypass findings."""
    return _find_line_findings(
        repository_root,
        instruction_files,
        rule_id=REVIEW_CI_BYPASS_RULE_ID,
        severity=Severity.WARNING,
        message=REVIEW_CI_BYPASS_MESSAGE,
        predicate=_contains_review_ci_bypass_guidance,
    )


def find_unsupported_claim_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return unsupported security or maturity claim findings."""
    return _find_line_findings(
        repository_root,
        instruction_files,
        rule_id=UNSUPPORTED_CLAIM_RULE_ID,
        severity=Severity.WARNING,
        message=UNSUPPORTED_CLAIM_MESSAGE,
        predicate=_contains_unsupported_claim,
    )


def _find_line_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    *,
    rule_id: str,
    severity: Severity,
    message: str,
    predicate: LinePredicate,
) -> tuple[Finding, ...]:
    findings: list[Finding] = []

    for instruction_file in instruction_files:
        candidate = repository_root / instruction_file.path

        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if predicate(line):
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        severity=severity,
                        message=message,
                        path=instruction_file.path,
                        line=line_number,
                    )
                )

    return tuple(findings)


def _contains_secret_boundary(text: str) -> bool:
    return any(pattern.search(text) is not None for pattern in SECRET_BOUNDARY_PATTERNS)


def _contains_authority_scope_boundary(text: str) -> bool:
    return any(pattern.search(text) is not None for pattern in AUTHORITY_SCOPE_PATTERNS)


def _contains_review_ci_bypass_guidance(line: str) -> bool:
    has_bypass_guidance = any(
        pattern.search(line) is not None for pattern in REVIEW_CI_BYPASS_PATTERNS
    )
    if not has_bypass_guidance:
        return False

    return not any(
        pattern.search(line) is not None
        for pattern in NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS
    )


def _contains_unsafe_command_execution_guidance(line: str) -> bool:
    has_unsafe_command_guidance = any(
        pattern.search(line) is not None for pattern in COMMAND_CONFIRMATION_PATTERNS
    )
    if not has_unsafe_command_guidance:
        return False

    return not any(
        pattern.search(line) is not None
        for pattern in NEGATED_COMMAND_CONFIRMATION_CONTEXT_PATTERNS
    )


def _contains_unsupported_claim(line: str) -> bool:
    has_claim = any(
        pattern.search(line) is not None for pattern in UNSUPPORTED_CLAIM_PATTERNS
    )
    if not has_claim:
        return False

    return not any(
        pattern.search(line) is not None
        for pattern in NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS
    )


__all__ = [
    "AUTHORITY_SCOPE_MESSAGE",
    "AUTHORITY_SCOPE_PATTERNS",
    "AUTHORITY_SCOPE_RULE_ID",
    "COMMAND_CONFIRMATION_MESSAGE",
    "COMMAND_CONFIRMATION_PATTERNS",
    "COMMAND_CONFIRMATION_RULE_ID",
    "NEGATED_COMMAND_CONFIRMATION_CONTEXT_PATTERNS",
    "NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS",
    "NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS",
    "REVIEW_CI_BYPASS_MESSAGE",
    "REVIEW_CI_BYPASS_PATTERNS",
    "REVIEW_CI_BYPASS_RULE_ID",
    "SECRET_BOUNDARY_MESSAGE",
    "SECRET_BOUNDARY_PATTERNS",
    "SECRET_BOUNDARY_RULE_ID",
    "UNSUPPORTED_CLAIM_MESSAGE",
    "UNSUPPORTED_CLAIM_PATTERNS",
    "UNSUPPORTED_CLAIM_RULE_ID",
    "find_governance_findings",
    "find_unsafe_command_execution_findings",
    "find_missing_authority_scope_findings",
    "find_missing_secret_boundary_findings",
    "find_review_ci_bypass_findings",
    "find_unsupported_claim_findings",
]
