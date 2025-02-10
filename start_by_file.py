import dashscope
from datetime import datetime
import argparse
from pathlib import Path
import copy

from utils.commen import read_yaml
from agents.team import Team


# the __init__ of the agents folder has already imported the class, there's no need to write additional class import statements.
from agents import *
from model.model import Qwen, GPT, GPT_topP

from langchain_openai import ChatOpenAI

import json
import os
import re
import argparse


def start_project():
    # _________ from run ___________
    # category = "website"
    # name = "BookWormSearch.md"
    # _________ from run ___________

    # __________ from shell __________
    parser = argparse.ArgumentParser(description="original Requirement")
    parser.add_argument("--category", type=str, help="gui")
    parser.add_argument("--name", type=str, help="DailyHealthTips.md")
    parser.add_argument("--seq", type=str, help="1")
    args = parser.parse_args()
    category = args.category
    name = args.name
    # game and gui specification
    seq = args.seq

    match = re.match(r"^(.*)\.md$", name)
    if match:
        project_name = match.group(1)
        print(project_name)
    # __________ from shell __________

    # project_description_path = f"./dataset/rSDE_Bench/inference/dataset/{category}/{name}"
    project_description_path = (
        # f"D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\dataset\\{category}/{name}"
        f"D:\\Project\\CE\\CE\\dataset\\SD-bench\\dataset\\{category}\\{name}"
    )

    explore_num = 5
    test_cases_dir = "D:\\Project\\CE\\CE\\dataset\\SD-bench\\testcase"

    projdir = "D:/Project/CE/CE/project/" + category + "/" + project_name + "/"

    # web项目实际上还要配一个port.txt路径
    # 但是我改成相对路径了，暂时可以使用，不用再配了

    # framework execution start time
    start_time = datetime.now()
    formatted_time = start_time.strftime("%Y%m%d%H%M%S")

    ### 读取project_description_path中的md文件内容至project_description
    with open(project_description_path, "r", encoding="utf-8") as file:
        project_description = file.read()
    origin_req = project_description
    # Build Agent's Team
    team = Team()
    team.explore_num = explore_num
    team.test_cases_dir = test_cases_dir
    Team.projec_catogory = category
    Team.project_name = project_name

    # projdir = (
    #     "D:/Project/CE/CE/project/"
    #     + category
    #     + "/"
    #     + project_name
    #     + "_"
    #     + formatted_time
    #     + "/"
    # )

    # projdir = "D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\" + project_name + "\\"
    Team.set_projdir(projdir)
    Team.set_log()

    # woRTA
    Team.align_check_num = 0
    Team.mad_num = 0

    # config for framework
    config = model_config()

    # normal temperature model
    model = GPT(config["llm_4o"])

    # sampling model with changed temperature
    sample_model_config = create_config_copy_with_new_temperature(
        config["llm_4o"], config["llm_4o"]["programmer_temperature"]
    )
    # sample_model = GPT_topP(config["llm_4o"])
    sample_model = GPT(sample_model_config)
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

    # 设置探索次数
    #
    #
    # team.run()现在暂时只生成代码和testcode，测试以及根据测试的反馈重新生成都被分别拆开来
    # ------------------- launch project ------------------------

    # ———————————————————————————— 纯生成版 ————————————————————————————————
    # team.run_pure()
    # end_time = datetime.now()
    # execution_time = end_time - start_time
    # total_seconds = execution_time.total_seconds()
    # milliseconds = int((total_seconds % 1) * 1000)
    # milliseconds_str = str(milliseconds // 10).zfill(2)
    # formatted_time = f"{int(total_seconds)}.{milliseconds_str}"
    # Team.log.info(
    #     "\n-----------------\n"
    #     + team.log_project_stat()
    #     + "\n-------------------\n"
    #     + "Execute time: "
    #     + str(formatted_time)
    #     + " Seconds"
    #     + "\n-----------------"
    # )
    # # ------------------- Post Processing --------------------
    # print(
    #     "\n-----------------\n"
    #     + team.log_project_stat()
    #     + "\n-------------------\n"
    #     + "Execute time: "
    #     + str(formatted_time)
    #     + " Seconds"
    #     + "\n-----------------"
    # )
    # return
    # ———————————————————————————— 纯生成版 ————————————————————————————————
        
    if not seq:
        if category == "website":
            #     print("WEBWEB")
            # team.run_vice(seq)
            # team.run_web_iterative()
            team.run_web()
        else:
            team.run()
    elif seq:
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
