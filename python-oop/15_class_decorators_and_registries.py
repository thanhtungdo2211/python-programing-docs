"""A class decorator that builds an explicit plugin registry."""

from collections.abc import Callable
from typing import ClassVar, Protocol, TypeVar


class Handler(Protocol):
    def handle(self, payload: str) -> str: ...


H = TypeVar("H", bound=type[Handler])


class HandlerRegistry:
    _handlers: ClassVar[dict[str, type[Handler]]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[H], H]:
        def decorator(handler_class: H) -> H:
            if name in cls._handlers:
                raise ValueError(f"handler {name!r} is already registered")
            cls._handlers[name] = handler_class
            return handler_class

        return decorator

    @classmethod
    def create(cls, name: str) -> Handler:
        try:
            handler_class = cls._handlers[name]
        except KeyError as error:
            raise LookupError(f"unknown handler: {name!r}") from error
        return handler_class()


@HandlerRegistry.register("uppercase")
class UppercaseHandler:
    def handle(self, payload: str) -> str:
        return payload.upper()


@HandlerRegistry.register("reverse")
class ReverseHandler:
    def handle(self, payload: str) -> str:
        return payload[::-1]


def main() -> None:
    for name in ("uppercase", "reverse"):
        print(HandlerRegistry.create(name).handle("Decorator registry"))


if __name__ == "__main__":
    main()
