"""OCP: add retrieval ranking strategies without changing the RAG pipeline."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Candidate:
    document_id: str
    similarity: float
    quality: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(value) for value in (self.similarity, self.quality)):
            raise ValueError("ranking scores must be finite")


def coupled_rank(candidates: Sequence[Candidate], strategy: str) -> list[Candidate]:
    """Anti-pattern: every new ranking strategy requires editing this branch."""
    if strategy == "similarity":
        return sorted(candidates, key=lambda item: item.similarity, reverse=True)
    if strategy == "quality":
        return sorted(candidates, key=lambda item: item.quality, reverse=True)
    raise ValueError(f"unknown strategy: {strategy}")


class RankingStrategy(Protocol):
    def score(self, candidate: Candidate) -> float: ...


class SimilarityRanking:
    def score(self, candidate: Candidate) -> float:
        return candidate.similarity


@dataclass(frozen=True, slots=True)
class WeightedRanking:
    similarity_weight: float = 0.7

    def __post_init__(self) -> None:
        if not 0 <= self.similarity_weight <= 1:
            raise ValueError("weight must be between zero and one")

    def score(self, candidate: Candidate) -> float:
        return (
            self.similarity_weight * candidate.similarity
            + (1 - self.similarity_weight) * candidate.quality
        )


class RetrievalPipeline:
    def __init__(self, ranking: RankingStrategy) -> None:
        self._ranking = ranking

    def select(
        self, candidates: Sequence[Candidate], *, top_k: int = 2
    ) -> list[Candidate]:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        scored = [
            (self._ranking.score(candidate), candidate) for candidate in candidates
        ]
        if any(not math.isfinite(score) for score, _ in scored):
            raise ValueError("strategy produced a non-finite score")
        # An explicit tie-breaker keeps results reproducible across input order.
        scored.sort(key=lambda item: (-item[0], item[1].document_id))
        return [candidate for _, candidate in scored[:top_k]]


def main() -> None:
    candidates = [Candidate("doc-a", 0.95, 0.2), Candidate("doc-b", 0.85, 0.9)]
    for strategy in (SimilarityRanking(), WeightedRanking(0.5)):
        print(type(strategy).__name__, RetrievalPipeline(strategy).select(candidates))
    # A learned reranker implements score(); the selection algorithm stays stable.


if __name__ == "__main__":
    main()
