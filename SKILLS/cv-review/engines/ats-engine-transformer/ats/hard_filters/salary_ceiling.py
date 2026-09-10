"""Section 1 — Salary expectations above a preset ceiling (instant auto-reject).

API:
    parse_salary(text) -> int | None          # "120k", "$120,000", "80-100k", "1.2L"
    salary_ceiling_filter(expected, ceiling) -> FilterResult
"""
from __future__ import annotations

import re

from ..models import FilterResult

_SALARY_RE = re.compile(
    r"(?P<lo>\d+(?:[.,]\d+)?)\s*(?P<lo_suf>k|m)?(?:\s*[-–—to]+\s*(?P<hi>\d+(?:[.,]\d+)?)\s*(?P<hi_suf>k|m))?"
)


def _to_number(num: str, suffix: str | None) -> float | None:
    try:
        value = float(num.replace(",", ""))
    except ValueError:
        return None
    if suffix:
        value *= {"k": 1_000, "m": 1_000_000}[suffix.lower()]
    return value


def parse_salary(text: str) -> tuple[float | None, float | None]:
    """Extract (low, high) salary in absolute units from free text. (None, None) if absent.

    Scans ALL numeric matches and returns the first plausible salary (>=1000
    or k/m suffixed), ignoring stray small numbers like "3 days" or "5 years"."""
    if not text:
        return None, None
    cleaned = text.replace("$", "").replace(",", "").replace("usd", "").replace("USD", "")
    for match in _SALARY_RE.finditer(cleaned):
        lo = _to_number(match.group("lo"), match.group("lo_suf"))
        hi_raw = match.group("hi")
        hi_suf = match.group("hi_suf")
        hi = _to_number(hi_raw, hi_suf) if hi_raw else lo
        # "80-100k" convention: the suffix applies to both sides of the range
        if lo is not None and hi_suf and not match.group("lo_suf"):
            lo = _to_number(match.group("lo"), hi_suf)
        if lo and hi and lo > hi:
            lo, hi = hi, lo
        if lo is not None and (lo >= 1000 or match.group("lo_suf") or hi_suf):
            return lo, hi
    return None, None


def salary_ceiling_filter(expected: float | None, ceiling: float | None) -> FilterResult:
    name = "salary_ceiling"
    if expected is None:
        return FilterResult("salary_ceiling", True, "No salary expectation stated — pass through", "filter")
    if ceiling is None:
        return FilterResult("salary_ceiling", True, "No ceiling configured — pass through", "filter")
    if expected <= ceiling:
        return FilterResult("salary_ceiling", True, f"Expectation {expected:,.0f} within ceiling {ceiling:,.0f}", "filter")
    return FilterResult(
        "salary_ceiling", False,
        f"Expectation {expected:,.0f} exceeds ceiling {ceiling:,.0f} — instant auto-reject",
        "knockout",
    )


if __name__ == "__main__":
    for sample in ["$120,000", "120k", "80-100k", "90000 USD", "n/a"]:
        print(sample, "->", parse_salary(sample))
    print(salary_ceiling_filter(130000, 150000))
    print(salary_ceiling_filter(180000, 150000))
