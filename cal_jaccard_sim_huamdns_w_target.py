from pathlib import Path

from math_graph.graph.graph import make_math_guideline_graph
from math_graph.graph.sim import jaccard_similarity
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

sim_list = []

for name, dataset in dataset_table.items():
    graph1_dataset = dataset_table[name]

    G1 = make_math_guideline_graph(graph1_dataset, truncate=True, data_type="human")

    sim = jaccard_similarity(G1, target_G)
    sim_list.append(sim)
    print(f"Jaccard similarity between {name} and target is {sim}")

print(f"Average Jaccard similarity is {sum(sim_list) / len(sim_list)}")
