"""End-to-end universal pipeline tests."""
from __future__ import annotations

from ats.llm_client import LLMClient
from ats.models import CandidateRecord
from ats.pipeline import ATSPipeline
from ats.parsing.jd_parser import parse_job_description
from tests.conftest import (
    JD_BACKEND,
    JD_MARKETING,
    RESUME_BACKEND,
    RESUME_MARKETING,
    RESUME_STUFFING,
    SAMPLES,
)


def make_pipeline() -> ATSPipeline:
    llm = LLMClient(api_key=None)  # deterministic mode
    assert not llm.available
    return ATSPipeline(llm)


class TestFullPipeline:
    def test_backend_resume_vs_backend_jd(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(RESUME_BACKEND, jd)

        assert not report.auto_rejected
        assert not report.parse_warnings or all("OCR" not in w for w in report.parse_warnings)
        assert {"python", "docker", "kubernetes"} <= report.normalized_skills
        assert "cloud infrastructure capability" in report.inferred_capabilities
        assert len(report.matchers) >= 7
        assert len(report.factors) == 10
        assert 0 <= report.scores.percentage <= 100
        assert report.scores.tier
        assert report.scores.grade in {"A", "B", "C", "D"}
        assert report.scores.criteria.total >= 8
        assert report.route == "review"

    def test_marketing_resume_ranks_below_backend(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        backend_report = pipeline.analyze(RESUME_BACKEND, jd)
        marketing_report = pipeline.analyze(RESUME_MARKETING, jd)
        assert backend_report.scores.percentage > marketing_report.scores.percentage + 15

    def test_keyword_stuffer_penalized(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(RESUME_STUFFING, jd)
        assert report.stuffing_hits, "python repeated >=8 times should be detected"
        assert any(flag.startswith("stuffing") for flag in report.scores.flags)
        assert report.scores.percentage < 60

    def test_knockout_rejection_short_circuits(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(
            RESUME_BACKEND, jd, form_answers={"work_authorization": False}
        )
        assert report.auto_rejected
        assert report.route == "rejected"
        assert not report.matchers  # pipeline stopped before parsing

    def test_passing_answers_continue(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(
            RESUME_BACKEND,
            jd,
            form_answers={"work_authorization": True, "min_years": "7", "salary_expectation": "140k"},
        )
        assert not report.auto_rejected
        assert report.route in {"review", NEEDS_MANUAL := "needs_manual_review"}

    def test_undecided_criteria_route_manual(self):
        pipeline = make_pipeline()
        jd = parse_job_description(
            "REQUIREMENTS\n- Fluent in Swahili and Japanese\n- Quantum computing certification"
        )
        report = pipeline.analyze(RESUME_BACKEND, jd)
        # criteria with no evidence stay undecided -> human review (section 8)
        assert report.route == "needs_manual_review"


class TestPoolRanking:
    def test_stack_rank_pool(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        candidates = [
            CandidateRecord("jane_doe_backend", "Jane", resume_path=str(RESUME_BACKEND)),
            CandidateRecord("bob_smith_marketing", "Bob", resume_path=str(RESUME_MARKETING)),
            CandidateRecord("stuffy_stuffing", "Stuffy", resume_path=str(RESUME_STUFFING)),
        ]
        ranked = pipeline.rank_pool(candidates, jd)
        assert ranked[0].candidate.candidate_id == "jane_doe_backend"
        assert ranked[0].rank == 1
        percentages = [entry.score.percentage for entry in ranked]
        assert percentages == sorted(percentages, reverse=True)


class TestOutputFormats:
    def test_every_format_populated(self):
        pipeline = make_pipeline()
        jd = parse_job_description(JD_BACKEND.read_text(encoding="utf-8"))
        report = pipeline.analyze(RESUME_BACKEND, jd)
        scores = report.scores
        assert scores.percentage > 0                     # Taleo ACE %
        assert scores.tier in {"Strong", "Good", "Partial", "Limited", "Needs manual review"}
        assert scores.grade in {"A", "B", "C", "D"}      # Workday letters
        assert set(scores.stars) == {"Profile", "Education", "Experience", "Skills"}  # Oracle
        assert scores.criteria.total > 0                 # Ashby criteria
        assert "badge" in report.fit_gap                 # Lever narrative


NEEDS_MANUAL = "needs_manual_review"
