"""Section 5 — Oracle Recruiting Cloud 0-3 stars across 4 dimensions.

Research: "0-3 stars, 4 dimensions: Profile, Education, Experience, Skills
(Intelligent Matching)."

API:
    stars_for(score_0_1) -> int              # 0..3
    oracle_stars(factor_scores: dict) -> dict  # dimension -> stars
"""
from __future__ import annotations

DIMENSIONS = ["Profile", "Education", "Experience", "Skills"]


def stars_for(score: float) -> int:
    if score >= 0.85:
        return 3
    if score >= 0.6:
        return 2
    if score >= 0.35:
        return 1
    return 0


def oracle_stars(factor_scores: dict[str, float]) -> dict[str, int]:
    """Map factor scores to the 4 Oracle dimensions.

    factor_scores keys (any of): profile|overall, education|education_match,
    experience|years_experience, skills|skill_overlap. Missing -> 0 stars.
    """
    profile = factor_scores.get("profile") or factor_scores.get("overall") or 0.0
    education = factor_scores.get("education") or factor_scores.get("education_match") or 0.0
    experience = factor_scores.get("experience") or factor_scores.get("years_experience") or 0.0
    skills = factor_scores.get("skills") or factor_scores.get("skill_overlap") or 0.0
    return {
        "Profile": stars_for(float(profile)),
        "Education": stars_for(float(education)),
        "Experience": stars_for(float(experience)),
        "Skills": stars_for(float(skills)),
    }


if __name__ == "__main__":
    print(oracle_stars({"skill_overlap": 0.9, "education_match": 0.7, "years_experience": 0.65, "profile": 0.8}))
