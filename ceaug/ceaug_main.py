import shutil

from openai import OpenAI
from utils.read import read_codebase
from ceaug.auto_test import *
from utils.read import read_file_2_line
import re, random
import ast
from openai import OpenAI
import time
import math
from datetime import datetime


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


def format_prompt(template, values):
    result = template.format_map(values)
    return {"role": "user", "content": result}


def create_ce_document(project_dir, task_plan, log):

    ce_project_path = ""
    # make dir for the whole counter examples
    if not os.path.exists(os.path.join(project_dir, "ce")):
        os.makedirs(os.path.join(project_dir, "ce"))
        ce_project_path = os.path.join(project_dir, "ce")

    # _______________ generate disturbed plan/ arch / prd of counter example ______________
    # generate 2(default) error(disturbed, whatever) task plan
    ce_plans = ce_generate(task_plan, 5, log)
    ce_project_paths = []
    # make a directory for each counter example, and create prd, arch, task plan.
    for i in range(len(ce_plans)):
        ce_path = os.path.join(ce_project_path, f"ce_{i}")
        os.makedirs(ce_path)
        # create ce plan
        with open(os.path.join(ce_path, "task plan.md"), "w", encoding="utf-8") as f:
            f.write(str(ce_plans[i]))

        # copy prd and architect
        src_dir = project_dir
        dst_dir = ce_path

        # copy prd
        src_file = os.path.join(src_dir, "prd.md")
        dst_file = os.path.join(dst_dir, "prd.md")

        try:
            shutil.copy2(src_file, dst_file)  # 使用 copy2() 以保留文件元数据
            print(f"文件 prd 复制完成")
        except IOError as e:
            print(f"无法复制文件 prd: {e}")
        except:
            print(f"复制文件 prd 时发生未知错误")

        # copy arch
        src_file = os.path.join(src_dir, "architect.md")
        dst_file = os.path.join(dst_dir, "architect.md")

        try:
            # 复制文件到目标目录
            shutil.copy2(src_file, dst_file)  # 使用 copy2() 以保留文件元数据
            ce_project_paths.append(ce_path)
            print(f"文件 arch 复制完成")
        except IOError as e:
            print(f"无法复制文件 arch: {e}")
        except:
            print(f"复制文件 prd 时发生未知错误")

    # _______________ generate disturbed plan/ arch / prd of counter example ______________
    return ce_project_paths


def ceaug(base_dir, project_dirs, project_category, project_name, user_req, log):

    max_score = -1.0
    code_feedback_selected = ""
    all_code_feedbacks = []
    all_unit_test_results = []
    for i in range(len(project_dirs)):
        print("Ready Auto Test # # # # # # # # # # # # " + project_dirs[i])
        log.info("Ready Auto Test # # # # # # # # # # # # " + project_dirs[i])

        project_dir = project_dirs[i]
        code_base = read_codebase(os.path.join(project_dir, "code"))
        # 编写测试代码testcode.py
        test_code = autogen(project_dir, project_category, project_name)

        # 运行测试代码
        print("workdir before test: " + str(Path.cwd()))
        unit_test_result = runUnitTest(project_dir, project_category)
        log.info("unit_test_result" + str(unit_test_result))
        # 切回来目录
        os.chdir(base_dir)
        print("\n### # # # # # # # # # # #")
        print(unit_test_result["output"])
        print("\n### # # # # # # # # # # #")

        # _________________ ask LLM to get feedback ________________
        # 1. ask LLM to analyze the unit test results
        messages = []

        values = {
            "code_base": code_base,
            "unit_test_code": test_code,
            "test_results": str(unit_test_result),
        }

        # m_0, ask llm to analyze the unit test result
        PROMPT_FOR_TEST_ANA = """You are a software test analyst. Please help me analyze the code of a project.
        Here is the entire codebase for a project: {code_base}.
        Here are the unit test codes for this project: {unit_test_code}.
        These are all the unit test results (Only failed tests have detailed information):{test_results}
        Please analyze the test results one by one with related code. For each failed or error unit test, step by step to identify the reasons.
        If test code like "self.fail(XXX functionality not implemented)" occurs, it suggests a problem with the project code, not the test code.
        """
        messages.append(format_prompt(PROMPT_FOR_TEST_ANA, values))
        unit_test_result_analysis = chat_to_LLM(messages)

        log.info(messages[0]["content"])
        print("1-| unit test result analysis |")
        print(unit_test_result_analysis)
        print("\n###################################")

        # 2. judge if any of the issues is caused by code (rather than other unrelated reasons)
        # m_1, llm's response(unit test result)
        messages.append({"role": "assistant", "content": unit_test_result_analysis})
        log.info(str(messages[1]["content"]))
        # m_2, ask llm to decide if the issues is from code
        messages.append(
            {
                "role": "user",
                "content": "Do you think the issue is caused by errors in the project's code or poorly written test cases? If it is a code error, please include a [CODE] at the end of your output. If not, you don't need to add anything. Thank you.",
            }
        )
        log.info(str(messages[2]["content"]))
        relevance = chat_to_LLM(messages)
        print("2-| unit test result analysis and code relevance |")
        print(relevance)
        print("\n###################################")

        if "[CODE]" not in relevance:
            log.info("GOOD PATH GOOD PATH" + str(project_dirs[i]))
            continue
            # return max_score, "CodeIsGood"

        # 3. summarize the code feedback
        # m_3, llm's response(whether from code)
        messages.append({"role": "assistant", "content": relevance})
        log.info(str(messages[3]["content"]))
        # m_4, ask llm to summarize the unit test result
        messages.append(
            {
                "role": "user",
                "content": """Summarize the above mentioned unit test analysis. You only need to summarize the content in the project identified from the unit test result. You need to do 2 jobs:
                ### 1. summarize test pass cases
                Identify all passed test cases (test_XX_XX, marked as "ok"). For each passed case, find the corresponding project code in the codebase (not the test code) mentioned in previous conversations, understand the full implementation thought of the project code related to the test case, then express it in pseudocode format(pseudocode should capture all parts of the code, not just function body). Focus only on the project code, not the test code.

                ### 2. summarize test failed or error cases
                Summarize all previously mentioned failed or error test cases along with their error analyses and guidance.
                then, you need to provide guidance on how to write better project code (not related to testing). The guidance should adhere to the following aspects:
                (1) Be concise and instructive.
                (2) Must offer insights based on issues revealed by unit tests, highlighting points to watch for when developing the project again.
                (3) Provide guidance at the level of planning, rather than addressing simple code-related issues. 
                (4) don't write guidance on the test.
                (5) Only guidance related to the code is needed, without analyzing higher-level aspects such as project management, development models, etc.
                Attention: only consider failure or error exclusively those highlighted by the unit tests; areas that may need improvement (e.g., performance or security concerns) but pass the unit tests should be excluded. 
                Besides, the deficiencies of testcode.py (test code) do not need to be summarized. only analyze issues that are relevant to the project's own code.""",
            }
        )

        # _______________ 根据单元测试得到的反馈 ______________
        code_feedback = chat_to_LLM(messages)
        code_feedback_selected = code_feedback
        print(code_feedback)
        log.info(code_feedback)

        all_code_feedbacks.append(code_feedback)
        all_unit_test_results.append(unit_test_result)

    if len(project_dirs) > 1 and len(all_code_feedbacks) > 1:
        sum_messages = []
        all_summaries = ""
        for k in range(len(all_code_feedbacks)):
            all_summaries = (
                all_summaries
                + "the "
                + str(k)
                + "th result "
                + f"|(problem){all_unit_test_results[k]['output']}:(solution){all_code_feedbacks[k]}|\n"
            )

        # means it is counter example model
        PROMPT_FOR_SUMMARY_MERGE = """# instruction
I have multiple implementations of the same project, and I conducted respective unit tests, obtained results, analysis, guidance for each project. Now, you should summarize all my results. Here's what you need to do:
1.Summarize all test points: identify how many test_XXX_XXX (like this format) test points exist in all my result, may not need to outptut.
2.Prepare the output, two parts:
(2-1) For test points that passed, summarize the solutions from all results. Present the information as (Test Point + Pseudocode). the pseudocode has been given in input summary, use them. During the output, label this part as good and referable.
(2-2) For test points that failed or error, collect analysis and guidances related to this failure or error from all given results in the "#context". Then analyze and summarize them, present as (Test Point + Failure/Error Analysis(summarized from all results) + Improvement Guidance(textural,pseudocode,etc. summarized from all results)). 

# Attention
There is no need to output the list test cases again at the end. must consider all results in "context", don't omit. 
# Attention
try best to make a good summary while keeping the original content of the given result as much as possible, don't lose information. 
# Attention
if there are different analysis or guidance for one testcase, you should record them all. don't summarize guidance for testcode.
# context
The content you need to summarize is as follows: {summaries}."""
        summary_merge_values = {"summaries": all_summaries}
        sum_messages.append(
            format_prompt(PROMPT_FOR_SUMMARY_MERGE, summary_merge_values)
        )
        print(sum_messages[0]["content"])
        log.info("prompt for summaries summary:\n" + sum_messages[0]["content"])
        summaries_summary = chat_to_LLM(sum_messages)
        log.info("summaried summaries:\n" + summaries_summary)
        return max_score, summaries_summary

    if code_feedback_selected:
        print("final selected:\n" + code_feedback_selected)
        log.info("final selected:\n" + code_feedback_selected)
        return max_score, code_feedback_selected
    else:
        # code has no problem, maybe other fact"
        return max_score, "CodeIsGood"


# _______________ useful functions _______________
# _______________ useful functions _______________
def ce_generate(
    task_plan,
    ce_number,
    log,
):

    ce_result = []
    for i in range(ce_number):
        # avoid affecting the original plan.
        new_task_plan = task_plan
        # task_list_dict_copy = task_list_dict.copy()
        # # disturbing, get counter example task list
        # ce = disturbing(task_list_dict_copy, log)
        # # replace the origin task list to disturbed task list
        # new_task_plan["Task list"] = ce

        ce_result.append((new_task_plan))

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
    print()
    return task_dict


def disturbing(task_list_dict, log):
    """
    accept a task_dict, apply disturbing strategy to it.
    """
    # ________  swap the order of two tasks _________
    # return perform_swaps(task_dict)
    # ________  swap the order of two tasks _________

    # _________ remove a task(randomly) _________
    # return remove_task(task_list_dict)
    # _________ remove a task(randomly) _________

    # _________ edit a task _________
    # return edit_task(task_list_dict, log)
    # _________ edit a task _________

    # ________ no disturbing, just return the original one __________
    return task_list_dict
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


def edit_task(d, log):
    """
    edit one task
    """

    if not d:
        print("The dictionary is empty, nothing to remove.")
        return None
    # seed
    seed_value = int(time.time())
    # "D:\Project\CE\CE\seed.txt"
    with open("D:\\algorithm\\agent\\cese\\seed.txt", "a") as file:
        file.write(str(datetime.now()) + " " + str(seed_value))
    random.seed(seed_value)
    #
    keys = list(d.keys())
    num_to_select = max(1, round(len(keys) * 0.25))
    keys_to_edit = random.sample(keys, num_to_select)

    messages = []
    _log_task = ""
    print("before edit")
    for key, value in d.items():
        print(f"Key: {key}, Value: {value}")
        _log_task = _log_task + f"Key: {key}, Value: {value}" + "\n"

    template = """Here is a task plan list for implementing a project. I have selected one task, and now I want to create a negative example based on this task. Please make the task I selected more vague.
    You only need to return an edited task.
    I will provide you with an example where the task of creating a freely selectable area is omitted, and instead, a fixed area is selected. Please replicate this kind of mistake or ambiguous task behavior.
    # Example:
    input:Implement the image cropping feature by allowing users to freely select a region, then crop that region as the output.
    output:Implement the image cropping feature, allowing users to crop a central region as the result.
    ---
    the whole task plan is:{task_plan},
    the task I selected is:{task},
    follow instruction and return {num} edited task. 
    In the output, any unclear tasks or tasks that require special marking should be enclosed within two ***(3-star) symbols, and each task should end with '[end]' to facilitate the distinction between different parts of the task.
    example:
    ***
    T1:vague task1[end]
    T2:vague task2[end]
    ...
    ***
    """
    messages.append(
        {
            "role": "user",
            "content": template.format_map(
                {
                    "task_plan": _log_task,
                    "task": str(keys_to_edit),
                    "num": str(num_to_select),
                }
            ),
        }
    )
    edited_tasks = chat_to_LLM(messages)
    print(edited_tasks)
    log.info(edited_tasks)
    matches = re.findall(r"\*\*\*(.*?)\*\*\*", edited_tasks, re.DOTALL)
    print(matches[0].strip())
    match = re.search(r"\*\*\*(.*?)\*\*\*", edited_tasks)
    if match:
        # 获取被三个星号包围的内容
        enclosed_content = match.group(1)

        sentences = [
            sentence.strip()
            for sentence in enclosed_content.split("[end]")
            if sentence.strip()
        ]

        print(sentences)
        for i in range(len(sentences)):
            parts = sentences[i].split(":", 1)
            if len(parts) == 2:
                vague_key = parts[0].strip()  # 左侧内容
                vague_task = parts[1].strip()  # 右侧内容
                d[vague_key] = vague_task
    else:
        print("No content found between ***.")

    return d


# _______________ useful functions _______________
# _______________ useful functions _______________

if __name__ == "__main__":
    ceaug()
