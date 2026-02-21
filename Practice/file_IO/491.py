# Read entire file content

from pathlib import Path

file_path = Path(r"D:\AAA_Coding_files\Python\Practice\file_IO\filename.txt")

with open(file_path, "r") as file:
    content = file.readlines()
    tabbed_content = ''.join(f"\n\t{line}" for line in content)
    print(f"{tabbed_content}\n")