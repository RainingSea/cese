from openai import OpenAI
from utils.read import read_codebase
from ceaug.auto_test import *
from ceaug.auto_test_prompt import PROMPT_FOR_TEST_ANA


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


def ceaug():
    # 获取代码仓库
    # 默认操作code文件夹
    project_dir = "D:\Project\Align\models\RTADev\Altdev\project\game\WordLinkPuzzle"

    code_base = read_codebase(os.path.join(project_dir, "code"))
    # 编写测试代码并保存在code文件夹中
    test_code = autogen(project_dir)

    # 运行测试代码，并保存结果在一个log文件中
    unit_test_result = runUnitTest(project_dir)
    print(unit_test_result["output"])

    ## ask LLM
    values = {
        "code_base": code_base,
        "unit_test_code": test_code,
        "test_results": unit_test_result["output"],
    }
    messages = []
    messages.append(format_prompt(PROMPT_FOR_TEST_ANA, values))

    feedback = chat_to_LLM(messages)
    print(feedback)
    print()
    messages.append({"role": "assistant", "content": feedback})
    messages.append(
        {
            "role": "user",
            "content": "Do you think the issue is caused by errors in the project's code or poorly written test cases? If it is a code error, please include a [CODE] at the end of your output. If not, you don't need to add anything. Thank you.",
        }
    )
    feedback = chat_to_LLM(messages)
    print(feedback)
    print()
    messages.append({"role": "assistant", "content": feedback})
    messages.append(
        {
            "role": "user",
            "content": "summarize the issues in this project's code based on all the unit test results. Issues about the test codes is not needed to analyze.",
        }
    )
    feedback = chat_to_LLM(messages)
    print(feedback)
    print()


if __name__ == "__main__":
    ceaug()
