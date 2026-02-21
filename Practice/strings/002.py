# Count vowels in a string

message = "Counting vowels here!"

total_vowels = 0

wovels = ["A", "E", "I", "O", "U"]

# Uppercase the message
for letter in message.upper():
    if letter in wovels:
        total_vowels += 1

print(f"Total vowels: {total_vowels}")