

def bubble_sort(arr):
    n = len(arr)

    # Traverse through the elements
    for i in range(n):
        # Track for swaps
        swapped = False

        #Last i elements are already placed
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no two elements are swapped, the list is sorted
        if not swapped:
            break

    return arr

nums = [128, 64, 33, 90, 87, 33, 12, 5, 3, 83, 644, 23, 463]
print("Unsorted:", nums)
print("Sorted:", bubble_sort(nums))