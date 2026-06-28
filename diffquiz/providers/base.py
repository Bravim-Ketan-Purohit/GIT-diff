"""Provider interface — a uniform way to ask an LLM for one completion.

A provider is *available* when it can actually run right now (a binary on PATH,
or an API key plus the SDK). `complete()` returns text, or ``None`` on *any*
failure, so the caller can fall through to the next provider or to offline
behaviour. Nothing here ever raises.
"""
from __future__ import annotations

import os

# Fast + cheap by default. Swap to "claude-sonnet-4-6" for sharper grading.
DEFAULT_MODEL = os.environ.get("DIFFQUIZ_MODEL", "claude-haiku-4-5-20251001")


class Provider:
    name: str = "provider"

    def available(self) -> bool:
        raise NotImplementedError

    def complete(
        self, prompt: str, *, model: str | None = None, max_tokens: int = 400
    ) -> str | None:
        raise NotImplementedError
