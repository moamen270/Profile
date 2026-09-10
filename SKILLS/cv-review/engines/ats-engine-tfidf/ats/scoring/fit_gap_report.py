"""Section 5 — Lever-style narrative output (no score; badge + strengths/clarifications).

Research: "Lever: No score. Green 'TALENT FIT' badge + Strengths /
Areas-for-Clarification narrative."

API:
    fit_badge(criteria) -> str           # "TALENT FIT" | "NO BADGE"
    fit_narrative(factors, criteria) -> dict  # {badge, strengths, areas_for_clarification}
"""
from __future__ import annotations

from ..models import CriterionResult, FactorResult

_BADGE_THRESHOLD = 0.65


def fit_badge(factors: list[FactorResult], threshold: float = _BADGE_THRESHOLD) -> str:
    if not factors:
        return ""
    avg = sum(f.score * f.weight for f in factors) / sum(f.weight for f in factors)
    return "TALENT FIT" if avg >= threshold else "NO BADGE"


def fit_narrative(
    factors: list[FactorResult], criteria: list[CriterionResult] | None = None
) -> dict:
    """Strengths = top factors; Areas-for-Clarification = unmet/undecided criteria."""
    strengths = [
        f"{f.name} ({f.score:.0%})" for f in sorted(factors, key=lambda f: -f.score)[:3] if f.score >= 0.5
    ]
    areas: list[str] = []
    for result in criteria or []:
        if result.status != "met":
            areas.append(f"{result.qualification.text} — {result.status.replace('_', ' ')}")
    for factor in factors:
        if factor.score < 0.4:
            areas.append(f"low {factor.name}: {factor.detail}")
    return {
        "badge": fit_badge(factors),
        "strengths": strengths,
        "areas_for_clarification": areas[:5],
        "note": "Lever shows no numeric score — narrative only, human decides",
    }


if __name__ == "__main__":
    from ..models import CriterionResult as _CR
    from ..models import Qualification

    factors = [FactorResult("skill_overlap", 0.8, 3.0), FactorResult("years_experience", 0.4, 2.0)]
    criteria = [_CR(Qualification("AWS"), "undecided")]
    print(fit_narrative(factors, criteria))
