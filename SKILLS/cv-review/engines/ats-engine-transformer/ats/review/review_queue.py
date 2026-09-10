"""Human review queue — the final universal-pipeline stage.

Research: recruiters see tiers/grades/badges + evidence citations, then decide
in 5-10 seconds per CV. This module builds that queue view from ranked
candidates.

API:
    build_queue(ranked: list[RankedCandidate]) -> list[dict]
    queue_summary(queue) -> dict
"""
from __future__ import annotations

from ..models import RankedCandidate


def build_queue(ranked: list[RankedCandidate]) -> list[dict]:
    """Tiered, sorted recruiter queue with one-glance evidence."""
    queue = []
    for entry in ranked:
        queue.append(
            {
                "rank": entry.rank,
                "candidate": entry.candidate.name,
                "score": entry.score.percentage,
                "tier": entry.score.tier,
                "grade": entry.score.grade,
                "stars": entry.score.stars,
                "criteria": f"Meets {entry.score.criteria.met} of {entry.score.criteria.total}",
                "route": entry.route,
                "top_evidence": entry.top_evidence[:3],
            }
        )
    return queue


def queue_summary(queue: list[dict]) -> dict:
    counts: dict[str, int] = {}
    for entry in queue:
        route = entry["route"] if isinstance(entry, dict) else entry.route
        counts[route] = counts.get(route, 0) + 1
    top = queue[0]
    return {
        "total": len(queue),
        "routes": counts,
        "top": (top["candidate"] if isinstance(top, dict) else top.candidate.name),
        "note": "AI sorts the queue; the human decides (5-10s per CV)",
    }


if __name__ == "__main__":
    from ..models import CandidateRecord, CriterionSummary, RankedCandidate, ScoreResult

    entry = RankedCandidate(
        rank=1, candidate=CandidateRecord("c1", "Ann"),
        score=ScoreResult(percentage=88.0, tier="Strong", grade="A", criteria=CriterionSummary(met=3, total=4)),
    )
    print(build_queue([entry]))
    print(queue_summary([entry]))
