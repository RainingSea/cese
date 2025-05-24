import os, io
import openai
from openai import OpenAI
from pathlib import Path
import re
import subprocess
import pandas as pd
import sys
import unittest
from utils.read import read_dir, read_file_2_line
from ceaug.auto_test_prompt import (
    prompt_for_game_testing,
    prompt_for_gui_testing,
    prompt_for_web_testing,
)


### reletive path: codebase
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


### reletive path: testcase
def read_md_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"Error: Could not read the file '{file_path}'. Reason: {e}"


def chat_to_LLM(messages):

    client = OpenAI(
        api_key="sk-JQiygLRku49PwPTtPTax1mcy97OFAlO4EagYvHWlCVBVTUmC",  # 只需要填写key就可以了
        base_url="https://api.chatanywhere.tech",
    )
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        # stream=True, # 这个开了要用chunk的调用方法
    )
    # print(response.choices[0].message.content, end="", flush=True)
    return response.choices[0].message.content


### gpt api
def call_openai_api(prompt, model):
    client = OpenAI(
        api_key="sk-JQiygLRku49PwPTtPTax1mcy97OFAlO4EagYvHWlCVBVTUmC",
        base_url="https://api.chatanywhere.tech",
    )
    try:
        response = client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}], temperature=0.2
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def extract_python_code(llm_response):
    """
    Extract Python code blocks from LLM response.

    Args:
    - llm_response (str): The text response from LLM.

    Returns:
    - str: Extracted Python code.
    """
    # Use regex to extract code blocks between ```python and ```
    code_blocks = re.findall(r"```python\n(.*?)```", llm_response, re.DOTALL)
    return "\n\n".join(code_blocks)


def save_test_code(codebase_path, llm_response):
    """
    Extract Python code from LLM response and save it to testcode.py in the given codebase path.

    Args:
    - codebase_path (str): The path to the codebase folder where the file will be saved.
    - llm_response (str): The text response from LLM containing Python code.
    """
    # Ensure the path exists
    if not os.path.exists(codebase_path):
        os.makedirs(codebase_path)

    # Extract Python code from LLM response
    python_code = extract_python_code(llm_response)

    # Define the testcode.py file path
    # By default, write this test files to code path.
    testcode_path = os.path.join(codebase_path, "testcode.py")

    # Write the extracted code to testcode.py
    with open(testcode_path, "w", encoding="utf-8") as file:
        file.write(python_code)
    return testcode_path


def run_test_code(file_path):
    """
    Runs the Python script at the given file path and captures the output.

    Args:
    - file_path (str): Path to the Python file to run.

    Returns:
    - str: The output of the script execution.
    """
    try:
        result = subprocess.run(
            ["python", file_path], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error during execution: {e.stderr}"


def test_code_autogen(codebase_path, category, project_name):

    project_category = category

    if os.path.exists(os.path.join(codebase_path, "testcode.py")):
        print("### Already exist a testcode.py ###")
        testcode = read_file_2_line(os.path.join(codebase_path, "testcode.py"))
        return testcode
    # 只处理文件夹
    if os.path.isdir(codebase_path):

        # 换成绝对路径
        # 后期这里要更换，就是不刷数据集的情况下：在命令行里提供是否包含测试用例的参数，如果包含，就按类似这种方法提取；如果不包含，就生成测试用例，并且返回测试用例路径
        testcase_path = os.path.join(
            # "D:\\algorithm\\agent\\cese\\dataset\\FSD-bench\\testcase",
            "D:/Project/CE/CE/dataset/FSD-bench/testcase",
            category,
            f"TestCases_{project_name}.md",
        )
        # 读取代码库和测试用例文件
        codebase = read_codebase(codebase_path)
        print(f"Codebase :\n{codebase}")
        testcase = read_md_file(testcase_path)
        print(f"Test Cases:\n{testcase}")
        # 创建prompt并替换变量
        prompt = None
        if project_category == "website":
            prompt = prompt_for_web_testing
        elif project_category == "gui":
            prompt = prompt_for_gui_testing
        else:
            prompt = prompt_for_game_testing
        prompt = prompt.replace("{codebase}", codebase)
        prompt = prompt.replace("{testcase}", testcase)
        # 调用OpenAI API获取测试代码
        test_code = call_openai_api(prompt=prompt, model="gpt-4o")
        print(f"Test code:\n{test_code}")
        # 保存生成的测试代码并运行测试
        testcode_path = save_test_code(
            codebase_path=codebase_path, llm_response=test_code
        )
        return extract_python_code(test_code)


def clear_imports():
    """
    Clears imported modules from sys.modules to avoid import errors
    when running tests in different directories.
    """
    for module in list(sys.modules.keys()):
        if module.startswith("testcode"):
            del sys.modules[module]


def web_text_strip(input_text):

    patterns = [
        r"^.*?GetHandleVerifier.*$",
        r"^.*?\(No symbol\).*$",
        r"^.*?BaseThreadInitThunk.*$",
        r"^.*?RtlUserThreadStart.*$",
    ]

    # Combine patterns into a single regex
    combined_pattern = re.compile("|".join(patterns), re.MULTILINE)
    # Remove matching lines
    cleaned_text = re.sub(combined_pattern, "", input_text)
    # Remove extra blank lines
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text).strip()
    print(cleaned_text)
    return cleaned_text


def runUnitTest(codebase_path, project_category, project_name):

    print(f"----------------[START {project_name}]---------------------")
    os.chdir(codebase_path)
    print(f"CURRENT DIR1 {codebase_path}")
    # 在加载测试前清理模块缓存
    clear_imports()
    # 加载测试文件 (testcode.py)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # 自动加载 testcode.py 文件中的测试用例
    suite.addTests(loader.discover("."))
    output_stream = io.StringIO()

    # 创建 TextTestRunner 实例，运行测试用例并输出结果
    runner = unittest.TextTestRunner(stream=output_stream)
    result = runner.run(suite)

    test_output = output_stream.getvalue()
    if project_category == "website":
        # filter out some unimportant and repetitive output.
        print("#### strip ####")
        test_output = web_text_strip(test_output)

    total = int(result.testsRun)
    passed = int(result.testsRun - len(result.failures) - len(result.errors))
    failed = len(result.failures)
    errors = len(result.errors)
    info = {
        "category": project_category,
        "project_name": project_name,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "total": total,
        "output": test_output,
    }
    print(f"Total tests run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    print(f"----------------[END {project_name}]---------------------")

    print(info)
    # 清除当前的测试套件和加载器
    suite._tests.clear()  # 清除测试套件中的测试用例
    loader = None  # 清除测试加载器对象
    suite = None  # 清空 TestSuite 对象
    output_stream.close()  # 关闭 StringIO 流
    return info
