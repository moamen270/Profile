"""The Universal Pipeline (research 'Bottom Line'):

    Hard filters -> Parse -> Normalize -> Match -> Score/Rank -> Human review

Design notes from the research:
  - Knockout form questions are the ONLY auto-reject path (never resume text).
  - Parse failures surface as warnings (image PDFs, 2-column, tables...).
  - Normalization maps variations to canonical entities before matching.
  - Matching runs the full sophistication spectrum in parallel.
  - All 14 factors contribute to the weighted composite.
  - Every output format is produced (%, tier, grade, stars, criteria, narrative).
  - AI is advisory only: undecided criteria route to human review.
"""
from __future__ import annotations

from pathlib import Path

from .compliance.anonymizer import anonymize_text
from .compliance.human_review_router import route_candidate
from .compliance.protected_attribute_guard import compliance_summary, flags_from_findings, scan_jd
from .factors.career_trajectory import career_trajectory_factor
from .factors.certification_match import certification_match_factor
from .factors.education_match import education_match_factor
from .factors.evidence_verified_skills import evidence_verified_factor
from .factors.industry_alignment import industry_alignment_factor
from .factors.location_match import location_match_factor
from .factors.section_placement import section_placement_factor
from .factors.skill_overlap import skill_overlap_factor
from .factors.title_match import title_match_factor
from .factors.years_experience import years_experience_factor
from .hard_filters.location_filter import location_filter
from .hard_filters.min_years_form import min_years_form_filter
from .hard_filters.salary_ceiling import parse_salary, salary_ceiling_filter
from .hard_filters.work_authorization import work_authorization_filter
from .llm_client import LLMClient
from .matching.boolean_search import evaluate as boolean_evaluate
from .matching.co_attention import co_attention_similarity
from .matching.embedding_match import SemanticMatcher
from .matching.exact_match import exact_score
from .matching.fuzzy_match import fuzzy_score
from .matching.graph_fusion import graph_fusion_score
from .matching.llm_qualification import evaluate_qualifications, summarize as summarize_criteria
from .matching.ontology_match import ontology_match
from .matching.relationship_clusters import cluster_overlap
from .matching.stemmer import stem_score
from .matching.weighted_keywords import extract_keywords, weighted_score
from .models import (
    AnalysisReport,
    CandidateRecord,
    FactorResult,
    FilterResult,
    JobDescription,
    MatchResult,
    ParsedResume,
    ScoreResult,
)
from .normalization.relationship_inference import infer_relationships
from .normalization.taxonomy import SkillsTaxonomy
from .normalization.unique_concepts import detect_stuffing
from .parsing.certifications_extractor import extract_certifications
from .parsing.contact_extractor import extract_contact
from .parsing.docx_extractor import extract_docx
from .parsing.education_extractor import extract_education
from .parsing.experience_extractor import extract_experiences
from .parsing.jd_parser import parse_job_description
from .parsing.layout_diagnostics import diagnose
from .parsing.ocr_extractor import ocr_pdf
from .parsing.pdf_extractor import extract_pdf
from .parsing.section_detector import detect_sections
from .parsing.skills_extractor import skill_locations as compute_skill_locations
from .parsing.txt_extractor import extract_txt
from .scoring.criteria_met import criteria_met
from .scoring.fit_gap_report import fit_narrative
from .scoring.letter_grades import letter_grade
from .scoring.score_combiner import combine, composite_percentage
from .scoring.star_rating import oracle_stars
from .scoring.tier_classifier import classify_tier

# default factor weights (documented, tunable)
FACTOR_WEIGHTS = {
    "skill_overlap": 3.0,
    "evidence_verified_skills": 2.0,
    "years_experience": 2.0,
    "title_match": 2.0,
    "education_match": 1.0,
    "certification_match": 1.0,
    "location_match": 1.0,
    "industry_alignment": 0.5,
    "career_trajectory": 1.0,
    "section_placement": 0.5,
}


def _to_bool(value) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


class ATSPipeline:
    """End-to-end ATS engine. Optional LLM enriches qualification evaluation."""

    def __init__(self, llm: LLMClient | None = None, taxonomy_path=None) -> None:
        self.llm = llm if llm is not None else LLMClient()
        self.taxonomy = SkillsTaxonomy(taxonomy_path)
        self.semantic = SemanticMatcher()

    # ------------------------------------------------------------- stage 1
    def run_hard_filters(self, jd: JobDescription, form_answers: dict | None) -> list[FilterResult]:
        """Stage 1: knockout form questions — the only auto-reject path."""
        answers = form_answers or {}
        results: list[FilterResult] = []

        if "work_authorization" in answers:
            results.append(work_authorization_filter(_to_bool(answers.get("work_authorization"))))
        if "min_years" in answers:
            results.append(min_years_form_filter(answers.get("min_years"), jd.min_years))
        if "salary_expectation" in answers:
            lo, hi = parse_salary(str(answers["salary_expectation"]))
            results.append(salary_ceiling_filter(lo or hi, jd.salary_ceiling))
        if "location" in answers:
            results.append(
                location_filter(
                    [str(answers["location"])],
                    [jd.location] if jd.location else None,
                    remote_ok=jd.remote_allowed,
                    willing_to_relocate=_to_bool(answers.get("willing_to_relocate")),
                )
            )
        return results

    # ------------------------------------------------------------- stage 2
    def parse_resume(self, path: str | Path) -> ParsedResume:
        """Stage 2: extract text (PDF/DOCX/TXT, OCR fallback) and structure it."""
        path = Path(path)
        parsed = ParsedResume(source_file=str(path))

        suffix = path.suffix.lower()
        if suffix == ".pdf":
            extraction = extract_pdf(path)
            text = extraction.text
            warnings = list(extraction.warnings)
            if not text.strip() and path.exists():
                ocr = ocr_pdf_fallback(str(path))
                if ocr.ok:
                    text = ocr.text
                    warnings.append("recovered via OCR")
            if extraction.words and extraction.page_sizes:
                width, height = extraction.page_sizes[0]
                parsed.layout = diagnose(extraction.words, width, height)
                warnings.extend(parsed.layout.notes)
            if path.exists():
                from .parsing.design_tool_detector import inspect_pdf

                design = inspect_pdf(path)
                warnings.extend(design.notes)
        elif suffix == ".docx":
            extraction = extract_docx(path)
            text, warnings = extraction.text, list(extraction.warnings)
        else:
            extraction = extract_txt(path)
            text, warnings = extraction.text, list(extraction.warnings)

        parsed.raw_text = text
        parsed.warnings = warnings

        sections, unknown_headers = detect_sections(text.splitlines())
        parsed.sections = sections
        if unknown_headers:
            parsed.warnings.append(
                "Unrecognized section headers (content may be misrouted): "
                + ", ".join(unknown_headers[:5])
            )

        parsed.contact = extract_contact(text)
        parsed.experiences = extract_experiences(text, sections.get("experience"))
        parsed.education = extract_education(text, sections.get("education"))
        from .parsing.certifications_extractor import extract_certifications

        parsed.certifications = extract_certifications(text)

        all_found, locations = compute_skill_locations(text, sections, self.taxonomy.variation_map)
        parsed.skills = all_found
        parsed.skill_locations = locations
        if not text.strip():
            parsed.warnings.append("Empty document after extraction — many ATS silently drop it")
        return parsed

    # ------------------------------------------------------------- stage 3
    def normalize(self, parsed: ParsedResume) -> tuple[set[str], dict[str, list[str]]]:
        """Stage 3: canonical entities + canonical-keyed skill locations."""
        canonical = self.taxonomy.normalize_set(parsed.skills)
        locations: dict[str, list[str]] = {}
        for raw_skill, found_in in parsed.skill_locations.items():
            canon = self.taxonomy.canonical(raw_skill) or raw_skill
            bucket = locations.setdefault(canon, [])
            for loc in found_in:
                if loc not in bucket:
                    bucket.append(loc)
        return canonical, locations

    # ------------------------------------------------------------- stage 4
    def run_matchers(self, parsed: ParsedResume, jd: JobDescription) -> dict[str, MatchResult]:
        text = parsed.raw_text
        all_jd_skills = jd.required_skills | jd.preferred_skills
        matchers: dict[str, MatchResult] = {}

        matchers["exact"] = exact_score(all_jd_skills, text)
        matchers["stemming"] = stem_score(all_jd_skills, text)
        matchers["fuzzy"] = fuzzy_score(all_jd_skills, text)

        from .matching.weighted_keywords import extract_keywords, weighted_score

        jd_keywords = extract_keywords(jd.raw_text)
        matchers["weighted_keywords"] = weighted_score(jd_keywords, text)

        matchers["ontology"] = ontology_match(parsed.skills, jd.required_skills, jd.preferred_skills, self.taxonomy)
        matchers["semantic_embedding"] = self.semantic.compare(text, jd.raw_text)
        matchers["relationship_clusters"] = cluster_overlap(parsed.skills, all_jd_skills, self.taxonomy)
        matchers["co_attention"] = MatchResult(
            technique="co_attention",
            score=co_attention_similarity(jd.raw_text, text),
            notes="simplified co-attention alignment (APJFNN/PJFCANN-inspired)",
        )
        matchers["graph_fusion"] = graph_fusion_score(parsed.skills, all_jd_skills, self.taxonomy)

        if jd.qualifications:
            from .matching.cross_encoder import CrossEncoderReranker

            matchers["cross_encoder"] = CrossEncoderReranker(self.semantic).rerank(jd, text)

        if jd.qualifications:
            first_qualification = jd.qualifications[0].text
            matchers["boolean"] = MatchResult(
                technique="boolean",
                score=1.0 if boolean_evaluate(f'"{first_qualification}"', text) else 0.0,
                notes="quoted-phrase boolean over first extracted qualification",
            )
        return matchers

    def compute_factors(
        self, parsed: ParsedResume, jd: JobDescription, skill_locations: dict[str, list[str]]
    ) -> list[FactorResult]:
        weights = FACTOR_WEIGHTS
        factors: list[FactorResult] = [
            skill_overlap_factor(parsed.skills, jd.required_skills, jd.preferred_skills, weights["skill_overlap"]),
            evidence_verified_factor(parsed, jd.required_skills | jd.preferred_skills, weights["evidence_verified_skills"]),
            years_experience_factor(parsed, jd.min_years, weights["years_experience"]),
            title_match_factor([e.title for e in parsed.experiences if e.title], jd.title, weights["title_match"]),
            education_match_factor(parsed, jd, weights["education_match"]),
            certification_match_factor(parsed, jd.raw_text, weights["certification_match"]),
            location_match_factor(parsed, jd, weights["location_match"]),
            industry_alignment_factor(parsed.raw_text, jd, weights["industry_alignment"]),
            career_trajectory_factor(parsed, weights["career_trajectory"]),
            section_placement_factor(skill_locations, weights["section_placement"]),
        ]
        return [f for f in factors if f is not None]

    # ------------------------------------------------------------- full run
    def analyze(
        self,
        resume_path: str | Path,
        jd: JobDescription,
        form_answers: dict | None = None,
        candidate: CandidateRecord | None = None,
        anonymize_llm: bool = True,
    ) -> AnalysisReport:
        """One candidate through the complete universal pipeline."""
        report = AnalysisReport(candidate=candidate)

        # stage 1: hard filters — the ONLY auto-reject path
        report.knockout = self.run_hard_filters(jd, form_answers)
        report.auto_rejected = any(not r.passed and r.category == "knockout" for r in report.knockout)
        if report.auto_rejected:
            report.route = "rejected"
            return report

        # stage 2: parse
        parsed = self.parse_resume(resume_path)
        report.parse_warnings = list(parsed.warnings)

        # stage 3: normalize
        canonical_skills, skill_locations = self.normalize(parsed)
        report.normalized_skills = canonical_skills
        from .normalization.relationship_inference import infer_relationships

        report.inferred_capabilities = infer_relationships(canonical_skills, self.taxonomy)

        # stuffing detection (spam signal, section 3)
        stuffing = detect_stuffing(parsed.raw_text, list(canonical_skills))
        report.stuffing_hits = stuffing

        # bias guardrails (section 8): protected-attribute proxies in the JD
        guard_findings = scan_jd(jd)
        report.compliance["protected_attribute_guard"] = compliance_summary(guard_findings)

        # stage 4: match
        report.matchers = self.run_matchers(parsed, jd)

        # qualification evaluation (LLM if available, anonymized per Lever practice)
        llm = self.llm
        report.compliance["anonymized_for_llm"] = bool(anonymize_llm)
        if anonymize_llm and llm and llm.available:
            clean_text, _redactions = anonymize_text(parsed.raw_text)
            criteria = evaluate_qualifications(jd, clean_text, llm)
        else:
            criteria = evaluate_qualifications(jd, parsed.raw_text, llm)
        if not criteria:
            # The JD yielded no qualifications at all: usually a job description
            # pasted as prose with no bullet glyphs, which extract_qualifications
            # cannot see. Say so loudly rather than reporting a confident 0-of-0.
            report.parse_warnings.append(
                "No qualifications parsed from the job description — it has no "
                "bullet/numbered list items. Criteria counts and the fit badge "
                "are not meaningful; re-run with the JD's requirements as a "
                "bulleted list."
            )
        report.scores.criteria = summarize_criteria(criteria)

        # stage 5: score & rank outputs
        report.factors = self.compute_factors(parsed, jd, skill_locations)
        stuffing_penalty = min(0.2, 0.05 * len(stuffing))
        match_c, factor_c = combine(report.matchers, report.factors, stuffing_penalty)
        report.scores.match_composite = match_c
        report.scores.factor_composite = factor_c
        report.scores.percentage = composite_percentage(match_c, factor_c)
        report.scores.tier = classify_tier(report.scores.percentage / 100.0)
        report.scores.grade = letter_grade(
            report.scores.criteria.basic_met,
            report.scores.criteria.basic_total,
            report.scores.criteria.preferred_met,
            report.scores.criteria.preferred_total,
        )
        report.scores.stars = oracle_stars(
            {
                "skill_overlap": _factor_score(report.factors, "skill_overlap"),
                "education_match": _factor_score(report.factors, "education_match"),
                "years_experience": _factor_score(report.factors, "years_experience"),
                "profile": match_c,
            }
        )
        report.fit_gap = fit_narrative(report.factors, criteria)

        # stage 6: route (AI advisory only; undecided -> human review)
        criteria_summary = criteria_met(criteria)
        report.scores.criteria = criteria_summary
        undecided_ratio = criteria_summary.undecided / (criteria_summary.total or 1)
        report.route = route_candidate(knockout_failed=False, undecided_ratio=undecided_ratio)
        report.scores.flags = [f"stuffing: {t} x{c}" for t, c in stuffing]
        report.scores.flags.extend(flags_from_findings(guard_findings))

        # recommendations layer: every stage contributes actionable advice
        from .recommendations import collect as collect_recommendations

        report.recommendations = collect_recommendations(report)
        return report

    def rank_pool(
        self,
        candidates: list[CandidateRecord],
        jd: JobDescription,
        resumes_dir: str | Path | None = None,
    ) -> list:
        """Stack-rank a candidate pool (SuccessFactors style)."""
        from .scoring.stack_rank import rank_pool

        def score_fn(candidate: CandidateRecord) -> ScoreResult:
            path = candidate.resume_path
            if not path and resumes_dir:
                path = str(Path(resumes_dir) / f"{candidate.candidate_id}.txt")
            if not path or not Path(path).exists():
                result = ScoreResult()
                result.criteria.total = 0
                return result
            report = self.analyze(path, jd, candidate.form_answers, candidate)
            return report.scores

        return rank_pool(candidates, score_fn)


def all_jd_skills(skills: set[str]) -> set[str]:
    return skills


def ocr_pdf_fallback(path: str):
    from .parsing.ocr_extractor import ocr_pdf

    return ocr_pdf(path)


def _factor_score(factors: list[FactorResult], name: str) -> float:
    for factor in factors:
        if factor.name == name:
            return factor.score
    return 0.0


if __name__ == "__main__":
    print("ATSPipeline ready. Use cli.py for the command-line interface.")
