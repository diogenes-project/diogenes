# AI Research Methodology Repository Standards

## Table of Contents

- [Pre-flight checklist](#pre-flight-checklist)
- [Local validation](#local-validation)
- [Linting policy](#linting-policy)
- [Python invocation](#python-invocation)
- [Tooling requirement](#tooling-requirement)
- [Merge strategy override](#merge-strategy-override)

## Pre-flight checklist

- Before modifying any files, check the current branch with `git status -sb`.
- If on `develop`, create a short-lived `feature/*` branch or ask for explicit approval to proceed on `develop`.
- If approval is granted to work on `develop`, call it out in the response and proceed only for that user-approved scope.
- Enable repository git hooks before committing: `git config core.hooksPath .githooks`.

## Local validation

- `vrg-docker-run -- uv run vrg-validate`

## Linting policy

- Linter: `ruff`
- Rule set: `select = ["ALL"]` with scoped ignores per `pyproject.toml`
- Enforcement: CI and local validation
- Format: `ruff format` (double quotes, 120 char line length)

## Python invocation

- Always use `uv run` to invoke Python tools: `uv run pytest`, `uv run ruff`, `uv run mypy`.
- Never use `python3` directly outside of `uv run`.

## Tooling requirement

### Committing changes

```bash
vrg-commit \
  --type TYPE --scope SCOPE --message TEXT \
  [--body BODY]
```

- `--type` (required): one of
  `feat|fix|docs|style|refactor|test|chore|ci|build|revert`
- `--scope` (required): conventional commit scope
- `--message` (required): commit description
- `--body` (optional): detailed commit body

Co-author identity comes from the `VRG_CO_AUTHOR` environment
variable (set by the AI harness).

### Submitting PRs

```bash
vrg-submit-pr \
  --issue NUMBER --title TEXT --summary TEXT \
  [--linkage KEYWORD] [--notes TEXT] [--dry-run]
```

- `--issue` (required): issue number or cross-repo ref
  (e.g., `42` or `owner/repo#42`)
- `--title` (required): PR title
- `--summary` (required): one-line PR summary
- `--linkage` (optional, default: `Ref`): `Ref`
- `--notes` (optional): additional notes
- `--dry-run` (optional): print generated PR without executing

The script detects the target branch and merge strategy
automatically.

## Merge strategy override

| Source branch | Target | Strategy |
|---------------|--------|----------|
| `feature/*`, `bugfix/*`, `chore/*`, `docs/*` | `develop` | Squash (`--squash`) |
| `release/*` | `main` | Regular merge (`--merge`) |
