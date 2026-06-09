# Changelog

All notable changes to agent-rules-kit will be documented in this file.

This project has no stable public release yet.

## [Unreleased]

### Added

- Repository identity baseline with README, MIT license, and .gitignore.
- Python project metadata in pyproject.toml.
- Minimal package version module.
- Initial CLI entrypoint with version and help behavior.
- CLI smoke tests.
- Local check script for syntax, tests, text hygiene, and Git whitespace checks.
- GitHub Actions CI workflow using `local-checks / Python 3.12`.
- AGENTS.md with mandatory AI assistant operating rules.
- SECURITY.md with explicit security boundaries and non-goals.
- SUPPORT.md with pre-release support boundaries.
- CONTRIBUTING.md with Genesis and Always-Green workflow rules.
- GitHub issue templates and pull request template.
- Diagnostic fixtures for supported and risky instruction file scenarios.
- Finding model for diagnostic output.
- Instruction file discovery for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, GitHub Copilot instructions, and GitHub instruction files.
- `check` command with console output.
- JSON output for `check`.
- Markdown output for `check`.
- Secret-like value redaction helpers and tests.
- `init --dry-run` planning behavior.
- Explicit `init --write` behavior for root `AGENTS.md`.
- Backup behavior before replacing an existing root `AGENTS.md`.
- Path boundary tests for discovery and init write behavior.
- Threat model in `docs/THREAT-MODEL.md`.
- Public README with real CLI screenshots, command examples, safety boundaries, quality gates, maintainer workflow, and optional support badge.

### Security

- Runtime boundaries documented: read-only by default, no network behavior, no LLM dependency, and no execution of commands from analyzed repositories.
- `check` and `init --dry-run` documented as non-writing behavior.
- `init --write` documented as explicit write behavior only.
- Existing root `AGENTS.md` is backed up before replacement.
- Secret-like values are redacted in supported output paths.
- Path boundary tests cover root-only init write behavior and repository-relative discovery paths.
- Threat model documents assets, trust boundaries, threats, mitigations, and residual risk.
- The project is explicitly documented as not a security scanner and as providing no security guarantees.

### Changed

- Replaced the inception README with a public README reflecting implemented behavior and verified output examples.
- Updated security and support documentation from local-inception wording to current pre-release public repository status.

### Deprecated

- No deprecated entries.

### Removed

- No removed entries.

### Fixed

- Corrected release-readiness documentation that still referred to future write behavior after `init --write` had been implemented.
- Corrected stale local-inception wording in support and security documentation.

## Release policy

Before the first stable public release, the maintainer must verify:

- local checks pass;
- CI passes for the release SHA;
- README reflects actual behavior;
- SECURITY.md has a private reporting channel or clearly documents the absence of one;
- CHANGELOG.md describes the released changes;
- version number matches pyproject.toml and package metadata;
- no unsupported security, production, or maturity claims are present.

## Notes for maintainers

Do not use this changelog to exaggerate maturity.

A change is not released because it exists locally. A change is released only when it is tagged, documented, pushed, and verified.
