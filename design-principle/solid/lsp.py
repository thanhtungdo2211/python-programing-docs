"""LSP: embedding adapters preserve input and output behavior, not just types.

Every implementation accepts all non-empty texts, returns one finite vector per
text in input order, and uses the declared dimension. Empty batches return [].
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Protocol

Vector = tuple[float, ...]


class EmbeddingModel(Protocol):
    @property
    def dimensions(self) -> int: ...

    def embed(self, texts: Sequence[str]) -> list[Vector]: ...


def validate_texts(texts: Sequence[str]) -> None:
    if any(not text.strip() for text in texts):
        raise ValueError("texts must not be blank")


class LocalEmbedder:
    dimensions = 2

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        validate_texts(texts)
        return [(float(len(text)), float(len(text.split()))) for text in texts]


class BrokenShortTextEmbedder(LocalEmbedder):
    """Anti-pattern: strengthens a precondition by rejecting valid long texts."""

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        if any(len(text) > 10 for text in texts):
            raise ValueError("this adapter only supports short text")
        return super().embed(texts)


class BatchedEmbedder:
    """Adapt a backend's batch limit without narrowing the public contract."""

    def __init__(self, backend: EmbeddingModel, *, batch_size: int = 2) -> None:
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        self._backend = backend
        self._batch_size = batch_size

    @property
    def dimensions(self) -> int:
        return self._backend.dimensions

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        validate_texts(texts)  # Validate the entire request before backend calls.
        vectors: list[Vector] = []
        for start in range(0, len(texts), self._batch_size):
            vectors.extend(self._backend.embed(texts[start : start + self._batch_size]))
        return vectors


def checked_embed(model: EmbeddingModel, texts: Sequence[str]) -> list[Vector]:
    """Enforce shape and numeric postconditions at the infrastructure boundary.

    Semantic order needs adapter contract tests: shape checks cannot detect a
    backend that silently reorders vectors. Models with different vector spaces
    also require separate indexes even if their dimensions happen to match.
    """
    validate_texts(texts)
    vectors = model.embed(texts)
    if model.dimensions < 1 or len(vectors) != len(texts):
        raise ValueError("embedding contract violated: invalid output shape")
    if any(
        len(vector) != model.dimensions or not all(math.isfinite(v) for v in vector)
        for vector in vectors
    ):
        raise ValueError("embedding contract violated: invalid vector")
    return vectors


def main() -> None:
    texts = ["short", "a much longer document", "third document"]
    for model in (LocalEmbedder(), BatchedEmbedder(LocalEmbedder(), batch_size=1)):
        print(type(model).__name__, checked_embed(model, texts))
    try:
        checked_embed(BrokenShortTextEmbedder(), texts)
    except ValueError as error:
        print(f"LSP violation: {error}")


if __name__ == "__main__":
    main()
