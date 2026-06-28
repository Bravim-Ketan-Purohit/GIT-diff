"""AI layer: turn a git diff into a learning moment.

Both functions degrade gracefully. They route through `providers`, which prefers
the user's already-authenticated agent CLI (no API key needed) and falls back to
the direct API, then to offline behaviour — so the tool always works.

When a `grounding` subgraph is supplied (retrieved from the codebase graph), it's
folded into the prompt so questions can probe ripple effects and intent, not just
the literal lines that changed.
"""
from __future__ import annotations

from . import providers

# Re-exported for back-compat; the source of truth is providers.DEFAULT_MODEL.
DEFAULT_MODEL = providers.DEFAULT_MODEL

# Delimiters we wrap untrusted content in; neutralised below so repo/agent
# content can't close a block and inject instructions.
_DELIMS = ("diff", "context", "prediction")


def _fence(content: str, limit: int) -> str:
    """Truncate and stop content from breaking out of our prompt delimiters."""
    out = content[:limit]
    for tag in _DELIMS:
        out = out.replace(f"</{tag}>", f"<\\/{tag}>")
    return out


def _context_block(grounding: str | None) -> str:
    if not grounding:
        return ""
    return (
        "Use this map of how the changed code connects to the rest of the repo "
        "to ask about ripple effects or intent, not just the literal change:\n"
        f"<context>\n{_fence(grounding, 4000)}\n</context>\n\n"
    )


def generate_question(
    diff: str, changed_files: list[str], grounding: str | None = None
) -> str:
    """A question to ask BEFORE the dev sees the diff.

    With a provider, an LLM writes a pointed question that tests understanding
    without leaking the implementation. Offline, we ask a sensible default.
    """
    files = ", ".join(changed_files) or "the working tree"
    offline = (
        f"These files just changed: {files}.\n"
        "Before you look — what do you think changed, and why?"
    )

    prompt = (
        "You are a coding mentor running a 'predict the diff' drill. "
        "A developer is about to review changes an AI agent made to their repo. "
        "Below is the actual git diff. Write ONE short, specific question "
        "(max 25 words) that tests whether the developer understands what changed "
        "and why — WITHOUT revealing the answer. Focus on intent, risk, or a "
        "non-obvious consequence. Output only the question.\n\n"
        f"{_context_block(grounding)}"
        f"<diff>\n{_fence(diff, 6000)}\n</diff>"
    )
    return providers.complete_interactive(prompt, model=DEFAULT_MODEL, max_tokens=150) or offline


def grade_prediction(
    diff: str, prediction: str, grounding: str | None = None
) -> str | None:
    """Score the dev's guess against the real diff and flag risks.

    Returns None when no provider is available (caller just shows the diff).
    """
    prompt = (
        "You are a sharp code reviewer. A developer predicted what an AI agent "
        "changed, then saw the real diff. Compare their prediction to the diff.\n\n"
        "Reply in three tight sections, plain text, no markdown headers:\n"
        "SCORE: x/100 — one line on how close they were.\n"
        "MISSED: the most important thing they didn't anticipate (skip if none).\n"
        "WATCH: any bug, security, or correctness risk you see in the diff "
        "(skip if genuinely clean). Be concrete; cite the line/symbol.\n\n"
        f"{_context_block(grounding)}"
        f"<prediction>\n{_fence(prediction, 2000)}\n</prediction>\n\n"
        f"<diff>\n{_fence(diff, 8000)}\n</diff>"
    )
    return providers.complete_interactive(prompt, model=DEFAULT_MODEL, max_tokens=400)
