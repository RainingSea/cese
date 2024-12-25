import os
import re
import json
import ast
from pydantic import Field
from pathlib import Path

# langchain lib
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# project's utility lib
from utils.commen import str_to_role

# custom lib
from prompt.retrieval_prompt import RETRIEVAL_SYS, RETRIEVAL

from agents.role import Role
from agents.team import Team
from messages.message import Message
from utils.read import read_file_2_line


class Searcher:

    def __init__(self, llm, team=None):
        self.name: str = "Shinichi"
        self.profile: str = "Searcher"
        self.system_msg: str = RETRIEVAL_SYS
        self.llm: object = llm
        self.team: Team = team  # 使用传入的参数
        self.action: str = "Retrieval"

    def retrieval(self, task_description):

        # get task to retrieval
        # task_description = task_description

        # get PRD
        prd = self.getPRD().content
        original_req = self.getOriginalDescription().content

        # by default, retrieval is performed on the PRD.
        system_prompt = SystemMessage(content=RETRIEVAL_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(RETRIEVAL)
        user_prompt_msg = user_prompt_template.invoke(
            {"prd": prd, "user_demand": original_req, "task": task_description}
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        retrieval_result = self.llm.invoke(system_prompt, user_prompt)
        # ---------- logging --------
        Team.log.info("\n" + retrieval_result)
        return retrieval_result

    def getOriginalDescription(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def getArchiture(self):
        return Team.all_messages[2]

    def getProjectPlan(self):
        return Team.all_messages[3]
