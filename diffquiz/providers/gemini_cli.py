"""Gemini CLI provider — `gemini -p` non-interactive.

Sends the prompt headless and returns the printed response. Requires the Gemini
CLI installed and authenticated. Any failure returns None so the router degrades.
"""
from __future__ import annotations

import shutil
import subprocess

from .base import Provider, safe_model, strip_ansi


class GeminiCLIProvider(Provider):
    name = "gemini-cli"

    def available(self) -> bool:
        return shutil.which("gemini") is not None

    def complete(self, prompt, *, model=None, max_tokens=400):
        if not self.available():
            return None
        cmd = ["gemini", "-p", prompt]
        m = safe_model(model)
        if m and not m.startswith("claude"):   # ignore our Claude default
            cmd += ["-m", m]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120,
                stdin=subprocess.DEVNULL,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        if proc.returncode != 0:
            return None
        result = strip_ansi(proc.stdout).strip()
        return result or None
