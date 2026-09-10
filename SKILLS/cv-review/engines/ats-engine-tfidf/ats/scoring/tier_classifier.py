"""Section 5 — Greenhouse 5-tier classification.

Research: "Strong / Good / Partial / Limited / Needs manual review. Recruiter
calibration: 4-6 core skills with weight sliders."

API:
    classify_tier(score_0_1) -> str
    greenhouse_tiers() -> list[str]
"""
from __future__ import annotations

TIERS = ["Strong", "Good", "Partial", "Limited", "Needs manual review"]

_THRESHOLDS = [(0.8, "Strong"), (0.6, "Good"), (0.4, "Partial"), (0.2, "Limited")]


def classify_tier(score: float) -> str:
    """Map composite 0..1 score to a Greenhouse-style tier."""
    for threshold, tier in _THRESHOLDS:
        if score >= threshold:
            return tier
    return "Needs manual review"


def greenhouse_tiers() -> list[str]:
    return list(TIERS)


def classify_with_calibrated_skills(
    score: float, core_skills_hit: int, core_skills_total: int = 5, min_core: int = 4
) -> str:
    """Tier with recruiter calibration: even a high score drops a tier if fewer
    than min_core of core skills hit."""
    tier = classify_tier(score)
    if tier == "Strong" and core_skills_total and core_skills_hit < min_core:
        return "Good"
    return tier


if __name__ == "__main__":
    for s in [0.9, 0.7, 0.5, 0.3, 0.1]:
        print(s, "->", classify_tier(s))
    print(classify_with_calibrated_skills(0.9, 3, 5))
