"""Thin wrappers around git for capturing what changed."""
from __future__ import annotations

import os
import subprocess


def _run(args: list[str], cwd: str, ok_codes: tuple[int, ...] = (0,)) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if result.returncode not in ok_codes:
        return ""
    return result.stdout


def is_git_repo(path: str) -> bool:
    out = _run(["rev-parse", "--is-inside-work-tree"], path).strip()
    return out == "true"


# diffquiz writes its graph under .diffquiz/; never treat that as a code change,
# or saving the graph would itself trigger the next quiz round.
_STORE_DIR = ".diffquiz"


def _is_store_path(rel: str) -> bool:
    return rel == _STORE_DIR or rel.startswith(_STORE_DIR + "/")


def _untracked_files(path: str) -> list[str]:
    out = _run(["ls-files", "--others", "--exclude-standard"], path)
    files = [line.strip() for line in out.splitlines() if line.strip()]
    return [f for f in files if not _is_store_path(f)]


def get_uncommitted_diff(path: str = ".") -> str:
    """Everything changed since HEAD: tracked (staged + unstaged) + new files.

    `git diff HEAD` misses untracked files, so each new file is appended as a
    synthesized "added" diff via `git diff --no-index` (which exits 1 when the
    files differ — hence ok_codes=(0, 1)).
    """
    parts = []
    tracked = _run(["diff", "HEAD", "--", ".", f":(exclude){_STORE_DIR}"], path)
    if tracked.strip():
        parts.append(tracked)
    for rel in _untracked_files(path):
        added = _run(["diff", "--no-index", "--", os.devnull, rel], path, ok_codes=(0, 1))
        if added.strip():
            parts.append(added)
    return "\n".join(parts)


def get_changed_files(path: str = ".") -> list[str]:
    out = _run(["diff", "HEAD", "--name-only", "--", ".", f":(exclude){_STORE_DIR}"], path)
    files = [line.strip() for line in out.splitlines() if line.strip()]
    files.extend(_untracked_files(path))
    return [f for f in files if not _is_store_path(f)]


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

    return hashlib.sha256(diff.encode("utf-8", "ignore")).hexdigest()
