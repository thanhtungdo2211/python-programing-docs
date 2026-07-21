class Vertex:
    def __init__(self, label):
        self.label = label
        self.visited = False

class MyGraphDFS:
    def __init__(self):
        self.max_vertices = 20
        self.vertex_list = [None] * self.max_vertices
        self.adj_matrix = [[0 for _ in range(self.max_vertices)] 
                          for _ in range(self.max_vertices)]
        self.vertex_count = 0
        self.stack = []  # Python list làm stack
    
    def add_vertex(self, label):
        """Thêm đỉnh mới vào đồ thị"""
        self.vertex_list[self.vertex_count] = Vertex(label)
        self.vertex_count += 1
    
    def add_edge(self, start, end):
        """Thêm cạnh giữa hai đỉnh (đồ thị vô hướng)"""
        self.adj_matrix[start][end] = 1
        self.adj_matrix[end][start] = 1
    
    def display_vertex(self, v):
        """Hiển thị đỉnh"""
        print(self.vertex_list[v].label, end=" ")
    
    def dfs(self):
        """Thuật toán DFS sử dụng stack"""
        # Bắt đầu từ đỉnh 0
        self.vertex_list[0].visited = True
        self.display_vertex(0)
        self.stack.append(0)
        
        while self.stack:
            # Lấy đỉnh kề chưa thăm của đỉnh trên đỉnh stack
            v = self.get_adj_unvisited_vertex(self.stack[-1])  # peek()
            if v == -1:
                self.stack.pop()
            else:
                self.vertex_list[v].visited = True
                self.display_vertex(v)
                self.stack.append(v)
        
        # Reset trạng thái visited cho lần duyệt tiếp theo
        for j in range(self.vertex_count):
            self.vertex_list[j].visited = False
    
    def get_adj_unvisited_vertex(self, v):
        """Tìm đỉnh kề chưa thăm đầu tiên của đỉnh v"""
        for j in range(self.vertex_count):
            if (self.adj_matrix[v][j] == 1 and 
                not self.vertex_list[j].visited):
                return j
        return -1
    
    def display_matrix(self):
        """Hiển thị ma trận kề (thêm để debug)"""
        print("\nMa trận kề:")
        print("  ", end="")
        for i in range(self.vertex_count):
            print(f"{self.vertex_list[i].label} ", end="")
        print()
        
        for i in range(self.vertex_count):
            print(f"{self.vertex_list[i].label} ", end="")
            for j in range(self.vertex_count):
                print(f"{self.adj_matrix[i][j]} ", end="")
            print()
    
    def dfs_from_vertex(self, start_vertex):
        """DFS bắt đầu từ đỉnh chỉ định"""
        # Reset visited
        for j in range(self.vertex_count):
            self.vertex_list[j].visited = False
        
        self.vertex_list[start_vertex].visited = True
        self.display_vertex(start_vertex)
        self.stack = [start_vertex]
        
        while self.stack:
            v = self.get_adj_unvisited_vertex(self.stack[-1])
            if v == -1:
                self.stack.pop()
            else:
                self.vertex_list[v].visited = True
                self.display_vertex(v)
                self.stack.append(v)

# Chương trình chính
if __name__ == "__main__":
    # Tạo đồ thị giống như trong Java
    g = MyGraphDFS()
    
    # Thêm các đỉnh
    g.add_vertex('0')
    g.add_vertex('1')
    g.add_vertex('2')
    g.add_vertex('3')
    g.add_vertex('4')
    
    # Thêm các cạnh (đồ thị vô hướng)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(0, 3)
    g.add_edge(1, 2)
    g.add_edge(2, 4)
    
    print("Cấu trúc đồ thị:")
    g.display_matrix()
    
    print("\nDFS traversal starting from vertex 0:")
    g.dfs()
    
    print("\n\nDFS từ các đỉnh khác nhau:")
    for i in range(g.vertex_count):
        print(f"\nDFS từ đỉnh {g.vertex_list[i].label}: ", end="")
        g.dfs_from_vertex(i)
    
    print("\n")
    
    # Ví dụ thêm với đồ thị phức tạp hơn
    print("\n=== ĐỒNG THỊ PHỨC TẠP HỞN ===")
    g2 = MyGraphDFS()
    
    # Thêm đỉnh với ký tự
    vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    for vertex in vertices:
        g2.add_vertex(vertex)
    
    # Tạo đồ thị dạng cây + một số cạnh thêm
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (3, 4)]
    for start, end in edges:
        g2.add_edge(start, end)
    
    print("Cấu trúc đồ thị 2:")
    g2.display_matrix()
    
    print(f"\nDFS traversal từ A: ", end="")
    g2.dfs_from_vertex(0)
    print()