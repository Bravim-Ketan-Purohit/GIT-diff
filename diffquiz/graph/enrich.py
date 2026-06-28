"""LLM enrichment: give each graph node a one-sentence summary.

This is the token-heavy, one-time step (DESIGN §3). It is:

* **Bottom-up** — functions/methods first, then classes, then files, so a parent's
  prompt can reuse its children's summaries instead of re-reading all their code.
* **Resumable** — summaries are saved to disk every few nodes and on interrupt;
  a node already carrying a summary is skipped, so re-runs cost nothing.
* **Cost-gated** — `estimate_cost` lets the caller show a "~N nodes / ~T tokens"
  prompt before spending anything.

Per-node calls go through `providers.complete_bulk` (direct API preferred).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .. import providers
from . import store
from .model import Graph, Node

# Functions are leaves; classes/files summarise their children.
_ORDER = {"function": 0, "method": 0, "class": 1, "file": 2}
_SAVE_EVERY = 10
_MAX_OUTPUT_TOKENS = 120


@dataclass
class Estimate:
    nodes: int       # nodes still needing a summary
    est_tokens: int  # rough total input+output tokens


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def needs_summary(node: Node) -> bool:
    return node.summary is None


def estimate_cost(graph: Graph) -> Estimate:
    needing = [n for n in graph.nodes.values() if needs_summary(n)]
    tokens = 0
    for n in needing:
        span_lines = max(n.span[1] - n.span[0] + 1, 1)
        in_toks = min(span_lines * 40, 1500) // 4 + 100  # ~40 chars/line, ~4 chars/token
        tokens += in_toks + 40
    return Estimate(nodes=len(needing), est_tokens=tokens)


def enrich(repo, graph, *, model=None, on_node=None, save_every=_SAVE_EVERY) -> Graph:
    """Fill in missing node summaries, saving as we go so it can resume."""
    model = model or providers.DEFAULT_MODEL
    cache: dict[str, list[str]] = {}
    needing = sorted(
        (n for n in graph.nodes.values() if needs_summary(n)),
        key=lambda n: _ORDER.get(n.kind, 0),
    )
    done = 0
    try:
        for node in needing:
            summary = providers.complete_bulk(
                _prompt_for(graph, node, repo, cache),
                model=model,
                max_tokens=_MAX_OUTPUT_TOKENS,
            )
            summary = _clean_summary(summary) if summary else summary
            if summary:
                node.summary = summary
                node.summary_model = model
                node.last_indexed = _now()
                done += 1
                if done % save_every == 0:
                    store.save_graph(repo, graph)
            if on_node is not None:
                on_node(node, summary)
    except KeyboardInterrupt:
        store.save_graph(repo, graph)
        _save_manifest(repo, graph, "partial", model)
        raise

    store.save_graph(repo, graph)
    remaining = sum(1 for n in graph.nodes.values() if needs_summary(n))
    _save_manifest(repo, graph, "enriched" if remaining == 0 else "partial", model)
    return graph


# --- prompt construction --------------------------------------------------

# The agent CLI is agentic by default; without a firm, self-contained prompt it
# will try to "go read the file" and leak tool-call narration into the summary.
_RULES = (
    "You are writing a one-line index entry for a code-knowledge tool. Everything "
    "you need is below — do NOT use tools, read files, or ask questions. Reply with "
    "ONLY a single sentence (max 30 words), no preamble.\n\n"
)


def _prompt_for(graph: Graph, node: Node, repo: str, cache: dict) -> str:
    head = node.signature or node.name
    src = _source_slice(repo, node, cache)
    if node.kind in ("function", "method"):
        return (
            f"{_RULES}Describe what this {node.kind} does and why it exists:\n\n"
            f"{head}\n<code>\n{src[:1500]}\n</code>"
        )

    kind = "class" if node.kind == "class" else "file"
    children = _child_summaries(graph, node)
    contains = "".join(f"- {c}\n" for c in children)
    return (
        f"{_RULES}Describe what this {kind} is responsible for:\n\n{head}\n"
        + (f"It contains:\n{contains}" if contains else "")
        + f"<code>\n{src[:1200]}\n</code>"
    )


def _child_summaries(graph: Graph, node: Node) -> list[str]:
    out = []
    for e in graph.edges:
        if e.type == "contains" and e.src == node.id:
            child = graph.nodes.get(e.dst)
            if child and child.summary:
                out.append(f"{child.name}: {child.summary}")
    return out


def _source_slice(repo: str, node: Node, cache: dict) -> str:
    if node.path not in cache:
        try:
            cache[node.path] = (Path(repo) / node.path).read_text(
                encoding="utf-8", errors="ignore"
            ).splitlines()
        except OSError:
            cache[node.path] = []
    lines = cache[node.path]
    return "\n".join(lines[node.span[0] - 1 : node.span[1]])


def _one_line(text: str) -> str:
    return " ".join(text.strip().split())


def _clean_summary(text: str) -> str:
    """Strip any agent tool-call narration the CLI may emit, then collapse to a line."""
    for pat in (r"<function_calls>.*?</function_calls>", r"<invoke\b.*?</invoke>",
                r"<parameter\b.*?</parameter>"):
        text = re.sub(pat, " ", text, flags=re.DOTALL)
    return _one_line(text)


def _save_manifest(repo: str, graph: Graph, phase: str, model: str) -> None:
    manifest = store.load_manifest(repo)
    manifest.update(
        {
            "phase": phase,
            "nodes": len(graph.nodes),
            "enriched": sum(1 for n in graph.nodes.values() if n.summary),
            "model": model,
            "enriched_at": _now(),
        }
    )
    store.save_manifest(repo, manifest)
