# Frontend brief — diffquiz "setup" section

A handoff for the agent building the landing page. This describes **what the
setup section must do, why, and what data to use** — not how it should look.
All visual/layout/theme decisions are yours.

---

## 1. Context

**diffquiz** is a terminal tool that quizzes a developer on their coding agent's
diffs before they read them. To use it, a developer installs the CLI, picks which
coding agent powers the scoring, indexes their repo, and runs it beside their
agent.

**This feature** turns that into one paste. The visitor indicates which coding
agent they already use; the page gives them a single prompt to paste into that
agent; the agent then installs and configures diffquiz and explains how to use it.

**Why this way:** the audience already lives inside a coding agent, so "paste this
and let your agent set it up" is far lower friction than a list of shell commands.
The agent choice also determines which backend diffquiz uses for scoring.

---

## 2. What the section must do (functional requirements)

1. Let the visitor choose which coding agent they use — exactly these four options:
   **Claude Code**, **OpenAI Codex**, **Gemini CLI**, **OpenCode**.
2. For the chosen agent, present that agent's setup prompt and let the visitor
   **copy it to the clipboard in one action**.
3. Include brief instruction text: paste the copied prompt into that coding agent.
4. Offer a **manual-setup alternative** (plain shell commands) for visitors who'd
   rather not delegate to an agent.

(How you arrange or style any of this is up to you.)

---

## 3. The data, and where to get it (how to provide it)

**Single source of truth:** [`docs/setup-prompts.md`](setup-prompts.md) in this
repo. Read the content from there. It contains, as fenced ` ```text ` blocks:

- one ready-to-copy prompt per agent, under headings `Claude Code`,
  `OpenAI Codex`, `Gemini CLI`, `OpenCode`;
- a shell block under `Manual setup` for the fallback.

**Use the prompt text verbatim — do not paraphrase, summarize, or reformat it.**
Each prompt is safety-reviewed: it instructs the agent to ask before installing or
changing files, to avoid sudo / permission-skipping flags, and to verify each
step. Rewording can silently drop those guarantees, and the install commands were
already corrected once — don't regenerate them from memory.

Agent → which prompt to show (each prompt already contains the correct
`export DIFFQUIZ_PROVIDER=...`, so you don't set anything — just surface the right
block):

| Visitor uses | Prompt heading in `setup-prompts.md` | Backend baked into the prompt |
| --- | --- | --- |
| Claude Code | `Claude Code` | `claude` |
| OpenAI Codex | `OpenAI Codex` | `codex` |
| Gemini CLI | `Gemini CLI` | `gemini` |
| OpenCode | `OpenCode` | `opencode` |

Repo URL referenced inside the prompts (already embedded — don't change it):
`https://github.com/Bravim-Ketan-Purohit/GIT-diff`

> If you can't read `docs/setup-prompts.md`, ask for it. Do **not** reconstruct
> the prompts yourself.

---

## 4. Constraints (must-nots)

- Don't edit the Python CLI or the prompt wording. Prompt changes happen in
  `docs/setup-prompts.md` (and get re-reviewed), never inline in the frontend.
- Don't invent or "improve" install commands — use exactly what the doc has.
- Keep exactly these four agent options; they map 1:1 to supported backends.

---

## 5. One upcoming change to design the wiring around

diffquiz isn't on PyPI yet, so the prompts currently install from source
(git clone + uv/pip). Once it's published, the install line becomes
`uvx diffquiz` / `pip install diffquiz`. Pull the prompt text from one place
(mirror or read `docs/setup-prompts.md`) rather than hardcoding it in several
spots, so that single update is easy later.

---

## 6. Done when

- A visitor can choose their agent and copy that agent's **exact, unmodified**
  prompt in one action.
- A manual-setup alternative is available.
- The copied text matches `docs/setup-prompts.md` character-for-character.
