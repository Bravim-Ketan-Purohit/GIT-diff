from diffquiz.graph import store
from diffquiz.graph.model import Graph, Node


def test_save_load_graph_and_manifest(tmp_path):
    repo = str(tmp_path)
    assert store.load_graph(repo) is None

    g = Graph()
    g.add_node(Node(id="x.py", kind="file", name="x.py", path="x.py", span=(1, 3)))
    store.save_graph(repo, g)
    store.save_manifest(repo, {"phase": "structural", "nodes": 1})

    loaded = store.load_graph(repo)
    assert loaded is not None and "x.py" in loaded.nodes
    assert store.load_manifest(repo)["phase"] == "structural"
    assert (tmp_path / ".diffquiz" / "graph.json").exists()


def test_load_graph_handles_corrupt(tmp_path):
    (tmp_path / ".diffquiz").mkdir()
    (tmp_path / ".diffquiz" / "graph.json").write_text("{ not json")
    assert store.load_graph(str(tmp_path)) is None
