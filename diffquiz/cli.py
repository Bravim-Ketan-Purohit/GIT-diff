"""diffquiz — predict the diff before you read what your AI just wrote."""
from __future__ import annotations

import argparse
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

from . import ai, git_utils
from .graph import build, retrieve, store

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


def cmd_index(repo: str) -> int:
    console.print(Panel(
        f"{BANNER}\n[dim]Indexing the codebase into a graph…[/]",
        expand=False, border_style="cyan",
    ))
    graph = build.build_structural(repo)
    files = store.load_manifest(repo).get("files", 0)
    console.print(
        f"[green]Indexed[/] {files} files · "
        f"[bold]{len(graph.nodes)}[/] nodes · [bold]{len(graph.edges)}[/] edges "
        "→ [dim].diffquiz/graph.json[/]"
    )
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
        help="structure only (current default; LLM enrichment lands in Phase 2)",
    )

    args = parser.parse_args(argv)

    if args.command == "watch" and args.interval <= 0:
        parser.error("--interval must be greater than 0")

    if not git_utils.is_git_repo(args.repo):
        console.print(f"[red]Not a git repo:[/] {args.repo}")
        return 1

    if args.command == "watch":
        return cmd_watch(args.repo, args.interval)
    if args.command == "index":
        return cmd_index(args.repo)
    # Default to a single round if no subcommand given.
    return cmd_once(args.repo)


if __name__ == "__main__":
    sys.exit(main())
