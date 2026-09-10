"""Section 4 — Word stemming.

Used by Lever: "collaborate / collaborated / collaboration match" without
exact spelling. Light suffix stemmer — no heavyweight NLP dependency.

API:
    stem(word) -> str
    stem_match(term, text) -> bool
    stem_score(required_terms, text) -> MatchResult
"""
from __future__ import annotations

import re

from ..models import MatchResult

_SUFFIXES = [
    "ational", "iveness", "fulness", "ousness", "ization", "ations",
    "itives", "ments", "ement", "ation", "ively", "ities", "ances", "ences",
    "ingly", "ings", "ment", "ness", "ship", "edly", "ies", "ive",
    "ing", "ers", "est", "ity", "ive", "ed", "es", "ly", "er", "s",
]

_WORD_RE = re.compile(r"[a-zA-Z]+")


def stem_word(word: str) -> str:
    word = word.strip().lower()
    for suffix in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


# keep the original public name working
def stem(word: str) -> str:
    return stem_word(word)


def stems_related(a: str, b: str) -> bool:
    sa, sb = stem(a), stem(b)
    if not sa or not sb:
        return False
    if sa == sb:
        return True
    # prefix rule only for substantial stems (>=5 chars) to avoid
    # "japanese" ~ "jane" style false positives
    if len(sa) >= 5 and len(sb) >= 5:
        return sa.startswith(sb) or sb.startswith(sa)
    return False


def stem_tokens(text: str) -> list[str]:
    return [stem(w) for w in _WORD_RE.findall(text)]


def stem_match(term: str, text: str) -> bool:
    tokens = _WORD_RE.findall(text)
    return any(stems_related(term, token) for token in tokens)


def stem_score(required_terms, text: str) -> MatchResult:
    matched, missing = [], []
    for term in required_terms:
        (matched if stem_match(str(term), text) else missing).append(str(term))
    total = len(matched) + len(missing)
    return MatchResult(
        technique="stemming", score=len(matched) / total if total else 0.0,
        matched=matched, missing=missing,
        notes="Suffix stemming (Lever-style: collaborate/collaborated/collaboration)",
    )


if __name__ == "__main__":
    for w in ["collaborate", "collaborated", "collaboration", "managing", "management"]:
        print(w, "->", stem(w))
    print(stem_match("collaborated", "Led and collaboration across teams"))
    print(stem_score(["manage", "lead"], "I manage teams and led projects").score)
