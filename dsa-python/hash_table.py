"""A separate-chaining hash table backed by Python lists."""

from collections.abc import Hashable


class HashTable:
    def __init__(self, size: int = 10) -> None:
        if size < 1:
            raise ValueError("size must be positive")
        self.size = size
        self.table: list[list[tuple[Hashable, object]]] = [[] for _ in range(size)]

    def _hash_function(self, key: Hashable) -> int:
        return hash(key) % self.size

    def insert(self, key: Hashable, value: object) -> None:
        bucket = self.table[self._hash_function(key)]
        for index, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: Hashable) -> object:
        bucket = self.table[self._hash_function(key)]
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        raise KeyError(f"Key {key!r} not found")

    def delete(self, key: Hashable) -> None:
        bucket = self.table[self._hash_function(key)]
        for index, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[index]
                return
        raise KeyError(f"Key {key!r} not found")


def main() -> None:
    table = HashTable(size=2)
    for key, value in (("apple", 10), ("banana", 20), ("orange", 30)):
        table.insert(key, value)
    print(table.get("apple"))
    print(table.get("banana"))
    table.insert("apple", 100)
    print("Updated apple:", table.get("apple"))
    table.delete("banana")
    try:
        table.get("banana")
    except KeyError as error:
        print(error)


if __name__ == "__main__":
    main()
