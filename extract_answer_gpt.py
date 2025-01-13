from email.mime import image
import re
from openai import OpenAI
import os
from pathlib import Path
import base64
import json
from tqdm import tqdm
import json

# Set the API key and model name
MODEL = "gpt-4o"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))
print(os.environ.get("OPENAI_API_KEY"))

# Define the path to the text file, image directory, and output JSON file
PROMPT_TEMPLATE_PATH = "./prompt/extract_answer_gpt_prompt.txt"
IMAGE_DIR_PATH = "jhs-math-problem/jhs-math2/png_converted"
OUTPUT_JSON_PATH = Path(IMAGE_DIR_PATH) / "converted_txt_with_answer.json"

# Read the text content from the text file
with open(PROMPT_TEMPLATE_PATH, "r") as file:
    prompt_template = file.read()

# Get all image file paths from the specified directory using pathlib
# image_paths = list(Path(IMAGE_DIR_PATH).glob("*.png"))
# Define the path to the JSON file
problem_json_path = "jhs-math-problem/jhs-math2/png_converted/converted_txt_result.json"

# Read the JSON file and convert it into a list
with open(problem_json_path, "r") as json_file:
    data = json.load(json_file)

problem_image_paths = [item['image_path'] for item in data]
problems = [item['content'] for item in data]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def convert_problem2answer_path(problem_path):
    problem_path = problem_path.replace("problem", "answer")
    problem_path = re.sub(r'(_page)', r'ans\1', problem_path, 1)
    return problem_path

answer_iamge_paths = [convert_problem2answer_path(problem_path) for problem_path in problem_image_paths]

# List to store the results
results = []

# Process each image file with tqdm for progress tracking
for i in tqdm(range(len(answer_iamge_paths)), desc="Extracting answers"):
    image_path = Path(answer_iamge_paths[i])
    base64_image = encode_image(image_path)

    image_name = image_path.name
    problem = problems[i]

    text_content = prompt_template.replace("{ problem }", problem)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "あなたは、画像から数学の問題や答えを読み取って、数学の問題を文章に変換するプロフェッショナルな数学教育者です。次の指示に従ってください。"},
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