"""Section 4 — Co-attention similarity (APJFNN / PJFCANN-inspired).

Academic person-job fit models (APJFNN, PJFCANN) use co-attention neural
networks: the JD attends over CV tokens and vice-versa, and the pooled
alignment decides the match. This is a deterministic single-head
co-attention approximation:

  1. extract weighted content terms from each side (tf-weighted)
  2. build the alignment matrix via stem/fuzzy token similarity
  3. softmax-attend (temperature-scaled) over the alignment row
  4. pool both directions: 0.6 * JD->CV + 0.4 * CV->JD

API:
    co_attention_similarity(jd_text, resume_text, temperature=0.2) -> float
    attention_matrix(jd_text, resume_text) -> alignment matrix (explainability)
    co_attention_match(jd_text, resume_text) -> MatchResult
"""
from __future__ import annotations

import math
import re
from collections import Counter

from ..models import MatchResult
from .fuzzy_match import levenshtein
from .stemmer import stems_related

_WORD_RE = re.compile(r"[a-z][a-z+#.-]{2,}")
_STOP = {
    "and", "or", "the", "a", "an", "to", "of", "in", "for", "with", "on", "at",
    "is", "are", "be", "you", "your", "we", "our", "will", "as", "by", "that",
    "this", "it", "from", "have", "has", "not", "but", "they", "their",
}


def weighted_terms(text: str, max_terms: int = 60) -> dict[str, float]:
    """Content terms weighted by term frequency (range 1..~2.9)."""
    counts = Counter(_WORD_RE.findall(text.lower()))
    if not counts:
        return {}
    max_count = max(counts.values())
    terms = {
        term: 1.0 + (1.9 * count / max_count)
        for term, count in counts.items()
        if term not in _STOP
    }
    return dict(sorted(terms.items(), key=lambda kv: -kv[1])[:max_terms])


def token_sim(a: str, b: str) -> float:
    """Alignment score between two tokens (stem/fuzzy aware)."""
    if a == b:
        return 1.0
    if stems_related(a, b):
        return 0.95
    if len(a) >= 5 and len(b) >= 5 and levenshtein(a, b) <= 1:
        return 0.7
    return 0.0


def attention_direction(
    source_terms: dict[str, float], target_terms: list[str], temperature: float
) -> float:
    """Each source term aligns to its best target token; softmax over the
    alignment similarities pools the score (term weights scale the softmax)."""
    if not source_terms or not target_terms:
        return 0.0
    sims: list[float] = []
    weights: list[float] = []
    for term, weight in source_terms.items():
        best = 0.0
        for other in target_terms:
            sim = token_sim(term, other)
            if sim > best:
                best = sim
        sims.append(best)
        weights.append(weight)

    max_sim = max(sims)
    exponentials = [math.exp((s - max_sim) / max(temperature, 1e-6) + w) for s, w in zip(sims, weights)]
    total = sum(exponentials)
    attention = [e / total for e in exponentials]
    return sum(a * s for a, s in zip(attention, sims))


def co_attention_similarity(jd_text: str, resume_text: str, temperature: float = 0.2) -> float:
    """Symmetric co-attention similarity in 0..1."""
    jd = weighted_terms(jd_text)
    resume = weighted_terms(resume_text)
    if not jd or not resume:
        return 0.0
    resume_list = list(resume)
    jd_list = list(jd)
    forward = attention_direction(jd, resume_list, temperature)
    backward = attention_direction(resume, jd_list, temperature)
    return round(0.6 * forward + 0.4 * backward, 4)


def attention_matrix(jd_text: str, resume_text: str, limit: int = 20) -> dict[str, dict[str, float]]:
    """Raw alignment matrix (JD term x resume term) for explainability."""
    jd = list(weighted_terms(jd_text))[:limit]
    resume = list(weighted_terms(resume_text))[:limit]
    return {j: {r: token_sim(j, r) for r in resume if token_sim(j, r) > 0} for j in jd}


def co_attention_match(jd_text: str, resume_text: str) -> MatchResult:
    return MatchResult(
        technique="co_attention",
        score=co_attention_similarity(jd_text, resume_text),
        notes="simplified co-attention alignment (APJFNN/PJFCANN-inspired)",
    )


if __name__ == "__main__":
    a = "We need a senior backend engineer with Python, Docker and Kubernetes"
    b = "Senior engineer building Python services on kubernetes and docker at scale"
    c = "Hospital seeking registered nurses for night shifts"
    print("related:", co_attention_similarity(a, b))
    print("unrelated:", co_attention_similarity(a, c))
