"""A hash table that handles collisions with linked lists."""

from collections.abc import Hashable


class Node:
    def __init__(self, key: Hashable, value: object) -> None:
        self.key = key
        self.value = value
        self.next: Node | None = None


class HashTable:
    def __init__(self, size: int = 10) -> None:
        if size < 1:
            raise ValueError("size must be positive")
        self.size = size
        self.table: list[Node | None] = [None] * size

    def _hash_function(self, key: Hashable) -> int:
        return hash(key) % self.size

    def insert(self, key: Hashable, value: object) -> None:
        index = self._hash_function(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next

        node = Node(key, value)
        node.next = self.table[index]
        self.table[index] = node

    def get(self, key: Hashable) -> object:
        current = self.table[self._hash_function(key)]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(f"Key {key!r} not found")

    def delete(self, key: Hashable) -> None:
        index = self._hash_function(key)
        current = self.table[index]
        previous: Node | None = None
        while current is not None:
            if current.key == key:
                if previous is None:
                    self.table[index] = current.next
                else:
                    previous.next = current.next
                return
            previous, current = current, current.next
        raise KeyError(f"Key {key!r} not found")


def main() -> None:
    table = HashTable(size=1)  # Force collisions to demonstrate linked chaining.
    for key, value in (("apple", 10), ("banana", 20), ("orange", 30)):
        table.insert(key, value)
    print(table.get("apple"))
    table.insert("apple", 100)
    print("Updated apple:", table.get("apple"))
    table.delete("banana")
    try:
        table.get("banana")
    except KeyError as error:
        print(error)


if __name__ == "__main__":
    main()
