"""Stable merge sort that returns a new sorted list."""

from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: list[T]) -> list[T]:
    if len(values) <= 1:
        return values.copy()
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    return merge(left, right)


def merge(left: list[T], right: list[T]) -> list[T]:
    merged: list[T] = []
    left_index = right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def main() -> None:
    values = [4, 5, 1, 10, 3, 5]
    print(merge_sort(values))
    print("Original list:", values)


if __name__ == "__main__":
    main()
