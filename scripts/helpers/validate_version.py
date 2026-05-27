#!/usr/bin/env python3
"""Validate library version string rules for CI."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

VERSION_PATTERN = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


@dataclass(frozen=True)
class Version:
    """Semantic version without a build component."""

    major: int
    minor: int
    patch: int

    def as_string(self) -> str:
        """Return the version formatted as MAJOR.MINOR.PATCH."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def as_tuple(self) -> tuple[int, int, int]:
        """Return the version as a comparison tuple."""
        return (self.major, self.minor, self.patch)


def parse_arguments(argument_list: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate version string rules for CI.",
    )
    parser.add_argument(
        "--base-ref",
        default=None,
        help="Base branch reference for comparison (defaults to GITHUB_BASE_REF).",
    )
    parser.add_argument(
        "--event-name",
        default=None,
        help="Event name override (defaults to GITHUB_EVENT_NAME).",
    )
    return parser.parse_args(list(argument_list) if argument_list is not None else None)


def ensure_project_root() -> None:
    """Fail fast if invoked outside the repository root."""
    if not Path("VERSION").is_file():
        message = "Run from the repository root (VERSION file missing)."
        raise SystemExit(message)


def read_command_output(command: Sequence[str]) -> str:
    """Run a command and return its stripped standard output."""
    result = subprocess.run(command, check=True, text=True, capture_output=True)  # noqa: S603
    return result.stdout.strip()


def git_reference_exists(reference: str) -> bool:
    """Return True if the git reference exists."""
    result = subprocess.run(("git", "rev-parse", "--verify", "--quiet", reference), check=False)  # noqa: S603, S607
    return result.returncode == 0


def resolve_base_reference(base_reference: str) -> str:
    """Resolve a base reference to an existing git ref."""
    if git_reference_exists(base_reference):
        return base_reference
    remote_reference = f"origin/{base_reference}"
    if git_reference_exists(remote_reference):
        return remote_reference
    message = "Base reference not found. Fetch the base branch before running version checks."
    raise SystemExit(message)


def parse_version(version_value: str) -> Version:
    """Parse and validate a version string."""
    match = VERSION_PATTERN.match(version_value.strip())
    if not match:
        message = f"Invalid version format: {version_value!r}"
        raise SystemExit(message)
    major, minor, patch = (int(match.group(index)) for index in range(1, 4))
    return Version(major=major, minor=minor, patch=patch)


def _parse_version_from_toml(toml_text: str) -> Version:
    """Extract version from pyproject.toml content (legacy fallback)."""
    data = tomllib.loads(toml_text)
    project_section = data.get("project")
    if isinstance(project_section, dict):
        version_value = project_section.get("version")
        if isinstance(version_value, str):
            return parse_version(version_value)
    message = "Missing version in pyproject.toml (expected project.version)."
    raise SystemExit(message)


def load_version_from_worktree() -> Version:
    """Load the version from the VERSION file in the working tree."""
    version_text = Path("VERSION").read_text(encoding="utf-8")
    return parse_version(version_text)


def load_version_from_git(reference: str) -> Version:
    """Load the version from a git reference.

    Tries VERSION first, then falls back to pyproject.toml for older
    refs that predate the VERSION file.
    """
    try:
        version_text = read_command_output(("git", "show", f"{reference}:VERSION"))
        return parse_version(version_text)
    except subprocess.CalledProcessError:
        pass

    # Fall back to pyproject.toml for refs that predate the VERSION file.
    try:
        toml_text = read_command_output(("git", "show", f"{reference}:pyproject.toml"))
    except subprocess.CalledProcessError as exc:
        raise FileNotFoundError from exc
    return _parse_version_from_toml(toml_text)


def ensure_version_not_regressed(base_version: Version, head_version: Version, base_reference: str) -> None:
    """Ensure the head version does not regress from the base."""
    if head_version.as_tuple() < base_version.as_tuple():
        message = (
            "Version must not regress relative to the base branch. "
            f"Base ({base_reference}) is {base_version.as_string()}, "
            f"head is {head_version.as_string()}."
        )
        raise SystemExit(message)


def main() -> int:
    arguments = parse_arguments()
    ensure_project_root()

    head_version = load_version_from_worktree()

    base_reference = arguments.base_ref or os.environ.get("GITHUB_BASE_REF")
    event_name = arguments.event_name or os.environ.get("GITHUB_EVENT_NAME", "")
    if base_reference and (event_name == "pull_request" or arguments.base_ref is not None):
        resolved_base = resolve_base_reference(base_reference)
        try:
            base_version = load_version_from_git(resolved_base)
        except FileNotFoundError:
            print("Base reference missing version data; skipping version comparison.")
            return 0
        ensure_version_not_regressed(base_version, head_version, resolved_base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
