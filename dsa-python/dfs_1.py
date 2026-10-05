"""Iterative depth-first search over a fixed-capacity adjacency matrix."""


class Vertex:
    def __init__(self, label: str) -> None:
        self.label = label


class MyGraphDFS:
    def __init__(self, max_vertices: int = 20) -> None:
        if max_vertices < 1:
            raise ValueError("max_vertices must be positive")
        self.max_vertices = max_vertices
        self.vertex_list: list[Vertex] = []
        self.adj_matrix = [[0] * max_vertices for _ in range(max_vertices)]

    @property
    def vertex_count(self) -> int:
        return len(self.vertex_list)

    def add_vertex(self, label: str) -> None:
        if self.vertex_count >= self.max_vertices:
            raise ValueError("graph has reached its vertex capacity")
        self.vertex_list.append(Vertex(label))

    def add_edge(self, start: int, end: int) -> None:
        self._validate_vertex(start)
        self._validate_vertex(end)
        self.adj_matrix[start][end] = 1
        self.adj_matrix[end][start] = 1

    def _validate_vertex(self, vertex: int) -> None:
        if not 0 <= vertex < self.vertex_count:
            raise IndexError("vertex is out of range")

    def display_matrix(self) -> None:
        labels = [vertex.label for vertex in self.vertex_list]
        print("Adjacency matrix:")
        print("   " + " ".join(labels))
        for index, label in enumerate(labels):
            row = " ".join(map(str, self.adj_matrix[index][: self.vertex_count]))
            print(f"{label}: {row}")

    def dfs(self, start_vertex: int = 0) -> list[str]:
        if self.vertex_count == 0:
            return []
        self._validate_vertex(start_vertex)

        visited = [False] * self.vertex_count
        result: list[str] = []
        stack = [start_vertex]
        while stack:
            vertex = stack.pop()
            if visited[vertex]:
                continue
            visited[vertex] = True
            result.append(self.vertex_list[vertex].label)
            # Reverse the push order so smaller neighbor indices are visited first.
            for neighbor in range(self.vertex_count - 1, -1, -1):
                if self.adj_matrix[vertex][neighbor] and not visited[neighbor]:
                    stack.append(neighbor)
        return result


def main() -> None:
    graph = MyGraphDFS()
    for label in "01234":
        graph.add_vertex(label)
    for start, end in ((0, 1), (0, 2), (0, 3), (1, 2), (2, 4)):
        graph.add_edge(start, end)

    graph.display_matrix()
    for start in range(graph.vertex_count):
        print(
            f"DFS from {graph.vertex_list[start].label}: {' '.join(graph.dfs(start))}"
        )

    complex_graph = MyGraphDFS()
    for label in "ABCDEF":
        complex_graph.add_vertex(label)
    for start, end in ((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (3, 4)):
        complex_graph.add_edge(start, end)
    print("Complex graph DFS:", " ".join(complex_graph.dfs()))


if __name__ == "__main__":
    main()
