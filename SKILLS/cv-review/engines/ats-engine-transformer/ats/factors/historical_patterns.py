"""Section 6.13 — Historical success patterns (Eightfold/iCIMS).

Research: "Multiple models trained on 100M+ historical applications, learning
what successful hires looked like" / "validated against post-hire retention".

Requires hire-outcome data. This module implements a simple outcome-trained
lookup: similarity of the candidate's skill set to past successful hires
(Jaccard over skills), with graceful absence handling.

API:
    success_pattern_score(skills, hired_history) -> FactorResult | None
        hired_history: [{"skills": [...], "outcome": "hired"|"left"}]
"""
from __future__ import annotations

from ..models import FactorResult


def success_pattern_score(
    candidate_skills: set[str],
    hired_history: list[dict] | None,
    weight: float = 0.3,
) -> FactorResult | None:
    """Mean Jaccard similarity vs past hired candidates. None => no history data."""
    if not hired_history:
        return None
    candidate = {s.lower() for s in candidate_skills}
    scores = []
    for record in hired_history:
        hired_skills = {s.lower() for s in record.get("skills", [])}
        if candidate or hired_skills:
            union = candidate | hired_skills
            jaccard = len(candidate & hired_skills) / len(union) if union else 0.0
        else:
            jaccard = 0.0
        outcome_multiplier = 1.0 if record.get("outcome", "hired") == "hired" else 0.5
        scores.append(jaccard * outcome_multiplier)
    overall = sum(scores) / len(scores) if scores else 0.0
    return FactorResult(
        name="historical_success_patterns", score=round(min(1.0, overall * 2), 4), weight=weight,
        evidence={"n_hired_records": len(hired_history)},
        detail=f"similarity to {len(hired_history)} historical hired candidates (Eightfold/iCIMS style)",
    )


if __name__ == "__main__":
    history = [
        {"skills": ["python", "sql", "docker", "aws"], "outcome": "hired"},
        {"skills": ["python", "kubernetes", "go"], "outcome": "hired"},
        {"skills": ["python", "sql"], "outcome": "left"},
    ]
    print(success_pattern_score({"python", "sql", "docker"}, history).score)
