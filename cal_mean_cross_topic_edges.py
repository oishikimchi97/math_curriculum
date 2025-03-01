import json

import networkx as nx

data_path = "dataset/simplified_formatted/Human Shimomura.json"

with open(data_path, "r") as f:
    dataset = json.load(f)

# Create a directed graph using the filtered data
G = nx.DiGraph()  # Directed graph

topic_list = set()

for entry in dataset:
    drill_task_name1 = entry["data"][0]["drill_task_name"]
    drill_task_name2 = entry["data"][1]["drill_task_name"]
    drill_task_topic1 = entry["data"][0]["topic"]
    drill_task_topic2 = entry["data"][1]["topic"]

    topic_list.add(drill_task_topic1)
    topic_list.add(drill_task_topic2)

    if "result" in entry:
        result = entry["result"].lower()
    elif "annotation" in entry:
        result = entry["annotation"]["answer"].lower()
    if drill_task_name1 not in G:
        G.add_node(drill_task_name1, topic=drill_task_topic1)
    if drill_task_name2 not in G:
        G.add_node(drill_task_name2, topic=drill_task_topic2)

    # Add a directed edge from drill_task_name1 to drill_task_name2 if result is "related"
    if result == "related":
        G.add_edge(drill_task_name1, drill_task_name2)

Gt = nx.transitive_reduction(G)  # Remove redundant edges

print("Number of nodes:", Gt.number_of_nodes())
print("Number of edges:", Gt.number_of_edges())
print("Number of topics:", len(topic_list))

cross_topic_edge_count = 0

for edge in Gt.edges():
    node_name1, node_name2 = edge
    node1 = G.nodes[node_name1]
    node2 = G.nodes[node_name2]

    if node1["topic"] != node2["topic"]:
        cross_topic_edge_count += 1

print(f"Number of cross-topic edges: {cross_topic_edge_count}")
# Calculate the mean number of edges per node
print("The mean cross topic edge ratio is", cross_topic_edge_count / len(topic_list))
