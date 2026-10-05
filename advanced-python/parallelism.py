"""CPU document preprocessing using a bounded, portable process pool."""

from __future__ import annotations

import hashlib
import multiprocessing
from collections.abc import Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DocumentFeatures:
    document_id: int
    token_count: int
    fingerprint: str


def featurize(document: tuple[int, str]) -> DocumentFeatures:
    """A top-level function and plain data can be serialized for spawn workers."""
    document_id, text = document
    tokens = text.casefold().split()
    normalized = " ".join(tokens).encode("utf-8")
    fingerprint = hashlib.sha256(normalized).hexdigest()
    return DocumentFeatures(document_id, len(tokens), fingerprint)


def preprocess(
    documents: Iterable[tuple[int, str]], *, workers: int = 2, max_pending: int = 4
) -> Iterator[DocumentFeatures]:
    """Yield completion order while keeping at most max_pending jobs submitted.

    IDs allow callers to restore input order. Small jobs can be slower than a
    serial loop because process startup and serialization have a cost.
    """
    if workers < 1 or max_pending < 1:
        raise ValueError("workers and max_pending must be positive")
    source = iter(documents)
    # Explicit spawn avoids relying on platform-specific fork behavior.
    with ProcessPoolExecutor(
        max_workers=workers, mp_context=multiprocessing.get_context("spawn")
    ) as pool:
        pending: set[Future[DocumentFeatures]] = set()
        exhausted = False
        try:
            while pending or not exhausted:
                while not exhausted and len(pending) < max_pending:
                    try:
                        document = next(source)
                    except StopIteration:
                        exhausted = True
                    else:
                        pending.add(pool.submit(featurize, document))
                if not pending:
                    break
                done, pending = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    yield future.result()  # Surface worker failures to the caller.
        finally:
            for future in pending:
                future.cancel()
            # Already running jobs finish when the pool context shuts down.


def main() -> None:
    documents = enumerate(["Vector search for RAG", "Model evaluation", "AI serving"])
    for features in sorted(preprocess(documents), key=lambda item: item.document_id):
        print(features)


if __name__ == "__main__":
    main()
