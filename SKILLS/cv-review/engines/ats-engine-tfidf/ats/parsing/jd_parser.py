"""Section 2 — Job Description parsing: structured JD -> JobDescription.

Extracts title, required/preferred skills (taxonomy-normalized), minimum years,
education requirements, location, salary ceiling, industry — and the basic/
preferred qualification list that LLM-style "Fit & Gap" evaluation consumes.

API:
    parse_job_description(text) -> JobDescription
"""
from __future__ import annotations

import re

from ..models import JobDescription, Qualification
from ..hard_filters.salary_ceiling import parse_salary
from .industry import detect_industry
from .skills_extractor import build_variation_map, find_skills, load_taxonomy

_REQUIRED_HEADINGS = ["requirements", "required", "qualifications", "must have", "must-haves",
                      "what you'll need", "who you are", "about you", "you have"]
_PREFERRED_HEADINGS = ["preferred", "nice to have", "bonus", "plus", "bonus points",
                       "desirable", "would be a plus"]
_RESPONSIBILITY_HEADINGS = ["responsibilities", "what you'll do", "the role", "about the role",
                            "your role", "job description", "duties"]

_YEARS_RE = re.compile(r"(\d+)\s*\+?\s*years?", re.IGNORECASE)
_TITLE_HINTS = ["engineer", "manager", "developer", "designer", "analyst", "scientist",
                "architect", "director", "lead", "specialist", "consultant", "recruiter",
                "accountant", "marketer", "sales"]
_EDU_RE = re.compile(
    r"\b(ph\.?d|doctorate|master(?:'s)?|m\.?b\.?a\.?|m\.?s\.?|bachelor(?:'s)?|b\.?s\.?|b\.?tech)\b", re.I
)
_FIELD_RE = re.compile(r"degree\s+in\s+([A-Za-z&\s]{3,40})")


_MD_HEADING_RE = re.compile(r"^#{1,6}\s+")


def _normalize_heading(line: str) -> str:
    """Strip Markdown decoration so a heading compares as plain text.

    Deliberately literal: this only undoes formatting (``## Preferred
    qualifications`` -> ``preferred qualifications``, ``**Requirements**`` ->
    ``requirements``). It infers nothing. Real ATS parsers are dumb — the point
    is to read the format, not to understand the words.
    """
    text = _MD_HEADING_RE.sub("", line.strip())
    text = text.strip().strip("*_").strip()
    return text.rstrip(":").strip().lower()


def _split_sections_by_heading(text: str) -> list[tuple[str | None, list[str]]]:
    """Split JD text into (heading|None, lines) chunks by heuristic headings."""
    blocks: list[tuple[str | None, list[str]]] = [(None, [])]
    for line in text.splitlines():
        cleaned = _normalize_heading(line)
        if 0 < len(cleaned) <= 45 and _is_heading(line):
            blocks.append((cleaned, []))
        else:
            blocks[-1][1].append(line)
    return blocks


def _is_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    # A bullet is content, never a heading — checked first so that a line like
    # "- Required: C#" is not mistaken for a "Requirements" section header.
    if is_list_item_check(stripped):
        return False
    # A leading '#' is an unambiguous Markdown heading marker — treat it as one.
    if _MD_HEADING_RE.match(stripped):
        return 0 < len(_normalize_heading(stripped)) <= 45
    if len(stripped) > 45:
        return False
    if stripped.isupper() or stripped.endswith(":"):
        return True
    # Substring, not equality: real headings read "Preferred qualifications" or
    # "Minimum requirements", not the bare keyword. This mirrors the matching
    # that extract_qualifications() and _classify_skills() already do, so a
    # heading they would act on is one this function recognizes.
    normalized = _normalize_heading(stripped)
    return any(
        h in normalized
        for h in _REQUIRED_HEADINGS + _PREFERRED_HEADINGS + _RESPONSIBILITY_HEADINGS
    )


def extract_qualifications(text: str) -> list[Qualification]:
    """Lift basic/preferred qualifications out of the JD (bullet/numbered lists only).

    Only list items (bullets or numbered) qualify; prose lines, headers, and
    metadata (location/salary) are excluded."""
    quals: list[Qualification] = []
    kind = "basic"
    for heading, lines in _split_sections_by_heading(text):
        if heading and any(h in heading for h in _PREFERRED_HEADINGS):
            kind = "preferred"
        elif heading and any(h in heading for h in _REQUIRED_HEADINGS):
            kind = "basic"
        for line in lines:
            stripped = line.strip()
            # must look like a list item to be a qualification
            if not is_list_item_check(stripped):
                continue
            content = re.sub(r"^[•\-*–◦‣·]\s+|^\d+[.)]\s+", "", stripped).strip()
            if not content or len(content) < 8:
                continue
            words = content.split()
            if 2 <= len(words) <= 40:
                quals.append(Qualification(text=content, kind=kind))
    return quals


def is_list_item_check(line: str) -> bool:
    return bool(re.match(r"^[•\-*–◦‣·]\s+", line)) or bool(re.match(r"^\d+[.)]\s+", line))


def _classify_skills(text: str, variation_map: dict[str, str]) -> tuple[set[str], set[str]]:
    """Split taxonomy skills into required vs preferred by JD heading."""
    all_skills = find_skills(text, variation_map)
    required_txt, preferred_txt = [], []
    for heading, lines in _split_sections_by_heading(text):
        body = "\n".join(lines)
        if heading and any(h in heading for h in _PREFERRED_HEADINGS):
            preferred_txt.append(body)
        elif heading and any(h in heading for h in _REQUIRED_HEADINGS):
            required_txt.append(body)
    if required_txt:
        required = find_skills("\n".join(required_txt), variation_map)
    else:
        required = set(all_skills)
    preferred = find_skills("\n".join(preferred_txt), variation_map)
    return required, preferred


def parse_job_description(text: str, taxonomy_path=None) -> JobDescription:
    jd = JobDescription(raw_text=text)
    variation_map = build_variation_map(load_taxonomy(taxonomy_path))

    jd.required_skills, jd.preferred_skills = _classify_skills(text, variation_map)

    years_match = _YEARS_RE.search(text)
    if years_match:
        jd.min_years = int(years_match.group(1))

    edu = _EDU_RE.search(text)
    if edu:
        token = edu.group(0).lower()
        if "ph" in token or "doctor" in token:
            jd.education_level = "phd"
        elif token.startswith("m") and not token.startswith("manager"):
            jd.education_level = "master"
        else:
            jd.education_level = "bachelor"
    field = _FIELD_RE.search(text)
    if field:
        jd.education_field = field.group(1).strip(" ,.")

    title_match = re.search(r"(?:job title|position|role)\s*[:\-]\s*(.+)", text, re.I)
    if title_match:
        jd.title = title_match.group(1).strip()
    else:
        for line in text.splitlines():
            stripped = line.strip()
            if 3 <= len(stripped) <= 60 and not _YEARS_RE.search(stripped):
                lower = stripped.lower()
                if any(h in lower for h in _TITLE_HINTS):
                    jd.title = stripped
                    break

    loc = re.search(r"(?:location|based in)\s*[:\-]\s*(.+)", text, re.I)
    if loc:
        jd.location = loc.group(1).strip()
    jd.remote_allowed = bool(
        re.search(r"\bremote\b|\bwork from home\b|\bdistributed team\b", text, re.I)
    )

    _lo, hi = parse_salary(text)
    jd.salary_ceiling = int(hi) if hi else None

    jd.industry = detect_industry(text)
    jd.qualifications = extract_qualifications(text)
    return jd


if __name__ == "__main__":
    jd_text = """
Senior Backend Engineer

Location: Austin, TX (hybrid)
Salary: up to $150k

Requirements:
- 5+ years of professional software engineering experience
- Strong Python and SQL skills
- Experience with Docker and Kubernetes
- Bachelor's degree in Computer Science

Nice to have:
- Experience with Kafka and Terraform
- AWS certifications
"""
    jd = parse_job_description(jd_text)
    print("title:", jd.title)
    print("min years:", jd.min_years)
    print("required:", sorted(jd.required_skills))
    print("preferred:", sorted(jd.preferred_skills))
    print("quals:", len(jd.qualifications))
