import re
import os
import shutil
import chardet


def log_extract(dir):
    encoding_type = ""
    try:
        with open(os.path.join(dir, "log.log"), "rb") as file:
            raw_data = file.read()
            encoding_type = chardet.detect(raw_data)["encoding"]
    except:
        return

    with open(os.path.join(dir, "log.log"), mode="r", encoding=encoding_type) as file:
        text = file.read()

    # 正则表达式模式定义
    # pattern_template = r"ITERATIVE_FEEDBACK #_#({tag})#_#(.*?)(?=2025|\Z)"
    # tags = ["arch", "plan", "code"]

    pattern_template = r"({tag})(.*?)(?=2025|\Z)"
    tags = [
        "ITERATIVE_FEEDBACK #_#arch#_#",
        "ITERATIVE_FEEDBACK #_#plan#_#",
        "ITERATIVE_FEEDBACK #_#code#_#",
    ]

    matches = {}

    for tag in tags:
        pattern = pattern_template.format(tag=tag)
        match = re.search(pattern, text, re.DOTALL)
        if match:
            matches[tag] = match.group(2).strip()

    with open(os.path.join(dir, "feedbacks.txt"), "w", encoding="utf-8") as file:
        # 输出结果
        for tag, content in matches.items():
            if tag == "ITERATIVE_FEEDBACK #_#arch#_#":
                file.write(f"#_#architecture_feedback#_#\n{content}\n\n")
            elif tag == "ITERATIVE_FEEDBACK #_#plan#_#":
                file.write(f"#_#task_plan_feedback#_#\n{content}\n\n")
            elif tag == "ITERATIVE_FEEDBACK #_#code#_#":
                file.write(f"#_#code_feedback#_#\n{content}\n\n")


def clean_dir(dir):
    files_to_keep = ["prd.md", "feedbacks.txt"]
    try:
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)

            if os.path.isfile(item_path) and item not in files_to_keep:
                os.remove(item_path)
            # 如果是子目录，则直接删除整个目录及其内容
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    base_dir = "E:\Project\ATE\ATEdev_main\project\website"
    i = 1
    input("DELETE")
    for project_name in os.listdir(base_dir):
        print(str(i) + " " + project_name)
        i = i + 1

        project_path = os.path.join(base_dir, project_name)

        log_extract(project_path)

        clean_dir(project_path)

    # 删除单个项目的代码
    # base_dir = "E:\Project\ATE\ATEdev\ATEDev\project\website\CultureFacts"
    # project_path = base_dir

    # # log_extract(project_path)

    # clean_dir(project_path)
