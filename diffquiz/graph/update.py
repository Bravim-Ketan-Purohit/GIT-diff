"""Incrementally patch the graph from the current working-tree diff.

Cheap and per-round: re-extract only the files that changed (including new
untracked ones), carry over summaries whose code is unchanged, drop deleted
files, and optionally re-describe the touched nodes. Used by the live quiz loop
so grounding always reflects the code as it is right now.
"""
from __future__ import annotations

from pathlib import Path

from .. import git_utils
from . import build, enrich, extract, store
from .model import Graph, Node


def update_from_diff(
    repo: str, graph: Graph, *, model=None, reenrich: bool = False, on_node=None
) -> Graph:
    touched: list[Node] = []
    changed = False
    for rel in git_utils.get_changed_files(repo):
        extractor = extract.for_path(rel)
        if extractor is None:
            continue
        old = {nid: n for nid, n in graph.nodes.items() if n.path == rel}
        if old:
            _drop_file(graph, set(old))
            changed = True

        source = _read(repo, rel)
        if source is None:
            continue  # deleted — its nodes are already gone

        nodes, edges = extractor.extract(rel, source)
        for node in nodes:
            prev = old.get(node.id)
            if (
                prev
                and prev.summary
                and node.content_hash
                and prev.content_hash == node.content_hash
            ):
                node.summary = prev.summary
                node.summary_model = prev.summary_model
                node.last_indexed = prev.last_indexed
            graph.add_node(node)
            if node.summary is None:
                touched.append(node)
        for edge in edges:
            graph.add_edge(edge)
        changed = True

    if not changed:
        return graph
    build._resolve_edges(graph)
    if reenrich and touched:
        enrich.enrich_some(repo, graph, touched, model=model, on_node=on_node)
    store.save_graph(repo, graph)
    return graph


def _read(repo: str, rel: str) -> str | None:
    try:
        return (Path(repo) / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def _drop_file(graph: Graph, node_ids: set[str]) -> None:
    """Remove a file's nodes and the edges originating from them."""
    for nid in node_ids:
        graph.nodes.pop(nid, None)
    graph.edges = [e for e in graph.edges if e.src not in node_ids]
