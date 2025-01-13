import json
import os
from pathlib import Path

from langchain.prompts import FewShotPromptTemplate, PromptTemplate

from math_graph.chain.data import EducationGuideline
from math_graph.llm.openai import model
from math_graph.utils import convert_dict2str

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to template.txt
PROMPT_PATH = os.path.join(current_dir, "template.txt")
FEWSHOT_PROMPT_PATH = os.path.join(current_dir, "few-shot_template.txt")
INPUT_EXAMPLE_PATH = os.path.join(current_dir, "fewshot/input.txt")
OUTPUT_EXAMPLE_PATH = os.path.join(current_dir, "fewshot/output.json")

input_example = Path(INPUT_EXAMPLE_PATH).read_text()
with open(OUTPUT_EXAMPLE_PATH, "r", encoding="shift-jis") as file:
    output_example = json.load(file)
    output_example = convert_dict2str(output_example)

template = Path(PROMPT_PATH).read_text()
fewshot_template = Path(FEWSHOT_PROMPT_PATH).read_text()


examples = [{"input": input_example, "output": output_example}]

example_prompt = PromptTemplate(
    template=fewshot_template,
    input_variables=["input", "output"],
)

fewshot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix=template,
    input_variables=["text"],
)

convert_txt2json_chain = fewshot_prompt | model.bind_tools([EducationGuideline])
