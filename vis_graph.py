import json
from pathlib import Path

import japanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import legend

from math_graph.graph.graph import make_math_guideline_graph

COLOR_MAP = {
    "関数": (0.196, 0.659, 0.322, 0.5),
    "数と式": (0.50, 0.69, 0.82, 1.0),
    "データの活用": (0.9568627451, 0.1529411765, 0.1529411765, 0.5),
    "図形": (1.0, 0.92, 0.43, 1.0),
}


def visualize_math_graph(data_path, fontsize=30):
    data_name = data_path.stem

    output_dir = Path("visualization_paper")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / (data_path.stem + ".pdf")

    with open(data_path, "r") as f:
        dataset = json.load(f)

    graph = make_math_guideline_graph(dataset, convert_readable=True)
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

    # Assign colors to nodes based on their topic
    node_colors = [
        COLOR_MAP[graph.nodes[node].get("topic", None)] for node in graph.nodes
    ]

    plt.figure(figsize=(16, 16))
    # Fix the random seed for colormaps
    np.random.seed(42)
    # plt.title(data_name, fontsize=20)
    legend_size = fontsize - 5
    # pos = {k: (v[0], v[1] - 10) for k, v in pos.items()}  # Move nodes slightly down

    nx.draw(
        t_graph,
        pos,
        with_labels=True,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=15,
        node_size=5000,
        node_color=node_colors,
        # edgecolors="black",
        # linewidths=2,
        font_family="IPAexGothic",
        font_weight="bold",  # Make the words bold
        font_size=fontsize,
    )
    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=COLOR_MAP[topic],
            markersize=legend_size,
            label=topic,
        )
        for topic in topics
    ]
    plt.legend(
        handles=legend_handles,
        title="小単元",
        fontsize=legend_size,
        title_fontsize=legend_size,
        loc="upper center",  # Position the legend at the top center
        ncol=len(topics),  # Arrange the legend items in a single row
        bbox_to_anchor=(0.5, 1.05),  # Position the legend slightly above the plot
    )
    plt.tight_layout(
        rect=[1, 1, 1, 1.5]
    )  # Adjust the layout to make space for the legend
    # plt.gcf().set_size_inches(
    #     16, 18
    # )  # Increase the figure size to prevent legend cutoff
    # Create a legend for the topics
    plt.savefig(output_path)
    print(f"Graph visualization saved to {output_path}")


data_dir = Path("dataset/simplified_formatted_paper_name")
for data_path in data_dir.glob("*.json"):
    visualize_math_graph(data_path)
