from pathlib import Path

from diffquiz.graph.extract import for_path

FIXTURE = Path(__file__).parent / "fixtures" / "sample.py"


def test_extracts_nodes_and_edges():
    nodes, edges = for_path("sample.py").extract("sample.py", FIXTURE.read_text())
    by_id = {n.id: n for n in nodes}

    assert by_id["sample.py"].kind == "file"
    assert by_id["sample.py::helper"].kind == "function"
    assert by_id["sample.py::Greeter"].kind == "class"
    assert by_id["sample.py::Greeter.greet"].kind == "method"
    assert "def helper(x)" in by_id["sample.py::helper"].signature

    def has(t, s, d):
        return any(e.type == t and e.src == s and e.dst == d for e in edges)

    assert has("contains", "sample.py", "sample.py::helper")
    assert has("contains", "sample.py::Greeter", "sample.py::Greeter.greet")
    assert has("calls", "sample.py::Greeter.greet", "helper")   # unresolved name
    assert any(e.type == "imports" and e.dst == "os" for e in edges)


def test_syntax_error_still_yields_file_node():
    nodes, edges = for_path("bad.py").extract("bad.py", "def (:\n")
    assert len(nodes) == 1 and nodes[0].kind == "file"
    assert edges == []
