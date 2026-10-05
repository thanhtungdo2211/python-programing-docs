"""Two ways to find the largest value in a non-empty sequence."""

from collections.abc import Sequence


def largest(values: Sequence[int]) -> int:
    """Find the maximum in O(n) time and O(1) extra space."""
    if not values:
        raise ValueError("values must not be empty")
    current_max = values[0]
    for value in values[1:]:
        if value > current_max:
            current_max = value
    return current_max


def largest_by_comparison(values: Sequence[int]) -> int:
    """Find a maximum by comparing each candidate with every other value."""
    if not values:
        raise ValueError("values must not be empty")
    for candidate in values:
        if all(candidate >= value for value in values):
            return candidate
    raise AssertionError("a finite sequence must contain a maximum")


def main() -> None:
    values = [6, 6, 1, 18, 2]
    print("Linear scan:", largest(values))
    print("Pairwise comparison:", largest_by_comparison(values))


if __name__ == "__main__":
    main()
