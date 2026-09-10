"""Section 4 — Semantic embeddings: sentence-transformers + cosine (THIS PROJECT'S BACKEND).

Research: "BERT/word2vec vectors for CV & JD, cosine similarity — 'led
cross-functional team' ~ 'project management'" (Greenhouse, iCIMS, Eightfold).
This project uses sentence-transformers (all-MiniLM-L6-v2, ~90MB download on
first run). The sister project ats-engine-transformer... err, ats-engine-tfidf
implements the identical interface with TF-IDF vectors (zero downloads).

API (identical in both projects):
    SemanticMatcher().similarity(text_a, text_b) -> float       # cosine, 0..1
    SemanticMatcher().term_similarities(terms, context) -> {term: score}
    SemanticMatcher().compare(resume_text, jd_text) -> MatchResult
"""
from __future__ import annotations

import threading

from ..models import MatchResult

_model = None
_model_lock = threading.Lock()
_MODEL_NAME = "all-MiniLM-L6-v2"


def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer  # noqa: PLC0415
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "sentence-transformers is required for this backend: "
                "pip install sentence-transformers"
            ) from exc
        with _model_lock:
            if _model is None:
                _model = SentenceTransformer(_MODEL_NAME)
    return _model


class SemanticMatcher:
    """Sentence-transformer embeddings + cosine similarity (semantic tier)."""

    backend = "sentence-transformers"
    model_name = _MODEL_NAME

    def _embed(self, texts: list[str]):
        model = _get_model()
        return model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    def similarity(self, text_a: str, text_b: str) -> float:
        """Cosine similarity between two documents (0..1, clamped)."""
        vectors = _get_model().encode([text_a, text_b], normalize_embeddings=True)
        dot = float(vectors[0] @ vectors[1])
        return max(0.0, dot)

    def term_similarities(self, terms, resume_text: str) -> dict[str, float]:
        """Similarity of each JD term to the whole resume document."""
        texts = [resume_text] + [str(term) for term in terms]
        vectors = _get_model().encode(texts, normalize_embeddings=True)
        return {
            str(term): max(0.0, float(vectors[index] @ vectors[0]))
            for index, term in enumerate(terms, start=1)
        }

    def compare(self, resume_text: str, jd_text: str) -> MatchResult:
        score = self.similarity(resume_text, jd_text)
        return MatchResult(
            technique="semantic_embedding", score=round(score, 4),
            evidence={"backend": self.backend, "model": self.model_name},
            notes="Sentence-transformer embeddings + cosine (Greenhouse/iCIMS semantic tier)",
        )


if __name__ == "__main__":
    matcher = SemanticMatcher()
    a = "Senior backend engineer with Python, Docker and Kubernetes at scale"
    b = "We need a backend engineer with Python, Docker, K8s experience"
    c = "Seeking a nurse for a hospital ward, night shifts"
    print("related:", round(matcher.similarity(a, b), 3))
    print("unrelated:", round(matcher.similarity(a, c), 3))
