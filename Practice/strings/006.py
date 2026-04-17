# Count occurrences of a character in a string
# Two ways

string1 = "how are you doing?"
look_for = "h"

occurrences = string1.count(look_for)
print(f"\n{string1} \ncontains {look_for} {occurrences} time(s)")

############################################################

string2 = "banana"
char = "a"

count = 0
for ch in string2:
    if ch == char:
        count += 1

print(f"\n{string2} \ncontains {char} {count} time(s)")
