# Validation

## Canonical local validation command

```bash
vrg-docker-run -- uv run vrg-validate
```

This runs all Tier 1 validation checks inside one dev container:
common checks (markdownlint, shellcheck, yamllint), then
language-specific checks (lint, typecheck, test, audit) from the
built-in command registry, then repo-specific custom validation
(`scripts/bin/validate-custom`).

Anything CI rejects must be rejected locally.

## What vrg-validate runs (must match CI)

- **Common:** markdownlint, shellcheck, yamllint
- **Lint:** `ruff check src/ tests/`, `ruff format --check src/ tests/`
- **Typecheck:** `mypy src/`, `ty check src tests`
- **Test:** `pytest --cov=src --cov-branch --cov-fail-under=100`
- **Audit:** `uv sync --check --frozen --group dev`, `uv lock --check`,
  `pip-audit`, `pip-licenses` (centralized allowlist)
- **Custom:** `scripts/bin/validate-custom` (version validation)

## Manual validation (without vergil-tooling)

```bash
uv run ruff check
uv run ruff format --check .
uv run mypy src tests
uv run pytest --cov=diogenes --cov-branch --cov-fail-under=100
```
