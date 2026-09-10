"""Section 7 — Gamified psychometrics (pymetrics-style).

Research: "neuroscience games -> cognitive/emotional trait scores matched to a
company's top performers." Requires game/survey responses; this module scores
them deterministically against a top-performer trait benchmark.

API:
    trait_scores(responses: dict[trait, 0..9]) -> {trait: 0..1}
    match_score(scores, benchmark) -> (match 0..1, per-trait deltas)
    psychometric_assessment(responses, benchmark) -> dict  # traits, match, band
"""
from __future__ import annotations

# game/likert responses arrive on 0..9 scales; pymetrics traits are 0..1
RESPONSE_SCALE = 9.0

DEFAULT_BENCHMARK = {
    "attention": 0.8, "memory": 0.7, "risk_tolerance": 0.6, "learning": 0.9,
    "emotion_regulation": 0.75, "focus": 0.8,
}


def _norm_score(value) -> float:
    """0..9 raw response -> 0..1 trait score (0.5 for missing/invalid)."""
    try:
        return max(0.0, min(1.0, float(value) / RESPONSE_SCALE))
    except (TypeError, ValueError):
        return 0.5


def trait_scores(responses: dict) -> dict[str, float]:
    """Normalize raw game/likert responses into 0..1 trait scores."""
    return {trait: _norm_score(value) for trait, value in (responses or {}).items()}


def match_score(
    scores: dict[str, float], benchmark: dict[str, float]
) -> tuple[float, dict[str, float]]:
    """1 - mean absolute deviation from the top-performer profile (0..1)."""
    if not benchmark:
        return 0.0, {}
    deltas = {}
    for trait, target in benchmark.items():
        candidate_value = scores.get(trait, 0.5)
        deltas[trait] = round(candidate_value - target, 3)
    distance = sum(abs(delta) for delta in deltas.values()) / len(deltas)
    return round(max(0.0, 1.0 - distance), 4), deltas


def psychometric_band(match: float) -> str:
    if match >= 0.75:
        return "strong_fit"
    if match >= 0.5:
        return "moderate_fit"
    return "low_fit"


def psychometric_assessment(
    responses: dict, benchmark: dict[str, float] | None = None
) -> dict:
    """Full pymetrics-style output: trait scores, benchmark match, band."""
    benchmark = benchmark or dict(DEFAULT_BENCHMARK)
    scores = trait_scores(responses)
    match, deltas = match_score(scores, benchmark)
    return {
        "trait_scores": scores,
        "benchmark": benchmark,
        "match": match,
        "deltas": deltas,
        "band": psychometric_band(match),
        "note": "pymetrics pattern: game-derived traits matched to top-performer profile",
    }


if __name__ == "__main__":
    responses = {
        "attention": 8, "memory": 6, "risk_tolerance": 7,
        "learning": 8, "emotion_regulation": 7, "focus": 8,
    }
    result = psychometric_assessment(responses)
    print(result["match"], result["band"])
