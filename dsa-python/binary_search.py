def bas(A, target):
    low = 0
    high = len(A) - 1
    while low <= high:
        mid = (low + high) // 2
        if A[mid] > target:
            high = mid - 1
        elif A[mid] < target:
            low = mid + 1
        else:
            return True
    return False

A = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 3
print(bas(A, target))