from openai import OpenAI

inputs = """I love
"""


def chat_to_LLM(messages):

    client = OpenAI(
        api_key="sk-nF4KFp0FggnT6bfpH2JwYhRsFWnPpfohEAtERbHlMXCIdlki",  # 只需要填写key就可以了
        base_url="https://api.chatanywhere.tech",
    )
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        top_logprobs=
        # stream=True, # 这个开了要用chunk的调用方法
    )
    # print(response.choices[0].message.content, end="", flush=True)
    return response.choices[0].message.content


if __name__ == "__main__":
    messages = [{"role": "user", "content": inputs}]
    print(chat_to_LLM(messages))
