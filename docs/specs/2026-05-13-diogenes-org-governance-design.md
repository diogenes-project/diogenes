# Diogenes Org Governance Design

**Date:** 2026-05-13
**Status:** Draft

## Problem

The Diogenes migration moves `ai-research-methodology` from a personal
GitHub account (`wphillipmoore`) to the `diogenes-project` GitHub org.
The org requires the same governance model established for
`vergil-project`: identity separation, branch protection, credential
management, and mechanized automation. This spec defines what that model
looks like for `diogenes-project`, reusing the infrastructure and
conventions already established by VERGIL.

## Relationship to VERGIL Governance

This spec is structurally identical to the VERGIL org governance design
(`vergil-tooling/docs/specs/2026-05-11-org-governance-design.md`). The
same foundational principles, identity model, branch protection
rulesets, credential management patterns, and enforcement model apply.
Rather than duplicating that spec, this document references it and
calls out only the Diogenes-specific details.

**Canonical governance spec:**
`vergil-project/vergil-tooling/docs/specs/2026-05-11-org-governance-design.md`

All sections of the VERGIL governance spec apply to `diogenes-project`
unless overridden below.

## Foundational Principles

Same as VERGIL — no changes:

1. AI is a nondeterministic system operating in a space that demands
   deterministic results.
2. AI contributions are welcome. Unaccountable AI contributions are not.
3. The speed limit is human comprehension, not code generation.
4. Where enforcement can be hard-gated, it must be. Where it cannot,
   compliance must be audited post-facto.

## Section 1: Identity Model

Identical to VERGIL. Three identity categories:

| Identity | Represents |
|---|---|
| `wphillipmoore` | The human |
| `wphillipmoore-agent` | The human's AI agents |
| `diogenes-release[bot]` | Org-level GitHub App for mechanized automation |

The `wphillipmoore-agent` account already exists (created during VERGIL
setup). No new account is needed — the same agent identity is reused
across all orgs.

## Section 2: Branch Protection Rulesets

Identical to VERGIL. Org-level rulesets protect `develop` and `main`
in all repos:

- Require pull request before merging
- Require at least 1 approving review
- Require review from someone other than PR author
- Require status checks to pass
- Require branches to be up to date before merging
- No standing bypass permissions
- No deletion of protected branches
- No non-fast-forward pushes

The `main` branch additionally restricts merge to org owners only
(release gate).

## Section 3: Credential Management

### Credential Naming

Credentials follow the same pattern as VERGIL but use the `diogenes/`
namespace in the secure credential store:

| Credential | Store entry name | Used by |
|---|---|---|
| Human PAT | `diogenes/human-pat` | Admin, approvals, merges, releases |
| Agent PAT | `diogenes/agent-pat` | Development, AI agent sessions |
| App private key | `diogenes/app-private-key` | Release tool (PR creation) |
| App ID | `diogenes/app-id` | Release tool (token exchange) |

### Human PAT Scope

Fine-grained PAT scoped to `diogenes-project` as resource owner:

- Repository access: All repositories
- Permissions: Administration (R/W), Contents (R/W), Issues (R/W),
  Pull requests (R/W), Actions (R/W), Metadata (Read)

### Agent PAT Scope

Fine-grained PAT scoped to `diogenes-project` as resource owner:

- Repository access: All repositories
- Permissions: Contents (R/W), Issues (R/W), Pull requests (R/W),
  Metadata (Read)
- Explicitly excluded: Administration, Actions, org settings, secrets,
  deployments

### GitHub App

A new GitHub App `diogenes-release` is registered under the
`diogenes-project` org (not the VERGIL App — each org gets its own
App for isolation). Same permissions as `vergil-release`:

- Contents: Read and write
- Pull requests: Read and write
- Metadata: Read-only
- Installed org-wide on `diogenes-project`

## Section 4: Org Security Settings

Identical to VERGIL:

- Require two-factor authentication for all org members
- Default repository permission: Write
- Do not allow forking of private repos
- Agent accounts are outside collaborators, never org members

## Section 5: What VERGIL Already Handled

The following Phase 2 items from the VERGIL governance plan are
prerequisites that are already complete by the time this plan executes:

- Removal of `skip_rulesets` escape hatch from standard-tooling
- Consolidation of co-author config to single `agent` entry in
  standard-tooling's own config
- Verification that `vrg-commit` accepts arbitrary agent names

Consumer-repo co-author config updates (changing `claude`/`codex`
entries to `agent` in this repo's config) happen during the migration
(Plan B), not during governance setup.

## Section 6: Deferred Work

These items apply to `diogenes-project` but are deferred to future
plans, same as VERGIL:

1. **`diogenes-project/.github` profile repo** — org README, default
   community health files, issue/PR templates
2. **Cross-human review CI check** — required at 2+ human contributors
3. **Credential audit tooling** — reuse VERGIL's `vrg-credential-audit`
   once built; extend to cover `diogenes/` credential namespace
4. **Merge queue** — enable when org moves to a paid GitHub plan

## Risks

Same risk profile as VERGIL. The primary additional risk is credential
proliferation — each new org adds four credential entries to the
Keychain. This is manageable at the current scale but reinforces the
need for the credential audit tooling tracked in VERGIL's backlog.
