"""Section 2/6 — Certification extraction (both acronym AND full form needed).

Research section 6: "Certifications / licenses (both acronym and full form
needed)" — legacy Taleo literally matches only what's typed, so a resume with
"CPA" fails a JD requiring "Certified Public Accountant" unless normalized.

API:
    extract_certifications(text) -> list[Certification]
"""
from __future__ import annotations

import re

from ..models import Certification

# acronym -> full forms (either counts as the cert being present)
CERTS: dict[str, list[str]] = {
    "PMP": ["project management professional"],
    "CPA": ["certified public accountant"],
    "CFA": ["chartered financial analyst"],
    "CISA": ["certified information systems auditor"],
    "CISSP": ["certified information systems security professional"],
    "CCNA": ["cisco certified network associate"],
    "AWS SAA": ["aws certified solutions architect"],
    "AWS CDA": ["aws certified developer"],
    "CKA": ["certified kubernetes administrator"],
    "SHRM-CP": ["society for human resource management certified professional"],
    "PMP": [],
}

_CERT_TOKEN = re.compile(
    r"\b(pmp|cpa|cfa|cisa|cissp|ccna|cka|shrm-cp)\b"
    r"|\b(aws certified solutions architect"
    r"|aws certified developer"
    r"|certified kubernetes administrator"
    r"|project management professional"
    r"|certified public accountant"
    r"|chartered financial analyst"
    r"|certified information systems auditor"
    r"|certified information systems security professional"
    r"|cisco certified network associate"
    r"|shrm certified professional)",
    re.IGNORECASE,
)


def extract_certifications(text: str) -> list[Certification]:
    """Scan text for certification mentions, resolving acronym <-> full form."""
    found: dict[str, Certification] = {}
    for match in _CERT_TOKEN.finditer(text):
        token = match.group(0)
        canonical = _canonical_for(token)
        entry = found.setdefault(
            canonical, Certification(name=CERT_FULL_NAMES[canonical], acronym=canonical)
        )
        entry.raw = token
    return list(found.values())


CERT_FULL_NAMES = {
    "PMP": "Project Management Professional",
    "CPA": "Certified Public Accountant",
    "CFA": "Chartered Financial Analyst",
    "CISA": "Certified Information Systems Auditor",
    "CISSP": "Certified Information Systems Security Professional",
    "CCNA": "Cisco Certified Network Associate",
    "AWS SAA": "AWS Certified Solutions Architect",
    "AWS CDA": "AWS Certified Developer",
    "CKA": "Certified Kubernetes Administrator",
    "SHRM-CP": "SHRM Certified Professional",
}


def _canonical_for(token: str) -> str:
    upper = token.upper().strip()
    for acronym, full in CERT_FULL_NAMES.items():
        if upper == acronym or upper.startswith(full.upper()[:12]):
            return acronym
    return token.upper()


if __name__ == "__main__":
    sample = "Credentials: PMP, Certified Public Accountant, and working toward CKA."
    for cert in extract_certifications(sample):
        print(cert.acronym, "=", cert.name)
