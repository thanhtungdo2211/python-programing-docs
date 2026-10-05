"""Binary search over a sequence sorted in ascending order."""

from collections.abc import Sequence


def binary_search(values: Sequence[int], target: int) -> bool:
    """Return whether target occurs in the sorted sequence."""
    low = 0
    high = len(values) - 1

    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return True
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return False


def main() -> None:
    values = list(range(1, 11))
    target = 3
    print(binary_search(values, target))


if __name__ == "__main__":
    main()
