"""Section 6.5 — Education level & field match.

API:
    education_match_factor(parsed_resume, jd) -> FactorResult
"""
from __future__ import annotations

from ..models import Education, FactorResult, JobDescription, ParsedResume

_LEVEL_RANK = {"diploma": 1, "associate": 2, "bachelor": 3, "master": 4, "phd": 5}


def highest_degree(education: list[Education]) -> str | None:
    ranks = [(_LEVEL_RANK.get(ed.degree, 0), ed.degree) for ed in education if ed.degree]
    return max(ranks)[1] if ranks else None


def education_match_factor(
    parsed_resume: ParsedResume, jd: JobDescription, weight: float = 1.0
) -> FactorResult:
    if not jd.education_level:
        return FactorResult("education_match", 1.0, weight, detail="no education requirement in JD")

    resume_rank = _LEVEL_RANK.get(highest_degree(parsed_resume.education) or "", 0)
    required_rank = _LEVEL_RANK.get(jd.education_level, 3)

    if resume_rank >= required_rank:
        score = 1.0
        detail = f"education {'>=' if resume_rank > required_rank else '=='} requirement ({jd.education_level})"
    elif resume_rank > 0:
        score = max(0.0, 0.4 - 0.1 * (required_rank - resume_rank - 1))
        detail = f"education below requirement: have {highest_degree(parsed_resume.education)}, need {jd.education_level}"
    else:
        score = 0.0
        detail = "no recognizable degree in resume"

    # field match (soft +0.0/-0.2): only penalize a clearly different stated field
    if jd.education_field and parsed_resume.education:
        fields = {(_f(ed.field) or "").lower() for ed in parsed_resume.education}
        jd_field = jd.education_field.lower()
        if fields and jd_field not in fields and not any(jd_field in f or f in jd_field for f in fields if f):
            score = max(0.0, score - 0.2)
            detail += "; field mismatch"
    return FactorResult(
        name="education_match", score=round(score, 4), weight=weight,
        evidence={"required": jd.education_level, "field": jd.education_field},
        detail=detail,
    )


def _f(field):
    return field


if __name__ == "__main__":
    resume = ParsedResume(education=[Education(degree="bachelor", field="Computer Science")])
    jd = JobDescription(education_level="bachelor", education_field="Computer Science")
    print(education_match_factor(resume, jd).detail)
    jd2 = JobDescription(education_level="master")
    print(education_match_factor(resume, jd2).detail)
