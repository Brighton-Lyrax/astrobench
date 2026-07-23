"""
CLI entry point for AstroBench.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from astrobench.problems import load_problems, iter_categories, PROBLEMS_DIR
from astrobench.submit import run_benchmark


@click.group()
def cli() -> None:
    """AstroBench: open-source LLM benchmark using astrophysics reasoning."""


@cli.command()
@click.option("--category", multiple=True, help="Filter by category.")
@click.option("--difficulty", default=None, help="Filter by difficulty.")
def problems(category: tuple[str], difficulty: str | None) -> None:
    """List all benchmark problems."""
    ps = load_problems(categories=list(category) if category else None, difficulty=difficulty)
    click.echo(f"Loaded {len(ps)} problems from {PROBLEMS_DIR}")
    for p in ps:
        source = Path(p.get("_source", "?")).name
        click.echo(
            f"  [{p.get('difficulty','?')}] {p['id']} | {p.get('category','?')} | {p['prompt'][:80]}... ({source})"
        )


@cli.command()
@click.option("--category", multiple=True, help="Filter by category.")
@click.option("--difficulty", default=None, help="Filter by difficulty.")
@click.option("--provider", default="local", show_default=True,
              help="Provider: local/ollama/openai/anthropic")
@click.option("--model", default="ollama/llama3", show_default=True,
              help="Model id, e.g. openai/gpt-4o, anthropic/claude-sonnet-4-20250514")
@click.option("--output", "-o", default=None, help="Write JSON report to this file.")
@click.option("--show/--no-show", default=False, help="Print full JSON report to stdout.")
@click.option("--verbose", "-v", is_flag=True, default=False)
def run(
    category: tuple[str],
    difficulty: str | None,
    provider: str,
    model: str,
    output: str | None,
    show: bool,
    verbose: bool,
) -> None:
    """Run the benchmark and grade responses."""
    cats = list(category) if category else None
    summary = run_benchmark(
        categories=cats,
        difficulty=difficulty,
        provider=provider,
        model=model,
        output=output,
        show=show,
        verbose=verbose,
    )

    click.echo(f"\n{'='*60}")
    click.echo(f"AstroBench Results: {summary['passed']}/{summary['total']} passed")
    click.echo(f"Overall score : {summary['overall_score']:.2%}")
    click.echo(f"{'='*60}")
    for cat, stats in sorted(summary["by_category"].items()):
        click.echo(f"  {cat:<30s} {stats['avg_score']:.2%}  (n={stats['count']})")


@cli.command()
def categories() -> None:
    """List available problem categories."""
    cats = iter_categories()
    for c in cats:
        click.echo(c)


@cli.command()
@click.argument("url")
@click.option("--provider", default="local")
@click.option("--model", default="ollama/llama3")
@click.option("--output", "-o", default=None)
def submit(url: str, provider: str, model: str, output: str | None) -> None:
    """Submit to the public leaderboard (future: requires API key)."""
    click.echo("[WARN] Public leaderboard not yet open-sourced.")
    click.echo(f"       Set ASTROBENCH_API_KEY and rerun. URL: {url}")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
