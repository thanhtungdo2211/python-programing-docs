"""Lazy per-instance computation with ``functools.cached_property``."""

from functools import cached_property
from statistics import fmean


class DataSet:
    def __init__(self, values: list[float]) -> None:
        if not values:
            raise ValueError("values cannot be empty")
        self._values = list(values)

    @property
    def values(self) -> tuple[float, ...]:
        return tuple(self._values)

    @cached_property
    def mean(self) -> float:
        """Compute once, then store the result in this instance's ``__dict__``."""
        print("Computing mean...")
        return fmean(self._values)

    def append(self, value: float) -> None:
        self._values.append(value)
        self.__dict__.pop("mean", None)  # Invalidate derived cached state.


def main() -> None:
    data = DataSet([10.0, 20.0, 30.0])
    print(data.mean)
    print(data.mean)  # Uses the cached value.
    data.append(40.0)
    print(data.mean)  # Recomputes after invalidation.


if __name__ == "__main__":
    main()
