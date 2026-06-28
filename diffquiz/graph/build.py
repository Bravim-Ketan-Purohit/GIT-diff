"""Build the codebase graph from a repo's source files.

`build_structural` is token-free: extract nodes/edges, resolve calls/inherits,
and **carry over** any summaries from a previous index whose code is unchanged
(so re-indexing spends nothing and only changed nodes get re-enriched).
`build` runs the structural pass then the LLM enrichment pass.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .. import git_utils
from . import enrich as _enrich
from . import extract, store
from .model import Graph


def build_structural(repo: str) -> Graph:
    graph = Graph()
    indexed_files = 0
    for rel in git_utils.list_source_files(repo):
        extractor = extract.for_path(rel)
        if extractor is None:
            continue
        try:
            source = (Path(repo) / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        nodes, edges = extractor.extract(rel, source)
        for node in nodes:
            graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)
        indexed_files += 1

    _resolve_edges(graph)
    _carry_over_summaries(repo, graph)
    store.save_graph(repo, graph)
    store.save_manifest(
        repo,
        {
            "schema": store.SCHEMA_VERSION,
            "phase": _phase(graph),
            "files": indexed_files,
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "enriched": sum(1 for n in graph.nodes.values() if n.summary),
            "built_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return graph


def build(repo: str, *, enrich_summaries: bool = True, model=None, on_node=None) -> Graph:
    graph = build_structural(repo)
    if enrich_summaries:
        _enrich.enrich(repo, graph, model=model, on_node=on_node)
    return graph


def _phase(graph: Graph) -> str:
    total = len(graph.nodes)
    enriched = sum(1 for n in graph.nodes.values() if n.summary)
    if enriched == 0:
        return "structural"
    return "enriched" if enriched == total else "partial"


def _carry_over_summaries(repo: str, graph: Graph) -> None:
    """Reuse a prior summary when the node id and its code hash are unchanged."""
    old = store.load_graph(repo)
    if old is None:
        return
    for node_id, node in graph.nodes.items():
        prev = old.nodes.get(node_id)
        if prev and prev.summary and prev.content_hash == node.content_hash:
            node.summary = prev.summary
            node.summary_model = prev.summary_model
            node.last_indexed = prev.last_indexed


def _resolve_edges(graph: Graph) -> None:
    """Point unresolved `calls`/`inherits` edges at a uniquely-named node."""
    by_name: dict[str, list[str]] = {}
    for node in graph.nodes.values():
        by_name.setdefault(node.name, []).append(node.id)
    for edge in graph.edges:
        if edge.resolved or edge.type not in ("calls", "inherits"):
            continue
        matches = by_name.get(edge.dst)
        if matches and len(matches) == 1:
            edge.dst = matches[0]
            edge.resolved = True
