"""Section 6.14/7 — Talent rediscovery & CRM scoring (silver medalists).

Research: "surfacing past applicants / 'silver medalists' (Workday claims ~70%
of reqs can be filled this way)" and section 7 "past applicants scored against
new reqs".

API:
    rediscover(pool: list[CandidateRecord], jd, analyze_fn) -> list[RankedCandidate]
    silver_medalists(ranked, previous_stages=("offer", "final_round")) -> list
"""
from __future__ import annotations

from ..models import CandidateRecord, JobDescription, RankedCandidate


def silver_medalists(candidates: list[CandidateRecord],
                     previous_stages: tuple[str, ...] = ("offer", "final_round", "onsite")) -> list[CandidateRecord]:
    """Past applicants who got close but weren't hired."""
    return [
        candidate for candidate in candidates
        if str(candidate.meta.get("previous_stage", "")).lower() in previous_stages
    ]


def rediscover(
    pool: list[CandidateRecord],
    jd: JobDescription,
    analyze_fn,
) -> list[RankedCandidate]:
    """Re-score past applicants against a new req using any analyze_fn.

    analyze_fn(candidate_record, jd) -> AnalysisReport-like object with
    .scores (ScoreResult) and .route. Mirrors Workday's claim that ~70% of
    reqs can be filled from rediscovered candidates.
    """
    ranked: list[RankedCandidate] = []
    for candidate in pool:
        report = analyze_fn(candidate, jd)
        ranked.append(
            RankedCandidate(
                rank=0,
                candidate=candidate,
                score=report.scores,
                route=report.route,
                top_evidence=[str(f.detail) for f in report.factors[:3]],
            )
        )
    ranked.sort(key=lambda r: (-r.score.percentage, r.candidate.candidate_id))
    for index, entry in enumerate(ranked, start=1):
        entry.rank = index
    return ranked


if __name__ == "__main__":
    pool = [
        CandidateRecord("c1", "Ann", meta={"previous_stage": "offer"}),
        CandidateRecord("c2", "Bob", meta={"previous_stage": "phone_screen"}),
    ]
    print([c.name for c in silver_medalists(pool)])
