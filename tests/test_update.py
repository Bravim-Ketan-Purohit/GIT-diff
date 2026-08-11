import subprocess

from diffquiz import git_utils, providers
from diffquiz.graph import build, enrich, store, update

MOD = "def foo():\n    return 1\n\n\ndef bar():\n    return foo()\n"


def _init(tmp_path, files):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    for name, content in files.items():
        (tmp_path / name).write_text(content)
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    return str(tmp_path)


class _MockBulk:
    def __init__(self):
        self.calls = 0

    def __call__(self, prompt, *, model=None, max_tokens=400):
        self.calls += 1
        return f"summary {self.calls}"


def test_untracked_shows_in_diff_and_changed_files(tmp_path):
    repo = _init(tmp_path, {"mod.py": MOD})
    (tmp_path / "new.py").write_text("def n():\n    return 9\n")
    assert "new.py" in git_utils.get_changed_files(repo)
    assert "new.py" in git_utils.get_uncommitted_diff(repo)


def test_store_dir_is_never_a_change(tmp_path):
    # Even with no .gitignore, diffquiz's own .diffquiz/ must not look like a change
    # (otherwise saving the graph would retrigger the quiz loop).
    repo = _init(tmp_path, {"mod.py": MOD})
    build.build_structural(repo)  # writes untracked .diffquiz/graph.json
    assert git_utils.get_changed_files(repo) == []
    assert ".diffquiz" not in git_utils.get_uncommitted_diff(repo)


def test_update_reextracts_changed_only(tmp_path, monkeypatch):
    repo = _init(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    monkeypatch.setattr(providers, "complete_bulk", _MockBulk())
    enrich.enrich(repo, graph)

    (tmp_path / "mod.py").write_text(MOD.replace("return 1", "return 42"))
    g = store.load_graph(repo)
    bar_summary = g.nodes["mod.py::bar"].summary
    update.update_from_diff(repo, g, reenrich=False)

    assert g.nodes["mod.py::foo"].summary is None          # changed -> cleared
    assert g.nodes["mod.py::bar"].summary == bar_summary    # unchanged -> kept


def test_update_reenrich_describes_only_changed(tmp_path, monkeypatch):
    repo = _init(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    monkeypatch.setattr(providers, "complete_bulk", _MockBulk())
    enrich.enrich(repo, graph)

    (tmp_path / "mod.py").write_text(MOD.replace("return 1", "return 42"))
    g = store.load_graph(repo)
    mock = _MockBulk()
    monkeypatch.setattr(providers, "complete_bulk", mock)
    update.update_from_diff(repo, g, reenrich=True)

    assert g.nodes["mod.py::foo"].summary is not None
    assert mock.calls == 2   # foo + the file node (both hashes changed); bar untouched


def test_update_adds_new_untracked_file(tmp_path):
    repo = _init(tmp_path, {"mod.py": MOD})
    graph = build.build_structural(repo)
    (tmp_path / "extra.py").write_text("def hi():\n    return 0\n")
    update.update_from_diff(repo, graph, reenrich=False)
    assert "extra.py::hi" in graph.nodes


def test_update_removes_deleted_file(tmp_path):
    repo = _init(tmp_path, {"mod.py": MOD, "gone.py": "def g():\n    return 0\n"})
    graph = build.build_structural(repo)
    assert "gone.py::g" in graph.nodes
    (tmp_path / "gone.py").unlink()
    update.update_from_diff(repo, graph, reenrich=False)
    assert not any(n.path == "gone.py" for n in graph.nodes.values())
