"""Measure serial I/O, threaded I/O, and pure Python CPU preprocessing.

The I/O adapter simulates a blocking SDK. No network or credentials are needed.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

from parallelism import featurize, preprocess

T = TypeVar("T")


def blocking_download(document_id: int) -> tuple[int, str]:
    """Stand in for an object-store SDK configured with its own I/O timeout."""
    time.sleep(0.02)
    return document_id, f"Document {document_id} about embeddings and retrieval"


def measure(label: str, operation: Callable[[], T]) -> T:
    start = time.perf_counter()
    result = operation()
    print(f"{label}: {time.perf_counter() - start:.4f}s")
    return result


def main() -> None:
    ids = range(8)
    serial = measure("Serial blocking I/O", lambda: [blocking_download(i) for i in ids])
    # A small fixed batch is appropriate here. Executor.map on Python 3.11
    # eagerly submits input; use bounded submission for an unbounded source.
    with ThreadPoolExecutor(max_workers=4) as pool:
        threaded = measure(
            "Threaded blocking I/O", lambda: list(pool.map(blocking_download, ids))
        )
    serial_features = measure(
        "Serial CPU work", lambda: [featurize(doc) for doc in serial]
    )
    process_features = measure("Process CPU work", lambda: list(preprocess(threaded)))
    assert (
        sorted(process_features, key=lambda item: item.document_id) == serial_features
    )
    print("Outputs match; process overhead dominates this deliberately small workload.")


if __name__ == "__main__":
    main()
