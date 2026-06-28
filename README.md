<div align="center">

# 🎯 diffquiz

**Predict the diff before you read what your AI just wrote.**

*A terminal companion that quizzes you on every change your coding agent makes — so you actually understand your own codebase instead of rubber-stamping it.*

[![PyPI](https://img.shields.io/badge/pip%20install-diffquiz-3670A0?style=flat-square&logo=python&logoColor=white)](https://github.com/Bravim-Ketan-Purohit/GIT-diff)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat-square)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

<!-- Drop a terminal recording here. asciinema or a GIF. This is the #1 thing that earns stars. -->
<!-- ![demo](docs/demo.gif) -->

</div>

---

## The problem

AI agents write code faster than you can read it. So you don't read it. You skim the green squares, hit accept, and three weeks later you can't answer basic questions about your own project — *what does this function return, where is this used, why is it built this way.*

The danger isn't that the AI is wrong. It's that **you stopped paying attention.**

`diffquiz` fixes that with one mechanic backed by learning science: **commit to a guess before you see the answer.** Before it reveals what your agent changed, it asks you to predict it. That single act of prediction is what turns passive skimming into actual understanding — and it catches bugs you'd otherwise wave through.

## How it works

1. Run `diffquiz watch` in a split terminal pane next to your coding agent.
2. Your agent edits the repo. `diffquiz` notices the new changes.
3. **Before showing you the diff,** it asks: *"`auth.py` changed — what do you think changed, and why?"*
4. You type a one-line prediction.
5. It reveals the real diff, then (with an API key) scores your guess and **flags any bugs or risks it spots.**

You learn the codebase as it's being built, and you stop merging code you never read.

## Setup

### Requirements

- **Python 3.9+**
- **git** (diffquiz reads your repo through git)
- *Optional, for AI scoring & graph enrichment* — either **Claude Code** already
  logged in (zero config, no key), or an **`ANTHROPIC_API_KEY`**. Without either,
  diffquiz still runs; it just reveals the diff without a score.

### Install

> Not on PyPI yet — install from source. (`pip install diffquiz` lands once published.)

With **[uv](https://docs.astral.sh/uv/)** (recommended):

```bash
git clone https://github.com/Bravim-Ketan-Purohit/GIT-diff
cd GIT-diff
uv venv --python 3.12
uv pip install -e ".[ai]"        # core + AI scoring; drop [ai] for offline-only
uv run diffquiz --help
```

Or with plain `pip`:

```bash
git clone https://github.com/Bravim-Ketan-Purohit/GIT-diff
cd GIT-diff
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[ai]"
diffquiz --help
```

### Choose a backend (optional, recommended)

diffquiz writes questions, grades guesses, and summarises your code using the
**first backend it finds**:

| Priority | Backend | How to enable |
| --- | --- | --- |
| 1 | **Claude Code** — ideal for the live quiz | Just be logged in; `claude -p` is used under the hood (no key, tools disabled) |
| 2 | **Anthropic API** — ideal for the one-time index | `export ANTHROPIC_API_KEY=sk-...` |
| 3 | **Offline** | Nothing — it still works, just without the AI scorecard |

```bash
export ANTHROPIC_API_KEY=sk-...          # optional: enables the API backend
export DIFFQUIZ_MODEL=claude-sonnet-4-6  # optional: override the default model
```

> **Tip:** for the one-time `diffquiz index`, a direct `ANTHROPIC_API_KEY` is far
> faster/cheaper than the CLI (which cold-boots per node). For the live quiz, your
> Claude Code login is perfect.

### Build the codebase graph (one-time)

From inside the project you want to study:

```bash
cd /path/to/your/project
diffquiz index               # parse your code, then LLM-summarise it (asks before spending)
diffquiz index --structural  # or: structure only — no LLM, zero tokens
```

This writes a graph under `.diffquiz/` that grounds every question in how your
code actually connects. It's **cost-gated** (you confirm before any spend),
**resumable**, and re-indexing only re-describes what changed.

> Add `.diffquiz/` to your project's `.gitignore`. (diffquiz already ignores it
> internally, but you don't want the graph in version control.)

## Usage

```bash
diffquiz once            # one quiz round on the current uncommitted changes
diffquiz watch           # quiz on every change as your agent works
diffquiz watch -i 5      # ...polling every 5s (default: 3)
diffquiz -C /path once   # operate on a repo elsewhere
```

The graph refreshes automatically before each round, so questions always reflect
the code as it is right now — including brand-new files.

### Side-by-side with your agent (tmux)

```bash
# main pane = your agent, right third = diffquiz
tmux new-session \; split-window -h -p 33 'diffquiz watch'
```

### Command reference

| Command | What it does |
| --- | --- |
| `diffquiz index` | Build/refresh the graph (LLM-enriched, cost-gated) |
| `diffquiz index --structural` | Structure only — no LLM, free |
| `diffquiz index --yes` | Skip the cost confirmation |
| `diffquiz index --model <id>` | Model to use for enrichment |
| `diffquiz once` | One quiz round on the current diff |
| `diffquiz watch [-i SECS]` | Quiz on each change (default every 3s) |
| `-C, --repo <path>` | Run against a repo other than the current directory |

## Why predict-first works

Prediction before feedback is one of the most reliable learning mechanics there is: the moment of *being slightly wrong* is what makes the correction stick. `diffquiz` weaponizes the 30 seconds you'd otherwise spend waiting for your agent — turning dead time into retention.

## Roadmap

See [DESIGN.md](DESIGN.md) for the full architecture and phased build.

- [x] Zero-config scoring via your existing Claude Code login (no API key)
- [x] Codebase **knowledge graph** (`diffquiz index`) that grounds questions in blast radius
- [x] LLM-enriched node summaries — one-time, cost-gated, resumable indexing
- [x] Incremental graph updates on each diff + untracked-file support
- [ ] Streak + knowledge-coverage map (`diffquiz map`)
- [ ] More agent adapters (Codex, Gemini) — see `diffquiz/providers/`
- [ ] `docs/demo.gif` — record the first real session

Got an idea? [Open an issue](https://github.com/Bravim-Ketan-Purohit/GIT-diff/issues) — see [CONTRIBUTING](CONTRIBUTING.md).

## License

MIT © Bravim Purohit
