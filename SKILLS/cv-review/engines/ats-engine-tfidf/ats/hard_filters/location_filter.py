"""Section 1 — Location / willingness-to-relocate hard filter.

API:
    location_filter(candidate_locations, job_locations,
                    remote_ok=False, willing_to_relocate=False) -> FilterResult
"""
from __future__ import annotations

from ..models import FilterResult


def _norm(s: str) -> str:
    return " ".join(s.lower().split())


def location_filter(
    candidate_locations: list[str] | None,
    job_locations: list[str] | None,
    remote_ok: bool = False,
    willing_to_relocate: bool = False,
) -> FilterResult:
    if not job_locations:
        return FilterResult("location", True, "No location constraint on the job", "filter")
    if remote_ok:
        return FilterResult("location", True, "Remote allowed", "filter")
    if willing_to_relocate:
        return FilterResult("location", True, "Candidate willing to relocate", "filter")
    jobs = {_norm(j) for j in job_locations or []}
    cands = [_norm(c) for c in (candidate_locations or [])]
    for cand in cands:
        for job in jobs:
            if cand == job or cand in job or job in cand:
                return FilterResult("location", True, f"Location match: {cand}", "filter")
        # state-level containment: "austin, tx" vs "tx"
        cand_state = cand.split(",")[-1].strip()
        for job in jobs:
            job_state = job.split(",")[-1].strip()
            if cand_state and cand_state == job_state:
                return FilterResult("location", True, f"Same state/region: {cand_state}", "filter")
    return FilterResult(
        "location", False,
        f"No overlap between candidate {cands or ['(unknown)']} and job {sorted(jobs)}; not willing to relocate",
        "knockout",
    )


if __name__ == "__main__":
    print(location_filter(["Austin, TX"], ["Austin, TX"]))
    print(location_filter(["New York, NY"], ["Austin, TX"]))
    print(location_filter(["New York, NY"], ["Austin, TX"], willing_to_relocate=True))
    print(location_filter(["Remote"], ["Austin, TX"], remote_ok=True))
