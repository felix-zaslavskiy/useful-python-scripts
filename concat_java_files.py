import sys
import os
import re

def process_lines(lines):
    new_lines = []
    for line in lines:
        if not line.startswith('import ') and not line.startswith('package '):
            stripped_line = line.rstrip()
            if stripped_line:
                new_lines.append(stripped_line.lstrip() + '\n')
    return new_lines

def main():
    if len(sys.argv) < 2:
        print("Usage: python concat_java_files.py <file1.java> <file2.java> ...")
        sys.exit(1)

    java_files = sys.argv[1:]

    print("concat working")
    with open("concatenated_output.txt", "w") as output_file:
        for java_file in java_files:
            with open(java_file, "r") as input_file:
                # Print "// " before the filename
                output_file.write(f"// {java_file}\n\n")
                lines = input_file.readlines()
                processed_lines = process_lines(lines)

                file_text = "".join(processed_lines)
                file_text = file_text.rstrip() + '\n'

                output_file.write(file_text)


if __name__ == "__main__":
    main()
