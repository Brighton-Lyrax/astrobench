"""
Submit module: run CLI-based benchmarks with local model adapters.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .grader import grade_response
from .problems import load_problems


def list_all() -> list[dict[str, Any]]:
    return load_problems()


def run_benchmark(
    problems: list[dict[str, Any]] | None = None,
    categories: list[str] | None = None,
    difficulty: str | None = None,
    provider: str = "local",
    model: str = "ollama/llama3",
    output: str | None = None,
    show: bool = False,
    verbose: bool = False,
) -> dict[str, Any]:
    """Run benchmark on local problems and return summary."""
    if problems is None:
        problems = load_problems()
        if categories:
            problems = [p for p in problems if p.get("category") in categories]
        if difficulty:
            problems = [p for p in problems if p.get("difficulty") == difficulty]

    results = []
    by_category: dict[str, list[float]] = {}
    passed_total = sum(1 for p in problems if p.get("reference_answer"))

    for p in problems:
        ref = p.get("reference_answer", "")
        try:
            resp = _call_provider(provider, model, p["prompt"], p)
        except Exception as e:
            resp = f"[ERROR calling provider: {e}]"

        g = grade_response(p, resp)
        g["prompt"] = p["prompt"]
        results.append(g)
        cat = p.get("category", "uncategorized")
        by_category.setdefault(cat, []).append(g["score"])

    overall = (
        sum(1 for r in results if r["passed"]) / (passed_total or len(results))
        if results
        else 0.0
    )

    summary = {
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"]),
        "overall_score": round(sum(r["score"] for r in results) / len(results), 4) if results else 0.0,
        "by_category": {
            c: {
                "count": len(scores),
                "avg_score": round(sum(scores) / len(scores), 4),
            }
            for c, scores in by_category.items()
        },
        "results": results,
    }

    report = json.dumps(summary, indent=2)
    if output:
        Path(output).write_text(report)

    if show or verbose:
        print(report)

    return summary


# ---------------------------------------------------------------------------
# Provider callbacks
# ---------------------------------------------------------------------------

_PROVIDERS: dict[str, Any] = {}


def register(name: str):
    def wrapper(fn):
        _PROVIDERS[name] = fn
        return fn
    return wrapper


@register("local")
@register("ollama")
def _call_ollama(model: str, prompt: str, problem: dict[str, Any]) -> str:
    """Synchronous reference impl: import-time optional."""
    try:
        from ollama import chat as ollama_chat
    except ImportError as exc:
        return f"[ollama not installed: {exc}. Run: pip install ollama]"

    try:
        r = ollama_chat(
            model=model.split("/", 1)[-1],
            messages=[{"role": "user", "content": prompt}],
            options={"num_predict": 512},
        )
        return r.get("message", {}).get("content", "")
    except Exception as e:
        return f"[ollama call failed: {e}]"


@register("openai")
def _call_openai(model: str, prompt: str, problem: dict[str, Any]) -> str:
    try:
        import openai
    except ImportError as exc:
        return f"[openai not installed: {exc}]"
    client = openai.OpenAI()
    try:
        r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
        return r.choices[0].message.content or ""
    except Exception as e:
        return f"[openai call failed: {e}]"


@register("anthropic")
def _call_anthropic(model: str, prompt: str, problem: dict[str, Any]) -> str:
    try:
        import anthropic
    except ImportError as exc:
        return f"[anthropic not installed: {exc}]"
    client = anthropic.Anthropic()
    try:
        r = client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
        return "".join(b.text for b in r.content if hasattr(b, "text"))
    except Exception as e:
        return f"[anthropic call failed: {e}]"


def _call_provider(provider: str, model: str, prompt: str, problem: dict[str, Any]) -> str:
    fn = _PROVIDERS.get(provider) or _PROVIDERS.get("local")
    return fn(model, prompt, problem)
