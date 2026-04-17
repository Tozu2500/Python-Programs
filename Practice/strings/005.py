# Remove whitespace from both ends of the string

# skt = "                  hello world                  "
# print(len(skt))

def remove_whitespace(text):
    # Remove whitespace from both ends manually
    start = 0
    end = len(text) - 1

    # Move the starting index forward while whitespace
    while start <= end and text[start].isspace():
        start += 1

    # Move the index backward while whitespace
    while end >= start and text[end].isspace():
        end -= 1

    return text[start:end + 1]

def main():
    final_string = input("Enter a string: ")
    final_string = remove_whitespace(final_string)
    print(f"{final_string}")
    length = len(final_string)
    print(f"\nLength of the final string in chars: {length}")

if __name__ == "__main__":
    main()