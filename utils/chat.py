from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

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
        top_p=0.1,
        seed=42,
        # stream=True, # 这个开了要用chunk的调用方法
    )
    # print(response.choices[0].message.content, end="", flush=True)
    return response.choices[0].message.content


def chat_to_LLM_langchain():
    a = HumanMessage(content="Hello!")
    model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key="sk-nF4KFp0FggnT6bfpH2JwYhRsFWnPpfohEAtERbHlMXCIdlki",
        base_url="https://api.chatanywhere.tech",
        model_kwargs={"top_p": 1.2},
    )
    print(model.invoke([a]))


if __name__ == "__main__":
    messages = [{"role": "user", "content": inputs}]
    print(chat_to_LLM(messages))

    # chat_to_LLM_langchain()
