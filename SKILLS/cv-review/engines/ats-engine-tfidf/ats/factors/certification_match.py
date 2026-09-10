"""Section 6.6 — Certifications / licenses match (acronym OR full form counts).

API:
    certification_match_factor(parsed_resume, jd_text_or_certs) -> FactorResult
"""
from __future__ import annotations

import re

from ..models import FactorResult, ParsedResume
from ..parsing.certifications_extractor import extract_certifications

from ..parsing.certifications_extractor import CERT_FULL_NAMES


def resume_cert_acronyms(parsed_resume: ParsedResume) -> set[str]:
    acronyms = {cert.acronym for cert in parsed_resume.certifications if cert.acronym}
    text = parsed_resume.raw_text
    if text:
        for cert in extract_certifications(text):
            if cert.acronym:
                acronyms.add(cert.acronym)
    return acronyms


def required_certs(text: str) -> set[str]:
    """JD-side required certifications (acronyms only)."""
    return {c.acronym for c in extract_certifications(text) if c.acronym}


def certification_match_factor(
    parsed_resume: ParsedResume, jd_cert_text: str, weight: float = 1.0
) -> FactorResult:
    """score = matched / required (1.0 when JD requires none)."""
    required = required_certs(jd_cert_text)
    if not required:
        return FactorResult("certification_match", 1.0, weight, detail="no certifications required")
    have = resume_cert_acronyms(parsed_resume)
    matched = required & have
    score = len(matched) / len(required)
    return FactorResult(
        name="certification_match", score=round(score, 4), weight=weight,
        evidence={"required": sorted(required), "matched": sorted(matched),
                  "missing": sorted(required - have)},
        detail=f"{len(matched)}/{len(required)} required certs (acronym or full form accepted)",
    )


if __name__ == "__main__":
    resume = ParsedResume(raw_text="Credentials: PMP, Certified Public Accountant")
    jd_text = "Must hold PMP certification. CPA a plus."
    print(certification_match_factor(resume, jd_text).detail)
