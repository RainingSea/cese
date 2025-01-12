import os
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from prompt.write_architect_prompt import (
    WRITE_ARCHITECT_SYS,
    WRITE_ARCHITECT,
    WRITE_ARCHITECT_WITH_FDBACK,
)
from prompt.align_prompt import ARCHITECTURE_REVIEW_PROJECT_PLAN, ARCHITECTURE_CODE
from agents.role import Role
from agents.team import Team
from messages.message import Message


from utils.read import read_file_2_line


class Architect(Role):
    name: str = "Arnold"
    profile: str = "Architect"
    llm: object
    llm_sample: object
    system_msg: str = WRITE_ARCHITECT_SYS
    own_message: Message = None
    team: Team = None
    review_prompt: dict[str, str] = {
        "Project Manager": ARCHITECTURE_REVIEW_PROJECT_PLAN,
        "Programmer": ARCHITECTURE_CODE,
    }
    action: str = "Architecture"

    def getMessage():
        pass

    def go(self):
        print(self.profile + " " + self.name + " generate Architect......")
        Team.log.info(
            self.profile + " " + self.name + " generate System Architect......"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        original_requirement = self.getOriginRequirement().content
        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_ARCHITECT)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        result = self.llm.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)

        return

    def go_in_sample(self):
        print(
            self.profile + " " + self.name + " generate Architect variable temperature"
        )
        Team.log.info(
            self.profile + " " + self.name + " generate Architect variable temperature"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        original_requirement = self.getOriginRequirement().content
        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        user_prompt_template = ChatPromptTemplate.from_template(WRITE_ARCHITECT)
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        result = self.llm_sample.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)
        return

    def go_with_fdback(self, feedback):
        print(self.profile + " " + self.name + " generate Architect with feedback")
        Team.log.info(
            self.profile + " " + self.name + " generate Architect with feedback"
        )

        # ---------- get the information needed from SCR ----------
        functional_requirement = self.getPRD().content
        original_requirement = self.getOriginRequirement().content
        # ---------- constructing prompt to LLM ----------
        # using message template from LangChain, the result is SYS Message & HUMAN Message.
        user_prompt_template = ChatPromptTemplate.from_template(
            WRITE_ARCHITECT_WITH_FDBACK
        )
        user_prompt_msg = user_prompt_template.invoke(
            {
                "original_requirement": original_requirement,
                "functional_requirement": functional_requirement,
                "ce_feedback": feedback,
            }
        )
        user_prompt = user_prompt_msg.to_messages()[0]

        system_prompt = SystemMessage(content=self.system_msg)

        # ---------- prompt LLM ----------
        Team.log.info(system_prompt.content + "\n" + user_prompt.content)
        result = self.llm.invoke(system_prompt, user_prompt)

        # ------------ logging ----------
        Team.log.info(self.profile + " " + self.name)
        Team.log.info(result)

        # ---------- adding result to SCR(before align) ----------
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        self.update_scr(module_msg)

        # ---------- writing result to local ----------
        self.message_to_file(module_msg.content)
        return

    def update_scr(self, message):
        """
        update team's shared certificated repository, with generated architecture
        """
        if len(Team.all_messages) < 3:
            # indicate that no new architecture
            Team.all_messages.append(message)
        else:
            # the other teams document
            Team.log.info("already a architect, replace it")
            Team.all_messages[2] = message

    def update_own_message(self, msg: Message):
        self.own_message = msg
        Team.all_messages[2] = msg

    def message_to_file(self, msg_content):
        # ---------- writing Architecture to local ----------
        file_name = "architect.md"

        Team.log.info(self.profile + " writting ARCHITECT")
        super().save_file_overwrite(
            os.path.join(Team.project_dir, file_name), msg_content
        )

    def getOriginRequirement(self):
        return Team.all_messages[0]

    def getPRD(self):
        return Team.all_messages[1]

    def go_inter(self):
        # 从项目dir里读取，并且加到自己的
        print(self.profile + " " + self.name + " extracting Architect......")
        Team.log.info(self.profile + " " + self.name + " extracting Architect......")
        result = read_file_2_line(Path(Team.incremental_base_dir) / "architect.md")
        if not os.path.exists(os.path.join(Team.project_dir, "architect.md")):
            self.message_to_file(result)
        module_msg = Message(sender=self.profile, content=result)
        self.own_message = module_msg
        # not perfect for now
        if len(Team.all_messages) <= 2:
            Team.all_messages.append(module_msg)
        else:
            Team.all_messages[2] = module_msg
