"""AI layer: turn a git diff into a learning moment.

Both functions degrade gracefully: if there's no ANTHROPIC_API_KEY (or the
`anthropic` package isn't installed), they fall back to simple offline
behaviour so the tool still works.
"""
from __future__ import annotations

import os

# Fast + cheap by default. Swap to "claude-sonnet-4-6" for sharper grading.
DEFAULT_MODEL = os.environ.get("DIFFQUIZ_MODEL", "claude-haiku-4-5-20251001")


def _client():
    """Return an Anthropic client, or None if unavailable."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        from anthropic import Anthropic
    except ImportError:
        return None
    return Anthropic()


def generate_question(diff: str, changed_files: list[str]) -> str:
    """A question to ask BEFORE the dev sees the diff.

    With an API key, Claude writes a pointed question that tests understanding
    without leaking the implementation. Offline, we ask a sensible default.
    """
    client = _client()
    files = ", ".join(changed_files) or "the working tree"

    if client is None:
        return (
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
        f"<diff>\n{diff[:6000]}\n</diff>"
    )
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception:
        return (
            f"These files just changed: {files}.\n"
            "Before you look — what do you think changed, and why?"
        )


def grade_prediction(diff: str, prediction: str) -> str | None:
    """Score the dev's guess against the real diff and flag risks.

    Returns None when offline (caller just shows the diff).
    """
    client = _client()
    if client is None:
        return None

    prompt = (
        "You are a sharp code reviewer. A developer predicted what an AI agent "
        "changed, then saw the real diff. Compare their prediction to the diff.\n\n"
        "Reply in three tight sections, plain text, no markdown headers:\n"
        "SCORE: x/100 — one line on how close they were.\n"
        "MISSED: the most important thing they didn't anticipate (skip if none).\n"
        "WATCH: any bug, security, or correctness risk you see in the diff "
        "(skip if genuinely clean). Be concrete; cite the line/symbol.\n\n"
        f"<prediction>\n{prediction}\n</prediction>\n\n"
        f"<diff>\n{diff[:8000]}\n</diff>"
    )
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        return f"(AI grading unavailable: {e})"
