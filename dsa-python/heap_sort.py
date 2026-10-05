"""In-place heap sort using a max heap."""


def _sift_down(values: list[int], heap_size: int, root: int) -> None:
    while True:
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < heap_size and values[left] > values[largest]:
            largest = left
        if right < heap_size and values[right] > values[largest]:
            largest = right
        if largest == root:
            return
        values[root], values[largest] = values[largest], values[root]
        root = largest


def heap_sort(values: list[int]) -> list[int]:
    """Sort values in place and return the same list."""
    heap_size = len(values)
    for root in range(heap_size // 2 - 1, -1, -1):
        _sift_down(values, heap_size, root)

    for end in range(heap_size - 1, 0, -1):
        values[0], values[end] = values[end], values[0]
        _sift_down(values, end, 0)
    return values


def main() -> None:
    values = [10, 7, 8, 9, 1, 5]
    print("Sorted array:", heap_sort(values))


if __name__ == "__main__":
    main()
