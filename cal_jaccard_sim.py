from itertools import combinations
from pathlib import Path

import pandas as pd

from math_graph.graph.graph import make_math_guideline_graph
from math_graph.graph.sim import jaccard_similarity
from math_graph.utils import load_json

data_dir = Path("dataset/simplified_formatted_paper_name")
data_paths = list(data_dir.glob("*.json"))

pair_data_fps = combinations(data_paths, 2)

output_table = pd.DataFrame(
    columns=["data_name1", "data_name2", "similarity", "union", "intersection"]
)

for data1_fp, data2_fp in pair_data_fps:
    data1 = load_json(data1_fp)
    data2 = load_json(data2_fp)

    graph1 = make_math_guideline_graph(data1)
    graph2 = make_math_guideline_graph(data2)

    result_dict = jaccard_similarity(graph1, graph2)
    data1_name = data1_fp.stem
    data2_name = data2_fp.stem

    output_table = pd.concat(
        [
            output_table,
            pd.DataFrame(
                {
                    "data_name1": [data1_name],
                    "data_name2": [data2_name],
                    "similarity": [result_dict["similarity"]],
                    "union": [result_dict["union"]],
                    "intersection": [result_dict["intersection"]],
                }
            ),
        ]
    )

print(output_table.to_markdown(index=False))
