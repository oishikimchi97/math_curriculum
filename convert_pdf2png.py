import os
import fitz  # PyMuPDF
from tqdm import tqdm
import argparse

def convert_pdfs_in_folder(folder_path, zoom_x=2.0, zoom_y=2.0):
    # Define the directory to save the PNG files
    output_directory = os.path.join(folder_path, 'png_converted')

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over all PDF files in the directory
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, pdf_file)
            document = fitz.open(pdf_path)
            
            for page_num in range(len(document)):
                page = document.load_page(page_num)
                mat = fitz.Matrix(zoom_x, zoom_y)  # Set the zoom level
                pix = page.get_pixmap(matrix=mat)
                
                png_file = f"{os.path.splitext(pdf_file)[0]}_page_{page_num + 1}.png"
                png_path = os.path.join(output_directory, png_file)
                
                pix.save(png_path)

def convert_pdfs_in_multiple_folders(base_path, zoom_x=2.0, zoom_y=2.0):
    # Get all directories in the base path
    folders = [os.path.join(base_path, folder_name) for folder_name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, folder_name))]
    
    # Iterate over all directories with a progress bar
    for folder_path in tqdm(folders, desc="Converting PDFs"):
        convert_pdfs_in_folder(folder_path, zoom_x, zoom_y)

# Define the base directory containing multiple folders with PDFs
# Create an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--base_dir', type=str, default='./', help='Base directory containing multiple folders with PDFs')

# Parse the command-line arguments
args = parser.parse_args()

base_dir = args.base_dir

# Convert PDFs in all subfolders with higher resolution
convert_pdfs_in_multiple_folders(base_dir, zoom_x=2.0, zoom_y=2.0)

print("Conversion complete.")