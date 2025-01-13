import copy
import os

from langchain.prompts import PromptTemplate
from langchain_core.runnables import chain

from math_graph.chain.get_edge.utils import (
    add_suffix_to_keys,
    list_to_html_ordered_text,
    make_hyperlinked_tasks,
)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to template.txt
PROMPT_PATH = os.path.join(current_dir, "./html_template_jp.txt")

with open(PROMPT_PATH, "r") as file:
    template = file.read()

prompt_input_vars = [
    "school_name1",
    "grade_or_subject_name1",
    "topic1",
    "task_objective1",
    "thinking_judgement_expression1",
    "knowledge_and_skills1",
    "school_name2",
    "grade_or_subject_name2",
    "topic2",
    "task_objective2",
    "thinking_judgement_expression2",
    "knowledge_and_skills2",
]

prompt = PromptTemplate(
    input_variables=prompt_input_vars,
    template=template,
)


@chain
def preprocess(data_pair) -> dict:
    _data_pair = copy.deepcopy(data_pair)
    for data in _data_pair:
        data["thinking_judgement_expression"] = list_to_html_ordered_text(
            data["thinking_judgement_expression"]
        )
        data["knowledge_and_skills"] = list_to_html_ordered_text(
            data["knowledge_and_skills"]
        )
        data["linked_drill_tasks"] = make_hyperlinked_tasks(data["drill_tasks"])
        data["linked_drill_tasks"] = list_to_html_ordered_text(
            data["linked_drill_tasks"]
        )

    data1, data2 = _data_pair
    pre_data1 = add_suffix_to_keys(data1, "1")
    pre_data2 = add_suffix_to_keys(data2, "2")

    prompt_input = {**pre_data1, **pre_data2}
    return prompt_input


get_edge_html_prompt = preprocess | prompt
