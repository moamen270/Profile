"""Section 6.3 — Job title taxonomy match (heavy structural weight).

Research: "'Senior Product Manager' exact title + tenure beats title stuffing."
Seniority level comparison + alias resolution + family matching.

API:
    title_seniority(title) -> int                    # 1..9 via data/title_taxonomy.json
    title_match_factor(resume_titles, jd_title) -> FactorResult
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from ..models import FactorResult

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "title_taxonomy.json"


def load_title_taxonomy() -> dict:
    with open(DATA_FILE, encoding="utf-8") as handle:
        return json.load(handle)


def canonical_title(title: str, taxonomy: dict | None = None) -> str:
    taxonomy = taxonomy or load_title_taxonomy()
    title_l = " ".join(title.lower().split())
    title_l = re.sub(r"\(.*?\)", "", title_l).strip()  # strip "(Python)" qualifiers
    return taxonomy.get("title_aliases", {}).get(title_l, title_l)


def title_seniority(title: str | None, taxonomy: dict | None = None) -> int:
    if not title:
        return 0
    taxonomy = taxonomy or load_title_taxonomy()
    levels = taxonomy.get("seniority_levels", {})
    title_l = " ".join(title.lower().split())
    for token in reversed(title_l.split()):
        if token in levels:
            return int(levels[token])
    for alias, level in levels.items():
        if alias in title_l:
            return int(level)
    return int(taxonomy.get("default_level", 3))


def title_match_factor(resume_titles: list[str], jd_title: str | None, weight: float = 2.5) -> FactorResult:
    """Score = 0.5*family match + 0.5*seniority closeness; exact canonical match = 1.0."""
    taxonomy = load_title_taxonomy()
    if not jd_title or not resume_titles:
        return FactorResult("title_match", 0.0, weight, detail="missing title data")

    jd_canon = canonical_title(jd_title, taxonomy)
    jd_family = family_of(jd_canon, taxonomy)
    jd_level = title_seniority(jd_title, taxonomy)

    best = 0.0
    best_detail = ""
    for title in resume_titles:
        canon = canonical_title(title, taxonomy)
        if canon == jd_canon:
            candidate, detail = 1.0, f"exact title match: {title}"
        else:
            family_bonus = 0.5 if (family_of(canon, taxonomy) == jd_family and jd_family) else 0.0
            level_delta = abs(title_seniority(title, taxonomy) - jd_level)
            candidate = family_bonus + level_score(level_delta)
            detail = f"{title} vs {jd_title}"
        if candidate > best:
            best, best_detail = candidate, detail
    return FactorResult(
        name="title_match", score=round(min(1.0, best), 4), weight=weight,
        evidence={"jd_title": jd_title, "best_detail": best_detail},
        detail=best_detail,
    )


def family_of(title: str, taxonomy: dict) -> str:
    for family, members in taxonomy.get("title_families", {}).items():
        if title == family or title in members:
            return family
    return ""


def level_score(delta: int) -> float:
    return max(0.0, 0.5 - 0.125 * min(delta, 4))


if __name__ == "__main__":
    print(title_match_factor(["Senior Software Engineer", "Backend Developer"], "Senior Backend Engineer").detail)
    print(title_match_factor(["Marketing Manager"], "Senior Backend Engineer").detail)
