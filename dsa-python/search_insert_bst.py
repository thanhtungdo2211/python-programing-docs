"""Search and insert values using the shared binary search tree example."""

from balancing_bst import BinarySearchTree


def main() -> None:
    tree = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    for value in values:
        tree.insert(value)
    print("Values after insertion:", tree.inorder_traversal())

    for value in (40, 55, 90):
        found = tree.search(value) is not None
        print(f"{value} {'found' if found else 'not found'}")

    new_value = 55
    tree.insert(new_value)
    print(f"Inserted {new_value}:", tree.search(new_value) is not None)
    print("Values after insertion:", tree.inorder_traversal())


if __name__ == "__main__":
    main()
