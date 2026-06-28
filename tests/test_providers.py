import json
import shutil
import subprocess

from diffquiz import providers
from diffquiz.providers.base import Provider
from diffquiz.providers.claude_cli import ClaudeCLIProvider
from diffquiz.providers.codex_cli import CodexCLIProvider
from diffquiz.providers.gemini_cli import GeminiCLIProvider
from diffquiz.providers.opencode_cli import OpenCodeProvider


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


def test_claude_cli_rejects_flaglike_model(monkeypatch):
    captured = {}

    def fake_run(cmd, *a, **k):
        captured["cmd"] = list(cmd)
        return _Proc(0, json.dumps({"result": "ok"}))

    monkeypatch.setattr(shutil, "which", lambda _: "/x/claude")
    monkeypatch.setattr(subprocess, "run", fake_run)

    ClaudeCLIProvider().complete("q", model="--dangerously-skip-permissions")
    assert "--model" not in captured["cmd"]   # flag-like value rejected

    ClaudeCLIProvider().complete("q", model="claude-haiku-4-5")
    assert "--model" in captured["cmd"] and "claude-haiku-4-5" in captured["cmd"]


# --- codex / gemini / opencode adapters -----------------------------------

def test_codex_reads_final_message_file(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/codex")

    def fake_run(cmd, *a, **k):
        path = cmd[cmd.index("-o") + 1]   # codex writes the final message here
        with open(path, "w", encoding="utf-8") as f:
            f.write("  codex answer  ")
        return _Proc(0, "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert CodexCLIProvider().complete("q") == "codex answer"


def test_codex_nonzero_is_none(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/codex")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(1, ""))
    assert CodexCLIProvider().complete("q") is None


def test_codex_unavailable(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: None)
    assert CodexCLIProvider().complete("q") is None


def test_gemini_returns_stdout(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/gemini")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(0, "gemini answer\n"))
    assert GeminiCLIProvider().complete("q") == "gemini answer"


def test_gemini_unavailable(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: None)
    assert GeminiCLIProvider().complete("q") is None


def test_opencode_strips_ansi(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/opencode")
    monkeypatch.setattr(
        subprocess, "run", lambda *a, **k: _Proc(0, "\x1b[0mopencode answer\x1b[0m\n")
    )
    assert OpenCodeProvider().complete("q") == "opencode answer"


def test_opencode_nonzero_is_none(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: "/x/opencode")
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: _Proc(1, ""))
    assert OpenCodeProvider().complete("q") is None


def test_non_claude_adapters_ignore_claude_default_model(monkeypatch):
    captured = {}

    def fake_run(cmd, *a, **k):
        captured["cmd"] = list(cmd)
        if "-o" in cmd:
            with open(cmd[cmd.index("-o") + 1], "w", encoding="utf-8") as f:
                f.write("x")
        return _Proc(0, "x")

    monkeypatch.setattr(shutil, "which", lambda _: "/x/bin")
    monkeypatch.setattr(subprocess, "run", fake_run)

    GeminiCLIProvider().complete("q", model="claude-haiku-4-5-20251001")
    assert "-m" not in captured["cmd"]   # our Claude default isn't sent to Gemini

    GeminiCLIProvider().complete("q", model="gemini-2.5-pro")
    assert "-m" in captured["cmd"] and "gemini-2.5-pro" in captured["cmd"]
