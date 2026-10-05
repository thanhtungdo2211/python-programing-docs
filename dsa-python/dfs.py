"""Recursive depth-first traversal over an adjacency matrix."""


def depth_first_search(adjacency: list[list[int]], start: int = 0) -> list[int]:
    """Return vertices reachable from start, in depth-first order."""
    vertex_count = len(adjacency)
    if any(len(row) != vertex_count for row in adjacency):
        raise ValueError("adjacency matrix must be square")
    if vertex_count == 0:
        return []
    if not 0 <= start < vertex_count:
        raise IndexError("start vertex is out of range")

    visited = [False] * vertex_count
    result: list[int] = []

    def visit(vertex: int) -> None:
        visited[vertex] = True
        result.append(vertex)
        for neighbor, connected in enumerate(adjacency[vertex]):
            if connected and not visited[neighbor]:
                visit(neighbor)

    visit(start)
    return result


def add_undirected_edge(adjacency: list[list[int]], first: int, second: int) -> None:
    adjacency[first][second] = 1
    adjacency[second][first] = 1


def main() -> None:
    vertex_count = 5
    adjacency = [[0] * vertex_count for _ in range(vertex_count)]
    edges = [(1, 2), (1, 0), (2, 0), (2, 3), (2, 4)]
    for first, second in edges:
        add_undirected_edge(adjacency, first, second)
    print(" ".join(map(str, depth_first_search(adjacency))))


if __name__ == "__main__":
    main()
