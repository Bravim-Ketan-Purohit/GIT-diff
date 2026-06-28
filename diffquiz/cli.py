"""diffquiz — predict the diff before you read what your AI just wrote."""
from __future__ import annotations

import argparse
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from . import ai, git_utils, providers
from .graph import build, enrich, retrieve, store

console = Console()

BANNER = "[bold cyan]diffquiz[/]  [dim]· predict before you read[/]"


def _grounding_for(repo: str, diff: str) -> str | None:
    """Retrieve a grounding subgraph for the diff, if a graph has been built."""
    graph = store.load_graph(repo)
    if graph is None:
        return None
    ids = retrieve.changed_symbols(graph, diff)
    return retrieve.subgraph_for(graph, ids) or None


def _run_round(repo: str) -> bool:
    """Run one quiz round on the current uncommitted diff.

    Returns True if a round actually ran (there was a diff), else False.
    """
    diff = git_utils.get_uncommitted_diff(repo)
    if not diff.strip():
        return False

    changed = git_utils.get_changed_files(repo)
    grounding = _grounding_for(repo, diff)

    console.print()
    console.print(Panel(BANNER, expand=False, border_style="cyan"))

    question = ai.generate_question(diff, changed, grounding=grounding)
    console.print(Panel(question, title="🧠 your move", border_style="yellow"))

    prediction = Prompt.ask("[bold]Your prediction[/]")

    # Reveal.
    console.print(Panel(
        Syntax(diff, "diff", theme="ansi_dark", word_wrap=True),
        title="🔍 what actually changed",
        border_style="green",
    ))

    scorecard = ai.grade_prediction(diff, prediction, grounding=grounding)
    if scorecard:
        console.print(Panel(scorecard, title="📊 scorecard", border_style="magenta"))
    else:
        console.print(
            "[dim]No LLM backend found — log in to Claude Code (or set "
            "ANTHROPIC_API_KEY) for scoring + risk flags.[/]"
        )
    return True


def cmd_once(repo: str) -> int:
    if not _run_round(repo):
        console.print("[dim]Nothing uncommitted to quiz on. Make some changes first.[/]")
    return 0


def _print_index_summary(repo: str, graph) -> None:
    m = store.load_manifest(repo)
    console.print(
        f"[green]Indexed[/] {m.get('files', 0)} files · "
        f"[bold]{len(graph.nodes)}[/] nodes · [bold]{len(graph.edges)}[/] edges · "
        f"[bold]{m.get('enriched', 0)}[/] summarised → [dim].diffquiz/graph.json[/]"
    )


def cmd_index(repo: str, *, structural: bool = False, yes: bool = False, model=None) -> int:
    console.print(Panel(
        f"{BANNER}\n[dim]Indexing the codebase into a graph…[/]",
        expand=False, border_style="cyan",
    ))
    graph = build.build_structural(repo)

    if structural:
        _print_index_summary(repo, graph)
        return 0

    est = enrich.estimate_cost(graph)
    if est.nodes == 0:
        console.print("[green]Already enriched[/] — nothing new to describe.")
        _print_index_summary(repo, graph)
        return 0

    backend = next((p.name for p in providers.bulk_chain() if p.available()), None)
    if backend is None:
        console.print(
            "[yellow]No LLM backend for enrichment[/] — structural graph saved. "
            "Log in to Claude Code or set ANTHROPIC_API_KEY, then run "
            "[bold]diffquiz index[/] again."
        )
        return 0
    if backend == "claude-cli":
        console.print(
            "[yellow]Heads up:[/] only the Claude CLI is available for bulk indexing — "
            "it's slow and spends your coding quota. A direct ANTHROPIC_API_KEY is faster."
        )

    if not yes:
        proceed = Confirm.ask(
            f"Describe [bold]{est.nodes}[/] nodes (~{est.est_tokens:,} tokens) "
            f"via [bold]{backend}[/]?",
            default=False,
        )
        if not proceed:
            console.print("[dim]Skipped enrichment. Structural graph saved.[/]")
            return 0

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            transient=True,
            console=console,
        ) as prog:
            task = prog.add_task("Describing nodes", total=est.nodes)
            enrich.enrich(repo, graph, model=model, on_node=lambda *_: prog.advance(task))
    except KeyboardInterrupt:
        console.print(
            "\n[yellow]Interrupted[/] — progress saved. Run "
            "[bold]diffquiz index[/] again to resume."
        )
        return 130

    _print_index_summary(repo, graph)
    return 0


def cmd_watch(repo: str, interval: float) -> int:
    console.print(Panel(
        f"{BANNER}\n[dim]Watching for changes every {interval:g}s · Ctrl-C to quit[/]",
        expand=False, border_style="cyan",
    ))
    last_seen = git_utils.diff_fingerprint(git_utils.get_uncommitted_diff(repo))
    try:
        while True:
            time.sleep(interval)
            diff = git_utils.get_uncommitted_diff(repo)
            fp = git_utils.diff_fingerprint(diff)
            if diff.strip() and fp != last_seen:
                _run_round(repo)
                # Re-read: the diff may have grown while we were quizzing.
                last_seen = git_utils.diff_fingerprint(
                    git_utils.get_uncommitted_diff(repo)
                )
    except KeyboardInterrupt:
        console.print("\n[dim]bye 👋[/]")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="diffquiz",
        description="Predict the diff before you read what your AI just wrote.",
    )
    parser.add_argument("-C", "--repo", default=".", help="path to the git repo")
    sub = parser.add_subparsers(dest="command")

    p_watch = sub.add_parser("watch", help="watch the repo and quiz on each change")
    p_watch.add_argument("-i", "--interval", type=float, default=3.0)

    sub.add_parser("once", help="quiz once on the current uncommitted changes")

    p_index = sub.add_parser(
        "index", help="build the codebase graph that grounds quizzes"
    )
    p_index.add_argument(
        "--structural", action="store_true",
        help="structure only — skip LLM enrichment",
    )
    p_index.add_argument(
        "-y", "--yes", action="store_true", help="skip the cost confirmation prompt",
    )
    p_index.add_argument(
        "--model", default=None,
        help="model for enrichment (default: $DIFFQUIZ_MODEL or haiku)",
    )

    args = parser.parse_args(argv)

    if not git_utils.is_git_repo(args.repo):
        console.print(f"[red]Not a git repo:[/] {args.repo}")
        return 1

    if args.command == "watch":
        return cmd_watch(args.repo, args.interval)
    if args.command == "index":
        return cmd_index(
            args.repo, structural=args.structural, yes=args.yes, model=args.model
        )
    # Default to a single round if no subcommand given.
    return cmd_once(args.repo)


if __name__ == "__main__":
    sys.exit(main())
