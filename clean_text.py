import re
import argparse
import os

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    parser = argparse.ArgumentParser(description='Clean text in a file.')
    parser.add_argument('file_path', help='Path to the file to be cleaned')
    args = parser.parse_args()

    file_path = args.file_path

    # Read text from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    # Clean the text
    cleaned_text = clean_text(original_text)

    # Determine the path for the cleaned file
    dir_name, file_name = os.path.split(file_path)
    cleaned_file_name = 'cleaned_' + file_name
    cleaned_file_path = os.path.join(dir_name, cleaned_file_name)

    # Save the cleaned text
    with open(cleaned_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Cleaned text saved to {cleaned_file_path}")

if __name__ == "__main__":
    main()
