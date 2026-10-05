"""Selection sort over a mutable list."""


def selection_sort(values: list[int]) -> list[int]:
    for index in range(len(values) - 1):
        minimum_index = index
        for candidate in range(index + 1, len(values)):
            if values[candidate] < values[minimum_index]:
                minimum_index = candidate
        if minimum_index != index:
            values[index], values[minimum_index] = values[minimum_index], values[index]
    return values


def main() -> None:
    values = [7, 2, 4, 1]
    print(selection_sort(values))


if __name__ == "__main__":
    main()
