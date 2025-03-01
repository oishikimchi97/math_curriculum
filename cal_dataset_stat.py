import json
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def count_results(data):
    result_counts = {}
    for entry in data:
        result = entry.get("result")
        if result:
            if result in result_counts:
                result_counts[result] += 1
            else:
                result_counts[result] = 1
    return result_counts


def print_statistics(result_counts):
    total = sum(result_counts.values())
    print("Result Statistics:")
    for result, count in result_counts.items():
        print(f"{result}: {count} ({(count / total) * 100:.2f}%)")


if __name__ == "__main__":
    file_path = Path("dataset/simplified_formatted_paper_name/gpt4o.json")
    data = load_json(file_path)
    result_counts = count_results(data)
    print_statistics(result_counts)
