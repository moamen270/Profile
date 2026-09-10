"""Section 3 — Skills taxonomy / canonical entity mapping.

Workday Skills Cloud style: map "React.js / ReactJS / React library" to ONE
canonical entity so both CV and JD compare equal entities.

API:
    SkillsTaxonomy.canonical(term) -> str | None
    SkillsTaxonomy.normalize_set(terms) -> set[str]
    SkillsTaxonomy.find_in_text(text) -> set[str]
"""
from __future__ import annotations

import re

from ..parsing.skills_extractor import build_variation_map, find_skills, load_taxonomy


class SkillsTaxonomy:
    """Loads data/skills_taxonomy.json once; exposes canonical lookups."""

    def __init__(self, taxonomy_path=None) -> None:
        self.taxonomy = load_taxonomy(taxonomy_path)
        self.variation_map = build_variation_map(self.taxonomy)

    def canonical(self, term: str) -> str | None:
        term = term.strip().lower()
        return self.variation_map.get(term)

    def normalize_set(self, terms) -> set[str]:
        out: set[str] = set()
        for term in terms:
            canon = self.canonical(str(term))
            out.add(canon if canon else term.strip().lower())
        return out

    def find_in_text(self, text: str) -> set[str]:
        return find_skills(text, self.variation_map)

    @property
    def relationships(self) -> dict:
        return self.taxonomy.get("relationships", {})

    @property
    def clusters(self) -> dict:
        return self.taxonomy.get("clusters", {})


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9+#./-]*", text.lower())


if __name__ == "__main__":
    tax = SkillsTaxonomy()
    print(tax.canonical("ReactJS"))
    print(sorted(tax.normalize_set({"React.js", "k8s", "PostgreSQL", "weird-thing"})))
