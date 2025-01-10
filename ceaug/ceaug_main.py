import shutil

from openai import OpenAI
from utils.read import read_codebase, read_file
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


def make_ce_dirs(project_dir, ce_nums):
    """
    make ce dirs and copy no sampling docuement
    """
    ce_project_paths = []
    # make dir for the whole counter examples
    if not os.path.exists(os.path.join(project_dir, "ce")):
        os.makedirs(os.path.join(project_dir, "ce"))
    ce_project_path = os.path.join(project_dir, "ce")
    for i in range(ce_nums):
        ce_path = os.path.join(ce_project_path, f"ce_{i}")
        os.makedirs(ce_path)
        ce_project_paths.append(ce_path)

        src_dir = project_dir
        dst_dir = ce_path
        src_file = os.path.join(src_dir, "prd.md")
        dst_file = os.path.join(dst_dir, "prd.md")

        try:
            shutil.copy2(src_file, dst_file)  # 使用 copy2() 以保留文件元数据
            print(f"文件 prd 复制完成")
        except IOError as e:
            print(f"无法复制文件 prd: {e}")
        except:
            print(f"复制文件 prd 时发生未知错误")
    return ce_project_paths


def create_ce_document(project_dir, task_plan, log):

    ce_project_path = ""
    # make dir for the whole counter examples
    if not os.path.exists(os.path.join(project_dir, "ce")):
        os.makedirs(os.path.join(project_dir, "ce"))
        ce_project_path = os.path.join(project_dir, "ce")

    # _______________ generate disturbed plan/ arch / prd of counter example ______________
    # generate 2(default) error(disturbed, whatever) task plan
    ce_plans = ce_generate(task_plan, 1, log)
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


def ceaug(base_dir, project_dirs, project_category, project_name, flag, log):

    max_score = -1.0
    code_feedback_selected = ""
    all_unit_test_results = []
    all_code_feedbacks = []
    all_task_plan_feedbacks = []
    all_architecture_feedbacks = []

    for i in range(len(project_dirs)):
        print("Ready Auto Test # # # # # # # # # # # # " + project_dirs[i])
        log.info("Ready Auto Test # # # # # # # # # # # # " + project_dirs[i])

        project_dir = project_dirs[i]

        # 抽取代码，架构，计划
        code_base = read_codebase(os.path.join(project_dir, "code"))
        architecture = read_file(project_dir, "architect.md")
        task_plan = read_file(project_dir, "task plan.md")

        # 编写测试代码testcode.py
        test_code = autogen(project_dir, project_category, project_name)

        # 运行测试代码
        print("workdir before test: " + str(Path.cwd()))
        unit_test_result = runUnitTest(project_dir, project_category)
        log.info(unit_test_result["output"])

        # 切回来目录
        os.chdir(base_dir)
        print("\n --------- Unit Test Result is ----------")
        # print(unit_test_result["output"])
        print()
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

        print("1-| unit test result analysis |")
        log.info("1-| unit test result analysis |")
        print(unit_test_result_analysis)
        log.info(unit_test_result_analysis)
        # input("input to analyze code relevance")
        print("\n###################################")
        log.info("\n###################################")

        # 2. judge if any of the issues is caused by code (rather than other unrelated reasons)
        # m_1, llm's response(unit test result)
        messages.append({"role": "assistant", "content": unit_test_result_analysis})
        # for Architecture feedback and Task Plan feedback
        architecture_messages = messages.copy()
        task_plan_messages = messages.copy()

        # m_2, ask llm to decide if the issues is from code
        messages.append(
            {
                "role": "user",
                "content": "Do you think the error or failure is caused by errors in the project's code or poorly written test cases? If it is a code error, please include a [CODE] at the end of your output. If not, you don't need to add anything. Thank you.",
            }
        )

        relevance = chat_to_LLM(messages)
        print("2-| unit test result analysis and code relevance |")
        print(relevance)
        print("\n###################################")
        log.info("2-| unit test result analysis and code relevance |")
        log.info(relevance)

        if "[CODE]" not in relevance:
            continue

        # input("input to summarize")
        # 3. summarize the code feedback
        # m_3, llm's response(whether from code)
        messages.append({"role": "assistant", "content": relevance})

        # m_4, ask llm to summarize the unit test result
        messages.append(
            {
                "role": "user",
                "content": """Summarize the above mentioned unit test analysis. You only need to summarize the content in the project identified from the unit test result. You need to do 2 jobs:
                ### 1. summarize test pass cases
                Identify all passed test cases (test_XX_XX, marked as "ok"). For each passed case, find the corresponding project code in the codebase (not the test code) mentioned in previous conversations, understand the full implementation thought of the project code related to the test case, then express it in pseudocode format(pseudocode should capture all parts of the code, not just function body). Focus only on the project code, not the test code.

                ### 2. summarize test failed or error cases
                Summarize all previously mentioned failed or error test cases along with their error analyses. then, you need to provide guidance on how to solve these issues. The guidance should adhere to the following aspects:
                (1) Be concise and instructive.
                (2) Must offer insights based on issues revealed by unit tests, highlighting points to watch for when developing the project again.
                (3) Provide guidance at the level of planning, rather than addressing simple code-related issues. 
                (4) don't write guidance on the test.
                (5) don't provide guidance from higher-level aspects such as project management, development pattern, etc.
                Attention: only consider failure or error exclusively those highlighted by the unit tests; areas that may need improvement (e.g., performance or security concerns) but pass the unit tests should be excluded. 
                Besides, the deficiencies of testcode.py (test code) do not need to be summarized. only analyze issues that are relevant to the project's own code.""",
            }
        )

        if flag == "self_evo":
            code_feedback = chat_to_LLM(messages)
            print("Code Feedback")
            print(code_feedback)
            log.info(code_feedback)
            feedback_result = {
                "arch": "Nothing",
                "plan": "Nothing",
                "code": code_feedback,
            }
            return max_score, feedback_result

        # prompt llm to get architecture feedback
        architecture_messages.append(
            {
                "role": "user",
                "content": REFINE_ARCHITECTURE_PROMPT.format(architecture=architecture),
            }
        )
        architecture_feedback = chat_to_LLM(architecture_messages)

        task_plan_messages.append(
            {
                "role": "user",
                "content": REFINE_TASK_PLAN_PROMPT.format(task_plan=task_plan),
            }
        )
        task_plan_feedback = chat_to_LLM(task_plan_messages)

        # _______________ 根据单元测试得到的反馈 ______________
        code_feedback = chat_to_LLM(messages)
        code_feedback_selected = code_feedback
        print("Code Feedback")
        print(code_feedback)
        log.info("Code Feedback\n" + code_feedback)
        # input("input to get architecture feedback")
        print("Architecture Feedback")
        print(architecture_feedback)
        log.info("Architecture Feedback\n" + architecture_feedback)
        # input("input to get plan feedback")
        print("Plan Feedback")
        print(task_plan_feedback)
        log.info("Plan Feedback\n" + task_plan_feedback)

        all_code_feedbacks.append(code_feedback)
        all_architecture_feedbacks.append(architecture_feedback)
        all_task_plan_feedbacks.append(task_plan_feedback)

        all_unit_test_results.append(unit_test_result)

    if flag == "ite_fdback":
        sum_messages = []
        all_summaries = ""
        for k in range(len(all_code_feedbacks)):
            all_summaries = (
                all_summaries
                + "### the "
                + str(k + 1)
                + "th"
                + " project result:\n"
                + f"test result is {all_unit_test_results[k]['output']}: analysis&guidance is {all_code_feedbacks[k]} \n\n"
            )

        # means it is counter example model
        PROMPT_FOR_SUMMARY_MERGE = """# instruction
I have multiple implementations of the same project, each of which has undergone unit testing. For each implementation, I have obtained test results, analyzed them, and developed improvement recommendations. Now, you should extract and compile all my contents with the following requirements:

1.Summarize all test cases: identify how many test_XXX_XXX (like this format) test cases exist in all my result, may not need to outptut.

2.Prepare the output, divided into two parts: Passed Test Cases and Failed or Error Test Cases, with following description:
### Passed Test Cases
Summarize solutions for all test cases that passed. Use the pseudocode provided in the input to represent the solutions; do not generate new pseudocode. Present each case in the format:
1. |Case|:**Case Name**
Followed by the pseudocode which represent the successful implementation for this function.

### Failed or Error Test Cases
Collect the analysis and guidance related to each failure or error. present it in the format:
For each error or failure, extract all related analyses and guidance from allthe content. If there are duplicates, please remove them.
Then, combine them and output them in the following format:
1. |Case|:**Case Name**
Followed by:
Failure/Error Analysis1
Improvement Guidance1 (textual, pseudocode, etc.)
Failure/Error Analysis2
Improvement Guidance2 (textual, pseudocode, etc.)
Each pair above represents content extracted from different projects (after deduplication).
Ensure that if there are differing analyses or guidance for a single test case, all are recorded. 

# Notes:
For ### Passed Test Cases, you need to "summarize"; for ### Failed or Error Test Cases, you need to "extract".
Case Name is the test case name with the test_ prefix removed (e.g., test_navigate_to_registration becomes navigate_to_registration).
Do not summarize guidance specifically for the test code itself.
There is no need to output the list test cases again at the end. 

# Attention
must consider all results in "context", don't omit. don't lose information.
The output should retain the section titles "### Passed Test Cases" and "### Failed or Error Test Cases" as fixed headers for easy differentiation. 

# Format: You Must add a |Case| before the Case Name for differentiation. like |case|: test_a_function, must use two "|".

# context
The content you need to summarize is as follows: {summaries}.\n"""
        summary_merge_values = {"summaries": all_summaries}
        sum_messages.append(
            format_prompt(PROMPT_FOR_SUMMARY_MERGE, summary_merge_values)
        )
        print(sum_messages[0]["content"])
        # log.info("prompt for summaries summary:\n" + sum_messages[0]["content"])
        code_summaries_summary = chat_to_LLM(sum_messages)
        print("Code Feedback is")
        print(code_summaries_summary)
        log.info("Code Feedback is\n" + code_summaries_summary)

        # summary the architecture feedback
        arch_sum_messages = []
        arch_all_summaries = ""
        for g in range(len(all_architecture_feedbacks)):
            arch_all_summaries = (
                arch_all_summaries
                + "### the "
                + str(g + 1)
                + "th"
                + " project result:\n"
                + f"{all_architecture_feedbacks[g]}\n\n"
            )

        PROMPT_FOR_ARCHITECT_MERGE = """You will act as a feedback summarization assistant. Your goal is to analyze multiple sets of architecture-related feedback for a software development project and produce a concise, unified summary.
## Instructions:
1. Combine Similar Feedback:Identify and merge duplicate or overlapping suggestions while retaining their key points. For example, if multiple feedback items suggest improving navigation in the UI, consolidate them into a single suggestion.
2. Retain Unique Feedback:Preserve suggestions that address distinct issues, even if they apply to different aspects of the project. Ensure no unique feedback is omitted.
3.Structure the Output:
Overall Evaluation
Specific Problems and Suggestions
Architecture Enhancements

Attention:Use bullet points for readability, and provide actionable suggestions where applicable.
Ensure Clarity and Precision.
Use concise language to convey the ideas clearly and avoid redundancy.
the content you need to summarize is:{summaries}.
        """
        arch_summary_merge_values = {"summaries": arch_all_summaries}
        arch_sum_messages.append(
            format_prompt(PROMPT_FOR_ARCHITECT_MERGE, arch_summary_merge_values)
        )
        print(arch_sum_messages[0]["content"])
        # log.info("prompt for summaries summary:\n" + sum_messages[0]["content"])
        arch_summaries_summary = chat_to_LLM(arch_sum_messages)
        print("Archtecture Summary")
        print(arch_summaries_summary)
        log.info("Archtecture Summary\n" + arch_summaries_summary)

        # plan summary
        plan_sum_messages = []
        plan_all_summaries = ""
        for i in range(len(all_task_plan_feedbacks)):
            plan_all_summaries = (
                plan_all_summaries
                + "### the "
                + str(i + 1)
                + "th"
                + " project result:\n"
                + f"{all_task_plan_feedbacks[g]}\n\n"
            )

        PROMPT_FOR_PLAN_MERGE = """You will act as a feedback summarization assistant. Your goal is to analyze multiple sets of task-related feedback for a software development project and produce a concise, unified summary.You will receive multiple feedback reports, each containing various suggestions, including areas for improvement and potential enhancements. Your task is to extract suggestions that are useful for generating new plans and meet the following requirements:
1.Categorize Suggestions: Group the suggestions into the following categories:
Specific Areas for Improvement
Suggested Enhancements
2.Merge Similar Suggestions: Combine identical or highly similar suggestions into a single statement, using clear and concise language.
3.Retain Unique Suggestions: Keep unique suggestions that appear in only one feedback report but are valuable for improvement. Highlight their source where applicable.
4.Organized Output: Structure the output clearly and logically by category and priority (if mentioned), making it easy for planners to incorporate into new plans.
output example:
### Specific Areas for Improvement:  
- Add logout functionality and error reporting for failed login/registration attempts.  
- Clarify task descriptions for edge cases, including invalid input, duplicate registrations, and empty feedback submissions.  
- Break down complex tasks (e.g., FeedbackManager implementation) into subtasks focusing on validation and file handling.  

### Suggested Enhancements:  
- Prioritize user authentication tasks, followed by feedback submission and navigation.  
- Specify expected behaviors after user actions, such as feedback confirmation messages.  
- Implement basic form validations to prevent invalid or empty submissions.  
Use this format to summarize the feedback provided, ensuring the suggestions are actionable for creating improved new plans.

the content you need to summarize is:{summaries}. follow the example, output you summary.
        """
        plan_summary_merge_values = {"summaries": plan_all_summaries}
        plan_sum_messages.append(
            format_prompt(PROMPT_FOR_PLAN_MERGE, plan_summary_merge_values)
        )
        print(plan_sum_messages[0]["content"])
        # log.info("prompt for summaries summary:\n" + sum_messages[0]["content"])
        plan_summaries_summary = chat_to_LLM(plan_sum_messages)
        print("Plan Summary")
        print(plan_summaries_summary)
        log.info("Plan Summary\n" + plan_summaries_summary)

        # get respective feedback: architecture suggestion, task plan suggestion, code suggestion
        # return 3 feedback

        feedback_result = {
            "arch": arch_summaries_summary,
            "plan": plan_summaries_summary,
            "code": code_summaries_summary,
        }
        return max_score, feedback_result

    # if no code feedback generated
    if code_feedback_selected:
        print("final selected:\n" + code_feedback_selected)
        # log.info("final selected:\n" + code_feedback_selected)
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


def feedback_split(feedback):
    # 提取所有通过的测试结果
    passed_test_cases = re.search(
        r"(?<=### Passed Test Cases)(.*?)(?=### Failed or Error Test Cases|$)",
        feedback,
        re.DOTALL,
    )
    if passed_test_cases:
        print(passed_test_cases)
        pattern = r"\|Case\|:.*?(?=\n\d+\.\s\|Case\|:|\Z)"
        pass_case_blocks = re.findall(
            pattern, passed_test_cases.group(0).strip(), re.DOTALL
        )
        pass_feedback = process_array(pass_case_blocks)
    else:
        pass_feedback = None

    # 提取没有通过测试的结果
    failed_or_error_test_cases = re.search(
        r"(?<=### Failed or Error Test Cases)(.*)", feedback, re.DOTALL
    )
    if failed_or_error_test_cases:
        print(failed_or_error_test_cases)
        pattern = r"\|Case\|:.*?(?=\n\d+\.\s\|Case\|:|\Z)"
        no_pass_case_blocks = re.findall(
            pattern, failed_or_error_test_cases.group(0).strip(), re.DOTALL
        )
        no_pass_feedback = process_array(no_pass_case_blocks)
    else:
        no_pass_feedback = None

    return pass_feedback, no_pass_feedback


def process_array(arr):
    n = len(arr)
    if n > 8:
        # 每个新数组元素包含原数组的 1/4 个元素（取下界）
        chunk_size = n // 4
        new_array = [arr[i * chunk_size : (i + 1) * chunk_size] for i in range(4)]
        # 如果还有剩余元素，新建一个额外的元素
        remaining = arr[4 * chunk_size :]
        if remaining:
            new_array.append(remaining)
    else:
        # 每个新数组元素包含原数组的 2 个元素，最后一个可能是 1 个
        chunk_size = 2
        new_array = [arr[i : i + chunk_size] for i in range(0, n, chunk_size)]
    return ["".join(chunk) for chunk in new_array]


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
    with open("D:\Project\CE\CE\seed.txt", "a") as file:
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


REFINE_ARCHITECTURE_PROMPT = """
### Instructions:
You are a software architect reviewing a Python project. 
Below are the details about the implementation, UI, data storage, 
file list, and data structures. 
Based on the architecture details, the context of unit testing results, 
the unit test code, the unit test result analysis, and the codebase, 
please provide improvement suggestions in the following areas:

### Architecture Details:
{architecture}

### Request:

1. **Overall Evaluation:**
   - Strengths: What works well in terms of **implementation**, **UI**, and **data structures**?
   - Weaknesses: What needs improvement in these areas?

2. **Specific Problems:**
   - Identify weaknesses and explain:
     - Problem: Describe the issue (e.g., missing features like login, registration).
     - Suggestions: Propose actionable solutions.
     - Problem: Describe the issue (e.g., missing files like main.py).
     - Suggestions: Propose actionable solutions.

3. **Architecture Enhancements:**
   - Implementation: Is Flask appropriate for this project?
   - UI Design: How can UI be improved to meet functional requirements?
   - Data Storage: Have the local text files covered all the necessary data? If not, make sure to add the required data.

### Attention
1. This is only a small project, we don't consider too much about scalability.
2. We don't use any database.
3. Don't provide guidance from higher-level aspects such as project management, development pattern, etc.
---------------------------
### Output Example:

1. **Overall Evaluation:**
   - **Strengths:**
     - Simple architecture suitable for small-scale projects.
     - Text file storage works well at this scale.
   - **Weaknesses:**
     - UI lacks filtering and sorting features.
     - Text files lack organization, making scaling difficult.

2. **Specific Problem Areas:**
   - **Problem 1:** UI lacks filtering and sorting features.
     - **Suggestions:** Add basic filtering and sorting functionalities.

3. **Architecture Enhancements:**
   - **Implementation:** Flask is suitable, but separate models and views for better clarity.
   - **UI Design:** Add filtering, searching, and sorting.
   - **Data Storage:** Add users.txt to store user accounts
   - **Data Structures:** Ensure classes focus on single responsibilities.

"""

REFINE_TASK_PLAN_PROMPT = """
### Task Plan Review:

You are an experienced software architect tasked with reviewing a Python web application task plan. 
The task plan outlines packages, logic, file structure, and tasks. 
Based on the task plan details, the context of unit testing results, 
the unit test code, the unit test result analysis, and the codebase, 
provide feedback on:

### Task Plan:
{task_plan}

### Request:
1. **Overall Evaluation:**
   - Does the task list cover key areas like user authentication, data storage, UI, and project management?
   - Are the tasks clear, actionable, and appropriately detailed for team understanding?

2. **Specific Areas for Improvement:**
   - **Missing Features:** Are there any basic features in test_xxx_xxx (e.g., login, registration) not implemented?
   - **Unclear Tasks:** Are any tasks vague or lacking detail (e.g., edge cases, assumptions)?
   - **Task Breakdown:** Are tasks appropriately sized and clear in their scope?
   - **Dependencies:** Are task dependencies well identified to avoid delays?

3. **Suggested Enhancements:**
   - **Prioritization:** Which tasks should be completed first for better workflow?
   - **Clarity:** Are any tasks lacking clarity and in need of more details or smaller sub-tasks?
   - **Feature Clarification:** Are there any features that need further elaboration?
   - **Task Grouping:** Should tasks be grouped for better clarity or workflow?
   - **Additional Considerations:** Are there any aspects (e.g., UI flow) not addressed in the plan?

### Attention
1. Provide **task plan-level feedback** with a focus on **task clarity**, and **workflow**.
2. This is only a small project, we don't consider too much about scalability.
3. We don't use any database.
4. We don't use hash or security check.
5. Don't provide guidance from higher-level aspects such as project management, development pattern, etc.

----------------------

### Example Output:

**1. Overall Evaluation:**
- **Strengths:** Covers key areas like user authentication, UI, and project management. UI components are well-defined.
- **Weaknesses:** Lacks details on handling edge cases and data validation.

**2. Specific Areas for Improvement:**
- **Missing Features:** Add tasks for login and registration.
- **Unclear Tasks:** `project_management.html` and `freelancer_profile.html` need more details on features (e.g., project editing, profile editing).
- **Task Breakdown:** Break down larger tasks like `profile_management.html` into smaller subtasks.
- **Dependencies:** Prioritize user login and registration first.

**3. Suggested Enhancements:**
- **Prioritization:** Implement authentication first to handle user data.
- **Clarity:** Add more details on form validation for login/registration.
- **Feature Clarification:** Specify editable fields for freelancer profile.
- **Task Grouping:** Group UI tasks for consistency.
- **Additional Considerations:** Consider optimizing the data in text file for correctness.

"""

if __name__ == "__main__":
    ceaug()
