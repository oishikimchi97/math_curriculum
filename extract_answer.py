import re
from llm.openai import gpt4o
from prompt.extract_answer import chat_message_chain, ExtractAnswerList
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain_community.callbacks import wandb_tracing_enabled
from pathlib import Path
import json
from tqdm import tqdm
import json
import wandb
import os

os.environ['LANGCHAIN_WANDB_TRACING'] = "true"
run = wandb.init(project="extract_answer")
run.name = "extract_answer_test1"

# Define the path to the text file, image directory, and output JSON file
IMAGE_DIR_PATH = "jhs-math-problem/jhs-math2/png_converted"
OUTPUT_JSON_PATH = Path(IMAGE_DIR_PATH) / "converted_txt_with_answer.json"

# Get all image file paths from the specified directory using pathlib
# image_paths = list(Path(IMAGE_DIR_PATH).glob("*.png"))
# Define the path to the JSON file
problem_json_path = "jhs-math-problem/jhs-math2/png_converted/converted_txt_result.json"

# Read the JSON file and convert it into a list
with open(problem_json_path, "r") as json_file:
    data = json.load(json_file)

problem_image_paths = [item['image_path'] for item in data]
problems = [item['content'] for item in data]

def convert_problem2answer_path(problem_path):
    problem_path = problem_path.replace("problem", "answer")
    problem_path = re.sub(r'(_page)', r'ans\1', problem_path, 1)
    return problem_path

answer_iamge_paths = [convert_problem2answer_path(problem_path) for problem_path in problem_image_paths]

# List to store the results
results = []


# Make a LLM chain
gpt4o = gpt4o.bind_tools([ExtractAnswerList])
parser = JsonOutputKeyToolsParser(key_name="ExtractAnswerList")
llm_chain = chat_message_chain | gpt4o | parser


with wandb_tracing_enabled():
    # Process each image file with tqdm for progress tracking
    for i in tqdm(range(len(answer_iamge_paths)), desc="Extracting answers"):
        image_path = Path(answer_iamge_paths[i])

        image_abs_path = str(image_path.absolute())
        problem = problems[i]
        image_kwargs = {'path': image_abs_path, 'detail': 'auto'}

        try:
            output = llm_chain.invoke({'problem': problem, **image_kwargs})
        except Exception as e:
            print(f"Error: {e}")

        if i == 0:
            break

wandb.finish()