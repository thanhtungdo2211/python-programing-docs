class Node:
    """Lớp Node đại diện cho một phần tử trong linked list."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    """Bảng băm sử dụng linked list để xử lý va chạm."""
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size  # Mỗi bucket là một linked list (ban đầu là None)

    def _hash_function(self, key):
        """Hàm băm trả về index dựa trên key."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Thêm hoặc cập nhật cặp key-value vào bảng băm."""
        index = self._hash_function(key)
        current = self.table[index]

        # Kiểm tra xem key đã tồn tại trong linked list chưa
        while current:
            if current.key == key:
                current.value = value  # Cập nhật giá trị nếu key tồn tại
                return
            current = current.next

        # Nếu key chưa tồn tại, thêm node mới vào đầu linked list
        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node

    def get(self, key):
        """Lấy giá trị từ key."""
        index = self._hash_function(key)
        current = self.table[index]

        # Duyệt linked list để tìm key
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"Key '{key}' không tồn tại")

    def delete(self, key):
        """Xóa cặp key-value khỏi bảng băm."""
        index = self._hash_function(key)
        current = self.table[index]
        previous = None

        # Duyệt linked list để tìm key
        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next  # Bỏ qua node cần xóa
                else:
                    self.table[index] = current.next  # Cập nhật head nếu xóa node đầu
                return
            previous = current
            current = current.next

        raise KeyError(f"Key '{key}' không tồn tại")

# Sử dụng HashTable với linked list
ht = HashTable()
ht.insert("apple", 10)
ht.insert("banana", 20)
ht.insert("orange", 30)

print(ht.get("apple"))    # Output: 10
print(ht.get("banana"))   # Output: 20

ht.insert("apple", 100)   # Cập nhật giá trị của "apple"
print(ht.get("apple"))    # Output: 100

ht.delete("banana")
# print(ht.get("banana")) # Sẽ gây ra KeyError