"""Section 3 — Unique concept counting & keyword-stuffing detection.

Research: modern systems count UNIQUE concepts, not frequency. Repetition gets
zero extra weight and can trigger spam detection (LinkedIn explicitly).

API:
    unique_concept_count(skills) -> int
    concept_frequency(text, terms) -> {term: count}
    detect_stuffing(text, terms, max_repeat=8) -> [(term, count)]
"""
from __future__ import annotations

import re

from .taxonomy import SkillsTaxonomy


def unique_concept_count(skills: set[str]) -> int:
    """Unique canonical concepts — repetition never adds weight."""
    return len({s.lower() for s in skills})


def concept_frequency(text: str, terms) -> dict[str, int]:
    lower = text.lower()
    freq: dict[str, int] = {}
    for term in terms:
        freq[term] = len(re.findall(rf"(?<!\w){re.escape(str(term).lower())}(?!\w)", lower))
    return freq


def detect_stuffing(
    text: str, terms, taxonomy: SkillsTaxonomy | None = None, max_repeat: int = 8
) -> list[tuple[str, int]]:
    """Terms repeated >= max_repeat times — spam-detection signal."""
    freq = concept_frequency(text, terms)
    return [(term, count) for term, count in freq.items() if count >= max_repeat]


def stuffing_penalty(stuffing_hits: list[tuple[str, int]]) -> float:
    """Penalty in 0..1 space: 0.05 per stuffed term, capped at 0.2."""
    return min(0.2, 0.05 * len(stuffing_hits))


if __name__ == "__main__":
    text = ("python python python python python python python python python "
            "docker kubernetes")
    print(unique_concept_count({"python", "docker", "kubernetes"}))
    print(detect_stuffing(text, ["python", "docker"]))
