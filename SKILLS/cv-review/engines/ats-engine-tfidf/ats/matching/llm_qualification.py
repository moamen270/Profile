"""Section 4 — LLM qualification evaluation (Workday 'Fit & Gap' / Lever 'Talent Fit' / Ashby).

Research: "Extract each basic/preferred qualification from JD and evaluate
individually against parsed CV, with natural-language explanations" and
"Ashby (up to 50 criteria, Meets/Does Not Meet/Undecided + evidence citations)".

Behavior without an API key (deterministic mode):
  - qualification extraction still works (regex/heuristics)
  - each criterion gets keyword/stem/fuzzy evidence search; a hit => "met"
    with the matching sentence as citation; no hit => "undecided" (never a
    fabricated rejection) and the candidate routes to human review — the exact
    opt-out behavior real systems implement for legal safety (section 8).

API:
    extract_qualifications(jd_text) -> list[Qualification]
    evaluate_qualification(qual, resume_text, llm=None) -> CriterionResult
    evaluate_qualifications(jd, resume_text, llm=None) -> list[CriterionResult]
    summarize(results) -> CriterionSummary
"""
from __future__ import annotations

import re

from ..llm_client import LLMClient
from ..matching.fuzzy_match import fuzzy_match
from ..matching.stemmer import stem_match
from ..models import CriterionResult, CriterionSummary, JobDescription, Qualification
from ..parsing.jd_parser import extract_qualifications as _jd_extract

_LLM_SYSTEM = (
    "You are an ATS qualification evaluator. For the given qualification and "
    "resume, answer with JSON: {\"status\": \"met|not_met|undecided\", "
    "\"evidence\": \"exact quote from the resume supporting the decision\"}. "
    "Be strict: only use evidence present in the resume."
)


def extract_qualifications(jd_text: str) -> list[Qualification]:
    """Public re-export of the JD qualification extractor."""
    return _jd_extract(jd_text)


GENERIC_WORDS = {
    "strong", "skills", "skill", "experience", "experienced", "fluent",
    "proficient", "ability", "knowledge", "working", "familiarity", "plus",
    "good", "excellent", "deep", "understanding", "degree", "years",
    "professional", "related", "field", "required", "preferred", "certification",
}


def qual_keywords(text: str) -> set[str]:
    """Significant words of a criterion (generic descriptors excluded)."""
    return {
        w.lower()
        for w in re.findall(r"[a-zA-Z]{3,}", text)
        if w.lower() not in GENERIC_WORDS
    }


def best_citation(qualification_text: str, resume_text: str) -> str:
    """Best resume sentence evidencing the qualification (keyword overlap)."""
    keywords = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", qualification_text)}
    best_sentence, best_overlap = "", 0
    for sentence in re.split(r"[.\n]", resume_text):
        words = {w.lower() for w in re.findall(r"[a-zA-Z]{3,}", sentence)}
        overlap = len(words & keywords)
        if overlap > best_overlap:
            best_overlap, best_sentence = overlap, sentence.strip()
    return best_sentence.strip()[:400]


def evaluate_qualification(
    qualification: Qualification, resume_text: str, llm: LLMClient | None = None
) -> CriterionResult:
    """One qualification -> met / not_met / undecided with evidence.

    With an available LLM client the model classifies strictly with a quote;
    otherwise a deterministic keyword/stem/fuzzy search decides, and absence
    of evidence yields "undecided" (never a fabricated rejection).
    """
    if llm is not None and getattr(llm, "available", False):
        response = llm.chat_json(
            _LLM_SYSTEM,
            f"Qualification: {qualification.text}\n\nResume:\n{resume_text[:6000]}",
        )
        if isinstance(response, dict) and response.get("status") in {"met", "not_met", "undecided"}:
            return CriterionResult(
                qualification=qualification,
                status=str(response["status"]),
                evidence=str(response.get("evidence", ""))[:400],
                method="llm",
            )

    keywords = list(qual_keywords(qualification.text))[:8]
    hits = sum(
        1
        for word in keywords
        if stem_match(word, resume_text) or fuzzy_match(word, resume_text, max_distance=1)
    )
    # Require majority coverage of the criterion's words — a single incidental
    # word match ("certification" in a section header) must not fabricate a "met".
    if keywords and hits / len(keywords) >= 0.5:
        return CriterionResult(
            qualification=qualification, status="met",
            evidence=best_citation(qualification.text, resume_text)[:400],
            method="heuristic",
        )
    return CriterionResult(qualification=qualification, status="undecided", method="heuristic")


def evaluate_qualifications(
    jd: JobDescription, resume_text: str, llm: LLMClient | None = None
) -> list[CriterionResult]:
    quals = jd.qualifications or _jd_extract(jd.raw_text)
    return [evaluate_qualification(q, resume_text, llm) for q in quals]


def summarize(results: list[CriterionResult]) -> CriterionSummary:
    """Aggregate criteria into Ashby-style 'Meets X of Y' counts."""
    summary = CriterionSummary(results=list(results), total=len(results))
    for result in results:
        if result.qualification.kind == "basic":
            summary.basic_total += 1
        else:
            summary.preferred_total += 1
        if result.status == "met":
            summary.met += 1
            if result.qualification.kind == "basic":
                summary.basic_met += 1
            else:
                summary.preferred_met += 1
        elif result.status == "undecided":
            summary.undecided += 1
    return summary


if __name__ == "__main__":
    jd_text = """
Requirements:
- 5+ years of professional software engineering experience
- Strong Python and SQL skills
- Experience with Docker and Kubernetes
"""
    quals = extract_qualifications(jd_text)
    resume = "I have 7 years of experience with Python, SQL, Docker and Kubernetes."
    for qual in quals[:3]:
        result = evaluate_qualification(qual, resume)
        print(qual.kind, "|", result.status, "|", result.evidence[:80])
