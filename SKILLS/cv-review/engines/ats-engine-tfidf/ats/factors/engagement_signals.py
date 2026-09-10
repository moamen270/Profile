"""Section 6.12 — Engagement signals (Phenom).

Research: "Phenom: email opens, chatbot interaction." Requires a tracking
system feeding candidate events; this module defines the scoring interface and
computes from event counts when provided.

API:
    engagement_factor(events: dict[str, int]) -> FactorResult | None
"""
from __future__ import annotations

from ..models import FactorResult

# event name -> value weight
EVENT_WEIGHTS = {
    "email_open": 0.15,
    "email_click": 0.3,
    "chatbot_message": 0.25,
    "job_view": 0.1,
    "event_attend": 0.35,
    "sms_reply": 0.25,
}

_MAX_SCORE = 1.0


def engagement_factor(events: dict[str, int] | None, weight: float = 0.3) -> FactorResult | None:
    """events: {"email_open": 3, "chatbot_message": 1, ...}. None => not tracked."""
    if events is None:
        return None
    raw = 0.0
    for event, count in events.items():
        value = EVENT_WEIGHTS.get(event, 0.05)
        raw += min(value, value * _safe_count(count))
    score = min(_MAX_SCORE, raw)
    return FactorResult(
        name="engagement_signals", score=round(score, 4), weight=weight,
        evidence=dict(events),
        detail=f"Phenom-style engagement from {sum(events.values())} tracked events",
    )


def _safe_count(count) -> int:
    try:
        return max(0, int(count))
    except (TypeError, ValueError):
        return 0


if __name__ == "__main__":
    print(engagement_factor({"email_open": 2, "chatbot_message": 1}).score)
    print(engagement_factor(None))
