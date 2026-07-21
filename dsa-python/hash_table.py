class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # Mỗi bucket là một list rỗng

    def _hash_function(self, key):
        return hash(key) % self.size  # Ánh xạ khóa thành chỉ số

    def insert(self, key, value):
        index = self._hash_function(key)
        # Kiểm tra xem khóa đã tồn tại chưa
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value  # Cập nhật giá trị nếu khóa tồn tại
                return
        # Thêm cặp khóa-giá trị mới vào bucket
        self.table[index].append([key, value])

    def get(self, key):
        index = self._hash_function(key)
        # Tìm kiếm khóa trong bucket
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        raise KeyError(f"Key '{key}' không tồn tại")

    def delete(self, key):
        index = self._hash_function(key)
        # Xóa khóa khỏi bucket
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return
        raise KeyError(f"Key '{key}' không tồn tại")

# Sử dụng HashTable
ht = HashTable()
ht.insert("apple", 10)
ht.insert("banana", 20)
ht.insert("orange", 30)

print(ht.get("apple"))   # Output: 10
print(ht.get("banana"))  # Output: 20

ht.insert("apple", 100)  # Cập nhật giá trị của "apple"
print(ht.get("apple"))   # Output: 100

ht.delete("banana")
print(ht.get("banana"))  # Sẽ gây ra KeyError