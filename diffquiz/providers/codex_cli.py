"""Codex CLI provider — stub seam (good-first-issue).

Detection works, but `complete()` is not implemented yet, so the router falls
through to the next provider. Wiring this to `codex exec` (parse its output,
keep it on a no-tools leash) is a small, self-contained contribution.
"""
from __future__ import annotations

import shutil

from .base import Provider


class CodexCLIProvider(Provider):
    name = "codex-cli"

    def available(self) -> bool:
        return shutil.which("codex") is not None

    def complete(self, prompt, *, model=None, max_tokens=400):
        return None  # not implemented yet — router falls through
