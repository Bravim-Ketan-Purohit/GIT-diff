"""Language extractor interface: one source file -> (nodes, edges).

Deterministic static analysis, zero tokens. New languages are additive — drop
in another extractor and register it in this package's `__init__`.
"""
from __future__ import annotations

from ..model import Edge, Node


class LanguageExtractor:
    extensions: tuple[str, ...] = ()

    def extract(self, path: str, source: str) -> tuple[list[Node], list[Edge]]:
        raise NotImplementedError
