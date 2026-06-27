import json
import shutil
import subprocess

from diffquiz import providers
from diffquiz.providers.base import Provider
from diffquiz.providers.claude_cli import ClaudeCLIProvider


class _Fake(Provider):
    def __init__(self, name, avail, out):
        self.name, self._avail, self._out, self.calls = name, avail, out, 0

    def available(self):
        return self._avail

    def complete(self, prompt, *, model=None, max_tokens=400):
        self.calls += 1
        return self._out


def test_route_falls_through_on_none(monkeypatch):
    a, b, c = _Fake("a", True, None), _Fake("b", True, "hi"), _Fake("c", True, "x")
    monkeypatch.setattr(providers, "interactive_chain", lambda: [a, b, c])
    assert providers.complete_interactive("p") == "hi"
    assert (a.calls, b.calls, c.calls) == (1, 1, 0)


def test_route_skips_unavailable(monkeypatch):
    a, b = _Fake("a", False, "nope"), _Fake("b", True, "yes")
    monkeypatch.setattr(providers, "bulk_chain", lambda: [a, b])
    assert providers.complete_bulk("p") == "yes"
    assert a.calls == 0


def test_route_none_when_nothing_available(monkeypatch):
    monkeypatch.setattr(providers, "interactive_chain", lambda: [_Fake("a", False, "x")])
    assert providers.complete_interactive("p") is None


# --- claude CLI adapter ---------------------------------------------------

class _Proc:
    def __init__(self, rc, out):
        self.returncode, self.stdout, self.stderr = rc, out, ""


def test_claude_cli_parses_result(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/claude")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(0, json.dumps({"result": " hi "})))
    assert ClaudeCLIProvider().complete("q") == "hi"


def test_claude_cli_unavailable(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: None)
    assert ClaudeCLIProvider().complete("q") is None


def test_claude_cli_bad_json_is_none(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/claude")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(0, "not json"))
    assert ClaudeCLIProvider().complete("q") is None


def test_claude_cli_nonzero_exit_is_none(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/claude")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(1, ""))
    assert ClaudeCLIProvider().complete("q") is None
