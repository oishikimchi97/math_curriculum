import json
from pathlib import Path

school_name_en2jp = {
    "elementary_school": "小学校",
    "middle_school": "中学校",
    "high_school": "高校",
}

grade_name_en2jp = {
    "1st_grade": "1年生",
    "2nd_grade": "2年生",
    "3rd_grade": "3年生",
    "4th_grade": "4年生",
    "5th_grade": "5年生",
    "6th_grade": "6年生",
}

school_name_jp2en = {
    "小学校": "elementary_school",
    "中学校": "middle_school",
    "高校": "high_school",
}

grade_name_jp2en = {
    "1年生": "1st_grade",
    "2年生": "2nd_grade",
    "3年生": "3rd_grade",
    "4年生": "4th_grade",
    "5年生": "5th_grade",
    "6年生": "6th_grade",
}


def convert_dict2str(data: dict) -> str:
    dict_str = json.dumps(data, ensure_ascii=False, indent=4)
    escaped_dict_str = dict_str.replace("{", "{{").replace("}", "}}")
    return escaped_dict_str


def get_output_path(
    input_path: Path, output_dir: Path, data_dir: Path, file_extension="md"
):

    return output_dir / input_path.relative_to(data_dir).with_suffix(
        "." + file_extension
    )


def convert_school_name_en2jp(school_name: str) -> str:
    return school_name_en2jp[school_name]


def convert_grade_name_en2jp(grade_or_subject_name: str) -> str:
    return grade_name_en2jp[grade_or_subject_name]


def load_json(path):
    with open(path, "r") as file:
        return json.load(file)


def load_jsonl(path):
    with open(path, "r") as file:
        return [json.loads(line) for line in file]


def save_output(
    input_path: Path,
    output_dir: Path,
    data_dir: Path,
    output_content: str,
    file_extension="md",
    encoding=None,
):
    output_path = get_output_path(input_path, output_dir, data_dir, file_extension)
    output_path.parent.mkdir(exist_ok=True, parents=True)

    if file_extension == "json":
        with open(output_path, "w", encoding=encoding) as file:
            json.dump(output_content, file, ensure_ascii=False, indent=4)
    else:
        with open(output_path, "w", encoding=encoding) as file:
            file.write(output_content)

    print(f"Converted {input_path} to {output_path}")


def get_task_global_id(data):
    return "-".join(
        [
            data["school_name"],
            data["grade_or_subject_name"],
            str(data["school_task_id"]),
        ]
    )


def get_pair_id(data1, data2):
    return "--".join(
        [
            get_task_global_id(data1),
            get_task_global_id(data2),
        ]
    )
