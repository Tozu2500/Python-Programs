# Read a file into a list

from pathlib import Path

file_path = Path(r"D:\AAA_Coding_files\Python\Practice\file_IO\filename.txt")

if file_path.exists():
    try:
        with open(file_path, "r") as file:
            # lines = [line.strip() for line in file]
            lines = file.readlines()
        print(lines)
    except FileNotFoundError:
        print("The file 'filename.txt' was not found")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("BAD")