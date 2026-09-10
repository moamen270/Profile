"""Section 8 — Human-in-the-loop routing / opt-out.

Research: "Greenhouse/Lever/iCIMS/Eightfold all design AI as *advisory
prioritization*, never autonomous rejection" and "opt-out (routing to
'Needs manual review')". The ONLY auto-rejection in real ATS is knockout
form questions — everything else routes to a human queue.

API:
    route_candidate(knockout_failed, undecided_ratio, threshold=0.34) -> str
    human_review_queue(ranked) -> dict  # {review: [...], needs_manual_review: [...]}
"""
from __future__ import annotations

from ..models import RankedCandidate

REVIEW = "review"
NEEDS_MANUAL_REVIEW = "needs_manual_review"


def route_candidate(
    knockout_failed: bool,
    undecided_ratio: float = 0.0,
    llm_used: bool = False,
    opted_out: bool = False,
    threshold: float = 0.34,
) -> str:
    """Decide the pipeline route. AI never rejects — only knockouts do."""
    if knockout_failed:
        return "rejected"          # only form-based knockout rejections, per research
    if opted_out:
        return NEEDS_MANUAL_REVIEW
    if undecided_ratio > threshold:
        return NEEDS_MANUAL_REVIEW  # too many undecided criteria -> human review
    return REVIEW


def needs_manual_review(ranked: list[RankedCandidate]) -> list[RankedCandidate]:
    return [r for r in ranked if r.route == NEEDS_MANUAL_REVIEW]


def human_review_queue(ranked: list[RankedCandidate]) -> dict[str, list[RankedCandidate]]:
    """Split a ranked queue into normal review vs needs-manual-review buckets."""
    queue: dict[str, list[RankedCandidate]] = {REVIEW: [], NEEDS_MANUAL_REVIEW: []}
    for entry in ranked:
        queue.setdefault(entry.route, []).append(entry)
    return queue


NEEDS_MANUAL_REVIEW = "needs_manual_review"


if __name__ == "__main__":
    print(route_candidate(knockout_failed=True))
    print(route_candidate(knockout_failed=False, undecided_ratio=0.5))
    print(route_candidate(knockout_failed=False, opted_out=True))
