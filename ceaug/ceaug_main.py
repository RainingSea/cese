import shutil

from openai import OpenAI
from utils.read import read_codebase
from ceaug.auto_test import *
from ceaug.auto_test_prompt import PROMPT_FOR_TEST_ANA, PROMPT_FOR_SCORING
from ceaug.manipulate import ce_generate
from utils.read import read_file_2_line


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


def make_ce_dirs(project_dir, task_plan):

    # _______________ generate disturbed plan/ arch / prd of counter example ______________
    # generate 2(default) error(disturbed, whatever) task plan
    ce_plans = ce_generate(task_plan)
    ce_project_paths = []
    ce_project_path = ""

    if not os.path.exists(os.path.join(project_dir, "ce")):
        os.makedirs(os.path.join(project_dir, "ce"))
        ce_project_path = os.path.join(project_dir, "ce")

    for i in range(len(ce_plans)):
        ce_path = os.path.join(ce_project_path, f"ce_{i}")
        os.makedirs(ce_path)
        # create ce plan
        with open(os.path.join(ce_path, "task plan.md"), "w", encoding="utf-8") as f:
            f.write(ce_plans[i])
        # copy prd and architect
        src_dir = project_dir
        dst_dir = ce_path
        src_file = os.path.join(src_dir, "prd.md")
        dst_file = os.path.join(dst_dir, "prd.md")

        # 检查是否为文件（而不是目录）
        try:
            # 复制文件到目标目录
            shutil.copy2(src_file, dst_file)  # 使用 copy2() 以保留文件元数据
            print(f"文件 prd 复制完成")
        except IOError as e:
            print(f"无法复制文件 prd: {e}")
        except:
            print(f"复制文件 prd 时发生未知错误")

        src_file = os.path.join(src_dir, "architect.md")
        dst_file = os.path.join(dst_dir, "architect.md")

        # 检查是否为文件（而不是目录）
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


def ceaug(
    project_dirs,
    user_req,
):
    # 获取代码仓库
    # 默认操作code文件夹
    # project_dirs = [
    #     "D:\Project\CE\CE\project\game\WordLinkPuzzle",
    #     "D:\Project\CE\CE\project\game\WordLinkPuzzle_1",
    #     "D:\Project\CE\CE\project\game\WordLinkPuzzle_2",
    # ]
    # generate ce project dirs (not contains code)
    # project_dirs = make_ce_dirs(project_dir, task_plan)

    max_score = -1.0
    code_feedback_selected = ""

    user_req = read_file_2_line(
        "D:\Project\CE\CE\dataset\SD-bench\dataset\game\WordLinkPuzzle.md"
    )

    for i in range(len(project_dirs)):
        print("# # # # # # # # # # # # " + project_dirs[i])
        project_dir = project_dirs[i]

        code_base = read_codebase(os.path.join(project_dir, "code"))
        # 编写测试代码testcode.py并保存在code文件夹中
        test_code = autogen(project_dir)

        # 运行测试代码，并保存结果在一个log文件中
        unit_test_result = runUnitTest(project_dir)
        print(unit_test_result["output"])
        print("\n###################################")

        # _________________ ask LLM to get feedback ________________
        # 1. ask LLM to analyze the unit test results
        messages = []

        values = {
            "code_base": code_base,
            "unit_test_code": test_code,
            "test_results": unit_test_result["output"],
        }

        messages.append(format_prompt(PROMPT_FOR_TEST_ANA, values))
        unit_test_result_analysis = chat_to_LLM(messages)

        print(unit_test_result_analysis)
        print("\n###################################")

        # 2. judge if any of the issues is caused by code (rather than other unrelated reasons)
        messages.append({"role": "assistant", "content": unit_test_result_analysis})
        messages.append(
            {
                "role": "user",
                "content": "Do you think the issue is caused by errors in the project's code or poorly written test cases? If it is a code error, please include    a [CODE] at the end of your output. If not, you don't need to add anything. Thank you.",
            }
        )
        relevance = chat_to_LLM(messages)
        print(relevance)
        print("\n###################################")

        # 3. summarize the code feedback
        messages.append({"role": "assistant", "content": relevance})
        messages.append(
            {
                "role": "user",
                "content": "summarize the issues in this project's code based on all the unit test results. Issues about the test codes is not needed to analyze.   ",
            }
        )
        code_feedback = chat_to_LLM(messages)
        print(code_feedback)
        print("\n###################################")

        # 4. scoring the unit test result issues (0~10)
        messages.append({"role": "assistant", "content": code_feedback})
        values_scoring = {
            "user_req": user_req,
        }
        messages.append(format_prompt(PROMPT_FOR_SCORING, values_scoring))
        score_result = chat_to_LLM(messages)
        print(score_result)
        print("\n###################################")

        start_tag = "[END]"
        end_tag = "[END]"
        start_index = score_result.find(start_tag) + len(start_tag)
        end_index = score_result.find(end_tag, start_index)

        # 提取出的内容
        score = float(score_result[start_index:end_index])
        # _________________ ask LLM to get feedback ________________
        print(score)
        print(code_feedback)

        if score > max_score:
            max_score = score
            code_feedback_selected = code_feedback

    print(code_feedback_selected)

    return code_feedback_selected
    # return code_feedback


## _________________ ask LLM to get feedback ________________


if __name__ == "__main__":
    ceaug()
