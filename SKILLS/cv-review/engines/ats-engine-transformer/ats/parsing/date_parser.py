"""Section 2 — Date parsing & normalization (MM/YYYY preferred).

Research failures handled here: "Dates placed before employer names (Taleo
loses whole experience sections)", "Non-standard date formats (miscalculated
tenure)".

API:
    parse_date(token) -> (year, month) | None
    parse_date_range(line) -> DateRange
    normalize_date(d) -> "MM/YYYY" | ""
"""
from __future__ import annotations

import re

from ..models import DateRange

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

MONTH_RE = (
    r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
)

# "01/2020" (MM/YYYY — month taken from the numerator)
_DATE_NUMERIC = re.compile(r"\b(?P<nmonth>0?[1-9]|1[0-2])/(?P<year>(?:19|20)\d{2})\b")
# "Jan 2020", "January 2020", "SEP 2019", "2020"
_DATE_TOKEN = re.compile(
    rf"(?:(?P<month>{MONTH_RE})\.?,?\s*)?(?P<year>\b(?:19|20)\d{{2}}\b)",
    re.IGNORECASE,
)
_CURRENT_RE = re.compile(r"\b(present|current|currently|now|till date|today|ongoing)\b", re.IGNORECASE)
_RANGE_SPLIT = re.compile(r"\s*(?:[-–—]|\bto\b|\buntil\b)\s*", re.IGNORECASE)


def parse_date(token: str) -> tuple[int, int] | None:
    """Parse a date-ish token into (year, month). Month defaults to 1."""
    token = token.strip()
    if not token:
        return None
    numeric = _DATE_NUMERIC.search(token)
    if numeric:
        return int(numeric.group("year")), int(numeric.group("nmonth"))
    match = _DATE_TOKEN.search(token)
    if not match:
        return None
    year = int(match.group("year"))
    month = 1
    if match.group("month"):
        month = MONTHS.get(match.group("month").lower()[:3], 1)
    return year, month


def normalize_date(d: tuple[int, int] | None) -> str:
    if not d:
        return ""
    year, month = d
    return f"{month:02d}/{year}"


def parse_date_range(line: str) -> DateRange:
    """Extract a date range from a line. Tolerates dates before or after employer names."""
    line = line.strip()
    result = DateRange(raw=line)

    has_current = bool(_CURRENT_RE.search(line))
    parts = _RANGE_SPLIT.split(line, maxsplit=1)

    if len(parts) == 2:
        left, right = parts
        result.start = parse_date(left)
        if has_current:
            result.is_current = True
            result.end = None
        else:
            result.end = parse_date(right)
            if result.start is None:
                result.start = parse_date(right)
        return result

    if has_current:
        result.is_current = True
        result.start = parse_date(_CURRENT_RE.sub("", line))
        return result

    result.start = parse_date(line)
    return result


def range_to_months(rng: DateRange, today: tuple[int, int] = (2026, 9)) -> int:
    """Tenure in months for a DateRange (used by factors/years_experience)."""
    if rng.start is None:
        return 0
    sy, sm = rng.start
    if rng.is_current or rng.end is None:
        ey, em = today
    else:
        ey, em = rng.end
    return max(0, (ey - sy) * 12 + (em - sm))


if __name__ == "__main__":
    for sample in [
        "01/2020 - Present  |  Senior Engineer, Acme",
        "Jan 2018 – Dec 2019   Backend Developer, Beta LLC",
        "2020-2023",
        "2015",
        "May 2016 to Aug 2017",
    ]:
        rng = parse_date_range(sample)
        print(f"{sample!r:55} -> {normalize_date(rng.start)} -> "
              f"{'Present' if rng.is_current else normalize_date(rng.end)} "
              f"({range_to_months(rng)} mo)")
