"""Section 5 — Ashby criteria-met percentage ("Meets 1 of 3" + citations).

Research: "Ashby: Criteria Met % — e.g. 'Meets 1 of 3' with clickable resume
evidence citations" and "up to 50 criteria, Meets/Does Not Meet/Undecided".

API:
    criteria_met_summary(results) -> dict  # {met, total, label, undecided}
    criteria_met_label(summary) -> str     # "Meets 2 of 3"
"""
from __future__ import annotations

from ..models import CriterionResult, CriterionSummary


def criteria_met_summary(results: list[CriterionResult]) -> dict:
    met = sum(1 for r in results if r.status == "met")
    not_met = sum(1 for r in results if r.status == "not_met")
    undecided = sum(1 for r in results if r.status == "undecided")
    return {
        "met": met,
        "not_met": not_met,
        "undecided": undecided,
        "total": len(results),
        "label": criteria_met_label(len(results), met),
    }


def criteria_met_label(total: int, met: int) -> str:
    return f"Meets {met} of {total}"


def undecided_ratio(summary: dict) -> float:
    """High undecided ratio -> route to human review (section 8 opt-out)."""
    return summary["undecided"] / summary["total"] if summary["total"] else 0.0


def criteria_met(results: list[CriterionResult]) -> CriterionSummary:
    """Full CriterionSummary (with basic/preferred split)."""
    summary = CriterionSummary(results=list(results), total=len(results))
    for result in results:
        if result.qualification.kind == "basic":
            summary.basic_total += 1
        else:
            summary.preferred_total += 1
        if result.status == "met":
            summary.met += 1
            if result.qualification.kind == "basic":
                summary.basic_met += 1
            else:
                summary.preferred_met += 1
        elif result.status == "undecided":
            summary.undecided += 1
    return summary


if __name__ == "__main__":
    from ..models import Qualification

    results = [
        CriterionResult(Qualification("5+ years exp"), "met", "7 years"),
        CriterionResult(Qualification("Python"), "met", "python expert"),
        CriterionResult(Qualification("AWS"), "undecided"),
    ]
    print(criteria_met_summary(results))
