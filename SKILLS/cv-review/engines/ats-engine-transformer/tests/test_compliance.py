"""Sections 7/8 + human review — adjacent, compliance, review queue tests."""
from __future__ import annotations

from ats.adjacent.chatbot_prescreen import ChatbotPrescreen
from ats.adjacent.rediscovery import silver_medalists
from ats.adjacent.skills_assessment import assessment_gate, score_assessment
from ats.compliance.anonymizer import anonymize_contact, anonymize_text
from ats.compliance.bias_audit import bias_audit, disparate_impact_ratio, selection_rates
from ats.compliance.human_review_router import NEEDS_MANUAL_REVIEW, human_review_queue, route_candidate
from ats.models import CandidateRecord, Contact


class TestRediscovery:
    def test_silver_medalists(self):
        pool = [
            CandidateRecord("c1", "Ann", meta={"previous_stage": "offer"}),
            CandidateRecord("c2", "Bob", meta={"previous_stage": "phone_screen"}),
        ]
        names = [c.name for c in silver_medalists(pool)]
        assert names == ["Ann"]


class TestAssessment:
    def test_scoring(self):
        key = {"q1": "b", "q2": "a", "q3": "c", "q4": "d"}
        answers = {"q1": "b", "q2": "A", "q3": "x", "q4": "d"}
        result = score_assessment(answers, key, pass_threshold=0.7)
        assert result["correct"] == 3
        assert result["score"] == 75.0
        assert result["passed"]

    def test_gate(self):
        assert assessment_gate({"passed": True}) == "advance"
        assert assessment_gate({"passed": False}) == "stage_reject"


class TestChatbot:
    def test_flow(self):
        questions = [
            {"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"},
        ]
        bot = ChatbotPrescreen(questions)
        assert bot.next_question() is not None
        bot.submit(True)
        assert bot.next_question() is None
        assert not bot.auto_rejected()

    def test_rejection(self):
        questions = [{"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"}]
        bot = ChatbotPrescreen(questions)
        bot.next_question()
        bot.submit(False)
        assert bot.auto_rejected()


class TestAnonymizer:
    def test_strips_pii(self):
        text = "Jane Doe jane@x.com (512) 555-0134 veteran married python"
        clean, redactions = anonymize_text(text)
        assert "jane@x.com" not in clean
        assert "555" not in clean
        assert "veteran" not in clean and "married" not in clean
        assert "python" in clean
        assert set(redactions) >= {"email", "phone", "military status", "demographics"}

    def test_contact(self):
        blank = anonymize_contact(Contact(name="X", email="x@x.com", phone="123"))
        assert blank.name is None and blank.email is None and blank.phone is None


class TestBiasAudit:
    def test_four_fifths(self):
        outcomes = {
            "group_a": [True] * 8 + [False] * 2,   # 80%
            "group_b": [True] * 4 + [False] * 6,   # 20%
        }
        audit = bias_audit(outcomes)
        assert not audit["passed"]
        assert "group_b" in audit["flagged_groups"]

    def test_pass(self):
        outcomes = {"a": [True, False], "b": [True, False]}
        assert bias_audit(outcomes)["passed"]

    def test_rates(self):
        rates = selection_rates({"a": [True, True, False], "b": [True, False, False]})
        assert disparate_impact_ratio(rates) == 0.5


class TestRouter:
    def test_only_knockouts_reject(self):
        assert route_candidate(knockout_failed=True) == "rejected"
        assert route_candidate(knockout_failed=False, undecided_ratio=0.9) == NEEDS_MANUAL_REVIEW
        assert route_candidate(knockout_failed=False, undecided_ratio=0.1) == "review"
        assert route_candidate(knockout_failed=False, opted_out=True) == NEEDS_MANUAL_REVIEW

    def test_queue_split(self):
        from ats.models import RankedCandidate, ScoreResult

        entries = [
            RankedCandidateLite(1, "review"),
            RankedCandidateLite(2, NEEDS_MANUAL_REVIEW),
        ]
        queue = human_review_queue(entries)
        assert len(queue["review"]) == 1
        assert len(queue[NEEDS_MANUAL_REVIEW]) == 1


class RankedCandidateLite:
    """Minimal stand-in satisfying review_queue's attribute access."""

    def __init__(self, rank, route):
        self.rank = rank
        self.route = route
