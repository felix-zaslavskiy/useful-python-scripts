import sys
import os
import argparse

def process_lines(lines):
    new_lines = []
    for line in lines:
        if not line.startswith('import ') and not line.startswith('package '):
            stripped_line = line.rstrip()
            if stripped_line:
                new_lines.append(stripped_line.lstrip() + '\n')
    return new_lines

def main():
    parser = argparse.ArgumentParser(description="Concatenate Java files from a list or a directory.")
    parser.add_argument('-f', '--files', nargs='+', help="List of Java files to concatenate.")
    parser.add_argument('-d', '--directory', help="Directory containing Java files to concatenate.")

    args = parser.parse_args()

    java_files = []
    if args.files:
        java_files = args.files
    elif args.directory:
        if not os.path.isdir(args.directory):
            print("Provided directory does not exist.")
            sys.exit(1)
        java_files = [os.path.join(args.directory, f) for f in os.listdir(args.directory) if f.endswith('.java')]
        if not java_files:
            print("No Java files found in the directory.")
            sys.exit(1)
    else:
        print("No files or directory provided.")
        sys.exit(1)

    with open("concatenated_output.txt", "w") as output_file:
        for java_file in java_files:
            with open(java_file, "r") as input_file:
                # Print "// " before the filename
                output_file.write(f"// {java_file}\n\n")
                lines = input_file.read().splitlines()
                processed_lines = process_lines(lines)

                file_text = "".join(processed_lines)
                file_text = file_text.rstrip() + '\n'

                output_file.write(file_text)

if __name__ == "__main__":
    main()

