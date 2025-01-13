import json
from pathlib import Path
from typing import Dict, List, Literal, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class Task(BaseModel):
    task_objective: str = Field(
        description="Educational Objective of a task. List each item separately",
    )
    thinking_judgement_expression: List[str] = Field(
        description="To acquire the following knowledge and skills.",
    )
    knowledge_and_skills: List[str] = Field(
        description="To acquire the following thinking skills, judgment skills, and expressive abilities, etc.",
    )


class ContentItem(BaseModel):
    topic: str = Field(description="The topic of the lesson")
    task: List[Task] = Field(description="Objectives and descriptions for each item")
    terms: List[str] = Field(description="List of terms")


class Activity(BaseModel):
    activity_objective: str = Field(
        description="Educational Objective of an activity.",
    )
    activity_description: List[str] = Field(
        description="descriptions of an activity",
    )


class EducationGuideline(BaseModel):
    """Education guideline for a specific grade or subject in a school."""

    objective: List[str] = Field(description="Educational objectives of this course")
    content: List[ContentItem] = Field(description="Content of this course")
    activities: List[Activity] = Field(description="Activities of this course")
    content_instruction: List[str] = Field(
        description="instructional methods and related information. List each item separately",
    )


class EducationGuidelineReader:
    def __init__(self, data_dir: str):
        """_summary_
        Data reader class for the education guideline data.

        Args:
            data_dir (str): a dataset directory path. This is a directory that
            contains all json files of a specific type of school.
        """
        self.dir_path = Path(data_dir)
        self.school_name = self.dir_path.name
        self.file_paths = list(self.dir_path.glob("*.json"))
        self.dataset = self._load_data()

    def _load_data(self) -> List[Dict]:
        data_list = []
        for file_path in self.file_paths:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
                data_list.append(json_data)

        dataset = self._get_data_from_json(data_list)
        dataset = sorted(dataset, key=lambda x: x["grade_or_subject_name"])
        return dataset

    def _get_data_from_json(self, data_list) -> List[Dict]:
        tasks = []
        for json_data in data_list:
            for content_item in json_data["content"]:
                for task in content_item["task"]:
                    tasks.append(
                        {
                            "school_name": self.school_name,
                            "grade_or_subject_name": json_data["grade_or_subject_name"],
                            "topic": content_item["topic"],
                            "task_objective": task["task_objective"],
                            "thinking_judgement_expression": task[
                                "thinking_judgement_expression"
                            ],
                            "knowledge_and_skills": task["knowledge_and_skills"],
                        }
                    )
        return tasks

    def __getitem__(self, idx):
        return self.dataset[idx]

    def __len__(self):
        return len(self.dataset)
