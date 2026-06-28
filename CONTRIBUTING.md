# Contributing to diffquiz

Thanks for being here! diffquiz is small and deliberately scoped, which makes it
a great repo for a first contribution. This guide covers how to set up, what to
work on, the checks to run, and how to get your change merged.

## Ways to contribute

- **Fix a bug** — found something broken? Open an issue with a repro, or send a PR.
- **Pick up a feature** — see [Roadmap](#roadmap--where-to-help) below. Anything
  unchecked is fair game.
- **Improve docs** — setup steps, recipes, examples, a demo GIF.

## How to contribute (the flow)

1. **Find something to work on** — browse the [open issues] and the
   [Roadmap](#roadmap--where-to-help).
2. **Open an issue first** (or comment on an existing one) describing what you
   plan to do. This avoids duplicate work and lets us agree on the approach
   before you write code — especially for the bigger features.
3. **Fork & branch** — `feat/<short-name>` or `fix/<short-name>`.
4. **Make the change with tests** (see [Checks](#checks-run-before-you-pr)).
5. **Run the checks** and make sure they pass.
6. **Open a PR** that references the issue and explains the *why*, not just the *what*.

[open issues]: https://github.com/Bravim-Ketan-Purohit/GIT-diff/issues

## Dev setup

```bash
git clone https://github.com/Bravim-Ketan-Purohit/GIT-diff
cd GIT-diff
uv venv --python 3.12              # or: python -m venv .venv && source .venv/bin/activate
uv pip install -e ".[ai,dev]"      # runtime + AI + test deps
uv run pytest                      # should be all green
```

(`uv` is recommended but optional — plain `pip install -e ".[ai,dev]"` works too.)

## Checks (run before you PR)

- **Tests pass:** `uv run pytest` — and add tests for any new behavior. The
  deterministic layers (extractor, graph model, store, retrieve, update, providers)
  are unit-tested; LLM calls are tested with a mock provider, never a live key.
- **Still works offline:** the tool must run with **no API key and no agent CLI**
  (it degrades to revealing the diff). Never make an LLM backend mandatory.
- **Dependency-light:** runtime deps are `rich` (+ optional `anthropic`). The graph
  uses only the standard library. Don't add runtime dependencies without discussion.
- **Quick manual smoke** (optional but nice): in a throwaway git repo,
  `diffquiz index --structural` then `diffquiz once`.
- **Style:** match the surrounding code — type hints, short docstrings, and the
  "every function degrades, never raises in the provider layer" convention.

Keep PRs **focused** — one change per PR.

## Project map

```
diffquiz/
  cli.py          # commands: index · once · watch  (+ map/ask to come)
  ai.py           # question generation + grading prompts
  git_utils.py    # git plumbing (diff, changed/untracked files)
  providers/      # LLM backends + routing (claude CLI, anthropic API, codex stub)
  graph/
    model.py      # Node / Edge / Graph
    extract/      # language extractors (Python via stdlib ast today)
    build.py      # build the structural graph
    enrich.py     # LLM node summaries (bottom-up, resumable, cost-gated)
    update.py     # incremental, diff-driven graph updates
    retrieve.py   # diff → changed symbols → grounding subgraph
    store.py      # persist the graph under .diffquiz/
tests/            # pytest suite
DESIGN.md         # architecture + the full phased plan
```

## Roadmap — where to help

The phased plan lives in [DESIGN.md](DESIGN.md). **M1–M3 (the core product) are
done**; below is what's open. Open an issue to claim one before starting.

### Good first issues (small, self-contained)
- **Another agent adapter** — Claude Code, Codex, Gemini, and OpenCode ship today;
  add the next one (Cursor, Aider, Amp, …) by copying any `diffquiz/providers/*_cli.py`.
  Keep it read-only / no-tools and degrade to `None` on any failure.
- **A new question or grading style** in `diffquiz/ai.py`.
- **Editor/multiplexer recipes** (zellij, wezterm, screen) for the split-pane view.
- **`docs/demo.gif`** — record a real session (this is the #1 thing that earns stars).

### Bigger features (please open an issue to discuss first)
- **M4 — Gamified knowledge map** (`diffquiz map`): a `progress.py` storing per-node
  scores/streaks in `.diffquiz/`, parsing the `SCORE:` line from grading. *(DESIGN §9, Phase 4)*
- **M5 — Second brain** (`diffquiz ask "…"`): query / RAG over the graph. *(DESIGN §8/§9, Phase 5 — deferred)*
- **Multi-language extractors** beyond Python (e.g. tree-sitter), behind the
  `LanguageExtractor` interface in `diffquiz/graph/extract/`.
- **Embeddings-backed retrieval** in `diffquiz/graph/retrieve.py` (it's structural today).
- **A Textual TUI** for the watch pane.
- **Spaced-repetition deck** built from past diffs.

## License

By contributing, you agree your contributions are licensed under the
[MIT License](LICENSE).
