from openai import OpenAI
import os
from pathlib import Path
import base64
import json
from tqdm import tqdm

# Set the API key and model name
MODEL = "gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))

# Define the path to the text file, image directory, and output JSON file
PROMPT_PATH = "convert2txt_prompt.txt"
IMAGE_DIR_PATH = "jhs-math-problem/jhs-math2/png_converted"
OUTPUT_JSON_PATH = Path(IMAGE_DIR_PATH) / "converted_txt_result.json"

# Read the text content from the text file
with open(PROMPT_PATH, "r") as file:
    text_content = file.read()

# Get all image file paths from the specified directory using pathlib
image_paths = list(Path(IMAGE_DIR_PATH).glob("*.png"))

# Function to encode an image file as a base64 string
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# List to store the results
results = []

# Process each image file with tqdm for progress tracking
for i, image_path in enumerate(tqdm(image_paths, desc="Processing images")):
    base64_image = encode_image(image_path)
    image_name = image_path.name
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "次のガイドラインに従って画像ファイルから問題文を抽出し、適切にフォーマットしてください。"},
                {"role": "user", "content": [
                    {"type": "text", "text": text_content},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/{image_path.suffix[1:]};base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,
        )
    except Exception as e:
        print(f"Error processing {image_name}: {e}")
        results.append({
            "image_path": str(image_path),
            "content": "Error processing image"
        })
        continue

    content = response.choices[0].message.content
    results.append({
        "image_path": str(image_path),
        "content": content
    })

# Save the results to a JSON file
with open(OUTPUT_JSON_PATH, "w") as json_file:
    json.dump(results, json_file, indent=4)

print(f"Results saved to {OUTPUT_JSON_PATH}")