"""Thin wrappers around git for capturing what changed."""
from __future__ import annotations

import subprocess
from pathlib import Path


def _run(args: list[str], cwd: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def is_git_repo(path: str) -> bool:
    out = _run(["rev-parse", "--is-inside-work-tree"], path).strip()
    return out == "true"


def get_uncommitted_diff(path: str = ".") -> str:
    """Everything changed since the last commit (staged + unstaged)."""
    return _run(["diff", "HEAD"], path)


def get_changed_files(path: str = ".") -> list[str]:
    out = _run(["diff", "HEAD", "--name-only"], path)
    return [line.strip() for line in out.splitlines() if line.strip()]


def list_source_files(path: str = ".") -> list[str]:
    """All source files git knows about: tracked + untracked-but-not-ignored.

    Uses `git ls-files` so it respects .gitignore (skips .venv, __pycache__,
    .diffquiz, etc.) while still seeing brand-new files not yet committed.
    """
    out = _run(["ls-files", "--cached", "--others", "--exclude-standard"], path)
    return [line.strip() for line in out.splitlines() if line.strip()]


def diff_fingerprint(diff: str) -> str:
    """Cheap identity for a diff so we only quiz once per change."""
    import hashlib

    return hashlib.sha1(diff.encode("utf-8", "ignore")).hexdigest()
