"""Retrieve the slice of the graph relevant to a diff, as grounding text.

`changed_symbols` maps a unified diff's changed line ranges to the graph nodes
that contain them; `subgraph_for` renders those nodes + their 1-hop neighbours
into a compact, length-bounded block to ground a quiz question.
"""
from __future__ import annotations

import re

from .model import Graph

_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def _strip_prefix(path: str) -> str:
    # Diff paths look like "b/diffquiz/ai.py"; drop the a/ or b/ prefix.
    return path[2:] if path.startswith(("a/", "b/")) else path


def changed_line_ranges(diff: str) -> dict[str, list[tuple[int, int]]]:
    """Map each file in a unified diff to its changed new-side line ranges."""
    ranges: dict[str, list[tuple[int, int]]] = {}
    current: str | None = None
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            current = None if path == "/dev/null" else _strip_prefix(path)
        elif line.startswith("@@") and current is not None:
            m = _HUNK.match(line)
            if m:
                start = int(m.group(1))
                count = int(m.group(2)) if m.group(2) else 1
                ranges.setdefault(current, []).append((start, start + max(count, 1) - 1))
    return ranges


def changed_symbols(graph: Graph, diff: str) -> list[str]:
    """Node ids whose span overlaps a changed region of the diff."""
    ids: list[str] = []
    seen: set[str] = set()
    for path, line_ranges in changed_line_ranges(diff).items():
        for start, end in line_ranges:
            for line in range(start, end + 1):
                node = graph.node_at(path, line)
                if node and node.id not in seen:
                    seen.add(node.id)
                    ids.append(node.id)
    return ids


def subgraph_for(
    graph: Graph, node_ids: list[str], hops: int = 1, limit: int = 40
) -> str:
    """Compact, length-bounded grounding text for the nodes + neighbours."""
    if not node_ids:
        return ""
    targets = set(node_ids)
    related: set[str] = set()
    for nid in node_ids:
        related |= graph.neighbors(nid, hops=hops)

    ordered = list(node_ids) + [r for r in related if r not in targets]
    lines: list[str] = []
    for nid in ordered[:limit]:
        node = graph.nodes.get(nid)
        if node is None:
            continue  # unresolved external name
        marker = "changed" if nid in targets else "related"
        summary = f" — {node.summary}" if node.summary else ""
        lines.append(f"[{marker}] {node.signature or node.kind}  ({node.path}){summary}")

    seen_calls: set[tuple[str, str]] = set()
    for e in graph.edges:
        if e.type != "calls" or not e.resolved:
            continue
        if e.src not in targets and e.dst not in targets:
            continue
        src, dst = graph.nodes.get(e.src), graph.nodes.get(e.dst)
        if src and dst and (e.src, e.dst) not in seen_calls:
            seen_calls.add((e.src, e.dst))
            lines.append(f"call: {src.name} -> {dst.name}")
    return "\n".join(lines)
