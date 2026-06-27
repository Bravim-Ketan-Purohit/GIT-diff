from diffquiz.graph import retrieve
from diffquiz.graph.model import Edge, Graph, Node

DIFF = """diff --git a/f.py b/f.py
--- a/f.py
+++ b/f.py
@@ -2,3 +2,4 @@ def a():
     x = 1
+    y = 2
"""


def _graph():
    g = Graph()
    g.add_node(Node(id="f.py", kind="file", name="f.py", path="f.py", span=(1, 20)))
    g.add_node(Node(id="f.py::a", kind="function", name="a", path="f.py",
                    span=(2, 6), signature="def a()"))
    g.add_node(Node(id="f.py::b", kind="function", name="b", path="f.py",
                    span=(8, 12), signature="def b()"))
    g.add_edge(Edge("f.py::b", "f.py::a", "calls"))   # b calls a
    return g


def test_changed_line_ranges():
    assert retrieve.changed_line_ranges(DIFF) == {"f.py": [(2, 5)]}


def test_new_file_dev_null_handled():
    diff = "--- /dev/null\n+++ b/new.py\n@@ -0,0 +1,2 @@\n+a\n+b\n"
    assert retrieve.changed_line_ranges(diff) == {"new.py": [(1, 2)]}


def test_changed_symbols_maps_to_most_specific_node():
    assert retrieve.changed_symbols(_graph(), DIFF) == ["f.py::a"]


def test_subgraph_text_shows_blast_radius():
    text = retrieve.subgraph_for(_graph(), ["f.py::a"])
    assert "[changed]" in text and "def a()" in text
    assert "call: b -> a" in text   # who calls the changed node
