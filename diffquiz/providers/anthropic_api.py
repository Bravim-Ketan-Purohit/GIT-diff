"""Direct Anthropic API provider — preferred for bulk index enrichment.

Batchable and lets us pin a cheap model, which is exactly what the one-time
graph enrichment needs. Requires ANTHROPIC_API_KEY and the `anthropic` package.
"""
from __future__ import annotations

import os

from .base import DEFAULT_MODEL, Provider


class AnthropicAPIProvider(Provider):
    name = "anthropic-api"

    def available(self) -> bool:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return False
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return False
        return True

    def complete(self, prompt, *, model=None, max_tokens=400):
        if not self.available():
            return None
        try:
            from anthropic import Anthropic

            resp = Anthropic().messages.create(
                model=model or DEFAULT_MODEL,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text.strip()
        except Exception:
            return None
