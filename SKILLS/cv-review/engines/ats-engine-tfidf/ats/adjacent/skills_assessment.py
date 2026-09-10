"""Section 7 — Coding / skills assessments as a pipeline stage.

Research: "scored tests integrated as pipeline stages" (HackerRank/Codility
style). Deterministic quiz scoring; questions come from the adjacent quiz
generator or any external assessment export.

API:
    score_assessment(answers: dict[qid, answer], key: dict[qid, answer]) -> dict
    assessment_factor(score_result) -> FactorResult-like dict
"""
from __future__ import annotations


def score_assessment(answers: dict, key: dict, pass_threshold: float = 0.7) -> dict:
    """Grade submitted answers against an answer key (exact match)."""
    total = len(key)
    if not total:
        return {"score": 0.0, "correct": 0, "total": 0, "passed": False}
    correct = sum(1 for qid, answer in key.items() if _norm(answers.get(qid)) == _norm(answer))
    ratio = correct / total
    return {
        "score": round(ratio * 100.0, 1),
        "correct": correct,
        "total": total,
        "passed": ratio >= pass_threshold,
    }


def _norm(value) -> str:
    return str(value).strip().lower()


def assessment_gate(score_result: dict) -> str:
    """Assessment as a pipeline stage: pass -> advance, fail -> stage reject."""
    if score_result.get("passed"):
        return "advance"
    return "stage_reject"


if __name__ == "__main__":
    key = {"q1": "b", "q2": "a", "q3": "c", "q4": "d"}
    answers = {"q1": "b", "q2": "A", "q3": "b", "q4": "d"}
    print(score_assessment(answers, key))
