"""Section 2 — Contact info extraction (what all parsers extract first).

Research: "Contact info, employers, job titles, date ranges (MM/YYYY preferred),
education, degrees, skills, certifications. Output as HR-XML/JSON."

API:
    extract_contact(lines | text) -> Contact
"""
from __future__ import annotations

import re

from ..models import Contact

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-/%]+", re.IGNORECASE)
GITHUB_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[\w-]+", re.IGNORECASE)
LOCATION_RE = re.compile(
    r"\b([A-Z][a-zA-Z.'-]+(?:\s[A-Z][a-zA-Z.'-]+)*),\s*([A-Z]{2}|[A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})?)\b"
)


def extract_contact(lines: list[str] | str) -> Contact:
    if isinstance(lines, str):
        lines = lines.splitlines()
    contact = Contact()

    for line in lines[:15]:
        if not contact.email:
            match = EMAIL_RE.search(line)
            if match:
                contact.email = match.group(0)
        if not contact.linkedin:
            match = LINKEDIN_RE.search(line)
            if match:
                contact.linkedin = match.group(0)
        if not contact.github:
            match = GITHUB_RE.search(line)
            if match:
                contact.github = match.group(0)
        if not contact.phone:
            # phone may share a line with email/links — match the number fragment only
            match = PHONE_RE.search(line)
            if match:
                contact.phone = match.group(0).strip()

    for line in lines[:15]:
        match = LOCATION_RE.search(line)
        if match and not contact.location:
            contact.location = f"{match.group(1)}, {match.group(2)}"
            break

    for line in lines[:5]:
        stripped = line.strip()
        if (
            stripped
            and not EMAIL_RE.search(stripped)
            and not any(ch.isdigit() for ch in stripped)
            and 1 <= len(stripped.split()) <= 4
            and stripped.replace(" ", "").replace(".", "").replace("'", "").isalpha()
        ):
            contact.name = stripped
            break

    return contact


if __name__ == "__main__":
    sample = [
        "Jane Doe",
        "jane.doe@gmail.com | (512) 555-0134",
        "linkedin.com/in/janedoe | github.com/janedoe",
        "Austin, TX 78701",
        "SUMMARY",
        "Backend engineer with 6 years of experience.",
    ]
    print(extract_contact(sample))
