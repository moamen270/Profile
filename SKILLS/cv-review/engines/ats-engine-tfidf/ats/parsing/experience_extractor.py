"""Section 2 — Experience extraction: employers, titles, date ranges, bullets.

Handles "Dates placed before employer names (Taleo loses whole experience
sections)" by scanning any line containing a date range and treating it as an
experience divider — whether the date comes first or last.

API:
    extract_experiences(text | lines, experience_section: str | None) -> list[Experience]
"""
from __future__ import annotations

import re

from ..models import Experience
from .date_parser import MONTH_RE, parse_date_range

# A date RANGE (two sides) or "<date> - Present" — required to open an entry.
# A bare year ("Hackathon 2021", "graduated 2017") is NOT an experience divider.
DATE_RANGE_RE = re.compile(
    rf"(?:{MONTH_RE}\.?,?\s*)?(?:(?:19|20)\d{{2}}|\d{{1,2}}/(?:19|20)\d{{2}})"
    rf"\s*(?:[-–—]|\bto\b|\buntil\b)\s*"
    rf"(?:{MONTH_RE}\.?,?\s*)?(?:(?:19|20)\d{{2}}|\d{{1,2}}/(?:19|20)\d{{2}}"
    rf"|\b(?:present|current|currently|now|till date|today|ongoing)\b)",
    re.IGNORECASE,
)
DATE_FRAGMENT_RE = re.compile(
    rf"(?:{MONTH_RE}\.?,?\s*)?(?:(?:19|20)\d{{2}}|\d{{1,2}}/(?:19|20)\d{{2}})"
    rf"(?:\s*(?:[-–—]|\bto\b|\buntil\b)\s*(?:{MONTH_RE}\.?,?\s*)?(?:(?:19|20)\d{{2}}|\d{{1,2}}/(?:19|20)\d{{2}}))?"
    rf"|\b(?:present|current|currently|now|till date|today|ongoing)\b",
    re.IGNORECASE,
)
BULLET_PREFIX_RE = re.compile(r"^\s*[•\-*–◦‣·]\s+")
SEPARATORS = (" at ", " @ ", " — ", " – ", " | ", ", ")


def has_date(line: str) -> bool:
    """A line opens a new experience only if it contains a true date RANGE."""
    return bool(DATE_RANGE_RE.search(line))


def strip_dates(line: str) -> str:
    """Remove date-looking fragments, leaving title/company text."""
    cleaned = DATE_FRAGMENT_RE.sub(" ", line)
    cleaned = " ".join(cleaned.split())
    return cleaned.strip(" |,–—-\t")


def split_title_company(text: str) -> tuple[str | None, str | None]:
    text = text.strip(" |,\t–—-")
    if not text:
        return None, None
    for sep in SEPARATORS:
        if sep in text:
            left, right = text.split(sep, 1)
            left, right = left.strip(), right.strip(" ,|")
            if left and right:
                return left, right
    return text, None


def is_bullet(line: str) -> bool:
    return bool(BULLET_PREFIX_RE.match(line))


def clean_bullet(line: str) -> str:
    return line.strip().lstrip("•-*–◦‣· ").strip()


def extract_experiences(text: str, experience_section: str | None = None) -> list[Experience]:
    """Parse experience entries from raw text (or a pre-isolated section).

    A line containing a date range starts a new Experience; the leftover text
    is split into title/company. Bullet-ish and prose lines attach to the
    current entry. Entries without any dates are ignored (matches conservative
    real-parser behavior).
    """
    source = experience_section if experience_section else text
    lines = [line for line in source.splitlines() if line.strip()]

    experiences: list[Experience] = []
    current: Experience | None = None

    for line in lines:
        stripped = line.strip()
        if has_date(stripped):
            leftover = strip_dates(stripped)
            title, company = split_title_company(leftover)
            current = Experience(
                title=title,
                company=company,
                date_range=parse_date_range(stripped),
                raw=stripped,
            )
            experiences.append(current)
        elif current is not None:
            if is_bullet(stripped) or len(stripped.split()) >= 8:
                current.bullets.append(clean_bullet(stripped))
            elif len(stripped) <= 60:
                # continuation line: title on one line, company on the next
                t, c = split_title_company(stripped)
                if current.title is None and t:
                    current.title = t
                elif current.company is None and c:
                    current.company = c
            current.raw += "\n" + stripped
    return experiences


if __name__ == "__main__":
    section = """
01/2020 - Present  |  Senior Backend Engineer, Acme Corp
- Led migration of monolith to microservices, cutting latency 40%
- Mentored team of 4 engineers

Jan 2018 – Dec 2019   Backend Developer, Beta LLC
Built REST APIs serving 2M requests/day
"""
    for exp in extract_experiences(section):
        print(exp.title, "|", exp.company, "|", exp.date_range.raw, "|", len(exp.bullets), "bullets")
