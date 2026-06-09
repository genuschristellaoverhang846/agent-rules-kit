"""Command line entry point for agent-rules-kit."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_rules_kit import __version__
from agent_rules_kit.discovery import InstructionFile, discover_instruction_files
from agent_rules_kit.redaction import redact_secret_like_values

OUTPUT_FORMATS = ("console", "json")


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="agent-rules-kit",
        description="Diagnose baseline quality of AI agent instruction files in repositories.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the package version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser(
        "check",
        help="Discover supported agent instruction files in a repository.",
    )
    check_parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Repository root to inspect. Defaults to the current directory.",
    )
    check_parser.add_argument(
        "--format",
        choices=OUTPUT_FORMATS,
        default="console",
        help="Output format. Defaults to console.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"agent-rules-kit {__version__}")
        return 0

    if args.command == "check":
        return _run_check(Path(args.repository), output_format=args.format)

    parser.print_help()
    return 0


def _run_check(repository_root: Path, *, output_format: str = "console") -> int:
    try:
        instruction_files = discover_instruction_files(repository_root)
    except ValueError as error:
        message = redact_secret_like_values(str(error))

        if output_format == "json":
            _print_json(
                {
                    "command": "check",
                    "status": "error",
                    "repository": redact_secret_like_values(str(repository_root)),
                    "instruction_files": [],
                    "summary": {
                        "supported_instruction_file_count": 0,
                    },
                    "error": {
                        "message": message,
                    },
                }
            )
        else:
            print(f"ERROR: {message}", file=sys.stderr)

        return 2

    if output_format == "json":
        status = "ok" if instruction_files else "no_instruction_files"
        _print_json(_build_check_payload(repository_root, instruction_files, status=status))
        return 0 if instruction_files else 1

    return _print_console_check(repository_root, instruction_files)


def _print_console_check(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> int:
    print(f"agent-rules-kit check: {repository_root}")

    if not instruction_files:
        print("No supported agent instruction files found.")
        return 1

    print(f"Found {len(instruction_files)} supported instruction file(s):")
    for instruction_file in instruction_files:
        print(f"- {instruction_file.path} [{instruction_file.kind.value}]")

    return 0


def _build_check_payload(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    *,
    status: str,
) -> dict[str, object]:
    return {
        "command": "check",
        "status": status,
        "repository": redact_secret_like_values(str(repository_root)),
        "instruction_files": [
            {
                "path": redact_secret_like_values(instruction_file.path),
                "kind": instruction_file.kind.value,
            }
            for instruction_file in instruction_files
        ],
        "summary": {
            "supported_instruction_file_count": len(instruction_files),
        },
        "error": None,
    }


def _print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
