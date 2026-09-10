"""Section 5 — scoring output format tests."""
from __future__ import annotations

from ats.models import (
    CandidateRecord,
    CriterionResult,
    FactorResult,
    MatchResult,
    Qualification,
    ScoreResult,
)
from ats.scoring.criteria_met import criteria_met_summary
from ats.scoring.fit_gap_report import fit_badge, fit_narrative
from ats.scoring.letter_grades import letter_grade
from ats.scoring.percentage_score import ace_from_factors, ace_tier, meets_asset_threshold
from ats.scoring.score_combiner import combine, composite_percentage
from ats.scoring.stack_rank import rank_pool, stack_rank
from ats.scoring.star_rating import oracle_stars, stars_for
from ats.scoring.tier_classifier import classify_tier
from ats.models import CandidateRecord


class TestAce:
    def test_percentage(self):
        factors = [FactorResult("a", 0.9, 3.0), FactorResult("b", 0.5, 1.0)]
        result = ace_from_factors(factors)
        assert result["percentage"] == 80.0  # (0.9*3 + 0.5*1) / 4 = 0.8
        assert result["tier"] == "ACE candidate"

    def test_tiers(self):
        assert ace_tier(80) == "ACE candidate"
        assert ace_tier(60) == "minimally qualified"
        assert ace_tier(20) == "other"

    def test_asset_threshold(self):
        assert meets_asset_threshold(3, 5)
        assert not meets_asset_threshold(2, 5)


class TestTiers:
    def test_boundaries(self):
        from ats.scoring.tier_classifier import classify_tier

        assert classify_tier(0.85) == "Strong"
        assert classify_tier(0.65) == "Good"
        assert classify_tier(0.45) == "Partial"
        assert classify_tier(0.25) == "Limited"
        assert classify_tier(0.1) == "Needs manual review"


class TestGrades:
    def test_workday_rules(self):
        assert letter_grade(4, 4, 3, 3) == "A"
        assert letter_grade(4, 4, 0, 3) == "B"
        assert letter_grade(3, 4) == "C"
        assert letter_grade(1, 4) == "D"


class TestCriteriaMet:
    def test_label(self):
        quals = [
            Qualification("5 years", "basic"),
            Qualification("python", "basic"),
            Qualification("aws", "preferred"),
        ]
        results = [
            CriterionResult(quals[0], "met"),
            CriterionResult(quals[1], "not_met"),
            CriterionResult(quals[2], "met"),
        ]
        summary = criteria_met_summary(results)
        assert summary["label"] == "Meets 2 of 3"
        assert summary["not_met"] == 1


class TestStars:
    def test_oracle(self):
        from ats.scoring.star_rating import oracle_stars

        stars = oracle_stars({"skill_overlap": 0.9, "education_match": 0.5, "years_experience": 0.0})
        assert stars["Skills"] == 3
        assert stars["Experience"] == 0
        assert len(stars) == 4


class TestStackRank:
    def test_order_and_tiebreak(self):
        candidates = [
            CandidateRecord("c2", "Bob"),
            CandidateRecord("c1", "Ann"),
            CandidateRecord("c3", "Cid"),
        ]
        scores = {"c1": 90.0, "c2": 80.0, "c3": 80.0}
        ranked = stack_rank([(c, scores[c.candidate_id]) for c in candidates])
        assert ranked[0][1].candidate_id == "c1"
        assert ranked[1][1].candidate_id == "c2"  # tie broken by id
        assert [rank for rank, _ in ranked] == [1, 2, 3]

    def test_rank_pool(self):
        candidates = [CandidateRecord("c1", "Ann"), CandidateRecord("c2", "Bob")]

        def score_fn(candidate):
            result = ScoreResult()
            result.percentage = {"c1": 50.0, "c2": 70.0}[candidate.candidate_id]
            return result

        ranked = rank_pool(candidates, score_fn)
        assert ranked[0].candidate.candidate_id == "c2"


class TestCombiner:
    def test_blend(self):
        matchers = {"exact": MatchResult("exact", 0.8), "ontology": MatchResult("ontology", 0.6)}
        factors = [FactorResult("skill_overlap", 0.8, 3.0)]
        match_c, factor_c = combine(matchers, factors)
        assert match_c == 0.7
        assert factor_c == 0.8
        assert composite_percentage(0.7, 0.8) == round(100 * (0.55 * 0.7 + 0.45 * 0.8), 1)

    def test_stuffing_penalty(self):
        matchers = {"keyword_stuffing": MatchResult("keyword_stuffing", 1.0)}
        factors = [FactorResult("skill_overlap", 0.8, 3.0)]
        _m, factor_c = combine(matchers, factors, stuffing_penalty=0.1)
        assert factor_c == 0.7


class TestFitGap:
    def test_badge(self):
        factors = [FactorResult("skill", 0.9, 3.0)]
        assert fit_badge(factors) == "TALENT FIT"
        assert fit_narrative(factors)["badge"] == "TALENT FIT"

    def test_narrative_lists_weak(self):
        factors = [FactorResult("weak", 0.2, 1.0)]
        narrative = fit_narrative(factors)
        assert any("weak" in area for area in narrative["areas_for_clarification"])
