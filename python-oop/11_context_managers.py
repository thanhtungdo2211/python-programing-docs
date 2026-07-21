"""Class-based, generator-based, and asynchronous context managers."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator
from contextlib import AbstractContextManager, asynccontextmanager, contextmanager
from types import TracebackType


class ManagedConnection(AbstractContextManager["ManagedConnection"]):
    def __init__(self, name: str) -> None:
        self.name = name
        self.is_open = False

    def __enter__(self) -> ManagedConnection:
        self.is_open = True
        print(f"Opened {self.name}")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        self.is_open = False
        print(f"Closed {self.name}")
        return False  # Never hide exceptions.

    @contextmanager
    def transaction(self) -> Iterator[None]:
        if not self.is_open:
            raise RuntimeError("connection must be open")
        print("Begin transaction")
        try:
            yield
        except Exception:
            print("Roll back transaction")
            raise
        else:
            print("Commit transaction")


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.connected = False

    @asynccontextmanager
    async def session(self) -> AsyncIterator[ApiClient]:
        self.connected = True
        print(f"Connected to {self.base_url}")
        try:
            yield self
        finally:
            self.connected = False
            print("Disconnected API client")


async def async_example() -> None:
    client = ApiClient("https://api.example.test")
    async with client.session() as active_client:
        print(f"Client ready: {active_client.connected}")


def main() -> None:
    with ManagedConnection("primary-db") as connection:
        with connection.transaction():
            print("Update completed")
    asyncio.run(async_example())


if __name__ == "__main__":
    main()
