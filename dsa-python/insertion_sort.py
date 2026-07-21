def insertion_sort(array):
    array_lenght = len(array)
    
    for i in range(1, array_lenght):
        for j in range(i, 0, -1):
            if array[j-1] <= array[j]:
                break
            array[j], array[j-1] = array[j-1], array[j]
    
    return array

array = [2, 4, 6, 1, 5]
sorted_array = insertion_sort(array=array)

print(sorted_array)