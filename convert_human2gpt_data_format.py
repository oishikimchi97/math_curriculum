import json
from math import e
from pathlib import Path


def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


human_data_path = Path(
    "./dataset/extracted_human/integrated_data-Kojima_Kim_Simomura_simplified-Simomura.json"
)
output_dir = Path("./dataset/formatted")

output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / human_data_path.name

human_dataset = load_json(human_data_path)

for i, entry in enumerate(human_dataset):
    data = entry["data"]
    data1_keys = [key for key in data.keys() if "1" in key]
    data2_keys = [key for key in data.keys() if "2" in key]
    the_other_keys = [key for key in data.keys() if not "1" in key and not "2" in key]

    basic_keys = [key.replace("1", "") for key in data1_keys]

    data1 = {}
    data2 = {}
    for key in basic_keys:
        try:
            data1[key] = data[key + "1"]
            data2[key] = data[key + "2"]
        except KeyError:
            print(f"Key {key} not found in data")

    formatted_data = [data1, data2]
    human_dataset[i]["data"] = formatted_data

with open(output_path, "w") as f:
    json.dump(human_dataset, f, indent=4, ensure_ascii=False)

print(f"Formatted data saved at {output_path}")
