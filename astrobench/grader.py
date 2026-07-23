"""
Grading logic: normalized-score evaluation over model responses.
"""
from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any


def _normalize(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.lower().strip().split())


def grade_response(problem: dict[str, Any], response: str) -> dict[str, Any]:
    """Grade a model response against a problem's reference solution."""
    ref = problem.get("reference_answer", "")
    ref_norm = _normalize(ref)
    resp_norm = _normalize(response)

    if not ref_norm and not resp_norm:
        score = 0.0
        method = "empty"
    elif ref_norm in resp_norm or resp_norm in ref_norm:
        score = 1.0
        method = "exact_substring"
    elif len(ref_norm.split()) <= 3 and _normalize(ref_norm) == _normalize(resp_norm):
        score = 1.0
        method = "normalized_exact"
    else:
        ratio = SequenceMatcher(None, ref_norm, resp_norm).ratio()
        score = round(ratio, 4)
        method = "sequence_ratio"

    threshold = problem.get("passing_threshold", 0.7)
    passed = score >= threshold

    return {
        "id": problem["id"],
        "score": score,
        "passed": passed,
        "threshold": threshold,
        "method": method,
        "reference_answer": ref,
        "model_response_preview": response[:300],
    }
