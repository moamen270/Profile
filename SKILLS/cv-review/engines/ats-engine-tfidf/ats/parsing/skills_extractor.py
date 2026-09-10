"""Section 2/3 — Skills extraction (taxonomy-driven, variation -> canonical).

Uses the ESCO-style taxonomy in data/skills_taxonomy.json: every variation
("ReactJS", "react.js", "react library") maps to one canonical entity
("react") — the normalization layer from research section 3.

API:
    load_taxonomy() -> dict
    build_variation_map(taxonomy) -> {variation: canonical}
    find_skills(text, variation_map) -> set[str]
    skill_locations(text, sections, variation_map) -> {skill: [sections]}
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "skills_taxonomy.json"


def load_taxonomy(path: Path | None = None) -> dict:
    path = path or DATA_FILE
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def build_variation_map(taxonomy: dict) -> dict[str, str]:
    """variation (lowercased) -> canonical skill name."""
    mapping: dict[str, str] = {}
    for canonical, variations in taxonomy.get("skills", {}).items():
        mapping[canonical.lower()] = canonical
        for variation in variations:
            mapping[variation.lower()] = canonical
    return mapping


def find_skills(text: str, variation_map: dict[str, str]) -> set[str]:
    """Longest-first scan of the text for any known skill variation."""
    text_lower = text.lower()
    found: set[str] = set()
    for variation, canonical in variation_map.items():
        if re.search(rf"(?<!\w){re.escape(variation)}(?!\w)", text_lower):
            found.add(canonical)
    return found


def skill_locations(
    text: str, sections: dict[str, str], variation_map: dict[str, str]
) -> tuple[set[str], dict[str, list[str]]]:
    """Return (all canonical skills, {skill: [sections where it appears]})."""
    all_found = find_skills(text, variation_map)
    locations: dict[str, list[str]] = {}
    for skill in all_found:
        found_in = [name for name, body in sections.items() if find_skills(body, variation_map) and skill in find_skills(body, variation_map)]
        locations[skill] = found_in
    return all_found, locations


if __name__ == "__main__":
    taxonomy = load_taxonomy()
    mapping = build_variation_map(taxonomy)
    sample = "Skilled in ReactJS, k8s and Postgres. CPA certified."
    print(sorted(find_skills(sample, mapping)))
