import dashscope
from datetime import datetime
import argparse
from pathlib import Path
import copy

from utils.commen import read_yaml
from agents.team import Team

from agents import *
from model.model import Qwen, GPT, GPT_topP

from langchain_openai import ChatOpenAI

import json
import os
import re
import argparse


def start_project():
    # __________ from shell __________
    parser = argparse.ArgumentParser(description="original Requirement")
    parser.add_argument("--category", type=str, help="gui")
    parser.add_argument("--name", type=str, help="DailyHealthTips.md")
    parser.add_argument("--seq", type=str, help="1")
    args = parser.parse_args()
    category = args.category
    name = args.name

    # specification for different running time
    seq = args.seq

    match = re.match(r"^(.*)\.md$", name)

    if match:
        project_name = match.group(1)
        print("|| Project Name: " + project_name + " ||")
    # __________ from shell __________

    # ______________ project soft config ________________

    # dataset dir
    project_description_path = (
        # f"D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\dataset\\{category}/{name}"
        f"D:\Project\ATEdev\ATEDev_main\\dataset\\SD-bench\\dataset\\{category}\\{name}"
    )
    # test case dir
    test_cases_dir = "D:\Project\ATEdev\ATEDev_main\\dataset\\SD-bench\\testcase"

    # project dir
    projdir = (
        "D:\\Project\\ATEdev\\ATEDev_main\\project\\"
        + category
        + "\\"
        + project_name
        + "\\"
    )

    # exploration numbers
    explore_num = 2
    #
    # ______________ project soft config ________________

    # framework execution start time
    start_time = datetime.now()
    formatted_time = start_time.strftime("%Y%m%d%H%M%S")

    ### 读取project_description_path中的md文件内容至project_description
    with open(project_description_path, "r", encoding="utf-8") as file:
        project_description = file.read()

    # Build Agent's Team
    origin_req = project_description
    team = Team()
    team.explore_num = explore_num
    team.test_cases_dir = test_cases_dir
    Team.projec_catogory = category
    Team.project_name = project_name

    Team.set_projdir(projdir)
    Team.set_log()

    # config for framework
    config = model_config()

    # normal model
    # config temperature only (fixed 0.2)
    model = GPT(config["llm_4o"])

    # -------------- sample model ----------------
    # [model 1] (with no config for top P)
    # sample_model_config = create_config_copy_with_new_temperature(
    #     config["llm_4o"], config["llm_4o"]["programmer_temperature"]
    # )
    # sample_model = GPT(sample_model_config)

    # [model 2] (config top p)
    # 自己配温度和top p
    sample_model = GPT_topP(config["llm_4o"])
    # --------------- sample model----------------

    # launch project
    team.set_origin_req(project_name, origin_req)

    # 创建不同的角色
    product_manager = Product_Manager(llm=model, llm_sample=sample_model, team=team)
    architect = Architect(llm=model, llm_sample=sample_model, team=team)
    projct_manager = Project_Manager(llm=model, llm_sample=sample_model, team=team)
    programmer = Programmer(llm=model, llm_sample=sample_model, team=team)
    code_tester = Code_Tester(llm=model, team=team)
    reviewer = Reviewer(target=projct_manager, team=team)
    searcher = Searcher(llm=model, team=team)

    # this is a normal programmer, don't need to change temperature
    c_programmer = C_Programmer(llm=model, team=team)

    team.hire_roles(
        product_manager,
        architect,
        projct_manager,
        programmer,
        code_tester,
        reviewer,
        searcher,
        c_programmer,
    )

    # 正常情况 不测试gui和game，或者一些特殊情况
    # 都走这个分支
    # 类似于这种命令 python start_by_file.py --category website --name MovieRecommendationSystem.md （没有seq参数）
    if not seq:
        if category == "website":
            team.run_web()
        else:
            team.run()
    elif seq:
        # team.run()
        team.run_vice(seq)

    # team.run_self_evo()
    # ------------------- launch project ------------------------
    #
    #
    # ------------------- Post Processing --------------------
    # statistics for this process(include team statistics and other information)
    # framework execution end time
    end_time = datetime.now()
    execution_time = end_time - start_time
    total_seconds = execution_time.total_seconds()
    milliseconds = int((total_seconds % 1) * 1000)
    milliseconds_str = str(milliseconds // 10).zfill(2)
    formatted_time = f"{int(total_seconds)}.{milliseconds_str}"
    Team.log.info(
        "\n-----------------\n"
        + team.log_project_stat()
        + "\n-------------------\n"
        + "Execute time: "
        + str(formatted_time)
        + " Seconds"
        + "\n-----------------"
    )
    # ------------------- Post Processing --------------------
    print(
        "\n-----------------\n"
        + team.log_project_stat()
        + "\n-------------------\n"
        + "Execute time: "
        + str(formatted_time)
        + " Seconds"
        + "\n-----------------"
    )


def create_config_copy_with_new_temperature(
    config: dict, new_temperature: float
) -> dict:
    """
    Args:
        config:
        new_temperature:

    Returns:

    """
    config_copy = copy.deepcopy(config)

    # 修改副本中的温度
    if "temperature" in config_copy:
        config_copy["temperature"] = new_temperature

    return config_copy


def model_config():
    # loading config for different models, include Qwen and GPT
    config = read_yaml("./0_config/config.yaml")
    dashscope.api_key = config["Qwen"]["api_key"]
    return config


if __name__ == "__main__":
    start_project()
