import re, random
import ast
from openai import OpenAI
import time
import math
from datetime import datetime


def ce_generate(task_plan):
    # transfer the task plan(dict str) to a dict in python
    dict_task_plan = ast.literal_eval(task_plan)

    # extract the task list, use re match
    task_list_dict = extract_task_list(task_plan)

    # assign the number of c.e.
    ce_number = 2
    ce_result = []
    for i in range(ce_number):
        # avoid affecting the original plan.
        new_task_plan = dict_task_plan.copy()
        task_list_dict_copy = task_list_dict.copy()
        # disturbing, get counter example task list
        ce = disturbing(task_list_dict_copy)
        # replace the origin task list to disturbed task list
        new_task_plan["Task list"] = ce

        ce_result.append(str(new_task_plan))

    return ce_result


def extract_task_list(task_plan):
    """
    accept a task_plan and extract the task_list to a dict, return this dict.
    """

    # extract *task list* from Task Plan
    task_list_pattern = r'"Task list":\s*\{(.*?)\},'
    match = re.search(task_list_pattern, task_plan, re.DOTALL)

    if match:
        # 提取任务列表
        task_list_content = match.group(1).strip()
        # 构造成 JSON 格式（可选）
        task_list_content = "{" + task_list_content + "}"
    else:
        return "Task list not found."
    # print(task_list_content)
    # transfer *task list*(string format) to a dict
    task_dict = ast.literal_eval(task_list_content)

    # 打印结果
    # print(task_dict)
    print("Extracted Task Dictionary:")

    _log_task = ""
    for key, value in task_dict.items():
        print(f"Key: {key}, Value: {value}")
        _log_task = _log_task + f"Key: {key}, Value: {value}" + "\n"

    return task_dict


def disturbing(task_list_dict):
    """
    accept a task_dict, apply disturbing strategy to it.
    """
    # ________  swap the order of two tasks _________
    # return perform_swaps(task_dict)
    # ________  swap the order of two tasks _________

    # _________ remove a task(randomly) _________
    return remove_task(task_list_dict)
    # _________ remove a task(randomly) _________

    # _________ edit a task _________
    # return edit_task(task_list_dict)
    # _________ edit a task _________

    # ________ no disturbing, just return the original one __________
    # return task_list_dict
    # ________ no disturbing, just return the original one __________


def perform_swaps(d, num_swaps=1):
    current_dict = d.copy()  # 创建原始字典的一个副本，以避免修改原始字典
    for _ in range(num_swaps):
        keys = list(d.keys())
        if len(keys) < 2:
            print("The dictionary must contain at least two items to perform a swap.")
        else:
            key1, key2 = random.sample(keys, 2)
            print(key1 + " " + key2)
            current_dict[key1], current_dict[key2] = (
                current_dict[key2],
                current_dict[key1],
            )

    # 将交换后的列表转换回字典

    return current_dict


def remove_task(d):
    """
    randomly remove a task
    """
    if not d:
        print("The dictionary is empty, nothing to remove.")
        return None
    sample_size = math.ceil(len(d) * 0.3)
    sample_size = min(sample_size, len(d))
    keys_to_remove = random.sample(list(d.keys()), sample_size)
    print("Keys to remove:", str(keys_to_remove))
    removed_values = [d.pop(key) for key in keys_to_remove]
    print("Removed values:", str(removed_values))

    return d


def chat_to_LLM(messages):

    client = OpenAI(
        api_key="sk-nF4KFp0FggnT6bfpH2JwYhRsFWnPpfohEAtERbHlMXCIdlki",  # 只需要填写key就可以了
        base_url="https://api.chatanywhere.tech",
    )
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        # stream=True, # 这个开了要用chunk的调用方法
    )
    # print(response.choices[0].message.content, end="", flush=True)
    return response.choices[0].message.content


def edit_task(d):
    """
    edit one task
    """
    if not d:
        print("The dictionary is empty, nothing to remove.")
        return None
    # seed
    seed_value = int(time.time())
    with open("D:\Project\CE\CE\seed.txt", "a") as file:
        file.write(str(datetime.now()) + " " + str(seed_value))
    random.seed(seed_value)
    #
    key_to_edit = random.choice(list(d.keys()))
    task_description = d[key_to_edit]

    messages = []
    _log_task = ""
    for key, value in d.items():
        print(f"Key: {key}, Value: {value}")
        _log_task = _log_task + f"Key: {key}, Value: {value}" + "\n"
    template = """Here is a task plan list for implementing a project. I have selected one task, and now I want to create a negative example based on this task. Please make the task I selected more vague.
    You only need to return an edited task.
    # Example:
    input:Create StoryManager class methods for creating and saving stories, handle form submission from story_creation.html, and save story data to stories.txt.
    output:Write some functions in the StoryManager class to do stuff with stories, handle some kind of form input, and save to a file.
    the whole task plan is:{task_plan},
    the task I selected is:{task},
    follow example and return a edited task.
    """
    messages.append(
        {
            "role": "user",
            "content": template.format_map(
                {
                    "task_plan": _log_task,
                    "task": str(key_to_edit) + ": " + task_description,
                }
            ),
        }
    )
    edited_task = chat_to_LLM(messages)
    print(
        "\nedit: "
        + str(key_to_edit)
        + " \nbefore edit: "
        + task_description
        + "\nafter edit: "
        + edited_task
    )
    d[key_to_edit] = edited_task
    return d
