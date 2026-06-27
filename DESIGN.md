# diffquiz — Design

> **Status:** design draft · **Last updated:** 2026-06-27
>
> This document is the blueprint for diffquiz's next phase: turning the codebase
> itself into a persistent, queryable knowledge graph that grounds every quiz —
> and lays the foundation for a "codebase second brain."

---

## 1. Vision

diffquiz today asks you to predict a diff, then reveals it. The question is built
from the diff alone, so it can only ask *"what changed in `auth.py`?"*

The next version builds a **semantic graph of the codebase** — every file, class,
and function, plus how they call, contain, and import one another, each enriched
with an LLM-written description. The graph becomes **agent memory**: it persists,
it updates incrementally as your agent edits the repo, and every quiz question is
**grounded** in it.

That unlocks two things a raw-diff tool can't do:

1. **Blast-radius questions.** Not *"what changed in `validate_token`?"* but
   *"`validate_token` changed — it's called by 3 routes, what breaks?"* The diff
   says *what* changed; the graph says *what it touches*.
2. **A gamified knowledge map.** Because the graph is a complete model of the
   codebase, diffquiz can track which parts *you* actually understand — a running
   coverage score that grows as the project is built. Learning the codebase as it
   ships, with a score, is the sticky loop.

Longer term the same graph powers a **second brain**: ask questions about the
codebase, RAG over it, navigate it. That is an explicit Phase 5 — not v1 (see
[§8 Non-goals](#8-non-goals)).

---

## 2. Design principles

- **The expensive work happens once.** Building the enriched graph is token-heavy.
  It must be a deliberate, cost-estimated, **resumable**, **cached** step — never a
  surprise on first launch. After that, only *changes* cost tokens.
- **Cheap per-diff path.** Every interactive quiz feeds the LLM a *small retrieved
  subgraph*, never the whole graph. Watch mode must never quietly eat the quota a
  developer needs for their actual coding.
- **Right tool for each job size.** Bulk indexing → batched direct API. Per-diff
  questions → the user's already-authenticated agent CLI (zero config).
- **Graceful degradation, top to bottom.** No graph → fall back to diff-only
  questions (today's behavior). No LLM enrichment → structural-only questions. No
  key *and* no agent CLI → just reveal the diff. It always works offline.
- **Dependency-light core.** Start with the Python standard library (`ast`) for
  parsing; abstract it behind an interface so heavier multi-language backends
  (tree-sitter) are additive, not required.

---

## 3. The three guardrails

These exist because we deliberately chose the **semantically rich** graph over a
cheap structural one. They are what make "token-heavy upfront" safe rather than a
footgun.

1. **One-time, cached, resumable index.** `diffquiz index` shows a size/cost
   estimate before spending anything, writes to disk, and on interruption resumes
   from where it stopped (per-node content hashing — already-described, unchanged
   nodes are skipped).
2. **Bulk indexing does not go through the agent CLI.** Shelling out to `claude -p`
   thousands of times means a cold agent boot per call *and* drains the user's
   coding quota. Bulk enrichment uses the **direct API** with a cheap model;
   the CLI is reserved for the one-off per-diff calls.
3. **Quiz time retrieves a subgraph, never the whole graph.** Given the changed
   symbols, pull their nodes + 1-hop neighbors and ground the question on that
   small slice. This keeps every per-diff call cheap and bounded.

---

## 4. Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  diffquiz index   (one-time, resumable, cost-estimated)            │
│                                                                    │
│   source tree ──▶ extract (ast) ──▶ structural skeleton graph      │
│                                          │                         │
│                                          ▼                         │
│                              enrich (LLM, bulk API) ──▶ summaries  │
│                                          │                         │
│                                          ▼                         │
│                              persist  .diffquiz/graph.json         │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  diff arrives  (watch / once — cheap, incremental)                 │
│                                                                    │
│   git diff HEAD ──▶ update graph (re-describe changed nodes only)  │
│                                          │                         │
│                                          ▼                         │
│                     retrieve subgraph around changed symbols       │
│                                          │                         │
│                                          ▼                         │
│      generate grounded question  ──▶  you predict                  │
│                                          │                         │
│                                          ▼                         │
│      reveal diff  +  grounded scorecard                            │
│                                          │                         │
│                                          ▼                         │
│      update knowledge-coverage map  (the gamified score)           │
└──────────────────────────────────────────────────────────────────┘
```

### Layers

| Layer       | Responsibility                                                        |
| ----------- | --------------------------------------------------------------------- |
| **extract** | Static parse → structural nodes & edges. Deterministic, zero tokens.  |
| **enrich**  | LLM-written `summary` per node, bottom-up. The expensive, one-time bit.|
| **store**   | Load/save the graph + index manifest to `.diffquiz/`. Resumable.       |
| **update**  | On a diff, patch only changed nodes/edges. Cheap.                      |
| **retrieve**| Pull the relevant subgraph for a set of changed symbols.              |
| **providers**| Route an LLM call to API / agent-CLI / offline by job size.          |
| **ai**      | `generate_question` / `grade_prediction`, now graph-grounded.         |
| **progress**| Knowledge-coverage scoring — the gamification store.                  |

---

## 5. Data model

The graph is two flat lists — nodes and edges — serialized as JSON. Flat keeps it
dependency-free and trivially diffable; we can swap in a real graph store later
behind the same `store` interface.

### Node

```jsonc
{
  "id": "diffquiz/ai.py::grade_prediction",  // stable: <path>::<qualname>
  "kind": "function",                         // file | class | function | method
  "name": "grade_prediction",
  "path": "diffquiz/ai.py",
  "span": [64, 92],                           // [start_line, end_line]
  "signature": "grade_prediction(diff: str, prediction: str) -> str | None",
  "summary": "Scores the developer's guess against the real diff and flags risks; returns None offline.",
  "summary_model": "claude-haiku-4-5-20251001",
  "content_hash": "sha1:…",                   // hash of the source span
  "last_indexed": "2026-06-27T15:24:53Z"
}
```

`content_hash` is the linchpin of incrementality and resumability: if a node's
source span hashes the same as what's already in the graph, its `summary` is
reused and **no tokens are spent**.

### Edge

```jsonc
{
  "src": "diffquiz/cli.py::_run_round",
  "dst": "diffquiz/ai.py::grade_prediction",
  "type": "calls",                  // contains | calls | imports | inherits | references
  "resolved": true                  // false = dst is external/unresolved (e.g. stdlib)
}
```

### On-disk layout (`.diffquiz/`, already git-ignored)

```
.diffquiz/
  graph.json        # nodes + edges
  manifest.json     # index progress: file hashes, nodes described, model, version
  progress.json     # per-node knowledge-coverage scores (gamification)
```

Repo-local (not `~/.diffquiz/`) so the graph travels with the working copy and is
naturally per-project. `.gitignore` already excludes `.diffquiz/`.

---

## 6. Providers — removing the API-key wall

A `providers` package abstracts "ask the LLM" and routes by **job size**, because
the right backend differs for a 900-call batch vs. a single quiz question.

**Detection** (in precedence order):
- `ANTHROPIC_API_KEY` set → direct Anthropic API available.
- `shutil.which("claude")` → Claude Code headless (`claude -p … --output-format json`).
- `shutil.which("codex")` / others → adapter (good-first-issue).
- none → offline.

**Routing:**

| Call type                  | Preference order                          | Why                                            |
| -------------------------- | ----------------------------------------- | ---------------------------------------------- |
| **Bulk** (index enrichment)| API key → agent CLI → skip (structural)   | Batchable, cheap model; CLI cold-boot × N is slow & drains coding quota. |
| **Interactive** (per diff) | agent CLI → API key → offline template    | Zero-config; one small call is fine on the CLI.|

Each agent adapter implements a tiny interface so adding Gemini/Cursor is a small,
self-contained PR:

```python
class Provider:
    def available(self) -> bool: ...
    def complete(self, prompt: str, *, model: str | None, max_tokens: int) -> str | None: ...
```

The Claude CLI adapter keeps the model on a leash so it only ever answers:

```python
cmd = ["claude", "-p", prompt, "--output-format", "json", "--tools", ""]  # "" disables all tools
```

Parsing is defensive (`.result` from the JSON, fall back to offline on any
surprise) — these CLIs rev fast.

---

## 7. Module layout (target)

```
diffquiz/
  __init__.py
  cli.py              # commands: index · once · watch · map · (ask → Phase 5)
  git_utils.py        # existing git wrappers
  ai.py               # generate_question / grade_prediction (graph-grounded)
  progress.py         # knowledge-coverage scoring store
  graph/
    __init__.py
    model.py          # Node, Edge, Graph dataclasses + JSON (de)serialize
    store.py          # .diffquiz/ load/save, manifest, resumability
    build.py          # orchestrate parse → enrich → persist (cost estimate first)
    enrich.py         # bulk LLM node summaries (bottom-up)
    update.py         # incremental patch on a diff
    retrieve.py       # subgraph retrieval around changed symbols
    extract/
      __init__.py
      base.py         # LanguageExtractor interface
      python.py       # stdlib `ast` extractor (v1)
  providers/
    __init__.py       # detection + precedence routing
    base.py           # Provider interface
    anthropic_api.py  # direct API (bulk)
    claude_cli.py     # claude -p adapter (interactive)
    codex_cli.py      # stub — good-first-issue
```

---

## 8. Non-goals

Kept off the table deliberately so the tight, lovable quiz isn't swallowed by a
platform:

- **No query/RAG surface in v1.** `diffquiz ask "…"` is Phase 5, reusing the same
  graph once it's proven by the quiz.
- **No embeddings / vector store yet.** Retrieval is structural (graph traversal
  around changed symbols). Add embeddings only if structural retrieval proves
  insufficient.
- **No multi-language on day one.** Python (`ast`) first; tree-sitter backends are
  additive behind the extractor interface.
- **No server, no daemon, no web UI.** Terminal-first.

---

## 9. Phased build order

Front-loaded so the **token-free, high-value** work lands first and de-risks the
expensive enrichment before a single token is spent.

- **Phase 0 — Providers (no graph yet).** Build `providers/`, remove the API-key
  wall, route per-diff questions through the local `claude` CLI. Independent, ships
  the "works with whatever agent you already have" win immediately.
- **Phase 1 — Structural graph.** `extract/python.py` + `graph/model.py` +
  `store.py`. `diffquiz index --structural` builds a token-free skeleton; wire
  `retrieve.py` so questions already gain blast-radius context. **Zero token cost.**
- **Phase 2 — LLM enrichment.** `enrich.py` + cost estimate + resumability.
  Questions become fully grounded. This is where the upfront tokens are spent —
  guarded by §3.
- **Phase 3 — Incremental update.** `update.py`: a diff re-describes only changed
  nodes and repairs their edges. Integrate retrieval into `generate_question` /
  `grade_prediction`. Per-diff path stays cheap.
- **Phase 4 — Gamification.** `progress.py` + `diffquiz map`: knowledge-coverage
  score, weak spots, streaks. The "learn it as it's built" loop.
- **Phase 5 — Second brain (deferred).** `diffquiz ask`, richer retrieval,
  multi-language extractors, more agent adapters.

---

## 10. Open decisions

- **Index granularity** — describe at function level only, or also file/module
  level? (Leaning: bottom-up — functions, then classes/files summarizing children,
  so parents are cheap.)
- **Cost-estimate model** — how to estimate tokens before indexing (node count ×
  avg span size) and where to set the "this will cost ~$X / ~N calls, continue?"
  gate.
- **Edge resolution depth** — how hard to try resolving `calls`/`imports` to real
  nodes vs. marking them `resolved: false`. Cheap heuristics first.
- **Knowledge-score model** — what makes a node "understood": last quiz score,
  decay over time (spaced repetition), or both.
```
