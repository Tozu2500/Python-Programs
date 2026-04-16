# Convert string to uppercase without using the upper() method at all

def uppercase(text):
    result = ""
    
    for char in text:
        # Checking if the 'char' is a lowercase letter (ASCII numbers 97-122)
        if 'a' <= char <= 'z':
            # Convert by subtracting 32 from the ASCII code
            result += chr(ord(char) - 32)
        else:
            result += char
    return result

def main():
    print(uppercase("Hello, World!"))

if __name__ == "__main__":
    main()
