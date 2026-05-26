#!/usr/bin/env bash
# Claude Code PreToolUse hook shim.
# Delegates to vrg-hook-guard if available; falls back to a
# jq-based git/gh check that hard-denies when vergil-tooling
# is not installed.
set -euo pipefail

if command -v vrg-hook-guard &>/dev/null; then
  exec vrg-hook-guard
fi

input=$(cat)
command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
bin=$(printf '%s' "$command" | awk '{print $1}')
base=$(basename "$bin" 2>/dev/null || printf '%s' "$bin")

case "$base" in
  git|gh)
    jq -n '{
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "deny",
        permissionDecisionReason: "vergil-tooling is not available. This repository requires a correctly configured environment — all git/gh operations are blocked until resolved."
      }
    }'
    exit 0
    ;;
esac

exit 0
