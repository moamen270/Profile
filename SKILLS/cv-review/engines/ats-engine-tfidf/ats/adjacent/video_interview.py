"""Section 7 — HireVue-style video interview scoring.

Research: "transcribes answers, NLP maps text to competency models trained by
IO psychologists; bands candidates Top/Middle/Bottom; bottom third often never
watched; human scorecard uses BARS — measures communication, problem-solving,
teamwork, drive, conscientiousness."

Deterministic competency scoring over an interview transcript (the video part
is upstream speech-to-text). Anchors follow BARS behavior-evidence style.

API:
    competency_scores(transcript, competencies=None) -> {name: 0..1}
    band_for(average) -> "Top"|"Middle"|"Bottom"
    interview_assessment(transcript) -> dict  # competencies, average, band
"""
from __future__ import annotations

import re

# BARS-style anchors: competency -> behavior evidence phrases
DEFAULT_COMPETENCIES: dict[str, list[str]] = {
    "communication": ["explained", "clarified", "presented", "articulated", "summarized"],
    "problem_solving": ["broke down", "analyzed", "root cause", "trade-off", "hypothesis",
                        "debug", "isolated", "approach", "solution"],
    "teamwork": ["team", "collaborated", "together", "paired", "supported",
                 "coordinated", "feedback"],
    "drive": ["initiative", "ownership", "shipped", "delivered", "deadline", "persisted",
              "volunteered", "self-taught"],
}

_STAR_WORDS = ["situation", "task", "action", "result"]
_METRIC_RE = re.compile(r"\d+%|\$\d|\b\d+x\b|\b\d+\s*(?:hours|days|weeks|months|users|customers)\b", re.I)


def star_structure_score(transcript_lower: str) -> float:
    """STAR coverage: >=2 of Situation/Task/Action/Result mentioned."""
    count = sum(1 for word in _STAR_WORDS if word in transcript_lower)
    return min(1.0, count / 2.0)


def competency_score(name: str, anchors: list[str], transcript: str) -> float:
    """One competency scored 0..1: anchor hits + answer depth + metrics + STAR."""
    text = transcript or ""
    lower = text.lower()

    anchor_hits = sum(1 for anchor in anchors if anchor in lower)
    anchor_component = min(1.0, 0.25 * anchor_hits)

    sentences = [s for s in re.split(r"[.!?\n]+", text) if s.strip()]
    depth_component = min(1.0, len(sentences) / 8.0)

    metric_count = len(_METRIC_RE.findall(text))
    metric_component = min(1.0, 0.25 * metric_count)

    star_component = star_structure_score(lower)

    score = (
        0.35 * anchor_component
        + 0.25 * depth_component
        + 0.2 * metric_component
        + 0.2 * star_component
    )
    return round(score, 4)


def competency_scores(
    transcript: str, competencies: dict[str, list[str]] | None = None
) -> dict[str, float]:
    """All competency scores from a transcript."""
    competencies = competencies or DEFAULT_COMPETENCIES
    return {
        name: competency_score(name, anchors, transcript)
        for name, anchors in competencies.items()
    }


def band_for(average: float) -> str:
    """HireVue bands: Top/Middle/Bottom (bottom third often never watched)."""
    if average >= 0.6:
        return "Top"
    if average >= 0.3:
        return "Middle"
    return "Bottom"


def interview_assessment(
    transcript: str, competencies: dict[str, list[str]] | None = None
) -> dict:
    """Full HireVue-style output: competency scores + Top/Middle/Bottom band."""
    competencies = competencies or DEFAULT_COMPETENCIES
    scores = {
        name: competency_score(name, anchors, transcript)
        for name, anchors in competencies.items()
    }
    average = sum(scores.values()) / len(scores) if scores else 0.0
    return {
        "competencies": scores,
        "average": round(average, 4),
        "band": band_for(average),
        "note": "HireVue pattern: transcript competency mapping, BARS anchors, human scorecard",
        "transcript_chars": len(transcript or ""),
    }


if __name__ == "__main__":
    transcript = (
        "Our situation was that checkout latency spiked. I owned the task of isolating "
        "the root cause. I debugged the cache layer, reduced latency by 40%, and shipped "
        "the fix with my team. I presented the results to leadership."
    )
    assessment = interview_assessment(transcript)
    print(assessment["band"], assessment["competencies"])
