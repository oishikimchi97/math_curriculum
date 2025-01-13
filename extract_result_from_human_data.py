import json
from pathlib import Path

input_path = Path("dataset/base/integrated_data-Kojima_Kim_Simomura_simplified.json")
file_name = input_path.name
output_dir = Path(f"dataset/extracted_human")
output_dir.mkdir(parents=True, exist_ok=True)

with open(input_path, "r") as file:
    dataset = json.load(file)


# Function to integrate annotations
def extract_annotation(dataset, extract_name):
    integrated_data = []
    for entry in dataset:
        # Combine "high" and "low" into "related"
        annotations = entry["annotations"]

        annotation = annotations[extract_name]

        # Add integrated annotations and the most frequent result to the entry
        entry["result"] = annotation
        integrated_data.append(entry)

    return integrated_data


names = dataset[0]["annotations"].keys()

for name in names:
    extracted_dataset = extract_annotation(dataset, name)

    output_path = output_dir / (input_path.stem + f"-{name}.json")
    with open(output_path, "w") as file:
        json.dump(extracted_dataset, file, indent=4, ensure_ascii=False)
    print(f"Saved to {output_path}")
