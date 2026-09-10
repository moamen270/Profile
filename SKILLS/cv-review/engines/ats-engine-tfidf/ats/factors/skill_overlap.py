"""Section 6.1 — Skill overlap with JD (normalized, unique concepts).

API:
    skill_overlap_factor(resume_skills, jd_skills) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult


def skill_overlap_factor(
    resume_skills: set[str],
    jd_required: set[str],
    jd_preferred: set[str] | None = None,
    weight: float = 3.0,
) -> FactorResult:
    """Required skills weigh 1.0 each; preferred 0.4. Unique concepts only."""
    jd_preferred = jd_preferred or set()
    resume_norm = {s.lower() for s in resume_skills}
    req_norm = {s.lower() for s in jd_required}
    pref_norm = {s.lower() for s in jd_preferred}

    req_hit = req_norm & resume_norm
    pref_hit = pref_norm & resume_norm

    possible = len(req_norm) + 0.4 * len(pref_norm)
    earned = len(req_hit) + 0.4 * len(pref_hit)
    score = earned / possible if possible else 0.0
    return FactorResult(
        name="skill_overlap", score=round(score, 4), weight=weight,
        evidence={
            "required_hit": sorted(req_hit),
            "required_missing": sorted(req_norm - resume_norm),
            "preferred_hit": sorted(pref_hit),
        },
        detail=f"{len(req_hit)}/{len(req_norm)} required, {len(pref_hit)}/{len(pref_norm)} preferred skills",
    )


if __name__ == "__main__":
    result = skill_overlap_factor(
        resume_skills={"python", "sql", "docker"},
        jd_required={"python", "sql", "kubernetes"},
        jd_preferred={"kafka"},
    )
    print(result.score, result.detail)
