import string
from typing import Dict, List, Literal

import networkx as nx

node_readable_table = {
    "平方の定理": "平方の定理",
    "円の性質": "円の性質",
    "対称と合同": "対称と合同",
    "平面図形と合同": "平面図形と\n合同",
    "平面図形": "平面図形",
    "空間図形": "空間図形",
    "2次関数": "2次関数",
    "平方根": "平方根",
    "式の展開と因数分解": "式の展開と\n因数分解",
    "1次関数": "1次関数",
    "比例と反比例": "比例と\n反比例",
    "文字と式": "文字と式",
    "方程式": "方程式",
    "式の計算": "式の計算",
    "立方野程": "立方野程",
    "不確定な事象の確率": "不確定な\n事象の確率",
    "確率（資料の活用）": "確率\n（資料の活用)",
    "資料の整理と活用": "資料の\n整理と活用",
    "データの活用": "データの活用",
    "基本調査": "基本調査",
    "標本調査": "標本調査",
    "正負の数": "正負の数",
}


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
    convert_readable: bool = False,
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

        if convert_readable:
            drill_task_name1 = node_readable_table.get(
                drill_task_name1, drill_task_name1
            )
            drill_task_name2 = node_readable_table.get(
                drill_task_name2, drill_task_name2
            )

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
