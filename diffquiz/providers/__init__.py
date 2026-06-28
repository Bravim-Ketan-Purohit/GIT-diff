"""Detect LLM backends and route a call by job size (see DESIGN §6).

Two cost classes:

* **interactive** — one small call per diff. Prefer the user's local agent CLI
  (zero-config, uses their existing login) over the API, so no key is needed for
  everyday use.
* **bulk** — the one-time index enrichment (potentially thousands of calls).
  Prefer the direct API (batchable, cheap model); the CLI would cold-boot per
  call and drain the user's coding quota.

Each router tries providers in order and falls through on failure, returning
``None`` only when nothing can answer — so callers always have an offline path.
"""
from __future__ import annotations

import os

from .anthropic_api import AnthropicAPIProvider
from .base import DEFAULT_MODEL, Provider
from .claude_cli import ClaudeCLIProvider
from .codex_cli import CodexCLIProvider
from .gemini_cli import GeminiCLIProvider
from .opencode_cli import OpenCodeProvider

__all__ = [
    "DEFAULT_MODEL",
    "PROVIDER_NAMES",
    "Provider",
    "interactive_chain",
    "bulk_chain",
    "complete_interactive",
    "complete_bulk",
]

# Canonical backend names a user can pin via DIFFQUIZ_PROVIDER.
PROVIDER_NAMES = ("claude", "codex", "gemini", "opencode", "anthropic")

# Accept friendly names and full provider .name values.
_BY_NAME = {
    "claude": ClaudeCLIProvider, "claude-cli": ClaudeCLIProvider,
    "codex": CodexCLIProvider, "codex-cli": CodexCLIProvider,
    "gemini": GeminiCLIProvider, "gemini-cli": GeminiCLIProvider,
    "opencode": OpenCodeProvider,
    "anthropic": AnthropicAPIProvider, "api": AnthropicAPIProvider,
    "anthropic-api": AnthropicAPIProvider,
}


def _forced() -> Provider | None:
    """The single backend pinned via DIFFQUIZ_PROVIDER, or None if unset/unknown."""
    cls = _BY_NAME.get(os.environ.get("DIFFQUIZ_PROVIDER", "").strip().lower())
    return cls() if cls else None


def interactive_chain() -> list[Provider]:
    """Per-diff: the pinned backend if DIFFQUIZ_PROVIDER is set, else agent CLIs
    first with the direct API as fallback."""
    forced = _forced()
    if forced is not None:
        return [forced]
    return [
        ClaudeCLIProvider(),
        CodexCLIProvider(),
        GeminiCLIProvider(),
        OpenCodeProvider(),
        AnthropicAPIProvider(),
    ]


def bulk_chain() -> list[Provider]:
    """One-time indexing: the pinned backend if DIFFQUIZ_PROVIDER is set, else the
    batchable API first with agent CLIs as fallback."""
    forced = _forced()
    if forced is not None:
        return [forced]
    return [
        AnthropicAPIProvider(),
        ClaudeCLIProvider(),
        CodexCLIProvider(),
        GeminiCLIProvider(),
        OpenCodeProvider(),
    ]


def _route(
    chain: list[Provider], prompt: str, model: str | None, max_tokens: int
) -> str | None:
    for provider in chain:
        if provider.available():
            out = provider.complete(prompt, model=model, max_tokens=max_tokens)
            if out:
                return out
    return None


def complete_interactive(
    prompt: str, *, model: str | None = None, max_tokens: int = 400
) -> str | None:
    return _route(interactive_chain(), prompt, model, max_tokens)


def complete_bulk(
    prompt: str, *, model: str | None = None, max_tokens: int = 400
) -> str | None:
    return _route(bulk_chain(), prompt, model, max_tokens)
