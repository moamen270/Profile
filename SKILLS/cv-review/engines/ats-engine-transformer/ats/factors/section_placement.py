"""Section 6.10 — Section placement weighting (older systems).

Research: "keywords in Skills/Summary score higher than buried in old bullets."

API:
    section_placement_factor(skill_locations, weight) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult

_SECTION_VALUE = {"skills": 1.0, "summary": 0.9, "projects": 0.7, "experience": 0.5}


def placement_value(section: str) -> float:
    return _SECTION_VALUE.get(section.lower(), 0.5)


def best_of(locations: list[str]) -> float:
    return max((placement_value(loc) for loc in locations), default=0.0)


def section_placement_factor(
    skill_locations: dict[str, list[str]], weight: float = 0.5
) -> FactorResult:
    """skill_locations: {skill: [sections where found]}.

    Score = mean over skills of the BEST placement value for that skill.
    """
    if not skill_locations:
        return FactorResult("section_placement", 0.0, weight, detail="no skill locations")

    scores = [best_of(locations) for locations in skill_locations.values()]
    score = sum(scores) / len(scores)
    return FactorResult(
        name="section_placement", score=round(score, 4), weight=weight,
        detail="keywords in Skills/Summary outrank buried mentions (legacy ATS weighting)",
    )


if __name__ == "__main__":
    print(section_placement_factor({"python": ["skills", "experience"], "sql": ["experience"]}).score)
