import string
from collections import Counter

def word_frequency_counter(filename, top_n=10):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error reading the file. '{filename} wasn't found.")

    # Normalize text
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Word split
    words = text.split()

    # Word frequencies
    word_counts = Counter(words)

    most_common = word_counts.most_common(top_n)

    print(f"\nTop {top_n} most frequent words in '{filename}':\n")
    for word, count in most_common:
        print(f"{word}: {count}")

if __name__ == "__main__":
    filename = input("Enter the filename: ").strip()

    try:
        top_n = int(input("Enter number of top results (default 10): ").strip() or 10)
    except ValueError:
        top_n = 10

    word_frequency_counter(filename, top_n)