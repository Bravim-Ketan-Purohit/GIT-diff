import subprocess

import pytest

from diffquiz import providers
from diffquiz.graph import build, enrich, store

MOD = "def foo():\n    return 1\n\n\ndef bar():\n    return foo()\n"


def _init_repo(tmp_path, files):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    for name, content in files.items():
        (tmp_path / name).write_text(content)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    return str(tmp_path)


class _MockBulk:
    """Stand-in for providers.complete_bulk; counts calls, can raise mid-run."""

    def __init__(self, raise_after=None):
        self.calls = 0
        self.raise_after = raise_after

    def __call__(self, prompt, *, model=None, max_tokens=400):
        self.calls += 1
        if self.raise_after is not None and self.calls > self.raise_after:
            raise KeyboardInterrupt
        return f"summary {self.calls}"


def test_enrich_populates_all_summaries(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    needing = enrich.estimate_cost(graph).nodes
    assert needing == len(graph.nodes) > 0

    mock = _MockBulk()
    monkeypatch.setattr(providers, "complete_bulk", mock)
    enrich.enrich(repo, graph)

    assert all(n.summary for n in graph.nodes.values())
    assert mock.calls == needing
    assert store.load_manifest(repo)["phase"] == "enriched"


def test_rerun_carries_over_and_spends_nothing(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    monkeypatch.setattr(providers, "complete_bulk", _MockBulk())
    enrich.enrich(repo, graph)

    graph2 = build.build_structural(repo)  # summaries carried over from disk
    assert all(n.summary for n in graph2.nodes.values())
    assert enrich.estimate_cost(graph2).nodes == 0

    mock2 = _MockBulk()
    monkeypatch.setattr(providers, "complete_bulk", mock2)
    enrich.enrich(repo, graph2)
    assert mock2.calls == 0


def test_changed_node_is_reenriched(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    monkeypatch.setattr(providers, "complete_bulk", _MockBulk())
    enrich.enrich(repo, graph)

    # Editing foo's body changes foo's hash and the file's hash, not bar's.
    (tmp_path / "mod.py").write_text(MOD.replace("return 1", "return 42"))
    graph2 = build.build_structural(repo)
    needing = {n.id for n in graph2.nodes.values() if n.summary is None}
    assert needing == {"mod.py", "mod.py::foo"}

    mock2 = _MockBulk()
    monkeypatch.setattr(providers, "complete_bulk", mock2)
    enrich.enrich(repo, graph2)
    assert mock2.calls == 2


def test_interrupt_saves_progress_then_resumes(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    total = enrich.estimate_cost(graph).nodes
    assert total >= 3

    monkeypatch.setattr(providers, "complete_bulk", _MockBulk(raise_after=2))
    with pytest.raises(KeyboardInterrupt):
        enrich.enrich(repo, graph, save_every=1)

    saved = store.load_graph(repo)
    assert sum(1 for n in saved.nodes.values() if n.summary) == 2

    resumed = build.build_structural(repo)  # carries the 2 done so far
    mock2 = _MockBulk()
    monkeypatch.setattr(providers, "complete_bulk", mock2)
    enrich.enrich(repo, resumed)
    assert all(n.summary for n in resumed.nodes.values())
    assert mock2.calls == total - 2


def test_clean_summary_strips_tool_call_narration():
    raw = (
        'Let me check. <function_calls><invoke name="read">'
        '<parameter name="path">x</parameter></invoke></function_calls> '
        "Provides caching utilities."
    )
    out = enrich._clean_summary(raw)
    assert "function_calls" not in out and "<invoke" not in out
    assert "Provides caching utilities." in out


def test_failed_call_leaves_node_for_retry(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    monkeypatch.setattr(providers, "complete_bulk", lambda *a, **k: None)  # all fail
    enrich.enrich(repo, graph)
    assert all(n.summary is None for n in graph.nodes.values())
    assert enrich.estimate_cost(graph).nodes == len(graph.nodes)
