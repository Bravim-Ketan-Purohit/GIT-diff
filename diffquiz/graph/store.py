"""Persist the graph + index manifest under repo-local `.diffquiz/` (git-ignored).

Writes are atomic (temp file + `os.replace`) so an interrupted index never
leaves a half-written graph behind.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .model import Graph

DIR_NAME = ".diffquiz"
GRAPH_FILE = "graph.json"
MANIFEST_FILE = "manifest.json"
SCHEMA_VERSION = 1


def graph_dir(repo: str) -> Path:
    return Path(repo) / DIR_NAME


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def save_graph(repo: str, graph: Graph) -> None:
    _atomic_write(graph_dir(repo) / GRAPH_FILE, graph.to_json())


def load_graph(repo: str) -> Graph | None:
    path = graph_dir(repo) / GRAPH_FILE
    if not path.exists():
        return None
    try:
        return Graph.from_json(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, OSError):
        return None


def save_manifest(repo: str, manifest: dict) -> None:
    _atomic_write(graph_dir(repo) / MANIFEST_FILE, manifest)


def load_manifest(repo: str) -> dict:
    path = graph_dir(repo) / MANIFEST_FILE
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
