import os
from bs4 import BeautifulSoup
import requests

# Function to check if a URL exists
def url_exists(url):
    response = requests.head(url)
    return response.status_code == 200

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

# Directory to save the PDFs
directory = 'jhs-math3'
if not os.path.exists(directory):
    os.makedirs(directory)

# Base URL format
base_url = 'https://happylilac.net/pdf/jhs-math3_{:02d}-{:02d}ans.pdf'

# Loop through the numbers to construct the URLs and download the PDFs
for i in range(0, 10):
    for j in range(0, 10):
        pdf_url = base_url.format(i, j)
        if url_exists(pdf_url):
            filename = os.path.join(directory, pdf_url.split('/')[-1])
            # download_pdf(pdf_url, filename)
            # print(f"Downloaded: {filename}")
        else:
            print(f"URL does not exist: {pdf_url}")

print("All PDFs downloaded.")