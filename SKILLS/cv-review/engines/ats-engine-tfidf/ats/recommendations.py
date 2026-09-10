"""Actionable recommendations layer — one generator per concern.

Every stage contributes recommendations alongside its scores:
  - knockout results -> recruiter-side guidance (the only reject path)
  - parse warnings   -> resume-format fixes (candidate)
  - stuffing hits    -> de-duplication advice (candidate)
  - matchers         -> missing keywords + semantic/requirement alignment
  - factors          -> per-factor improvement advice
  - criteria results -> clarify/address unmet & undecided qualifications

Priority: high = score < 0.4 or knockout/bias-block; medium = < 0.65;
low = nice-to-have. Item shape: {source, priority, audience, text}.
"""
from __future__ import annotations

_FACTOR_HIGH = 0.4
_FACTOR_MED = 0.65
_MAX_KEYWORDS = 12


def _rec(source: str, priority: str, audience: str, text: str) -> dict:
    return {"source": source, "priority": priority, "audience": audience, "text": text}


# --------------------------------------------------------------- parse stage
def from_parse_warnings(warnings: list[str]) -> list[dict]:
    recs: list[dict] = []
    for warning in warnings or []:
        lower = warning.lower()
        if "no extractable text" in lower or "ocr" in lower or "scanned" in lower:
            recs.append(_rec("parsing", "high", "candidate",
                "Document has no machine-readable text (image-only/scanned). Re-export as a "
                "text-based PDF — many ATS reject or silently drop image-only resumes."))
        elif "two-column" in lower:
            recs.append(_rec("parsing", "high", "candidate",
                "Rebuild the resume as a single-column layout — two-column layouts garble "
                "in most ATS parsers."))
        elif "unrecognized section headers" in lower:
            recs.append(_rec("parsing", "medium", "candidate",
                "Rename non-standard section headings to standard ones (e.g. 'My Journey' -> "
                "'Work Experience', 'Tech Stack' -> 'Skills') — misrouted content "
                "weakens matching."))
        elif "header" in lower or "footer" in lower:
            recs.append(_rec("parsing", "medium", "candidate",
                "Move text out of the page header/footer — many parsers skip it entirely."))
        elif "table" in lower:
            recs.append(_rec("parsing", "medium", "candidate",
                "Replace tables with plain text lists — tables scramble chronology and "
                "company associations in ATS parsers."))
        elif "tiny font" in lower:
            recs.append(_rec("parsing", "low", "candidate",
                "Increase font size to >=10pt — small fonts degrade parsing accuracy."))
        elif "produced with" in lower:
            recs.append(_rec("parsing", "high", "candidate",
                "Re-export the resume from the design tool as a text-based PDF (avoid "
                "Canva/Illustrator graphical layers) or rebuild in a plain editor."))
        elif "embedded images" in lower:
            recs.append(_rec("parsing", "medium", "candidate",
                "Remove graphics/skill bars/photos — ATS parsers only read text."))
        elif "empty document" in lower:
            recs.append(_rec("parsing", "high", "recruiter",
                "Empty extraction — verify the file manually; the ATS would show nothing."))
    return recs


# --------------------------------------------------------------- match stage
def from_matchers(matchers: dict) -> list[dict]:
    recs: list[dict] = []
    seen: set[str] = set()

    exact = matchers.get("exact")
    if exact is not None and exact.missing:
        for term in exact.missing[:_MAX_KEYWORDS]:
            if str(term) not in seen:
                seen.add(str(term))
                priority = "high" if len(exact.missing) <= 4 else "medium"
                recs.append(_rec("matcher:exact", priority, "candidate",
                    f"Add '{term}' to the resume (skills section AND an experience "
                    "bullet) if truthful."))

    semantic = matchers.get("semantic_embedding")
    if semantic is not None and semantic.score < 0.45:
        recs.append(_rec("semantic_embedding", "high", "candidate",
            "Rewrite the summary/experience language toward the job description's "
            "vocabulary — semantic similarity is low, meaning wording diverges even "
            "when concepts may overlap."))

    cross = matchers.get("cross_encoder")
    if cross is not None and cross.score < 0.45:
        recs.append(_rec("cross_encoder", "medium", "candidate",
            "No resume sentence strongly matches individual JD qualifications — address "
            "each requirement with a dedicated achievement line."))

    return recs


def from_stuffing(stuffing_hits: list[tuple[str, int]]) -> list[dict]:
    return [
        _rec("keyword_stuffing", "high", "candidate",
             f"'{term}' appears {count} times — modern ATS count unique concepts, not "
             "frequency; repetition can trigger spam detection. Reduce to natural usage.")
        for term, count in stuffing_hits or []
    ]


# -------------------------------------------------------------- factor stage
def _factor_priority(score: float) -> str:
    if score < _FACTOR_HIGH:
        return "high"
    if score < _FACTOR_MED:
        return "medium"
    return "low"


def from_factors(factors: list) -> list[dict]:
    """Per-factor advice: explicit recommendation field first, then evidence."""
    items: list[dict] = []
    for factor in factors or []:
        rec_text = getattr(factor, "recommendation", "") or ""
        if rec_text:
            items.append(_rec(factor.name, _factor_priority(factor.score), "candidate", rec_text))
        else:
            items.extend(_factor_advice(factor))
    return items


def _factor_advice(factor) -> list[dict]:
    """Derive recommendations from a factor's evidence when no explicit hint."""
    recs: list[dict] = []
    evidence = factor.evidence or {}
    name = factor.name

    if name == "skill_overlap":
        missing = evidence.get("required_missing") or []
        for skill in missing:
            recs.append(_rec(name, "high" if len(missing) <= 3 else "medium", "candidate",
                f"Required skill '{skill}' is missing — add it to skills and evidence it "
                "in an experience bullet with a measurable outcome (if truthful)."))
    elif name == "evidence_verified_skills":
        for skill in evidence.get("listed_only") or []:
            recs.append(_rec(name, "medium", "candidate",
                f"'{skill}' appears only in the skills list — demonstrate it in an "
                "experience bullet with a measurable outcome (Ashby/iCIMS factor)."))
    elif name == "years_experience":
        min_years = evidence.get("jd_min_years")
        years = evidence.get("calculated_years") or 0
        if min_years and years < min_years:
            recs.append(_rec(name, "high", "candidate",
                "Calculated experience is below the JD minimum — front-load total relevant "
                "years in the summary; the application form answer is what screens "
                "(declare honestly)."))
    elif name == "title_match":
        recs.append(_rec(name, "medium", "candidate",
            "Include the target job title (if truthful) in your headline or most recent "
            "role header — title match carries heavy structural weight."))
    elif name == "education_match":
        if evidence.get("required"):
            recs.append(_rec(name, "medium", "candidate",
                "State the degree, field, and institution explicitly in the Education "
                "section; if below the requirement, expect recruiter judgment."))
    elif name == "certification_match":
        for acronym in evidence.get("missing") or []:
            recs.append(_rec(name, "medium", "candidate",
                f"Required certification missing: {acronym}. Obtain it or list the full "
                "form + acronym when earned."))
    elif name == "location_match":
        recs.append(_rec(name, "low", "candidate",
            "State your city/region clearly and relocation willingness — location and "
            "authorization are knockout questions in real ATS."))
    elif name == "career_trajectory":
        if "gap" in factor.detail:
            recs.append(_rec(name, "medium", "candidate",
                "Employment gap detected — add a one-line context (education, contract, "
                "career break) so parsers don't infer instability."))
        if "job-hopping" in factor.detail:
            recs.append(_rec(name, "medium", "candidate",
                "Multiple short tenures — emphasize contract/project nature of roles if applicable."))
    elif name == "section_placement":
        recs.append(_rec(name, "medium", "candidate",
            "Move the most relevant keywords into the Skills and Summary sections near "
            "the top — legacy ATS weight placement."))
    elif name == "industry_alignment":
        recs.append(_rec(name, "low", "candidate",
            "Add industry-specific accomplishments/terminology from the target domain."))
    return recs


# ------------------------------------------------------- qualification stage
def from_criteria(criteria) -> list[dict]:
    recs: list[dict] = []
    for result in getattr(criteria, "results", []) or []:
        text = result.qualification.text
        if result.status == "undecided":
            recs.append(_rec("criteria", "high", "candidate",
                f"Cannot verify: '{text[:80]}' — add explicit evidence (dates, tools, "
                "outcomes) so the system can adjudicate; otherwise a recruiter reviews."))
        elif result.status == "not_met":
            recs.append(_rec("criteria", "medium", "candidate",
                f"Not met: '{text[:80]}' — address it or prepare a clarification for the "
                "recruiter conversation."))
    return recs


# ------------------------------------------------------------------ pipeline
def collect(report) -> list[dict]:
    """Aggregate every stage's recommendations into one prioritized list."""
    guard_summary = (report.compliance or {}).get("protected_attribute_guard", {})
    items: list[dict] = []
    items.extend(from_knockout(report.knockout, report.auto_rejected))
    items.extend(from_parse_warnings(report.parse_warnings))
    items.extend(from_stuffing(report.stuffing_hits))
    items.extend(from_matchers(report.matchers))
    items.extend(from_factors(report.factors))
    items.extend(from_criteria(report.scores.criteria))
    items.extend(from_bias_guard(guard_summary))
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(items, key=lambda r: order.get(r["priority"], 3))


def from_knockout(knockout_results: list, auto_rejected: bool) -> list[dict]:
    if not auto_rejected:
        return []
    return [
        _rec("knockout", "high", "recruiter",
             f"Auto-reject on '{result.name}': {result.reason} (form-based knockout — the "
             "only legitimate auto-rejection path; verify question legality under "
             "LL144/AEDT before deploying).")
        for result in knockout_results or []
        if not result.passed and result.category == "knockout"
    ]


def from_bias_guard(guard_summary: dict) -> list[dict]:
    return [
        _rec("bias_guard", "high" if finding["severity"] == "block" else "medium", "recruiter",
             f"JD wording risk: '{finding['term']}' ({finding['category']}) — {finding['note']}")
        for finding in (guard_summary or {}).get("findings", [])
    ]
