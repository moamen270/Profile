"""Section 1 — Knockout / disqualification questions.

Single-answer form questions; a wrong answer = instant auto-rejection.
Used by: Taleo (Disqualification Questions Library + CSW), Greenhouse
("Auto-reject" rules on Yes/No / single-select / multi-select answers),
Ashby (Global Auto-Reject Rules), Workday (prescreening questionnaires).

API:
    evaluate_knockout(question: dict, answer) -> FilterResult
    run_knockouts(questions: list[dict], answers: dict) -> list[FilterResult]
"""
from __future__ import annotations

from ..models import FilterResult


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def _to_number(answer) -> float | None:
    """Parse '120000', '120,000', '$120k', '140k', '1.2m'."""
    text = str(answer).strip().lower().replace(",", "").replace("$", "")
    multiplier = 1.0
    if text.endswith("k"):
        multiplier, text = 1_000.0, text[:-1]
    elif text.endswith("m"):
        multiplier, text = 1_000_000.0, text[:-1]
    try:
        return float(text) * multiplier
    except ValueError:
        return None


def evaluate_knockout(question: dict, answer) -> FilterResult:
    """Evaluate one form question. Never raises on bad input — a missing answer
    simply fails (conservative, mirrors real ATS behavior)."""
    qid = question.get("id", "question")
    qtype = str(question.get("type", "yes_no")).lower()
    category = question.get("category", "knockout")

    if answer is None or answer == "":
        return FilterResult(qid, False, "No answer provided (treated as fail)", category)

    if qtype == "yes_no":
        passed = _as_bool(answer) in [bool(v) for v in question.get("pass_values", [])]
        reason = "Answer accepted" if passed else f"Disqualifying answer: {answer!r}"
        return FilterResult(qid, passed, reason, category)

    if qtype == "single_select":
        passed = str(answer).strip() in [str(v) for v in question.get("pass_values", [])]
        reason = "Answer accepted" if passed else f"Disqualifying answer: {answer}"
        return FilterResult(qid, passed, reason, category)

    if qtype == "multi_select":
        selected = {str(s).strip() for s in (answer if isinstance(answer, (list, tuple, set)) else [answer])}
        pass_vals = {str(v) for v in question.get("pass_values", [])}
        if question.get("require_all"):
            passed = pass_vals.issubset(selected)
            reason = "All required selections present" if passed else "Missing required selections"
        else:
            passed = bool(selected & pass_vals)
            reason = "At least one acceptable selection" if passed else "No acceptable selection"
        return FilterResult(qid, passed, reason, category)

    if qtype == "number":
        value = _to_number(answer)
        if value is None:
            return FilterResult(qid, False, f"Non-numeric answer: {answer}", category)
        lo = question.get("min")
        hi = question.get("max")
        passed = (lo is None or value >= lo) and (hi is None or value <= hi)
        if passed:
            reason = f"{value:g} within acceptable range"
        elif hi is not None and value > hi:
            reason = f"{value:g} exceeds ceiling of {hi:g}"
        else:
            reason = f"{value:g} below required minimum of {lo:g}"
        return FilterResult(qid, passed, reason, category)

    return FilterResult(qid, True, f"Unknown question type '{qtype}' — not enforced", category)


def run_knockouts(questions: list[dict], answers: dict) -> list[FilterResult]:
    """Evaluate a full questionnaire. Any failed 'knockout' category result means
    the candidate is auto-rejected before parsing."""
    return [evaluate_knockout(q, answers.get(q.get("id"))) for q in questions]


def is_auto_rejected(results: list[FilterResult]) -> bool:
    return any(not r.passed and r.category == "knockout" for r in results)


if __name__ == "__main__":
    qs = [
        {"id": "auth", "type": "yes_no", "pass_values": [True], "category": "knockout"},
        {"id": "salary", "type": "number", "max": 120000},
        {"id": "days", "type": "single_select", "pass_values": ["3", "4", "5"]},
    ]
    answers = {"auth": True, "days": "2"}
    for r in run_knockouts(qs, answers):
        print(("PASS " if r.passed else "FAIL "), r.name, "-", r.reason)
    print("Auto-rejected:", is_auto_rejected(run_knockouts(qs, answers)))
