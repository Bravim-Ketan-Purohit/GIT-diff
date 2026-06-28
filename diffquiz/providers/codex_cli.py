"""Codex CLI provider — stub seam (good-first-issue).

Detection works, but `complete()` is not implemented yet, so the router falls
through to the next provider. Wiring this to `codex exec` (parse its output,
keep it on a no-tools leash) is a small, self-contained contribution.
"""
from __future__ import annotations

from .base import Provider


class CodexCLIProvider(Provider):
    name = "codex-cli"

    def available(self) -> bool:
        # Not a usable backend yet, so it stays out of routing. Once complete()
        # is implemented, switch to `shutil.which("codex") is not None`.
        return False

    def complete(self, prompt, *, model=None, max_tokens=400):
        return None  # not implemented yet
