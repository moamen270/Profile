"""Industry detection (shared by JD parsing and the industry-alignment factor).

API:
    detect_industry(text) -> str | None
"""
from __future__ import annotations

INDUSTRY_KEYWORDS: dict[str, list[str]] = {
    "fintech": ["fintech", "payments", "lending", "banking", "trading platform"],
    "finance": ["investment bank", "asset management", "hedge fund", "financial services", "insurance"],
    "healthcare": ["healthcare", "health tech", "hospital", "pharma", "clinical", "medical"],
    "ecommerce": ["e-commerce", "ecommerce", "marketplace", "retail", "d2c"],
    "saas": ["saas", "b2b software", "software company"],
    "education": ["edtech", "education", "learning platform", "online courses"],
    "gaming": ["gaming", "game studio", "esports"],
    "logistics": ["logistics", "supply chain", "shipping", "fulfillment"],
    "energy": ["energy", "oil & gas", "renewables", "solar"],
    "media": ["media", "streaming", "publishing", "advertising agency"],
    "consulting": ["consulting", "consultancy", "professional services"],
    "government": ["government", "public sector", "civic"],
}


def detect_industry(text: str) -> str | None:
    """Return the most likely industry for a JD or resume text.

    Requires >= 2 keyword hits to avoid false positives (e.g. "University"
    inside an institution name triggering 'education')."""
    lower = text.lower()
    best: tuple[str, int] = ("", 0)
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in lower)
        if count > best[1]:
            best = (industry, count)
    return best[0] if best[1] >= 2 else None


if __name__ == "__main__":
    print(detect_industry("We are a fintech building payments infrastructure"))
    print(detect_industry("Hospital network seeking nurses and clinical staff"))
