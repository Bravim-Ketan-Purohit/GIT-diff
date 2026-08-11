"""OpenCode provider — `opencode run` non-interactive.

Sends the prompt headless and returns the printed assistant response. Requires
OpenCode installed and a provider configured (`opencode auth`). Models use
OpenCode's `provider/model` form. Any failure returns None so the router degrades.
"""
from __future__ import annotations

import shutil
import subprocess

from .base import Provider, safe_model, strip_ansi


class OpenCodeProvider(Provider):
    name = "opencode"

    def available(self) -> bool:
        return shutil.which("opencode") is not None

    def complete(self, prompt, *, model=None, max_tokens=400):
        if not self.available():
            return None
        cmd = ["opencode", "run"]
        m = safe_model(model)
        if m and not m.startswith("claude"):   # our Claude default isn't a provider/model id
            cmd += ["-m", m]
        cmd.append(prompt)
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
