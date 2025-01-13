import json


def update_drill_task_name(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        for entry in item["data"]:
            if (
                entry.get("school_task_id") == 7
                and entry.get("school_name") == "middle_school"
                and entry.get("grade_or_subject_name") == "1st_grade"
            ):
                entry["drill_task_name"] = "不確定な事象の確率"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Update the JSON file
update_drill_task_name("gpt_v2.json")
