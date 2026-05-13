# Diogenes Migration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transfer and rename `wphillipmoore/ai-research-methodology` to
`diogenes-project/diogenes`, flatten the plugin directory structure,
update all references to post-VERGIL names, and release `v0.2.0`.

**Architecture:** Single-repo migration — transfer, rename, restructure,
reference sweep, validate, release. No dependency chain to manage.

**Spec:** `docs/specs/2026-05-13-diogenes-migration-design.md`

**Relationship to org governance plan:** This is Plan B (migration).
The org governance plan
(`docs/plans/2026-05-13-diogenes-org-governance-setup.md`) is Plan A.
Plan A Tasks 1–5 must complete before this plan begins. Plan A Tasks
6–10 execute after this plan completes.

**Prerequisites:**
- VERGIL rename complete (all tooling at post-VERGIL names)
- `diogenes-project` org governance Phase 1 complete (Tasks 1–5)
- No open PRs on `wphillipmoore/ai-research-methodology`
- Clean working state on `develop`

---

## Task 1: Pre-Flight Checks

**Files:** None (verification only)

- [ ] **Step 1: Verify no open PRs**

  ```bash
  gh pr list --repo wphillipmoore/ai-research-methodology --state open
  ```

  Expected: no open PRs. If any exist, merge or close them first.

- [ ] **Step 2: Verify clean working state**

  ```bash
  cd ~/dev/github/ai-research-methodology
  git status
  git log --oneline -5
  ```

  Expected: on `develop`, clean working tree, up to date with origin.

- [ ] **Step 3: Verify org governance Phase 1 is complete**

  ```bash
  gh api orgs/diogenes-project --jq '.login'
  # Expected: diogenes-project

  security find-generic-password -s "diogenes/human-pat" -w > /dev/null \
    && echo "human-pat: OK"

  gh api orgs/diogenes-project/installations --jq '.[].app_slug'
  # Expected: diogenes-release
  ```

- [ ] **Step 4: Verify vergil-actions v2.0 exists**

  ```bash
  gh release view v2.0.0 --repo vergil-project/vergil-actions \
    --json tagName --jq '.tagName'
  ```

  Expected: `v2.0.0`. If this fails, the VERGIL rename is not
  complete — do not proceed.

---

## Task 2: Transfer and Rename

**Files:** None (GitHub API operations)

- [ ] **Step 1: Transfer repo to org**

  ```bash
  gh api repos/wphillipmoore/ai-research-methodology/transfer \
    -f new_owner=diogenes-project --silent
  ```

  Wait ~30 seconds for GitHub to process.

- [ ] **Step 2: Rename repo**

  ```bash
  gh repo rename diogenes \
    --repo diogenes-project/ai-research-methodology --yes
  ```

- [ ] **Step 3: Verify transfer and rename**

  ```bash
  gh repo view diogenes-project/diogenes \
    --json nameWithOwner --jq '.nameWithOwner'
  ```

  Expected: `diogenes-project/diogenes`

- [ ] **Step 4: Update local remote**

  ```bash
  cd ~/dev/github/ai-research-methodology
  git remote set-url origin git@github.com:diogenes-project/diogenes.git
  git fetch origin
  ```

- [ ] **Step 5: Create release branch**

  ```bash
  git checkout -b release/0.2.0
  ```

---

## Task 3: Flatten Plugin Directory

**Files:**
- Move: `ai-research-methodology/skills/` → `skills/`
- Move: `ai-research-methodology/standalone/` → `standalone/`
- Delete: `ai-research-methodology/` (after contents moved)
- Modify: `.claude-plugin/marketplace.json`
- Modify: `.claude-plugin/plugin.json` (replace with nested copy)

This task commits directory moves separately from content changes to
preserve `git log --follow` history.

- [ ] **Step 1: Move skill and standalone directories to repo root**

  ```bash
  git mv ai-research-methodology/skills skills
  git mv ai-research-methodology/standalone standalone
  ```

- [ ] **Step 2: Replace top-level plugin.json with nested copy**

  ```bash
  cp ai-research-methodology/.claude-plugin/plugin.json \
    .claude-plugin/plugin.json
  ```

  The content will be updated in Task 4 (reference updates).

- [ ] **Step 3: Remove the now-empty wrapper directory**

  ```bash
  rm -rf ai-research-methodology/
  git add -A
  ```

- [ ] **Step 4: Commit directory restructure**

  ```bash
  vrg-commit --type refactor --scope plugin \
    --message "flatten plugin directory to repo root" \
    --body "Move skills/ and standalone/ from ai-research-methodology/ wrapper to repo root, matching vergil-claude-plugin layout. The ai-research-methodology/ directory is removed." \
    --agent agent
  ```

---

## Task 4: Update Plugin Configuration

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update plugin.json**

  Replace `.claude-plugin/plugin.json` with:

  ```json
  {
    "name": "diogenes",
    "description": "Diogenes — deterministic AI research methodology combining ICD 203, GRADE, PRISMA, Cochrane, and five other frameworks into an evidence-based process. Anti-sycophantic by design.",
    "author": {
      "name": "W. Phillip Moore",
      "email": "w.phillip.moore@gmail.com"
    },
    "homepage": "https://github.com/diogenes-project/diogenes",
    "repository": "https://github.com/diogenes-project/diogenes",
    "license": "GPL-3.0-only",
    "keywords": [
      "research",
      "methodology",
      "fact-checking",
      "evidence",
      "ICD-203",
      "GRADE",
      "PRISMA",
      "anti-sycophancy",
      "claim-verification",
      "intelligence-analysis"
    ]
  }
  ```

- [ ] **Step 2: Update marketplace.json**

  Replace `.claude-plugin/marketplace.json` with:

  ```json
  {
    "name": "diogenes",
    "owner": {
      "name": "W. Phillip Moore",
      "email": "w.phillip.moore@gmail.com"
    },
    "metadata": {
      "description": "Deterministic AI research methodology for evidence-based investigation",
      "version": "0.2.0"
    },
    "plugins": [
      {
        "name": "diogenes",
        "source": ".",
        "description": "Deterministic AI research methodology combining ICD 203, GRADE, PRISMA, Cochrane, and five other frameworks into an evidence-based process. Anti-sycophantic by design.",
        "version": "0.2.0",
        "author": {
          "name": "W. Phillip Moore",
          "email": "w.phillip.moore@gmail.com"
        },
        "homepage": "https://github.com/diogenes-project/diogenes",
        "repository": "https://github.com/diogenes-project/diogenes",
        "license": "GPL-3.0-only",
        "keywords": ["research", "methodology", "fact-checking", "evidence", "anti-sycophancy"]
      }
    ]
  }
  ```

- [ ] **Step 3: Commit**

  ```bash
  vrg-commit --type refactor --scope plugin \
    --message "update plugin namespace and metadata for diogenes" \
    --body "Plugin namespace changes from ai-research-methodology to diogenes. Skill invocation becomes /diogenes:research. All URLs point to diogenes-project/diogenes." \
    --agent agent
  ```

---

## Task 5: Update Tooling Configuration

**Files:**
- Rename: `standard-tooling.toml` → `vergil.toml`
- Modify: `vergil.toml` (contents)
- Modify: `.githooks/pre-commit`

- [ ] **Step 1: Rename config file**

  ```bash
  git mv standard-tooling.toml vergil.toml
  ```

- [ ] **Step 2: Update vergil.toml contents**

  Replace the full file with:

  ```toml
  [project]
  repository-type = "library"
  versioning-scheme = "library"
  branching-model = "library-release"
  release-model = "artifact-publishing"
  primary-language = "python"

  [project.co-authors]
  agent = "Co-Authored-By: wphillipmoore-agent <AGENT_ID+wphillipmoore-agent@users.noreply.github.com>"

  [ci]
  versions = ["3.14"]
  integration-tests = false

  [publish]
  release = true

  [dependencies]
  vergil = "v2.0"
  ```

  Replace `AGENT_ID` with the actual GitHub user ID for
  `wphillipmoore-agent` (obtained during VERGIL governance setup):

  ```bash
  gh api users/wphillipmoore-agent --jq '.id'
  ```

- [ ] **Step 3: Update pre-commit hook**

  In `.githooks/pre-commit`, make the following replacements:

  - `st-commit` → `vrg-commit` (all occurrences)
  - `ST_COMMIT_CONTEXT` → `VRG_COMMIT_CONTEXT` (all occurrences)
  - `standard-tooling` → `vergil-tooling` (comment references)
  - `standard-tooling-plugin` → `vergil-claude-plugin` (comment
    references)

- [ ] **Step 4: Commit**

  ```bash
  vrg-commit --type refactor --scope config \
    --message "migrate to vergil.toml and vrg-commit" \
    --body "Rename standard-tooling.toml to vergil.toml, update dependency to vergil v2.0, consolidate co-author config to single agent entry, and update pre-commit hook to use vrg-commit." \
    --agent agent
  ```

---

## Task 6: Update CI/CD Workflows

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `.github/workflows/cd.yml`
- Modify: `.github/ISSUE_TEMPLATE/config.yml`
- Modify: `.github/ISSUE_TEMPLATE/issue.yml`

- [ ] **Step 1: Update ci.yml**

  Replace all occurrences:
  - Comment URL: `wphillipmoore/standard-actions` →
    `vergil-project/vergil-actions`
  - All `uses:` lines: `wphillipmoore/standard-actions/...@v1.5` →
    `vergil-project/vergil-actions/...@v2.0`

  ```bash
  sed -i '' \
    -e 's|wphillipmoore/standard-actions|vergil-project/vergil-actions|g' \
    -e 's|@v1\.5|@v2.0|g' \
    .github/workflows/ci.yml
  ```

- [ ] **Step 2: Update cd.yml**

  Same replacements:

  ```bash
  sed -i '' \
    -e 's|wphillipmoore/standard-actions|vergil-project/vergil-actions|g' \
    -e 's|@v1\.5|@v2.0|g' \
    .github/workflows/cd.yml
  ```

- [ ] **Step 3: Update issue templates**

  ```bash
  sed -i '' \
    's|wphillipmoore/standard-tooling|vergil-project/vergil-tooling|g' \
    .github/ISSUE_TEMPLATE/config.yml \
    .github/ISSUE_TEMPLATE/issue.yml
  ```

- [ ] **Step 4: Verify no old references remain in .github/**

  ```bash
  grep -rn "wphillipmoore\|standard-actions\|standard-tooling" \
    .github/ --include="*.yml"
  ```

  Expected: zero matches.

- [ ] **Step 5: Commit**

  ```bash
  vrg-commit --type refactor --scope ci \
    --message "update workflows and templates for vergil-actions v2.0" \
    --body "Point CI/CD workflows at vergil-project/vergil-actions@v2.0 and update issue template source comments to vergil-project/vergil-tooling." \
    --agent agent
  ```

---

## Task 7: Update Python Project Metadata

**Files:**
- Modify: `pyproject.toml`
- Modify: `src/diogenes/mcp_server.py`

- [ ] **Step 1: Update pyproject.toml**

  Change the version:

  ```toml
  version = "0.2.0"
  ```

  Change the URLs:

  ```toml
  [project.urls]
  Homepage = "https://github.com/diogenes-project/diogenes"
  Repository = "https://github.com/diogenes-project/diogenes"
  Issues = "https://github.com/diogenes-project/diogenes/issues"
  ```

- [ ] **Step 2: Update mcp_server.py example path**

  Replace the example path reference:
  - `/path/to/ai-research-methodology` → `/path/to/diogenes`

- [ ] **Step 3: Verify no old references remain in Python source**

  ```bash
  grep -rn "ai-research-methodology\|wphillipmoore" \
    src/ --include="*.py"
  ```

  Expected: zero matches.

- [ ] **Step 4: Commit**

  ```bash
  vrg-commit --type refactor --scope project \
    --message "update project metadata for diogenes-project/diogenes" \
    --body "Bump version to 0.2.0 and update all project URLs to diogenes-project/diogenes." \
    --agent agent
  ```

---

## Task 8: Update Schema URLs

**Files:**
- Modify: `docs/specs/schemas/research-input.schema.json`
- Modify: `src/diogenes/schemas/*.json` (any with `$id` URLs)
- Modify: `skills/research/prompts/compiled/*.md`

- [ ] **Step 1: Update source schema $id URLs**

  ```bash
  find docs/specs/schemas src/diogenes/schemas -name '*.json' \
    -exec grep -l 'wphillipmoore/ai-research-methodology' {} \; \
    | xargs sed -i '' \
      's|wphillipmoore/ai-research-methodology|diogenes-project/diogenes|g'
  ```

- [ ] **Step 2: Update compiled prompt schema URLs**

  ```bash
  find skills/research/prompts/compiled -name '*.md' \
    -exec sed -i '' \
      's|wphillipmoore/ai-research-methodology|diogenes-project/diogenes|g' \
      {} +
  ```

- [ ] **Step 3: Verify no old URLs remain**

  ```bash
  grep -rn "wphillipmoore/ai-research-methodology" \
    docs/specs/schemas/ src/diogenes/schemas/ \
    skills/research/prompts/compiled/
  ```

  Expected: zero matches.

- [ ] **Step 4: Commit**

  ```bash
  vrg-commit --type refactor --scope schemas \
    --message 'update schema $id URLs for diogenes-project/diogenes' \
    --agent agent
  ```

---

## Task 9: Update Scripts

**Files:**
- Modify: `scripts/compile-prompts.py`

- [ ] **Step 1: Update output path constants**

  In `scripts/compile-prompts.py`, change:

  ```python
  SKILL_COMPILED_DIR = REPO_ROOT / "ai-research-methodology" / "skills" / "research" / "prompts" / "compiled"
  STANDALONE_PATH = REPO_ROOT / "ai-research-methodology" / "standalone" / "research.md"
  ```

  To:

  ```python
  SKILL_COMPILED_DIR = REPO_ROOT / "skills" / "research" / "prompts" / "compiled"
  STANDALONE_PATH = REPO_ROOT / "standalone" / "research.md"
  ```

- [ ] **Step 2: Update docstring references**

  Replace `ai-research-methodology/skills/research/prompts/compiled/`
  with `skills/research/prompts/compiled/` and
  `ai-research-methodology/standalone/research.md` with
  `standalone/research.md` in the module docstring.

- [ ] **Step 3: Run the script to verify output**

  ```bash
  python scripts/compile-prompts.py
  ```

  Expected: script completes without error, compiled files exist at
  `skills/research/prompts/compiled/`.

- [ ] **Step 4: Commit**

  ```bash
  vrg-commit --type refactor --scope scripts \
    --message "update compile-prompts paths for flattened plugin layout" \
    --agent agent
  ```

---

## Task 10: Update Documentation

**Files:**
- Modify: `CLAUDE.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/standards-and-conventions.md`
- Modify: `docs/tech-debt-register.md`
- Modify: `docs/design/tooling-integration.md`
- Modify: `skills/research/SKILL.md` (if old-name references exist)

- [ ] **Step 1: Update CLAUDE.md**

  This is the largest documentation file. Apply the following
  replacements:

  ```bash
  sed -i '' \
    -e 's|ai-research-methodology|diogenes|g' \
    -e 's|wphillipmoore/standards-and-conventions|vergil-project/vergil-tooling (active docs)|g' \
    -e 's|wphillipmoore/standard-tooling/blob/develop|vergil-project/vergil-tooling/blob/develop|g' \
    -e 's|wphillipmoore/standard-actions|vergil-project/vergil-actions|g' \
    -e "s|standard-tooling-plugin|vergil-claude-plugin|g" \
    -e 's|standard-tooling\.toml|vergil.toml|g' \
    -e 's|standard-tooling|vergil-tooling|g' \
    -e 's|st-docker-run|vrg-docker-run|g' \
    -e 's|st-validate|vrg-validate|g' \
    -e 's|st-commit|vrg-commit|g' \
    -e 's|ST_COMMIT_CONTEXT|VRG_COMMIT_CONTEXT|g' \
    CLAUDE.md
  ```

  **Manual review required** after sed — CLAUDE.md has nuanced
  references (worktree paths, agent prompt contract, etc.) that
  may need manual adjustment. In particular:

  - `~/dev/github/ai-research-methodology/` →
    `~/dev/github/diogenes/`
  - Plugin directory references: `ai-research-methodology/` → root
    paths (`skills/`, `standalone/`)
  - Host install command: update to vergil-tooling

- [ ] **Step 2: Update AGENTS.md**

  ```bash
  sed -i '' \
    -e 's|ai-research-methodology|diogenes|g' \
    -e 's|wphillipmoore/standards-and-conventions|vergil-project/vergil-tooling (active docs)|g' \
    -e 's|standard-tooling-plugin|vergil-claude-plugin|g' \
    -e 's|standard-tooling|vergil-tooling|g' \
    AGENTS.md
  ```

- [ ] **Step 3: Update README.md**

  ```bash
  sed -i '' \
    -e 's|ai-research-methodology|diogenes|g' \
    -e 's|wphillipmoore|diogenes-project|g' \
    README.md
  ```

  **Manual review required** — the README has plugin install
  commands and usage examples that need to reference the new
  `diogenes` namespace correctly.

- [ ] **Step 4: Update docs/ files**

  ```bash
  sed -i '' \
    -e 's|ai-research-methodology|diogenes|g' \
    -e 's|wphillipmoore/standards-and-conventions|vergil-project/vergil-tooling (active docs)|g' \
    -e 's|wphillipmoore/standard-tooling|vergil-project/vergil-tooling|g' \
    -e 's|wphillipmoore|diogenes-project|g' \
    -e 's|standard-tooling\.toml|vergil.toml|g' \
    -e 's|standard-tooling|vergil-tooling|g' \
    docs/standards-and-conventions.md \
    docs/tech-debt-register.md \
    docs/design/tooling-integration.md
  ```

- [ ] **Step 5: Update skill file if needed**

  ```bash
  grep -n "ai-research-methodology" skills/research/SKILL.md
  ```

  If matches found, update them. The SKILL.md may reference the
  plugin directory path or the standalone prompt path.

- [ ] **Step 6: Final grep for any remaining old references**

  ```bash
  grep -rn "ai-research-methodology\|wphillipmoore\|standard-tooling\|st-commit\|st-validate\|st-docker\|ST_COMMIT" \
    --include="*.py" --include="*.md" --include="*.toml" \
    --include="*.yml" --include="*.yaml" --include="*.json" \
    --include="*.sh" . \
    | grep -v CHANGELOG.md | grep -v .git/
  ```

  Expected: zero matches outside of historical files. Fix any
  remaining references.

- [ ] **Step 7: Commit**

  ```bash
  vrg-commit --type docs \
    --message "update all documentation for diogenes-project/diogenes" \
    --body "Replace ai-research-methodology with diogenes, wphillipmoore with diogenes-project (for repo refs) and vergil-project (for tooling refs), and all standard-tooling references with vergil-tooling equivalents." \
    --agent agent
  ```

---

## Task 11: Validate and Release

- [ ] **Step 1: Run full validation**

  ```bash
  vrg-docker-run -- uv run vrg-validate
  ```

  If this fails because host tools are still named `st-*`, use:

  ```bash
  uv run pytest tests/ -v
  uv run ruff check src/ tests/
  uv run ruff format --check .
  uv run mypy src tests
  ```

- [ ] **Step 2: Run compile-prompts to verify output**

  ```bash
  python scripts/compile-prompts.py
  git diff --stat
  ```

  If the compiled prompts changed (updated URLs), stage and commit
  them:

  ```bash
  vrg-commit --type refactor --scope prompts \
    --message "recompile prompts with updated schema URLs" \
    --agent agent
  ```

- [ ] **Step 3: Fix any failures**

  If tests or linting fail, fix the issues and commit each fix.

- [ ] **Step 4: Push and open PR**

  ```bash
  git push -u origin release/0.2.0
  ```

  Open PR targeting `develop`:

  ```bash
  gh pr create \
    --repo diogenes-project/diogenes \
    --title "feat!: migrate to diogenes-project/diogenes" \
    --body "$(cat <<'EOF'
  ## Summary

  Completes the migration of ai-research-methodology to diogenes-project/diogenes (#210).

  - Transfer repo to diogenes-project org, rename to diogenes
  - Flatten plugin directory to repo root (matching vergil-claude-plugin layout)
  - Plugin namespace: ai-research-methodology → diogenes
  - Config: standard-tooling.toml → vergil.toml (vergil v2.0)
  - CI: wphillipmoore/standard-actions@v1.5 → vergil-project/vergil-actions@v2.0
  - Pre-commit: st-commit → vrg-commit
  - Co-authors: consolidated to single agent entry
  - Version: 0.1.0 → 0.2.0

  ## Test plan

  - [ ] `vrg-docker-run -- uv run vrg-validate` passes
  - [ ] `uv run pytest -v` passes
  - [ ] CI passes on PR
  - [ ] No remaining references to ai-research-methodology or wphillipmoore
  - [ ] `python scripts/compile-prompts.py` succeeds with flattened paths
  - [ ] Plugin installs under new namespace (`/diogenes:research`)

  Closes #210
  EOF
  )"
  ```

- [ ] **Step 5: Iterate on CI failures**

  If CI fails, fix issues, commit, push.

- [ ] **Step 6: Merge and tag release**

  After CI passes and PR is approved, merge. Then follow the repo's
  release workflow to create the `v0.2.0` tag and GitHub release.

---

## Task 12: Cross-Repo Cleanup

- [ ] **Step 1: Update VERGIL consumer manifest**

  In `vergil-project/vergil-tooling`, update the consumer repo
  manifest in `docs/plans/2026-05-11-vergil-rename.md` Task 11 to
  note that `ai-research-methodology` has moved to
  `diogenes-project/diogenes`.

- [ ] **Step 2: Search for cross-references**

  ```bash
  for repo in $(gh repo list wphillipmoore --limit 100 --json name \
    --jq '.[] | .name'); do
    matches=$(gh api repos/wphillipmoore/$repo/git/ref/heads/develop \
      --jq '.object.sha' 2>/dev/null)
    if [ -n "$matches" ]; then
      result=$(gh api \
        "repos/wphillipmoore/$repo/git/trees/$matches?recursive=1" \
        --jq '.tree[].path' 2>/dev/null \
        | grep -E '\.(md|toml|yml|json)$' | head -5)
    fi
  done
  ```

  Alternatively, search directly:

  ```bash
  gh search code "ai-research-methodology" --owner wphillipmoore \
    --json repository,path --jq '.[] | "\(.repository.fullName): \(.path)"'
  ```

  Update any cross-references found.

---

## Task 13: Local Cleanup

- [ ] **Step 1: Rename local directory**

  ```bash
  cd ~/dev/github
  mv ai-research-methodology diogenes
  cd diogenes
  ```

- [ ] **Step 2: Verify remote**

  ```bash
  git remote -v
  ```

  Expected: `origin git@github.com:diogenes-project/diogenes.git`

- [ ] **Step 3: Clean up worktrees**

  ```bash
  git worktree list
  git worktree prune
  rm -rf .worktrees/
  ```

- [ ] **Step 4: Reinstall plugin**

  Update Claude Code plugin source from
  `wphillipmoore/ai-research-methodology` to
  `diogenes-project/diogenes`.

- [ ] **Step 5: Verify skill loads**

  In a Claude Code session, confirm `/diogenes:research` loads and
  the skill content is correct.

- [ ] **Step 6: Smoke test end-to-end**

  ```bash
  cd ~/dev/github/diogenes
  vrg-docker-run -- uv run vrg-validate
  ```

  This proves: host tools work, config parsed from `vergil.toml`,
  docker images pulled, validation runs.

- [ ] **Step 7: Migrate Claude Code memory**

  The memory directory slug changes because the CWD path changes.
  Review memories at the old path and move any that are still
  relevant to the new path:

  ```
  Old: ~/.claude/projects/-Users-pmoore-dev-github-ai-research-methodology/memory/
  New: ~/.claude/projects/-Users-pmoore-dev-github-diogenes/memory/
  ```
