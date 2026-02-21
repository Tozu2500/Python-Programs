# Remove duplicates from a list

list_before = ["A", "A", "B", "C", "C", "D", "E"]
print(list_before)

list_after = list(set(list_before))
print(list_after)