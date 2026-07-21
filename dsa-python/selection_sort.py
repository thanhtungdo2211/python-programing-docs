def selection_sort(array):
    array_lenght = len(array)
    
    for i in range(array_lenght-1):
        min_index = i
        for j in range(i+1, array_lenght):
            if array[j] < array[min_index]:
                min_index = j
        if min_index != i:        
            array[i], array[min_index] = array[min_index], array[i] # Swap
    
    return array
    
# Example usage
array = [7, 2, 4, 1]

# Step-by-step illustration of selection sort:
# Initial array: [7, 2, 4, 1]

# Pass 1:
# Find the minimum element in the unsorted part [7, 2, 4, 1]
# Minimum is 1 at index 3
# Swap 7 and 1
# Array after Pass 1: [1, 2, 4, 7]

# Pass 2:
# Find the minimum element in the unsorted part [2, 4, 7]
# Minimum is 2 at index 1
# No swap needed
# Array after Pass 2: [1, 2, 4, 7]

# Pass 3:
# Find the minimum element in the unsorted part [4, 7]
# Minimum is 4 at index 2
# No swap needed
# Array after Pass 3: [1, 2, 4, 7]

# Final sorted array: [1, 2, 4, 7]
sorted_array = selection_sort(array=array)

print(sorted_array)