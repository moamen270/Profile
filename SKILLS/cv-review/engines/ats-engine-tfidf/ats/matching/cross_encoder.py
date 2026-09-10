"""Section 4 — Cross-encoder re-ranking.

Bi-encoders (embedding_match) embed CV and JD independently and compare
vectors. Cross-encoders score each (query, passage) pair JOINTLY — the
academic BERT cross-encoder pattern and production re-ranking stages.

This implementation applies the cross-encoder *interaction pattern* on top of
the project's embedding backend: every (JD qualification x resume sentence)
pair is scored at fine granularity; each qualification takes its best
sentence; the mean over qualifications is the re-ranked score. It fixes the
classic bi-encoder failure where one strong section is drowned out by bulk text.

API:
    CrossEncoderReranker(matcher).score_qualification(qual_text, resume_text) -> float
    CrossEncoderReranker(matcher).rerank(jd, resume_text) -> MatchResult
"""
from __future__ import annotations

import re

from ..models import MatchResult

_SENT_SPLIT = re.compile(r"[.!?\n]+")


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_SPLIT.split(text) if len(s.strip().split()) >= 3]


class CrossEncoderReranker:
    """Pairwise (qualification, sentence) interaction scoring."""

    technique = "cross_encoder"

    def __init__(self, matcher) -> None:
        self.matcher = matcher  # SemanticMatcher (either backend)

    def qualification_score(self, qual_text: str, sentences: list[str]) -> tuple[float, str]:
        """Max pair score for one qualification; returns (score, best sentence)."""
        if not sentences:
            return 0.0, ""
        scores = []
        for sentence in sentences:
            scores.append(self.matcher.similarity(qual_text, sentence))
        best_index = max(range(len(scores)), key=lambda i: scores[i])
        return max(scores), sentences[best_index]

    def rerank(self, jd, resume_text: str) -> MatchResult:
        qualifications = [q.text for q in (jd.qualifications or [])]
        if not qualifications:
            return MatchResult(
                technique=self.technique, score=0.0,
                notes="no JD qualifications extracted",
            )
        sentences = split_sentences(resume_text)
        per_qual: dict[str, float] = {}
        best_evidence: dict[str, str] = {}
        for qual in qualifications[:50]:  # Ashby caps criteria at 50
            score, evidence = self.qualification_score(qual, sentences)
            best_evidence[qual] = round(score, 3)
        score = sum(best_evidence.values()) / len(best_evidence)
        top_qual = max(best_evidence, key=best_evidence.get)
        return MatchResult(
            technique=self.technique, score=round(score, 4),
            evidence={"per_qualification": best_evidence, "top": top_qual[:120]},
            notes="pairwise interaction re-ranking (BERT cross-encoder pattern)",
        )


if __name__ == "__main__":
    from .embedding_match import SemanticMatcher

    reranker = CrossEncoderReranker(SemanticMatcher())
    jd_text = "REQUIREMENTS\n- Strong Python and SQL skills\n- Kubernetes operations experience"
    from ..parsing.jd_parser import parse_job_description

    jd = parse_job_description(jd_text)
    resume = "Python developer. Ran postgres databases.\nOperated k8s clusters in production for 3 years."
    result = reranker.rerank(jd, resume)
    print(result.score, result.evidence["top"])
