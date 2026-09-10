"""Section 5 — Workday HiredScore letter grades (A/B/C/D).

Research: "All basic quals met = A/B; miss one = C/D; preferred quals
differentiate A vs B. -57% recruiter screening time."

API:
    letter_grade(basic_met, basic_total, preferred_met, preferred_total) -> str
    workday_grade_rules() -> dict
"""
from __future__ import annotations


def letter_grade(
    basic_met: int,
    basic_total: int,
    preferred_met: int = 0,
    preferred_total: int = 0,
) -> str:
    """Workday HiredScore rules:
    - all basic met: A if preferred met ratio high (>=0.6 or none specified), else B
    - missing >=1 basic: C if >=60% of basic met, else D
    """
    if basic_total == 0:
        return "B"
    if basic_met >= basic_total:
        if preferred_total == 0:
            return "A"
        ratio = preferred_met / preferred_total
        return "A" if ratio >= 0.6 else "B"
    ratio = basic_met / basic_total
    return "C" if ratio >= 0.6 else "D"


def workday_grade_rules() -> dict:
    return {
        "A": "all basic qualifications met + strong preferred coverage",
        "B": "all basic qualifications met, weaker preferred coverage",
        "C": "missing at least one basic qualification (>=60% met)",
        "D": "missing multiple basic qualifications (<60% met)",
    }


if __name__ == "__main__":
    print(letter_grade(4, 4, 2, 2))   # A
    print(letter_grade(4, 4, 0, 3))   # B
    print(letter_grade(3, 4))         # C
    print(letter_grade(1, 4))         # D
