from pathlib import Path

import networkx as nx

from math_graph.graph.graph import make_math_guideline_graph
from math_graph.utils import load_json

human_data_path = Path(
    "dataset/base/integrated_data-Kojima_Kim_Simomura_simplified.json"
)
target_data_path = Path(
    "dataset/base/integrated_data-Kojima_Kim_Simomura_discrete.json"
)

human_dataset = load_json(human_data_path)
target_dataset = load_json(target_data_path)

human_names = human_dataset[0]["annotations"].keys()

dataset_table = {}

for name in human_names:
    dataset_table[name] = [
        {**entry, "result": entry["annotations"][name]} for entry in human_dataset
    ]

target_G = make_math_guideline_graph(target_dataset, truncate=True, data_type="human")

for name, dataset in dataset_table.items():
    graph1_dataset = dataset_table[name]

    G1 = make_math_guideline_graph(graph1_dataset, truncate=True, data_type="human")

    ged = nx.graph_edit_distance(G1, target_G)
    print(f"Graph edit distance between {name} and target is {ged}")
