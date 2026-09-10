"""Section 6.11 — Competency self-ratings (Taleo proficiency model).

Research: Taleo scores "proficiency (None->Expert) x years x last used x interest".
Data comes from candidate self-ratings in the application form, not the CV.

API:
    competency_score(rating) -> FactorResult        # rating dict from form data
    competency_factor_from_answers(answers) -> FactorResult | None
"""
from __future__ import annotations

from ..models import FactorResult

PROFICIENCY_LEVELS = {"none": 0.0, "beginner": 0.25, "intermediate": 0.5, "advanced": 0.75, "expert": 1.0}
RECENCY_DECAY = {"<1 year": 1.0, "1-2 years": 0.8, "3-5 years": 0.5, "5+ years": 0.3}


def competency_score(rating: dict) -> float:
    """rating: {skill, proficiency, years, last_used, interest} all optional."""
    proficiency = PROFICIENCY_LEVELS.get(str(rating.get("proficiency", "")).lower(), 0.5)
    years = _safe_float(rating.get("years"), default=1.0)
    years_component = min(1.0, years / 5.0)
    recency = RECENCY_DECAY.get(str(rating.get("last_used", "")).lower(), 0.7)
    interest = _safe_float(rating.get("interest"), default=0.7)
    interest_component = max(0.0, min(1.0, interest))
    return 0.4 * proficiency + 0.3 * years_component + 0.2 * recency + 0.1 * interest_component


def competency_factor_from_answers(ratings: list[dict] | None, weight: float = 0.5) -> FactorResult | None:
    """Ratings come from Taleo-style self-assessment forms; None means not collected."""
    if not ratings:
        return None
    scores = [competency_score(r if isinstance(r, dict) else {}) for r in ratings]
    overall = sum(scores) / len(scores)
    return FactorResult(
        name="competency_ratings", score=round(overall_of(scores), 4), weight=weight,
        evidence={"n_ratings": len(scores)},
        detail=f"Taleo model over {len(scores)} self-ratings: proficiency x years x last-used x interest",
    )


def overall_of(scores: list[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def _safe_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


if __name__ == "__main__":
    ratings = [
        {"skill": "python", "proficiency": "expert", "years": 6, "last_used": "<1 year", "interest": 0.9},
        {"skill": "sql", "proficiency": "intermediate", "years": 3, "last_used": "1-2 years"},
    ]
    print(competency_factor_from_answers(ratings).score)
