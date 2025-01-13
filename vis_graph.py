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
    graph_reverse = t_graph.reverse()

    # Ensure the graph is a directed acyclic graph (DAG)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError(
            "The graph is not a directed acyclic graph (DAG) and cannot be visualized as a tree."
        )

    # Use NetworkX's hierarchy layout for tree visualization
    pos = nx.nx_agraph.graphviz_layout(
        graph_reverse, prog="dot"
    )  # 'dot' creates a hierarchical layout

    topics = set(graph.nodes[node]["topic"] for node in graph.nodes)

    # Create a color map for the topics
    color_map = {}
    colors = plt.cm.get_cmap(
        "Set3", len(topics)
    )  # Use a colormap with enough unique colors

    for i, topic in enumerate(topics):
        color_map[topic] = colors(i)

    # Assign colors to nodes based on their topic
    node_colors = [
        color_map[graph.nodes[node].get("topic", None)] for node in graph.nodes
    ]

    plt.figure(figsize=(16, 16))
    # Fix the random seed for colormaps
    np.random.seed(42)
    plt.title(data_name, fontsize=20)
    nx.draw(
        t_graph,
        pos,
        with_labels=True,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=15,
        node_size=3000,
        node_color=node_colors,
        edgecolors="black",
        linewidths=2,
        font_family="IPAexGothic",
        font_weight="bold",  # Make the words bold
    )
    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color_map[topic],
            markersize=10,
            label=topic,
        )
        for topic in topics
    ]
    plt.legend(handles=legend_handles, title="Topics", loc="best", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    # Create a legend for the topics
    plt.savefig(output_path)
    print(f"Graph visualization saved to {output_path}")


data_dir = Path("dataset/formatted")
for data_path in data_dir.glob("*.json"):
    visualize_math_graph(data_path)
