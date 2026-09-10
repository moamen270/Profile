"""Section 4 — Learning-to-rank (academic / iCIMS-Eightfold style).

Research: "learning-to-rank on application history" and "ensemble ML ...
trained on historical applications, learning what successful hires looked
like". Real systems train on 100M+ applications; this implements the
learning-to-rank *pattern* with a pure-Python logistic-regression ranker over
matcher/factor features — fit it on your historical application outcomes,
then rank new candidates.

API:
    LTRanker().fit(X, y)                    # y: 1=advanced, 0=rejected
    LTRanker().score(features) -> float     # P(advance)
    LTRanker().rank(candidates) -> [(id, p)] best-first
    features_from_matchers(matchers, factors) -> feature row
    features_from_report(report) -> feature row
"""
from __future__ import annotations

import math

from ..models import AnalysisReport, FactorResult, MatchResult

_E = math.e


class LTRanker:
    """Pure-Python logistic-regression learning-to-ranker (deterministic)."""

    technique = "learning_to_rank"

    def __init__(self, learning_rate: float = 0.5, epochs: int = 300, l2: float = 1e-3) -> None:
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.l2 = l2
        self.weights: list[float] = []
        self.bias = 0.0
        self.trained = False

    @staticmethod
    def _sigmoid(z: float) -> float:
        if z >= 0:
            return 1.0 / (1.0 + math.exp(-z))
        e = math.exp(z)
        return e / (1.0 + e)

    def score(self, row: list[float]) -> float:
        """P(advance) for one feature row."""
        if not self.trained:
            return 0.5  # untrained -> neutral
        z = sum(w * x for w, x in zip(self.weights, row)) + self.bias
        return round(self._sigmoid(z), 4)

    def fit(self, rows: list[list[float]], labels: list[int]) -> "LTRanker":
        if not rows:
            return self
        self.weights = [0.0] * len(rows[0])
        self.bias = 0.0
        n = len(rows)
        for _ in range(self.epochs):
            grad_w = [0.0] * len(self.weights)
            grad_b = 0.0
            for row, label in zip(rows, labels):
                error = self._predict(row) - label
                for i, value in enumerate(row):
                    grad_w[i] += error * value + self.l2 * self.weights[i]
                grad_b += error
            self.weights = [w - self.learning_rate * (g / n) for w, g in zip(self.weights, grad_w)]
            self.bias -= self.learning_rate * (grad_b / n)
        self.trained = True
        return self

    def rank(self, scored: list[tuple[str, list[float]]]) -> list[tuple[str, float]]:
        """[(candidate_id, features)] -> ranked best-first."""
        ranked = [(candidate_id, self.score(row)) for candidate_id, row in scored]
        return sorted(ranked, key=lambda pair: -pair[1])

    # internal
    def _predict(self, row: list[float]) -> float:
        z = sum(w * x for w, x in zip(self.weights, row)) + self.bias
        return self._sigmoid(z)


def features_from_matchers(matchers: dict[str, MatchResult], factors: list[FactorResult]) -> list[float]:
    """Feature row: every matcher score + weighted-mean factor score."""
    row = [m.score for m in matchers.values()]
    if factors:
        total_weight = sum(f.weight for f in factors) or 1.0
        row.append(sum(f.score * f.weight for f in factors) / total_weight)
    else:
        row.append(0.0)
    return row


def features_from_report(report: AnalysisReport) -> list[float]:
    return features_from_matchers(report.matchers, report.factors)


def predict_value(ranker: "LTRanker", row: list[float]) -> float:
    return ranker.score(row)


if __name__ == "__main__":
    ranker = LTRanker()
    ranker.fit([[0.9], [0.8], [0.1], [0.2]], [1, 1, 0, 0])
    print("high:", ranker.score([0.9]), "low:", ranker.score([0.1]))
    print("ranked:", ranker.rank([("a", [0.2]), ("b", [0.85])]))
