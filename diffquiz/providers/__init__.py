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

from .anthropic_api import AnthropicAPIProvider
from .base import DEFAULT_MODEL, Provider
from .claude_cli import ClaudeCLIProvider
from .codex_cli import CodexCLIProvider
from .gemini_cli import GeminiCLIProvider
from .opencode_cli import OpenCodeProvider

__all__ = [
    "DEFAULT_MODEL",
    "Provider",
    "interactive_chain",
    "bulk_chain",
    "complete_interactive",
    "complete_bulk",
]


def interactive_chain() -> list[Provider]:
    """Per-diff: zero-config agent CLIs first, direct API as fallback."""
    return [
        ClaudeCLIProvider(),
        CodexCLIProvider(),
        GeminiCLIProvider(),
        OpenCodeProvider(),
        AnthropicAPIProvider(),
    ]


def bulk_chain() -> list[Provider]:
    """One-time indexing: batchable API first, agent CLIs as fallback."""
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
