# Setup prompts (for the landing page "paste into your agent" flow)

The idea: the visitor picks the coding agent they use (Claude Code / Codex /
Gemini / OpenCode), copies one prompt, and pastes it into that agent. The agent
installs diffquiz, pins the right backend, indexes the project, and then teaches
the user how to use it — one paste, fully set up.

Each prompt is **safe by default**: it tells the agent to ask before installing or
changing files, forbids sudo / permission-skipping flags, and has it verify each
step. Offer a **Manual setup** tab too (bottom of this file) for people who'd
rather run the commands themselves.

> **When diffquiz is on PyPI:** replace the clone + install step with
> `uvx diffquiz` (or `pip install diffquiz`) and drop the local clone.

---

## Anatomy (DRY source of truth)

All four prompts are the same core with **one line swapped** — step 2, the backend.

**Core template** (`{{BACKEND}}` is replaced per agent):

```text
Set up diffquiz for me in this project — it's a CLI that quizzes me on your diffs
before I read them, so I actually understand the code you write. Do the setup now.
Rules: ask me before any install or file change, never use sudo or any
permission-skipping / auto-approve flags, and stop and tell me if a step fails.

1. Install (not on PyPI yet — from source):
   - Clone https://github.com/Bravim-Ketan-Purohit/GIT-diff to a tools folder (e.g. ~/.diffquiz-src).
   - Install it as an isolated CLI on my PATH — e.g. `uv tool install --editable ~/.diffquiz-src`
     (or `pipx install ~/.diffquiz-src`, or a venv + `pip install -e ~/.diffquiz-src`). Add the
     Anthropic extra (`--with anthropic`) only if I'll use an Anthropic API key.
   - Verify: `diffquiz --help` prints usage.

2. Backend: {{BACKEND}}

3. Index THIS project (run from the repo root we're in):
   - `diffquiz index --structural`  (fast, free — builds the code graph that grounds questions).
     Tell me I can run `diffquiz index` (no flag) later for richer, LLM-written summaries.
   - Add `.diffquiz/` to this repo's .gitignore.

4. Then teach me, briefly:
   - How to run it beside you in a split pane:
     `tmux new-session \; split-window -h -p 33 'diffquiz watch'`
     (or, without tmux, just run `diffquiz watch` in a second terminal in this repo).
   - The loop: when you change code, diffquiz names the changed files and asks me to
     PREDICT the diff; I type a one-line guess; it reveals the real diff and SCORES it,
     flagging any risks.
   - The commands I'll use: `diffquiz once`, `diffquiz watch`, `diffquiz index`.

Keep the explanation short and friendly, and confirm each step worked.
```

**Backend lines** (step 2):

| Agent | `{{BACKEND}}` |
| --- | --- |
| Claude Code | diffquiz will use you (Claude Code) automatically — no API key. Run `export DIFFQUIZ_PROVIDER=claude` and offer to add it to my shell profile to pin it. |
| OpenAI Codex | Pin diffquiz to Codex: `export DIFFQUIZ_PROVIDER=codex` (offer to add it to my shell profile). Make sure I'm logged in: `codex login`. |
| Gemini CLI | Pin diffquiz to Gemini: `export DIFFQUIZ_PROVIDER=gemini` (offer to add it to my shell profile). Make sure the Gemini CLI is installed and authenticated. |
| OpenCode | Pin diffquiz to OpenCode: `export DIFFQUIZ_PROVIDER=opencode` (offer to add it to my shell profile). Make sure a provider is configured: `opencode auth`. |

---

## Ready-to-copy prompts

### Claude Code

```text
Set up diffquiz for me in this project — it's a CLI that quizzes me on your diffs
before I read them, so I actually understand the code you write. Do the setup now.
Rules: ask me before any install or file change, never use sudo or any
permission-skipping / auto-approve flags, and stop and tell me if a step fails.

1. Install (not on PyPI yet — from source):
   - Clone https://github.com/Bravim-Ketan-Purohit/GIT-diff to a tools folder (e.g. ~/.diffquiz-src).
   - Install it as an isolated CLI on my PATH — e.g. `uv tool install --editable ~/.diffquiz-src`
     (or `pipx install ~/.diffquiz-src`, or a venv + `pip install -e ~/.diffquiz-src`). Add the
     Anthropic extra (`--with anthropic`) only if I'll use an Anthropic API key.
   - Verify: `diffquiz --help` prints usage.

2. Backend: diffquiz will use you (Claude Code) automatically — no API key. Run
   `export DIFFQUIZ_PROVIDER=claude` and offer to add it to my shell profile to pin it.

3. Index THIS project (run from the repo root we're in):
   - `diffquiz index --structural`  (fast, free — builds the code graph that grounds questions).
     Tell me I can run `diffquiz index` (no flag) later for richer, LLM-written summaries.
   - Add `.diffquiz/` to this repo's .gitignore.

4. Then teach me, briefly:
   - How to run it beside you in a split pane:
     `tmux new-session \; split-window -h -p 33 'diffquiz watch'`
     (or, without tmux, just run `diffquiz watch` in a second terminal in this repo).
   - The loop: when you change code, diffquiz names the changed files and asks me to
     PREDICT the diff; I type a one-line guess; it reveals the real diff and SCORES it,
     flagging any risks.
   - The commands I'll use: `diffquiz once`, `diffquiz watch`, `diffquiz index`.

Keep the explanation short and friendly, and confirm each step worked.
```

### OpenAI Codex

```text
Set up diffquiz for me in this project — it's a CLI that quizzes me on your diffs
before I read them, so I actually understand the code you write. Do the setup now.
Rules: ask me before any install or file change, never use sudo or any
permission-skipping / auto-approve flags, and stop and tell me if a step fails.

1. Install (not on PyPI yet — from source):
   - Clone https://github.com/Bravim-Ketan-Purohit/GIT-diff to a tools folder (e.g. ~/.diffquiz-src).
   - Install it as an isolated CLI on my PATH — e.g. `uv tool install --editable ~/.diffquiz-src`
     (or `pipx install ~/.diffquiz-src`, or a venv + `pip install -e ~/.diffquiz-src`). Add the
     Anthropic extra (`--with anthropic`) only if I'll use an Anthropic API key.
   - Verify: `diffquiz --help` prints usage.

2. Backend: Pin diffquiz to Codex: `export DIFFQUIZ_PROVIDER=codex` (offer to add it
   to my shell profile). Make sure I'm logged in: `codex login`.

3. Index THIS project (run from the repo root we're in):
   - `diffquiz index --structural`  (fast, free — builds the code graph that grounds questions).
     Tell me I can run `diffquiz index` (no flag) later for richer, LLM-written summaries.
   - Add `.diffquiz/` to this repo's .gitignore.

4. Then teach me, briefly:
   - How to run it beside you in a split pane:
     `tmux new-session \; split-window -h -p 33 'diffquiz watch'`
     (or, without tmux, just run `diffquiz watch` in a second terminal in this repo).
   - The loop: when you change code, diffquiz names the changed files and asks me to
     PREDICT the diff; I type a one-line guess; it reveals the real diff and SCORES it,
     flagging any risks.
   - The commands I'll use: `diffquiz once`, `diffquiz watch`, `diffquiz index`.

Keep the explanation short and friendly, and confirm each step worked.
```

### Gemini CLI

```text
Set up diffquiz for me in this project — it's a CLI that quizzes me on your diffs
before I read them, so I actually understand the code you write. Do the setup now.
Rules: ask me before any install or file change, never use sudo or any
permission-skipping / auto-approve flags, and stop and tell me if a step fails.

1. Install (not on PyPI yet — from source):
   - Clone https://github.com/Bravim-Ketan-Purohit/GIT-diff to a tools folder (e.g. ~/.diffquiz-src).
   - Install it as an isolated CLI on my PATH — e.g. `uv tool install --editable ~/.diffquiz-src`
     (or `pipx install ~/.diffquiz-src`, or a venv + `pip install -e ~/.diffquiz-src`). Add the
     Anthropic extra (`--with anthropic`) only if I'll use an Anthropic API key.
   - Verify: `diffquiz --help` prints usage.

2. Backend: Pin diffquiz to Gemini: `export DIFFQUIZ_PROVIDER=gemini` (offer to add it
   to my shell profile). Make sure the Gemini CLI is installed and authenticated.

3. Index THIS project (run from the repo root we're in):
   - `diffquiz index --structural`  (fast, free — builds the code graph that grounds questions).
     Tell me I can run `diffquiz index` (no flag) later for richer, LLM-written summaries.
   - Add `.diffquiz/` to this repo's .gitignore.

4. Then teach me, briefly:
   - How to run it beside you in a split pane:
     `tmux new-session \; split-window -h -p 33 'diffquiz watch'`
     (or, without tmux, just run `diffquiz watch` in a second terminal in this repo).
   - The loop: when you change code, diffquiz names the changed files and asks me to
     PREDICT the diff; I type a one-line guess; it reveals the real diff and SCORES it,
     flagging any risks.
   - The commands I'll use: `diffquiz once`, `diffquiz watch`, `diffquiz index`.

Keep the explanation short and friendly, and confirm each step worked.
```

### OpenCode

```text
Set up diffquiz for me in this project — it's a CLI that quizzes me on your diffs
before I read them, so I actually understand the code you write. Do the setup now.
Rules: ask me before any install or file change, never use sudo or any
permission-skipping / auto-approve flags, and stop and tell me if a step fails.

1. Install (not on PyPI yet — from source):
   - Clone https://github.com/Bravim-Ketan-Purohit/GIT-diff to a tools folder (e.g. ~/.diffquiz-src).
   - Install it as an isolated CLI on my PATH — e.g. `uv tool install --editable ~/.diffquiz-src`
     (or `pipx install ~/.diffquiz-src`, or a venv + `pip install -e ~/.diffquiz-src`). Add the
     Anthropic extra (`--with anthropic`) only if I'll use an Anthropic API key.
   - Verify: `diffquiz --help` prints usage.

2. Backend: Pin diffquiz to OpenCode: `export DIFFQUIZ_PROVIDER=opencode` (offer to add
   it to my shell profile). Make sure a provider is configured: `opencode auth`.

3. Index THIS project (run from the repo root we're in):
   - `diffquiz index --structural`  (fast, free — builds the code graph that grounds questions).
     Tell me I can run `diffquiz index` (no flag) later for richer, LLM-written summaries.
   - Add `.diffquiz/` to this repo's .gitignore.

4. Then teach me, briefly:
   - How to run it beside you in a split pane:
     `tmux new-session \; split-window -h -p 33 'diffquiz watch'`
     (or, without tmux, just run `diffquiz watch` in a second terminal in this repo).
   - The loop: when you change code, diffquiz names the changed files and asks me to
     PREDICT the diff; I type a one-line guess; it reveals the real diff and SCORES it,
     flagging any risks.
   - The commands I'll use: `diffquiz once`, `diffquiz watch`, `diffquiz index`.

Keep the explanation short and friendly, and confirm each step worked.
```

---

## Manual setup (fallback tab)

For people who'd rather not delegate to an agent:

```bash
# 1. Install from source (until it's on PyPI)
git clone https://github.com/Bravim-Ketan-Purohit/GIT-diff ~/.diffquiz-src
uv tool install --editable ~/.diffquiz-src   # or: pipx install ~/.diffquiz-src / venv + pip
#   add `--with anthropic` if you'll use an Anthropic API key
diffquiz --help

# 2. (optional) pin your backend — claude / codex / gemini / opencode / anthropic
export DIFFQUIZ_PROVIDER=codex

# 3. In your project: build the graph, then quiz
cd /path/to/your/project
diffquiz index --structural      # fast/free; `diffquiz index` adds LLM summaries
echo ".diffquiz/" >> .gitignore
tmux new-session \; split-window -h -p 33 'diffquiz watch'
```
