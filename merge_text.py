import os
import argparse

def merge_txt_files(subdirectory):
    # Define the parent directory (one level up from the subdirectory)
    parent_directory = os.path.dirname(subdirectory)

    # Extract the name of the parent directory (assuming it's the year)
    year = os.path.basename(parent_directory)

    # Define the output file path in the parent directory
    output_file_name = f"{year}_text.txt"
    output_file_path = os.path.join(parent_directory, output_file_name)

    # Open the output file in write mode
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate over all files in the subdirectory
        for file in os.listdir(subdirectory):
            # Check if the file is a .txt file
            if file.endswith('.txt'):
                file_path = os.path.join(subdirectory, file)
                
                # Open and read the content of the .txt file
                with open(file_path, 'r', encoding='utf-8') as input_file:
                    output_file.write(input_file.read() + "\n\n")  # Add two newlines for separation

    print(f"All .txt files have been merged into {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Merge all .txt files in a specified subdirectory.')
    parser.add_argument('subdirectory', help='Path to the subdirectory containing .txt files')
    args = parser.parse_args()

    merge_txt_files(args.subdirectory)

if __name__ == '__main__':
    main()
