"""Stable, in-place insertion sort."""


def insertion_sort(values: list[int]) -> list[int]:
    for index in range(1, len(values)):
        current = index
        while current > 0 and values[current - 1] > values[current]:
            values[current - 1], values[current] = values[current], values[current - 1]
            current -= 1
    return values


def main() -> None:
    values = [2, 4, 6, 1, 5]
    print(insertion_sort(values))


if __name__ == "__main__":
    main()
