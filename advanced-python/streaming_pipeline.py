"""Stream document embeddings through a bounded queue and fixed workers."""

from __future__ import annotations

import asyncio
import math
from collections.abc import AsyncIterable
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Document:
    document_id: str
    text: str


class Embedder(Protocol):
    async def embed(self, text: str) -> tuple[float, ...]: ...


class VectorSink(Protocol):
    async def upsert(self, document_id: str, vector: tuple[float, ...]) -> None: ...


async def index_documents(
    source: AsyncIterable[Document],
    embedder: Embedder,
    sink: VectorSink,
    *,
    workers: int = 3,
    queue_size: int = 6,
    item_timeout: float = 1.0,
) -> int:
    """Fail the pipeline on an item error; cancel all remaining tasks.

    Upserts completed before a failure remain committed. Use stable IDs and an
    idempotent sink when replaying a job. The caller owns the job deadline and
    resource lifecycle. Adapters must support concurrent async calls.
    """
    if workers < 1 or queue_size < 1:
        raise ValueError("workers and queue_size must be positive")
    if not math.isfinite(item_timeout) or item_timeout <= 0:
        raise ValueError("item_timeout must be finite and positive")
    queue: asyncio.Queue[Document | None] = asyncio.Queue(maxsize=queue_size)

    async def produce() -> None:
        async for document in source:
            await queue.put(document)  # Backpressure pauses the source.
        for _ in range(workers):
            await queue.put(None)  # One stop marker per consumer.

    async def consume() -> int:
        count = 0
        while True:
            document = await queue.get()
            try:
                if document is None:
                    return count
                async with asyncio.timeout(item_timeout):
                    vector = await embedder.embed(document.text)
                    await sink.upsert(document.document_id, vector)
                count += 1
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        group.create_task(produce(), name="document-source")
        consumers = [group.create_task(consume()) for _ in range(workers)]
    return sum(task.result() for task in consumers)


class FakeEmbedder:
    async def embed(self, text: str) -> tuple[float, ...]:
        await asyncio.sleep(0)
        return float(len(text)), float(len(text.split()))


class InMemorySink:
    """A small demo sink; a real sink persists vectors outside process memory."""

    def __init__(self) -> None:
        self.vectors: dict[str, tuple[float, ...]] = {}

    async def upsert(self, document_id: str, vector: tuple[float, ...]) -> None:
        self.vectors[document_id] = vector


async def main() -> None:
    async def documents() -> AsyncIterable[Document]:
        for index in range(10):
            yield Document(str(index), f"RAG document {index}")

    sink = InMemorySink()
    async with asyncio.timeout(5):
        count = await index_documents(documents(), FakeEmbedder(), sink)
    print(f"Indexed {count} documents")
    print(sink.vectors)


if __name__ == "__main__":
    asyncio.run(main())
