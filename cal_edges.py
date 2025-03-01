import json
from pathlib import Path

import japanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from math_graph.graph.graph import make_math_guideline_graph


def cal_edge(data_path):
    data_name = data_path.stem

    with open(data_path, "r") as f:
        dataset = json.load(f)

    graph = make_math_guideline_graph(dataset)
    t_graph = nx.transitive_reduction(graph)

    num_edges = t_graph.number_of_edges()
    num_nodes = t_graph.number_of_nodes()
    mean_edges_per_node = num_edges / num_nodes if num_nodes > 0 else 0
    # print(f"{data_name}: {num_edges} edges")
    print(f"{data_name}: {mean_edges_per_node * 2:.2f} mean edges per node")


data_dir = Path("dataset/simplified_formatted")
for data_path in data_dir.glob("*.json"):
    cal_edge(data_path)
