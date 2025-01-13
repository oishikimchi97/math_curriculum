import os
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# Function to get all links starting with the given prefix
def get_links(start_url, prefix):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    filtered_links = [link['href'] for link in links if link['href'].startswith(prefix)]
    return filtered_links

# Function to download PDF from a given URL
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Function to get the title of the HTML page
def get_page_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.title.string.strip() if soup.title else 'No Title'


if __name__ == '__main__':

    # List of starting URLs
    start_urls = [
        'https://happylilac.net/jhs-math1.html',
        'https://happylilac.net/jhs-math2.html',
        'https://happylilac.net/jhs-math3.html'
    ]

    # List to hold metadata for JSON
    metadata_list = []
    # Process each start URL

    output_dir = 'jhs-math-problem'
    
    for start_url in start_urls:
        # Determine the prefix for the current start URL
        prefix = start_url.replace('.html', '')

        # Get all links starting with the current prefix
        urls = get_links(start_url, prefix)
        print(f"Found {len(urls)} PDFs for {prefix}.")

        # Create a directory for the current prefix
        directory = prefix.split('/')[-1]
        directory = output_dir + '/' + directory
        if not os.path.exists(directory):
            os.makedirs(directory)


        # Loop through the URLs and download the corresponding PDFs
        for url in tqdm(urls, desc=f"Downloading PDFs for {prefix}"):
            # Get the title of the HTML page
            page_title = get_page_title(url)
            pdf_url = url.replace('.html', '.pdf')
            filename = os.path.join(directory, pdf_url.split('/')[-1])
            download_pdf(pdf_url, filename)

            # Add metadata to the list
            metadata_list.append({
                'pdf_file_path': filename,
                'theme': page_title
            })

    # Save metadata to a JSON file
    with open('pdf_metadata.json', 'w', encoding='utf-8') as json_file:
        json.dump(metadata_list, json_file, ensure_ascii=False, indent=4)

    print("All PDFs downloaded and metadata saved to pdf_metadata.json.")