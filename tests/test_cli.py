import subprocess

from diffquiz import cli, providers
from diffquiz.graph import store
from diffquiz.providers.base import Provider


def _init_repo(tmp_path):
    repo = tmp_path
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=repo, check=True)
    (repo / "mod.py").write_text("def foo():\n    return 1\n")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=repo, check=True)
    return str(repo)


class _DummyPrompt:
    @staticmethod
    def ask(*a, **k):
        return "it returns 2 now"


def test_index_builds_graph(tmp_path):
    repo = _init_repo(tmp_path)
    assert cli.cmd_index(repo, structural=True) == 0
    assert (tmp_path / ".diffquiz" / "graph.json").exists()
    g = store.load_graph(repo)
    assert "mod.py::foo" in g.nodes


def test_run_round_grounds_prompt_from_graph(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    cli.cmd_index(repo, structural=True)
    (tmp_path / "mod.py").write_text("def foo():\n    return 2\n")  # create a diff

    captured = {}

    def fake_complete(prompt, *, model=None, max_tokens=400):
        captured["prompt"] = prompt
        return "SCORE: 100/100 — spot on."

    monkeypatch.setattr(providers, "complete_interactive", fake_complete)
    monkeypatch.setattr(cli, "Prompt", _DummyPrompt)

    assert cli._run_round(repo) is True
    assert "<context>" in captured["prompt"]   # grounding block was injected
    assert "foo" in captured["prompt"]          # changed symbol present


class _FakeBulk(Provider):
    name = "fake-bulk"

    def available(self):
        return True

    def complete(self, prompt, *, model=None, max_tokens=400):
        return "a one-line summary"


def test_index_enriches_with_yes(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.setattr(providers, "bulk_chain", lambda: [_FakeBulk()])
    assert cli.cmd_index(repo, yes=True) == 0
    g = store.load_graph(repo)
    assert any(n.summary for n in g.nodes.values())
    assert store.load_manifest(repo)["phase"] == "enriched"


def test_index_structural_does_not_enrich(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    calls = {"n": 0}

    def boom(*a, **k):
        calls["n"] += 1
        return "x"

    monkeypatch.setattr(providers, "complete_bulk", boom)
    assert cli.cmd_index(repo, structural=True) == 0
    assert calls["n"] == 0
    g = store.load_graph(repo)
    assert all(n.summary is None for n in g.nodes.values())


def test_index_no_backend_saves_structural(tmp_path, monkeypatch):
    repo = _init_repo(tmp_path)
    monkeypatch.setattr(providers, "bulk_chain", lambda: [])  # nothing available
    assert cli.cmd_index(repo, yes=True) == 0
    g = store.load_graph(repo)
    assert all(n.summary is None for n in g.nodes.values())
