"""Section 8 — Resume anonymization before LLM processing (Lever practice).

Research: "Lever anonymizes resumes (strips names, demographics, military
status) before LLM processing."

API:
    anonymize_text(text) -> (clean_text, redactions)
    anonymize_contact(contact) -> Contact
"""
from __future__ import annotations

import re

from ..models import Contact

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
MILITARY_RE = re.compile(
    r"\b(?:us\s?(?:army|navy|marines|air force|coast guard)|veteran|sergeant|"
    r"lieutenant|captain|colonel|general|petty officer|corporal)\b",
    re.IGNORECASE,
)
DEMOGRAPHIC_RE = re.compile(
    r"\b(?:male|female|gender|marital status|married|single|religion|"
    r"ethnicity|race|disability|national origin|\d{1,3}\s*years old)\b",
    re.IGNORECASE,
)


def anonymize_text(text: str) -> tuple[str, list[str]]:
    """Strip PII + protected attributes. Returns (clean_text, list_of_redactions)."""
    redactions: list[str] = []

    if EMAIL_RE.search(text):
        text = EMAIL_RE.sub("[EMAIL]", text)
        redactions.append("email")
    if PHONE_RE.search(text):
        text = PHONE_RE.sub("[PHONE]", text)
        redactions.append("phone")
    if URL_RE.search(text):
        text = URL_RE.sub("[URL]", text)
        redactions.append("urls")
    if MILITARY_RE.search(text):
        text = MILITARY_RE.sub("[MILITARY]", text)
        redactions.append("military status")
    if DEMOGRAPHIC_RE.search(text):
        text = DEMOGRAPHIC_RE.sub("[DEMOGRAPHIC]", text)
        redactions.append("demographics")
    return text, redactions


def anonymize_contact(contact: Contact) -> Contact:
    """Blank every contact field — name/contact never leaves for LLM calls."""
    return Contact(location=contact.location)


if __name__ == "__main__":
    sample = ("Jane Doe, jane@x.com, (512) 555-0134, veteran, married, "
              "linkedin.com/in/jane. Python expert.")
    clean, redactions = anonymize_text(sample)
    print(redactions)
    print(clean)
