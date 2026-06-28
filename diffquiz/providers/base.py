"""Provider interface — a uniform way to ask an LLM for one completion.

A provider is *available* when it can actually run right now (a binary on PATH,
or an API key plus the SDK). `complete()` returns text, or ``None`` on *any*
failure, so the caller can fall through to the next provider or to offline
behaviour. Nothing here ever raises.
"""
from __future__ import annotations

import os
import re

# Fast + cheap by default. Swap to "claude-sonnet-4-6" for sharper grading.
DEFAULT_MODEL = os.environ.get("DIFFQUIZ_MODEL", "claude-haiku-4-5-20251001")

# A model name goes straight into CLI argv. Require a leading alphanumeric (no
# leading "-") so it can't be smuggled in as a flag; allow "/" for provider/model
# forms like "anthropic/claude-sonnet".
_MODEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def safe_model(model: str | None) -> str | None:
    """Return the model if it's a safe CLI token (no flag injection), else None."""
    return model if model and _MODEL_RE.match(model) else None


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


class Provider:
    name: str = "provider"

    def available(self) -> bool:
        raise NotImplementedError

    def complete(
        self, prompt: str, *, model: str | None = None, max_tokens: int = 400
    ) -> str | None:
        raise NotImplementedError
