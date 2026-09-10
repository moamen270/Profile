"""Section 4 — matching technique tests."""
from __future__ import annotations

from ats.matching.boolean_search import evaluate, matched_terms
from ats.matching.embedding_match import SemanticMatcher
from ats.matching.exact_match import exact_score
from ats.matching.fuzzy_match import fuzzy_score, levenshtein
from ats.matching.llm_qualification import (
    evaluate_qualification,
    extract_qualifications,
    summarize,
)
from ats.matching.ontology_match import ontology_match
from ats.matching.relationship_clusters import cluster_overlap
from ats.matching.stemmer import stem, stem_score
from ats.matching.weighted_keywords import extract_keywords, weighted_score
from ats.models import Qualification


class TestExact:
    def test_literal(self):
        result = exact_score(["project manager", "agile"], "agile project manager")
        assert result.score == 1.0

    def test_no_inflection(self):
        assert exact_score(["project management"], "I was a project manager").score == 0.0


class TestBoolean:
    def test_and(self):
        assert evaluate("python AND sql", "knows python and sql")

    def test_or(self):
        assert evaluate("python OR java", "knows java")

    def test_not(self):
        assert not evaluate("python NOT marketer", "python marketer")

    def test_parens(self):
        assert evaluate('(python OR java) AND docker', "java docker dev")
        assert not evaluate('(python OR java) AND docker', "java dev")


class TestStemming:
    def test_collaborate_family(self):
        from ats.matching.stemmer import stems_related

        assert stems_related("collaborated", "collaboration")
        assert stems_related("collaborate", "collaboration")

    def test_inflections_match(self):
        assert stem_score(["manage"], "I managed teams and led projects").score >= 0.5


class TestFuzzy:
    def test_levenshtein(self):
        assert levenshtein("kitten", "sitting") == 3
        assert levenshtein("same", "same") == 0

    def test_typo_tolerance(self):
        result = fuzzy_score(["javascript"], "experienced with Javsacript")
        assert result.score == 1.0


class TestWeighted:
    def test_required_boosted(self):
        jd = "REQUIREMENTS\n- python expert\n\nNICE TO HAVE\n- kafka"
        keywords = extract_keywords(jd)
        assert keywords["python"] > keywords["kafka"]

    def test_score(self):
        jd = "REQUIREMENTS\n- python\n- sql\n- docker"
        keywords = extract_keywords(jd)
        result = weighted_score(keywords, "python sql docker developer")
        assert result.score > 0.5


class TestOntology:
    def test_entity_match(self):
        result = ontology_match(
            resume_skills={"ReactJS", "k8s"},
            jd_required={"react", "kubernetes"},
        )
        assert result.score >= 0.8


class TestClusters:
    def test_cluster_credit(self):
        result = cluster_overlap(
            resume_skills={"docker", "kubernetes", "terraform"},
            jd_skills={"docker", "kubernetes"},
        )
        assert result.score > 0.3


class TestLLMQualification:
    def test_extraction(self):
        jd_text = "REQUIREMENTS\n- 5+ years of experience\n- Strong Python skills"
        quals = extract_qualifications(jd_text)
        assert len(quals) == 2
        assert all(q.kind == "basic" for q in quals)

    def test_deterministic_evaluation(self):
        qual = Qualification(text="Strong Python skills", kind="basic")
        result = evaluate_qualification(qual, "I am a python expert with 5 years.")
        assert result.status == "met"
        assert result.evidence

    def test_undecided_without_evidence(self):
        qual = Qualification(text="Fluent in Japanese language", kind="basic")
        result = evaluate_qualification(qual, "Python developer.")
        assert result.status == "undecided"

    def test_summary_counts(self):
        quals = [
            Qualification(text="python skills here", kind="basic"),
            Qualification(text="aws experience here", kind="preferred"),
            Qualification(text="unknown language xq", kind="basic"),
        ]
        resume = "python skills here and aws experience here"
        results = [evaluate_qualification(q, resume) for q in quals]
        summary = summarize(results)
        assert summary.met == 2
        assert summary.undecided == 1
        assert summary.preferred_met == 1


class TestEmbedding:
    def test_related_higher_than_unrelated(self):
        matcher = SemanticMatcherSafe()
        related = matcher.similarity(
            "backend engineer with python docker kubernetes",
            "we need a python backend engineer with kubernetes",
        )
        unrelated = matcher.similarity(
            "backend engineer with python docker kubernetes",
            "hospital nurse night shifts",
        )
        assert related > unrelated


def SemanticMatcherSafe():
    from ats.matching.embedding_match import SemanticMatcher

    return SemanticMatcher()
