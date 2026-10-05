"""DIP: RAG orchestration depends on application ports, not vendor SDKs.

The composition root chooses adapters. Constructor injection is the mechanism;
placing the abstraction at the application boundary is the design principle.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


class HardwiredRAGService:
    """Anti-pattern: high-level policy constructs concrete infrastructure."""

    def __init__(self) -> None:
        self.retriever = InMemoryRetriever(
            [Document("doc-1", "Python supports protocols")]
        )
        self.generator = ExtractiveGenerator()

    def answer(self, question: str) -> str:
        documents = self.retriever.search(question, limit=2)
        return self.generator.generate(question, documents)


@dataclass(frozen=True, slots=True)
class Document:
    document_id: str
    text: str


@dataclass(frozen=True, slots=True)
class Answer:
    text: str
    source_ids: tuple[str, ...]


class Retriever(Protocol):
    def search(self, query: str, *, limit: int) -> Sequence[Document]: ...


class GroundedGenerator(Protocol):
    def generate(self, question: str, context: Sequence[Document]) -> str: ...


class RAGService:
    def __init__(
        self, retriever: Retriever, generator: GroundedGenerator, *, top_k: int = 2
    ) -> None:
        if top_k < 1:
            raise ValueError("top_k must be positive")
        self._retriever = retriever
        self._generator = generator
        self._top_k = top_k

    def answer(self, question: str) -> Answer:
        if not question.strip():
            raise ValueError("question must not be blank")
        documents = tuple(self._retriever.search(question, limit=self._top_k))
        if not documents:
            return Answer("No supporting documents found.", ())
        text = self._generator.generate(question, documents)
        # These are supplied context IDs, not proof of claim-level grounding.
        return Answer(text, tuple(document.document_id for document in documents))


class InMemoryRetriever:
    """Deterministic lexical search; replace with a vector-store adapter."""

    def __init__(self, documents: Sequence[Document]) -> None:
        self._documents = tuple(documents)

    def search(self, query: str, *, limit: int) -> Sequence[Document]:
        if limit < 1:
            raise ValueError("limit must be positive")
        terms = set(query.casefold().split())
        matches = [
            (len(terms & set(document.text.casefold().split())), document)
            for document in self._documents
        ]
        matches.sort(key=lambda item: (-item[0], item[1].document_id))
        return [document for score, document in matches if score > 0][:limit]


class ExtractiveGenerator:
    def generate(self, question: str, context: Sequence[Document]) -> str:
        return " ".join(document.text for document in context)


def build_service() -> RAGService:
    """Composition root: this is where concrete infrastructure is selected."""
    documents = [
        Document("doc-1", "Python protocols describe application interfaces"),
        Document("doc-2", "Dependency injection simplifies adapter testing"),
    ]
    return RAGService(InMemoryRetriever(documents), ExtractiveGenerator())


def main() -> None:
    service = build_service()
    print(service.answer("Python protocols"))
    print(service.answer("unmatched"))


if __name__ == "__main__":
    main()
