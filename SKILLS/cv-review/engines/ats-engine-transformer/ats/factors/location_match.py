"""Section 6.7 — Location match (distance / work authorization).

API:
    location_match_factor(parsed_resume, jd) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult, JobDescription, ParsedResume


def _norm(s: str | None) -> str:
    return " ".join((s or "").lower().split())


def location_match_factor(
    parsed_resume: ParsedResume, jd: JobDescription, weight: float = 1.0
) -> FactorResult:
    if jd.remote_allowed:
        return FactorResult("location_match", 1.0, weight, detail="remote allowed")
    if not jd.location:
        return FactorResult("location_match", 1.0, weight, detail="no location in JD")

    candidate_loc = parsed_resume.contact.location or ""
    cand_city = candidate_loc.split(",")[0].strip().lower()
    jd_loc = jd.location.lower()
    if cand_city and (cand_city in jd_loc or jd_loc in candidate_loc.lower()):
        score, detail = 1.0, f"location match: {candidate_loc} ~ {jd.location}"
    elif candidate_loc:
        # same-state heuristic ("austin, tx" vs "tx")
        cand_state = candidate_loc.split(",")[-1].strip().lower()
        jd_state = jd.location.split(",")[-1].strip().lower()
        if cand_state and cand_state == jd_state:
            score, detail = 0.7, f"same state/region: {cand_state}"
        else:
            score, detail = 0.3, f"relocation likely needed: {candidate_loc} vs {jd.location}"
    else:
        score, detail = 0.5, "candidate location unknown"
    return FactorResult("location_match", score, weight, detail=detail)


if __name__ == "__main__":
    resume = ParsedResume(contact=type("C", (), {"location": "Dallas, TX"})())
    jd = JobDescription(location="Austin, TX", remote_allowed=False)
    print(location_match_factor(resume, jd).detail)
