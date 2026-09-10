"""Section 5 — Taleo ACE percentage scoring.

Research: "Points -> % (points earned / total possible x 100). Tiers: ACE
candidate / minimally qualified / other. Star icon + threshold alerts
(e.g. >=75% or >=3 of 5 assets)."

API:
    ace_score(points_earned, points_possible) -> float
    ace_points(factors) -> (earned, possible)
    ace_tier(percentage) -> str
    meets_asset_threshold(assets_hit, assets_total=5, min_assets=3, min_pct=75) -> bool
"""
from __future__ import annotations

from ..models import FactorResult


def ace_score(points_earned: float, points_possible: float) -> float:
    if points_possible <= 0:
        return 0.0
    return round(points_earned / points_possible * 100.0, 1)


def ace_points(factors: list[FactorResult]) -> tuple[float, float]:
    """Each factor contributes score*weight points; possible = sum(weights)."""
    earned = sum(f.score * f.weight for f in factors)
    possible = sum(f.weight for f in factors)
    return round(earned, 3), round(possible, 3)


def ace_tier(percentage: float) -> str:
    if percentage >= 75:
        return "ACE candidate"
    if percentage >= 50:
        return "minimally qualified"
    return "other"


def meets_asset_threshold(assets_hit: int, assets_total: int = 5, min_assets: int = 3, min_pct: float = 75.0) -> bool:
    """Taleo threshold alerts: >=75% OR >=3 of 5 assets."""
    pct = assets_hit / assets_total * 100 if assets_total else 0
    return pct >= min_pct or assets_hit >= min_assets


def ace_from_factors(factors: list[FactorResult]) -> dict:
    earned, possible = ace_points(factors)
    percentage = ace_score(earned, possible)
    return {
        "percentage": percentage,
        "points_earned": earned,
        "points_possible": possible,
        "tier": ace_tier(percentage),
    }


if __name__ == "__main__":
    factors = [
        FactorResult("skills", 0.9, 3.0), FactorResult("experience", 0.6, 2.0),
        FactorResult("education", 1.0, 1.0),
    ]
    print(ace_from_factors(factors))
    print(meets_asset_threshold(3, 5))
