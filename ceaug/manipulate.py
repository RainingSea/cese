import re, random
import ast


def ce_generate(task_plan):
    task_list_dict = extract_task_list(task_plan)
    dict_task_plan = ast.literal_eval(task_plan)
    # assign the number of c.e.
    ce_number = 3
    ce_result = []
    for i in range(ce_number):
        new_task_plan = dict_task_plan.copy()
        ce = disturbing(task_list_dict)
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
    print("Task Dictionary:")

    _log_task = ""
    for key, value in task_dict.items():
        print(f"Key: {key}, Value: {value}")
        _log_task = _log_task + f"Key: {key}, Value: {value}" + "\n"

    return task_dict


def disturbing(task_dict):
    """
    accept a task_dict, apply disturbing strategy to it.
    """
    return perform_swaps(task_dict)


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
