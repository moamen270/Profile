"""Section 3/4 — Skills-ontology matching.

Research: "Normalize both CV & JD to taxonomy, compare entities" —
Workday Skills Cloud / Phenom / Eightfold style entity comparison.

API:
    ontology_match(resume_skills, jd_skills, taxonomy) -> MatchResult
"""
from __future__ import annotations

from ..models import MatchResult
from ..normalization.taxonomy import SkillsTaxonomy


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 0.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def ontology_match(
    resume_skills: set[str],
    jd_required: set[str],
    jd_preferred: set[str] | None = None,
    taxonomy: SkillsTaxonomy | None = None,
) -> MatchResult:
    """Normalize both sides to canonical entities, then compare entity sets.

    Required entities weigh 1.0; preferred 0.5. Overlap measured with Jaccard
    on the canonical sets; relationship (inferred-capability) overlap adds up
    to +0.15.
    """
    taxonomy = taxonomy or SkillsTaxonomy()
    jd_preferred = jd_preferred or set()

    resume_entities = taxonomy.normalize_set(resume_skills)
    req_entities = taxonomy.normalize_set(jd_required)
    pref_entities = taxonomy.normalize_set(jd_preferred)

    required_hit = req_entities & resume_entities
    preferred_hit = pref_entities & resume_entities

    required_score = (len(required_hit) / len(req_entities)) if req_entities else 1.0
    preferred_score = (len(preferred_hit) / len(pref_entities)) if pref_entities else 0.0

    base = 0.8 * required_score + 0.2 * preferred_score if (req_entities or pref_entities) else 0.0

    # relationship bonus
    from ..normalization.relationship_inference import infer_relationships

    jd_caps = infer_relationships(req_entities | pref_entities, taxonomy)
    resume_caps = infer_relationships(resume_entities, taxonomy)
    common_caps = set(jd_caps) & set(resume_caps)

    score = min(1.0, base + caps_bonus(len(common_caps)))
    return MatchResult(
        technique="ontology", score=score,
        matched=sorted(required_hit | preferred_hit),
        missing=sorted(req_entities - resume_entities),
        evidence={
            "required_hit": sorted(required_hit),
            "preferred_hit": sorted(preferred_hit),
            "inferred_capabilities": sorted(common_caps),
        },
        notes="Canonical entity comparison over skills taxonomy (Workday/Phenom)",
    )


def caps_bonus(common_caps: int) -> float:
    return min(0.15, 0.05 * common_caps)


if __name__ == "__main__":
    result = ontology_match(
        resume_skills={"ReactJS", "k8s", "docker"},
        jd_required={"react", "kubernetes"},
        jd_preferred={"aws"},
    )
    print(result.score, result.matched, result.missing)
