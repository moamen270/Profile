"""Section 4 — Weighted keyword scoring (Taleo ACE style).

Research: "Required keywords weighted 3-10x vs preferred; score =
sum(weighted matches) / sum(weights)". Words under Requirements/Qualifications
headings get the required weight; preferred sections a lighter one.

API:
    extract_keywords(jd_text, required_weight=5.0, preferred_weight=3.0,
                     top_n=40) -> dict[term, weight]
    weighted_score(keywords, resume_text) -> MatchResult
"""
from __future__ import annotations

import re

from ..models import MatchResult

_STOPWORDS = {
    "and", "or", "the", "a", "an", "to", "of", "in", "for", "with", "on", "at",
    "is", "are", "be", "you", "your", "we", "our", "will", "as", "by", "that",
    "this", "it", "from", "have", "has", "not", "but", "they", "their",
}

_WORD_RE = re.compile(r"[a-z][a-z+#.-]{2,}")
_REQUIRE_HINTS = ["requirement", "qualification", "must have", "must-have", "required"]
_PREFERRED_HINTS = ["preferred", "nice to have", "nice-to-have", "bonus", "plus"]


def extract_keywords(
    jd_text: str, required_weight: float = 5.0, preferred_weight: float = 3.0, top_n: int = 40
) -> dict[str, float]:
    """Term-frequency keywords; words under Requirements get the required weight,
    bigrams get +2, words under preferred sections get the preferred weight."""
    lines = jd_text.splitlines()
    in_required = in_preferred = False
    weights: dict[str, float] = {}

    for line in lines:
        cleaned = line.strip().lower().rstrip(":")
        if any(h in cleaned for h in _REQUIRE_HINTS) and len(cleaned) < 45:
            in_required, in_preferred = True, False
            continue
        if any(h in cleaned for h in _PREFERRED_HINTS) and len(cleaned) < 45:
            in_preferred, in_required = True, False
            continue

        weight = required_weight if in_required else preferred_weight if in_preferred else 1.0
        tokens = [t for t in _WORD_RE.findall(cleaned) if t not in _STOPWORDS]
        for token in tokens:
            weights[token] = weights.get(token, 0.0) + weight
        for first, second in zip(tokens, tokens[1:]):
            bigram = f"{first} {second}"
            weights[bigram] = weights.get(bigram, 0.0) + weight + 2.0

    ranked = sorted(weights.items(), key=lambda kv: -kv[1])[:top_n]
    return dict(ranked)


def weighted_score(keywords: dict[str, float], resume_text: str) -> MatchResult:
    """Blended score: unigram hits weighted by weight (80%), bigram coverage (20%).
    Keys containing a space are treated as bigrams."""
    resume_lower = resume_text.lower()
    uni_earned = uni_possible = 0.0
    bi_earned = bi_possible = 0.0
    matched, missing = [], []
    for term, weight in keywords.items():
        hit = re.search(rf"(?<!\w){re.escape(term)}(?!\w)", resume_lower) is not None
        if " " in term:
            bi_possible += weight
            bi_earned += weight if hit else 0.0
        else:
            uni_possible += weight
            uni_earned += weight if hit else 0.0
        (matched if hit else missing).append(term)
    uni_ratio = uni_earned / uni_possible if uni_possible else 0.0
    bi_ratio = bi_earned / bi_possible if bi_possible else 0.0
    score = min(1.0, 0.8 * uni_ratio + 0.2 * bi_ratio)
    return MatchResult(
        technique="weighted_keywords", score=score, matched=matched, missing=missing,
        evidence={"unigram_coverage": uni_ratio, "bigram_coverage": bi_ratio},
        notes=f"Taleo ACE style: required terms weighted x{required_weight_note(keywords)}",
    )


def required_weight_note(keywords: dict[str, float]) -> str:
    max_w = max(keywords.values(), default=0)
    return str(int(max_w)) if max_w and max_w == int(max_w) else str(max_w)


if __name__ == "__main__":
    jd = """
Requirements:
- Strong Python and SQL skills
- Docker and Kubernetes experience

Nice to have:
- Kafka, Terraform
"""
    kw = extract_keywords(jd)
    print(dict(list(kw.items())[:8]))
    print(weighted_score(kw, "I know Python, SQL and Docker very well.").score)
