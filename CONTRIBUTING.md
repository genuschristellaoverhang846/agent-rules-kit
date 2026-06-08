# Contributing Guide

Thank you for considering a contribution to agent-rules-kit.

This repository is intentionally strict. The goal is not to move fast at the cost of reliability. The goal is to keep the project clear, local-first, testable, auditable, and safe to maintain.

All contributors, AI assistants, and coding agents must read and follow AGENTS.md before changing files.

## Project boundaries

agent-rules-kit is a local Python CLI for diagnosing baseline quality of AI agent instruction files in repositories.

It is not a security scanner.

The project must preserve these boundaries:

- read-only by default;
- no network access in runtime behavior;
- no LLM dependency in runtime behavior;
- no execution of commands from analyzed repositories;
- no unsupported security claims;
- secret-like findings must be redacted.

Do not propose changes that break these boundaries without explicit maintainer approval.

## Work modes

This repository distinguishes two work modes.

### Genesis / Inception

Genesis is the initial local creation phase before the remote repository and branch protection exist.

During Genesis, work on main is allowed only under strict control:

- main starts clean;
- create one file or one minimal unit;
- validate that file;
- status shows exactly one change whenever possible;
- stage the exact file;
- review the staged diff visibly;
- ensure there are no unstaged changes;
- commit;
- return main to clean state.

Do not batch unrelated files during Genesis.

### Always-Green

Always-Green begins after Genesis closes.

After Genesis:

- do not work directly on main;
- create a branch for every logical phase;
- read existing files before editing;
- make one minimal change at a time;
- run checks before stage;
- stage exact files only;
- never use git add .;
- review the staged diff fully;
- commit small;
- push only after local checks pass;
- open a pull request;
- merge only after CI is green;
- return main to a clean synchronized state.

## One-change discipline

Prefer one file per commit.

Allowed exceptions must be justified before the change, not after.

Examples of acceptable one-file commits:

- add one source file;
- add one test file;
- add one documentation file;
- add one workflow file;
- update one policy file.

Examples of changes that should not be mixed:

- source code plus unrelated documentation;
- tests plus unrelated CI;
- README rewrite plus package logic;
- security policy plus product roadmap;
- formatting churn plus feature logic.

## Local checks

Run the local check script before committing:

./scripts/check.sh

The check script currently verifies:

- Python syntax;
- unit tests;
- text hygiene;
- Git whitespace checks.

Additional file-specific checks are required when relevant.

For Python files:

- compile the file;
- run related tests;
- run the full local check script.

For shell files:

- run sh -n;
- verify executable mode when needed;
- run the script if safe.

For Markdown files:

- verify UTF-8;
- verify LF line endings;
- verify final newline;
- verify no trailing whitespace;
- avoid fake claims, secrets, or unsupported security promises.

## Commit messages

Use small, specific commit messages.

Examples:

- chore: add repository identity baseline
- chore: add python project metadata
- feat: add initial cli entrypoint
- test: add cli smoke tests
- chore: add local check script
- docs: add security policy boundaries

Avoid vague messages such as:

- update files
- fixes
- changes
- work in progress
- final version

## Pull requests

A pull request should include:

- what changed;
- why it changed;
- how it was tested;
- known limitations;
- security or boundary impact, if any.

Do not open a pull request with known failing checks unless the pull request is explicitly marked as diagnostic and not intended to merge.

## Security-sensitive changes

Treat these areas as security-sensitive:

- secret detection;
- redaction;
- file traversal;
- symlink handling;
- write behavior;
- command execution boundaries;
- reporting formats that may expose file contents;
- CI permissions;
- GitHub Actions configuration.

For security-sensitive changes:

- keep the diff small;
- add or update tests;
- avoid broad rewrites;
- document the risk;
- request careful review before merge.

## AI assistant rules

AI assistants must not improvise workflow.

Required behavior:

- inspect real state first;
- avoid assumptions;
- change one thing at a time;
- never use git add .;
- never hide failing checks;
- never continue after a broken command without inspection;
- never add secrets;
- never make unsupported production or security claims;
- never use `path` as a zsh variable name.

If a step fails, stop and recover before continuing.

## Issue quality

Good issues include:

- clear problem statement;
- expected behavior;
- actual behavior;
- reproduction steps;
- relevant files;
- environment details;
- whether the issue affects safety, correctness, documentation, or usability.

Poor issues include:

- vague requests;
- missing reproduction;
- demands to bypass checks;
- requests to add network, LLM, or command execution behavior without a design discussion.

## Non-goals

This project does not aim to be:

- a universal AI agent framework;
- a security scanner;
- a dependency vulnerability scanner;
- a CI/CD security auditor;
- a tool that executes repository commands;
- a tool that proves a repository is safe.

## Maintainer expectations

Maintainers should protect the project by keeping changes:

- small;
- reviewed;
- tested;
- documented;
- reversible;
- aligned with project boundaries.

A contribution is not ready because it looks useful. It is ready when it is understandable, tested, safe within the project boundaries, and easy to review.
