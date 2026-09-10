"""Section 6.8 — Industry alignment.

API:
    industry_alignment_factor(resume_text, jd, weight) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult, JobDescription
from ..parsing.industry import detect_industry


def industry_alignment_factor(resume_text: str, jd: JobDescription, weight: float = 0.5) -> FactorResult:
    resume_industry = detect_industry(resume_text)
    if not jd.industry:
        return FactorResult("industry_alignment", 1.0, weight, detail="JD has no detectable industry")
    if resume_industry == jd.industry:
        return FactorResult(
            "industry_alignment", 1.0, weight,
            evidence={"resume_industry": resume_industry, "jd_industry": jd.industry},
            detail=f"industry match: {resume_industry}",
        )
    if resume_industry:
        return FactorResult(
            "industry_alignment", 0.5, weight,
            evidence={"resume_industry": resume_industry, "jd_industry": jd.industry},
            detail=f"resume: {resume_industry}, JD: {jd.industry}",
        )
    return FactorResult("industry_alignment", 0.4, weight, detail="resume industry undetectable")


if __name__ == "__main__":
    jd = JobDescription(raw_text="fintech payments startup", industry="fintech")
    print(industry_alignment_factor("Built ledger systems at a payments startup", jd).detail)
