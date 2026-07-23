"""
AstroBench YAML-based problem loader.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import Iterator

PROBLEMS_DIR = Path(__file__).parent.parent / "problems"


def load_problems(category: str | None = None, difficulty: str | None = None,
                  categories: list[str] | None = None) -> list[dict]:
    """Load all problems, optionally filtered by category/categories and/or difficulty."""
    results: list[dict] = []
    for yml in sorted(PROBLEMS_DIR.glob("*.yaml")):
        data = yaml.safe_load(yml.read_text())
        for p in data.get("problems", []):
            cats_in = (categories or [])
            if category:
                cats_in = cats_in + [category]
            if cats_in and p.get("category") not in cats_in:
                continue
            if difficulty and p.get("difficulty") != difficulty:
                continue
            p["_source"] = str(yml)
            results.append(p)
    return results


def iter_categories() -> list[str]:
    cats = set()
    for yml in PROBLEMS_DIR.glob("*.yaml"):
        data = yaml.safe_load(yml.read_text())
        for p in data.get("problems", []):
            cats.add(p.get("category", "uncategorized"))
    return sorted(cats)
