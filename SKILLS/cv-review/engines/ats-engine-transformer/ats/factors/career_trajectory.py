"""Section 6.9 — Career trajectory logic (progression, tenure, gaps, job-hopping).

API:
    career_gaps(experiences, min_gap_months=3) -> [(gap_months, from, to)]
    career_trajectory_factor(parsed_resume) -> FactorResult
"""
from __future__ import annotations

from ..models import FactorResult, ParsedResume
from ..parsing.date_parser import range_to_months

SENIOR_WORDS = ["senior", "staff", "principal", "lead", "head", "director", "vp", "manager"]


def experience_spans(parsed_resume: ParsedResume, today=(2026, 9)) -> list[tuple[int, int]]:
    """(start_month_index, end_month_index) per experience, relative to 1900-01."""
    return experience_spans_list(parsed_resume.experiences, today)


def experience_spans_list(experiences: list, today=(2026, 9)) -> list[tuple[int, int]]:
    """(start_month_index, end_month_index) per experience, relative to 1900-01."""
    spans = []
    for experience in experiences:
        rng = experience.date_range
        if rng.start is None:
            continue
        sy, sm = rng.start
        if rng.is_current or rng.end is None:
            ey, em = today
        else:
            ey, em = rng.end
        spans.append(((sy - 1900) * 12 + sm, (ey - 1900) * 12 + em))
    return sorted(spans)


def career_gaps(parsed_resume_or_experiences, min_gap_months: int = 3, today: tuple[int, int] = (2026, 9)) -> list[tuple[int, tuple, tuple]]:
    """Employment gaps >= min_gap_months between consecutive roles."""
    experiences = _as_experiences(parsed_resume_or_experiences)
    gaps = []
    spans = experience_spans_list(experiences, today)
    for (prev_start, prev_end), (next_start, _next_end) in zip(spans, spans[1:]):
        gap = next_start - prev_end - 1
        if gap >= min_gap_months:
            gaps.append((gap, prev_end, next_start))
    return gaps


def _as_experiences(value) -> list:
    if hasattr(value, "experiences"):
        return value.experiences
    return value


def has_progression(parsed_resume: ParsedResume) -> bool:
    """Seniority keyword present in a later title than the earliest."""
    titles = [e.title or "" for e in parsed_resume.experiences if e.title]
    if len(titles) < 2:
        return False
    earliest, latest = titles[-1].lower(), titles[0].lower()
    return any(w in latest for w in SENIOR_WORDS) and not any(w in earliest for w in SENIOR_WORDS)


def career_trajectory_factor(parsed_resume: ParsedResume, weight: float = 1.0) -> FactorResult:
    experiences = parsed_resume.experiences
    if not experiences:
        return FactorResult("career_trajectory", 0.0, weight, detail="no parsed experiences")

    score = 0.5
    notes = []

    if has_progression(parsed_resume):
        score += 0.2
        notes.append("title progression detected")
    else:
        notes.append("no clear title progression")

    tenures = [range_to_months(e.date_range) for e in experiences]
    avg_tenure = sum(tenures) / len(tenures) / 12 if tenures else 0
    if avg_tenure >= 2.0:
        score += 0.1
        notes.append(f"healthy avg tenure {avg_tenure:.1f}y")
    elif avg_tenure < 1.0 and len(tenures) >= 3:
        score -= 0.15
        notes.append(f"job-hopping pattern: avg tenure {avg_tenure:.1f}y")

    gaps = career_gaps(experiences)
    big_gaps = [g for g in gaps if g[0] >= 12]
    if big_gaps:
        score -= 0.1 * min(len(big_gaps), 2)
        notes.append(f"{len(big_gaps)} employment gap(s) >= 12mo")
    else:
        notes.append("no significant gaps")

    return FactorResult(
        name="career_trajectory", score=round(max(0.0, min(1.0, score)), 4), weight=weight,
        evidence={"avg_tenure_months": avg_tenure_months(tenures), "gaps": len(gaps)},
        detail="; ".join(notes),
    )


def avg_tenure_months(tenures: list[int]) -> float:
    return sum(tenures) / len(tenures) if tenures else 0.0


if __name__ == "__main__":
    from ..models import DateRange, Experience

    resume = ParsedResume(experiences=[
        Experience(title="Senior Engineer", date_range=DateRange(start=(2020, 1), is_current=True)),
        Experience(title="Engineer", date_range=DateRange(start=(2017, 1), end=(2019, 12))),
    ])
    print(career_trajectory_factor(resume).detail)
