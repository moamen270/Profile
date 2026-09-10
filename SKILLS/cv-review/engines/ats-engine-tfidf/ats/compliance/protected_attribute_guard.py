"""Section 8 — Protected-attribute proxy guardrails (Greenhouse practice).

Research: "Greenhouse blocks adding protected attributes as criteria and warns
when a skill is a proxy for one" (NYC LL144 / AEDT, EEOC context).

Scans JD text and qualification criteria for protected attributes and their
common proxies (age proxies, family-status proxies, disability proxies,
gendered wording, national-origin proxies), returning findings with severity.
Findings are advisory: they surface in the compliance block and flags, never
silently altering scores.

API:
    scan_text(text, context) -> list[Finding]
    scan_jd(jd) -> list[Finding]     # raw text + each qualification criterion
    compliance_summary(findings) -> dict
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ..models import JobDescription


@dataclass
class Finding:
    term: str
    category: str      # age | family | disability | gender | national_origin
    severity: str      # block | warn
    context: str
    note: str


# (regex, category, severity, note) — common protected-attribute proxies
PROXIES: list[tuple[re.Pattern, str, str, str]] = [
    (re.compile(r"\b(?:digital native|recent graduate|young|energetic|fresh out of|millennial|gen\s?z)\b", re.I),
     "age", "warn", "Age proxy — ADEA risk; use skill-based wording"),
    (re.compile(r"\b(?:native english|perfect english|no accent|english native speaker|native language)\b", re.I),
     "national_origin", "warn", "National-origin proxy"),
    (re.compile(r"\b(?:family oriented|marriage|children|kids|maternity|paternity)\b", re.I),
     "family", "block", "Family-status proxy — protected category"),
    (re.compile(r"\b(?:able[- ]bodied|no disabilities|healthy|physically fit|non[- ]disabled)\b", re.I),
     "disability", "block", "Disability proxy — ADA/EEOC risk"),
    (re.compile(r"\b(?:he will|she will|his role|her role|waitress|salesman|chairman)\b", re.I),
     "gender", "warn", "Gendered wording — use neutral terms"),
    (re.compile(r"\byears['’]?\s+experience\s*(?:max|maximum|or less)\b", re.I),
     "age", "warn", "Age proxy via experience ceiling"),
]


def _snippet(text: str, start: int, end: int) -> str:
    return " ".join(text[max(0, start - 30):min(len(text), end + 30)].split())


def scan_text(text: str, context: str = "jd") -> list[Finding]:
    """Scan one text blob for protected-attribute proxies."""
    findings: list[Finding] = []
    for regex, category, severity, note in PROXIES:
        for match in regex.finditer(text or ""):
            findings.append(
                Finding(
                    term=match.group(0).lower(),
                    category=category,
                    severity=severity,
                    context=f"{context}: ...{_snippet(text, match.start(), match.end())}...",
                    note=note,
                )
            )
    return findings


def scan_jd(jd: JobDescription) -> list[Finding]:
    """Scan the JD raw text plus every extracted qualification criterion."""
    findings = scan_text(jd.raw_text, context="jd")
    for qualification in jd.qualifications:
        findings.extend(scan_text(qualification.text, context="qualification"))
    return findings


def compliance_summary(findings: list[Finding]) -> dict:
    """Advisory summary for the pipeline compliance block."""
    return {
        "findings": [
            {"term": f.term, "category": f.category, "severity": f.severity,
             "context": f.context, "note": f.note}
            for f in findings
        ],
        "blocks": sum(1 for f in findings if f.severity == "block"),
        "warnings": sum(1 for f in findings if f.severity == "warn"),
        "passed": not any(f.severity == "block" for f in findings),
        "note": "AEDT/LL144: protected attributes (or proxies) must not be ranking criteria",
    }


def flags_from_findings(findings: list[Finding]) -> list[str]:
    return [
        f"bias-guard[{f.severity}] {f.term} ({f.category})"
        for f in findings
    ]


if __name__ == "__main__":
    jd_text = """
REQUIREMENTS
- Digital native with 5 years experience
- Able-bodied and healthy
- He will lead the team
"""
    parsed = __import__("ats.parsing.jd_parser", fromlist=["parse_job_description"]).parse_job_description(jd_text)
    found = scan_jd(parsed)
    for finding in found:
        print(f"[{finding.severity}] {finding.term} ({finding.category})")
