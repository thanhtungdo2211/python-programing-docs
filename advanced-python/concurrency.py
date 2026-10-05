"""Bounded inference fan-out with retries, deadlines, and cancellation.

Run with Python 3.11+. The fake provider performs no network requests.
"""

from __future__ import annotations

import asyncio
import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


class TransientProviderError(Exception):
    """A retryable failure such as an explicitly classified HTTP 429 or 503."""


class InferenceProvider(Protocol):
    async def predict(self, text: str) -> str: ...


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    attempts: int = 3
    attempt_timeout: float = 0.2
    base_delay: float = 0.01
    max_delay: float = 0.1

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("attempts must be positive")
        values = (self.attempt_timeout, self.base_delay, self.max_delay)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("retry timings must be finite")
        if self.attempt_timeout <= 0 or self.base_delay < 0 or self.max_delay < 0:
            raise ValueError("invalid retry timings")


async def predict_with_retry(
    provider: InferenceProvider,
    text: str,
    semaphore: asyncio.Semaphore,
    policy: RetryPolicy,
) -> str:
    for attempt in range(policy.attempts):
        try:
            # Release the concurrency slot before sleeping between retries.
            async with semaphore:
                async with asyncio.timeout(policy.attempt_timeout):
                    return await provider.predict(text)
        except (TransientProviderError, TimeoutError):
            if attempt + 1 == policy.attempts:
                raise
            ceiling = min(policy.max_delay, policy.base_delay * 2**attempt)
            await asyncio.sleep(random.uniform(0, ceiling))  # Full jitter.
    raise AssertionError("unreachable")


async def infer_batch(
    provider: InferenceProvider,
    texts: Sequence[str],
    *,
    concurrency: int = 3,
    batch_timeout: float = 2.0,
    policy: RetryPolicy = RetryPolicy(),
) -> list[str]:
    """Return results in input order; one terminal failure cancels siblings.

    This API accepts a small, materialized batch. Use streaming_pipeline.py
    for a large source: a semaphore alone does not bound the task count.
    """
    if concurrency < 1 or not math.isfinite(batch_timeout) or batch_timeout <= 0:
        raise ValueError("concurrency and batch_timeout must be positive")
    semaphore = asyncio.Semaphore(concurrency)
    async with asyncio.timeout(batch_timeout):
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(
                    predict_with_retry(provider, text, semaphore, policy),
                    name=f"inference-{index}",
                )
                for index, text in enumerate(texts)
            ]
    # Do not catch CancelledError: the request owner controls cancellation.
    return [task.result() for task in tasks]


class FakeProvider:
    def __init__(self) -> None:
        self.calls: dict[str, int] = {}

    async def predict(self, text: str) -> str:
        self.calls[text] = self.calls.get(text, 0) + 1
        await asyncio.sleep(0.01)
        if text == "retry me" and self.calls[text] == 1:
            raise TransientProviderError("simulated provider overload")
        return f"prediction:{text.upper()}"


async def main() -> None:
    provider = FakeProvider()
    results = await infer_batch(provider, ["classify", "retry me", "summarize"])
    print(results)
    print(f"Provider calls: {provider.calls}")


if __name__ == "__main__":
    asyncio.run(main())
