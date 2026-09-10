"""Section 3 — normalization tests."""
from __future__ import annotations

from ats.normalization.relationship_inference import infer_relationships
from ats.normalization.synonym_normalizer import SynonymNormalizer
from ats.normalization.taxonomy import SkillsTaxonomy
from ats.normalization.unique_concepts import detect_stuffing, unique_concept_count


class TestTaxonomy:
    def test_canonical(self):
        tax = SkillsTaxonomy()
        assert tax.canonical("ReactJS") == "react"
        assert tax.canonical("k8s") == "kubernetes"

    def test_normalize_set(self):
        tax = SkillsTaxonomy()
        normalized = tax.normalize_set({"React.js", "k8s", "PostgreSQL", "weird-thing"})
        assert {"react", "kubernetes", "sql"} <= normalized

    def test_find_in_text(self):
        tax = SkillsTaxonomy()
        assert "react" in tax.find_in_text("built with React.js and Redux")


class TestSynonyms:
    def test_acronym(self):
        norm = SynonymNormalizer()
        assert norm.canonical("CPA") == "certified public accountant"

    def test_terms_equal(self):
        norm = SynonymNormalizer()
        assert norm.terms_equal("CPA", "Certified Public Accountant")
        assert not norm.terms_equal("CPA", "CFA")

    def test_expand_text(self):
        norm = SynonymNormalizer()
        expanded = norm.expand_text("CPA with k8s and ETL experience")
        assert "certified public accountant" in expanded.lower()


class TestRelationships:
    def test_docker_k8s_infer_cloud(self):
        inferred = infer_relationships({"docker", "kubernetes", "python"})
        assert "cloud infrastructure capability" in inferred

    def test_insufficient_skills(self):
        inferred = infer_relationships({"docker"})
        assert "cloud infrastructure capability" not in inferred


class TestUniqueConcepts:
    def test_unique_count(self):
        assert unique_concept_count({"python", "docker", "PYTHON"}) == 2

    def test_stuffing_detection(self):
        text = " ".join(["python"] * 10) + " docker"
        hits = detect_stuffing(text, ["python", "docker"])
        assert ("python", 10) in hits

    def test_no_stuffing(self):
        assert detect_stuffing("python and docker developer", ["python", "docker"]) == []
