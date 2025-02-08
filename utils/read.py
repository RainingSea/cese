import chardet
import re, os
from pathlib import Path


# 读取文件的原始字节
def read_file_2_line(file_path):

    with open(
        file_path,
        "rb",
    ) as file:
        raw_data = file.read()

    # 检测文件编码
    result = chardet.detect(raw_data)
    encoding = result["encoding"]

    # 使用检测到的编码读取文件内容
    with open(
        file_path,
        "r",
        encoding=encoding,
    ) as file:
        content = file.read()  # 直接读取文件内容，不要使用 repr()

        # Remove special characters like \u200b (zero-width space)
        cleaned_text = re.sub(r"[\u200b]", "", content)

        # Remove tabs and multiple newlines, replace with single newline
        # Replace tabs with a single space
        cleaned_text = re.sub(r"\t+", " ", cleaned_text)
        cleaned_text = re.sub(r"\n\s*\n", "\n", cleaned_text)

        # Remove leading and trailing whitespace from each line
        # cleaned_text = "\n".join(line.strip() for line in cleaned_text.splitlines())
        # print(cleaned_text)

        single_line_cleaned_text = cleaned_text.replace("\n", " ").replace("\r", "")
        return single_line_cleaned_text
        print(single_line_cleaned_text)


def list_files_with_absolute_paths(directory_path):
    result = []
    try:
        # 将字符串路径转换为Path对象
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if not file.endswith(".pyc"):
                    result.append(Path(os.path.join(root, file)))
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def read_dir(dir):
    result = ""
    for file in list_files_with_absolute_paths(dir):
        result = result + os.path.basename(file) + " " + read_file_2_line(file) + "\n"
    return result


def read_codebase(codebase_path):
    content = []
    for root, _, files in os.walk(codebase_path):
        # Calculate the folder depth relative to the input codebase path
        depth = root[len(codebase_path) :].count(os.sep)
        indent = "  " * depth
        content.append(f"{indent}--- DIRECTORY: {root} ---\n")

        for file in files:
            file_type = os.path.splitext(file)[-1].lower()
            if file_type in {".html", ".py", ".txt", ".csv", ".json"}:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                    annotation = f"{indent}  --- FILE: {file} (PATH: {file_path}, TYPE: {file_type}) ---\n"
                    content.append(annotation + file_content + "\n\n")
                except Exception as e:
                    # Handle unreadable files
                    content.append(f"{indent}  --- FILE: {file} (ERROR: {e}) ---\n")
    return "".join(content)


def read_file(path, filename):
    """
    Walk the path and read filename
    Args:
        path: repo path

    Returns:
        str: Content of filename if found, otherwise an error message.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path '{path}' does not exist.")

    for root, _, files in os.walk(path):
        if filename in files:
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read()
            except Exception as e:
                raise RuntimeError(f"Error reading file '{file_path}': {e}")

    raise FileNotFoundError(f"No {filename} file found in the specified path.")


import os
import shutil


def delete_code_folders(root_folder):
    """
    遍历root_folder下的所有直接子文件夹（视为项目），并在每个项目中查找名为'code'的文件夹，
    如果存在，则删除它及其所有内容。

    :param root_folder: 根文件夹路径，包含多个项目的总目录
    """
    # 获取根目录下的所有直接子文件夹（假设这些是项目文件夹）
    for project_folder in os.scandir(root_folder):
        if project_folder.is_dir():  # 确认是文件夹
            code_folder_path = os.path.join(project_folder.path, "code")
            if os.path.exists(code_folder_path) and os.path.isdir(code_folder_path):
                print(f"Deleting folder: {code_folder_path}")
                shutil.rmtree(code_folder_path)
            else:
                print(f"No 'code' folder found in {project_folder.path}")
    print("Task completed.")


# 改变ce目录名称
def rename_ce_folders(root_folder):
    """
    遍历root_folder下的所有直接子文件夹（视为项目），并在每个项目中查找名为'ce'的文件夹，
    如果存在，则将其重命名为'ce_old'。

    :param root_folder: 根文件夹路径，包含多个项目的总目录
    """
    # 获取根目录下的所有直接子文件夹（假设这些是项目文件夹）
    for project_folder in os.scandir(root_folder):
        if project_folder.is_dir():  # 确认是文件夹
            ce_folder_path = os.path.join(project_folder.path, "ce")
            new_ce_folder_path = os.path.join(project_folder.path, "ce_old")

            if os.path.exists(ce_folder_path) and os.path.isdir(ce_folder_path):
                print(f"Renaming folder: {ce_folder_path} to {new_ce_folder_path}")
                os.rename(ce_folder_path, new_ce_folder_path)
            else:
                print(f"No 'ce' folder found in {project_folder.path}")
    print("Task completed.")


def delete_files(root_folder):
    """
    遍历root_folder下的所有直接子文件夹（视为项目），并在每个项目中查找名为'architect.md'的文件，
    如果存在，则删除它。

    :param root_folder: 根文件夹路径，包含多个项目的总目录
    """
    # file = "log.log"
    # file="architect.md"
    file = "task plan.md"

    # 获取根目录下的所有直接子文件夹（假设这些是项目文件夹）
    for project_folder in os.scandir(root_folder):
        if project_folder.is_dir():  # 确认是文件夹
            architect_file_path = os.path.join(project_folder.path, file)
            if os.path.exists(architect_file_path) and os.path.isfile(
                architect_file_path
            ):
                print(f"Deleting file: {architect_file_path}")
                os.remove(architect_file_path)
            else:
                print(f"No 'architect.md' file found in {project_folder.path}")
    print("Task completed.")


if __name__ == "__main__":
    # 设置你的根文件夹路径
    root_folder_path = "D:\Project\CE\CE\project\website"

    # delete_files(root_folder_path)
    rename_ce_folders(root_folder_path)
    # delete_code_folders(root_folder_path)
