from email.mime import image
import json
from pathlib import Path
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Convert JSON content to Markdown files.')
parser.add_argument('--json_path', type=str, help='Path to the JSON file')

args = parser.parse_args()

# Define the path to the JSON file
json_file_path = Path(args.json_path)

# Load JSON content
with json_file_path.open('r') as file:
    data = json.load(file)

# Define the output directory
output_dir = json_file_path.parent 
output_dir.mkdir(exist_ok=True)

# Iterate over each item in the JSON array
for i, item in enumerate(data):
    image_path = item['image_path']
    content = item['content']
    
    # Extract the filename from the image_path and change its extension to .md
    markdown_filename = Path(image_path).with_suffix('.md').name
    markdown_filepath = output_dir / markdown_filename

    # Relative path from the markdown file to the image
    relative_image_path = Path(image_path).relative_to(output_dir)

    # Create the markdown file content
    markdown_content = f"![Image]({relative_image_path})\n\n{content}"
    
    # Write to the markdown file
    with markdown_filepath.open('w') as md_file:
        md_file.write(markdown_content)
    
    # print(f"Markdown file {i+1}/{len(data)} has been created: {markdown_filepath}")

print("Markdown files have been created successfully.")