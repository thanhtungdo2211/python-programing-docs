"""A simple, unbalanced binary search tree for learning purposes."""

from __future__ import annotations


class Node:
    def __init__(self, key: int) -> None:
        self.key = key
        self.left: Node | None = None
        self.right: Node | None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, key: int) -> None:
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, root: Node | None, key: int) -> Node:
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)
        return root

    def search(self, key: int) -> Node | None:
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def inorder_traversal(self) -> list[int]:
        result: list[int] = []

        def visit(node: Node | None) -> None:
            if node is not None:
                visit(node.left)
                result.append(node.key)
                visit(node.right)

        visit(self.root)
        return result


def main() -> None:
    tree = BinarySearchTree()
    for key in (5, 3, 7, 1, 9):
        tree.insert(key)

    print("Inorder traversal:", tree.inorder_traversal())
    for key in (7, 8):
        node = tree.search(key)
        print(f"Search for {key}: {node.key if node else 'not found'}")


if __name__ == "__main__":
    main()
