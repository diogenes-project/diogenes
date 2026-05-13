# Diogenes Org Governance Setup — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps
> use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configure the `diogenes-project` GitHub org with the same
governance model as `vergil-project` (identity separation, branch
protection, credential management, GitHub App) so that the Diogenes
migration (separate plan) can proceed into a properly configured org.

**Architecture:** Two-phase approach — manual infrastructure setup
(credentials, org settings, GitHub App) and post-migration governance
activation (agent invitation, org-level rulesets, verification). Phase 2
from the VERGIL governance plan (codebase preparation) is already
complete and is not repeated here.

**Spec:** `docs/specs/2026-05-13-diogenes-org-governance-design.md`

**Relationship to migration plan:** This is Plan A (org setup). The
migration plan (`docs/plans/2026-05-13-diogenes-migration.md`) is
Plan B. Plan A must complete through Task 5 before Plan B begins.
Tasks 6–10 execute after Plan B completes.

**Prerequisites:**
- VERGIL rename complete
- `wphillipmoore-agent` GitHub account exists (created during VERGIL
  setup)

---

## Phase 1: Manual Infrastructure Setup

These tasks are performed once, mostly via the GitHub web UI and `gh`
CLI. They establish the credentials and org configuration that the rest
of the plan depends on.

### Task 1: Verify Org Exists and Configure Security Settings

**Files:** None (`gh` CLI)

The `diogenes-project` org already exists. This task verifies it and
applies security settings.

- [ ] **Step 1: Verify org exists**

  ```bash
  gh api orgs/diogenes-project --jq '.login'
  ```

  Expected: `diogenes-project`

- [ ] **Step 2: Require 2FA for all org members**

  ```bash
  gh api orgs/diogenes-project \
    -X PATCH \
    -f two_factor_requirement_enabled=true
  ```

- [ ] **Step 3: Set default repository permission to Write**

  ```bash
  gh api orgs/diogenes-project \
    -X PATCH \
    -f default_repository_permission=write
  ```

- [ ] **Step 4: Disable forking of private repos**

  ```bash
  gh api orgs/diogenes-project \
    -X PATCH \
    -F members_can_fork_private_repositories=false
  ```

- [ ] **Step 5: Verify settings**

  ```bash
  gh api orgs/diogenes-project \
    --jq '{two_factor: .two_factor_requirement_enabled, default_perm: .default_repository_permission, fork_private: .members_can_fork_private_repositories}'
  ```

  Expected:
  ```json
  {
    "two_factor": true,
    "default_perm": "write",
    "fork_private": false
  }
  ```

### Task 2: Generate Human Fine-Grained PAT

**Files:** None (GitHub web UI)

- [ ] **Step 1: Generate the human PAT**

  Go to <https://github.com/settings/personal-access-tokens/new>
  (logged in as `wphillipmoore`).

  - Token name: `diogenes-human`
  - Expiration: 1 year
  - Resource owner: `diogenes-project`
  - Repository access: All repositories
  - Permissions:
    - Administration: Read and write
    - Contents: Read and write
    - Issues: Read and write
    - Pull requests: Read and write
    - Actions: Read and write
    - Metadata: Read (auto-granted)

  Copy the token value.

- [ ] **Step 2: Verify PAT scope is correct**

  ```bash
  GH_TOKEN=<human-pat> gh api user --jq '.login'
  ```

  Expected: `wphillipmoore`

### Task 3: Store Human PAT in macOS Keychain

**Files:** None (macOS Keychain)

- [ ] **Step 1: Store the human PAT**

  ```bash
  security add-generic-password \
    -a "diogenes" \
    -s "diogenes/human-pat" \
    -w "<paste-human-pat-here>" \
    -T "" \
    -U
  ```

- [ ] **Step 2: Verify retrieval**

  ```bash
  security find-generic-password -s "diogenes/human-pat" -w
  ```

  Should print the stored token.

### Task 4: Register `diogenes-release` GitHub App

**Files:** None (GitHub web UI + Keychain)

- [ ] **Step 1: Register the App**

  Go to <https://github.com/organizations/diogenes-project/settings/apps/new>

  - App name: `diogenes-release`
  - Homepage URL: `https://github.com/diogenes-project`
  - Webhook: uncheck "Active" (not needed)
  - Permissions:
    - Repository permissions:
      - Contents: Read and write
      - Pull requests: Read and write
      - Metadata: Read-only
    - No organization permissions
    - No account permissions
  - Where can this app be installed: Only on this account

- [ ] **Step 2: Generate a private key**

  On the App settings page, under "Private keys", click
  "Generate a private key". Download the `.pem` file.

- [ ] **Step 3: Store the App private key and ID in Keychain**

  ```bash
  # Store the App ID (visible on the App settings page)
  security add-generic-password \
    -a "diogenes" \
    -s "diogenes/app-id" \
    -w "<app-id>" \
    -T "" \
    -U

  # Store the private key (read from the downloaded .pem file)
  security add-generic-password \
    -a "diogenes" \
    -s "diogenes/app-private-key" \
    -w "$(cat /path/to/downloaded-key.pem)" \
    -T "" \
    -U
  ```

- [ ] **Step 4: Install the App on the org**

  Go to the App settings page → "Install App" → Install on
  `diogenes-project` → All repositories.

- [ ] **Step 5: Verify the installation**

  ```bash
  gh api orgs/diogenes-project/installations --jq '.[].app_slug'
  ```

  Expected: `diogenes-release`

- [ ] **Step 6: Delete the downloaded `.pem` file**

  ```bash
  rm /path/to/downloaded-key.pem
  ```

  The key is now stored in the Keychain only.

### Task 5: Pre-Migration Gate

**Files:** None (verification only)

- [ ] **Step 1: Verify all Phase 1 tasks are complete**

  ```bash
  # Org exists and configured
  gh api orgs/diogenes-project \
    --jq '{two_factor: .two_factor_requirement_enabled, default_perm: .default_repository_permission}'

  # Human PAT in Keychain
  security find-generic-password -s "diogenes/human-pat" -w > /dev/null && echo "human-pat: OK"

  # App installed
  gh api orgs/diogenes-project/installations --jq '.[].app_slug'

  # App credentials in Keychain
  security find-generic-password -s "diogenes/app-id" -w > /dev/null && echo "app-id: OK"
  security find-generic-password -s "diogenes/app-private-key" -w > /dev/null && echo "app-private-key: OK"
  ```

- [ ] **Step 2: Record completion**

  Phase 1 is complete. Plan B (the migration) can now proceed.

---

## Phase 2: Post-Migration Governance Activation

These tasks execute after Plan B (the migration) is complete and the
repo is at `diogenes-project/diogenes`.

### Task 6: Invite Agent Account to Org Repos

**Files:** None (`gh` CLI)

- [ ] **Step 1: List all repos in the org**

  ```bash
  gh repo list diogenes-project --json name --jq '.[].name'
  ```

- [ ] **Step 2: Invite `wphillipmoore-agent` as outside collaborator**

  ```bash
  for repo in $(gh repo list diogenes-project --json name --jq '.[].name'); do
    gh api repos/diogenes-project/$repo/collaborators/wphillipmoore-agent \
      -X PUT \
      -f permission=push
  done
  ```

- [ ] **Step 3: Accept the invitation**

  Log in as `wphillipmoore-agent` in the GitHub web UI and accept
  the collaboration invitation.

- [ ] **Step 4: Verify access**

  Confirm the org's repos are visible at
  `https://github.com/orgs/diogenes-project/repositories`.

- [ ] **Step 5: Generate the agent PAT**

  Go to <https://github.com/settings/personal-access-tokens/new>
  (logged in as `wphillipmoore-agent`).

  - Token name: `diogenes-agent`
  - Expiration: 1 year
  - Resource owner: `diogenes-project`
  - Repository access: All repositories
  - Permissions:
    - Contents: Read and write
    - Issues: Read and write
    - Pull requests: Read and write
    - Metadata: Read (auto-granted)
  - **Not granted:** Administration, Actions, org settings, secrets,
    deployments

  Copy the token value.

- [ ] **Step 6: Store the agent PAT in macOS Keychain**

  ```bash
  security add-generic-password \
    -a "diogenes" \
    -s "diogenes/agent-pat" \
    -w "<paste-agent-pat-here>" \
    -T "" \
    -U
  ```

- [ ] **Step 7: Verify agent PAT**

  ```bash
  # Verify identity
  GH_TOKEN=<agent-pat> gh api user --jq '.login'
  # Expected: wphillipmoore-agent

  # Verify Keychain retrieval
  security find-generic-password -s "diogenes/agent-pat" -w
  ```

### Task 7: Configure Org-Level Rulesets

**Files:** None (`gh` CLI)

- [ ] **Step 1: Create the branch protection ruleset for `develop`**

  ```bash
  gh api orgs/diogenes-project/rulesets \
    -X POST \
    --input - <<'JSON'
  {
    "name": "Branch protection (develop)",
    "target": "branch",
    "enforcement": "active",
    "conditions": {
      "ref_name": {
        "include": ["refs/heads/develop"],
        "exclude": []
      }
    },
    "rules": [
      { "type": "pull_request",
        "parameters": {
          "required_approving_review_count": 1,
          "dismiss_stale_reviews_on_push": true,
          "require_code_owner_review": false,
          "require_last_push_approval": true,
          "required_review_thread_resolution": true
        }
      },
      { "type": "required_status_checks",
        "parameters": {
          "strict_status_checks_policy": true,
          "status_checks": []
        }
      },
      { "type": "deletion" },
      { "type": "non_fast_forward" }
    ],
    "bypass_actors": []
  }
  JSON
  ```

  **Note:** `bypass_actors: []` means no one can bypass — not even
  org owners. `status_checks` is empty at the org level because CI
  check names vary by repo.

- [ ] **Step 2: Create the branch protection ruleset for `main`**

  ```bash
  gh api orgs/diogenes-project/rulesets \
    -X POST \
    --input - <<'JSON'
  {
    "name": "Branch protection (main)",
    "target": "branch",
    "enforcement": "active",
    "conditions": {
      "ref_name": {
        "include": ["refs/heads/main"],
        "exclude": []
      }
    },
    "rules": [
      { "type": "pull_request",
        "parameters": {
          "required_approving_review_count": 1,
          "dismiss_stale_reviews_on_push": true,
          "require_code_owner_review": false,
          "require_last_push_approval": true,
          "required_review_thread_resolution": true
        }
      },
      { "type": "required_status_checks",
        "parameters": {
          "strict_status_checks_policy": true,
          "status_checks": []
        }
      },
      { "type": "deletion" },
      { "type": "non_fast_forward" }
    ],
    "bypass_actors": []
  }
  JSON
  ```

- [ ] **Step 3: Verify rulesets are active**

  ```bash
  gh api orgs/diogenes-project/rulesets \
    --jq '.[] | {name: .name, enforcement: .enforcement}'
  ```

  Expected:
  ```json
  {"name": "Branch protection (develop)", "enforcement": "active"}
  {"name": "Branch protection (main)", "enforcement": "active"}
  ```

### Task 8: Test Rulesets

**Files:** None (manual verification)

- [ ] **Step 1: Verify direct push is blocked**

  Create a test branch in `diogenes-project/diogenes` and attempt
  to push directly to `develop`:

  ```bash
  cd /tmp && git clone git@github.com:diogenes-project/diogenes.git diogenes-test
  cd diogenes-test
  git checkout develop
  echo "test" >> /tmp/test-rulesets
  git add /tmp/test-rulesets
  git commit -m "test: verify branch protection"
  git push origin develop
  ```

  Expected: push rejected with a message about branch protection.

- [ ] **Step 2: Verify PR without review is blocked**

  ```bash
  git checkout -b test/verify-rulesets
  echo "test" > test-rulesets.txt
  git add test-rulesets.txt
  git commit -m "test: verify branch protection"
  git push -u origin test/verify-rulesets

  GH_TOKEN=<agent-pat> gh pr create \
    --repo diogenes-project/diogenes \
    --title "test: verify branch protection" \
    --body "Testing governance rulesets. Will delete." \
    --head test/verify-rulesets \
    --base develop

  # Attempt to merge without approval — should fail
  GH_TOKEN=<agent-pat> gh pr merge <PR-NUMBER> \
    --repo diogenes-project/diogenes \
    --merge
  ```

  Expected: merge rejected — required reviews not satisfied.

- [ ] **Step 3: Verify human approval enables merge**

  ```bash
  # Approve as human
  GH_TOKEN=<human-pat> gh pr review <PR-NUMBER> \
    --repo diogenes-project/diogenes \
    --approve

  # Merge as human
  GH_TOKEN=<human-pat> gh pr merge <PR-NUMBER> \
    --repo diogenes-project/diogenes \
    --merge
  ```

  Expected: merge succeeds.

- [ ] **Step 4: Clean up test branch**

  ```bash
  gh api repos/diogenes-project/diogenes/git/refs/heads/test/verify-rulesets \
    -X DELETE
  ```

### Task 9: Create Deferred Work Issues

**Files:** None (`gh` CLI)

Create issues in `diogenes-project/diogenes` for deferred governance
work.

- [ ] **Step 1: Create issue for `.github` profile repo**

  ```bash
  gh issue create --repo diogenes-project/diogenes \
    --title "feat: set up diogenes-project/.github profile repo" \
    --body "Create the diogenes-project/.github repository for org-level configuration (org README, default community health files, CONTRIBUTING.md, issue/PR templates). Mirrors the same setup planned for vergil-project."
  ```

- [ ] **Step 2: Create issue for Claude Code permission model**

  ```bash
  gh issue create --repo diogenes-project/diogenes \
    --title "feat: design Claude Code permission model for diogenes-project" \
    --body "Define the minimal set of allowed operations for AI agent sessions, moving away from permissive mode. Coordinate with the same effort in vergil-project for consistency."
  ```

- [ ] **Step 3: Verify issues are created**

  ```bash
  gh issue list --repo diogenes-project/diogenes \
    --json number,title \
    --jq '.[] | "\(.number): \(.title)"'
  ```

### Task 10: End-to-End Verification

**Files:** None (manual verification)

- [ ] **Step 1: Verify identity separation**

  ```bash
  # Agent can push a branch
  GH_TOKEN=<agent-pat> git push origin test-verify-identity

  # Agent cannot merge without approval
  GH_TOKEN=<agent-pat> gh pr create \
    --repo diogenes-project/diogenes \
    --title "test: identity verification" \
    --body "Verifying governance model." \
    --head test-verify-identity \
    --base develop

  GH_TOKEN=<agent-pat> gh pr merge <PR> --merge
  # Expected: FAIL — review required

  # Human approves and merges
  GH_TOKEN=<human-pat> gh pr review <PR> --approve
  GH_TOKEN=<human-pat> gh pr merge <PR> --merge
  # Expected: SUCCESS
  ```

- [ ] **Step 2: Verify credential isolation**

  ```bash
  # Agent PAT cannot administer
  GH_TOKEN=<agent-pat> gh api orgs/diogenes-project \
    -X PATCH \
    -f description="test"
  # Expected: 403 Forbidden

  # Human PAT can administer
  GH_TOKEN=<human-pat> gh api orgs/diogenes-project \
    -X PATCH \
    -f description="Diogenes — deterministic AI research coordinator for evidence-based investigation"
  # Expected: 200 OK
  ```

- [ ] **Step 3: Verify GitHub App**

  ```bash
  GH_TOKEN=<human-pat> gh api orgs/diogenes-project/installations \
    --jq '.[].app_slug'
  # Expected: diogenes-release
  ```

- [ ] **Step 4: Clean up test branches and PRs**

  Remove any test branches and close any test PRs created during
  verification.

- [ ] **Step 5: Record completion**

  The org governance setup is complete. The migration is verified
  and the org is ready for production use.
