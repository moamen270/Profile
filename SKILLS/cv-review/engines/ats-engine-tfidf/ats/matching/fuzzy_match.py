"""Section 4 — Fuzzy matching (Levenshtein distance <= 2).

Used by most parsers for typos and spelling variants. Pure Python — no
external dependency required.

API:
    levenshtein(a, b) -> int
    fuzzy_hits(term, text, max_distance=2) -> [(token, distance)]
    fuzzy_score(required_terms, text, max_distance=2) -> MatchResult
"""
from __future__ import annotations

import re

from ..models import MatchResult

_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z+#./-]*")


def levenshtein(a: str, b: str) -> int:
    """Iterative DP Levenshtein distance."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            insert_cost = current[j - 1] + 1
            delete_cost = previous[j] + 1
            substitute_cost = previous[j - 1] + (ca != cb)
            current.append(min(insert_cost, delete_cost, substitute_cost))
        previous = current
    return previous[-1]


def fuzzy_hits(term: str, text: str, max_distance: int = 2) -> list[tuple[str, int]]:
    """Tokens within max_distance of the term."""
    term_l = str(term).lower()
    if len(term_l) <= max_distance:
        max_distance = max(1, len(term_l) - 1)
    hits = []
    for token in set(re.findall(r"[a-z0-9+#./-]+", text.lower())):
        distance = levenshtein(term_l, token)
        if distance <= max_distance and distance > 0:
            hits.append((token, distance))
    return sorted(hits, key=lambda pair: pair[1])


def fuzzy_match(term: str, text: str, max_distance: int = 2) -> bool:
    """True if term (or its exact form) appears within distance."""
    if re.search(rf"(?<!\w){re.escape(str(term).lower())}(?!\w)", text.lower()):
        return True
    return bool(fuzzy_hits(term, text, max_distance))


def fuzzy_score(required_terms, text: str, max_distance: int = 2) -> MatchResult:
    matched, missing = [], []
    evidence = {}
    for term in required_terms:
        term_s = str(term)
        if fuzzy_match(term_s, text, max_distance):
            hits = fuzzy_hits(term_s, text, max_distance)
            matched.append(term_s)
            evidence[term_s] = hits[:3]
        else:
            missing.append(term_s)
    total = len(matched) + len(missing)
    return MatchResult(
        technique="fuzzy", score=len(matched) / total if total else 0.0,
        matched=matched, missing=missing, evidence=evidence,
        notes=f"Levenshtein distance <= {max_distance} for typos/variants",
    )


if __name__ == "__main__":
    result = fuzzy_score(["javascript", "kubernetes"], "experienced with Javsacript and Kuberntes clusters")
    print(result.score, result.matched)
    print(result.evidence)
    print(levenshtein("kitten", "sitting"))
