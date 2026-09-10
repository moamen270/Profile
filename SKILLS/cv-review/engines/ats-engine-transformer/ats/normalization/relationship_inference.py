"""Section 3 — Relationship inference.

"Docker + Kubernetes -> cloud infrastructure capability." Two related skills
together imply a capability neither proves alone (Workday/Phenom ontologies).

API:
    infer_relationships(skills, taxonomy) -> {capability: [skills that triggered it]}
"""
from __future__ import annotations

from .taxonomy import SkillsTaxonomy


def infer_relationships(
    skills: set[str], taxonomy: SkillsTaxonomy | None = None
) -> dict[str, list[str]]:
    """Infer high-level capabilities from co-occurring skill sets."""
    taxonomy = taxonomy or SkillsTaxonomy()
    inferred: dict[str, list[str]] = {}
    normalized = {s.lower() for s in skills}

    for capability, spec in taxonomy.relationships.items():
        group = {s.lower() for s in spec.get("skills", [])}
        required = int(spec.get("min_skills", 2))
        overlap = sorted(normalized & group)
        if len(overlap) >= required:
            inferred[capability] = overlap
    return inferred


if __name__ == "__main__":
    inferred = infer_relationships({"docker", "kubernetes", "aws", "python"})
    for capability, evidence in inferred.items():
        print(f"{capability}: {evidence}")
