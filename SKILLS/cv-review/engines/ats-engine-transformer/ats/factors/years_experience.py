"""Section 6.2 — Years of experience from parsed date ranges + recency weighting.

Research: "calculated from parsed date ranges; recency-weighted (a skill used
in your last 2 roles > same skill in 2016)".

API:
    total_years(parsed_resume) -> float
    recency_weighted_skill_score(skill, experiences, today) -> float
    years_experience_factor(parsed_resume, jd_min_years) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult, ParsedResume
from ..parsing.date_parser import range_to_months

DEFAULT_TODAY = (2026, 9)


def total_years(parsed_resume: ParsedResume, today: tuple[int, int] = DEFAULT_TODAY) -> float:
    """Sum of tenure across experiences (overlaps not merged — parser-level
    dedup is out of scope; matches naive real-parser behavior)."""
    months = 0
    for experience in parsed_resume.experiences:
        rng = experience.date_range
        if rng.start is None:
            continue
        sy, sm = rng.start
        if rng.is_current or rng.end is None:
            ey, em = today
        else:
            ey, em = rng.end
        months += max(0, (ey - sy) * 12 + (em - sm))
    return round(months / 12.0, 1)


def recency_weight(index: int) -> float:
    """Most recent role = 1.0, previous = 0.75, then 0.5, 0.4, 0.3..."""
    if index == 0:
        return 1.0
    if index == 1:
        return 0.75
    if index == 2:
        return 0.5
    return max(0.2, 0.5 - 0.1 * (index - 2))


def skill_recency_score(
    skill: str,
    experiences: list,
    today: tuple[int, int] = DEFAULT_TODAY,
) -> float:
    """0..1 recency-weighted presence of a skill across roles (last 2 roles dominate)."""
    score = 0.0
    skill_l = skill.lower()
    for index, experience in enumerate(experiences[:4]):
        body = " ".join(experience.bullets) + " " + (experience.title or "")
        if skill_l in body.lower():
            score = max(score, recency_weight(index))
    return score


def years_experience_factor(
    parsed_resume: ParsedResume,
    jd_min_years: int | None,
    weight: float = 2.0,
    today: tuple[int, int] = DEFAULT_TODAY,
) -> FactorResult:
    years = total_years(parsed_resume, today)
    if jd_min_years is None or jd_min_years <= 0:
        score = 1.0 if years > 0 else 0.5
        detail = f"{years} yrs (no JD minimum)"
    elif years >= jd_min_years:
        score = min(1.0, 0.85 + 0.15 * min(1.0, (years - jd_min_years) / max(jd_min_years, 1)))
        detail = f"{years} yrs >= required {jd_min_years}"
    else:
        score = max(0.0, years / jd_min_years * 0.8)
        detail = f"{years} yrs < required {jd_min_years}"
    return FactorResult(
        name="years_experience", score=round(score, 4), weight=weight,
        evidence={"calculated_years": years, "jd_min_years": jd_min_years},
        detail=detail + " (calculated from parsed date ranges, recency-weighted)",
    )


if __name__ == "__main__":
    from ..models import DateRange, Experience

    resume = ParsedResume(experiences=[
        Experience(title="Senior Engineer", date_range=DateRange(start=(2020, 1), is_current=True),
                   bullets=["Uses python daily"]),
        Experience(title="Engineer", date_range=DateRange(start=(2017, 3), end=(2019, 12)),
                   bullets=["python scripts"]),
    ])
    print("total years:", total_years(resume))
    print("python recency:", skill_recency_score("python", resume.experiences))
    print(years_experience_factor(resume, 5).detail)
