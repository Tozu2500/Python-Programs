# Quicksort

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

if __name__ == "__main__":
    sample_array = [3, 6, 7, 2, 1, 5, 4, 8, 9, 10, 15, 12]
    sorted_array = quicksort(sample_array)
    print("Unsorted array:", sample_array)
    print("Sorted array:", sorted_array)
