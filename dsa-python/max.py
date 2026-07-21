def largest(A):
    my_max = A[0]
    for idx in range(1, len(A)):
        if my_max < A[idx]:
            my_max = A[idx]
    return my_max

def alternate(A):
    for v in A:
        v_is_largest = True
        for x in A:
            if v < x:
                v_is_largest = False
            break
    if v_is_largest:
        return v
    return None
A = [6, 6, 1, 18, 2]
print(alternate(A))
