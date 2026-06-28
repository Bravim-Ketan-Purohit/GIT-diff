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

## Install

```bash
pip install diffquiz            # core
pip install "diffquiz[ai]"      # + AI scoring & risk flags (recommended)
```

## Quickstart

```bash
# One-time: build the codebase graph that grounds every question
# (LLM-summarises your code; shows a cost estimate before spending anything)
diffquiz index

# In your project, after your agent has made some changes:
diffquiz once

# Or run it live in a pane and get quizzed on every change:
diffquiz watch
```

### Side-by-side with your agent (tmux)

```bash
# main pane = your agent, right third = diffquiz
tmux new-session \; split-window -h -p 33 'diffquiz watch'
```

### Scoring & risk flags (zero-config)

`diffquiz` writes questions and grades guesses using the first backend it finds:

1. **Claude Code, if you're logged in** — no API key needed. It calls `claude -p`
   under the hood using your existing session (tools disabled, so it only answers).
2. **`ANTHROPIC_API_KEY`**, if set — a direct API call.
3. **Offline** — neither available: it just reveals the diff after your guess.

```bash
export DIFFQUIZ_MODEL=claude-sonnet-4-6  # optional: sharper, slower than the default
```

## Why predict-first works

Prediction before feedback is one of the most reliable learning mechanics there is: the moment of *being slightly wrong* is what makes the correction stick. `diffquiz` weaponizes the 30 seconds you'd otherwise spend waiting for your agent — turning dead time into retention.

## Roadmap

See [DESIGN.md](DESIGN.md) for the full architecture and phased build.

- [x] Zero-config scoring via your existing Claude Code login (no API key)
- [x] Codebase **knowledge graph** (`diffquiz index`) that grounds questions in blast radius
- [x] LLM-enriched node summaries — one-time, cost-gated, resumable indexing
- [ ] Incremental graph updates on each diff + untracked-file support
- [ ] Streak + knowledge-coverage map (`diffquiz map`)
- [ ] More agent adapters (Codex, Gemini) — see `diffquiz/providers/`
- [ ] `docs/demo.gif` — record the first real session

Got an idea? [Open an issue](https://github.com/Bravim-Ketan-Purohit/GIT-diff/issues) — see [CONTRIBUTING](CONTRIBUTING.md).

## License

MIT © Bravim Purohit
