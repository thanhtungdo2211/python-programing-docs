"""In-place quick sort with a three-way partition for duplicate values."""


def _partition(values: list[int], low: int, high: int) -> tuple[int, int]:
    pivot = values[(low + high) // 2]
    lower = current = low
    upper = high

    while current <= upper:
        if values[current] < pivot:
            values[lower], values[current] = values[current], values[lower]
            lower += 1
            current += 1
        elif values[current] > pivot:
            values[current], values[upper] = values[upper], values[current]
            upper -= 1
        else:
            current += 1
    return lower, upper


def quick_sort(values: list[int]) -> list[int]:
    """Sort values in place; duplicate-heavy inputs avoid repeated partitions."""

    def sort_range(low: int, high: int) -> None:
        while low < high:
            equal_start, equal_end = _partition(values, low, high)
            if equal_start - low < high - equal_end:
                sort_range(low, equal_start - 1)
                low = equal_end + 1
            else:
                sort_range(equal_end + 1, high)
                high = equal_start - 1

    sort_range(0, len(values) - 1)
    return values


def main() -> None:
    values = [10, 80, 30, 90, 40, 50, 70, 40]
    print(quick_sort(values))


if __name__ == "__main__":
    main()
