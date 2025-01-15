import string
from typing import Dict, List, Literal

import networkx as nx


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
) -> nx.DiGraph:

    graph = nx.DiGraph()  # Directed graph

    for entry in dataset:
        drill_task_name1 = entry["data"][0]["drill_task_name"]
        drill_task_name2 = entry["data"][1]["drill_task_name"]
        drill_task_topic1 = entry["data"][0]["topic"]
        drill_task_topic2 = entry["data"][1]["topic"]

        if drill_task_topic1[0] in string.ascii_uppercase:
            drill_task_topic1 = drill_task_topic1[1:]
        if drill_task_topic2[0] in string.ascii_uppercase:
            drill_task_topic2 = drill_task_topic2[1:]

        result = entry["result"].lower()

        if drill_task_name1 not in graph:
            graph.add_node(drill_task_name1, topic=drill_task_topic1)
        if drill_task_name2 not in graph:
            graph.add_node(drill_task_name2, topic=drill_task_topic2)

        # Add a directed edge from drill_task_name1 to drill_task_name2 if result is "related"
        if result == "related":
            graph.add_edge(drill_task_name1, drill_task_name2)

    return graph


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
