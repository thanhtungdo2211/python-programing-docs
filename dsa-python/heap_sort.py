def heapify(arr, n, i):
    """
    Hàm heapify để duy trì tính chất max heap.
    Tham số:
        arr: Mảng cần heapify
        n: Kích thước của heap
        i: Chỉ số của node gốc hiện tại
    """
    largest = i  # Khởi tạo largest là root
    left = 2 * i + 1  # Left child
    right = 2 * i + 2  # Right child

    # Kiểm tra xem left child có lớn hơn root không
    if left < n and arr[left] > arr[largest]:
        largest = left

    # Kiểm tra xem right child có lớn hơn root không
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Nếu largest không phải là root
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap
        # Gọi đệ quy để đảm bảo cây con cũng là max heap
        heapify(arr, n, largest)


def heap_sort(arr):
    """
    Thuật toán Heap Sort sử dụng max binary heap.
    Tham số:
        arr: Mảng cần sắp xếp
    Trả về:
        arr: Mảng đã sắp xếp
    """
    n = len(arr)

    # Xây dựng max heap (tái cấu trúc mảng)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Trích xuất từng phần tử từ heap
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # Swap
        heapify(arr, i, 0)
    
    return arr


# Example usage
if __name__ == "__main__":
    sample_array = [10, 7, 8, 9, 1, 5]
    sorted_array = heap_sort(sample_array)
    print("Sorted array:", sorted_array)