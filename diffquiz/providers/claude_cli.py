"""Claude Code headless provider — preferred for zero-config interactive use.

Shells out to `claude -p` using the user's *existing* Claude Code login, so no
API key is needed. `--tools ""` disables every tool, so the agent can only
answer — it never edits or runs anything. Any failure returns ``None`` and the
caller degrades to the next provider (or offline).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess

from .base import Provider

# Model names go straight into the CLI argv; require a leading alphanumeric so a
# value like "--dangerously-skip-permissions" can't be smuggled in as a flag.
_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class ClaudeCLIProvider(Provider):
    name = "claude-cli"

    def available(self) -> bool:
        return shutil.which("claude") is not None

    def complete(self, prompt, *, model=None, max_tokens=400):
        # `max_tokens` has no `claude -p` equivalent; we keep prompts short instead.
        if not self.available():
            return None
        cmd = ["claude", "-p", prompt, "--output-format", "json", "--tools", ""]
        if model and _MODEL_RE.match(model):
            cmd += ["--model", model]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.SubprocessError):
            return None
        if proc.returncode != 0:
            return None
        # Output shape can change across CLI versions — parse defensively.
        try:
            result = json.loads(proc.stdout).get("result")
        except (ValueError, AttributeError):
            return None
        if isinstance(result, str) and result.strip():
            return result.strip()
        return None
