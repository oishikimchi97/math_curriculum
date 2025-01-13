import base64
import copy
import os
from operator import itemgetter
from typing import List, Literal

from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough, chain

from math_graph.chain.get_edge.utils import add_suffix_to_keys, list_to_numbered_text
from math_graph.llm.openai import model

current_dir = os.path.dirname(os.path.abspath(__file__))


# Utility function for image encoding
def encode_image(image_path: str) -> dict:
    """
    Encode an image to base64 for OpenAI vision model

    Args:
        image_path (str): Path to the image file

    Returns:
        dict: Encoded image dictionary for vision model
    """
    try:
        with open(image_path, "rb") as image_file:
            return {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
                },
            }
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None


# Construct the path to template.txt
PROMPT_PATH = os.path.join(current_dir, "./template_jp2.j2")

with open(PROMPT_PATH, "r") as file:
    template = file.read()


class ResponseSchema(BaseModel):
    reasoning: str = Field(
        description="学習タスク1と学習タスク2の関係性を説明してください"
    )
    answer: Literal["High required", "Low required", "Not required"] = Field(
        description="""次のいずれかを答えてください。
High required: 学習タスク1が学習タスク2の直接な先行科目である
Low required: 学習タスク1が学習タスク2の間接的な先行科目である
Not required: 学習タスク1と学習タスク2がお互いに関係ない
Unknown: この説明だけでは判断することが難しい"""
    )


prompt = PromptTemplate.from_template(template=template, template_format="jinja2")


@chain
def preprocess(data_pair: List[dict]) -> dict:
    # Deep copy to avoid modifying original data
    data_pair = copy.deepcopy(data_pair)

    image_paths = []

    for data in data_pair:
        data["thinking_judgement_expression"] = list_to_numbered_text(
            data["thinking_judgement_expression"]
        )
        data["knowledge_and_skills"] = list_to_numbered_text(
            data["knowledge_and_skills"]
        )
        for drill_task in data["drill_tasks"]:
            if "png_paths" in drill_task:
                image_paths.extend(drill_task["png_paths"])

    data1, data2 = data_pair
    pre_data1 = add_suffix_to_keys(data1, "1")
    pre_data2 = add_suffix_to_keys(data2, "2")

    # Prepare prompt input
    prompt_input = {**pre_data1, **pre_data2}

    images = [encode_image(path) for path in image_paths if encode_image(path)]

    return {"prompt_input": prompt_input, "images": images}


@chain
def convert_human_message(data) -> dict:
    message_content = [{"type": "text", "text": data["text"]}]
    message_content.extend(data["images"])

    return [HumanMessage(content=message_content)]


parser = JsonOutputToolsParser(key_name="ResponseSchema")

get_edge_prompt = preprocess | {
    "text": lambda prompt_input: prompt.format(**prompt_input["prompt_input"])
}
get_edge_chain = (
    preprocess
    | {
        "text": lambda prompt_input: prompt.format(**prompt_input["prompt_input"]),
        "images": itemgetter("images"),
    }
    | convert_human_message
    | model.bind_tools([ResponseSchema])
    | parser
)
