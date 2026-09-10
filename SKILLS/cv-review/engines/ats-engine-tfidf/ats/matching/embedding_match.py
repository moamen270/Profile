"""Section 4 — Semantic embeddings: TF-IDF + cosine similarity (THIS PROJECT'S BACKEND).

Research: "BERT/word2vec vectors for CV & JD, cosine similarity" — this project
implements the semantic tier with scikit-learn TF-IDF vectors instead of
transformers: zero model downloads, deterministic, fast. The sister project
ats-engine-transformer implements the same interface with sentence-transformers.

API (identical in both projects):
    SemanticMatcher().similarity(text_a, text_b) -> float       # cosine, 0..1
    SemanticMatcher().term_similarities(terms, context) -> {term: score}
    SemanticMatcher().compare(resume_text, jd_text) -> MatchResult
"""
from __future__ import annotations

from ..models import MatchResult

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError as _exc:  # pragma: no cover
    raise ImportError(
        "scikit-learn is required for the TF-IDF backend: pip install scikit-learn"
    ) from _exc


class SemanticMatcher:
    """TF-IDF vector space + cosine similarity. Zero downloads, deterministic."""

    backend = "tfidf"
    model_name = "tfidf-1-2gram"

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

    def similarity(self, text_a: str, text_b: str) -> float:
        """Cosine similarity between two documents (0..1)."""
        matrix = self._matrix([text_a, text_b])
        return float(max(matrix[0][1], 0.0))

    def term_similarities(self, terms, resume_text: str) -> dict[str, float]:
        """Similarity of each JD term to the whole resume document."""
        docs = [resume_text] + [str(term) for term in terms]
        matrix = self._matrix(docs)
        return {
            str(term): float(max(matrix[index][0], 0.0))
            for index, term in enumerate(terms, start=1)
        }

    def compare(self, resume_text: str, jd_text: str) -> MatchResult:
        score = self.similarity(resume_text, jd_text)
        return MatchResult(
            technique="semantic_embedding", score=round(score, 4),
            evidence={"backend": self.backend, "model": self.model_name},
            notes="TF-IDF vectors + cosine similarity (Greenhouse/iCIMS semantic tier)",
        )

    def _matrix(self, docs: list[str]):
        vectors = self._vectorizer.fit_transform(docs)
        return cosine_similarity(vectors)


if __name__ == "__main__":
    matcher = SemanticMatcher()
    a = "Senior backend engineer with Python, Docker and Kubernetes at scale"
    b = "We need a backend engineer with Python, Docker, K8s experience"
    c = "Seeking a nurse for a hospital ward, night shifts"
    print("related:", round(matcher.similarity(a, b), 3))
    print("unrelated:", round(matcher.similarity(a, c), 3))
