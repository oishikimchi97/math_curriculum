from itertools import combinations
from pathlib import Path

import networkx as nx

from math_graph.graph.graph import make_math_guideline_graph
from math_graph.utils import load_json

human_data_path = Path(
    "dataset/base/integrated_data-Kojima_Kim_Simomura_simplified.json"
)

human_dataset = load_json(human_data_path)

human_names = human_dataset[0]["annotations"].keys()

dataset_table = {}

for name in human_names:
    dataset_table[name] = [
        {**entry, "result": entry["annotations"][name]} for entry in human_dataset
    ]

human_comb = combinations(human_names, 2)

for name1, name2 in human_comb:
    graph1_dataset = dataset_table[name1]
    graph2_dataset = dataset_table[name2]

    G1 = make_math_guideline_graph(graph1_dataset, truncate=True, data_type="human")
    G2 = make_math_guideline_graph(graph2_dataset, truncate=True, data_type="human")

    ged = nx.graph_edit_distance(G1, G2)
    print(f"Graph edit distance between {name1} and {name2} is {ged}")
