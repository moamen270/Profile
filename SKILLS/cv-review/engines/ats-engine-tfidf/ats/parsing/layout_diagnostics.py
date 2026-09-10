"""Section 2 — Layout diagnostics: the failures that silently kill CVs.

Detects two-column layouts (interleaved garble), text in headers/footers
(skipped entirely), tables, and tiny fonts — from positioned words produced by
pdf_extractor. Also renders the "what the ATS sees" reading-order preview.

API:
    diagnose(words, page_width, page_height) -> LayoutReport
    reading_order_preview(words, page_width, page_height, lines=...) -> list[str]
"""
from __future__ import annotations

import re

from ..models import LayoutReport
from .pdf_extractor import PositionedWord

_NUMERIC = re.compile(r"\d")


def _column_mass(words: list[PositionedWord], width: float) -> tuple[float, float, float]:
    """Fraction of text mass in left band, middle band, right band."""
    if width <= 0 or not words:
        return 0.0, 0.0, 0.0
    left = middle = right = 0
    for word in words:
        rel = word.x / width
        chars = max(len(word.text), 1)
        if rel < 0.35:
            left += chars
        elif rel > 0.55:
            right += chars
        else:
            middle += chars
    total = left + middle + right
    if not total:
        return 0.0, 0.0, 0.0
    return left / total, middle / total, right / total


def diagnose(words: list[PositionedWord], page_width: float, page_height: float) -> LayoutReport:
    report = LayoutReport()
    if not words or page_width <= 0 or page_height <= 0:
        return report

    left, middle, right = _column_mass(words, page_width)
    if left > 0.25 and right > 0.25 and middle < 0.35:
        report.two_column = True
        report.notes.append(
            "Two-column layout detected — interleaved garble in most ATS parsers. "
            "Use a single-column layout."
        )

    headers: list[str] = []
    for word in words:
        if word.y > page_height * 0.93 and len(word.text) > 3:
            headers.append(word.text)
        elif word.y < page_height * 0.07 and len(word.text) > 3:
            headers.append(word.text)
    if headers:
        report.header_footer_text = headers[:10]
        report.notes.append(
            "Text found in page header/footer region — many parsers skip it entirely."
        )

    report.tiny_fonts = sum(1 for w in words if 0 < w.font_size < 8)
    if report.tiny_fonts > 5:
        report.notes.append("Tiny fonts detected (<8pt) — parsing accuracy degrades.")

    for word in words:
        if word.text.count("\t") >= 2 or word.text.count("|") >= 2:
            report.table_like_lines += 1
        elif len(word.text) > 20 and sum(1 for ch in word.text if _NUMERIC.match(ch)) >= 3:
            report.table_like_lines += 1
    if report.table_like_lines > 3:
        report.notes.append("Table-like content detected — tables scramble chronology in ATS parsers.")

    return report


def reading_order_preview(
    words: list[PositionedWord], page_width: float, page_height: float, max_lines: int = 40
) -> list[str]:
    """Simulated ATS reading order: naive top-to-bottom, left-to-right per line band.
    In a two-column layout this demonstrates the interleaving problem."""
    if not words:
        return []

    two_col = False
    left, _middle, right = _column_mass(words, page_width)
    if left > 0.25 and page_width > 0:
        # crude split: any words starting in left 45% vs rest
        two_col = len([w for w in words if w.x < page_width * 0.45]) > 0.4 * len(words)
    if not two_col:
        ordered = sorted(words, key=lambda w: (-w.y, w.x))
    else:
        left_col = sorted([w for w in words if w.x < page_width * 0.5], key=lambda w: (-w.y, w.x))
        right_col = sorted([w for w in words if w.x >= page_width * 0.5], key=lambda w: (-w.y, w.x))
        # interleave: all left column first (how many real parsers mangle it)
        ordered = left_col + right_col

    return [w.text for w in ordered[:max_lines]]


if __name__ == "__main__":
    demo = [
        PositionedWord("Summary", 300, 700, 12),
        PositionedWord("Experience", 300, 500, 12),
        PositionedWord("Skills", 50, 400, 10),
        PositionedWord("Python", 50, 380, 10),
        PositionedWord("Java", 50, 360, 10),
        PositionedWord("React", 300, 400, 10),
    ]
    report = diagnose(demo, page_width=612, page_height=792)
    print(report)
    print("\n".join(reading_order_preview(demo, 612, 792)))
