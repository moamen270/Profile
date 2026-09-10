"""Section 8 — Bias audit: 4/5ths (80%) disparate-impact rule.

Research (NYC Local Law 144 / AEDT, EEOC): "any ranking tool must have annual
independent bias audits, disparate-impact ratios".

API:
    selection_rates(groups: dict[group, (selected, total)]) -> dict[group, float]
    disparate_impact_ratio(groups) -> float | None     # min/max ratio
    bias_audit(groups) -> dict                         # pass/fail per 4/5ths rule
"""
from __future__ import annotations


def selection_rates(outcomes: dict[str, list[bool]]) -> dict[str, float]:
    """outcomes: {group_name: [True(advanced)/False(rejected), ...]}"""
    rates = {}
    for group, flags in outcomes.items():
        flags = list(flags)
        rates[group] = (sum(1 for f in flags if f) / len(flags)) if flags else 0.0
    return rates


def disparate_impact_ratio(rates: dict[str, float]) -> float | None:
    """min rate / max rate across groups (None if no data)."""
    values = [v for v in rates.values() if v >= 0]
    if not values or max(values) == 0:
        return None
    return round(min(values) / max(values), 4)


def bias_audit(outcomes: dict[str, list[bool]], threshold: float = 0.8) -> dict:
    """Full audit result: rates, ratio, pass/fail under the 4/5ths rule."""
    rates = selection_rates(outcomes)
    ratio = disparate_impact_ratio(rates)
    passed = ratio is None or ratio >= threshold
    flagged = [] if passed else [
        group for group, rate in rates.items() if rate == min(rates.values())
    ]
    return {
        "rates": rates,
        "disparate_impact_ratio": ratio,
        "four_fifths_threshold": threshold,
        "passed": passed,
        "flagged_groups": flagged,
        "note": "4/5ths rule (EEOC): ratio < 0.8 indicates adverse impact — AEDT audit finding",
    }


if __name__ == "__main__":
    outcomes = {
        "group_a": [True, True, True, True, False],
        "group_b": [True, False, False, False, False],
    }
    print(bias_audit(outcomes))
