"""Section 4 — Exact / literal string matching.

"project manager" != "project management". This is legacy Taleo behavior —
the most automated, least intelligent end of the spectrum.

API:
    exact_match(term, text, word_boundary=True) -> bool
    exact_score(required_terms, text) -> MatchResult
"""
from __future__ import annotations

import re

from ..models import MatchResult


def exact_match(term: str, text: str, word_boundary: bool = True) -> bool:
    term_l = str(term).strip().lower()
    text_l = text.lower()
    if not term_l:
        return False
    if word_boundary:
        return re.search(rf"(?<!\w){re.escape(term_l)}(?!\w)", text_l) is not None
    return term_l in text_l


def exact_score(required_terms, text: str, word_boundary: bool = True) -> MatchResult:
    matched, missing = [], []
    for term in required_terms:
        (matched if exact_match(term, text, word_boundary) else missing).append(str(term))
    total = len(matched) + len(missing)
    score = len(matched) / total if total else 0.0
    return MatchResult(
        technique="exact", score=score, matched=matched, missing=missing,
        notes="Literal string match (legacy Taleo behavior)",
    )


if __name__ == "__main__":
    result = exact_score(["project manager", "agile"], "I am an agile project manager.")
    print(result.score, result.matched)
    print(exact_score(["project management"], "I was a project manager.").missing)
