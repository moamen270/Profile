"""Section 1 — hard filter tests."""
from __future__ import annotations

from ats.hard_filters.knockout_questions import evaluate_knockout, is_auto_rejected, run_knockouts
from ats.hard_filters.location_filter import location_filter
from ats.hard_filters.min_years_form import min_years_form_filter
from ats.hard_filters.salary_ceiling import parse_salary, salary_ceiling_filter
from ats.hard_filters.work_authorization import work_authorization_filter


class TestKnockouts:
    def test_yes_no_pass(self):
        q = {"id": "auth", "type": "yes_no", "pass_values": [True]}
        assert evaluate_knockout(q, True).passed

    def test_yes_no_fail_is_knockout(self):
        q = {"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"}
        result = evaluate_knockout(q, False)
        assert not result.passed
        assert is_auto_rejected([result])

    def test_missing_answer_fails(self):
        q = {"id": "auth", "type": "yes_no", "pass_values": [True]}
        assert not evaluate_knockout(q, None).passed

    def test_number_range(self):
        q = {"id": "yrs", "type": "number", "min": 3}
        assert evaluate_knockout(q, 5).passed
        assert not evaluate_knockout(q, 2).passed

    def test_number_with_k_suffix(self):
        q = {"id": "salary", "type": "number", "max": 150000}
        assert evaluate_knockout(q, "140k").passed
        assert not evaluate_knockout(q, "200k").passed

    def test_single_select(self):
        q = {"id": "days", "type": "single_select", "pass_values": ["3", "4", "5"]}
        assert evaluate_knockout(q, "3").passed
        assert not evaluate_knockout(q, "1").passed

    def test_multi_select(self):
        q = {"id": "langs", "type": "multi_select", "pass_values": ["python"], "require_all": True}
        assert evaluate_knockout(q, ["python", "sql"]).passed
        assert not evaluate_knockout(q, ["java"]).passed

    def test_full_questionnaire(self):
        qs = [
            {"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"},
            {"id": "days", "type": "single_select", "pass_values": ["3"], "category": "filter"},
        ]
        # failing a 'filter' category does NOT auto-reject
        results = run_knockouts(qs, {"auth": True})
        assert not is_auto_rejected(results)
        # failing a knockout does
        assert is_auto_rejected(run_knockouts(qs, {"auth": False, "days": "3"}))


class TestSalary:
    def test_parse_salary(self):
        assert parse_salary("$120,000") == (120000.0, 120000.0)
        assert parse_salary("120k") == (120000.0, 120000.0)
        assert parse_salary("80-100k") == (80000.0, 100000.0)

    def test_non_salaries_ignored(self):
        assert parse_salary("3 days onsite") == (None, None)
        assert parse_salary("5+ years") == (None, None)

    def test_ceiling_filter(self):
        assert salary_ceiling_filter(140000, 150000).passed
        assert not salary_ceiling_filter(180000, 150000).passed


class TestMinYears:
    def test_pass(self):
        assert min_years_form_filter(5, 3).passed

    def test_fail(self):
        result = min_years_form_filter(2, 3)
        assert not result.passed
        assert result.category == "knockout"

    def test_missing(self):
        assert not min_years_form_filter(None, 3).passed


class TestWorkAuth:
    def test_authorized(self):
        assert work_authorization_filter(True).passed

    def test_not_authorized_rejects(self):
        assert not work_authorization_filter(False).passed

    def test_sponsorship(self):
        assert not work_authorization_filter(True, needs_sponsorship=True).passed
        assert work_authorization_filter(True, needs_sponsorship=True, offers_sponsorship=True).passed


class TestLocation:
    def test_match(self):
        assert location_filter(["Austin, TX"], ["Austin, TX"]).passed

    def test_same_state(self):
        assert location_filter(["Dallas, TX"], ["Austin, TX"]).passed

    def test_no_match(self):
        assert not location_filter(["New York, NY"], ["Austin, TX"]).passed

    def test_relocate_ok(self):
        assert location_filter(["NY"], ["Austin"], willing_to_relocate=True).passed

    def test_remote(self):
        assert location_filter(["NY"], ["Austin"], remote_ok=True).passed
