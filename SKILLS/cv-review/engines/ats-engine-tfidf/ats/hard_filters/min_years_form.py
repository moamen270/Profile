"""Section 1 — Minimum years of experience answered ON THE FORM.

Critical research finding: enterprise ATS take this number from the application
form answer, NOT calculated from the CV. Legacy Taleo literally never inspects
the resume for this.

API:
    min_years_form_filter(answered_years, required_years) -> FilterResult
"""
from __future__ import annotations

from ..hard_filters.knockout_questions import _to_number
from ..models import FilterResult


def min_years_form_filter(answered_years: float | int | None, required_years: int | None) -> FilterResult:
    if required_years is None:
        return FilterResult("min_years_form", True, "No minimum configured — pass through", "filter")
    if answered_years is None or str(answered_years).strip() == "":
        return FilterResult("min_years_form", False, "Required form answer missing — instant auto-reject", "knockout")
    years = _to_number(answered_years)
    if years is None:
        return FilterResult("min_years_form", False, f"Non-numeric answer: {answered_years}", "knockout")
    if years >= required_years:
        return FilterResult("min_years_form", True, f"{years:g} >= required {required_years}", "knockout")
    return FilterResult(
        "min_years_form", False,
        f"{years:g} < required {required_years} (form answer, not CV-derived) — instant auto-reject",
        "knockout",
    )


if __name__ == "__main__":
    print(min_years_form_filter(5, 3))
    print(min_years_form_filter(2, 3))
    print(min_years_form_filter(None, 3))
