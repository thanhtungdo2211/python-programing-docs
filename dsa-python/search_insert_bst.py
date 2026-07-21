class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)
        
    def _insert_recursive(self, root, key):
        if root is None:
            return Node(key)
        
        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
            
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)
            
        return root
    
    def search(self, key):
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, root, key):
        if root is None or root.key == key:
            return root
        
        if key < root.key:
            return self._search_recursive(root.left, key)

        return self._search_recursive(root.right, key)
    
    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, root, result):
        if root:
            self._inorder_recursive(root.left, result)
            result.append(root.key)
            self._inorder_recursive(root.right, result)

bst = BinarySearchTree()

values_to_insert = [50, 30, 70, 20, 40, 60, 80]
print("Chèn các giá trị:", values_to_insert)
for value in values_to_insert:
    bst.insert(value)

# Hiển thị cây theo thứ tự tăng dần
print("Cây sau khi chèn (inorder):", bst.inorder_traversal())

# Tìm kiếm một số giá trị
values_to_search = [40, 55, 90]
for value in values_to_search:
    result = bst.search(value)
    if result:
        print(f"Tìm thấy {value} trong cây")
    else:
        print(f"Không tìm thấy {value} trong cây")

# Chèn thêm giá trị mới
new_value = 55
print(f"Chèn giá trị mới: {new_value}")
bst.insert(new_value)

# Hiển thị cây sau khi chèn giá trị mới
print("Cây sau khi chèn (inorder):", bst.inorder_traversal())

# Kiểm tra giá trị vừa chèn
result = bst.search(new_value)
if result:
    print(f"Đã chèn thành công: Tìm thấy {new_value} trong cây")

