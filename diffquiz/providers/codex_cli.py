"""OpenAI Codex CLI provider — `codex exec`, read-only and ephemeral.

Runs the prompt non-interactively in a read-only sandbox (model-generated
commands can't write or exec) and reads the final message from a temp file via
`-o`. Requires `codex login`. Any failure returns None so the router degrades.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

from .base import Provider, safe_model


class CodexCLIProvider(Provider):
    name = "codex-cli"

    def available(self) -> bool:
        return shutil.which("codex") is not None

    def complete(self, prompt, *, model=None, max_tokens=400):
        if not self.available():
            return None
        fd, out_path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        cmd = [
            "codex", "exec",
            "--sandbox", "read-only",   # no writes / no command exec
            "--skip-git-repo-check",
            "--ephemeral",              # don't persist a session
            "--color", "never",
            "-o", out_path,             # write just the final message here
        ]
        m = safe_model(model)
        if m and not m.startswith("claude"):   # ignore our Claude default
            cmd += ["-m", m]
        cmd.append(prompt)
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120,
                stdin=subprocess.DEVNULL,
            )
            if proc.returncode != 0:
                return None
            with open(out_path, encoding="utf-8", errors="replace") as f:
                result = f.read().strip()
            return result or None
        except (OSError, subprocess.SubprocessError):
            return None
        finally:
            try:
                os.unlink(out_path)
            except OSError:
                pass
