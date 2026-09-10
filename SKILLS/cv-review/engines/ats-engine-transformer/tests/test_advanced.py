"""§4 academic models + §2 design-tool + §7 adjacent + §8 guard tests."""
from __future__ import annotations

from ats.adjacent.psychometrics import psychometric_assessment, psychometric_band
from ats.adjacent.sourcing_rank import rank_candidates
from ats.adjacent.video_interview import band_for, interview_assessment
from ats.compliance.protected_attribute_guard import compliance_summary, scan_jd, scan_text
from ats.matching.co_attention import co_attention_similarity
from ats.matching.cross_encoder import CrossEncoderReranker
from ats.matching.embedding_match import SemanticMatcher
from ats.matching.graph_fusion import graph_fusion_score
from ats.matching.learning_to_rank import LTRanker
from ats.models import CandidateRecord
from ats.parsing.design_tool_detector import inspect_pdf
from ats.parsing.jd_parser import parse_job_description


class TestCrossEncoder:
    def test_good_beats_bad(self):
        jd = parse_job_description("REQUIREMENTS\n- Strong Python and SQL skills\n- Kubernetes operations")
        reranker = CrossEncoderReranker(SemanticMatcher())
        good = reranker.rerank(jd, "Expert in python and sql databases.\nManaged kubernetes clusters in production.")
        bad = reranker.rerank(jd, "Ballet dancer and pastry chef.")
        assert good.score > bad.score


class TestCoAttention:
    def test_related_beats_unrelated(self):
        a = "We need a senior backend engineer with Python, Docker and Kubernetes"
        related = co_attention_similarity(a, "Senior engineer building Python services on kubernetes and docker")
        unrelated = co_attention_similarity(a, "Hospital seeking registered nurses for night shifts")
        assert related > unrelated

    def test_alignment_matrix(self):
        from ats.matching.co_attention import attention_matrix

        matrix = attention_matrix("python engineer with docker", "docker and python developer")
        assert any(any(row.values()) for row in matrix.values())


class TestGraphFusion:
    def test_related_skills_propagate(self):
        from ats.normalization.taxonomy import SkillsTaxonomy

        tax = SkillsTaxonomy()
        good = graph_fusion_score({"docker", "kubernetes", "terraform"}, {"docker", "kubernetes", "aws"}, tax)
        weak = graph_fusion_score({"baking", "painting"}, {"docker", "kubernetes", "aws"}, tax)
        assert good.score > weak.score
        assert weak.score == 0.0


class TestLTR:
    def test_learns_separable_data(self):
        ranker = LTRanker()
        ranker.fit([[0.9], [0.8], [0.1], [0.2]], [1, 1, 0, 0])
        assert ranker.score([0.9]) > ranker.score([0.1])

    def test_ranking(self):
        ranker = LTRanker()
        ranker.fit([[0.9], [0.1]], [1, 0])
        ranked = ranker.rank([("low", [0.2]), ("high", [0.85])])
        assert ranked[0][0] == "high"

    def test_untrained_neutral(self):
        assert LTRanker().score([0.9]) == 0.5


class TestVideoInterview:
    def test_band_ordering(self):
        assert band_for(0.8) == "Top"
        assert band_for(0.4) == "Middle"
        assert band_for(0.1) == "Bottom"

    def test_strong_transcript(self):
        transcript = (
            "Our situation was that checkout latency spiked. I owned the task of "
            "isolating the root cause. I debugged the cache layer, reduced latency "
            "by 40%, and shipped the fix with my team. I presented the results."
        )
        assessment = interview_assessment(transcript)
        assert assessment["band"] in {"Top", "Middle"}
        assert all(0 <= score <= 1 for score in assessment["competencies"].values())


class TestPsychometrics:
    def test_match_and_band(self):
        responses = {
            "attention": 8, "memory": 6, "risk_tolerance": 7,
            "learning": 8, "emotion_regulation": 7, "focus": 8,
        }
        result = psychometric_assessment(responses)
        assert 0 <= result["match"] <= 1
        assert result["band"] in {"strong_fit", "moderate_fit", "low_fit"}

    def test_off_profile_scores_lower(self):
        close = psychometric_assessment({"attention": 8, "learning": 8, "focus": 8})
        far = psychometric_assessment({"attention": 1, "learning": 1, "focus": 1})
        assert close["match"] > far["match"]


class TestSourcing:
    def test_personalized_ranking(self):
        candidates = [
            CandidateRecord("c1", "Py Dev", meta={"skills": ["python", "sql", "docker"], "top_applicant": True}),
            CandidateRecord("c2", "Designer", meta={"skills": ["figma", "ux"]}),
        ]
        ranked = rank_candidates(candidates, {"python", "sql"}, {"team_skills": ["python", "docker"]}, [{"skills": ["python"]}])
        assert ranked[0]["candidate"] == "Py Dev"
        assert ranked[0]["relevance"] > ranked[1]["relevance"]
        assert ranked[0]["spotlight"] and not ranked[1]["spotlight"]


class TestDesignToolDetector:
    def test_missing_file_graceful(self):
        report = inspect_pdf("definitely_missing.pdf")
        assert report.design_tool is None
        assert any("failed" in note for note in report.notes)

    def test_non_pdf_graceful(self):
        report = inspect_pdf("samples/resumes/jane_doe_backend.txt")
        assert report.design_tool is None


class TestProtectedAttributeGuard:
    def test_blocks_disability_proxies(self):
        jd = parse_job_description("REQUIREMENTS\n- Must be able-bodied and healthy")
        findings = guard_scan_safe(jd)
        summary = compliance_summary(findings)
        assert not summary["passed"]
        assert summary["blocks"] >= 2

    def test_warns_on_age_proxies(self):
        jd = parse_job_description("REQUIREMENTS\n- Digital native with modern skills")
        findings = guard_scan_safe(jd)
        assert any(f.category == "age" and f.severity == "warn" for f in findings)

    def test_clean_jd_passes(self):
        jd = parse_job_description("REQUIREMENTS\n- Strong python skills")
        assert compliance_summary(guard_scan_safe(jd))["passed"]


def guard_scan_safe(jd):
    from ats.compliance.protected_attribute_guard import scan_jd

    return scan_jd(jd)
