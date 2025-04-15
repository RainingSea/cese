import os
import chardet
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from prompt.write_prd_prompt import WRITE_PRD, WRITE_PRD_SYS
from prompt.meta_prompt import META_PROMPT

from agents.role import Role
from agents.team import Team
from messages.message import Message
from utils.read import read_file_2_line

from utils.commen import write_to_file


class Product_Manager(Role):
    name: str = "Pole"
    profile: str = "Product Manager"
    team: Team = None
    llm: object
    llm_sample: object
    system_msg: str = WRITE_PRD_SYS
    own_message: Message = None
    action: str = "functional requirement document"

    def go(self):
        print(self.profile + " " + self.name + " generate PRD......")
        Team.log.info(self.profile + " " + self.name + " Writing PRD...")

        # ---------- get the information needed from SCR ----------
        original_requirement = self.getOriginRequirement().content

        # ---------- use metaprompt to let LLM write prompt to generate PRD
        meta_prompt_tplt = ChatPromptTemplate.from_template(META_PROMPT)
        meta_prompt_prompt = meta_prompt_tplt.invoke(
            {
                "role_input": "original_requirement",
                "role_output": "functional requirements",
            }
        )
        meta_prompt_msg = meta_prompt_prompt.to_messages()[0]
        result = self.llm.invoke(meta_prompt_msg)

        Team.log(result)
        return

        # ---------- constructing prompt to LLM ----------
        system_prompt = SystemMessage(content=WRITE_PRD_SYS)
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_PRD)
        user_prompt_msg = user_prompt_template.invoke(
            {"original_requirement": original_requirement}
        )
        user_prompt = user_prompt_msg.to_messages()[0]
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        # prompt LLM
        result = self.llm.invoke(system_prompt, user_prompt)

        # ---------- logging -----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        prd_msg = Message(sender=self.profile, content=result)
        self.own_message = prd_msg

        Team.all_messages.append(prd_msg)
        # ---------- writing result to local ----------
        self.message_to_file(prd_msg.content)

        return

    def message_to_file(self, msg_content):
        # # ---------- writing PRD to local ----------
        file_name = "prd.md"

        # log.info(self.profile + " writting PRD")
        super().save_file_overwrite(Team.project_dir + file_name, msg_content)

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[1] = msg

    def get_team_roles(self):
        return self.team.get_team_roles()

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def setSuggestion(self, suggestion):
        self.suggestion = suggestion

    def clearSuggestion(self):
        self.suggestion = ""

    def test(self):
        Team.arthur_talk(self)

    def go_inter(self):
        # 从项目dir里读取，并且加到自己的
        print(self.profile + " " + self.name + " extracting PRD......")
        Team.log.info(self.profile + " " + self.name + " extracting PRD......")
        result = read_file_2_line(Path(Team.incremental_base_dir) / "prd.md")
        if not os.path.exists(os.path.join(Team.project_dir, "prd.md")):
            self.message_to_file(result)
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        # not perfect for now
        if len(Team.all_messages) <= 1:
            Team.all_messages.append(module_msg)
        else:
            Team.all_messages[1] = module_msg
