import os
import re
import json
import urllib.request
import csv
import datetime
import time
import logging

# Constants
MAX_PAGES = 100 # The first 100 pages of data will be downloaded.
SLEEP_INTERVAL = 5

# Download data from the Chronicling America website
def download_data(url, page, timeout_sec=200):
    try:
        with urllib.request.urlopen(f'{url}&rows=10&format=json&page={page}', timeout=timeout_sec) as response:
            return json.loads(response.read().decode('utf8'))
    except urllib.error.URLError as e:
        print(f"Error downloading data: {e}")
        return None
    
# Process json data into txt file
def process_item(p, writer, directory):
    if 'ocr_eng' in p:
        edition = re.search('(?<=\/ed-)(.*)(?=\/seq-)', p['id']).group(1)
        sequence = re.search('(?<=\/seq-)(.*)(?=\/)', p['id']).group(1)
            
        # Create a base file name using the date, title, edition, and sequence
        base_file_name = f"{p['date']}_{p['title']}_{edition}_{sequence}"

        # Sanitize the file name to remove non-alphanumeric characters, except underscores
        base_file_name_without_dot = base_file_name.replace('.', '_')
        sanitized_file_name = re.sub('[^a-zA-Z0-9_]', '', base_file_name_without_dot)

        # Ensure the sanitized file name is not empty
        if not sanitized_file_name.strip():
            sanitized_file_name = "default_name"

        # Append the .txt extension
        file_name = sanitized_file_name + ".txt"
        file_path = os.path.join(directory, file_name)

        # Generate .txt file
        with open(file_path, "w", encoding='utf8') as file:
            file.write(p['ocr_eng'])

        city, county, state = (p.get(key, [''])[0] for key in ['city', 'county', 'state'])
        writer.writerow([file_path, p['title'], p['date'], p['edition'], p['page'], p['sequence'], city, county, state, f"https://chroniclingamerica.loc.gov{p['id']}"])

def write_csv(metadata_csv_path, chronam_url, end_page, ocr_texts_dir):
    """
    Writes data to a CSV file.

    :param metadata_csv_path: Path to the CSV file.
    :param chronam_url: URL for downloading data.
    :param end_page: Maximum number of pages to process.
    :param ocr_texts_dir: Directory to store OCR text files.
    :return: Total count of texts processed.
    """
    # Initialize a counter for processed texts
    text_counter = 0

    # Open the CSV file in append mode
    with open(metadata_csv_path, 'a', encoding='utf8') as metadata_file:
        # Create a CSV writer object
        csv_writer = csv.writer(metadata_file, delimiter=',')

        # Write the header row to the CSV file
        headers = [
            'file', 'title', 'date', 'edition', 'page', 
            'sequence', 'city', 'county', 'state', 'page_url'
        ]
        csv_writer.writerow(headers)

        # Loop over each page to process
        for page in range(1, end_page):
            # Download the data for the current page
            data = download_data(chronam_url, page)

            # Check for valid data and break loop if data is not valid
            if not data or 'items' not in data or data['endIndex'] >= data['totalItems']:
                break

            # Process each item in the data
            for item in data['items']:
                # Process and write item to CSV
                process_item(item, csv_writer, ocr_texts_dir)

                # Increment text counter if OCR text is present
                text_counter += 1 if 'ocr_eng' in item else 0

            # Log the progress of downloading
            logging.info(f"Progress: {page}/{MAX_PAGES - 1}")

            # Sleep between requests to avoid overloading the server
            time.sleep(SLEEP_INTERVAL)

    # Return the count of processed texts
    return text_counter
def write_searchterms(searchterms_path, data, chronam_url, text_counter):
    """
    Writes a searchterms file.

    :param searchterms_path: Path to the searchterms file.
    :param data: Data object containing totalItems.
    :param chronam_url: URL for the search.
    :param text_counter: Total count of texts processed.
    """
    # Open the searchterms file in write mode
    with open(searchterms_path, 'w') as searchterms:
        # Write the download timestamp and number of results
        download_info = (
            f"Downloaded: {datetime.datetime.now()}\n\n"
            f"Num of results: {data['totalItems']} newspaper pages—"
            f"{text_counter} of those pages had OCR files.\n\n"
            f"Search URL: {chronam_url}\n\n"
            f"Search results in JSON: {chronam_url}&format=json\n\n"
        )
        searchterms.write(download_info)

        # Split the URL to extract search terms
        search_components = chronam_url.split("&")
        search_terms_section = "Seach Terms:\n" + search_components[0].split("?")[1] + '\n'

        # Write the search terms section
        searchterms.write(search_terms_section)

        # Write each term in a new line
        for term in search_components[1:]:
            searchterms.write(term + '\n')

def main():
    # Ask user for input url
    chronam_url = input("Paste in the URL for the Chronicling America search results you want to download: ")
    # Extract year from URL
    match = re.search(r'date1=(\d{4})', chronam_url)

    if not match:
        print("Year not found in URL.")
        return
    year = match.group(1)

    # Create directories
    year_directory = os.path.join(year)
    ocr_texts_dir = os.path.join(year_directory, 'ocr_texts')
    if not os.path.exists(ocr_texts_dir):
        os.makedirs(ocr_texts_dir)

    # CSV and metadata file paths
    metadata_csv_path = os.path.join(year_directory, 'metadata.csv')
    searchterms_path = os.path.join(year_directory, 'searchterms.txt')

    text_counter = write_csv(metadata_csv_path, chronam_url, MAX_PAGES, ocr_texts_dir)

    data = download_data(chronam_url, 1)  # Assuming data['totalItems'] is required for the readme
    if data:
        write_searchterms(searchterms_path, data, chronam_url, text_counter)

    print("Download complete")

if __name__ == "__main__":
    main()
