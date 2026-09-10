"""Section 5 — Ensemble score combiner.

Fuses matcher results and factor results into one composite (0..1) plus a
0-100 percentage, mirroring how modern engines blend multiple signals
(iCIMS ensemble ML, Eightfold match prediction).

Default blend (documented, deterministic):
    matchers 55%  (mean of exact/stem/fuzzy/weighted/ontology/embedding/clusters)
    factors  45%  (weighted mean of factor scores)

API:
    combine(matchers, factors) -> (match_composite, factor_composite)
    composite_percentage(match_composite, factor_composite) -> float  # 0..100
"""
from __future__ import annotations

from ..models import FactorResult, MatchResult

_MATCH_WEIGHT = 0.55
_FACTOR_WEIGHT = 0.45


def combine_matchers(matchers: dict[str, MatchResult]) -> float:
    """Mean of available matcher scores (missing matchers ignored)."""
    scores = [m.score for m in matchers.values() if 0.0 <= m.score <= 1.0]
    return sum(scores) / len(scores) if scores else 0.0


def combine_factors(factors: list[FactorResult]) -> float:
    """Weighted mean of factor scores."""
    if not factors:
        return 0.0
    total_weight = sum(f.weight for f in factors)
    if total_weight <= 0:
        return sum(f.score for f in factors) / len(factors)
    return sum(f.score * f.weight for f in factors) / total_weight


def combine(
    matchers: dict[str, MatchResult],
    factors: list[FactorResult],
    stuffing_penalty: float = 0.1,
) -> tuple[float, float]:
    """Returns (match_composite, factor_composite) with optional stuffing penalty.

    A keyword_stuffing matcher result with score > 0 applies the penalty to the
    factor composite (research section 3: repetition triggers spam detection).
    """
    match_composite = combine_matchers(matchers)
    factor_composite = combine_factors(factors)
    if any(m.technique == "keyword_stuffing" and m.score > 0 for m in matchers.values()):
        factor_composite = max(0.0, factor_composite - stuffing_penalty)
    return round(match_composite, 4), round(factor_composite, 4)


def composite_percentage(match_composite: float, factor_composite: float) -> float:
    """Final 0-100 number (the 'Jobscan-style' % the research says real ATS
    don't produce — provided here because consumers expect one)."""
    blended = _MATCH_WEIGHT * match_composite + _FACTOR_WEIGHT * factor_composite
    return round(blended * 100.0, 1)


if __name__ == "__main__":
    matchers = {
        "exact": MatchResult("exact", 0.8),
        "semantic_embedding": MatchResult("semantic_embedding", 0.6),
        "ontology": MatchResult("ontology", 0.7),
    }
    factors = [
        FactorResult("skill_overlap", 0.8, 3.0),
        FactorResult("years_experience", 0.6, 2.0),
        FactorResult("education_match", 1.0, 1.0),
    ]
    match_c, factor_c = combine(matchers, factors)
    print(match_c, factor_c, "->", composite_percentage(match_c, factor_c))
