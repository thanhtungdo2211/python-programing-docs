"""ISP: clients depend only on AI capabilities they actually consume."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol


class AllPurposeAIClient(Protocol):
    """Anti-pattern: forces embedding-only adapters to expose unrelated methods."""

    def embed(self, text: str) -> tuple[float, ...]: ...

    def generate(self, prompt: str) -> str: ...

    def stream(self, prompt: str) -> Iterator[str]: ...

    def fine_tune(self, dataset_uri: str) -> str: ...


class EmbeddingClient(Protocol):
    def embed(self, text: str) -> tuple[float, ...]: ...


class TextGenerator(Protocol):
    def generate(self, prompt: str) -> str: ...


class StreamingGenerator(Protocol):
    def stream(self, prompt: str) -> Iterator[str]: ...


class SemanticIndexer:
    def __init__(self, embeddings: EmbeddingClient) -> None:
        self._embeddings = embeddings

    def index(self, text: str) -> tuple[float, ...]:
        if not text.strip():
            raise ValueError("text must not be blank")
        return self._embeddings.embed(text)


class AnswerService:
    def __init__(self, generator: TextGenerator) -> None:
        self._generator = generator

    def answer(self, question: str) -> str:
        if not question.strip():
            raise ValueError("question must not be blank")
        return self._generator.generate(question)


class LocalEmbeddingClient:
    # No dummy generate(), stream(), or fine_tune() methods are necessary.
    def embed(self, text: str) -> tuple[float, ...]:
        return float(len(text)), float(len(text.split()))


class OfflineGenerator:
    def generate(self, prompt: str) -> str:
        return f"Offline answer to: {prompt}"

    def stream(self, prompt: str) -> Iterator[str]:
        for word in self.generate(prompt).split():
            yield word + " "


def render_stream(generator: StreamingGenerator, prompt: str) -> Iterator[str]:
    """Expose a lazy iterator; an HTTP adapter would forward chunks to its client."""
    if not prompt.strip():
        raise ValueError("prompt must not be blank")
    yield from generator.stream(prompt)


def main() -> None:
    print(SemanticIndexer(LocalEmbeddingClient()).index("embedding example"))
    generator = OfflineGenerator()
    print(AnswerService(generator).answer("What is interface segregation?"))
    print("".join(render_stream(generator, "How does streaming work?")))


if __name__ == "__main__":
    main()
