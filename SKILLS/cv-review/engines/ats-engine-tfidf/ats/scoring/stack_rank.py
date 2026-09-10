"""Section 5 — Stack ranking a candidate pool (SAP SuccessFactors style).

Research: "Stack ranking: Best -> least fit using company skills framework."
Also powers LinkedIn-style recruiter queues and rediscovery flows.

API:
    stack_rank(scored: list[(candidate, score_value)]) -> list[RankedCandidate-like dicts]
    rank_pool(candidates, jd, score_fn) -> list[dict]
"""
from __future__ import annotations

from typing import Callable

from ..models import CandidateRecord, RankedCandidate, ScoreResult


def stack_rank(scored: list[tuple[object, float]]) -> list[tuple[int, object]]:
    """Deterministic sort: score desc, candidate_id asc (stable tie-break)."""
    ranked = sorted(scored, key=lambda pair: (-pair[1], getattr(pair[0], "candidate_id", str(pair[0]))))
    return [(index + 1, candidate) for index, (candidate, _score) in enumerate(ranked)]


def rank_pool(
    candidates: list[CandidateRecord],
    score_fn: Callable[[CandidateRecord], ScoreResult],
) -> list[RankedCandidate]:
    """Score every candidate and return a ranked queue (best -> least fit)."""
    scored = []
    for candidate in candidates:
        score = score_fn(candidate)
        scored.append((candidate, score.percentage, score))
    scored.sort(key=lambda triple: (-triple[1], triple[0].candidate_id))
    ranked = []
    for index, (candidate, _pct, score) in enumerate(scored, start=1):
        ranked.append(
            RankedCandidate(
                rank=index,
                candidate=candidate,
                score=score,
                route="needs_manual_review" if score.criteria.undecided else "review",
            )
        )
    return ranked


if __name__ == "__main__":
    from ..models import ScoreResult

    c1 = CandidateRecord("c1", "Ann"); c2 = CandidateRecord("c2", "Bob"); c3 = CandidateRecord("c3", "Cid")
    def score_fn(candidate):
        result = ScoreResult()
        result.percentage = {"c1": 82.0, "c2": 91.0, "c3": 82.0}[candidate.candidate_id]
        return result
    for ranked in rank_pool([c1, c2, c3], score_fn):
        print(ranked.rank, ranked.candidate.name, ranked.score.percentage)
