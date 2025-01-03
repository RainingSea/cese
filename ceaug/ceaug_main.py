import shutil

from openai import OpenAI
from utils.read import read_codebase
from ceaug.auto_test import *
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


def create_ce_document(project_dir, task_plan, log):

    ce_project_path = ""
    # make dir for the whole counter examples
    if not os.path.exists(os.path.join(project_dir, "ce")):
        os.makedirs(os.path.join(project_dir, "ce"))
        ce_project_path = os.path.join(project_dir, "ce")

    # _______________ generate disturbed plan/ arch / prd of counter example ______________
    # generate 2(default) error(disturbed, whatever) task plan
    ce_plans = ce_generate(task_plan,log)
    ce_project_paths = []
    # make a directory for each counter example, and create prd, arch, task plan.
    for i in range(len(ce_plans)):
        ce_path = os.path.join(ce_project_path, f"ce_{i}")
        os.makedirs(ce_path)
        # create ce plan
        with open(os.path.join(ce_path, "task plan.md"), "w", encoding="utf-8") as f:
            f.write(ce_plans[i])

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

    print(project_dirs)
    print(user_req)

    for i in range(len(project_dirs)):
        print("# # # # # # # # # # # # " + project_dirs[i])
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

        # m_0, ask llm to analyze the unit test result
        PROMPT_FOR_TEST_ANA = """You are a software test analyst. Please help me analyze the code of a project.
        Here is the entire codebase for a project: {code_base}.
        Here are the unit test codes for this project: {unit_test_code}.
        These are all the unit test results (only including the failed ones):{test_results}
        
        Please analyze the test results one by one. For each unit test result, analyze step by step to identify the reasons for the test failure."""
        messages.append(format_prompt(PROMPT_FOR_TEST_ANA, values))
        unit_test_result_analysis = chat_to_LLM(messages)

        log.info(messages[0]["content"])
        print(unit_test_result_analysis)
        print("\n###################################")

        # 2. judge if any of the issues is caused by code (rather than other unrelated reasons)
        # m_1, llm's response(unit test result)
        messages.append({"role": "assistant", "content": unit_test_result_analysis})
        log.info(str(messages[1]))
        # m_2, ask llm to decide if the issues is from code
        messages.append(
            {
                "role": "user",
                "content": "Do you think the issue is caused by errors in the project's code or poorly written test cases? If it is a code error, please include a [CODE] at the end of your output. If not, you don't need to add anything. Thank you.",
            }
        )
        log.info(str(messages[2]))
        relevance = chat_to_LLM(messages)

        if "[CODE]" not in relevance:
            continue

        print(relevance)
        print("\n###################################")

        # 3. summarize the code feedback
        # m_3, llm's response(whether from code)
        messages.append({"role": "assistant", "content": relevance})
        log.info(str(messages[3]))
        # m_4, ask llm to summarize the unit test result
        messages.append(
            {
                "role": "user",
                # "content": "summarize the issues in this project's code based on all the unit test results. Only neIssues about the test codes is not needed to analyze.   ",
                "content": """Summarize the above mentioned issues or errors. You only need to summarize the issues or errors in the project identified from the unit test result. 
                Attention: The issues must be exclusively those highlighted by the unit tests; areas that may need improvement (e.g., performance or security concerns) but pass the unit tests should be excluded. Besides, issues result from the test codes is not needed to analyze, only analyze issues that are relevant to the project's own code.
                Then, you need to provide guidance(Needs to be concise and summarative) for improvement. The guidance you provide should adhere to the following aspects:
                (1) Be concise and general in nature.
                (2) Must offer insights based on issues revealed by unit tests, highlighting points to watch for when developing the project again.
                (3) Ideally, provide guidance at the level of pseudo-code or a planning framework, rather than addressing simple code-related issues. """,
            }
        )

        code_feedback = chat_to_LLM(messages)
        log.info(code_feedback)
        print(code_feedback)
        print("\n###################################")

        # 4. scoring the unit test result issues (0~10)
        # m_5, llm's response(issues summary)
        messages.append({"role": "assistant", "content": code_feedback})

        values_scoring = {
            "user_req": user_req,
        }
        # m_6, ask the llm to score
        PROMPT_FOR_SCORING = """
        Next, step to step, analyze the issues mentioned above and assess the extent to which these issues hinder the code from perfectly fulfilling the user requirements. Assign a score (0-10) based on the significance of the issues, where 0 indicates the issue has minimal impact or is unlikely to occur during coding, and 10 indicates the issue has a major impact or is highly likely to occur during coding.
        the user requirement is:{user_req}.
        At the end of your output, you need to display the average score(also range from 0 to 10), using the following format:[END]score[END], where "score" should be replaced with the score you have assigned.
        example:[END]5.0[END]"""
        messages.append(format_prompt(PROMPT_FOR_SCORING, values_scoring))
        # m_7, llm's response(score)
        score_result = chat_to_LLM(messages)
        log.info(str(score_result))
        print(score_result)
        print("\n###################################")

        start_tag = "[END]"
        end_tag = "[END]"
        start_index = score_result.find(start_tag) + len(start_tag)
        end_index = score_result.find(end_tag, start_index)

        # 提取出的内容
        score = float(score_result[start_index:end_index])
        # _________________ ask LLM to get feedback ________________

        if score > max_score:
            max_score = score
            code_feedback_selected = code_feedback

    print("final selected:\n" + code_feedback_selected)
    log.info("final selected:\n" + code_feedback_selected)

    return max_score, code_feedback_selected
    # return code_feedback


if __name__ == "__main__":
    ceaug()
