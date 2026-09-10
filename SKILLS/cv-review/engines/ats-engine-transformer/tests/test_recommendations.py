"""Recommendations layer — every module advises beyond the score."""
from __future__ import annotations

from ats.models import AnalysisReport, FactorResult
from ats.pipeline import ATSPipeline
from ats.parsing.jd_parser import parse_job_description
from ats.recommendations import (
    collect,
    from_criteria,
    from_factors,
    from_knockout,
    from_matchers,
    from_parse_warnings,
    from_stuffing,
)
from tests.conftest import JD_BACKEND, RESUME_BACKEND, RESUME_STUFFING


class TestParseRecs:
    def test_two_column(self):
        recs = from_parse_warnings(["Two-column layout detected — interleaved garble"])
        assert any("single-column" in r["text"] for r in recs)
        assert recs[0]["audience"] == "candidate"

    def test_design_tool(self):
        recs = from_parse_warnings(["Produced with canva — text may be stored as graphical layers"])
        assert recs[0]["priority"] == "high"

    def test_unknown_headers(self):
        recs = from_parse_warnings(["Unrecognized section headers (content may be misrouted): MY JOURNEY"])
        assert recs and "Rename" in recs[0]["text"]

    def test_empty_is_empty(self):
        assert from_parse_warnings([]) == []


class TestMatcherRecs:
    def test_missing_keywords_advised(self):
        from ats.matching.exact_match import exact_score

        result = exact_score(["docker", "kubernetes", "aws"], "python developer")
        recs = from_matchers({"exact": result})
        assert any("docker" in r["text"] for r in recs)

    def test_low_semantic_advised(self):
        from ats.models import MatchResult

        recs = from_matchers({"semantic_embedding": MatchResult("semantic_embedding", 0.2)})
        assert any("semantic" in r["text"] for r in recs)


class TestStuffingRecs:
    def test_dedupe_advice(self):
        recs = from_stuffing([("python", 10)])
        assert recs[0]["priority"] == "high"
        assert "python" in recs[0]["text"]


class TestFactorRecs:
    def test_skill_overlap_missing(self):
        from ats.factors.skill_overlap import skill_overlap_factor

        factor = skill_overlap_factor({"python"}, {"python", "kubernetes", "docker"})
        recs = from_factors([factor])
        assert any("kubernetes" in r["text"] for r in recs)

    def test_cert_missing(self):
        from ats.factors.certification_match import certification_match_factor
        from ats.models import ParsedResume

        factor = certification_match_factor(ParsedResume(raw_text="no certs"), "Requires PMP")
        recs = from_factors([factor])
        assert any("PMP" in r["text"] for r in recs)

    def test_strong_factor_advises_nothing(self):
        from ats.factors.skill_overlap import skill_overlap_factor

        factor = skill_overlap_factor({"python", "docker"}, {"python", "docker"})
        assert from_factors([factor]) == []


class TestCriteriaRecs:
    def test_undecided_advised(self):
        from ats.models import CriterionResult, CriterionSummary, Qualification

        summary = CriterionSummary(results=[
            CriterionResult(Qualification("Fluent Japanese"), "undecided"),
        ])
        recs = from_criteria(summary)
        assert any("Cannot verify" in r["text"] for r in recs)


class TestKnockoutRecs:
    def test_recruiter_guidance(self):
        from ats.models import FilterResult

        results = [FilterResult("work_authorization", False, "Not authorized", "knockout")]
        recs = from_knockout(results, auto_rejected=True)
        assert recs and recs[0]["audience"] == "recruiter"
        assert recs[0]["priority"] == "high"


class TestCollect:
    def test_full_report_sorted(self):
        report = AnalysisReport()
        report.parse_warnings = ["Two-column layout detected"]
        report.stuffing_hits = [("python", 10)]
        report.recommendations = collect(report)
        assert report.recommendations[0]["priority"] in {"high", "medium", "low"}

    def test_pipeline_produces_recommendations(self):
        from ats.llm_client import LLMClient
        from ats.pipeline import ATSPipeline
        from ats.parsing.jd_parser import parse_job_description
        from tests.conftest import JD_BACKEND

        pipeline = ATSPipeline(LLMClient(api_key=None))
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        result = pipeline.analyze(RESUME_STUFFING, jd)
        assert result.recommendations, "stuffing resume must generate advice"
        assert any(r["source"] == "keyword_stuffing" for r in result.recommendations)
        # high priority first
        priorities = [r["priority"] for r in report_recs(result)]
        assert priorities == sorted(priorities, key={"high": 0, "medium": 1, "low": 2}.get)

    def test_clean_profile_few_recommendations(self):
        from ats.llm_client import LLMClient
        from ats.pipeline import ATSPipeline
        from tests.conftest import JD_BACKEND, RESUME_BACKEND

        pipeline = ATSPipeline(LLMClient(api_key=None))
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(RESUME_BACKEND, jd)
        high_recs = [r for r in report.recommendations if r["priority"] == "high"]
        assert len(high_recs) <= 4  # strong match -> few high-priority advice items


def report_recs(report):
    return [r for r in report.recommendations]
