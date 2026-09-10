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


_NO_CRITERIA_BADGE = "UNSCORED — JD qualifications not parsed"


def fit_narrative(
    factors: list[FactorResult], criteria: list[CriterionResult] | None = None
) -> dict:
    """Strengths = top factors; Areas-for-Clarification = unmet/undecided criteria.

    ``criteria=None`` means qualifications were never evaluated. An *empty
    list* means they were evaluated and the JD yielded nothing — the parse
    failed, so no badge is issued. A real screener would not clear a candidate
    off a job description it could not read; neither should this.
    """
    strengths = [
        f"{f.name} ({f.score:.0%})" for f in sorted(factors, key=lambda f: -f.score)[:3] if f.score >= 0.5
    ]
    areas: list[str] = []
    jd_unparsed = criteria is not None and len(criteria) == 0
    if jd_unparsed:
        areas.append(
            "No qualifications could be parsed from the job description — "
            "the badge and criteria counts are not meaningful for this run."
        )
    for result in criteria or []:
        if result.status != "met":
            areas.append(f"{result.qualification.text} — {result.status.replace('_', ' ')}")
    for factor in factors:
        if factor.score < 0.4:
            areas.append(f"low {factor.name}: {factor.detail}")
    return {
        "badge": _NO_CRITERIA_BADGE if jd_unparsed else fit_badge(factors),
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
