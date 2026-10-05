"""Scoped request context and exception-safe startup of serving resources."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

request_id: ContextVar[str] = ContextVar("request_id", default="unscoped")


@contextmanager
def request_scope(identifier: str) -> Iterator[None]:
    if not identifier.strip():
        raise ValueError("request ID must not be empty")
    token = request_id.set(identifier)
    try:
        yield
    finally:
        # Reset the previous context, including for nested scopes and errors.
        request_id.reset(token)


@dataclass(slots=True)
class ServingResource:
    name: str
    closed: bool = False

    def close(self) -> None:
        self.closed = True
        print(f"Closed {self.name}")


def load_model() -> ServingResource:
    return ServingResource("embedding model")


def connect_vector_store() -> ServingResource:
    return ServingResource("vector store")


@contextmanager
def serving_resources() -> Iterator[tuple[ServingResource, ServingResource]]:
    """Clean up in reverse order, including when partial startup fails.

    In an async application use AsyncExitStack for async close methods.
    Startup/shutdown belongs to the application lifespan, not every request.
    """
    with ExitStack() as stack:
        model = load_model()
        stack.callback(model.close)  # Register cleanup immediately after acquisition.
        store = connect_vector_store()
        stack.callback(store.close)
        yield model, store


def main() -> None:
    with serving_resources() as (model, store):
        with request_scope("request-001"):
            print(f"{request_id.get()}: using {model.name} and {store.name}")
    print(f"Context after request: {request_id.get()}")


if __name__ == "__main__":
    main()
