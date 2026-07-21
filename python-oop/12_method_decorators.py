"""Type-safe decorators for methods using ``ParamSpec`` and ``functools.wraps``."""

from collections.abc import Callable
from functools import wraps
from typing import Concatenate, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
T = TypeVar("T")


def audit_method(
    function: Callable[Concatenate[T, P], R],
) -> Callable[Concatenate[T, P], R]:
    """Log a method call while preserving its metadata and type signature."""

    @wraps(function)
    def wrapper(self: T, /, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"AUDIT {type(self).__name__}.{function.__name__}")
        return function(self, *args, **kwargs)

    return wrapper


def require_role(role: str) -> Callable[[Callable[Concatenate[T, P], R]], Callable[Concatenate[T, P], R]]:
    """A parameterized authorization decorator for service methods."""

    def decorator(
        function: Callable[Concatenate[T, P], R],
    ) -> Callable[Concatenate[T, P], R]:
        @wraps(function)
        def wrapper(self: T, /, *args: P.args, **kwargs: P.kwargs) -> R:
            roles = getattr(self, "roles", frozenset())
            if role not in roles:
                raise PermissionError(f"the {role!r} role is required")
            return function(self, *args, **kwargs)

        return wrapper

    return decorator


class UserService:
    def __init__(self, roles: set[str]) -> None:
        self.roles = frozenset(roles)

    @audit_method
    @require_role("admin")
    def deactivate(self, user_id: int, *, reason: str) -> str:
        return f"Deactivated user {user_id}: {reason}"


def main() -> None:
    service = UserService({"admin"})
    print(service.deactivate(42, reason="duplicate account"))
    print(f"Preserved method name: {service.deactivate.__name__}")


if __name__ == "__main__":
    main()
