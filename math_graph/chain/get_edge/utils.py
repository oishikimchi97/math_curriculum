def add_suffix_to_keys(data: dict, suffix: str) -> dict:
    return {f"{key}{suffix}": value for key, value in data.items()}


def list_to_numbered_text(items: list) -> str:
    assert isinstance(items, list), "data_list must be a list"
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])


def convert_linked_text(text, link) -> str:
    return f"[{text}]({link})"


def convert_hyperlinked_text(text, link):
    return f'<a href="{link}" target="_blank">{text}</a>'


def list_to_html_ordered_text(items: list) -> str:
    html_list = "<ol>\n"
    for item in items:
        html_list += f"  <li>{item}</li>\n"
    html_list += "</ol>"
    return html_list


def make_linked_tasks(drill_tasks):
    linked_drill_tasks = []
    for task in drill_tasks:
        linked_drill_task = convert_linked_text(
            task["drill_sub_task_name"], task["pdf_link"]
        )
        linked_drill_tasks.append(linked_drill_task)
    return linked_drill_tasks


def make_hyperlinked_tasks(drill_tasks):
    linked_drill_tasks = []
    for task in drill_tasks:
        linked_drill_task = convert_hyperlinked_text(
            task["drill_sub_task_name"], task["pdf_link"]
        )
        linked_drill_tasks.append(linked_drill_task)
    return linked_drill_tasks
