"""Section 4 — Graph-based fusion (academic model).

Academic person-job fit work fuses CV/JD signals on a graph: skills are
nodes, edges encode relatedness (shared clusters, shared inferred
capabilities), and relevance propagates through the graph — a JD term can be
partially satisfied by a *related* skill, not just itself.

Implementation: personalized PageRank over the skill graph, teleporting to
the JD skills; score = PageRank mass on resume skills relative to the JD
mass. A resume skill earns mass for itself AND its neighbors, so
"kubernetes" partially covers a JD asking for "docker" (same cluster) —
relationship inference (research §3) fused across a graph.

API:
    build_adjacency(skills, taxonomy) -> {skill: {related_skill: weight}}
    graph_fusion_score(resume_skills, jd_skills, taxonomy) -> MatchResult
"""
from __future__ import annotations

from ..models import MatchResult
from ..normalization.taxonomy import SkillsTaxonomy

_SEED_WEIGHT = 0.15  # teleport mass (standard PR (1-d))
_DAMPING = 0.85
_ITERATIONS = 30


def _group_members(members) -> set[str]:
    return {m.lower() for m in members}


def build_adjacency(skills: set[str], taxonomy: SkillsTaxonomy) -> dict[str, dict[str, float]]:
    """Skill -> {related skill: edge weight} via shared clusters/capabilities."""
    normalized = [s.lower() for s in skills]
    adjacency: dict[str, dict[str, float]] = {s: {} for s in normalized}

    def connect(a: str, b: str, weight: float) -> None:
        if a != b:
            adjacency[a][b] = max(adjacency[a].get(b, 0.0), weight)
            adjacency[b][a] = max(adjacency[b].get(a, 0.0), weight)

    for cluster_members in taxonomy.clusters.values():
        cluster = _group_members(cluster_members)
        for i, a in enumerate(normalized):
            if a in cluster:
                for b in normalized[i + 1:]:
                    if b in cluster:
                        connect(a, b, 0.5)

    for spec in taxonomy.relationships.values():
        group = _group_members(spec.get("skills", []))
        for i, a in enumerate(normalized):
            if a in group:
                for b in normalized[i + 1:]:
                    if b in group:
                        connect(a, b, 0.5)
    return adjacency


def _out_weight(node: str, adjacency: dict[str, dict[str, float]]) -> float:
    return sum(adjacency.get(node, {}).values()) or 1.0


def _normalize(values: dict[str, float]) -> dict[str, float]:
    total = sum(values.values()) or 1.0
    return {n: v / total for n, v in values.items()}


def graph_fusion_score(
    resume_skills: set[str],
    jd_skills: set[str],
    taxonomy: SkillsTaxonomy | None = None,
    damping: float = _DAMPING,
    iterations: int = _ITERATIONS,
) -> MatchResult:
    """Personalized PageRank seeded on JD skills; score = mass on resume skills."""
    taxonomy = taxonomy or SkillsTaxonomy()
    resume = {s.lower() for s in resume_skills}
    jd = {s.lower() for s in jd_skills}
    if not jd or not resume:
        return MatchResult(technique="graph_fusion", score=0.0, notes="empty input")

    nodes = set(resume) | set(jd)
    adjacency = build_adjacency(nodes, taxonomy)

    teleport = {n: (1.0 / len(jd) if n in jd else 0.0) for n in nodes}
    ranks = {n: 1.0 / len(nodes) for n in nodes}

    for _ in range(iterations):
        incoming = {n: 0.0 for n in nodes}
        for source, weight_map in adjacency.items():
            out = _out_weight(source, adjacency)
            for target, weight in weight_map.items():
                incoming[target] += ranks[source] * weight / out
        ranks = _normalize({
            node: _SEED_WEIGHT * teleport[node] + damping * incoming[node]
            for node in nodes
        })

    resume_mass = sum(ranks.get(node, 0.0) for node in resume)
    jd_mass = sum(ranks.get(node, 0.0) for node in jd) or 1e-9
    # ratio of resume-captured graph mass to JD-seeded mass, scaled by coverage
    direct = len(resume & jd) / len(jd)
    score = min(1.0, direct + (resume_mass / jd_mass) * (1 - direct) / len(jd) * len(jd))
    score = min(1.0, max(0.0, direct + 0.3 * (resume_mass / jd_mass - direct) if resume_mass >= jd_mass else resume_mass / jd_mass))
    return MatchResult(
        technique="graph_fusion",
        score=round(_final_score(ranks, resume, jd), 4),
        matched=sorted(resume & jd),
        evidence={"graph_nodes": len(nodes)},
        notes="personalized-PageRank skill-graph fusion (academic graph-based person-job fit)",
    )


def _final_score(ranks: dict[str, float], resume: set[str], jd: set[str]) -> float:
    """Direct hits get full credit; neighbor mass adds a partial bonus."""
    direct = len(resume & jd) / len(jd) if jd else 0.0
    total = sum(ranks.values()) or 1.0
    resume_mass = sum(ranks.get(n, 0.0) for n in resume) / total
    neighbor_bonus = min(0.3, max(0.0, resume_mass - direct))
    return direct + neighbor_bonus


if __name__ == "__main__":
    tax = SkillsTaxonomy()
    good = graph_fusion_score({"docker", "kubernetes", "terraform"}, {"docker", "kubernetes", "aws"}, tax)
    weak = graph_fusion_score({"baking", "painting"}, {"docker", "kubernetes", "aws"}, tax)
    print("good:", good.score, "weak:", weak.score)
