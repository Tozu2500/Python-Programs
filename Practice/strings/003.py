# Check if a string is palindrome

def check_palindrome(message):
    # Remove spaces and convert to lowercase
    cleaned_message = ''.join(char.lower() for char in message if char.isalnum())

    # Check for equal reverse
    return cleaned_message == cleaned_message[::-1]

# Testing
message = "Is this a palindrome"
message2 = "Madam"
if check_palindrome(message):
    print(f'"{message}" is a palindrome')
else:
    print(f'"{message}" is not a palindrome')

if check_palindrome(message2):
    print(f'"{message2}" is a palindrome')
else:
    print(f'"{message2} is not a palindrome')