import json
from pathlib import Path

import japanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from math_graph.graph.graph import make_math_guideline_graph


def visualize_math_graph(data_path):
    data_name = data_path.stem

    output_dir = Path("visualization")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / (data_path.stem + ".png")

    with open(data_path, "r") as f:
        dataset = json.load(f)

    graph = make_math_guideline_graph(dataset)
    t_graph = nx.transitive_reduction(graph)

    num_edges = t_graph.number_of_edges()
    print(f"{data_name}: {num_edges} edges")


data_dir = Path("dataset/formatted")
for data_path in data_dir.glob("*.json"):
    visualize_math_graph(data_path)
