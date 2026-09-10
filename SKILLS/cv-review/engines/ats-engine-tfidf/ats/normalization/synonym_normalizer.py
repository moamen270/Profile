"""Section 3 — Synonym normalization.

"CPA" <-> "Certified Public Accountant". Legacy Taleo doesn't do this —
literal matching only — which is exactly why it rejects qualified people.

API:
    SynonymNormalizer.expand_text(text) -> str        # variants -> canonical
    SynonymNormalizer.terms_equal(a, b) -> bool
    SynonymNormalizer.variant_group(term) -> set[str]
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "synonyms.json"


def load_synonyms(path: Path | None = None) -> dict[str, str]:
    path = path or Path(__file__).resolve().parents[2] / "data" / "synonyms.json"
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


class SynonymNormalizer:
    """Word-boundary, longest-first replacement of synonym variants."""

    def __init__(self, synonyms: dict[str, str] | None = None) -> None:
        self.synonyms = synonyms if synonyms is not None else load_synonyms()
        # longest first so "etl pipelines" wins over "etl"
        self._ordered = sorted(self.synonyms.items(), key=lambda kv: -len(kv[0]))

    def expand_text(self, text: str) -> str:
        for variant, canonical in self._ordered:
            text = re.sub(
                rf"(?<!\w){re.escape(variant)}(?!\w)", canonical, text, flags=re.IGNORECASE
            )
        return text

    def terms_equal(self, a: str, b: str) -> bool:
        a_l, b_l = a.strip().lower(), b.strip().lower()
        if a_l == b_l:
            return True
        return self.canonical(a_l) == self.canonical(b_l) and self.canonical(a_l) is not None

    def canonical(self, term: str) -> str:
        term = term.strip().lower()
        return self.synonyms.get(term, term)


if __name__ == "__main__":
    norm = SynonymNormalizer()
    print(norm.canonical("CPA"))
    print(norm.terms_equal("CPA", "Certified Public Accountant"))
    print(norm.expand_text("CPA with k8s and ETL experience"))
