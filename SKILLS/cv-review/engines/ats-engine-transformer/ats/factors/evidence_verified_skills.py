"""Section 6.4 — Evidence-verified skills (Ashby/iCIMS explicit factor).

Research: "skills inside experience bullets with measurable outcomes >
unaudited skills lists". A skill claimed in the Skills section only scores
partial; the same skill demonstrated in an experience bullet with a number
scores full.

API:
    skill_evidence(skill, parsed_resume) -> {location, quantified}
    evidence_verified_factor(parsed_resume, jd_skills) -> FactorResult
"""
from __future__ import annotations

import re

from ..models import FactorResult, ParsedResume

_NUMBER_RE = re.compile(r"\d+%|\$\d|\b\d{2,}\b|\b\d+\.\d+\b|\b\d+x\b")


def bullet_is_quantified(bullet: str) -> bool:
    return bool(_NUMBER_RE.search(bullet))


def skill_evidence(parsed_resume: ParsedResume, skill: str) -> tuple[str, bool]:
    """(location, quantified) for one skill. location in
    {'experience_bullets','skills_section','summary','nowhere'}"""
    skill_l = skill.lower()
    for experience in parsed_resume.experiences:
        for bullet in experience.bullets:
            if skill_l in bullet.lower():
                return "experience_bullets", bullet_is_quantified(bullet)
    body = parsed_resume.sections.get("skills", "").lower()
    if skill_l in body:
        return "skills_section", False
    summary = parsed_resume.sections.get("summary", "").lower()
    if skill_l in summary:
        return "summary", False
    return "nowhere", False


def evidence_verified_factor(
    parsed_resume: ParsedResume, jd_skills: set[str], weight: float = 2.0
) -> FactorResult:
    """Mean quality of evidence across JD skills present in the resume."""
    if not jd_skills:
        return FactorResult("evidence_verified_skills", 0.0, weight, detail="no JD skills")

    values = {"experience_bullets": 1.0, "summary": 0.7, "skills_section": 0.4, "nowhere": 0.0}
    quality_scores: dict[str, float] = {}
    for skill in jd_skills:
        location, quantified = skill_evidence(parsed_resume, skill)
        base = values_at(location)
        bonus = 0.15 if quantified else 0.0
        quality_scores[skill] = min(1.0, base + bonus)
    score = sum(quality_scores.values()) / len(quality_scores)
    demonstrated = [s for s, q in quality_scores.items() if q >= 0.7]
    listed_only = [s for s, q in quality_scores.items() if 0 < q < 0.7]
    return FactorResult(
        name="evidence_verified_skills", score=round(score, 4), weight=weight,
        evidence={"demonstrated": demonstrated, "listed_only": listed_only},
        detail=f"{len(demonstrated)} demonstrated in bullets, {len(listed_only)} listed only "
               "(Ashby/iCIMS: demonstrated skills score higher)",
    )


def values_at(location: str) -> float:
    return {"experience_bullets": 1.0, "summary": 0.7, "skills_section": 0.4, "nowhere": 0.0}[location]


if __name__ == "__main__":
    resume = ParsedResume(
        sections={"skills": "python, sql, kubernetes"},
        experiences=[type("E", (), {"title": "Engineer", "bullets": ["Cut latency 40% with python and docker"]})()],
    )
    print(evidence_verified_factor(resume, {"python", "sql", "kubernetes"}).detail)
