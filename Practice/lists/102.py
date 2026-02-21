# Find 2nd largest element from a list

numbers = [7, 11, 15, 25, 30]

largest = second_largest = float('-inf')
# print(largest)

if len(numbers) >= 2:
    for num in numbers:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num

print(f"The second largest element is {second_largest}")