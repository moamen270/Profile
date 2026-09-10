"""Section 4 — Semantic relationship clusters (Workday HiredScore style).

Research: "Related-concept clusters ('stakeholder alignment' + 'delivery
optimization') score higher than one keyword repeated." A cluster needs 2+
member skills for full credit; a single member earns partial credit.

API:
    cluster_overlap(resume_skills, jd_skills, taxonomy) -> MatchResult
"""
from __future__ import annotations

from ..models import MatchResult
from ..normalization.taxonomy import SkillsTaxonomy

_FULL_CREDIT = 1.0
_PARTIAL_CREDIT = 0.5


def cluster_overlap(
    resume_skills: set[str],
    jd_skills: set[str],
    taxonomy: SkillsTaxonomy | None = None,
) -> MatchResult:
    """Score related-concept clusters: 2+ members in both sides = full credit."""
    taxonomy = taxonomy or SkillsTaxonomy()
    resume_norm = {s.lower() for s in resume_skills}
    jd_norm = {s.lower() for s in jd_skills}

    earned = possible = 0.0
    cluster_hits: dict[str, float] = {}
    matched: list[str] = []

    for cluster_name, members in taxonomy.clusters.items():
        members_l = {m.lower() for m in members}
        jd_in = jd_norm & members_l
        if not jd_in:
            continue  # cluster not relevant to this JD
        possible += _FULL_CREDIT
        resume_in = resume_norm & members_l
        if len(resume_in) >= 2:
            earned += _FULL_CREDIT
            cluster_hits[cluster_name] = _FULL_CREDIT
        elif len(resume_in) == 1:
            earned += _PARTIAL_CREDIT
            cluster_hits[cluster_name] = _PARTIAL_CREDIT
        else:
            cluster_hits[cluster_name] = 0.0
        matched.extend(sorted(resume_in))

    score = earned / possible if possible else 0.0
    return MatchResult(
        technique="relationship_clusters", score=round(score, 4),
        matched=sorted(set(matched)),
        evidence=cluster_hits,
        notes="Related-concept clusters (Workday HiredScore semantic relationships)",
    )


if __name__ == "__main__":
    result = cluster_overlap(
        resume_skills={"stakeholder management", "communication", "docker"},
        jd_skills={"stakeholder management", "leadership", "agile"},
    )
    print(result.score, result.evidence)
