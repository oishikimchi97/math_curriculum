import json
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


human_data_path = Path("dataset/base/llm_gpt_simple_label_updated.json")
output_dir = Path("./dataset/formatted")

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / human_data_path.name

gpt_dataset = load_json(human_data_path)

for i, entry in enumerate(gpt_dataset):
    result = entry["annotation"]["answer"]
    del entry["annotation"]
    entry["result"] = result
    gpt_dataset[i] = entry


with open(output_path, "w") as f:
    json.dump(gpt_dataset, f, indent=4, ensure_ascii=False)

print(f"Formatted data saved at {output_path}")
