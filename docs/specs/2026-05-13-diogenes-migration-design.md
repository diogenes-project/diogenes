# Diogenes Migration Design

**Date:** 2026-05-13
**Status:** Draft

## Problem

The repository `wphillipmoore/ai-research-methodology` needs to move to
`diogenes-project/diogenes`. The `ai-research-methodology` name is being
dropped completely — the project is Diogenes. The move involves a GitHub
transfer, repo rename, plugin namespace change, directory restructure,
and reference sweep.

## Prerequisites

1. **VERGIL rename complete.** All references target post-VERGIL names:
   `vergil-project/vergil-actions`, `vergil.toml`, `vrg-commit`, etc.

2. **`diogenes-project` org governance complete.** The org exists with
   security settings, rulesets, credentials, and GitHub App configured
   per `docs/specs/2026-05-13-diogenes-org-governance-design.md`.

## Scope

This is a single-repo migration. Unlike the VERGIL rename (four repos
in dependency order), Diogenes has no downstream consumers that depend
on it as a package. The blast radius is contained to this repo and
cross-references from other repos.

### What changes

| Category | Before | After |
|---|---|---|
| GitHub location | `wphillipmoore/ai-research-methodology` | `diogenes-project/diogenes` |
| Plugin namespace | `ai-research-methodology` | `diogenes` |
| Plugin directory | `ai-research-methodology/` (nested) | Flattened to repo root |
| Skill invocation | `/ai-research-methodology:research` | `/diogenes:research` |
| Config file | `standard-tooling.toml` | `vergil.toml` |
| Tooling dependency | `standard-tooling = "v1.4"` | `vergil = "v2.0"` |
| Co-authors | `claude`, `codex` (per-harness) | `agent` (single entry) |
| Pre-commit hook | `st-commit` / `ST_COMMIT_CONTEXT` | `vrg-commit` / `VRG_COMMIT_CONTEXT` |
| CI workflows | `wphillipmoore/standard-actions@v1.5` | `vergil-project/vergil-actions@v2.0` |
| Python package name | `diogenes` | `diogenes` (unchanged) |
| CLI entry points | `dio`, `diogenes`, `dio-mcp` | unchanged |
| Python module path | `src/diogenes/` | unchanged |
| Version | `0.1.0` / `1.9.1` | `2.0.0` (unified) |

### What does NOT change

- Python package name (`diogenes`) — already correct
- Python module directory (`src/diogenes/`)
- CLI entry points (`dio`, `diogenes`, `dio-mcp`)
- Test directory structure (`tests/`)
- Source code imports (`from diogenes...`, `import diogenes`)
- License (GPL-3.0-only)

## Section 1: Transfer and Rename

Transfer `wphillipmoore/ai-research-methodology` to the
`diogenes-project` org via the GitHub API, then rename to `diogenes`.
GitHub creates automatic redirects from the old URL.

**Pre-flight checks:**
- No open PRs on the repo
- Clean working state on `develop`
- All CI passing

**Post-transfer:**
- Update local git remote to `git@github.com:diogenes-project/diogenes.git`
- Create feature branch for migration changes (e.g. `feature/210-diogenes-move`)
- All migration work merges to `develop` via PR; cut `release/2.0.0`
  from `develop` after merge

## Section 2: Plugin Directory Flattening

The current structure nests the plugin content under a wrapper
directory:

```
ai-research-methodology/           <- plugin wrapper dir
  .claude-plugin/plugin.json        <- nested plugin config
  skills/research/...               <- skill files
  standalone/research.md            <- standalone prompt
.claude-plugin/marketplace.json     <- top-level marketplace
```

The target structure matches `vergil-claude-plugin` — plugin content
at repo root:

```
.claude-plugin/
  plugin.json                       <- merged from nested copy
  marketplace.json                  <- updated source path
skills/research/...                 <- moved to root
standalone/research.md              <- moved to root
```

### Changes required

- `git mv ai-research-methodology/skills skills`
- `git mv ai-research-methodology/standalone standalone`
- Replace top-level `.claude-plugin/marketplace.json` — update
  `"source"` from `"./ai-research-methodology"` to `"."`
- Replace top-level `.claude-plugin/` content with the nested
  `ai-research-methodology/.claude-plugin/plugin.json` (updated with
  new names/URLs)
- Delete the now-empty `ai-research-methodology/` directory
- Update `scripts/compile-prompts.py` — output paths change from
  `ai-research-methodology/skills/research/prompts/compiled/` to
  `skills/research/prompts/compiled/` and
  `ai-research-methodology/standalone/research.md` to
  `standalone/research.md`

### Commit strategy

The directory moves are committed separately from reference updates to
preserve `git log --follow` history.

## Section 3: Reference Updates

**Commit ordering:** The pre-commit hook update (Section 3.4) must be
the first commit on the migration branch. The current hook checks for
`ST_COMMIT_CONTEXT=1` and references `st-commit`, but only `vrg-commit`
is installed on the host. Until the hook is updated, `vrg-commit` cannot
commit to this repo.

A bulk sweep of all files that reference the old name, org, or
pre-VERGIL tooling. Since VERGIL is complete, references jump directly
from the old names to the post-VERGIL names.

### 3.1 Plugin configuration

**`.claude-plugin/plugin.json`:**
- `"name"`: `"ai-research-methodology"` -> `"diogenes"`
- `"homepage"`: -> `https://github.com/diogenes-project/diogenes`
- `"repository"`: -> `https://github.com/diogenes-project/diogenes`

**`.claude-plugin/marketplace.json`:**
- `"name"`: `"ai-research-methodology"` -> `"diogenes"`
- `"source"`: `"./ai-research-methodology"` -> `"."`
- All nested `"name"`, `"homepage"`, `"repository"` fields updated
- Version updated to `2.0.0`

**Version unification:** The plugin (`marketplace.json`, currently
`1.9.1`) and Python package (`pyproject.toml`, currently `0.1.0`) adopt
a single unified version (`2.0.0`) going forward. The old independent
plugin versioning scheme is retired as part of this migration.

**Note:** Having both a Python package and a Claude plugin in one repo
creates a potential tooling conflict — `vergil-tooling` assumes one
version file per repo and has a `claude-plugin` language type with its
own versioning expectations. This may require tooling changes or a repo
split in the future.

### 3.2 Python project metadata

**`pyproject.toml`:**
- `version`: `"0.1.0"` -> `"2.0.0"`
- `Homepage`: -> `https://github.com/diogenes-project/diogenes`
- `Repository`: -> `https://github.com/diogenes-project/diogenes`
- `Issues`: -> `https://github.com/diogenes-project/diogenes/issues`

### 3.3 Tooling configuration

**`standard-tooling.toml` -> `vergil.toml`:**
- Rename file via `git mv`
- `[dependencies]`: `standard-tooling = "v1.4"` -> `vergil = "v2.0"`
- `[project.co-authors]`: replace `claude` and `codex` entries with
  single `agent` entry using `wphillipmoore-agent` noreply email

### 3.4 Pre-commit hook

**`.githooks/pre-commit`:**
- `st-commit` -> `vrg-commit` (all occurrences including error message)
- `ST_COMMIT_CONTEXT` -> `VRG_COMMIT_CONTEXT`
- Comment references: `standard-tooling` -> `vergil-tooling`,
  `standard-tooling-plugin` -> `vergil-claude-plugin`

### 3.5 CI/CD workflows

**`.github/workflows/ci.yml`:**
- Comment URL: `wphillipmoore/standard-actions` ->
  `vergil-project/vergil-actions`
- All `uses:` references: `wphillipmoore/standard-actions/...@v1.5` ->
  `vergil-project/vergil-actions/...@v2.0`

**`.github/workflows/cd.yml`:**
- Same pattern as ci.yml

### 3.6 Issue templates

**`.github/ISSUE_TEMPLATE/config.yml`:**
- Source comment: `wphillipmoore/standard-tooling` ->
  `vergil-project/vergil-tooling`

**`.github/ISSUE_TEMPLATE/issue.yml`:**
- Source comment: `wphillipmoore/standard-tooling` ->
  `vergil-project/vergil-tooling`

### 3.7 Schema `$id` URLs

Compiled prompts and source schema files contain `$id` URLs pointing
at the old GitHub URLs. Two URL patterns need updating:

**Pattern 1** (source schemas + compiled prompts): All instances of:
```
https://raw.githubusercontent.com/wphillipmoore/ai-research-methodology/main/src/diogenes/schemas/
```
become:
```
https://raw.githubusercontent.com/diogenes-project/diogenes/main/src/diogenes/schemas/
```

**Pattern 2** (`docs/specs/schemas/`): Uses a different format:
```
https://github.com/wphillipmoore/ai-research-methodology/schemas/
```
becomes:
```
https://github.com/diogenes-project/diogenes/schemas/
```
Note: this URL does not resolve to an actual file in the repo tree —
consider fixing the path to match the real schema location while
updating the org/repo segments.

Affected files:
- `src/diogenes/schemas/*.json` (16 files — all contain `$id` URLs)
- All files under `skills/research/prompts/compiled/*.md`
  (post-flattening path)
- `docs/specs/schemas/research-input.schema.json` (Pattern 2)

### 3.8 Python source

**`src/diogenes/mcp_server.py`:**
- Example path in docstring/comment:
  `/path/to/ai-research-methodology` -> `/path/to/diogenes`

### 3.9 Documentation

**`CLAUDE.md`:**
- All `ai-research-methodology` references -> `diogenes`
- All `wphillipmoore` repo references -> `diogenes-project` (for this
  repo) or `vergil-project` (for tooling references)
- Worktree paths: `~/dev/github/ai-research-methodology/` ->
  `~/dev/github/diogenes/`
- `standard-tooling` references -> `vergil-tooling`
- `standard-actions` references -> `vergil-actions`
- `st-docker-run`, `st-validate`, etc. -> `vrg-docker-run`,
  `vrg-validate`, etc.
- `standard-tooling.toml` -> `vergil.toml`
- Plugin directory references: `ai-research-methodology/` ->
  root-level paths (`skills/`, `standalone/`)
- Host install command updated to vergil-tooling

**`AGENTS.md`:**
- Title: `ai-research-methodology` -> `diogenes`
- Standards reference URL: `wphillipmoore/standards-and-conventions` ->
  note that active docs are in vergil-tooling
- `standard-tooling-plugin` -> `vergil-claude-plugin`

**`README.md`:**
- All `ai-research-methodology` references -> `diogenes`
- Plugin install commands updated for new namespace
- All `wphillipmoore` -> `diogenes-project`

**`docs/` files:**
- `docs/standards-and-conventions.md`: URL update
- `docs/tech-debt-register.md`: repo name reference
- `docs/design/tooling-integration.md`: repo name, tooling references
- Any other docs referencing the old name

### 3.10 Changelog config

**`cliff.toml` and `cliff-release-notes.toml`:**
- No repo-name references in these files — no changes needed.

### 3.11 Scripts

**`scripts/compile-prompts.py`:**
- `SKILL_COMPILED_DIR` path: `"ai-research-methodology"` ->
  `"skills"` (post-flattening)
- `STANDALONE_PATH`: `"ai-research-methodology"` -> `"standalone"`
- Docstring references updated

## Section 4: Validation and Release

After all changes:

1. Run `vrg-docker-run -- uv run vrg-validate` (full pre-commit
   validation)
2. Run `uv run pytest -v` (test suite)
3. Run `uv run mypy src tests` (type checking)
4. Fix any failures
5. Push feature branch, open PR to `develop`, iterate until CI passes
6. Merge to `develop`, cut `release/2.0.0`, merge and tag `v2.0.0`

## Section 5: Cross-Repo Cleanup

This repo appears in the VERGIL consumer manifest
(`vergil-tooling/docs/plans/2026-05-11-vergil-rename.md`, Task 11).
After migration:

- The VERGIL consumer manifest entry for `ai-research-methodology`
  should be updated to note it has moved to `diogenes-project/diogenes`
  (or removed from the list entirely, since it is no longer in the
  `wphillipmoore` org)
- Any other repos that reference `wphillipmoore/ai-research-methodology`
  should be updated (search across all repos in both orgs)

## Section 6: Local Cleanup

Post-merge housekeeping:

- Update local git remote
- Rename local directory: `~/dev/github/ai-research-methodology/` ->
  `~/dev/github/diogenes/`
- Clean up `.worktrees/` if any exist
- Reinstall plugin from new location
- Verify `/diogenes:research` skill loads correctly
- Update Claude Code memory files that reference the old repo path
  (the memory directory slug will change since CWD changes)

## Risks

| Risk | Mitigation |
|---|---|
| Compiled prompts contain hardcoded schema URLs that break after move | Grep-verify all `$id` URLs are updated; run validation |
| Plugin namespace change breaks existing skill installations | Pre-alpha, no external users; document the change in release notes |
| `scripts/compile-prompts.py` paths break after flattening | Update paths and run the script to verify output |
| Claude Code memory path changes when CWD changes | Document this; user migrates relevant memories manually |
| GitHub redirect from old URL eventually expires | GitHub maintains redirects indefinitely for transferred repos |
| CI workflows fail because vergil-actions reference is wrong | Verify `vergil-project/vergil-actions@v2.0` exists before pushing |

## File Map

Summary of every file touched, grouped by change type:

### Renamed/moved
- `standard-tooling.toml` -> `vergil.toml`
- `ai-research-methodology/skills/` -> `skills/`
- `ai-research-methodology/standalone/` -> `standalone/`
- `ai-research-methodology/.claude-plugin/plugin.json` -> merged into
  `.claude-plugin/plugin.json`

### Deleted
- `ai-research-methodology/` directory (after contents moved)

### Modified
- `.claude-plugin/marketplace.json`
- `.claude-plugin/plugin.json`
- `.githooks/pre-commit`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/issue.yml`
- `.github/workflows/cd.yml`
- `.github/workflows/ci.yml`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `pyproject.toml`
- `vergil.toml` (post-rename contents)
- `scripts/compile-prompts.py`
- `src/diogenes/mcp_server.py`
- `docs/design/tooling-integration.md`
- `docs/standards-and-conventions.md`
- `docs/tech-debt-register.md`
- `docs/specs/schemas/research-input.schema.json`
- `src/diogenes/schemas/*.json` (16 files — `$id` URL updates)
- `skills/research/SKILL.md`
- `skills/research/prompts/compiled/*.md` (schema `$id` URLs)

### Not modified
- `cliff.toml`, `cliff-release-notes.toml`
- `src/diogenes/**/*.py` (except `mcp_server.py`)
- `tests/` (no old-name references in test code)
- `uv.lock` (regenerated automatically)
- `CHANGELOG.md` (historical record, not updated)
