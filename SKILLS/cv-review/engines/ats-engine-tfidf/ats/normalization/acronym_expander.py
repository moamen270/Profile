"""Section 3 — Acronym expansion (k8s -> Kubernetes, CPA -> full form).

Same data as synonym_normalizer but focused on expanding acronyms inline so
downstream literal matchers see both forms.

API:
    expand_acronyms(text) -> str          # "k8s" -> "kubernetes"
    expand_term(term) -> str
    acronym_pairs() -> {acronym: full form}
"""
from __future__ import annotations

import re

from .synonym_normalizer import load_synonyms

_ACRONYM_MAX_LEN = 6  # tokens this short (or shorter) are treated as acronyms

_SYNONYMS: dict[str, str] = {}


def _ensure_synonyms() -> dict[str, str]:
    global _SYNONYMS
    if not _SYNONYMS:
        _SYNONYMS = load_synonyms()
    return _SYNONYMS


def expand_acronyms(text: str, synonyms: dict[str, str] | None = None) -> str:
    """Replace short acronym tokens with their full form, word-boundary safe."""
    synonyms = synonyms if synonyms is not None else _ensure_synonyms()
    for variant, canonical in synonyms.items():
        if len(variant) > _ACRONYM_MAX_LEN:
            continue
        text = re.sub(rf"(?<!\w){re.escape(variant)}(?!\w)", canonical, text, flags=re.IGNORECASE)
    return text


def expand_term(term: str, synonyms: dict[str, str] | None = None) -> str:
    synonyms = synonyms if synonyms is not None else _ensure_synonyms()
    return synonyms.get(term.strip().lower(), term)


def acronym_pairs(synonyms: dict[str, str] | None = None) -> dict[str, str]:
    """Acronym -> full form map (filtered to short tokens)."""
    synonyms = synonyms if synonyms is not None else _ensure_synonyms()
    return {variant: canonical for variant, canonical in synonyms.items() if len(variant) <= _ACRONYM_MAX_LEN}


if __name__ == "__main__":
    print(expand_acronyms("CPA with k8s and ETL experience"))
