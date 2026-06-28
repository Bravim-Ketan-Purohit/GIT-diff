"""The codebase graph: flat node/edge lists, JSON-serialisable.

Kept dependency-free and diffable on purpose; a real graph store can slot in
behind this interface later without touching callers.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Node:
    id: str                       # "<path>::<qualname>"  (file nodes use "<path>")
    kind: str                     # file | class | function | method
    name: str
    path: str
    span: tuple[int, int]         # (start_line, end_line), 1-based inclusive
    signature: str | None = None
    summary: str | None = None    # filled by enrichment (Phase 2)
    summary_model: str | None = None
    content_hash: str | None = None
    last_indexed: str | None = None


@dataclass
class Edge:
    src: str
    dst: str                      # node id, or a bare name when resolved is False
    type: str                     # contains | calls | imports | inherits | references
    resolved: bool = True


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)

    # --- construction -----------------------------------------------------
    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    # --- queries ----------------------------------------------------------
    def nodes_in_file(self, path: str) -> list[Node]:
        return [n for n in self.nodes.values() if n.path == path]

    def node_at(self, path: str, line: int) -> Node | None:
        """The most specific (smallest-span) node containing `line` in `path`."""
        best: Node | None = None
        for n in self.nodes.values():
            if n.path == path and n.span[0] <= line <= n.span[1]:
                if best is None or _span_len(n) < _span_len(best):
                    best = n
        return best

    def neighbors(self, node_id: str, hops: int = 1) -> set[str]:
        """Node ids reachable within `hops` edges, either direction."""
        seen = {node_id}
        frontier = {node_id}
        for _ in range(hops):
            nxt: set[str] = set()
            for e in self.edges:
                if e.src in frontier and e.dst not in seen:
                    nxt.add(e.dst)
                if e.dst in frontier and e.src not in seen:
                    nxt.add(e.src)
            nxt -= seen
            if not nxt:
                break
            seen |= nxt
            frontier = nxt
        return seen - {node_id}

    # --- serialisation ----------------------------------------------------
    def to_json(self) -> dict:
        return {
            "nodes": [_node_to_json(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
        }

    @classmethod
    def from_json(cls, data: dict) -> "Graph":
        g = cls()
        for nd in data.get("nodes", []):
            g.add_node(_node_from_json(nd))
        for ed in data.get("edges", []):
            g.add_edge(
                Edge(
                    src=ed["src"],
                    dst=ed["dst"],
                    type=ed["type"],
                    resolved=ed.get("resolved", True),
                )
            )
        return g


def _span_len(n: Node) -> int:
    return n.span[1] - n.span[0]


def _node_to_json(n: Node) -> dict:
    d = asdict(n)
    d["span"] = list(n.span)      # JSON has no tuples
    return d


def _node_from_json(d: dict) -> Node:
    span = d.get("span") or [0, 0]
    return Node(
        id=d["id"],
        kind=d["kind"],
        name=d["name"],
        path=d["path"],
        span=(span[0], span[1]),
        signature=d.get("signature"),
        summary=d.get("summary"),
        summary_model=d.get("summary_model"),
        content_hash=d.get("content_hash"),
        last_indexed=d.get("last_indexed"),
    )
