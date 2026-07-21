"""Method overloading with ``singledispatchmethod`` and rich ordering."""

from dataclasses import dataclass
from datetime import date, datetime
from functools import singledispatchmethod, total_ordering
from typing import Any


class JsonEncoder:
    @singledispatchmethod
    def encode(self, value: object) -> Any:
        raise TypeError(f"unsupported value: {type(value).__name__}")

    @encode.register
    def _(self, value: date) -> str:
        return value.isoformat()

    @encode.register
    def _(self, value: datetime) -> str:
        return value.isoformat(timespec="seconds")

    @encode.register
    def _(self, value: set) -> list[Any]:
        return sorted(value)


@total_ordering
@dataclass(frozen=True, eq=False)
class Version:
    major: int
    minor: int
    patch: int = 0

    @property
    def _key(self) -> tuple[int, int, int]:
        return self.major, self.minor, self.patch

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key == other._key

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._key < other._key


def main() -> None:
    encoder = JsonEncoder()
    print(encoder.encode(datetime(2026, 7, 21, 9, 30)))
    print(encoder.encode({3, 1, 2}))
    print(Version(2, 0) > Version(1, 9, 9))


if __name__ == "__main__":
    main()
