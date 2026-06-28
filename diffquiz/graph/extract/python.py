"""Python extractor using the stdlib `ast` — zero extra dependencies.

Produces file/class/function/method nodes with signatures and per-node content
hashes, plus `contains`, `calls`, `imports`, and `inherits` edges. `calls`,
`imports`, and `inherits` are emitted unresolved (dst = a bare name); the build
step resolves them to node ids where it can.
"""
from __future__ import annotations

import ast
import hashlib

from ..model import Edge, Node
from .base import LanguageExtractor


class PythonExtractor(LanguageExtractor):
    extensions = (".py",)

    def extract(self, path: str, source: str) -> tuple[list[Node], list[Edge]]:
        lines = source.splitlines()
        nodes: list[Node] = [
            Node(
                id=path,
                kind="file",
                name=path.rsplit("/", 1)[-1],
                path=path,
                span=(1, max(len(lines), 1)),
                content_hash=_content_hash(source),
            )
        ]
        edges: list[Edge] = []
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return nodes, edges  # still record the file node

        _Visitor(path, lines, nodes, edges).visit_body(tree.body, parent_id=path, qual="")
        return nodes, edges


class _Visitor:
    def __init__(self, path, lines, nodes, edges):
        self.path = path
        self.lines = lines
        self.nodes = nodes
        self.edges = edges

    def visit_body(self, body, parent_id, qual, in_class=False):
        for stmt in body:
            if isinstance(stmt, ast.ClassDef):
                self._class(stmt, parent_id, qual)
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._func(stmt, parent_id, qual, in_class)
            elif isinstance(stmt, (ast.Import, ast.ImportFrom)):
                self._imports(stmt)

    def _class(self, stmt, parent_id, qual):
        q = f"{qual}.{stmt.name}" if qual else stmt.name
        node_id = f"{self.path}::{q}"
        self.nodes.append(
            Node(
                id=node_id, kind="class", name=stmt.name, path=self.path,
                span=_span(stmt), signature=f"class {stmt.name}",
                content_hash=self._hash(stmt),
            )
        )
        self.edges.append(Edge(parent_id, node_id, "contains"))
        for base in stmt.bases:
            bname = _name_of(base)
            if bname:
                self.edges.append(Edge(node_id, bname, "inherits", resolved=False))
        self.visit_body(stmt.body, parent_id=node_id, qual=q, in_class=True)

    def _func(self, stmt, parent_id, qual, in_class):
        q = f"{qual}.{stmt.name}" if qual else stmt.name
        node_id = f"{self.path}::{q}"
        self.nodes.append(
            Node(
                id=node_id, kind="method" if in_class else "function",
                name=stmt.name, path=self.path, span=_span(stmt),
                signature=_signature(stmt), content_hash=self._hash(stmt),
            )
        )
        self.edges.append(Edge(parent_id, node_id, "contains"))
        for callee in _called_names(stmt):
            self.edges.append(Edge(node_id, callee, "calls", resolved=False))
        # Nested defs become their own nodes, contained by this one.
        self.visit_body(stmt.body, parent_id=node_id, qual=q, in_class=False)

    def _imports(self, stmt):
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                self.edges.append(Edge(self.path, alias.name, "imports", resolved=False))
        elif stmt.module:
            self.edges.append(Edge(self.path, stmt.module, "imports", resolved=False))

    def _hash(self, stmt) -> str:
        start, end = _span(stmt)
        return _content_hash("\n".join(self.lines[start - 1 : end]))


def _span(stmt) -> tuple[int, int]:
    return (stmt.lineno, getattr(stmt, "end_lineno", stmt.lineno) or stmt.lineno)


def _signature(fn) -> str:
    prefix = "async def " if isinstance(fn, ast.AsyncFunctionDef) else "def "
    try:
        args = ast.unparse(fn.args)
    except Exception:
        args = ""
    sig = f"{prefix}{fn.name}({args})"
    if fn.returns is not None:
        try:
            sig += f" -> {ast.unparse(fn.returns)}"
        except Exception:
            pass
    return sig


def _name_of(node) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _called_names(fn) -> list[str]:
    names: list[str] = []
    seen: set[str] = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Call):
            nm = _name_of(n.func)
            if nm and nm not in seen:
                seen.add(nm)
                names.append(nm)
    return names


def _content_hash(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()
