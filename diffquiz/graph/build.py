"""Build the structural graph from a repo's source files (token-free).

Enumerates source files via git (so .gitignore is respected), runs each through
its language extractor, then resolves `calls`/`inherits` edges to node ids where
a uniquely-named target exists. Persists graph + manifest.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .. import git_utils
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
    store.save_graph(repo, graph)
    store.save_manifest(
        repo,
        {
            "schema": store.SCHEMA_VERSION,
            "phase": "structural",
            "files": indexed_files,
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "built_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return graph


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
