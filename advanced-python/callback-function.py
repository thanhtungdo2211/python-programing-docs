"""Typed training callbacks with explicit failure and stopping semantics."""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class EpochMetrics:
    epoch: int
    validation_loss: float

    def __post_init__(self) -> None:
        if self.epoch < 1 or not math.isfinite(self.validation_loss):
            raise ValueError("epoch must be positive and loss must be finite")


class TrainingCallback(Protocol):
    def __call__(self, metrics: EpochMetrics) -> bool:
        """Return True to continue training, or False to request a stop."""
        ...


class EarlyStopping:
    def __init__(self, *, patience: int = 2, min_delta: float = 0.0) -> None:
        if patience < 1 or not math.isfinite(min_delta) or min_delta < 0:
            raise ValueError("invalid early stopping configuration")
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = math.inf
        self.stale_epochs = 0

    def __call__(self, metrics: EpochMetrics) -> bool:
        if metrics.validation_loss < self.best_loss - self.min_delta:
            self.best_loss = metrics.validation_loss
            self.stale_epochs = 0
        else:
            self.stale_epochs += 1
        return self.stale_epochs < self.patience


class MetricsRecorder:
    """An in-memory observer; use a telemetry adapter in a real trainer."""

    def __init__(self) -> None:
        self.history: list[EpochMetrics] = []

    def __call__(self, metrics: EpochMetrics) -> bool:
        self.history.append(metrics)
        return True


def train(
    validation_losses: Iterable[float], callbacks: Sequence[TrainingCallback]
) -> int:
    """Simulate a training loop; callback failures abort the run.

    Instantiate stateful callbacks per run. Slow telemetry or checkpoint I/O
    belongs behind a bounded queue rather than inside this synchronous hook.
    """
    completed = 0
    for epoch, loss in enumerate(validation_losses, start=1):
        metrics = EpochMetrics(epoch, loss)
        # Invoke every observer, even when an earlier callback requests a stop.
        decisions = [callback(metrics) for callback in callbacks]
        completed = epoch
        if not all(decisions):
            break
    return completed


def main() -> None:
    recorder = MetricsRecorder()
    stopping = EarlyStopping(patience=2, min_delta=0.01)
    epochs = train([0.9, 0.6, 0.5, 0.505, 0.51, 0.4], [stopping, recorder])
    print(f"Stopped after {epochs} epochs; best loss: {stopping.best_loss}")
    print(recorder.history)


if __name__ == "__main__":
    main()
