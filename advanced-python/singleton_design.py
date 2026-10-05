"""Application-owned model registry instead of an implicit global singleton.

A singleton is only process-local and can obscure configuration and cleanup.
This registry is explicitly injected, has bounded ownership, and is testable.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from threading import Lock
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ModelKey:
    name: str
    revision: str
    device: str = "cpu"


class Model(Protocol):
    def predict(self, text: str) -> str: ...

    def close(self) -> None: ...


class ModelRegistry:
    """Load each key once under a lock; own models for one application lifetime.

    The simple lock serializes loading for different keys too. For slow loaders,
    use per-key synchronization. This lock does not make model inference safe:
    the serving layer must honor the underlying runtime's threading contract.
    """

    def __init__(
        self, loader: Callable[[ModelKey], Model], *, capacity: int = 2
    ) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._loader = loader
        self._capacity = capacity
        self._models: dict[ModelKey, Model] = {}
        self._lock = Lock()
        self._closed = False

    def get(self, key: ModelKey) -> Model:
        with self._lock:
            if self._closed:
                raise RuntimeError("registry is closed")
            if key not in self._models:
                if len(self._models) >= self._capacity:
                    raise RuntimeError("model capacity exceeded")
                # A failed loader is not cached; a later request may try again.
                self._models[key] = self._loader(key)
            return self._models[key]

    def close(self) -> None:
        """Close after requests drain; attempt every cleanup even if one fails."""
        with self._lock:
            if self._closed:
                return
            self._closed = True
            models = list(self._models.values())
            self._models.clear()
        errors: list[Exception] = []
        for model in models:
            try:
                model.close()
            except Exception as error:
                errors.append(error)
        if errors:
            raise ExceptionGroup("model cleanup failed", errors)


class FakeModel:
    def __init__(self, key: ModelKey) -> None:
        self.key = key
        self.closed = False

    def predict(self, text: str) -> str:
        if self.closed:
            raise RuntimeError("model is closed")
        return f"{self.key.name}@{self.key.revision}: {text.upper()}"

    def close(self) -> None:
        self.closed = True


def main() -> None:
    registry = ModelRegistry(FakeModel)
    try:
        key = ModelKey("classifier", "v1")
        model = registry.get(key)
        print(f"Same model instance: {model is registry.get(key)}")
        print(model.predict("customer feedback"))
    finally:
        registry.close()


if __name__ == "__main__":
    main()
