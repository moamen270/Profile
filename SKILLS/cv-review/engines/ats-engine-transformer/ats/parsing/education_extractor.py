"""Section 2 — Education extraction (degrees, fields, institutions, years).

API:
    extract_education(text | lines, education_section: str | None) -> list[Education]
"""
from __future__ import annotations

import re

from ..models import Education
from .date_parser import _DATE_TOKEN

DEGREE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(ph\.?d|doctorate|doctor of philosophy)\b", re.I), "phd"),
    (re.compile(r"\b(m\.?b\.?a\.?|master of business administration)\b", re.I), "master"),
    (re.compile(r"\b(m\.?s\.?c?|master of \w+|masters?)\b", re.I), "master"),
    (re.compile(r"\b(b\.?s\.?c?|b\.?a\.?|b\.?tech|bachelor(?:'s)?(?: of \w+)?)\b", re.I), "bachelor"),
    (re.compile(r"\bassociate(?:'s)?(?: degree)?\b", re.I), "associate"),
    (re.compile(r"\bdiploma\b", re.I), "diploma"),
]

FIELD_RE = re.compile(
    r"(?:(?:of|in)\s+)?([A-Z][A-Za-z&\s]{3,40}?)(?=\s*(?:,|from|[-–]|\(|University|College|Institute|School|\d{4}|$))"
)
INSTITUTION_RE = re.compile(
    r"((?:[A-Z][\w.&'-]*\s+){0,3}(?:University|College|Institute|School|Academy|Polytechnic)"
    r"(?:\s+(?:of|at|for)\s+[A-Z][\w.&'-]*|\s+[A-Z][\w.&'-]*){0,3})"
)
_INSTITUTE_ABBR_RE = re.compile(r"\b((?:IIT|NIT|IIIT|BITS|VIT|MIT|NUS)\s+[A-Z][\w-]*)\b")


def extract_education(text: str, education_section: str | None = None) -> list[Education]:
    source = education_section if education_section else text
    results: list[Education] = []

    for line in (l for l in source.splitlines() if l.strip()):
        degree = None
        raw_degree = None
        for regex, canonical in DEGREE_PATTERNS:
            match = regex.search(line)
            if match:
                degree = canonical
                raw_degree = match.group(0)
                degree_end = match.end()
                break
        if not degree:
            continue

        field_match = FIELD_RE.search(line, degree_end)
        institution_match = INSTITUTION_RE.search(line) or _INSTITUTE_ABBR_RE.search(line)
        year = None
        year_match = _DATE_TOKEN.search(line)
        if year_match:
            year = int(year_match.group("year"))
        results.append(
            Education(
                degree=degree,
                raw_degree=raw_degree,
                field=(field_match.group(1).strip(" ,.") if field_match else None),
                institution=(institution_match.group(0).strip() if institution_match else None),
                year=year,
            )
        )
    return results


if __name__ == "__main__":
    section = """
EDUCATION
M.S. Computer Science, University of Texas, 2019
B.Tech Information Technology - IIT Delhi, 2015
"""
    for ed in extract_education(section):
        print(ed.degree, "|", ed.field, "|", ed.institution, "|", ed.year)
