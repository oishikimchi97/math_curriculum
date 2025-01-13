from typing import Dict, List, Literal

import networkx as nx

# Create a directed graph using the filtered data

data = []


def get_single_path(graph, source, target):
    try:
        # Find shortest path between source and target
        path = nx.shortest_path(graph, source=source, target=target)
        return path
    except nx.NetworkXNoPath:
        return None


def get_longest_path_length(graph, edges):
    longest_path_len = None
    longest_path = None

    for edge in edges:
        source, target = edge
        path = get_single_path(graph, source, target)
        path_len = len(path) - 1
        if longest_path_len is None or path_len > longest_path_len:
            longest_path_len = path_len
            longest_path = path

    longest_path_dict = {
        "longest_path": longest_path,
        "longest_path_len": longest_path_len,
    }
    return longest_path_dict


def make_math_guideline_graph(
    dataset: List[Dict],
    truncated: bool = False,
    data_type: Literal["human", "llm"] = "human",
) -> nx.DiGraph:

    graph = nx.DiGraph()  # Directed graph

    for entry in dataset:
        if data_type == "human":
            drill_task_name1, drill_task_name2, result = get_anno_result_from_human(
                entry
            )
        elif data_type == "llm":
            drill_task_name1, drill_task_name2, result = get_anno_result_from_llm(entry)
        else:
            raise ValueError("Invalid data_type")

        if drill_task_name1 is None or drill_task_name2 is None:
            print("No drill task is founded")
            print(entry["pair_id"])
        elif result == "related":
            graph.add_edge(drill_task_name1, drill_task_name2)

    if truncated:
        truncated_graph = nx.transitive_reduction(graph)  # Remove redundant edges
        return truncated_graph
    else:
        return graph


def get_anno_result_from_human(entry):
    if "drill_task_name1" in entry["data"] and "drill_task_name2" in entry["data"]:
        drill_task_name1 = entry["data"]["drill_task_name1"]
        drill_task_name2 = entry["data"]["drill_task_name2"]
        result = entry["result"]
    else:
        drill_task_name1 = None
        drill_task_name2 = None
        result = None
    return drill_task_name1, drill_task_name2, result


def get_anno_result_from_llm(entry):
    if "drill_task_name" in entry["data"][0] and "drill_task_name" in entry["data"][1]:
        drill_task_name1 = entry["data"][0]["drill_task_name"]
        drill_task_name2 = entry["data"][1]["drill_task_name"]
        result = entry["annotation"]["answer"]
    else:
        drill_task_name1 = None
        drill_task_name2 = None
        result = None
    return drill_task_name1, drill_task_name2, result
