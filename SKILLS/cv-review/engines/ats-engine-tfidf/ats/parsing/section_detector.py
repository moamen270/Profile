"""Section 2 — Section detection via a dictionary of known headers.

Research: "'Work Experience' works; 'My Journey' fails. Keywords get assigned
to the wrong category — or none at all." We detect known headers, map lines to
sections, and flag unrecognized candidate headers as warnings.

API:
    detect_sections(lines) -> (sections: dict[str, str], unknown_headers: list[str])
"""
from __future__ import annotations

import re

SECTION_ALIASES: dict[str, list[str]] = {
    "summary": ["summary", "professional summary", "objective", "profile", "about me", "about"],
    "experience": ["work experience", "experience", "employment", "employment history",
                   "professional experience", "career history", "work history"],
    "education": ["education", "academic background", "academics", "education & training"],
    "skills": ["skills", "technical skills", "core skills", "key skills", "competencies",
               "skills & expertise", "technologies", "tech stack"],
    "certifications": ["certifications", "certificates", "licenses & certifications",
                       "licenses", "credentials"],
    "projects": ["projects", "personal projects", "selected projects"],
    "achievements": ["achievements", "awards", "accomplishments", "honors", "honors & awards"],
    "contact": ["contact", "contact information", "contact info"],
}

_KNOWN_FLAT = {alias: canon for canon, aliases in SECTION_ALIASES.items() for alias in aliases}

_HEADER_CANDIDATE = re.compile(r"^[A-Z][A-Za-z&/ ,'()-]{2,44}$")


def _clean(line: str) -> str:
    return " ".join(line.strip().strip(":").split()).lower()


def _looks_like_header(line: str, lines: list[str], idx: int) -> bool:
    stripped = line.strip()
    if not stripped or not _HEADER_CANDIDATE.match(stripped):
        return False
    if stripped.isupper() and 2 < len(stripped) <= 45:
        return True
    words = stripped.split()
    nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
    # title-case standalone line: few words, no punctuation lists, followed by blank/end
    return (
        len(words) <= 4
        and "," not in stripped
        and not any(ch.isdigit() for ch in stripped)
        and nxt == ""
    )


def detect_sections(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    """Assign lines to sections based on known headers.

    Returns (sections dict section->text, list of unrecognized header lines).
    Content before any known header lands in 'header' (usually the contact block).
    """
    sections: dict[str, list[str]] = {}
    unknown: list[str] = []
    current = "header"

    for idx, line in enumerate(lines):
        cleaned = _clean(line)
        matched = _KNOWN_FLAT.get(cleaned)
        if matched:
            current = matched
            sections.setdefault(current, [])
            continue
        if _looks_like_header(line, lines, idx):
            unknown.append(line.strip())
        sections.setdefault(current, []).append(line)

    return {name: "\n".join(body).strip() for name, body in sections.items() if "\n".join(body).strip()}, unknown


if __name__ == "__main__":
    sample = [
        "Jane Doe", "jane@example.com", "Austin, TX",
        "WORK EXPERIENCE", "Engineer at Acme 2020-Present",
        "MY JOURNEY", "I started coding at age 12",
        "SKILLS", "Python, SQL",
    ]
    found, unknown = detect_sections(sample)
    for name, body in found.items():
        print(f"[{name}] {body[:60]!r}")
    print("unknown headers:", unknown)
