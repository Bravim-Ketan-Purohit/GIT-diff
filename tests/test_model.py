from diffquiz.graph.model import Edge, Graph, Node


def _graph():
    g = Graph()
    g.add_node(Node(id="f.py", kind="file", name="f.py", path="f.py", span=(1, 20)))
    g.add_node(Node(id="f.py::a", kind="function", name="a", path="f.py", span=(2, 6)))
    g.add_node(Node(id="f.py::b", kind="function", name="b", path="f.py", span=(8, 12)))
    g.add_edge(Edge("f.py", "f.py::a", "contains"))
    g.add_edge(Edge("f.py", "f.py::b", "contains"))
    g.add_edge(Edge("f.py::a", "f.py::b", "calls"))
    return g


def test_node_at_picks_most_specific():
    g = _graph()
    assert g.node_at("f.py", 3).id == "f.py::a"   # inside a's span
    assert g.node_at("f.py", 15).id == "f.py"     # only the file covers line 15
    assert g.node_at("other.py", 3) is None


def test_neighbors_both_directions():
    g = _graph()
    nb = g.neighbors("f.py::a", hops=1)
    assert "f.py::b" in nb   # a calls b
    assert "f.py" in nb      # file contains a


def test_json_roundtrip_restores_tuple_span():
    g = _graph()
    g2 = Graph.from_json(g.to_json())
    assert set(g2.nodes) == set(g.nodes)
    assert len(g2.edges) == len(g.edges)
    assert g2.nodes["f.py::a"].span == (2, 6)
