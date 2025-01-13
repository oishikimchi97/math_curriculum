import json
from pathlib import Path

import japanize_matplotlib
import matplotlib.pyplot as plt
import networkx as nx

from math_graph.graph.graph import make_math_guideline_graph

data_path = Path("dataset/formatted/gpt_v2_simplified.json")

output_dir = Path("visualization")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / (data_path.stem + ".pdf")

with open(data_path, "r") as f:
    dataset = json.load(f)

graph = make_math_guideline_graph(dataset, truncate=True)
graph_reverse = graph.reverse()

# Ensure the graph is a directed acyclic graph (DAG)
if not nx.is_directed_acyclic_graph(graph):
    raise ValueError(
        "The graph is not a directed acyclic graph (DAG) and cannot be visualized as a tree."
    )

# Use NetworkX's hierarchy layout for tree visualization
pos = nx.nx_agraph.graphviz_layout(
    graph_reverse, prog="dot"
)  # 'dot' creates a hierarchical layout

# Visualize the graph as a tree
plt.figure(figsize=(16, 12))
nx.draw(
    graph,
    pos,
    with_labels=True,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=15,
    node_size=3000,
    node_color="lightblue",
    edgecolors="black",
    linewidths=2,
    font_family="IPAexGothic",
)
plt.title("Tree-Structured Visualization of Directed Relationships", fontsize=18)
plt.axis("off")
plt.show()
plt.savefig(output_path)
print(f"Graph visualization saved to {output_path}")
