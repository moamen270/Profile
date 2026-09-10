"""Section 7 — LinkedIn Recruiter personalized relevance ranking.

Research: "personalized relevance ranking (query match + searcher context +
similar-search patterns + past search history); boolean filters; 'Spotlights'
(more likely to engage, top applicants); spam detection on keyword stuffing."

Deterministic re-ranking of a candidate list for a specific searcher:

  relevance = 0.5*query_match + 0.2*team_context + 0.2*similar_search
              + 0.1*history_boost  -  spam_penalty
  + a 'Spotlights' flag for engageable/top applicants.

API:
    relevance_score(candidate, query_skills, searcher_profile, history) -> (score, components)
    rank_candidates(candidates, query_skills, searcher_profile, history) -> list[dict]
"""
from __future__ import annotations

from ..models import CandidateRecord

WEIGHTS = {"query": 0.5, "context": 0.2, "similar": 0.2, "history": 0.1}


def _norm(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _safe_int(value) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def candidate_skills(candidate: CandidateRecord) -> set[str]:
    return {s.lower() for s in (candidate.meta.get("skills") or [])}


def query_match(candidate: CandidateRecord, query_skills: set[str]) -> float:
    """% of the query's skills present in the candidate."""
    if not query_skills:
        return 0.5
    skills = candidate_skills(candidate)
    if not skills:
        return 0.0
    return _norm(len({s.lower() for s in query_skills} & skills) / len(query_skills))


def searcher_context(candidate: CandidateRecord, searcher_profile: dict) -> float:
    """Similarity to the searcher's team skills (past hires / open reqs)."""
    team_skills = {s.lower() for s in searcher_profile.get("team_skills", [])}
    skills = candidate_skills(candidate)
    if not team_skills:
        return 0.5
    return _norm(len(team_skills & skills) / len(team_skills))


def similar_search(candidate: CandidateRecord, history: list[dict]) -> float:
    """How much this candidate resembles past accepted search results."""
    if not history:
        return 0.5
    skills = candidate_skills(candidate)
    ratios = []
    for record in history:
        past = {s.lower() for s in record.get("skills", [])}
        if past:
            ratios.append(len(past & skills) / len(past))
    return _norm(sum(ratios) / len(history)) if ratios else 0.5


def history_boost(candidate: CandidateRecord) -> float:
    """Past interactions: viewed before / replied / engaged with content."""
    interactions = candidate.meta.get("interactions") or {}
    if not interactions:
        return 0.5
    return _norm(sum(min(0.2, 0.05 * _safe_int(count)) for count in interactions.values()))


def spam_penalty(candidate: CandidateRecord) -> float:
    """LinkedIn spam detection on keyword stuffing (meta.stuffing_hits)."""
    return min(0.2, 0.05 * len(candidate.meta.get("stuffing_hits") or []))


def spotlight(candidate: CandidateRecord) -> bool:
    """LinkedIn 'Spotlights': more likely to engage or a top applicant."""
    meta = candidate.meta
    return bool(meta.get("top_applicant") or meta.get("open_to_work") or meta.get("engaged_recently"))


def relevance_score(
    candidate: CandidateRecord,
    query_skills: set[str],
    searcher_profile: dict,
    history: list[dict],
) -> tuple[float, dict]:
    """Personalized relevance = query + context + similar-search + history - spam."""
    components = {
        "query": query_match(candidate, query_skills),
        "context": searcher_context(candidate, searcher_profile),
        "similar": similar_search(candidate, history),
        "history": history_boost(candidate),
    }
    base = sum(WEIGHTS[key] * value for key, value in components.items())
    return round(max(0.0, base - spam_penalty(candidate)), 4), components


def rank_candidates(
    candidates: list[CandidateRecord],
    query_skills: set[str],
    searcher_profile: dict,
    history: list[dict],
) -> list[dict]:
    """Personalized relevance-ranked queue with spotlight flags."""
    scored = []
    for candidate in candidates:
        score, components = relevance_score(candidate, query_skills, searcher_profile, history)
        scored.append(
            {
                "candidate": candidate.name,
                "relevance": score,
                "spotlight": spotlight(candidate),
                "components": components,
            }
        )
    return sorted(scored, key=lambda entry: (-entry["relevance"], entry["candidate"]))


if __name__ == "__main__":
    candidates = [
        CandidateRecord("c1", "Py Dev", meta={"skills": ["python", "sql", "docker"], "top_applicant": True}),
        CandidateRecord("c2", "Designer", meta={"skills": ["figma", "ux"]}),
    ]
    searcher = {"team_skills": ["python", "docker", "aws"]}
    history = [{"skills": ["python", "sql", "docker"]}]
    for entry in rank_candidates(candidates, {"python", "sql"}, searcher, history):
        print(entry)
